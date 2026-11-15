"""The documents of the fourteenth batch (GFX\\items\\<name>.jpg), drawn by make_docs2.typed().
Wording is written for this game, from the general shape of the two SCPs (see the wiki articles SCP-4035 and
SCP-3886). Names of living people are redacted, as in the originals."""
from make_docs2 import typed

TITLES = {
    'doc4035': 'Experiment Log SCP-4035', 'doc3886': 'Containment Record SCP-3886',
    'doc3886b': 'Journal Page (1932)', 'photo3886': 'Photograph, Circus Train',
}


def docs():
    typed('doc4035', [('Clearance Level', '3'), ('Item #', 'SCP-4035'), ('Object Class', '[DATA EXPUNGED]')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Store SCP-4035 unplugged, with the shade off. Staff who have answered SCP-4035-1 are kept under observation '
              'for fourteen days and do not sign for stock.'),
        ('h', 'Description:'),
        ('p', 'A table lamp with a stained-glass shade and an iron base, with no wiring except the socket. A bulb lights it, '
              'blue. A gaseous man in a brown coat steps out of the shade, smoking a cigar that gives no smoke, and asks '
              'whether you would like to buy something. {Any answer at all counts as a yes.} What you get is always a '
              'disappointment, and often a harmful one.'),
        ('h', 'Testing log 4035-1:'),
        ('p', 'Subject D-4088 was told to ask for telepathy. He said something else. He could afterwards name what any '
              'animal had eaten from its droppings. {Not what he asked for.}'),
        ('h', 'Addendum:'),
        ('p', 'When the subject tries to speak to SCP-4035-1 again, the lamp says: "Sorry kid, no refunds."')])
    typed('doc3886', [('Clearance Level', '3'), ('Item #', 'SCP-3886'), ('Object Class', 'Neutralized Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Keep SCP-3886 in a locked storage box in the Safe Object Wing at Site-102. The living relative of the original '
              'owner is held in the Low-Threat Humanoid Wing, may read and take recreation, and may not go more than 1.6 km '
              'from the saddle. Testing needs a Level 3 present.'),
        ('h', 'Description:'),
        ('p', 'A black leather dressage saddle, silver clasps, no damage that anybody has been able to find. Put it on a '
              'recently dead animal of useful size, and the animal stands up, walks to its owner\'s relative and does what '
              'it is told. {Living horses panic when it is in the room.}')])
    typed('doc3886b', [('Clearance Level', '4'), ('Item #', '3886-01'), ('Object Class', 'Recovered Document')], [
        ('h', 'Translated from the French.'),
        ('p', 'July 14, 1932. Another day, another performance. We stopped at Cincinnati, which I think is a fine city. '
              'Mr. Sherwood spoke to me in private. The horse acts are no longer good enough for the show, and I am to be '
              'let go at Louisville. The saddle goes with the wagon, and the wagon is staying with me. {I will not be the '
              'only one who keeps something of this circus.}')])
    # the photograph is the image itself (see make_assets14.photo); this writes nothing more
    print('%d documents written (photo3886 is the image copy)' % (len(TITLES) - 1))


if __name__ == '__main__':
    docs()
    assert set(TITLES) == {'doc4035', 'doc3886', 'doc3886b', 'photo3886'}
