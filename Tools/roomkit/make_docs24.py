"""The 25 notes of the twenty-fourth batch, from scps_b24.py: summaries in our own words of SCP Wiki articles
(CC BY-SA 3.0); each note names its source."""
from make_docs20 import note
from scps_b24 import SCPS

TITLES = {'doc24_' + n: 'SCP-%s Summary' % n for n, *_ in SCPS}


def docs():
    for n, cls, kind, col, desc, cont, rem, *_ in SCPS:
        note('doc24_' + n, n, cls, desc, cont, rem)


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
