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


files_folder = 'files'
filename_foto_kort = 'src/foto_kort.csv'
filename_filer = 'src/filer.csv'
filename_oversettelse = 'src/filer_oversettelse.csv'

# 1. The filenames in the 'files/' folder matches either the column "filnavn_a"
#    or "filnavn_b" in `filer_oversettelse.csv` table uniquely.
# 2.  From this match we find the `file_name`, which is the file name used in the
#     `filer.csv` table, from which we find the corresponding `foto_kort_id`,
#     which identifies the letter the file belongs to.



def format_page_designations(x):
    if x == '':
        return None

    if x == 'f':
        return 'Konvolutt-forside'

    if x == 'b':
        return 'Konvolutt-bakside'

    # Add spacing
    x = re.sub(r'([0-9])([a-z])', r'\1, \2', x)

    # Labels
    x = re.sub(r's([0-9]+)', r'side \1', x)
    x = re.sub(r'v([0-9]+)', r'vedlegg \1', x)
    x = re.sub(r'd([0-9]+)', r'del \1', x)

    x = x.capitalize()

    return x


def write_csv(filename, reader, rows):
    with open(filename, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# Create map: foto_kort_id -> tilvekstnr
tilvekstnr = {}
with open(filename_foto_kort) as fp:
    for row in csv.DictReader(fp):
        tilvekstnr[row['foto_kort_id']] = row['tilvekstnr']

# Create map: file_name -> foto_kort_id
foto_kort_id = {}
with open(filename_filer) as fp:
    for row in csv.DictReader(fp):
        foto_kort_id[row['file_name']] = row['foto_kort_id']


# Create filename maps
filnavn_map = {}  # Forward map: Baeyer010964b_2.tif (unique) -> USD_UNIHIST_BREV_2042953.tif (unique)
filnavn_map_r = {}   # Reverse map: USD_UNIHIST_BREV_2042953.tif (unique) -> Baeyer010964b_2.tif (unique)

letters = OrderedDict()
with open(filename_oversettelse) as fp:
    reader = csv.DictReader(fp)
    out = []
    for row in reader:
        usd_filename = row['file_name']
        real_filename = row['new_file_name']

        filnavn_map[real_filename] = usd_filename
        filnavn_map_r[usd_filename] = real_filename

        fkid = foto_kort_id[row['file_name']]
        if fkid not in tilvekstnr:
            sys.stderr.write('File %s is linked to a non-existent record %s!\n' % (usd_filename, fkid))
            continue

        ident = tilvekstnr[fkid]

        m = re.match(r'(.*?)((v[0-9]?)?([abfs]{1,2}[0-9]{0,3})?(d[0-9])?)(_[0-9])?\.tif', real_filename)
        if m is None:
            sys.stderr.write('Inconsistent data: %s\n' % real_filename)
            continue

        fn_part = m.group(1)
        page_part = m.group(2)

        if len(page_part) != 0:
            new_fname = '%s_%s.tif' % (ident, page_part)
        else:
            new_fname = '%s.tif' % (ident,)

        if new_fname != real_filename:
            if os.path.exists(os.path.join(files_folder, new_fname)):
                sys.stderr.write('Won\'t overwrite %s → %s\n' % (real_filename, new_fname))
            else:
                sys.stderr.write('Rename %s -> %s\n' % (real_filename, new_fname))
                row['new_file_name'] = new_fname
                os.rename(
                    os.path.join(files_folder, real_filename),
                    os.path.join(files_folder, new_fname)
                )

        if not os.path.exists(os.path.join(files_folder, new_fname)):
            sys.stderr.write('ERR: File not found: %s\n' % os.path.join(files_folder, new_fname))

        out.append(row)

        label = format_page_designations(page_part)
        if label is None or label == '':
            sys.stderr.write('ERR: Couldn\'t generate label for %s\n' % new_fname)

        letters[ident] = letters.get(ident, []) + [{
            'filename': new_fname,
            'label': label
        }]

    write_csv('tmp.csv', reader, out)

os.rename('tmp.csv', filename_oversettelse)

sys.stderr.write('Verified validity of all filenames\n')

for k in letters:
    letters[k] = sorted(letters[k], key=lambda page: page['label'])

def sha1sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

rows = []
for ident, pages in tqdm(letters.items()):
    for page in pages:
        path = os.path.join(files_folder, page['filename'])
        page['filesize'] = os.path.getsize(path)
        page['mimetype'] = magic.from_file(path, mime=True)
        page['sha1'] = sha1sum(path)


print(json.dumps(letters, indent=3))
