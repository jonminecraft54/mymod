"""The notes of the twenty-fifth batch, from scps_b25.py (summaries of SCP Wiki articles, CC BY-SA 3.0), and the
office suite's memo."""
from make_docs2 import typed
from make_docs20 import note
from scps_b25 import SCPS

TITLES = {'doc25_' + n: 'SCP-%s Summary' % n for n, *_ in SCPS}
TITLES['doc25_office'] = 'Office Suite Memo'


def docs():
    for n, cls, kind, col, desc, cont, rem, *_ in SCPS:
        note('doc25_' + n, n, cls, desc, cont, rem)
    typed('doc25_office', [('Clearance Level', '2'), ('Item #', 'Offices'), ('Object Class', 'Memo')], [
        ('h', 'To all staff in this suite'),
        ('p', 'The intercom will page you when a block needs a check. Records are west, the break room is west too, '
              'and the hoist panel in the control room is not a toy.'),
        ('p', '{Whoever keeps taking batteries from the break room: we know.}')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
