import overpy

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
        temp = {'id': node.id, 'lat': node.lat, 'lon': node.lon, 'highway': node.tags['highway']}
        if 'direction' in node.tags:
            temp['direction'] = node.tags['direction']
        node_collected.append(temp)

    return node_collected

#################################
#                               #
#################################
if __name__ == "__main__":


	print(get_node('fast'))