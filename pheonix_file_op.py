import json

#Saving as json format.
def jsonsave(content,filename):
    with open(filename,'w') as file_obj:
        json.dump(content,file_obj)

#Loading json file
def jsonload(filename):
    with open(filename) as file_obj:
        return json.load(file_obj)