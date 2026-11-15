"""The notes of the twenty-ninth batch: short summaries of scp-wiki.wikidot.com/scp-820-jp, /scp-867, /scp-120,
/secure-facility-dossier-lunar-area-32, /scp-2219 and /scp-l001 (all CC BY-SA 3.0), in our own words, plus the
procedure sheets and memos written for the mod."""
from make_docs2 import typed

TITLES = {'doc820jp': 'SCP-820-JP Summary', 'doc867': 'SCP-867 Summary', 'doc120': 'SCP-120 Summary',
          'doc120_22': 'Document #120-22: Dialling Procedure', 'docla32': 'Lunar Area-32: Arrival Advisory',
          'doc2219': 'SCP-2219 Summary', 'docl001': 'Memo: Lost SCP-001 Files', 'herbicide867': 'Herbicide Injector',
          'scp820jp': 'SCP-820-JP'}
DOCS = [k for k in TITLES if k.startswith('doc')]


def docs():
    typed('doc820jp', [('Clearance Level', '3'), ('Item #', 'SCP-820-JP'), ('Object Class', 'Euclid')], [
        ('h', 'Containment'),
        ('p', 'Kept in a containment unit inside an unmanned submarine that never stops moving. Brought up for '
              'inspection at intervals. On land it must be moved every two hours; if it stays in one place for more '
              'than three hours its transmitter signals and a Mobile Task Force retrieves it.'),
        ('h', 'Description'),
        ('p', 'An indestructible stone knife in an Aztec style, a snake coiling from the handle up the blade. Whoever '
              'looks at it for long enough wants to hurt someone with it, as publicly as possible.'),
        ('p', 'Information about the knife or what it has done is mildly contagious: people find it fascinating, lose '
              'a little of their judgement and drift towards it. Around every incident a carefree "tourist" trade '
              'grows - stalls, snacks, mascots - and keeps growing unless it is stopped.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-820-jp (CC BY-SA 3.0).')])
    typed('doc867', [('Clearance Level', '3'), ('Item #', 'SCP-867'), ('Object Class', 'Euclid')], [
        ('h', 'Containment'),
        ('p', 'Specimens are kept in Section E. Maintenance only by remote rovers and automatic irrigation. Anyone '
              'entering wears full NBC protection with a Kevlar underlayer. Everyone leaving gets a full herbicidal '
              'treatment; anyone with puncture marks is quarantined for at least fifteen days.'),
        ('h', 'Description'),
        ('p', 'A conifer like a blue spruce, but blood red, with no cones. Each needle is a hollow injector holding a '
              'single seed: brush against it and the seed is shot painlessly into the skin.'),
        ('p', 'The seed sleeps for up to two weeks, then grows tendrils through the blood vessels: a day of agony, '
              'then death, and a new tree grows out of the body.'),
        ('p', '{Section E note: the herbicide injectors in the decon room kill a dormant seed. Use one if in doubt.}'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-867 (CC BY-SA 3.0).')])
    typed('doc120', [('Clearance Level', '3'), ('Item #', 'SCP-120'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A child\'s paddling pool, pastel pink, 2.5 m across, indestructible. The glowing liquid in it is only '
              'partly here. A conscious human carrying under 37.8 kg who steps in alone falls through and arrives at '
              'one of eleven destinations, which follow each other in a fixed cycle.'),
        ('p', '1 Pacific (blue): the SCPS Demeter\'s cargo hold. 2 Greenland (white). 4 Himalayas (white). '
              '6 Sahara (yellow). 7 Gobi (brown). 9 Mare Imbrium, the Moon (grey): Lunar Area-32.'),
        ('p', '3, 5, 8, 10, 11 are Lagrange points (black). Anyone sent there is lost.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-120 (CC BY-SA 3.0).')])
    typed('doc120_22', [('Clearance Level', '2'), ('Document', '#120-22'), ('Subject', 'Dialling')], [
        ('h', 'Moving SCP-120 to the next destination'),
        ('p', '1. Read the colour of the liquid against the chart. Black means a Lagrange point. DO NOT ENTER.'),
        ('p', '2. Each use moves SCP-120 to the next configuration. Operators "dial" it from the control room.'),
        ('p', '3. Weight limit 37.8 kg including clothing. Overloaded subjects stand on a smooth floor and go nowhere.'),
        ('p', '4. One subject at a time. Wait for grey (9) for Lunar Area-32. Return by the supply lander.'),
        ('p', '{Every dial costs us someone. Do not dial for fun. - Facility Head}')])
    typed('docla32', [('Clearance Level', '2'), ('Facility', 'Lunar Area-32'), ('Code', 'LMaImb-Area-32')], [
        ('h', 'Welcome to Lunar Area-32'),
        ('p', 'You are in the SCP-120 Reception, an airtight room built round its ninth destination point on Mare '
              'Imbrium. The cargo bay is east; the observatory north. Sub-Level 1 (containment, storage) by the lift.'),
        ('p', 'Gravity is one sixth of Earth\'s. Walk slowly. Head injuries are common among new personnel; bring '
              'your own protective headgear - administration will not provide it.'),
        ('p', 'Bring medication for nine months. If you run out, nothing can be done until the next supply run.'),
        ('p', 'Returning to Earth: the supply lander, cargo bay, east airlock.'),
        ('p', 'After the facility dossier at scp-wiki.wikidot.com (CC BY-SA 3.0).')])
    typed('doc2219', [('Clearance Level', '2'), ('Item #', 'SCP-2219'), ('Object Class', 'Safe')], [
        ('h', 'Containment'),
        ('p', 'Standard containment locker. Testing only through the remote analog proxy and a camera on the console. '
              'Direct human testing is prohibited.'),
        ('h', 'Description'),
        ('p', 'An unlicensed handheld game, "PORRIDGE", a platformer after Goldilocks and the Three Bears. What happens '
              'in the game happens to the player: collect porridge and you feel calm; fail a level and you have a '
              'seizure; lose a life and your throat swells shut; lose them all and you contract leprosy.'),
        ('p', 'Nobody knows what beating the final boss does.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-2219 (CC BY-SA 3.0).')])
    typed('docl001', [('Clearance Level', '6'), ('From', 'O5 Command'), ('To', 'Investigation Dept.')], [
        ('h', 'SCP-L001: lost files'),
        ('p', 'Several objects listed under the SCP-001 designation, and their files, have been lost. O5 Command '
              'will neither confirm nor deny which. They are to be found as soon as possible.'),
        ('p', 'The index terminal on Sub-Level 1 returns template fields where the files should be. Do not alter it.'),
        ('p', '{The vault next door is still sealed. Nobody here knows what it held.}'),
        ('p', 'After scp-wiki.wikidot.com/scp-l001 (CC BY-SA 3.0).')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
