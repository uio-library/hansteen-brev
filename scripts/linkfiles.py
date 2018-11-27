# Link TIFF files to the letter identifiers
# Usage:  python scripts/linkfiles.py files > build/filelinks.json
#
import sys
import os
import re
import csv
import json
import xmlwitch
from copy import copy
from glob import glob
from datetime import datetime

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
    if row['filnavn_a'] != '' and row['filnavn_b'] != '':
        sys.stderr.write('ERR: Inconsistent data!\n')
    elif row['filnavn_a'] != '':
        real_filename = row['filnavn_a']
    elif row['filnavn_b'] != '':
        real_filename = row['filnavn_b']
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

rows = []
for letter_id, real_filenames in brev_map.items():
    for real_filename in real_filenames:
        m = re.match(r'(.*?)((v[0-9])?([bfs][0-9]{0,2})?(d[0-9])?)(_2)?\.tif', real_filename)
        if m is None:
            sys.stderr.write('Inconsistent data!\n')
            sys.exit(1)
        fn_part = m.group(1)
        page_part = m.group(2)
        rows.append([letter_id, real_filename, fn_part, page_part])

rows = sorted(rows, key=lambda x: (int(x[0]), x[3]))


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

from collections import OrderedDict
out = OrderedDict([])
for row in rows:
    if row[0] not in out:
        out[row[0]] = []

    pd = format_page_designations(row[3])
    out[row[0]].append({'filename': row[1], 'basename': row[2], 'page_designation': pd})

print(json.dumps(out, indent=3))
