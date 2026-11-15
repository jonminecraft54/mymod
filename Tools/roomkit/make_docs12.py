"""The handwritten note of the twelfth batch (GFX\\items\\<name>.jpg), drawn by make_docs2.note().
The name ends in b so wire12.py gives it the note texture, as the other handwritten documents have."""
from make_docs2 import note
from rooms_b12 import TEXTS

TITLES = {
    'docbal1b': 'Cell Block C Gallery Log',
}

if __name__ == '__main__':
    for name, (rows, sign) in TEXTS.items():
        note(name, rows, sign=sign)
    assert set(TEXTS) == set(TITLES), (set(TEXTS) ^ set(TITLES))
    print('%d notes written' % len(TEXTS))
