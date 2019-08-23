# -*- coding: utf-8 -*-
"""
v.test0.2
"""

import pandas as pd
from datetime import datetime
import folium
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input File(only json)")
    parser.add_argument("-o", "--output", help="Output File (overwritten)")
    parser.add_argument("-r", "--radious", type = float, default = 0.005, help="line from each to each within this distance(degree)")
    parser.add_argument("-m", "--map", help="make map.html (all time overwrite!)", action="store_true")
    args = parser.parse_args()
    if not args.output:
        name = args.input.split('.')[:-1]
        args.output=".".join(name)+'.csv'
        
    d2,counter = seikei(args.output, args.radious)  
    if args.map:
        makemap(d2,counter)
        
def seikei(outputfile, radious):
    counter = 0
    t =[]
    l = []
    l2 = []
    count=[]
    df = pd.read_json('locate.json')
    i = 0
    while True:
        try:
            accuracy = float(df.iat[i,0]['accuracy'])
            print(accuracy)
            if accuracy > 30:
                pass
            else:
                time = datetime.fromtimestamp(float(df.iat[i,0]['timestampMs'])/1000)
                lon = float(df.iat[i,0]['longitudeE7'])/10000000
                lat = float(df.iat[i,0]['latitudeE7'])/10000000
                if i>0 and abs((l[-1]-lon)**2+(l2[-1]-lat)**2)>radious:
                    counter +=1
                count.append(counter)
                t.append(time)
                l.append(lon)
                l2.append(lat)
                print(str(time))
        except IndexError:
            break
        i+=1
    d1 = pd.DataFrame({'date':t, 'lat':l2,'lon':l,'numbering':count})
    d2 = pd.DataFrame({'lat':l2,'lon':l,'numbering':count})
    d1['date'] = d1['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    d1.to_csv(outputfile)
    return d2,counter

def makemap(d2,counter):
    df_dict = {}
    for name, group in d2.groupby('numbering'):
        df_dict[name] = group
    m = folium.Map(location=[35.0, 135.0], zoom_start=5)
    for d in df_dict:
        loc = df_dict[d][['lat','lon']].values.tolist()
        folium.PolyLine(locations=loc).add_to(m)
    m.save('map.html')

if __name__=='__main__':
    main()