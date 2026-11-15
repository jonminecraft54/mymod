"""The notes of the forty-third batch (all original writing)."""
from make_docs2 import typed

TITLES = {'docb43_hoist': 'Hoist Control Log', 'docb43_checkpoint': 'Checkpoint Logbook',
          'docb43_contraband': 'Confiscated Items List', 'docb43_memo': 'Office Memo'}
DOCS = list(TITLES)


def docs():
    typed('docb43_hoist', [('Area', 'Light Containment'), ('Document', 'Hoist control log')], [
        ('h', 'Lifts 1-3'),
        ('p', 'Lift 1: in service. Lifts 2 and 3: out of service since the breach drill - DOOR circuit fused.'),
        ('p', 'Do not throw the HOIST switch with anyone in shaft 2. Something in shaft 2 has been calling the '
              'car since Tuesday. There is no car in shaft 2.')])
    typed('docb43_checkpoint', [('Area', 'Heavy Containment'), ('Document', 'Checkpoint logbook')], [
        ('h', 'Shift log'),
        ('p', '06:00 - quiet. 07:12 - two researchers through, cards checked. 07:40 - one researcher through. '
              'Same one as 07:12. Didn\'t come back the other way.'),
        ('p', '08:03 - the lights went red. Lockdown. I am staying in the booth. Nobody is to be let through '
              'without a Level 3 card. Nobody.')])
    typed('docb43_contraband', [('Area', 'Heavy Containment'), ('Document', 'Confiscated items')], [
        ('h', 'Screening hall - this week'),
        ('p', 'One lighter. Two personal phones. A pocket watch running backwards (sent to Temporary Containment). '
              'A tooth, not human. A sandwich (D-class, apologised).'),
        ('p', 'The scanner arch beeps at people who are carrying nothing. Engineering says the arch is fine.')])
    typed('docb43_memo', [('Area', 'Entrance Zone'), ('Document', 'Memo')], [
        ('h', 'Re: the telephone on the open floor'),
        ('p', 'Yes, it rings when it is unplugged. No, do not answer it. Dr. ____ answered it on Monday and has '
              'been very quiet since.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
