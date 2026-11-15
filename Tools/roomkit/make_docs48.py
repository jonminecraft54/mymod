"""The notes of the forty-eighth batch: SCP-806 (summarised in our own words from scp-wiki.wikidot.com/scp-806,
CC BY-SA 3.0; people by role only)."""
from make_docs2 import typed

TITLES = {'doc806': 'SCP-806 Document', 'docb48_tests': 'SCP-806 Test Log (Excerpt)',
          'docb48_locker': 'Containment Locker 8: Reel Index'}
DOCS = list(TITLES)


def docs():
    typed('doc806', [('Item #', 'SCP-806'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures'),
        ('p', 'SCP-806 is kept sealed in Containment Locker 8. Creating an SCP-806-1 instance needs written approval '
              'from both senior researchers of the project. SCP-806-1-a is housed in a standard humanoid suite.'),
        ('h', 'Description'),
        ('p', 'A large film projector, built around 1900 and heavily rebuilt: a lens of several dozen thin layers of '
              'shaved gemstone and unknown materials, an LED array in place of the bulb, alloy gearing that takes '
              'almost any film size, and extra spools so many reels can run without a break.'),
        ('p', 'Run with 13 to 27 hours of footage of a dead person onto a silver lenticular screen, it builds a copy '
              'of that person in the open space before the screen, as they were in the last recording used. The '
              'matter arrives as needle-thin rays of light from the lens. Someone must watch the film the whole time, '
              'or the forming stops and slowly undoes itself. Shut the projector down and the copy fails, usually '
              'collapsing into blood and graphite dust.'),
        ('p', 'Only real people return: an actor, never the character. Cartoons do nothing. Living people do '
              'nothing. With several people on film, the one with the most screen time forms.'),
        ('p', 'Instances (SCP-806-1) have no colour at all and believe they are the original person. All but one die '
              'of cardiac arrest 70 to 75 hours after forming.'),
        ('h', 'SCP-806-1-a'),
        ('p', 'The first instance and the only survivor: a young woman who remembers nothing of who she was, not even '
              'her name. She was recovered with the projector and about fifty hours of film - most of it 5.8 seconds '
              'of her laughing, looped over and over.')])
    typed('docb48_tests', [('Item #', 'SCP-806'), ('Document', 'Test log, excerpt')], [
        ('h', 'Selected tests'),
        ('p', 'Archive footage of a deceased staff member, single subject: instance formed. Correct memories up to the '
              'date of the footage. Cardiac arrest at hour 72.'),
        ('p', 'Security footage, two officers on screen: the officer with more screen time formed. The other did not.'),
        ('p', 'Animated short: nothing formed. Interview footage of a living researcher: nothing formed.'),
        ('p', 'Two runs deliberately stopped at hour 19: both unfinished bodies fell to the floor. The more complete '
              'one suffered brain death, the less complete one simply died.'),
        ('p', 'Note: the screening room projector has been geared to run a full set of reels in minutes, not hours. '
              'Do not leave the room while it runs.')])
    typed('docb48_locker', [('Area', 'Containment Locker 8'), ('Document', 'Reel index')], [
        ('h', 'Reels on the shelves'),
        ('p', 'D - orientation and work-detail footage, one Class-D subject, deceased.'),
        ('p', 'SEC - corridor security footage, two officers, both deceased.'),
        ('p', 'TOON - animated training short.'),
        ('p', 'LIVE - staff interview footage. The interviewee is alive and well and would like it back.'),
        ('p', '5.8s - a short loop recovered with the projector. Not enough footage for anything. Do not run it.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
