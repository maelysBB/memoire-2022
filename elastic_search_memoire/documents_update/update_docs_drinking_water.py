from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd


es = Elasticsearch("http://localhost:9200", request_timeout= 30)
print(es.info().body)

# es.indices.put_settings(index="area1", body={
#     "index.mapping.total_fields.limit": 200000
# })

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
                            "gps_coordinates": ""
                        }]}                  
              } }   


for i in [ i * 500 for i in range(60)]:  
  df = pd.read_csv("healthcare_tosave.csv")[i:i+500]
  df.reset_index(inplace = True)
  helpers.bulk(es, doc_generator())