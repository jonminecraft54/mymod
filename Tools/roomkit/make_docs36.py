"""The notes of the thirty-sixth batch: summaries in our own words of scp-wiki.wikidot.com/scp-1200, -1916, -1921,
-3147, -3409 and an expedition log for SCP-1479 (CC BY-SA 3.0); titles for the four items."""
from make_docs2 import typed

TITLES = {'docb36_1200': 'SCP-1200 Summary', 'docb36_1916': 'SCP-1916 Summary', 'docb36_1921': 'SCP-1921 Summary',
          'docb36_3147': 'SCP-3147 Summary', 'docb36_3409': 'SCP-3409 Summary', 'docb36_1479': 'SCP-1479 Expedition Log'}
DOCS = list(TITLES)
TITLES.update({'gum1200': 'SCP-1200 (Tastes Like Chewing Gum)', 'jar1916': 'SCP-1916 (Jawbreakers)',
               'pop3147': 'SCP-3147 (Tongue Twister)', 'cotton1921': 'SCP-1921-A2 (Black Cotton Candy)'})
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('docb36_1200', [('Clearance Level', '2'), ('Item #', 'SCP-1200'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', '"Tastes Like Chewing Gum", made by "The Factory". Packs turn up in shops across the US. Chew a stick and '
              'something happens, depending on the flavour - 83 flavours so far. Swallowing it does nothing more.'),
        ('p', 'Tastes Like Lemons: everything tastes of lemon for 28 hours. Tastes Like Sunshine: you shine, 40,000 lux, '
              'for twenty minutes, harmlessly. Another lets you rearrange parts of your own body for a few hours.'),
        ('p', 'The flavour is printed on the wrapper. Read it first.'),
        ('p', SRC('scp-1200'))])
    typed('docb36_1916', [('Clearance Level', '2'), ('Item #', 'SCP-1916'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'Six jawbreakers: red; beige with white streaks; white with moon-grey patches; orange and white bands '
              'with a big red spot; black; black with a white question mark.'),
        ('p', 'Ten to twenty minutes after eating one, your weight changes by a fixed proportion - your size and mass '
              'do not. You move as if the gravity around you had changed: Mars, Venus, the Moon, Jupiter...'),
        ('p', 'Nobody has volunteered for the black one twice.'),
        ('p', SRC('scp-1916'))])
    typed('docb36_1921', [('Clearance Level', '3'), ('Item #', 'SCP-1921'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A carved and painted cotton-candy kiosk, scorched, under an arch: "Cotton Candy - Free With Admission". '
              'Its spinner has a pump to a reservoir. With the right thing in the reservoir, the floss comes out black.'),
        ('p', 'The black floss shrinks on your tongue until you cannot feel it - then swells in the gut and works its '
              'way to the brain. Most people never notice. It is kept in a sealed cell. A sample hatch is fitted for '
              'tests by D-class only.'),
        ('p', SRC('scp-1921'))])
    typed('docb36_3147', [('Clearance Level', '2'), ('Item #', 'SCP-3147'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'Dr. Wondertainment\'s Tantalizing Tongue Twisters: lollipops. Nothing about the sugar is anomalous.'),
        ('p', 'When two or more people taste the same one within ten minutes, each gets control of another\'s mouth: '
              'you try to speak and your words come out of someone else, in your voice. From two to twenty-four '
              'minutes, depending how much you ate. Alone, it is a lollipop.'),
        ('p', SRC('scp-3147'))])
    typed('docb36_3409', [('Clearance Level', '4'), ('Item #', 'SCP-3409'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'An abandoned confectionery plant held by a cult in hazmat suits until the Foundation went in. Inside, a '
              'fungus of non-terrestrial origin, SCP-3409-A, made mostly of something like chocolate, spreading '
              '0.6 m an hour from a spacetime anomaly (SCP-3409-B) in the central chamber.'),
        ('p', 'It infects by touch, stinging fungal matter into the blood. Within two days the infected want only to '
              'go to SCP-3409-B. The sample in the sealed cell here is not to be approached without a suit.'),
        ('p', SRC('scp-3409'))])
    typed('docb36_1479', [('Clearance Level', '3'), ('Item #', 'SCP-1479'), ('Document', 'Expedition log (abridged)')], [
        ('p', 'An empty utility room in the basement of a closed coal plant that holds about 144 square kilometres of '
              'taiga. Electronic devices show the walls. Eyes do not.'),
        ('p', 'Day 1: Clear night, always night. Rope line from the door. Found a cabin within 300 m - smoke from the '
              'chimney, a lantern lit. Nobody answered.'),
        ('p', 'Day 2: Something watched from the trees, a pair of eyes at a time. They are gone when you get close.'),
        ('p', 'Day 3: The rope line was cut. We found the door by the lantern light. We are not going back for the '
              'cabin. Whoever lit that lantern can keep it.'),
        ('p', 'From the summary of scp-wiki.wikidot.com/scp-1479 (CC BY-SA 3.0); the log is our own.')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
