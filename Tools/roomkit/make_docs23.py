"""SCP-6483's notes: short summaries in our own words of scp-wiki.wikidot.com/scp-6483 (CC BY-SA 3.0)."""
from make_docs2 import typed

TITLES = {'doc23_6483': 'SCP-6483 Summary', 'doc23_coix': 'SCP-6483 Psychology Note'}
SRC = 'Summary of scp-wiki.wikidot.com/scp-6483 (CC BY-SA 3.0).'


def docs():
    typed('doc23_6483', [('Clearance Level', '3'), ('Item #', 'SCP-6483'), ('Object Class', 'Integrated')], [
        ('h', 'Description'),
        ('p', 'SCP-6483, Nicolas Roberts, is a 67-year-old Class IV reality bender who has only ever used his abilities '
              'for Christmas: decorating rooms, changing into a Santa suit, laying out holiday meals, giving small '
              'gifts, and travelling to the poles. Several at once make a Nativitatis Event: a Christmas supper, '
              'then on to the next place.'),
        ('h', 'Containment'),
        ('p', 'A microscale Scranton Reality Anchor in his spine is checked weekly. If it fails, Site-322 goes into '
              'ontokinetic lockdown. He is employed as maintenance staff and seasonal entertainment, and his weekly '
              'therapy sessions are a priority. Use his preferred pronouns.'),
        ('p', SRC)])
    typed('doc23_coix', [('Clearance Level', '3'), ('Item #', 'SCP-6483'), ('Object Class', 'Psychology')], [
        ('h', 'Project lead\'s note'),
        ('p', 'The Integration Program worked: Nick had begun to see his gift as bringing the character of Santa to '
              'life, not as being him. He spent the year looking forward to December.'),
        ('p', 'Then the anomalies began to fade, and his first. He has a job, a house and some company, but he is not '
              'suited to a mundane life. Please be kind to him. Please do not tell him he is not Santa.'),
        ('p', '{If the anchor monitor reads OFFLINE, you will smell pine and cinnamon first.}'),
        ('p', SRC)])


if __name__ == '__main__':
    docs()
    print('2 notes written')
