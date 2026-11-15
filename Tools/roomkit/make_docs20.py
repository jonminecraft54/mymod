"""The notes of the twentieth batch, drawn by make_docs2.typed(). Short summaries in our own words of SCP Wiki
articles (scp-wiki.wikidot.com, CC BY-SA 3.0); each note names its source."""
from make_docs2 import typed

TITLES = {
    'doc20_3008': 'SCP-3008 Summary', 'doc20_999': 'SCP-999 Summary', 'doc20_131': 'SCP-131 Summary',
    'doc20_529': 'SCP-529 Summary', 'doc20_111': 'SCP-111 Summary', 'doc20_458': 'SCP-458 Summary',
    'doc20_261': 'SCP-261 Summary', 'doc20_241': 'SCP-241 Summary', 'doc20_113': 'SCP-113 Summary',
}
SRC = 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).'


def note(key, num, cls, desc, cont, remark):
    typed(key, [('Clearance Level', '2'), ('Item #', 'SCP-' + num), ('Object Class', cls)], [
        ('h', 'Description'), ('p', desc), ('h', 'Containment'), ('p', cont), ('p', '{' + remark + '}'),
        ('p', SRC % ('scp-' + num))])


def docs():
    note('doc20_3008', '3008', 'Euclid', 'A large furniture store whose inside is far bigger than its outside, perhaps '
         'without end. People who wander in lose the exit. Its tall, faceless staff are harmless by day; when the lights '
         'go down they become hostile to anyone still inside.', 'The entrance is sealed. Survivor camps inside are not '
         'to be contacted.', 'If you hear the store closing, find a bed and stay off the aisles.')
    note('doc20_999', '999', 'Safe', 'A friendly orange jelly that loves to play. Touching it brings on a strong sense '
         'of happiness.', 'A pen with toys. It may roam the site if escorted.', 'It got out through the vent again. '
         'Nobody minds.')
    note('doc20_131', '131', 'Safe', 'Two small teardrop creatures with one eye each, who follow people they like '
         'and stare at threats. They cannot stand being looked away from.', 'Free to roam.', 'They are watching the '
         'cell door for you.')
    note('doc20_529', '529', 'Safe', 'Josie, a tabby cat of whom only the front half can be seen. She behaves like a '
         'normal cat.', 'A cat bed and a litter tray. Petting is allowed.', 'Please stop asking where the rest of her is.')
    note('doc20_111', '111', 'Safe', 'Small snails with tiny dragon wings that breathe fire when frightened '
         'or hungry.', 'A fireproof terrarium. Feed lettuce, not fingers.', 'One of them sneezed on the clipboard.')
    note('doc20_458', '458', 'Safe', 'A pizza box that always holds a fresh pizza, of the holder\'s favourite kind.',
         'In the break room cabinet.', 'Do not share the box - it only fills for whoever holds it.')
    note('doc20_261', '261', 'Safe', 'A vending machine that takes yen and gives out odd snacks, some harmless, some '
         'not quite food.', 'Experiments logged. No more than one item per day.', 'Do not eat anything that moves.')
    note('doc20_241', '241', 'Euclid', 'A cookbook, Good Home Cooking, whose margins fill with handwritten notes '
         'urging the reader to cook the people around them. People who follow its recipes do not stop.', 'Kept closed in a '
         'locked drawer. Recipes are not to be followed.', 'Someone wrote back in the margin: NO.')
    note('doc20_113', '113', 'Safe', 'A red jasper stone. Holding it painfully swaps the holder\'s sex within seconds; '
         'the change is lasting.', 'On a pedestal. No bare-skin contact.', 'Use the tongs.')


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
