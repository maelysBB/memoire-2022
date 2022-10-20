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
  df['banque'] = data['banque'].iloc[df['loc']]
  df['santé'] = data['santé'].iloc[df['loc']]
  df['cimetière'] = data['cimetière'].iloc[df['loc']]
  df['cinéma'] = data['cinéma'].iloc[df['loc']]
  df['jardin'] = data['jardin'].iloc[df['loc']]
  return df