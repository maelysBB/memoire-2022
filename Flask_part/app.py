from flask import Flask, redirect, url_for, render_template, jsonify, request, session
import folium
import shapely.wkt
import pandas as pd
import geopandas as gpd
import requests
from converter import test, compare
from choices import category, name_cat



app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
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
    # return "works"

@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

@app.route('/fonctionne')
def fonctionne():
    return render_template('fonctionne.html')

@app.route('/map')
# @app.route('/map/<result>')
def map(result = None):
    start_coords = (48.5, 2.3360300)
    folium_map = folium.Map(location=start_coords, zoom_start=9)
    return folium_map._repr_html_()
        
@app.route('/update_map')
# @app.route('/update_map/<query>')
def update_map():
    data =  request.args.values()
    start_coords = (48.7, 2.3360300)
    folium_map = folium.Map(location=start_coords, zoom_start =10)
    data = [eval(d) for d in data][0]
    checkboxes = data["checkboxes"]
    inputs =  data["inputs"]    
    free_field = {}
    if len(inputs) > 0 :
        for key, value in inputs.items():
            free_field[key.replace("name_","")] = value
    result = test(checkboxes, free_field)
    folium.GeoJson(result).add_to(folium_map)
    return folium_map._repr_html_()
    # return jsonify(result)


@app.route('/update_map_api', methods = ["POST"])
# @app.route('/update_map/<query>')
def update_map_api():
    data = request.get_json()
    start_coords = (48.7, 2.3360300)
    folium_map = folium.Map(location=start_coords, zoom_start =10)
    # data = [eval(d) for d in data][0]
    checkboxes = data["checkboxes"]
    inputs =  data["inputs"]    
    free_field = {}
    if len(inputs) > 0 :
        for key, value in inputs.items():
            free_field[key.replace("name_","")] = value
    result = test(checkboxes, free_field).to_json()
    return jsonify(result)

    
if __name__ == "__main__":
    app.run(debug=True)