# Convert JSON to MARC
# Usage: python json2marc.py aut/person_autoriteter.json build/hansteen.json > build/hansteen.marc21.xml
#
import sys
import os
import re
import csv
import json
import xmlwitch
from copy import copy
from datetime import datetime


aut_file = sys.argv[1]
src_file = sys.argv[2]


with open(aut_file) as fp:
    autoritetsdata = json.load(fp)


with open(src_file) as fp:
    brev_saml = json.load(fp)


xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
with xml.collection:

    for row in brev_saml:

        # Unik identifikator
        ident = re.sub(r's[0-9+]\.tif', '', row['filnavn'])

        with xml.record:

            # Bearbeid dato
            if row['klass']['datering_dato'] is None or row['klass']['datering_dato'] == '':
                dato = None
                year = None
            else:
                dato = row['klass']['datering_dato'].replace('x', 'u').strip()
                year = dato[:5]
                if year == 'uuuu':
                    year = None

            # Bearbeid sted
            sted = None
            if len(row['steder']) == 1:
                sted = row['steder'][0]
                if sted['lokalitet'] is not None and sted['nasjon'] is not None:
                    sted_str = '%s, %s' % (sted['lokalitet'], sted['nasjon'])
                elif sted['lokalitet'] is not None:
                    sted_str = sted['lokalitet']
                else:
                    sted_str = sted['nasjon']

            # LDR
            # 00-04=(blank)
            # 05=a: new record
            # 06=a: language material
            # 07=m: monograph/item?
            # 18=c: ISBD punctuation omitted (eller mååå vi?)
            #
            xml.leader('     aas          c     ')

            # 006:
            # 006/00="t": Manuscript language material
            xml.controlfield('t       TODO', tag='006')

            # 007:
            xml.controlfield('ta', tag='007')

            # 008
            f008 = ''
            xml.controlfield('{}{}{}    xx#|||||||||||000|0|nor|d'.format(
                '181105',
                's' if year else 'n',
                year or 'uuuu'
            ), tag='008')

            # 024: Identifier
            with xml.datafield(tag='024', ind1='8', ind2=' '):
                xml.subfield(ident, code='a')
                xml.subfield('UIO_FUH', code='2')

            # 100/700: Avsender og mottaker
            sender = None
            rcpt = None
            for n, person in enumerate(row['personer']):
                tag = '100' if n == 0 else '700'
                with xml.datafield(tag=tag, ind1='1', ind2=' '):

                    aut = autoritetsdata.get(person['navn'], {'a': None, '0': None})

                    if aut['a'] is not None:
                        xml.subfield(aut['a'], code='a')
                    else:
                        xml.subfield(person['navn'], code='a')

                    if person['rolle']['navn'] == 'Avsender':
                        xml.subfield('aut', code='4')
                        sender = person['navn']
                    elif person['rolle']['navn'] == 'Mottaker':
                        xml.subfield('rcp', code='4')
                        rcpt = person['navn']
                    else:
                        xml.subfield(person['rolle']['navn'], code='e')
                        # print('WARNING: Ukjent rolle ' + person['rolle_navn'])

                    if aut['0'] is not None:
                        aut_id = '(NO-TrBIB)%s' % aut['0']
                        xml.subfield(aut_id, code='0')

            # 245: Lag en gøyal tittel
            title = 'UÆ, vi har ikke noen tittel!'
            if sender is not None and rcpt is not None:
                dato_f = datetime.strptime('2018-09-01', '%Y-%m-%d').strftime('%d. %B %Y').lstrip('0')
                title = 'Brev fra %s til %s datert %s' % (sender, rcpt, dato_f)
            with xml.datafield(tag='245', ind1='0', ind2='0'):
                xml.subfield(title, code='a')

            # 264: Sted og dato
            if sted is not None or dato is not None:
                with xml.datafield(tag='264', ind1=' ', ind2='0'):
                    if sted is not None:
                        xml.subfield(sted_str, code='a')
                    if dato is not None:
                        xml.subfield(dato, code='c')

            # 300: Fysisk beskrivelse
            with xml.datafield(tag='300', ind1=' ', ind2=' '):
                # Trenger tilgang til filene før jeg vet hvor mange sider det er
                xml.subfield('X sider', code='a')

            # 500: Dateringsnote
            if row['klass']['datering_komm'] is not None:
                with xml.datafield(tag='500', ind1=' ', ind2=' '):
                    xml.subfield(row['klass']['datering_komm'], code='a')

            # 535: Originalens plassering
            with xml.datafield(tag='535', ind1='1', ind2=' '):
                xml.subfield('Originalene befinner seg i: Observatoriets magasin  TODO', code='a')

            # 546: Språk
            with xml.datafield(tag='546', ind1=' ', ind2=' '):
                xml.subfield('Kan vi si noe om språk?', code='a')

            # YALE-guiden bruker 580, men er ikke 773 bedre? Eller?
            with xml.datafield(tag='773', ind1='0', ind2=' '):
                xml.subfield('Hansteens brevsamling', code='a')

            # Alma collection ID
            with xml.datafield(tag='787', ind1=' ', ind2=' '):
                xml.subfield('81218451430002204', code='w')

            # 856: Filnavn
            # https://developers.exlibrisgroup.com/alma/integrations/digital/almadigital/ingest

            for fil in row['filer']:
                with xml.datafield(tag='856', ind1=' ', ind2=' '):
                    page_designation = fil['page_designation']
                    xml.subfield(page_designation, code='a')
                    xml.subfield(fil['filename'], code='u')

print(xml)
