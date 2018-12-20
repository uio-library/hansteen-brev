import json
import re

filename = 'src/hansteen.json'

def sortkey(x):
    if x['label'] is None:
        return ''
    lab = x['label'].lower()
    lab = re.sub(r'ide ([1-9])(?![0-9])', r'ide 0\1', lab)  # Add 0 prefix to single numbers

    if lab == 'konvoluttbakside':
        return 'konvoluttg'  # etter forside

    return lab

labels = set()
with open(filename, 'r') as fp:
    data = json.load(fp)
    for letter in data:
        for page in letter['structure']:
            labels.add(page['label'])

        letter['structure'] = sorted(letter['structure'], key=sortkey)

for x in labels:
    print(x)

with open(filename, 'w') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)
