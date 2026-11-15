"""SCP-2107's note: a summary in our own words of scp-wiki.wikidot.com/scp-2107 (CC BY-SA 3.0)."""
from make_docs2 import typed

TITLES = {'doc2107': 'SCP-2107 Summary'}


def docs():
    typed('doc2107', [('Clearance Level', '2'), ('Item #', 'SCP-2107'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'SCP-2107 is a soft drink sold as "Diet Ghost", always in a light blue can: the DIET GHOST logo, "SCARE '
              'YOUR THIRST!" beneath it, and usually a sticker reading "MADE WITH NATURAL GHOSTS!". The cans and the '
              'drink are ordinary.'),
        ('p', 'A few minutes after drinking it, the subject is haunted - footsteps, voices, slamming doors, cold, things '
              'moving - until the drink has broken down in the body, one to three hours later. The more is drunk, the '
              'worse it gets, up to physical harm.'),
        ('h', 'Containment'),
        ('p', 'Cans are kept in a CNSI locker; some in a refrigerated unit before trials. New cans keep turning up in '
              'shops and, once, fifteen from a cafeteria vending machine.'),
        ('p', '{Do not drink the samples. Do not drink two.}'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-2107 (CC BY-SA 3.0).')])


if __name__ == '__main__':
    docs()
    print('1 note written')
