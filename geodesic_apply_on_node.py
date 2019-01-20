# get road direction of each node

import os
import json
from glob import glob




with open('./workspace/highway_nodes.json') as json_file:  
    roads = json.load(json_file)




paths = glob('./workspace/*')

for path in paths:
    if os.path.isfile(path+'/data.json'):
        with open(path+'/data.json') as json_file:  
            data = json.load(json_file)
        data['road_direction'] = roads[str(data['id'])]['road_direction']
        with open(path+'/data2.json', 'w') as foo:
            json.dump(data, foo)

