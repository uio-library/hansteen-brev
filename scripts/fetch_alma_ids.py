# This scripts adds Alma MMS id and Alma Digital Representation ID to letters
# that do not have these. The letters are matched based on the local 'id' that
# is stored in 024 in the MARC records. The script assumes there's only one
# digital representation and will warn if there's more.
#
# Usage:
#
# An ALMA API key with read access to Bibs must be provided as an
# environment variable ALMA_KEY.

import os
import json
import requests
from lxml import etree
from collections import OrderedDict
from itertools import islice
from dotenv import load_dotenv

load_dotenv()

def get_all(session, url, top_key):
    # Iterator that handles pagination
    offset = 0
    total = 1
    batch_size = 100
    while offset < total:
        res = session.get(url, params={
            'offset': offset,
            'limit': batch_size
        }).json()
        total = res['total_record_count']
        for bib in res[top_key]:
            yield bib
            offset += 1

def load_collection():
    with open('src/hansteen.json') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)

def store_collection(collection):
    with open('src/hansteen.json', 'w') as fp:
        json.dump(collection, fp, indent=2, ensure_ascii=False)

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def get_bibs(session, collection_id):
    for bibs in chunk(get_all(session, 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/collections/%s/bibs' % collection_id, 'bib'), 100):
        mms_ids = [x['mms_id'] for x in bibs]
        res = session.get('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs', params={
            'mms_id': ','.join(mms_ids)
        }).json()

        for bib in res['bib']:
            bib['representations'] = session.get('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/%(mms_id)s/representations' % {
                'mms_id': bib['mms_id']
            }).json()['representation']

            for rep in bib['representations']:
                rep['files'] = session.get('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/%(mms_id)s/representations/%(pid)s/files' % {
                    'mms_id': bib['mms_id'],
                    'pid': rep['id']
                }).json()['representation_file']

            yield bib

# ---

apikey = os.getenv('ALMA_KEY')

session = requests.Session()
session.headers['Authorization'] = 'apikey %s' % apikey
session.headers['Accept'] = 'application/json'

collection_file = 'src/hansteen.json'
collection = load_collection()
collection_id = collection['collection']['alma_id']

for bib in get_bibs(session, collection_id):

    marc = bib['anies'][0].replace('encoding="UTF-16"', 'encoding="UTF-8"')
    xml = etree.fromstring(marc.encode('utf-8'))
    val = xml.xpath('.//datafield[@tag="024"]/subfield[@code="a"]/text()')
    local_id = val[0]

    print('CHECK ' + bib['mms_id'])

    out = []
    for letter in collection['members']:
        x = list(letter.items())
        if letter['id'] == local_id:
            if 'alma_id' not in letter:
                # Insert right after id
                print('ADD alma_id')
                x.insert(1, ('alma_id', mms_id))
            if 'alma_representation_id' not in letter:
                if len(bib['representations']) > 1:
                    print('WARN: More than one digital representation!')
                rep_id = bib['representations'][0]['id']
                # Insert right after alma_id
                print('ADD alma_representation_id')
                x.insert(2, ('alma_representation_id', rep_id))

            for local_file in letter['structure']:
                for alma_file in bib['representations'][0]['files']:
                    if local_file['filename'] == alma_file['path'].split('/')[-1]:
                        local_file['alma_id'] = alma_file['pid']

            letter = OrderedDict(x)
        out.append(letter)
    collection['members'] = out

store_collection(collection)
