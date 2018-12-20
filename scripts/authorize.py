import json
import re
import sys
import csv

filename = 'src/hansteen.json'
aut_file = 'src/person_autoriteter.json'


auts = {}
with open('src/openrefine_reconcile.tsv') as fp:
    for row in csv.DictReader(fp, delimiter='\t'):
        auts[row['id']] = row


with open(aut_file, 'r') as fp:
    authorities = json.load(fp)


labels = set()
with open(filename, 'r') as fp:
    data = json.load(fp)
    for letter in data:
        for agent_type, agent in letter['descriptive']['agents'].items():

            if agent_type == 'correspondent' and auts.get(letter['id']):
                a = auts.get(letter['id'])
                agent['wikidata_id'] = a['wd']
                agent['aut_name'] = a['name']

            aut = authorities.get(agent['name'])
            if aut is not None and aut.get('0') is not None:
                agent['bibsys_id'] = aut['0']
            if aut is not None and aut.get('wd') is not None:
                agent['wikidata_id'] = aut['wd']
            if aut is not None and aut.get('a') is not None:
                agent['aut_name'] = aut['a']



with open(filename, 'w') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)
