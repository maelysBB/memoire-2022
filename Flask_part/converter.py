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
                    "shop_craft_office6": "Opticien", "shop_craft_office7": "Supermarché/Epicerie", "shop_craft_office8": "Vêtements/Chaussures"}
 
total_number = {}
for key, value in category.items() :
    if "category" in value :
        total_number[key] = len(value["category"])
    else :
        total_number[key] = 1
        
        
def compare(list_of_choices, word): #list of choices lists all the choice the users have made
    
    return [item_translator[x] for x in list_of_choices if re.search(word, x)] #return choices made by the user for a given category, the category is retrieve with the prefix (ex : healthcare1, charging_station etc) 
  

def test(result, free_input):
  user_demand = {"healthcare":
                  {
                   "number": len(compare(result, "healthcare")),
                   "category" : compare(result, "healthcare")},
                  "charging_station": 
                    {"number": 
                      len(compare(result, "charging_station"))
                      },
                  "aed":
                  {
                   "number": len(compare(result, "aed")),
                   "category" : compare(result, "aed")},
                  "bank":
                  {
                   "number": len(compare(result, "bank")),
                   "category" : compare(result, "bank")},
                  "carpool":
                  {
                   "number": len(compare(result, "carpool")),
                   "category" : compare(result, "carpool")},
                  "cemetery": 
                    {"number": 
                      len(compare(result, "cemetery"))
                      },
                  "cinema":
                  {
                   "number": len(compare(result, "cinema")),
                   "category" : compare(result, "cinema")},
                  "cycleway": 
                    {"number": 
                      len(compare(result, "cycleway"))
                      },
                  "library":
                  {
                   "number": len(compare(result, "library")),
                   "category" : compare(result, "library")},
                  "playground": 
                    {"number": 
                      len(compare(result, "playground"))
                      },
                  "recycling": 
                    {"number": 
                      len(compare(result, "recycling"))
                      },
                  "shop_craft_office":
                  {
                   "number": len(compare(result, "shop_craft_office")),
                   "category" : compare(result, "shop_craft_office")}
                    }
                    
  data = {"size": 100}
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
    # return data

