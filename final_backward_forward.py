
# calculate backward or forward at the end


import os
import json



def backward_or_forward(node):
    with open('./workspace/'+str(node)+'/data2.json') as json_file:  
        data = json.load(json_file)
        
    for img in data['images']:
        if img['classifier_prediction'] == 1:
            #print(img['path'],'- img direction', img['direction'],'- road direction', data['road_direction'])
            delta = (abs(int(data['road_direction'])-int(img['direction'])))
            if delta > 90:
                return 'backward'
            else:
                return 'forward'
            
    return 'undetermined'


#################################
#                               #
#################################
if __name__ == "__main__":
    res = backward_or_forward(1364412209)
    print(res)
