
# coding: utf-8

import os 
import sys
import glob
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


result_missing = pd.read_pickle('./missing.pkl')


def give_ll(row):
    return str(round(row['goog_lat'],2)) + ',' + str(round(row['goog_lng'],2))

result_missing['ll']  =result_missing.apply(give_ll, axis=1)


for g, chunk in result_missing.groupby(np.arange(len(result_missing)) // 100):
    data = []
    for index, row in chunk.iterrows():
        try:
            print ('ll: {}, query {}'.format(row['ll'], row['DBA_x']))
            query = client.venues.search(params={'ll': row['ll'], 'query': row['DBA_x']})
            data.append(pd.io.json.json_normalize(query["venues"]).loc[0])
        except:
            print('no data')
    pd.concat(data, axis=0).to_csv('./data/missing/missin_{}'.format(g))

