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
import json


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
    distance= data['distance']
    url = f"https://my-deployment-8a262e.es.us-central1.gcp.cloud.es.io/area{distance}/_search"
    free_field = {}
    if len(inputs) > 0 :
        for key, value in inputs.items():
            free_field[key.replace("name_","")] = value
    result =  test(url, checkboxes, free_field)
        # result =  test(url, checkboxes, free_field)[1].to_json()

    # result_0 = {"test": {result[0]}}.to_json()
    # from jsonmerge import merge
    result = {1: result[0].to_json(), 2: result[1]}
    # json.loads(result)
    # result1 = .to_json()

    if len(checkboxes)==0:
        return folium_map._repr_html_()
    # return jsonify(result[0].to_json()), result[1]
    return result



# *** Deuxième application

@app.route('/app2')
def app2():
    list_of_choices =  category
    return render_template(
        'index_app2.html', list_of_choices = list_of_choices)
    
@app.route('/predict_app2', methods=['GET', 'POST'])
def predict_app2():
    #Extraction des informations saisies par l'utilisateur
    input_data = list(request.form.values())
    input_data=list(map(int, input_data))
    input_values = [x for x in input_data]
    arr_val = np.array(input_values)
    print(input_data)

    #Préparation des données polygones 
    data = pd.read_csv("polygon_radius_complete.csv")
    sample = data[data["Nb lieux"] != 0].loc[:, "shop_craft_office" : "fuel"]

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
    Dans cette zone,se trouvent <b>%s</b> commerce(s), <b>%s</b> restaurant(s),<br> 
    <b>%s</b> cinéma(s), <b>%s</b> bibliothèque(s), <b>%s</b> aire(s) de jeux,<br> 
    <b>%s</b> installation(s) sportive(s), <b>%s</b> jardin(s), <b>%s</b> lieu(x) historique(s),<br> 
    <b>%s</b> hébergement(s), <b>%s</b> école(s), <b>%s</b>  lieu(x) de santé,<br> 
    <b>%s</b> banque(s), <b>%s</b> service(s) public(s), <b>%s</b> toilette(s),<br> 
    <b>%s</b> station(s) d'eau potable, <b>%s</b> défibrillateur(s),<br> 
    <b>%s</b> équipement(s) anti-incendie, <b>%s</b> station(s) de covoiturage, <br>
    <b>%s</b> parking(s), <b>%s</b> borne(s) de chargement, <br>
    <b>%s</b> station(s) de taxi et <b>%s</b> station(s) essence
    """ % (top['shop_craft_office'].iloc[i], top['cinema'].iloc[i], top['restaurant'].iloc[i],
    top['library'].iloc[i], top['playground'].iloc[i], top['sports'].iloc[i],top['allotments'].iloc[i], 
    top['historic'].iloc[i], top['hosting'].iloc[i], top['education'].iloc[i],
    top['healthcare'].iloc[i], top['bank'].iloc[i], top['public_service'].iloc[i],
    top['toilets'].iloc[i], top['drinking_water'].iloc[i], top['aed'].iloc[i],
    top['fire_hydrant'].iloc[i], top['carpool'].iloc[i], top['parking'].iloc[i],
    top['charging_station'].iloc[i], top['taxi'].iloc[i],
    top['fuel'].iloc[i])
            folium.Circle(location=[top['lat'].iloc[i], top['lon'].iloc[i]],
                    radius=1000,
                    tooltip=popup1,
                    color='#FFBA00',
                    fill_color='#FFBA00',
                    fill=True).add_to(carte)
        else:
            popup2 = """
    Ce n'est pas un match parfait !<br>
        Dans cette zone,se trouvent <b>%s</b> commerce(s), <b>%s</b> restaurant(s),<br> 
    <b>%s</b> cinéma(s), <b>%s</b> bibliothèque(s), <b>%s</b> aire(s) de jeux,<br> 
    <b>%s</b> installation(s) sportive(s), <b>%s</b> jardin(s), <b>%s</b> lieu(x) historique(s),<br> 
    <b>%s</b> hébergement(s), <b>%s</b> école(s), <b>%s</b>  lieu(x) de santé,<br> 
    <b>%s</b> banque(s), <b>%s</b> service(s) public(s), <b>%s</b> toilette(s),<br> 
    <b>%s</b> station(s) d'eau potable, <b>%s</b> défibrillateur(s),<br> 
    <b>%s</b> équipement(s) anti-incendie, <b>%s</b> station(s) de covoiturage, <br>
    <b>%s</b> parking(s), <b>%s</b> borne(s) de chargement, <br>
    <b>%s</b> station(s) de taxi et <b>%s</b> station(s) essence
    """ % (top['shop_craft_office'].iloc[i], top['cinema'].iloc[i], top['restaurant'].iloc[i],
    top['library'].iloc[i], top['playground'].iloc[i], top['sports'].iloc[i],top['allotments'].iloc[i], 
    top['historic'].iloc[i], top['hosting'].iloc[i], top['education'].iloc[i],
    top['healthcare'].iloc[i], top['bank'].iloc[i], top['public_service'].iloc[i],
    top['toilets'].iloc[i], top['drinking_water'].iloc[i], top['aed'].iloc[i],
    top['fire_hydrant'].iloc[i], top['carpool'].iloc[i], top['parking'].iloc[i],
    top['charging_station'].iloc[i], top['taxi'].iloc[i],
    top['fuel'].iloc[i])
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