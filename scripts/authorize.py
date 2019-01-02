import json
import re
import sys
import csv
from collections import OrderedDict

main_file = 'src/hansteen.json'
agents_file = 'src/agents.json'
places_file = 'src/places.json'


def read_aut_file(filename):
    with open(filename, 'r') as fp:
        obj = json.load(fp)
        obj = {x['name']: x for x in obj}
    return obj


def write_aut_file(obj, filename):
    with open(filename, 'w') as fp:
        canonical_rep = sorted(obj.values(), key=lambda x: x['name'])
        canonical_rep = [OrderedDict(sorted(x.items())) for x in canonical_rep]
        json.dump(canonical_rep, fp, indent=2, ensure_ascii=False)


agents = read_aut_file(agents_file)
places = read_aut_file(places_file)

with open(main_file, 'r') as fp:
    data = json.load(fp)
    for letter in data:

        for place in letter['descriptive']['places']:
            aut = places.get(place['place'])
            if aut is None:
                places[place['place']] = {
                    'name': place['place'],
                    'country': place['country'],
                    'wikidata_id': None,
                }
            elif aut.get('wikidata_id') is not None:
                place['wikidata_id'] = aut['wikidata_id']

        for agent_type, agent in letter['descriptive']['agents'].items():
            aut = agents.get(agent['name'])
            if aut is None:
                agents[agent['name']] = {
                    'name': agent['name'],
                    'wikidata_id': None,
                }
            else:
                if aut.get('bibsys_id') is not None:
                    agent['bibsys_id'] = aut['bibsys_id']
                if aut.get('wikidata_id') is not None:
                    agent['wikidata_id'] = aut['wikidata_id']
                if aut.get('bibsys_name') is not None:
                    agent['aut_name'] = aut['bibsys_name']

with open(main_file, 'w') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)

write_aut_file(places, places_file)
write_aut_file(agents, agents_file)
