# -*- coding: utf-8 -*-

import overpy
import requests
from time import sleep
import os, shutil, json

def printlist(list):
    print(*list, sep = "\n")

def get_node(zone):
    """collect node ["highway"="stop"] from OSMOSE / OVERPASS TURBO

    Keyword arguments:
    zone -- the area to scan : lemans (whole city), whatever (small part for faster exec)
    output -- list of dict : id, lat, lon, highway, direction (optionnal)
    """
    api = overpy.Overpass()

# fetch stop 
    if zone == 'lemans':
        result = api.query("""[out:json][timeout:25];area(3600107435)->.searchArea;(node["highway"="stop"](area.searchArea););out;>;out skel qt;""")
    else:
        result = api.query("""[out:json][timeout:25];(node["highway"="stop"](47.99686464222191,0.18395662307739258,48.00295961729204,0.19527554512023926););out;>;out skel qt;""")

    node_collected = []
 
    for node in result.nodes:
        temp = {'id': node.id, 'lat': str(node.lat), 'lon': str(node.lon), 'highway': node.tags['highway']}
        if 'direction' in node.tags:
            temp['direction'] = node.tags['direction']
        node_collected.append(temp)

    return node_collected

def get_images_around(node, radius = 20):
    """Return all images around a gps point

    Keyword arguments:
    node -- the {node} with "lat" and "lon" keys
    output (optionnal) -- number of meter to get images around
    """
    #Hi I'm not a bot
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    query="http://api-pic4carto.openstreetmap.fr/search/around?lat={}&lng={}&radius={}".format(node["lat"], node["lon"], radius)
    response = requests.get(query, headers=headers)
    images = response.json()
    return images['pictures']

def save_workspace(images, node, path = './workspace'):
    if not os.path.exists(path+"/"+str(node["id"])+"/"):
        os.makedirs(path+"/"+str(node["id"])+"/")

    for img in images:
        print(img['pictureUrl'][39:60]+str(img["date"]))
        img_data = requests.get(img['pictureUrl']).content
        with open(path+"/"+str(node["id"])+"/"+img['pictureUrl'][39:60]+str(img["date"])+'.jpg', 'wb') as handler:
            handler.write(img_data)
        img["path"]=path+"/"+str(node["id"])+"/"+img['pictureUrl'][39:60]+str(img["date"])+'.jpg'
        sleep(0.2)
    return images

def delete_workspace(path = './workspace/'):
    if os.path.exists(path):
        shutil.rmtree(path)
    return 1

def add_info_to_images(images, node):
    for img in images : #list of images around the node
        img["node_coordinates"]={"lat":node["lat"],"lng":node["lon"]}
        img["node_id"]=node["id"]
        if "direction" in node :
            img["node_direction"]=node["direction"]
        else :
            img["node_direction"]=None
        img["road_direction"]=None
        img["human_prediction"]=None
        img["classifier_prediction"]=None

    return images

#################################
#                               #
#################################
if __name__ == "__main__":

    nodes = get_node('fast')
    for node in nodes :
        images = get_images_around(node, radius = 2)
        images = save_workspace(images, node)
        images = add_info_to_images(images, node)
        node["images"]=images


    print(nodes)

    with open('./data.json', 'w') as foo:
        json.dump(nodes, foo)


    delete_workspace()
