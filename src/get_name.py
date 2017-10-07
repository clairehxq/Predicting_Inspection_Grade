import os 
import sys
import json
import time
import numpy as np 
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import foursquare as fs
from keys import fsapi

client = fs.Foursquare(client_id=fsapi['client_id'],
                            client_secret=fsapi['client_secret'])

def preprocessed(file):
    '''
    Only take data has grade
    find unique data
    '''
    df = pd.read_csv(file)
    clean = df[pd.notnull(df['GRADE'])].drop_duplicates('CAMIS')
    clean['clean_ad'] = clean['BUILDING'].str.strip()+ " " + clean['STREET'].str.strip() + " "+\
                        clean['ZIPCODE'].astype(int).astype(str)
    return clean 

def get_info(x):
    try:
        print ("Sucessfully get {}".format(x['DBA'].strip()))
        query = client.venues.search(params={'near': x["clean_ad"], 'query': x['DBA'].strip()})
        try:
            results = pd.io.json.json_normalize(query["venues"][0])
            return results['id'].values
        except:
            print(len(results))
            return 'NAN'
    except:
        print ("no info about this vanue")
        return 'NAN'
    
    

def get_data(df):
    get_data = []
    for index, row in df.iterrows():

        get_data.append((get_info(row), row['CAMIS'], row['DBA']))
        
    df = pd.DataFrame(get_data, columns=['id', 'CAMIS', 'DBA'])
    
    return df

if __name__ == '__main__':

    df = preprocessed('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    
    for g, chunk in df.groupby(np.arange(len(df)) // 100):
        if g > 121 and g< 251:
            meta = get_data(chunk)
            meta.to_csv('./data/master2/master_listi_{}.csv'.format(g))
            meta.to_pickle('./data/master2/master_listi_{}.pkl'.format(g))