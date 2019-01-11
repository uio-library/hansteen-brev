# This script uses the National Library URN service to generate URNs
# pointing to the Alma Delivery URL for any letter that do not have a URN.
#
# Usage:
#
# Authentication must be provided through the environment variables
# URN_USER and URN_PASSWORD.
#

import os
import sys
import json
import dotenv
from collections import OrderedDict
from zeep import Client
from dotenv import load_dotenv

load_dotenv()

ws_url = 'https://www.nb.no/idtjeneste/ws?wsdl'
urn_series = 'URN:NBN:no'
username = os.getenv('URN_USER')
password = os.getenv('URN_PASSWORD')

if username is None or password is None:
    print('Please provide username and password')
    sys.exit(1)

client = Client(ws_url)
service = client.service
session_token = service.login(username, password)

def load_collection():
    with open('src/hansteen.json') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)

def store_collection(collection):
    with open('src/hansteen.json', 'w') as fp:
        json.dump(collection, fp, indent=2, ensure_ascii=False)

def create_urn(url):
    info = service.createURN(session_token, urn_series, url)
    return info['URN']

def replace_url(urn, old_value, new_value):
    info = service.replaceURL(session_token, urn, old_value, new_value);
    print(info)


collection = load_collection()

for idx, letter in enumerate(collection['members']):
    letter_props = list(letter.items())

    if 'urn' not in letter:

        print('Generating URN for letter %s' % letter['id'])

        # Generate URN
        delivery_url = 'https://bibsys-k.alma.exlibrisgroup.com/view/delivery/47BIBSYS_UBO/%s' % letter['alma_representation_id']
        urn = create_urn(delivery_url)
        print('Generated URN: %s' % urn)

        # Insert the URN prop right after the alma_representation_id
        letter_props.insert(3, ('urn', urn))

        # Store collection after each new URN to avoid loosing any URNs
        # in the case of an exception later on.
        letter = OrderedDict(letter_props)
        collection['members'][idx] = letter
        store_collection(collection)

    elif 'urn' in letter:

        old_url = 'https://bibsys-k.alma.exlibrisgroup.com/view/delivery/47BIBSYS_UBO/%s' % letter['alma_representation_id']
        new_url = 'https://bibsys-k.alma.exlibrisgroup.com/view/delivery/47BIBSYS_UBO/%s' % letter['alma_id']
        replace_url(letter['urn'], old_url, new_url)
        print('Replace URL for URN %s' % letter['urn'])

