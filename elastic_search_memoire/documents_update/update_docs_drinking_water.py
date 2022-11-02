<<<<<<< HEAD
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd

es = Elasticsearch("http://localhost:9200", request_timeout= 30)
print(es.info().body)

def doc_generator():
  df_iter = df.iterrows()
  for index, line in df_iter:
        yield {
                  "_op_type": "update",
                  "_index": 'area1',
                  "_id" :  line["0"],
                  "script": {
                    "source": "ctx._source.drinking_water.addAll(params.drinking_water)",
                    "lang": "painless",
                    "params": {
                        "drinking_water": [{
                            "gps_coordinates": line["geometry"],
                            "category": line["Type_détaillé"]
                        }]}                  
              } }   


for i in [ i * 500 for i in range(24)]:  
  df = pd.read_csv("drinking_water_cleaned.csv")[i:i+500]
  df.reset_index(inplace = True)
=======
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd

es = Elasticsearch("http://localhost:9200", request_timeout= 30)
print(es.info().body)

def doc_generator():
  df_iter = df.iterrows()
  for index, line in df_iter:
        yield {
                  "_op_type": "update",
                  "_index": 'area1',
                  "_id" :  line["0"],
                  "script": {
                    "source": "ctx._source.drinking_water.addAll(params.drinking_water)",
                    "lang": "painless",
                    "params": {
                        "drinking_water": [{
                            "gps_coordinates": line["geometry"],
                            "category": line["Type_détaillé"]
                        }]}                  
              } }   


for i in [ i * 500 for i in range(24)]:  
  df = pd.read_csv("drinking_water_cleaned.csv")[i:i+500]
  df.reset_index(inplace = True)
>>>>>>> 0b279288ee2d23b1c32f80b5cc39a9eb7c1e5103
  helpers.bulk(es, doc_generator())