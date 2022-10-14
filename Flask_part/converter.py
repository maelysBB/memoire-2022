from elasticsearch import Elasticsearch
import requests
import folium
import shapely.wkt
import pandas as pd
import geopandas as gpd
import requests
import re
from choices import category

url = "http://localhost:9200/area1/_search"

item_translator = { "healthcare0" : "Hopital", "healthcare1": "Pharmacie", "healthcare2": "Cabinet Médical et Clinique", "charging_station": "charging_station", 
                    "aed0": "Intérieur", "aed1": "Extérieur", "bank0": "Banque Postale", "bank1": "BNP Paribas", "bank2": "BRED/Banque populaire", "bank3": "Caisse d'Epargne", 
                    "bank4": "CIC", "bank5": "Crédit Agricole", "bank6": "Crédit Mutuel", "bank7": "HSBC", "bank8": "LCL", "bank9": "Société Générale", 
                    "carpool0": "Aire de covoiturage", "carpool1": "Parking", "cemetery": "cemetery", "cinema0": "MK2", "cinema1": "Pathé Gaumont", "cinema2": "UGC", "cycleway": "cycleway", "library0": "Bibliothèque", "library1": "Médiathèque", "library2": "Dépôt à livres", "playground": "playground", 
                    "recycling": "recycling", "shop_craft_office0": "Achat et entretien voitures", "shop_craft_office1": "Agence immobilière", "shop_craft_office2": "Boucher", 
                    "shop_craft_office3": "Boulanger/Pâtisserie", "shop_craft_office4": "Café", "shop_craft_office5": "Coiffeur", 
                    "shop_craft_office6": "Opticien", "shop_craft_office7": "Supermarché/Epicerie", "shop_craft_office8": "Vêtements/Chaussures",
                    "allotments0": "garden", "allotments1": "Autre", "allotments2": "potager", "allotments3": "association", "bicycle_parking0": "prive", "bicycle_parking1": "libre acces", "bicycle_parking2": "Missing",
                    "education0": "kindergarten", "education1": "school", "education2" : "university","education3": "college", "fire_hydrant0": "utiliser_que_par_les_pompiers", "fire_hydrant1": "utiliser_par_tous",
                    "historic0":"memorial", "historic1": "nature", "historic2": "man-made_waterbody", "historic3": "place_of_worship", "historic4": "monument", "historic5": "tomb", "historic6": "castle","historic7": "ruins",
                    "historic8": "Autre", "historic9": "archaeological_site", "historic10": "building", "historic11": "industrial ", "historic12": "military", "historic13": "vehicle", "historic14": "scientific",
                    "hosting0": "hotel", "hosting1": "guest_house", "hosting2": "outdoor", "hosting3": "Autre", "internet_access0": "wlan", "internet_access1": "terminal", "internet_access2": "Autre",
                    "internet_access3": "wired", "internet_access4": "service_provider", "parking0": "Missing", "parking1": "ouvrage", "parking2": "enclos_en_surface", "sports0": "sports_centre", "sports1": "pitch",
                    "sports2": "horse_riding", "sports3": "swimming_pool", "sports4": "golf_course", "sports5": "fitness_station", "sports6": "recreation_ground", "sports7": "track", "sports8": "stadium", "sports9": "grass", "sports10": "Autre"
                    }
 
total_number = {}
for key, value in category.items() :
    if "category" in value :
        total_number[key] = len(value["category"])
    else :
        total_number[key] = 1
        
        
def compare(list_of_choices, word): #list of choices lists all the choice the users have made
    
    return [item_translator[x] for x in list_of_choices if re.search(word, x)] #return choices made by the user for a given category, the category is retrieve with the prefix (ex : healthcare1, charging_station etc) 
  

def test(result, free_input):
  user_demand ={}
  for key, value in category.items():
    if 'category' in value:
      user_demand[key] = {"number": len(compare(result, key)),
                   "category" : compare(result, key)}
    else : 
      user_demand[key] = {"number": len(compare(result, key))}
      
  data = {"size": 50}
  data["query"] = {"bool": {"must": []}}
  

  for key, value in user_demand.items() :
    if total_number[key] == value["number"] : ##si l'utilsateur a choisi tous les lieux du type, ou qu'il n'y a qu'une seule  catégorie on fait une requête existe
        to_append = {"nested": {"path": key ,"query": {"exists": {"field": key}}}} 
        data["query"]["bool"]["must"].append(to_append)
        
    else:
      if total_number[key] > 1 :    
        for cat in value["category"]: ##si l'utilsateur a choisi certaines catégories, on fait une query avec must, pour que cela réponde aux différentes catégorie
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
          
    response  = requests.get(url, json = data)
    polygon = response.json()["hits"]["hits"]
    retrieve_polygons = [shapely.wkt.loads(element["_source"]["polygon"]) for element in polygon] #retrieve only the polygon coordinates of each doc. We apply wkt loads to convert to proper format
    geo_serie = gpd.GeoSeries(retrieve_polygons) #transform the list of polygons to a geoSerie
    geo_serie.crs = "epsg:4326"
    return geo_serie
    # return response
    # return data

