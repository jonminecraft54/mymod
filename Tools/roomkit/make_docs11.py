"""The three handwritten notes of the eleventh batch (GFX\\items\\<name>.jpg), drawn by make_docs2.note().
Names end in b so wire11.py gives them the note texture, as the other handwritten documents have."""
from make_docs2 import note
from rooms_b11 import TEXTS

TITLES = {
    'docho1b': 'Hoist Office Operator Log',
    'docshut1b': 'Shutter 4 Closure Record',
    'docmach1b': 'Machine Alcove Service Memo',
}

if __name__ == '__main__':
    for name, (rows, sign) in TEXTS.items():
        note(name, rows, sign=sign)
    assert set(TEXTS) == set(TITLES), (set(TEXTS) ^ set(TITLES))
    print('%d notes written' % len(TEXTS))
