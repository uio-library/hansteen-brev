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

src_folder = sys.argv[1]


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


def main():
    tab_k = simle_map('foto_klassifikasjon.csv', 'klassifikasjons_id')
    tab_s = simle_map('sted.csv', 'sted_id')
    tab_p = simle_map('person.csv', 'person_id')
    tab_r = simle_map('personrolle.csv', 'personrolle_id')

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

        brev = copy(row)
        brev['foto_kort_id'] = int(brev['foto_kort_id'])
        brev['klass'] = tab_k[kid]
        brev['klass']['datering_dato'] = brev['klass']['datering_dato'].replace('.', '-')
        brev['steder'] = tab_ks.get(kid, [])
        brev['personer'] = tab_kpr.get(kid, [])
        brev['filer'] = filer[kid]


        # Rydd vekk felter som ikke er i bruk og unødvendige felter,
        # for å gjøre JSON-filen mer oversiktlig.

        for k in list(brev.keys()):
            if brev[k] == '':
                brev[k] = None
        for k in list(brev['klass'].keys()):
            if k in [
                'foto_kort_id', 'klassifikasjons_id',  # Nøkler vi ikke trenger i dokumentrepresentasjonen
                'datering_fra', 'datering_til', # Kun brukt i to poster, med verdien 'uten dato', informasjon som allerede finnes i annet felt
                'annen_informasjon'  # Ikke i bruk
            ]:
                pass
            elif brev['klass'][k] == '':
                brev[k] = None
            else:
                brev[k] = brev['klass'][k]

        del brev['klass']  # Flyttet til brev
        del brev['siste_klassifikasjon']  # Fremmednøkkel
        del brev['filnavn']  # Meningsløst, tilfeldig verdi fra en join
        del brev['samlings_id']  # Ikke i bruk
        del brev['tittel']  # Ikke i bruk
        del brev['registrert']  # I praksis ikke i bruk, kun brukt av post 21
        del brev['annen_arkivident']  # Meningsløst, tilfeldig verdi fra en join
        del brev['mediagruppe_enhets_id']  # Meningsløst
        for val in brev['steder']:
            for k in list(val.keys()):
                if k in ['adresse', 'fylke', 'kommune', 'omraade']:  # Ikke i bruk
                    del val[k]
                elif val[k] == '':
                    val[k] = None

        # Normaliser koding av ukjent dato
        if brev['datering_dato'] == 'xxxx-xx-xx':
            brev['datering_dato'] = None

        # Sorter avsender først, så denne havner i 100
        brev['personer'] = sorted(brev['personer'],
                                  key=lambda person: 0 if person['rolle']['navn'] == 'Avsender' else 1)

        brev_saml.append(brev)

    sys.stderr.write('Leste %d brev, %d personer, %d steder fra %s\n' % (
        len(brev_saml),
        len(tab_p),
        len(tab_s),
        src_folder
    ))

    print(json.dumps(brev_saml, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
