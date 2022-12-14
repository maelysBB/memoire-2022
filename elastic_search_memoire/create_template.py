import requests
from elasticsearch import Elasticsearch, helpers
import configparser
from run import distance

config = configparser.ConfigParser()
config.read('example.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

data = {"index_patterns": ["*area*"], 
"template": {
"settings": {
"number_of_shards": 1,
"number_of_replicas": 0
},
"mappings": {
"properties": {
"id_df": {
  "type": "integer"
      },
"polygon": {
    "type": "geo_shape"
        },
"centroid": {
    "type": "geo_point"
        },
"coordinates": {
  "type": "nested",
  "properties": {
    "x": {"type":"integer"}, 
    "y":{"type":"integer"}
                }
              },
"healthcare": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"drinking_water":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
    }
}, 
"charging_station":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
    }
    },
"restaurant":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"public_service":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"fuel":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"taxi":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"}
      }
    },
"toilets":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"power_supports":  {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"aed": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
         "acc":
         {"type":"text"}
      }
    },
"bank": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"carpool": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"cemetery": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
         "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
        }
    },
"cinema": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"cycleway": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"library": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"playground": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"recycling": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"}
      }
    },
"shop_craft_office": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"allotments": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    }, 
"bicycle_parking": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"education": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"fire_hydrant": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"historic": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"hosting": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },
"internet_acess": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    },
"parking": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"}
      }
    }, 
"sports": {
    "type": "nested",
    "properties": {"gps_coordinates": 
        {"type":"geo_point"},
        "category": 
        {"type":"keyword"},
        "name_text":
         {"type":"text"},
         "name_keyword":
         {"type":"keyword"}
      }
    },    
}
}
},
"priority": 500
}

url = "https://my-deployment-8a262e.es.us-central1.gcp.cloud.es.io/_index_template/template_area"

response = requests.post(url, auth=(config['ELASTIC']['user'], config['ELASTIC']['password']), json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())