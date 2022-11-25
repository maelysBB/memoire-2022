import math
import pandas as pd
import numpy as np



"""Observer la similarité entre un vecteur donné et l'ensemble des vecteurs"""

def difference(origin_vector, vector_matrix): #On pénalise quand il y en a plus d'éléments ou qu'il y en a moins
  dif = sum(np.square(origin_vector - vector_matrix))**(1/2)
  return dif


def add(df, data):
  df['loc']=df.index
  df['lat'] = data['lat'].iloc[df['loc']]
  df['lon'] = data['lon'].iloc[df['loc']]
  for i in ['shop_craft_office','restaurant','cinema','library','playground','sports','allotments',
  'historic','hosting','education','healthcare','bank','public_service','toilets','drinking_water',
  'aed','fire_hydrant','carpool','parking','bicycle_parking','charging_station','taxi','fuel']:
    df[i]=data[i].iloc[df['loc']]
  return df