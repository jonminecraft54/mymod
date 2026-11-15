"""The notes of the thirtieth batch, Site-42: short summaries of scp-wiki.wikidot.com/scp-2648, /scp-2758,
/scp-3069, /scp-4427, /scp-4433, /scp-4434 and the Site-42 hub page (CC BY-SA 3.0) in our own words, plus a
Site Director's memo and the Figure A note written for the mod. Only the in-universe Site Director appears."""
from make_docs2 import typed

TITLES = {'docsite42': 'Site-42 Overview', 'docpr42': 'Memo: Site Director, Public Relations',
          'doc2648': 'SCP-2648 Summary', 'doc2758': 'SCP-2758 Summary', 'doc3069': 'SCP-3069 Summary',
          'doc4427': 'SCP-4427 Summary', 'doc4433': 'SCP-4433 Summary', 'doc4434': 'SCP-4434 Summary',
          'doc4434ad': 'Figure A (Recreation)', 'thermal4427': 'Thermal Camera', 'phone4433': 'Flip Phone',
          'card2758': 'Room G14 ID Card', 'jar3069': 'SCP-3069 Specimen Jar'}
DOCS = [k for k in TITLES if k.startswith('doc')]


def docs():
    typed('docsite42', [('Clearance Level', '2'), ('Facility', 'Site-42'), ('Director', 'Dr. T. Sherman')], [
        ('h', 'Site-42'),
        ('p', 'A facility for the containment of sapient SCP objects, on the North Carolina coast. Since the public '
              'reveal of the Foundation it has grown to the size of a small town: secrecy is no longer necessary, '
              'but every civilian now has questions, and the site invests heavily in public relations.'),
        ('h', 'Holdings on file'),
        ('p', 'SCP-2648 (Safe, pending Euclid) - SCP-2758 (Safe) - SCP-3069 (Keter) - SCP-4427 (Keter) - '
              'SCP-4433 (Euclid) - SCP-4434 (Euclid)'),
        ('h', 'Departments'),
        ('p', 'Media Relations & Support. The Multi-U Dept. The Ethics Subcommittee for Sentient and Sapient '
              'Anomalies. Safe-Class Wing A4. Euclid-Level Wing B4.'),
        ('p', 'After the Site-42 hub page at scp-wiki.wikidot.com (CC BY-SA 3.0).')])
    typed('docpr42', [('From', 'Site Director'), ('To', 'All Site-42 Staff'), ('Re', 'Public Relations')], [
        ('h', 'We are being watched. Good.'),
        ('p', 'The town outside our fence knows what we are now. They see our trucks, read our press releases and '
              'call Media Relations twelve hundred times a day. Every one of those calls is answered.'),
        ('p', 'Our residents are people. They have privacy, privileges and rights under the Ethics Subcommittee. '
              'Visitors stop at the yellow line. No photographs of residents. No exceptions.'),
        ('p', 'If a civilian asks you a question on duty, you send them to Media Relations & Support. You do not '
              'answer it yourself - not even the easy ones.'),
        ('p', '- Dr. T. Sherman, Site Director, Site-42')])
    typed('doc2648', [('Clearance Level', '2'), ('Item #', 'SCP-2648'), ('Object Class', 'Safe (pending Euclid)')], [
        ('h', 'Description'),
        ('p', 'A mobile, roughly spherical amalgam of mostly organic matter, about 4 m across. It grows by taking in '
              'whatever it rolls over: bushes, turf (plastic mesh and all), firewood, carcasses, pineapples, '
              'mushrooms. It hums, smells, weeps a red fluid, and attacks only when threatened.'),
        ('h', 'Containment'),
        ('p', 'Kept in a steel shipping container under 24/7 observation by five to seven Site-42 personnel on '
              '28-day rotations. It must not be allowed to take in any more matter. MTF Lambda-14 monitor soil and '
              'groundwater on the property it came from.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-2648 (CC BY-SA 3.0).')])
    typed('doc2758', [('Clearance Level', '2'), ('Item #', 'SCP-2758'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'Room G14, Safe-Class Containment Wing A4. Entering it once started a process: two voices arranging '
              'someone, then, 3 minutes 33 seconds in, a man (SCP-2758-A) appeared in the centre of the room and '
              'vanished seconds later in a Hume fluctuation.'),
        ('p', 'Leaving and re-entering at the right moment kept him there. He cannot leave G14: at the doorway he '
              'un-manifests. Nineteen attempts to free him have failed. He now lives in the room.'),
        ('h', 'Containment'),
        ('p', 'G14 is locked at all times and opens only to a custom identification card kept in Safe-class locker '
              '#2758. A table, chair and microphone rig are provided for interviews.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-2758 (CC BY-SA 3.0).')])
    typed('doc3069', [('Clearance Level', '4'), ('Item #', 'SCP-3069'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A massive constructed structure some 6000 km long beneath the North Atlantic, discovered when part of '
              'it breached the Mid-Atlantic Ridge and cut the last working transatlantic cable. It now releases '
              'specimens and substances of unknown origin.'),
        ('p', 'Access Point I: a sealed pipe 25 m wide at 3500 m; a light current on its ports opens a hatch. '
              'Access Point II: blocked by a sponge-like mass. Access Point III: a spatial distortion round '
              'SCP-3069-A, an immovable steel pole topped with a glowing green sphere.'),
        ('h', 'Containment'),
        ('p', 'MTF Gamma-6 ("Deep Feeders") with Site-3069 and Site-42 monitor it. No descent below explored '
              'depths without two O5s and both Site Directors.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-3069 (CC BY-SA 3.0).')])
    typed('doc4427', [('Clearance Level', '3'), ('Item #', 'SCP-4427'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'An incorporeal sphere, 60 cm across, 37.8 C, visible only on thermal imaging. It appears in busy '
              'places 1.5 m off the ground and stays until exactly 45 people have walked through it. Within an hour, '
              'one of the 45 develops a severe anomalous trait (SCP-4427-A).'),
        ('p', 'SCP-4427-B, the first person affected, is kept in Room 35, Wing B4, behind Scranton netting at over '
              '100 Hm. It loses its memory and is not to be told what happened to it.'),
        ('h', 'Containment'),
        ('p', 'Cone it off before 45 people pass. Civilian questions go to Site-42 Media Relations & Support.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-4427 (CC BY-SA 3.0).')])
    typed('doc4433', [('Clearance Level', '3'), ('Item #', 'SCP-4433'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'Five sentient entities that phone one person at a time from a restricted number, posing as family - '
              '"mother" and "country", over and over - until the person comes to SCP-4433-A, a fire-gutted house. '
              'Inside, the subject sees a warm, working home and stays until they die of thirst or hunger.'),
        ('p', 'To others they are figures seen only in infrared, or at the edge of vision. While they are in the '
              'house, radio, radar and microwave equipment for kilometres around fails.'),
        ('h', 'Containment'),
        ('p', 'Outpost 4433-A watches the house round the clock. Affected callers are detained until the calls stop.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-4433 (CC BY-SA 3.0).')])
    typed('doc4434', [('Clearance Level', '3'), ('Item #', 'SCP-4434'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A valley that hunts. SCP-4434-A: advertisements that compel readers to its address and photograph as '
              'blank white. SCP-4434-B: a shape-taking entity that coaxes visitors downhill. SCP-4434-C: 25 '
              'deer-like pack hunters that kill and eat them. SCP-4434-D: the hole at the bottom.'),
        ('h', 'Containment'),
        ('p', 'Outpost-4434 (15 personnel or fewer) watches the valley. Affected visitors are detained and given '
              'amnestics; mere trespassers may go to Site-42.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-4434 (CC BY-SA 3.0).')])
    typed('doc4434ad', [('Exhibit', 'Figure A'), ('Item #', 'SCP-4434-A'), ('Status', 'Non-anomalous')], [
        ('h', 'Recreation of an SCP-4434-A instance'),
        ('p', 'Real instances photograph as blank white space and carry a Class II textual cognitohazard. This '
              'sheet is a non-anomalous recreation made for the file, with the address redacted.'),
        ('p', '{If you feel any urge to find the address after reading this, report to Outpost-4434 staff at once.}')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
