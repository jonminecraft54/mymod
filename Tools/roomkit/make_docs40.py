"""The notes of the fortieth batch: SCP-1197, -1220, -1192, -1355 and -1196 summarised in our own words from
scp-wiki.wikidot.com (CC BY-SA 3.0), and a note on the Residential Sector itself."""
from make_docs2 import typed

TITLES = {'docb40_1197': 'SCP-1197 Summary', 'docb40_1220': 'SCP-1220 Summary', 'docb40_1192': 'SCP-1192 Summary',
          'docb40_1355': 'SCP-1355 Summary', 'docb40_1196': 'SCP-1196 Summary', 'docb40_house': 'Residential Sector Notice'}
DOCS = list(TITLES)
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('docb40_1197', [('Clearance Level', '3'), ('Item #', 'SCP-1197'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'An ordinary hotel suite - bed, bathroom, television, mini-fridge, telephone. Its walls cannot be '
              'damaged. A door in the west wall (SCP-1197-1) seems to lead to the next suite.'),
        ('p', 'SCP-1197-1 only opens while the entrance door is shut. Behind it is an identical suite - with an '
              'identical you in it, who opened their door at the same moment. While a session lasts, the entrance '
              'will not open. Every recorded session has ended the same way: one of each occupant dies.'),
        ('p', 'The suite reproduced here is kept sealed. Keep the entrance door OPEN.'),
        ('p', SRC('scp-1197'))])
    typed('docb40_1220', [('Clearance Level', '2'), ('Item #', 'SCP-1220'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'An unknown, possibly extinct tonal language with sounds a human throat should not manage. The only '
              'record is three cassettes: an elderly woman, one of its last speakers, telling a flood story in it '
              'and then in English. A man in an empty world shapes clay, and it becomes wheat, an ox, another '
              'person, and [data expunged].'),
        ('p', 'The recordings are harmless. A living person SPEAKING it is not: a zone of anomalous space opens '
              'around the speaker, usually about two metres across, its nature set by what was said.'),
        ('p', 'Do not repeat anything you hear on the tape.'),
        ('p', SRC('scp-1220'))])
    typed('docb40_1192', [('Clearance Level', '2'), ('Item #', 'SCP-1192'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A young gang-gang cockatoo, scruffy and unwilling to preen, with the mind of a six- to eight-year-'
              'old child and a healed bump on the back of its head. It cannot talk, but it writes, badly: "who ar u", '
              '"timmi", "i wana go hom".'),
        ('p', 'It follows anyone who looks like an authority figure, such as a police officer. The address it wrote '
              'is a real house. The family there has a son named Timmy.'),
        ('p', SRC('scp-1192'))])
    typed('docb40_1355', [('Clearance Level', '3'), ('Item #', 'SCP-1355'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A small closed school used to store boxes of textbooks. Some of the boxes are not boxes: SCP-1355-1, '
              'living things identical to them, warm as a person on thermal cameras - except when they move.'),
        ('p', 'Visitors hear beautiful singing, a song they know, and feel calm. They are later found asleep in '
              'the front office with no memory of how they got there - and with no larynx. They do not notice. They '
              'believe they can still speak.'),
        ('p', 'The basement here holds boxes recovered from the site. Count them when you go in.'),
        ('p', SRC('scp-1355'))])
    typed('docb40_1196', [('Clearance Level', '2'), ('Item #', 'SCP-1196'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'The basement of a former back clinic: concrete, pillars, an unfinished floor, three working '
              'fluorescent tubes. Put a chair in it and the chair comes alive (SCP-1196-1) - shuffling about, or, if '
              'it is a folding chair, snapping its legs open and shut to move.'),
        ('p', 'They talk, in squeaky little voices, about posture: "Stand up straight!" "Don\'t slouch!" Stay long '
              'enough and they fixate on one person, follow them, and their voices grow deeper and louder. Leave '
              'and it stops.'),
        ('p', 'The chairs in this garage were brought from the site. The garage now has the same property.'),
        ('p', SRC('scp-1196'))])
    typed('docb40_house', [('Area', 'Light Containment'), ('Document', 'Residential Sector notice')], [
        ('h', 'Residential Sector'),
        ('p', 'These rooms are reconstructions: whole rooms and the objects in them recovered from homes, rebuilt '
              'here for study. Do not use the furniture. Do not eat anything in the kitchen. Do not answer the '
              'telephone. The television is not plugged in.'),
        ('p', 'Twelve rooms, three wings. If you count thirteen, report it.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
