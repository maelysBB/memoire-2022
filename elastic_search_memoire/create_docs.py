from elasticsearch import Elasticsearch
from elasticsearch import helpers
import configparser
import pandas as pd
from run import distance

config = configparser.ConfigParser()
config.read('example.ini')


df = pd.read_csv(f"./csv_files/{distance}/areas_{distance}.csv")


es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)
print(es.info().body)


def doc_generator():
  df_iter = df.iterrows()
  for index, line in df_iter:
        yield {
                  "_index": f'area{distance}',
                    "_id" : f"{index}",
                  "_source": { 
                        "coordinates": 
                        {"x": line["Row"], 
                        "y":  line["Column"]},
                        "centroid": line["centroid"],
                        "polygon": line["radius"], 
                        "healthcare": [], 
                        "charging_station": [],
                        "drinking_water":[],
                        "aed": [],
                        "bank":[],
                        "carpool": [],
                        "cemetery":[],
                        "cinema": [],
                        "cycleway":[],
                        "library": [],
                        "playground":[],
                        "recycling": [],
                        "shop_craft_office":[],
                        "allotments":[],
                        "bicycle_parking":[],
                        "education":[],
                        "fire_hydrant":[],
                        "historic":[],
                        "hosting":[],
                        "internet_acess":[],
                        "parking":[],
                        "sports":[],
                        "restaurant":[],
                        "public_service":[],
                        "fuel":[],
                        "taxi":[],
                        "power_supports":[],
                        "toilets":[]
              }}             

helpers.bulk(es, doc_generator())