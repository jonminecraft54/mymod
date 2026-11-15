"""Sanity check for a generated batch (default: the sixteen-SCP batch; or: check_s16.py b6_names.txt IndevS13.bb IndevS13Data.bb): every room file parses again, and every texture, prop
model, sound, item template and document image the rooms and IndevS16*.bb refer to exists."""
import os
import re
from rmesh import read_rmesh

G = 'I:/MythicalC v1.2.7/v0.1/scpcb-dx9/scpcb-dx9/'
BS = chr(92)


def strings(obj, out):
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            strings(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            strings(v, out)


bad = 0
import sys
NAMES_FILE, BB = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 2 else ('s16_names.txt', ['IndevS16.bb', 'IndevS16Data.bb'])
names = [l.strip() for l in open(NAMES_FILE) if l.strip()]
for n in names:
    d = read_rmesh(G + 'GFX/map/' + n + '.rmesh')
    found = []
    strings(d, found)
    files = sorted({s for s in found if re.search(r'\.(jpg|png|x|b3d)$', s, re.I)})
    for s in files:
        ok = os.path.exists(G + 'GFX/map/' + s) or os.path.exists(G + 'GFX/map/Props/' + s)
        if not ok:
            print('MISSING', n, s)
            bad += 1
    print('%-14s parses, %2d files referenced, %6d bytes, lightmap %s' % (
        n, len(files), os.path.getsize(G + 'GFX/map/' + n + '.rmesh'), os.path.exists(G + 'GFX/map/' + n + '_lm1.png')))

src = ''.join(open(G + b, encoding='latin-1').read() for b in BB)
for f in sorted(set(re.findall(r'"((?:GFX|SFX)[^"]+)"', src))):
    if not os.path.splitext(f)[1]:
        print('  (name completed at run time)', f)
        continue
    if not os.path.exists(G + f.replace(BS, '/')):
        print('MISSING FILE', f)
        bad += 1
for stem, rng in (('SFX/SCP/860/Cancer%d.ogg', range(0, 6)), ('SFX/General/Slash%d.ogg', (1, 2))):
    for i in rng:
        if not os.path.exists(G + stem % i):
            print('MISSING FILE', stem % i)
            bad += 1
items = set(re.findall(r'IV1Item\(r, "([^"]+)"', src)) | set(re.findall(r'IS16Give\("([^"]+)"', src))
ini = open(G + 'Data/items.ini', encoding='latin-1').read().lower()
strs = open(G + 'Data/strings.ini', encoding='latin-1').read().lower()
for i in sorted(items):
    if '[' + i.lower() + ']' not in ini:
        print('NO ITEM TEMPLATE', i)
        bad += 1
    if i.startswith('doc'):
        if not os.path.exists(G + 'GFX/items/' + i + '.jpg'):
            print('NO DOC IMAGE', i)
            bad += 1
        if (i + ' = ') not in strs:
            print('NO DISPLAY NAME', i)
            bad += 1
print('%d item names checked, %d problems' % (len(items), bad))
