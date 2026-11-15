"""The notes of the thirty-fifth batch: the registries of Storage Areas 10 (the cell block) and 11 (the bunker), six
SCPs to a page, one-line summaries in our own words (from data35.py); short titles for the four items."""
from make_docs2 import typed
from data35 import U

AREA = {'E': ('10', 'The cell block'), 'F': ('11', 'The bunker')}
PER = 6
PAGES = {k: [[u for u in U if u['room'] == k][i:i + PER] for i in range(0, len([u for u in U if u['room'] == k]), PER)]
         for k in AREA}
TITLES = {}
for k, (n, what) in AREA.items():
    for p in range(len(PAGES[k])):
        TITLES['docarea%sp%d' % (n, p + 1)] = 'Storage Area %s Registry (%d/%d)' % (n, p + 1, len(PAGES[k]))
DOCS = list(TITLES)
TITLES.update({'hat2890': 'SCP-2890 (Top Hat)', 'brush2816': 'SCP-2816 (Paintbrushes)', 'briefs1388': 'SCP-1388',
               'watch1912': 'SCP-1912 (Pocket Watch)'})


def docs():
    for k, (n, what) in AREA.items():
        for p, chunk in enumerate(PAGES[k]):
            body = [('h', 'Storage Area %s - %s' % (n, what))]
            for u in chunk:
                t = u['text'] if len(u['text']) < 120 else u['text'][:117].rsplit(' ', 1)[0] + '...'
                body.append(('p', 'SCP-%s (%s): %s' % (u['num'], u['cls'], t)))
            if p == len(PAGES[k]) - 1:
                body.append(('p', 'Summaries of scp-wiki.wikidot.com articles (CC BY-SA 3.0).'))
            typed('docarea%sp%d' % (n, p + 1), [('Area', 'Storage %s' % n), ('Page', '%d of %d' % (p + 1, len(PAGES[k]))),
                                                ('Clearance Level', '3')], body)


if __name__ == '__main__':
    docs()
    print('%d registry pages' % len(DOCS))
