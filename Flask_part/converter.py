from elasticsearch import Elasticsearch
import requests
import folium
import shapely.wkt
import pandas as pd
import geopandas as gpd
import requests
import re
from choices import category
import configparser
import random


config = configparser.ConfigParser()
config.read('example.ini')



item_translator = { "healthcare0" : "Hopital", "healthcare1": "Pharmacie", "healthcare2": "Cabinet Médical et Clinique", "charging_station": "charging_station", 
                     "bank0": "Banque Postale", "bank1": "BNP Paribas", "bank2": "BRED/Banque populaire", "bank3": "Caisse d'Epargne", 
                    "bank4": "CIC", "bank5": "Crédit Agricole", "bank6": "Crédit Mutuel", "bank7": "HSBC", "bank8": "LCL", "bank9": "Société Générale", 
                    "carpool0": "Aire de covoiturage", "carpool1": "Parking", "cinema0": "MK2", "cinema1": "Pathé Gaumont", "cinema2": "UGC", "library0": "Bibliothèque", "library1": "Médiathèque", "library2": "Dépôt à livres", 
                    "shop_craft_office0": "Achat et entretien voitures", "shop_craft_office1": "Agence immobilière", "shop_craft_office2": "Boucher", 
                    "shop_craft_office3": "Boulangerie/Pâtisserie", "shop_craft_office4": "Café", "shop_craft_office5": "Coiffeur", 
                    "shop_craft_office6": "Opticien", "shop_craft_office7": "Supermarché/Epicerie", "shop_craft_office8": "Vêtements/Chaussures",
                    "allotments0": "Jardin", "allotments1": "Potager", "allotments2": "Géré par une association", "allotments3": "Autre", 
                    "education0": "Crèche", "education1": "Ecole primaire ou secondaire", "education2" :  "Enseignement supérieur hors université", "education3":  "Université", "fire_hydrant0": "Utiliser par tous", "fire_hydrant1": "Utiliser que par les pompiers",
                    "historic0": "Bâtiment", "historic1": "Château", "historic2": "Fontaine ou aménagement de cours d'eau", "historic3": "Industriel ", "historic4": "Lieu de culte", "historic5": "Monument", "historic6": "Mémorial", "historic7": "Naturel",
                    "historic8": "Patrimoine militaire", "historic9": "Patrimoine scientifique", "historic10": "Ruines", "historic11": "Site archeologique", "historic12": "Tombe", "historic13": "Transport", "historic14": "Autre",
                    "playground": "playground", "hosting0": "Hôtel", "hosting1":  "Maison d'hôte", "hosting2": "Espaces extérieur", "hosting3": "Autre",
                    "parking0": "Ouvrage", "parking1": "Enclos en surface", "sports0": "Aire de jeux", "sports1":  "Centre d'équitation", "sports2": "Complexe sportif", "sports3": "Equipement de fitness ou de gymnastique",
                    "sports4": "Piscine", "sports5": "Piste d'athlétisme", "sports6": "Stade", "sports7": "Terrain de golf", "sports8": "Terrain de sport", "sports9": "Autre", "drinking_water0": "Gratuit", "drinking_water1":  "Payant", "toilets0": "Gratuit", "toilets1":  "Payant",
                    "taxi": "taxi", "aed": "aed", "fuel": "Station de carburant", 
                    "toilets0": "Gratuit", "toilets1":"Payant", 
                    "restaurant0": "Bar ou Pub", "restaurant1": "Café", "restaurant2": "Glacier", "restaurant3": "Foire alimentaire", "restaurant4": "Restaurant Fast Food", "restaurant5": "Restaurant Français",  "restaurant6": "Restaurant Régional",
                    "restaurant7": "Restaurant Italien", "restaurant8": "Restaurant Japonais", "restaurant9": "Restaurant Indien","restaurant10": "Restaurant",
                    "public_service0": "Mairie ou Hôtel de ville","public_service1":"Organisme gouvernemental", "public_service2": "Service de conseil", "public_service3": "Diplomatique", "public_service4": "Autre",
                    
                    }
 
total_number = {}
for key, value in category.items() :
    if "category" in value :
        total_number[key] = len(value["category"])
    else :
        total_number[key] = 1
        
        
def compare(list_of_choices, word): #list of choices lists all the choice the users have made
    
    return [item_translator[x] for x in list_of_choices if re.search(word, x)] #return choices made by the user for a given category, the category is retrieve with the prefix (ex : healthcare1, charging_station etc) 
  

def test(url, result, free_input):
  user_demand ={}
  for key, value in category.items():
    if 'category' in value:
      user_demand[key] = {"number": len(compare(result, key)),
                   "category" : compare(result, key)}
    else : 
      user_demand[key] = {"number": len(compare(result, key))}
      
  data = {"size": 200}
  data["query"] = {"bool": {"must": []}}
  

  for key, value in user_demand.items() :
    if total_number[key] == value["number"] : ##si l'utilisateur a choisi tous les lieux du type, ou qu'il n'y a qu'une seule  catégorie on fait une requête existe
        to_append = {"nested": {"path": key ,"query": {"exists": {"field": key}}}} 
        data["query"]["bool"]["must"].append(to_append)
        
    else:
      if total_number[key] > 1 :    
        for cat in value["category"]: ##si l'utilisateur a choisi certaines catégories, on fait une query avec must, pour que cela réponde aux différentes catégorie
            to_append = {"nested": {"path": key,"query": {"bool": {"must": [{"match": { "{}.category".format(key): cat  }}] } }}}
            data["query"]["bool"]["must"].append(to_append)
  
  for key, value in free_input.items():
    if value != "":
    ##Permet de rechercher un champ libre saisi par le user
      to_append = {"nested": {
                          "path": key,
                          "query": {
                                  "bool": {
                                  "must": [
                                      { "match": { "{}.name_text".format(key) : value } }
                                  ]
                                  }
                              }
                              }
                          }
      data["query"]["bool"]["must"].append(to_append)

  print(data["query"])
  

  # sampling with replacement
  # k = number of items to select

  response  = requests.get(url, auth=(config['ELASTIC']['user'], config['ELASTIC']['password']), json = data)
   
  polygon = response.json()["hits"]["hits"]  
  polygon = random.choices(polygon, k=100)

  
  detail =  [{element["_id"]: element["_source"] } for element in polygon]
  # detail =  [element["_id"] for element in polygon]
  
  retrieve_centroid = [shapely.wkt.loads(element["_source"]["centroid"]) for element in polygon] #retrieve only the polygon coordinates of each doc. We apply wkt loads to convert to proper format
  geo_serie_c = gpd.GeoSeries(retrieve_centroid) #transform the list of polygons to a geoSerie
  geo_serie_c.crs = "epsg:4326"

  retrieve_polygons = [shapely.wkt.loads(element["_source"]["polygon"]) for element in polygon] #retrieve only the polygon coordinates of each doc. We apply wkt loads to convert to proper format
  geo_serie = gpd.GeoSeries(retrieve_polygons) #transform the list of polygons to a geoSerie
  geo_serie.crs = "epsg:4326"
  return geo_serie_c, polygon
  # return responsey
  # return data

