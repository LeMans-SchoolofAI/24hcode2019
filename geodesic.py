
#calculate roads direction for every stop


import overpy
from geographiclib.geodesic import Geodesic
import json


def get_api_result():
    api = overpy.Overpass()
    return api.query("""[out:json][timeout:25];area(3600107435)->.searchArea;(node["highway"="stop"](area.searchArea););out body;way(bn);out body;>;out skel qt;""")



def get_nodes_list(result):
    nodes = {}
    for node in result.nodes:
        nodes[node.id] = {'lat': str(node.lat), 'lon': str(node.lon)}
        if 'highway' in node.tags:
            nodes[node.id]['highway'] = node.tags['highway']
            if 'direction' in node.tags:
                nodes[node.id]['direction'] = node.tags['direction']              
    return nodes


def get_roads_list(result):
    roads = {}
    for way in result.ways:
        temp = []
        for node in way.nodes:
            temp.append(node.id)
        roads[way.id] = temp   
    return roads


def get_roads_of_nodes_list(result):
    roads_of_nodes = []
    for way in result.ways:
        for node in way.nodes:
            roads_of_nodes.append({node.id: way.id})
    return roads_of_nodes


def get_road_of_a_sign(node, roads_of_nodes):
    temp = [w for w in roads_of_nodes if node in w]
    if len(temp) > 1:
        print('too many roads',node)
        #return 0
    return temp[0][node]


def get_prox_nodes_of_the_road(node, road, roads_list, nodes_list):
    idx = roads_list[road].index(node)
    if idx == 0:
        coords = [nodes_list[roads_list[road][idx]]['lat'],nodes_list[roads_list[road][idx]]['lon'],nodes_list[roads_list[road][idx+1]]['lat'],nodes_list[roads_list[road][idx+1]]['lon']]
    else:
        coords = [nodes_list[roads_list[road][idx-1]]['lat'],nodes_list[roads_list[road][idx-1]]['lon'],nodes_list[roads_list[road][idx]]['lat'],nodes_list[roads_list[road][idx]]['lon']]
    
    return float(coords[0]),float(coords[1]),float(coords[2]),float(coords[3])


def get_road_direction(lat1,lon1,lat2,lon2):
    geod = Geodesic.WGS84
    brng = geod.Inverse(lat1,lon1,lat2,lon2)['azi2']
    if brng < 0:
        brng+= 360
    return brng



#################################
#                               #
#################################
if __name__ == "__main__":
    result = get_api_result()

    nodes_list = get_nodes_list(result)
    roads_list = get_roads_list(result)
    roads_of_nodes_list = get_roads_of_nodes_list(result)

    highway_nodes = {}

    for n in nodes_list:
        if 'highway' in nodes_list[n]:
            way = get_road_of_a_sign(n, roads_of_nodes_list)
            lat1,lon1,lat2,lon2 = get_prox_nodes_of_the_road(n, way, roads_list, nodes_list)
            highway_nodes[n] = nodes_list[n]
            highway_nodes[n]['road_direction'] = get_road_direction(lat1,lon1,lat2,lon2) 
        
    print(highway_nodes)
    with open('./workspace/highway_nodes.json', 'w') as foo:
        json.dump(highway_nodes, foo)
