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
import locale

locale.setlocale(locale.LC_ALL, 'no_NO.UTF-8')

# Current date and time with 1 millisecond digit, as required by the MARC21 005 field
current_datetime = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f')[:16]
current_datetime = '20181127225134.9'  # Fix while testing, TODO: REMOVE THIS LINE

aut_file = sys.argv[1]
src_file = sys.argv[2]


with open(aut_file) as fp:
    autoritetsdata = json.load(fp)


with open(src_file) as fp:
    brev_saml = json.load(fp)


def formater_dato(dato):

    # Fullstendig dato
    m = re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', dato)
    if m is not None:
        return datetime.strptime(dato, '%Y-%m-%d').strftime('%d. %B %Y').lstrip('0')

    # Mangler årstall
    m = re.match('uuuu-[0-9]{2}-[0-9]{2}', dato)
    if m is not None:
        return datetime.strptime(dato[5:], '%m-%d').strftime('%d. %B').lstrip('0') + ' (ukjent år)'

    # Mangler dag
    m = re.match('[0-9]{4}-[0-9]{2}-uu', dato)
    if m is not None:
        return datetime.strptime(dato[:7], '%Y-%m').strftime('%B %Y')

    # Mangler dag og måned
    m = re.match('^[0-9]{4}-uu-uu$', dato)
    if m is not None:
        return dato[:5]

    # Mangler dag og måned
    m = re.match('^[0-9]{4}$', dato)
    if m is not None:
        return dato

    sys.stderr.write('Ukjent dato: %s\n' % dato)
    return '???????'

xml = xmlwitch.Builder(version='1.0', encoding='utf-8')

with xml.collection:

    for row in brev_saml:

        # Unik identifikator
        ident = row['tilvekstnr']

        with xml.record:

            # Bearbeid dato
            if row['datering_dato'] is None:
                dato = None
                year = 'uuuu'
                dato_type = 'n'  # Ukjent
            else:
                dato = row['datering_dato'].replace('x', 'u').strip()
                if re.match(r'^[0-9]{4}-[0-9]{2}', dato):
                    dato_type = 'e'  # Detaljert dato
                else:
                    dato_type = 's'  # Kun år
                year = dato[:5]

            # Bearbeid sted
            sted = None
            sted_s = None
            if len(row['steder']) == 1:
                sted = row['steder'][0]
                #if sted['lokalitet'] is not None and sted['nasjon'] is not None:
                #    sted_s = '%s, %s' % (sted['lokalitet'], sted['nasjon'])
                if sted['lokalitet'] is not None:
                    sted_s = sted['lokalitet']
                else:
                    sted_s = sted['nasjon']
            elif len(row['steder']) > 1:
                sys.stderr.write('%s : FLERE STEDER\n' % ident)

            # ---------------------------------------------------------------------------
            # LDR
            # ---------------------------------------------------------------------------

            ldr = [' ' for c in range(24)] # Start with a blank 24-character string
            ldr[5]  = 'a'  # Record status: New
            ldr[6]  = 't'  # Type of record: Manuscript language material
            ldr[7]  = 'm'  # Bibliographic level: Monograph/Item
            ldr[9]  = 'a'  # Character coding scheme: UCS/Unicode
            ldr[18] = 'c'  # Descriptive cataloging form: ISBD punctuation omitted
            xml.leader(''.join(ldr))

            # ---------------------------------------------------------------------------
            # 005: Date and Time of Latest Transaction
            # ---------------------------------------------------------------------------

            xml.controlfield(current_datetime, tag='005')

            # ---------------------------------------------------------------------------
            # 008: Fixed-Length Data Elements
            # ---------------------------------------------------------------------------

            f008 = [' ' for c in range(40)]  # Start with a blank 40-character string
            f008[0:6] = '181101'  # Date entered on file

            # Type of date
            if dato_type == 'e':
                # Detailed date which contains the month (and possibly the day) in
                # addition to the year is present.
                f008[6] = 'e'
                f008[7:15] = dato.replace('-', '')
            elif dato_type == 's':
                # Single known date/probable date
                f008[6] = 's'
                f008[7:11] = dato[:5]
            else:
                # Dates unknown
                f008[6] = 'n'
                f008[7:15] = 'uuuuuuuu'

            f008[15:18] = 'xx '  # No place, unknown, or undetermined

            # Språk: Ser ikke ut som det er katalogisert.
            # Kan gjette basert på avsendersted, men risky.
            f008[35:38] = '   '

            f008[39] = 'd'  # Cataloging source: Other, more info in 040.

            xml.controlfield(''.join(f008), tag='008')
            # Eks: {}{}{}    xx#|||||||||||000|0|nor|d'  # TODO: Legg inn ||||||... ???

            # ---------------------------------------------------------------------------
            # 024: Identifier
            # ---------------------------------------------------------------------------

            with xml.datafield(tag='024', ind1='8', ind2=' '):
                xml.subfield(ident, code='a')
                xml.subfield('UIO_FUH', code='2')

            # ---------------------------------------------------------------------------
            # 040 Cataloging source
            # ---------------------------------------------------------------------------

            with xml.datafield(tag='040', ind1=' ', ind2=' '):
                xml.subfield('NoOU', code='a')
                xml.subfield('nob', code='b')
                xml.subfield('katreg', code='e')

            # ---------------------------------------------------------------------------
            # 100: Avsender
            # ---------------------------------------------------------------------------

            if 'avsender' not in row['personer']:
                # TODO: Hvordan koder vi det?
                sys.stderr.write('Mangler avsender: %s\n' % row['tilvekstnr'])
            else:
                with xml.datafield(tag='100', ind1='1', ind2=' '):
                    person = row['personer']['avsender']
                    aut = autoritetsdata.get(person['navn'], {'a': None, '0': None})
                    if aut['a'] is not None:
                        xml.subfield(aut['a'], code='a')
                    else:
                        xml.subfield(person['navn'], code='a')

                    xml.subfield('aut', code='4')
                    sender = person['navn']

                    if aut['0'] is not None:
                        aut_id = '(NO-TrBIB)%s' % aut['0']
                        xml.subfield(aut_id, code='0')

            # ---------------------------------------------------------------------------
            # 245: Tittel
            # ---------------------------------------------------------------------------

            # Eksempler fra Katalogiseringsregler 4.1B2
            #  - [Brev] 1926-11-04, Paris [til] Jappe Nilssen, Oslo
            #  - [Brev] 1901 March 6, Dublin [til] Henrik Ibsen, Kristiania
            # if receiver is
            # if sender is None:
            #     title = '[til] %s [fra ukjent avsender]' % rcpt
            # elif sender is not None and rcpt is not None:
            #     title = '[til] %s fra %s' % (rcpt, sender)
            # else:
            #     sys.stderr.write('ERR: %s : Ukjent mottaker!\n' % ident)
            #     title = 'til ukjent mottaker fra %s' % sender
            # if dato is None:
            #     title = 'Udatert brev %s' % title
            # else:
            #     title = 'Brev %s, datert %s' % (title, dato_s)
            title = '[Brev]'
            if dato is None:
                title += ' [u.d.]'  # TODO: Sjekk mot katregler
            else:
                dato_s = formater_dato(dato)
                title += ' ' + dato_s
            if sted_s is not None:
                title += ', ' + sted_s
            title += ' [til] Hansteen, Christopher'
            with xml.datafield(tag='245', ind1='0', ind2='0'):
                xml.subfield(title, code='a')

            # sys.stderr.write('%s\n' % title)

            # ---------------------------------------------------------------------------
            # 264: Sted og dato
            # ---------------------------------------------------------------------------

            if sted is not None or dato is not None:
                with xml.datafield(tag='264', ind1=' ', ind2='0'):
                    if sted is not None:
                        xml.subfield(sted_s, code='a')
                    if dato is not None:
                        xml.subfield(dato, code='c')

            # ---------------------------------------------------------------------------
            # 300: Fysisk beskrivelse
            # ---------------------------------------------------------------------------

            with xml.datafield(tag='300', ind1=' ', ind2=' '):
                npages = len(row['filer'])
                # TODO: Sjekke formatering mot katregler.
                #       Forside, bakside, x sider.., vedlegg, del 1, 2...
                xml.subfield('%d s.' % npages, code='a')

            # ---------------------------------------------------------------------------
            # 500: Noter
            # ---------------------------------------------------------------------------

            # TODO: Sjekk hva som skal i hvilket notefelt

            if row['datering_komm'] is not None:
                with xml.datafield(tag='500', ind1=' ', ind2=' '):
                    xml.subfield(row['datering_komm'], code='a')

            if row['stedkommentar'] is not None:
                with xml.datafield(tag='500', ind1=' ', ind2=' '):
                    xml.subfield(row['stedkommentar'], code='a')

            if row['motivbeskrivelse'] is not None:
                with xml.datafield(tag='500', ind1=' ', ind2=' '):
                    xml.subfield(row['motivbeskrivelse'], code='a')

            # ---------------------------------------------------------------------------
            # 535: Originalens plassering
            # ---------------------------------------------------------------------------

            with xml.datafield(tag='535', ind1='1', ind2=' '):
                # TODO: Fyll ut mer detaljert
                xml.subfield('Originalene befinner seg i: Observatoriets magasin', code='a')

            # ---------------------------------------------------------------------------
            # UAVKLARTE FELTER
            # ---------------------------------------------------------------------------

            # TODO:
            # with xml.datafield(tag='546', ind1=' ', ind2=' '):
            #     xml.subfield('Kan vi si noe om språk?', code='a')

            # ---------------------------------------------------------------------------
            # 700: Avsender
            # ---------------------------------------------------------------------------

            if 'mottaker' not in row['personer']:
                sys.stderr.write('Mangler mottaker: %s\n' % row['tilvekstnr'])
            else:
                with xml.datafield(tag='700', ind1='1', ind2=' '):
                    person = row['personer']['mottaker']
                    aut = autoritetsdata.get(person['navn'], {'a': None, '0': None})
                    if aut['a'] is not None:
                        xml.subfield(aut['a'], code='a')
                    else:
                        xml.subfield(person['navn'], code='a')

                    xml.subfield('rcp', code='4')
                    sender = person['navn']

                    if aut['0'] is not None:
                        aut_id = '(NO-TrBIB)%s' % aut['0']
                        xml.subfield(aut_id, code='0')

            # TODO:
            # YALE-guiden bruker 580, men er ikke 773 bedre? Eller?
            with xml.datafield(tag='773', ind1='0', ind2=' '):
                xml.subfield('Hansteens brevsamling', code='a')

            # TODO:
            # Avsendersted: Legge til som 751 med $4 prp f.eks.???

            # ---------------------------------------------------------------------------
            # 787: Alma collection ID
            # ---------------------------------------------------------------------------

            with xml.datafield(tag='787', ind1=' ', ind2=' '):
                xml.subfield('81218451430002204', code='w')

            # ---------------------------------------------------------------------------
            # 856: Filnavn
            # ---------------------------------------------------------------------------

            for fil in row['filer']:
                with xml.datafield(tag='856', ind1=' ', ind2=' '):
                    page_designation = fil['page_designation']
                    xml.subfield(page_designation, code='a')
                    xml.subfield(fil['filename'], code='u')

print(xml)
