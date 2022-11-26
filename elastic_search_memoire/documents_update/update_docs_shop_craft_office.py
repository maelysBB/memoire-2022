from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
from run import distance
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)
print(es.info().body)

def doc_generator():
  df_iter = df.iterrows()
  for index, line in df_iter:
        yield {
                  "_op_type": "update",
                  "_index": f'area{distance}',
                    "_id" :  line["0"],
                  "script": {
                    "source": "ctx._source.shop_craft_office.addAll(params.shop_craft_office)",
                    "lang": "painless",
                    "params": {
                        "shop_craft_office": [{
                            "gps_coordinates": line["geometry"],
                              "name_text": line["name"],
                              "name_keyword": line["name"],
                              "category": line["Type_détaillé"]
                        }]}                  
              } }   

df = pd.read_csv(f"./csv_files/{distance}/shop_craft_office_cleaned_{distance}.csv")
helpers.bulk(es, doc_generator(), chunk_size=250, request_timeout= 120, raise_on_error=False)