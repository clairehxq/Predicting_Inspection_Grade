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
        location = '{0:.2f},{0:.2f}'.format(x["goog_lat"], x["goog_lng"])
        print (location)
        query = client.venues.search(params={'ll': location, 'query': x['DBA'].strip()})
        try:
            results = pd.io.json.json_normalize(query["venues"][0])
            return results
        except:
            print(len(result))
    except:
        print ("no info about this vanue")
    
    

def get_data(df):
    get_data = []
    for index, row in df.iterrows():
        get_data.append(get_info(row))
    agg = pd.concat(get_data)
    #agg.columns = agg.columns.map(lambda x: x.split(".")[-1])
    if 'shortName' in agg.categories[0]:
        agg['fs_cat'] = agg.categories.apply(lambda x: x[0]['shortName'])
    else:
        agg['fs_cat'] = np.nan
    filename = 'data2/venues/meta_{}_{}.pkl'.format(agg.iloc[0]['id'], agg.iloc[-1]['id'])
    agg.to_pickle(filename)
    output = agg[['id','fs_cat']]
    return output

def get_venue_detail(df, attr=['rating','stats.checkinsCount',
                                'stats.tipCount', 'stats.usersCount', 'stats.visitsCount',
                                'location.lat', 'location.lng', 'location.postalCode']):
    group = []
    venue_id = df['id'].dropna().unique()
    for vd in venue_id:
        print (vd) 
        query = client.venues(vd)
        #time.sleep(1)
        #print ('take a break on getting venue detail')
        venue = pd.io.json.json_normalize(query["venue"])
        venue.to_pickle('data/venues/venue_{}.pkl'.format(vd))
        a = set(attr)
        b = set(venue.columns.values)
        if a.difference(b):
            for col in list(a.difference(b)):
                venue[col] = np.nan
        temp = venue[attr]
        temp['id'] = vd
        group.append(temp)
    agg_frame = pd.concat(group)
    geometry = [Point(xy) for xy in zip(agg_frame['location.lng'], agg_frame['location.lat'])]
    gpvenue = GeoDataFrame(agg_frame, geometry=geometry)
    
    return gpvenue


def main():
    pass

if __name__ == '__main__':

    clean = preprocessed(sys.argv[1])
    print ("Thare are {} unqiue data".format(len(clean)))
    #### meta-data 
    #### spatial points included
    for g, chunk in clean.groupby(np.arange(len(clean)) // 50):
        if g > 245:
            meta = get_data(chunk)
            print ("missing data: {} %".format(len(meta)/(1.0*len(clean))))
            venue = get_venue_detail(meta)
            final_frame = venue.merge(meta, on='id')
            output = 'data/output/chunk_{}'.format(g)
            final_frame.to_csv(output+'.csv')
            final_frame.to_pickle(output+'.pkl')
            time.sleep(5)
            print ('{} is done'.format(len(chunk)))
        