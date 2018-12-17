# Convert CSV files into a simple JSON structure
# Usage: python csv2json.py src > build/hansteen.json
#
import sys
import os
import re
import csv
import json
import xmlwitch
from copy import copy
from datetime import datetime
import pycountry
import gettext

# Build a map of country names to country codes
nb = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['nb'])
nb.install()
countries = {}
for country in pycountry.countries:
    countries[_(country.name)] = country.alpha_2
countries['Russland'] = 'RU'
countries['USA'] = 'US'
countries['Portugal'] = 'PT'

src_folder = sys.argv[1]

roles = {
    'Avsender': 'correspondent',
    'Mottaker': 'addressee',
}

def get_table_rows(fname):
    path = os.path.join(src_folder, fname)
    with open(path) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield row


def simle_map(fname, key):
    return {row[key]: row for row in get_table_rows(fname)}


def one_to_many(fname, key, other, other_key, pivot_data={}):
    out = {}
    for row in get_table_rows(fname):
        kid = row[key]
        data = copy(other[row[other_key]])
        for k, v in pivot_data.items():
            data[k] = v[0][row[v[1]]]
        if not kid in out:
            out[kid] = []
        out[kid].append(data)
    return out


def null_if_empty(val):
    if val == '':
        return None
    return val


def main():
    tab_k = simle_map('foto_klassifikasjon.csv', 'klassifikasjons_id')
    tab_s = simle_map('sted.csv', 'sted_id')
    tab_p = simle_map('person.csv', 'person_id')
    tab_r = simle_map('personrolle.csv', 'personrolle_id')
    tab_b = simle_map('bruker.csv', 'bruker_id')

    with open(os.path.join(src_folder, 'filer_brev.json')) as fp:
        filer = json.load(fp)

    tab_ks = one_to_many('klassifikasjon_sted.csv', 'klassifikasjons_id', tab_s, 'sted_id')
    tab_kpr = one_to_many('klassifikasjon_person_rolle.csv', 'klassifikasjons_id', tab_p, 'person_id', {'rolle': [tab_r, 'personrolle_id']})

    brev_saml = []

    ids = set()
    for row in get_table_rows('foto_kort.csv'):
        kid = row['siste_klassifikasjon']

        ident = row['tilvekstnr']
        if ident in ids:
            sys.stderr.write('Tilvekstnr. er IKKE unikt: %s\n' % ident)
        ids.add(ident)

        klass = tab_k[kid]


        basenames = set([x['basename'] for x in filer[kid]])
        if len(basenames) > 1:
            sys.stderr.write('Basename differs: %s -- for %s\n' % (', '.join(basenames), ident))

        metadata = {
            'id': ident,
            'descriptive': {
                'date': klass['datering_dato'].replace('.', '-'),
                'date_comment': null_if_empty(klass['datering_komm']),
                'places': [],
                'agents': {},
                'comment': null_if_empty(klass['motivbeskrivelse'])
            },
            'administrative': {
                'described_by': tab_b[row['registrert_av']]['navn'],
                'described_at': row['registrert_dato'],
                'collection': row['samling'],
            },
            'structure': filer[kid],
        }

        for val in tab_ks.get(kid, []):
            metadata['descriptive']['places'].append({
                'place': null_if_empty(val['lokalitet']),
                'country': null_if_empty(val['nasjon']),
                'country_code': countries.get(val['nasjon']),
                'comment': null_if_empty(klass['stedkommentar']),
            })

            if metadata['descriptive']['places'][-1]['country'] is not None and metadata['descriptive']['places'][-1]['country_code'] is None:
                sys.stderr.write('Unknown country: "%s"\n' % metadata['descriptive']['places'][-1]['country'])

        for val in tab_kpr.get(kid, []):
            role = val['rolle']['navn']
            if role not in roles:
                sys.stderr.write('Ignoring unknown person role: %s\n' % role)
            else:
                metadata['descriptive']['agents'][roles[role]] = {
                    'name': val['navn'],
                }

        # Normaliser koding av ukjent dato
        if metadata['descriptive']['date'] == 'xxxx-xx-xx':
            metadata['descriptive']['date'] = None

        if 'correspondent' not in metadata['descriptive']['agents']:
            sys.stderr.write('Correspondent missing: %s\n' % ident)

        brev_saml.append(metadata)

    sys.stderr.write('Leste %d brev, %d personer, %d steder fra %s\n' % (
        len(brev_saml),
        len(tab_p),
        len(tab_s),
        src_folder
    ))

    print(json.dumps(brev_saml, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
