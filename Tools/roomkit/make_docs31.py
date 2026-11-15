"""The notes of the thirty-first batch: short summaries of scp-wiki.wikidot.com/scp-467, /scp-178, /scp-198, /scp-207,
/scp-1079 and /scp-1650 (CC BY-SA 3.0), in our own words, with the SCP-467 test log abridged."""
from make_docs2 import typed

TITLES = {'doc467': 'SCP-467 Summary', 'doc467log': 'Test Log 467-Various (Abridged)', 'doc178': 'SCP-178 Summary',
          'doc198': 'SCP-198 Summary', 'doc207': 'SCP-207 Summary', 'doc1079': 'SCP-1079 Summary',
          'doc1650': 'SCP-1650 Summary', 'scp178': 'SCP-178', 'scp198': 'SCP-198', 'scp207': 'SCP-207-B',
          'scp1079': 'SCP-1079', 'scp1650': 'SCP-1650'}
DOCS = [k for k in TITLES if k.startswith('doc')]


def docs():
    typed('doc467', [('Clearance Level', '2'), ('Item #', 'SCP-467'), ('Object Class', 'Safe')], [
        ('h', 'Containment'),
        ('p', 'One security guard, changed daily. No phones, pagers or other communication devices near SCP-467 '
              'without clearance for testing.'),
        ('h', 'Description'),
        ('p', 'An empty phone booth, once the home of a "haunted phone". The phone was never the anomaly; the booth '
              'is. When a person and a communication device are inside it together, the device receives a call from '
              'someone the person knows - friend, family, co-worker, acquaintance.'),
        ('p', 'Afterwards the call never happened: no log, no record, and the "caller" never picked up a phone. The '
              'calls reveal things the person did not know - most often secrets and confessions - from the trivial '
              'to the life-changing. The booth works for a person once a day. Personal use is discouraged.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-467 (CC BY-SA 3.0).')])
    typed('doc467log', [('Document', 'Test Log 467-Various'), ('Status', 'Abridged'), ('Item #', 'SCP-467')], [
        ('p', 'D-class: his mother, disappointed, blaming herself. Asked again and again to call home. Denied.'),
        ('p', 'D-class: the victim\'s family - never forgotten, slowly learning to forgive. Uneasy for hours.'),
        ('p', 'D-class: the researcher in the next room, on his ridiculous haircut. Annoyed, then amused.'),
        ('p', 'Dr. Rights: unknown. Two days of doubt about the Foundation; full recovery.'),
        ('p', 'Dr. Iceberg: unknown. Two days later, a fight with a researcher at Site 17.'),
        ('p', 'SCP-1599: its creators, saying they had lost its signal. It called the message a trick.'),
        ('h', 'Holidays'),
        ('p', 'Around Thanksgiving and Christmas the calls turn distressing. Subjects have been called by '
              'themselves, by the dead, and by people who never existed.'),
        ('p', 'D-class (amnesiac test subject): his own voice, explaining what he had been made to forget.'),
        ('p', 'D-class: a victim, screaming for five minutes. Attempted to destroy SCP-467. Terminated.'),
        ('p', 'Abridged from scp-wiki.wikidot.com/scp-467 (CC BY-SA 3.0).')])
    typed('doc178', [('Clearance Level', '3'), ('Item #', 'SCP-178'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'White cardboard 3-D glasses, blue and red lenses. Whoever wears them sees large bipedal entities all '
              'around - docile, curious, leaning over shoulders to watch people work.'),
        ('p', 'Any attempt to interact with them - by the wearer or anyone - and lacerations open on the people '
              'involved, three long parallel slashes at a time, and keep opening until the wearer is dead. Nothing '
              'is seen or heard by anyone else.'),
        ('h', 'Containment'),
        ('p', 'Class 3 container, two armed Level 3 guards. Tests are watched remotely; only the subject in the room. '
              'Level 4 staff must read Incident Report 178-14-Alpha.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-178 (CC BY-SA 3.0).')])
    typed('doc198', [('Clearance Level', '3'), ('Item #', 'SCP-198'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A drinking vessel that changes its form - now a white porcelain mug with blue stripes. Held by a living '
              'person for a few seconds, it bonds to their hand, painfully and permanently: nothing breaks the bond '
              'but death, and wounds below the wrist heal at once.'),
        ('p', 'Then it fills, by itself, with something from a human body. The holder starts to waste away, and the '
              'only thing that slows it is drinking what is in the cup. It refills as fast as it is emptied.'),
        ('h', 'Containment'),
        ('p', 'Sealed case on a digital scale with an alarm. Never handled by staff. Any weight change: Containment '
              'Protocol 198.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-198 (CC BY-SA 3.0).')])
    typed('doc207', [('Clearance Level', '2'), ('Item #', 'SCP-207'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A crate of 24 bottles of cola, SCP-207-A to -X. Drinking more than 5 ml of the cola removes all need '
              'for rest or sleep, and sharpens body and mind: about 50% faster every six hours.'),
        ('p', 'The body is not changed to cope. No subject has lived 48 hours: organs fail, arteries burst. After a '
              'day, subjects move very carefully - they cannot judge their own speed any more.'),
        ('h', 'Containment'),
        ('p', 'Waterproof locked container in bio-containment. Site vending machines dispense clear drinks only.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-207 (CC BY-SA 3.0).')])
    typed('doc1079', [('Clearance Level', '2'), ('Item #', 'SCP-1079'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', '"Dr. Wondertainment\'s Bubblebath Bonbons!" Label: not for under-3s; only one sweet per sitting.'),
        ('p', 'One sweet: a tingle, then the eater\'s blood foams out of the skin of the belly, arms and back as pink, '
              'bubblegum-scented froth - 30 to 50 ml, harmless. Each further sweet multiplies it: the blood boils '
              'with bubbles. Four or more in one sitting kill 95% of eaters.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-1079 (CC BY-SA 3.0).')])
    typed('doc1650', [('Clearance Level', '3'), ('Item #', 'SCP-1650'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A clay oil pot from Hasmonean-period Judea with a worn inscription. Upright it is empty. Held at an '
              'angle for thirty seconds it pours oil:'),
        ('p', '45 degrees: fine olive oil. 50: looks the same, but is oleander poison - 87% die, 12% are left '
              'brain-damaged. 65: a clear oil that burns for days with no heat and no air. 90: a red oil that '
              'preserves metal, eats living flesh, and erases blood - deadly if swallowed.'),
        ('p', 'Seized by MTF Alpha-12 from a sale between MC&D and the "Horizon Initiative".'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-1650 (CC BY-SA 3.0).')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
