"""The notes of the thirty-fourth batch: the registry of each deep storage area, six SCPs to a page, each with a
one-line summary in our own words (from data34.py); and short titles for the ten items."""
from make_docs2 import typed
from data34 import U

AREA = {'A': ('06', 'Humanoid storage'), 'B': ('07', 'Object storage'), 'C': ('08', 'Biological storage'),
        'D': ('09', 'Site-45 records')}
PER = 6
PAGES = {}
for k, (n, what) in AREA.items():
    units = [u for u in U if u['room'] == k]
    PAGES[k] = [units[i:i + PER] for i in range(0, len(units), PER)]
TITLES = {}
for k, (n, what) in AREA.items():
    for p in range(len(PAGES[k])):
        TITLES['docarea%sp%d' % (n, p + 1)] = 'Storage Area %s Registry (%d/%d)' % (n, p + 1, len(PAGES[k]))
DOCS = list(TITLES)
TITLES.update({'dice1974': 'SCP-1974-EX (d20s)', 'pills3866': 'SCP-3866 (Tablets)', 'stapler3709': 'SCP-3709 (Stapler)',
               'cards3803': 'SCP-3803 (Card Case)', 'book1841': 'SCP-1841', 'grapes1255': 'SCP-1255 (Grapes)',
               'caps4193': 'SCP-4193 (Caplets)', 'tabs5604': 'SCP-5604 (Tablets)', 'cereal2983': 'SCP-2983',
               'camera5701': 'SCP-5701 (Camera)'})


def docs():
    for k, (n, what) in AREA.items():
        pages = PAGES[k]
        for p, chunk in enumerate(pages):
            body = [('h', 'Deep Storage Area %s - %s' % (n, what))]
            for u in chunk:
                t = u['text'] if len(u['text']) < 120 else u['text'][:117].rsplit(' ', 1)[0] + '...'
                body.append(('p', 'SCP-%s (%s): %s' % (u['num'], u['cls'], t)))
            if p == len(pages) - 1:
                body.append(('p', 'Summaries of scp-wiki.wikidot.com articles (CC BY-SA 3.0).'))
            typed('docarea%sp%d' % (n, p + 1), [('Area', 'Deep Storage %s' % n), ('Page', '%d of %d' % (p + 1, len(pages))),
                                                ('Clearance Level', '3')], body)


if __name__ == '__main__':
    docs()
    print('%d registry pages' % len(DOCS))
