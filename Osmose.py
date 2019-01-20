# -*- coding: utf-8 -*-

import overpy
import requests
from time import sleep
import os, shutil, json
from osmapi import OsmApi

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

def get_images_around(node, radius=20, logger=None):
    """
    Return all images around a gps point
    Parameters
    ----------
    node               : the {node} with "lat" and "lon" keys
    radius (optionnal) : number of meter to get images around
    logger (optionnal) : a logger object to log debug messages instead of stdout
    Returns
    -------
    a list of images in the corresponding area
    """
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    #query="http://api-pic4carto.openstreetmap.fr/search/around?lat={}&lng={}&radius={}".format(node["lat"], node["lon"], radius)
    query="http://ns3114475.ip-5-135-139.eu:28111/search/around?lat={}&lng={}&radius={}".format(node["lat"], node["lon"], radius)

    if logger is not None:
        logger.log(f'API : {query}')
    else:
        print(f'API : {query}')

    response = requests.get(query, headers=headers)

    if logger is not None:
        logger.log(f'Response code : {response.status_code}')
    else:
        print(f'Response code : {response.status_code}')

    images = response.json()
    return images['pictures']

def save_workspace(images, node, path = './workspace'):
    if not os.path.exists(path+"/"+str(node["id"])+"/"):
        os.makedirs(path+"/"+str(node["id"])+"/")

    for index, img in enumerate(images):
        print(img['pictureUrl'][39:60]+str(img["date"]))
        img_data = requests.get(img['pictureUrl']).content
        with open(path+"/"+str(node["id"])+"/"+img['pictureUrl'][39:60]+str(img["date"])+'.jpg', 'wb') as handler:
            handler.write(img_data)
        images[index]["path"]=path+"/"+str(node["id"])+"/"+img['pictureUrl'][39:60]+str(img["date"])+'.jpg'
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

def update_node_direction(node_id, direction):
    my_OsmApi = OsmApi(api="http://ns3114475.ip-5-135-139.eu:3007", username = u"team9@coachaac.com", password = u"coachaac28")
    my_OsmApi.ChangesetCreate({u'comment': u'Modify node '+str(node_id)})
    node = my_OsmApi.NodeGet(node_id)
    node["tag"]["direction"]=direction
    ChangesData = [{"type": "node","action": "modify","data": node}]
    my_OsmApi.ChangesetUpload(ChangesData)
    my_OsmApi.ChangesetClose()

#################################
#                               #
#################################
if __name__ == "__main__":

    nodes = get_node('notlemans')
    for node in nodes :
        images = get_images_around(node, radius = 5)
#         path = './workspace'
    #     if os.path.exists(path+"/"+str(node["id"])):
    #         print(f'node {node["id"]} allready scrapped')
    #     else:
    #         images = save_workspace(images, node)
    #         print(images)

    #     images = add_info_to_images(images, node)
    #     node["images"]=images

    #     with open(path+"/"+str(node["id"])+'/data.json', 'w') as foo:
    #         json.dump(node, foo)


    #delete_workspace()
