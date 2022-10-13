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

item_translator = { "healthcare0" : "Hopital", "healthcare1": "Pharmacie", "healthcare2": "Cabinet Médical et Clinique", "charging_station": "charging_station"}
 
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
                      }
                    }
  data = {"size": 10}
  data["query"] = {"bool": {"must": []}}
  

  for key, value in user_demand.items() :
    if total_number[key] == value["number"] : ##si l'tuilsateur a choisi tous les lieux du type, ou qu'il n'y a qu'une seule  catégorie on fait une requête existe
        to_append = {"nested": {"path": key ,"query": {"exists": {"field": key}}}} 
        data["query"]["bool"]["must"].append(to_append)
        
    else:
      if total_number[key] > 1 :    
        for cat in value["category"]: ##si l'tuilsateur a choisi certaines catégorie, on fait une query avec must, pour que cela réponde aux différentes catégorie
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

