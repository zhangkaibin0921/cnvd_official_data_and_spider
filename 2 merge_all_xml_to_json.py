
import os
import xmltodict
import json
res={}

def addOne(filename):
    print(filename)
    global res
    with open('cnvd/'+filename, 'r',encoding='utf-8') as xml_file:
        xml_data = xml_file.read()
    xml_dict = xmltodict.parse(xml_data)
    json_data = json.dumps(xml_dict, indent=4, ensure_ascii=False)
    json_data=json.loads(json_data)

    print(type(json_data))


    print(len(json_data['vulnerabilitys']['vulnerability']))
    if not res:
        res=json_data
    else:
        res['vulnerabilitys']['vulnerability']=res['vulnerabilitys']['vulnerability']+json_data['vulnerabilitys']['vulnerability']

directory = 'cnvd'
file_names = os.listdir(directory)
xml_list= [file_name for file_name in file_names if file_name.endswith('.xml')]
print(len(xml_list))

for filename in xml_list:
    addOne(filename)

print(len(res['vulnerabilitys']['vulnerability']))
with open('cnvd/merger.json', 'w',encoding='utf-8') as json_file:
    json.dump(res, json_file, indent=4, ensure_ascii=False)