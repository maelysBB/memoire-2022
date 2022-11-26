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
                    "source": "ctx._source.taxi.addAll(params.taxi)",
                    "lang": "painless",
                    "params": {
                        "taxi": [{
                            "gps_coordinates": line["geometry"]
                        }]}                  
              } }   

df = pd.read_csv(f"./csv_files/{distance}/taxi_cleaned_{distance}.csv")
helpers.bulk(es, doc_generator(), chunk_size=250, request_timeout= 3000, raise_on_error=False)