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
import argparse

locale.setlocale(locale.LC_ALL, 'no_NO.UTF-8')


# Current date and time with 1 millisecond digit, as required by the MARC21 005 field
current_datetime = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f')[:16]
current_datetime = '20181127225134.9'  # Fix while testing, TODO: REMOVE THIS LINE


def format_date(dato):

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


def build(metadata, authorities, filename=None):

    # Ex: build('build/{id}/record.xml')
    if filename is None:
        xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
        with xml.collection:
            for row in metadata:
                build_doc(xml, row, authorities)
        print(xml)
    else:
        for row in metadata:
            xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
            build_doc(xml, row, authorities)
            fn = filename.format(**row)
            if not os.path.exists(os.path.dirname(fn)):
                os.mkdir(os.path.dirname(fn))
            with open(fn, 'w') as fd:
                fd.write(str(xml))


def build_doc(xml, row, authorities):
    # Unik identifikator
    ident = row['id']

    with xml.record:

        desc = row['descriptive']

        # Bearbeid dato
        if desc['date'] is None:
            dato = None
            year = 'uuuu'
            dato_type = 'n'  # Ukjent
        else:
            dato = desc['date'].replace('x', 'u').strip()
            if re.match(r'^[0-9]{4}-[0-9]{2}', dato):
                dato_type = 'e'  # Detaljert dato
            else:
                dato_type = 's'  # Kun år
            year = dato[:5]

        # Bearbeid sted
        place = None
        place_s = None
        if len(desc['places']) == 1:
            place = desc['places'][0]
            #if place['place'] is not None and place['country'] is not None:
            #    place_s = '%s, %s' % (place['place'], place['country'])
            if place['place'] is not None:
                place_s = place['place']
            else:
                place_s = place['country']
        elif len(desc['places']) > 1:
            sys.stderr.write('%s : Knyttet til flere steder!\n' % ident)

        # ---------------------------------------------------------------------------
        # LDR
        # ---------------------------------------------------------------------------

        ldr = [' ' for c in range(24)] # Start with a blank 24-character string
        ldr[5]  = 'n'  # Record status: New
        ldr[6]  = 't'  # Type of record: Manuscript language material
        ldr[7]  = 'm'  # Bibliographic level: Monograph/Item
        ldr[9]  = 'a'  # Character coding scheme: UCS/Unicode
        ldr[18] = 'c'  # Descriptive cataloging form: ISBD punctuation omitted
        ldr[20:24] = '4500'  # Alma vil gjerne ha dette
        xml.leader(''.join(ldr))

        # ---------------------------------------------------------------------------
        # 005: Date and Time of Latest Transaction
        # ---------------------------------------------------------------------------

        xml.controlfield(current_datetime, tag='005')

        # ---------------------------------------------------------------------------
        # 007 Physical Description Fixed Field
        # ---------------------------------------------------------------------------

        # Vi bruker 'tz' fremfor 'ta' siden brevene ikke er trykt.
        xml.controlfield('tz', tag='007')

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
            f008[7:11] = dato[:4]
        else:
            # Dates unknown
            f008[6] = 'n'
            f008[7:15] = 'uuuuuuuu'

        f008[15:18] = 'xx '  # No place, unknown, or undetermined

        f008[18:35] = '|||||||||||||||||'  # no attempt to code
        f008[28] = ' '  # Not a government publication
        f008[29] = '0'  # Not a conference publication
        f008[30] = '0'  # Not a conference publication
        f008[33] = 'i'  # Literary form: letter

        # Språk er ikke katalogisert, så setter denne foreløpig som 'ukjent'.
        f008[35:38] = '   '

        f008[38] = '|'  # Modified record: no attempt to code

        f008[39] = 'd'  # Cataloging source: Other, more info in 040.

        if len(f008) != 40:
            sys.stderr.write('Field 008 has wrong length afte processing: %d\n' % len(f008))

        xml.controlfield(''.join(f008), tag='008')

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

        if 'correspondent' not in desc['agents']:
            sys.stderr.write('%s: Correspondent missing\n' % row['id'])
        else:
            with xml.datafield(tag='100', ind1='1', ind2=' '):
                agent = desc['agents']['correspondent']
                aut = authorities.get(agent['name'], {'a': None, '0': None})
                if aut['a'] is not None:
                    xml.subfield(aut['a'], code='a')
                else:
                    xml.subfield(agent['name'], code='a')

                xml.subfield('crp', code='4')

                if aut['0'] is not None:
                    aut_id = '(NO-TrBIB)%s' % aut['0']
                    xml.subfield(aut_id, code='0')

        # ---------------------------------------------------------------------------
        # 245: Tittel
        # ---------------------------------------------------------------------------

        # Eksempler fra Katalogiseringsregler 4.1B2
        #  - [Brev] 1926-11-04, Paris [til] Jappe Nilssen, Oslo
        #  - [Brev] 1901 March 6, Dublin [til] Henrik Ibsen, Kristiania

        title = '[Brev]'
        if dato is None:
            title += ' [Udatert]'
        else:
            dato_s = format_date(dato)
            title += ' ' + dato_s
        if place_s is not None:
            title += ', ' + place_s
        title += ' [til] Hansteen, Christopher'
        with xml.datafield(tag='245', ind1='0', ind2='0'):
            xml.subfield(title, code='a')
            if 'correspondent' in desc['agents']:
                xml.subfield('[fra] ' + desc['agents']['correspondent']['name'], code='c')

        # ---------------------------------------------------------------------------
        # 264: Sted og dato
        # ---------------------------------------------------------------------------

        if place is not None or dato is not None:
            with xml.datafield(tag='264', ind1=' ', ind2='0'):
                if place is not None:
                    xml.subfield(place_s, code='a')
                if dato is not None:
                    xml.subfield(dato, code='c')

        # ---------------------------------------------------------------------------
        # 300: Fysisk beskrivelse
        # ---------------------------------------------------------------------------

        with xml.datafield(tag='300', ind1=' ', ind2=' '):
            npages = len(row['structure'])
            xml.subfield('%d s.' % npages, code='a')

        # SPØRSMÅL: Nå oppgir vi bare antall sider (eks.: "3 s."), men i
        #    mange tilfeller har vi informasjon om at sider er forside/bakside,
        #    vedlegg, del 1, 2, ... Er det ønskelig å kode denne informasjonen,
        #    og isåfall hvordan?


        # ---------------------------------------------------------------------------
        # 500: Merknader
        # ---------------------------------------------------------------------------

        # SPØRSMÅL: Er 500 greit for disse, eller er det et annet felt som er bedre?
        #    Tredie Bidrag til geographiske Længdebestemmelser
        #    Vedlegg til brev av samme dato
        #    Vedlegg til brev av samme dato
        #    Vedlegg til brev av samme dato
        #    Telegram
        #    Første vedlegg til brev av samme dato
        #    Vedlegg til brev av samme dato
        #    Første vedlegg til brev av samme dato
        #    Andre vedlegg til brev av samme dato
        #    Artikkel av J. J. Aastrand.
        if desc['comment'] is not None:
            with xml.datafield(tag='500', ind1=' ', ind2=' '):
                xml.subfield(desc['comment'], code='a')

        # Dateringskommentar
        if desc['date_comment'] is not None:
            with xml.datafield(tag='500', ind1=' ', ind2=' '):
                xml.subfield('Datering: ' + desc['date_comment'], code='a')

        # Stedkomentar
        if place is not None and place['comment'] is not None:
            with xml.datafield(tag='500', ind1=' ', ind2=' '):
                xml.subfield('Sted: ' + place['comment'], code='a')

        # ---------------------------------------------------------------------------
        # 535: Originalens plassering
        # ---------------------------------------------------------------------------

        with xml.datafield(tag='535', ind1='1', ind2=' '):
            xml.subfield('Christopher Hansteens korrespondanse', code='3')
            xml.subfield('Observatoriet', code='a')
            xml.subfield('Observatoriegata 1, Oslo', code='b')
            xml.subfield('no', code='g')

        # ---------------------------------------------------------------------------
        # 540 / 542: Tilgang
        # ---------------------------------------------------------------------------

        with xml.datafield(tag='540', ind1=' ', ind2=' '):
            xml.subfield('Falt i det fri', code='a')

        with xml.datafield(tag='542', ind1=' ', ind2=' '):
            if 'u' not in year:
                # SPØRSMÅL:
                # Hansteen døde i 1873, så brevene med ukjent årstall må være
                # produsert senest 1873. Kan vi kode dette på noen måte?
                xml.subfield(year, code='j')  # Year of creation for an unpublished resource
            xml.subfield('Falt i det fri', code='l')  # Copyright status
            xml.subfield('Upublisert', code='m')  # Whether the item is published or unpublished

        # ---------------------------------------------------------------------------
        # 700: Mottaker
        # ---------------------------------------------------------------------------

        if 'addressee' not in desc['agents']:
            sys.stderr.write('%s: Addressee missing\n' % row['id'])
        else:
            with xml.datafield(tag='700', ind1='1', ind2=' '):
                agent = desc['agents']['addressee']
                aut = authorities.get(agent['name'], {'a': None, '0': None})
                if aut['a'] is not None:
                    xml.subfield(aut['a'], code='a')
                else:
                    xml.subfield(agent['name'], code='a')

                xml.subfield('rcp', code='4')

                if aut['0'] is not None:
                    aut_id = '(NO-TrBIB)%s' % aut['0']
                    xml.subfield(aut_id, code='0')

        # ---------------------------------------------------------------------------
        # 751: Avsendersted
        # ---------------------------------------------------------------------------

        # SPØRSMÅL:
        # Gir det mening å putte dette i 751?
        # Gir det mening med $4 prp? Har vi evt. en bedre kode?
        if place is not None:
            with xml.datafield(tag='751', ind1=' ', ind2=' '):
                xml.subfield(place_s, code='a')
                xml.subfield('prp', code='4')

        # ---------------------------------------------------------------------------
        # 773: Samling (lenkefelt)
        # ---------------------------------------------------------------------------

        # Vi kan evt. også generere en 580-note.
        with xml.datafield(tag='773', ind1='0', ind2=' '):
            xml.subfield('Christopher Hansteens korrespondanse', code='t')

        # ---------------------------------------------------------------------------
        # 787: Alma collection ID
        # ---------------------------------------------------------------------------

        with xml.datafield(tag='787', ind1='1', ind2=' '):
            xml.subfield('81218451430002204', code='w')

        # ---------------------------------------------------------------------------
        # 856: Filnavn
        # ---------------------------------------------------------------------------
        # Brukes av Alma for å avgjøre hvilke filer som hører til hvilke MARC-poster.

        for page in row['structure']:
            with xml.datafield(tag='856', ind1='4', ind2='0'):
                # xml.subfield('ub-media.uio.no', code='a')        # Host
                # xml.subfield('/arkiv/hansteen/files/', code='d') # Path
                xml.subfield(page['filename'], code='f')         # Filename
                xml.subfield('image/tiff', code='q')             # Electronic format type
                xml.subfield(page['label'], code='y')            # Link text
                if 'filesize' in page:
                    xml.subfield(str(page['filesize']), code='s')     # File size


def main():
    parser = argparse.ArgumentParser(description='Build MARCXML from JSON file')
    parser.add_argument('-a', '--authorities', nargs='?', dest='autfile', help='Authorities JSON file')
    parser.add_argument('infile', help='Input JSON file')
    parser.add_argument('-o', '--out', nargs='?', dest='outfile',
                        help='Output MARC filename pattern (leave blank to output to stdout)')
    args = parser.parse_args()

    authorities = []
    if args.autfile is not None:
        with open(args.autfile) as fp:
            authorities = json.load(fp)

    with open(args.infile) as fp:
        metadata = json.load(fp)

    build(metadata, authorities, args.outfile)

if __name__ == '__main__':
    main()
