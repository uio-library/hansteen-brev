# Link TIFF files to the letter identifiers
# Usage:  python scripts/linkfiles.py files > build/filelinks.json
#
import sys
import os
import re
import csv
import json
from tqdm import tqdm
import xmlwitch
from copy import copy
from glob import glob
from datetime import datetime
import magic
import hashlib
from collections import OrderedDict


files_folder = sys.argv[1]

# 1. The filenames in the 'files/' folder matches either the column "filnavn_a"
#    or "filnavn_b" in `filer_oversettelse.csv` table uniquely.
# 2.  From this match we find the `file_name`, which is the file name used in the
#     `filer.csv` table, from which we find the corresponding `foto_kort_id`,
#     which identifies the letter the file belongs to.
csv_filer_oversettelse = 'src/filer_oversettelse.csv'
csv_filer = 'src/filer.csv'


def get_table_rows(path):
    with open(path) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield row


# Create filename maps
filnavn_map = {}  # Forward map: Baeyer010964b_2.tif (unique) -> USD_UNIHIST_BREV_2042953.tif (unique)
filnavn_map_r = {}   # Reverse map: USD_UNIHIST_BREV_2042953.tif (unique) -> Baeyer010964b_2.tif (unique)
for row in get_table_rows(csv_filer_oversettelse):
    usd_filename = row['file_name']
    if row['new_file_name'] != '':
        real_filename = row['new_file_name']
    else:
        sys.stderr.write('ERR: Inconsistent data!\n')

    filnavn_map[real_filename] = usd_filename
    filnavn_map_r[usd_filename] = real_filename

brev_map = {}
brev_map_r = {}
for row in get_table_rows(csv_filer):
    brev_id = row['foto_kort_id']
    usd_filename = row['file_name']
    real_filename = filnavn_map_r[usd_filename]
    if brev_id not in brev_map:
        brev_map[brev_id] = []
    brev_map[brev_id].append(real_filename)
    if real_filename in brev_map_r:
        sys.stderr.write('ERR, duplicate: %s\n' % real_filename)
    brev_map_r[real_filename] = brev_id

sys.stderr.write('%d files mapped to %d letters\n' % (len(brev_map_r.keys()), len(brev_map)))

# Check that all files are actually found
for real_filename in brev_map_r.keys():
    fp = 'files/' + real_filename
    if not os.path.exists(fp):
        sys.stderr.write('ERR: File not found: files/%s\n' % real_filename)

sys.stderr.write('Verified file existence\n')


def sha1sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def format_page_designations(x):
    if x == '':
        return None

    if x == 'f':
        return 'Forside'

    if x == 'b':
        return 'Bakside'

    # Add spacing
    x = re.sub(r'([0-9])([a-z])', r'\1, \2', x)

    # Labels
    x = re.sub(r's([0-9]+)', r'side \1', x)
    x = re.sub(r'v([0-9]+)', r'vedlegg \1', x)
    x = re.sub(r'd([0-9]+)', r'del \1', x)

    x = x.capitalize()

    return x


rows = []
for letter_id, real_filenames in tqdm(brev_map.items()):
    for real_filename in real_filenames:
        path = 'files/' + real_filename
        m = re.match(r'(.*?)((v[0-9])?([abfs]{1,2}[0-9]{0,2})?(d[0-9])?)(_2)?\.tif', real_filename)
        if m is None:
            sys.stderr.write('Inconsistent data!\n')
            sys.exit(1)
        fn_part = m.group(1)
        page_part = m.group(2)
        filesize = os.path.getsize(path)
        mimetype = magic.from_file(path, mime=True)
        checksum = sha1sum(path)
        page_part = format_page_designations(page_part)
        rows.append({
            'letter_id': int(letter_id),
            'filename': real_filename,
            'basename': fn_part,
            'label': page_part,
            'filesize': filesize,
            'mimetype': mimetype,
            'sha1': checksum,
        })

rows = sorted(rows, key=lambda row: (row['letter_id'], page_part))

out = OrderedDict([])
for row in rows:
    letter_id = row['letter_id']
    if letter_id not in out:
        out[letter_id] = []

    del row['letter_id']
    out[letter_id].append(row)

print(json.dumps(out, indent=3))
