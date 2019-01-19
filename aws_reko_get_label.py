import os
import boto3
import json
from glob import glob

def get_files_list(root,ext):

    files_list = []

    for path, subdirs, files in os.walk(root):
        files = [fi for fi in files if fi.endswith(ext)]
        for name in files:
            files_list.append(name)

    return files_list


def get_image(imageFile,client):

    with open(imageFile, 'rb') as image:
        return client.detect_labels(Image={'Bytes': image.read()},MaxLabels=60,MinConfidence=50)   

#################################
#                               #
#################################
if __name__ == "__main__":

    #session = boto3.session.Session()
    client=boto3.client('rekognition')
    #dir_ = './workspace/'
    paths = glob('./workspace/*')

    print(paths)

    for path in paths:
        print('\n>>',path)
        if os.path.isfile(path+'/aws_labels.json'):
            print(f'labels of {path} files already exec')
        else:
            files_list = get_files_list(path,'jpg')
            labels = []

            for file in files_list:
                print(file)
                aws = get_image(path+'/'+file,client)
                aws['file'] = file
                print(aws)
                labels.append(aws)

            with open(path+'/aws_labels.json', 'w') as foo:
                json.dump(labels, foo)


