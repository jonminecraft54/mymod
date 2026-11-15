"""The three handwritten notes of the tenth batch (GFX\\items\\<name>.jpg), drawn by make_docs2.note().
Names end in b so wire10.py gives them the note texture, as the other handwritten documents have."""
from make_docs2 import note
from rooms_b10 import TEXTS

TITLES = {
    'docres1b': 'Research Office Last Entry',
    'docmed1b': 'Medical Bay Record',
    'docelev1b': 'Lift 3 Maintenance Log',
}

if __name__ == '__main__':
    for name, (rows, sign) in TEXTS.items():
        note(name, rows, sign=sign)
    assert set(TEXTS) == set(TITLES), (set(TEXTS) ^ set(TITLES))
    print('%d notes written' % len(TEXTS))
