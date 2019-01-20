# use aws predictions to copy images containing signs


import os
import json
from glob import glob
from shutil import copyfile

paths = glob('./workspace/*')

for path in paths:
    if os.path.isfile(path+'/aws_labels.json'):
        print(path+'/aws_labels.json')
        with open(path+'/aws_labels.json') as json_file:  
            data = json.load(json_file)
            for dd in data:
                for lab in dd['Labels']:
                        if lab['Name'] == 'Sign' or lab['Name'] == 'Road Sign':
                            print(dd['file'],lab)
                            copyfile(path+'/'+dd['file'], './workspace/aws_predicts_signs/'+dd['file'])

