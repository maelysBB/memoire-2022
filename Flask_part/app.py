from flask import Flask, redirect, url_for, render_template, jsonify, request, session
import folium
import shapely.wkt
import pandas as pd
import numpy as np
import geopandas as gpd
import requests
from converter import test, compare
from choices import category, name_cat
from mémoire_algorithme import difference, add




app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/app1')
def app1():
    list_of_choices =  category
    return render_template('index.html', list_of_choices = list_of_choices)
    
@app.route("/process_demand", methods=["POST"]) #Traite la demande du user
def process_demand():
    list_of_choices =  category
    session.clear()
    result = request.form.getlist("user_demand")
    free_field = {}
    for element in name_cat:
        free_field[element.replace("name_","")] = request.form.get(element)
    session['query'] = result
    session['free_field'] = free_field
    return render_template('index.html', result=result, list_of_choices = list_of_choices, free_field = free_field)

@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

@app.route('/fonctionne')
def fonctionne():
    return render_template('fonctionne.html')

@app.route('/set_map')
def set_map(result = None):
    start_coords = (48.5, 2.3360300)
    folium_map = folium.Map(location=start_coords, zoom_start=9)
    return folium_map._repr_html_()
        

@app.route('/update_map_api', methods = ["POST"])
def update_map_api():
    data = request.get_json()
    start_coords = (48.7, 2.3360300)
    folium_map = folium.Map(location=start_coords, zoom_start =10)
    checkboxes = data["checkboxes"]
    inputs =  data["inputs"]    
    free_field = {}
    if len(inputs) > 0 :
        for key, value in inputs.items():
            free_field[key.replace("name_","")] = value
    result = test(checkboxes, free_field).to_json()
    if len(checkboxes)==0:
        return folium_map._repr_html_()
    return jsonify(result)


# *** Deuxième application

@app.route('/app2')
def app2():
    return render_template(
        'index_app2.html',
        data=[{'banque': 0}, {'banque': 1}, {'banque': 2}, {'banque': 3}, {'banque': 4}, {'banque': 5}, {'banque': 6}, {'banque': 7}, {'banque': 8}, {'banque': 9}, {'banque': 10}],
        data1=[{'santé': 0}, {'santé': 1}, {'santé': 2}, {'santé': 3}, {'santé': 4}, {'santé': 5}, {'santé': 6}, {'santé': 7}, {'santé': 8}, {'santé': 9}, {'santé': 10}],
        data2=[{'cimetière': 0}, {'cimetière': 1}, {'cimetière': 2}, {'cimetière': 3}, {'cimetière': 4}, {'cimetière': 5}, {'cimetière': 6}, {'cimetière': 7}, {'cimetière': 8}, {'cimetière': 9}, {'cimetière': 10}],
        data3=[{'cinéma': 0}, {'cinéma': 1}, {'cinéma': 2}, {'cinéma': 3}, {'cinéma': 4}, {'cinéma': 5}, {'cinéma': 6}, {'cinéma': 7}, {'cinéma': 8}, {'cinéma': 9}, {'cinéma': 10}],
        data4=[{'jardin': 0}, {'jardin': 1}, {'jardin': 2}, {'jardin': 3}, {'jardin': 4}, {'jardin': 5}, {'jardin': 6}, {'jardin': 7}, {'jardin': 8}, {'jardin': 9}, {'jardin': 10}])

@app.route('/predict_app2', methods=['GET', 'POST'])
def predict_app2():
    #Extraction des informations saisies par l'utilisateur
    input_data = list(request.form.values())
    input_data=list(map(int, input_data))
    input_values = [x for x in input_data]
    arr_val = np.array(input_values)

    #Préparation des données polygones 
    data = pd.read_csv("polygon_radius_complete.csv")
    sample = data[data["Nb lieux"] != 0].loc[:, "banque" : "jardin"]

    #Application de la fonction qui calcule la différence entre chaque polygone et les réponses de l'utilisateur
    np_result = np.apply_along_axis(lambda x : difference(input_values, x), 1, sample.to_numpy())
    top = pd.DataFrame(np_result, columns=['diff'], index = sample.index).sort_values(by=['diff'])

    #Afficher tous les matchs parfaits et ajouter des matchs non parfaits jusqu'à max 10 locations
    if len(top[top['diff']==0])>10:
        top=top[top['diff']==0]
    else:
        top = pd.DataFrame(np_result, columns=['diff'], index = sample.index).sort_values(by=['diff']).head(10)

    #Ajouts des informations pour les polygones les plus similaires
    top=add(top, data)

    #Création de la carte
    carte=folium.Map(
        location=[48.866667, 2.3333]
    )

    #Ajout de cercles et de popups pour chaque polygone
    for i in range(0,len(top)):
        if top['diff'].iloc[i]==0:
            popup1 = """
    Ceci est un match parfait !<br>
    Nombre de <b>banque(s)</b> : <b>%s</b><br>
    Nombre de <b>santé(s)</b> : <b>%s</b><br>
    Nombre de <b>cimetière(s)</b> : <b>%s</b><br>
    Nombre de <b>cinéma(s)</b> : <b>%d</b><br>
    Nombre de <b>jardin(s)</b> : <b>%d</b><br>
    """ % (top['banque'].iloc[i], top['santé'].iloc[i], top['cimetière'].iloc[i],top['cinéma'].iloc[i],top['jardin'].iloc[i])
            folium.Circle(location=[top['lat'].iloc[i], top['lon'].iloc[i]],
                    radius=1000,
                    tooltip=popup1,
                    color='#FFBA00',
                    fill_color='#FFBA00',
                    fill=True).add_to(carte)
        else:
            popup2 = """
    Ce n'est pas un match parfait !<br>
    Nombre de <b>banque(s)</b> : <b>%s</b><br>
    Nombre de <b>santé(s)</b> : <b>%s</b><br>
    Nombre de <b>cimetière(s)</b> : <b>%s</b><br>
    Nombre de <b>cinéma(s)</b> : <b>%d</b><br>
    Nombre de <b>jardin(s)</b> : <b>%d</b><br>
    """ % (top['banque'].iloc[i], top['santé'].iloc[i], top['cimetière'].iloc[i],top['cinéma'].iloc[i],top['jardin'].iloc[i])
            folium.Circle(location=[top['lat'].iloc[i], top['lon'].iloc[i]],
                    radius=1000,
                    tooltip=popup2,
                    color='#087FBF',
                    fill_color='#087FBF',
                    fill=True).add_to(carte)

    carte.save('templates/map_update.html')
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)