import json

data_json = open('datasets.json')
data_str = data_json.read()
data_dict = json.loads(data_str)

for item in data_dict['datasets']:
    print item['id'], ':', item['name'], '\n'
    for col in item['columns']:
        print col['name']
    print '\n\n'




