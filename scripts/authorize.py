import json
import re
import sys
import csv

filename = 'src/hansteen.json'
aut_file = 'src/person_autoriteter.json'


# auts = {}
# with open('src/openrefine_reconcile.tsv') as fp:
#     for row in csv.DictReader(fp, delimiter='\t'):
#         auts[row['id']] = row


with open(aut_file, 'r') as fp:
    authorities = json.load(fp)


labels = set()
with open(filename, 'r') as fp:
    data = json.load(fp)
    for letter in data:
        for agent_type, agent in letter['descriptive']['agents'].items():

            # if agent_type == 'correspondent' and auts.get(letter['id']):
            #     aut = auts.get(letter['id'])
            #     agent['wikidata_id'] = aut['wd']
            #     agent['aut_name'] = aut['name']

            aut = authorities.get(agent['name'])
            if aut is not None and aut.get('bibsys_id') is not None:
                agent['bibsys_id'] = aut['bibsys_id']
            if aut is not None and aut.get('wikidata_id') is not None:
                agent['wikidata_id'] = aut['wikidata_id']
            elif agent.get('wikidata_id'):
                print('Oi:', agent.get('wikidata_id'))
            if aut is not None and aut.get('bibsys_name') is not None:
                agent['aut_name'] = aut['bibsys_name']



with open(filename, 'w') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)
