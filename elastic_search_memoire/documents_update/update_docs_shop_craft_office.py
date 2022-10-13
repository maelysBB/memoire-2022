from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd

es = Elasticsearch("http://localhost:9200", request_timeout= 500)
print(es.info().body)

def doc_generator():
  df_iter = df.iterrows()
  for index, line in df_iter:
        yield {
                  "_op_type": "update",
                  "_index": 'area1',
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

for i in [ i * 100 for i in range(1270)]:  
  df = pd.read_csv("./csv_files/shop_craft_office_cleaned.csv")[i:i+500]
  df.reset_index(inplace = True)
  helpers.bulk(es, doc_generator())