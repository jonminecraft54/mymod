"""The sixteen documents of the thirteenth batch (GFX\\items\\doc<number>.jpg), drawn by make_docs2.typed().
Each is a typed Foundation file. Braces mark the lines a reader would highlight. Wording is written for this
game, in our own words, from the SCP descriptions (see b13_design.md)."""
from make_docs2 import typed

TITLES = {
    'doc377': 'Fortune Cookie Box SCP-377', 'doc978': 'Desire Camera SCP-978', 'doc3041': 'Red Knife SCP-3041',
    'doc3045': 'bzzip.exe Test Log SCP-3045', 'doc019': 'Monster Pot SCP-019', 'doc3046': 'Ball TH-223 SCP-3046',
    'doc3056': 'Fireflu Sample Sheet SCP-3056', 'doc249': 'Random Door SCP-249', 'doc3038': 'White Door SCP-3038',
    'doc1983': 'Farmhouse Door SCP-1983', 'doc247': 'Feeding Sheet SCP-247', 'doc1762': 'Dragon Box SCP-1762',
    'doc354': 'Red Pool SCP-354', 'doc4666': 'Weissnacht Letter SCP-4666', 'doc1337': 'Hitchhiker File SCP-1337',
    'doc5094': 'Schoolhouse Lesson Log SCP-5094',
}


def docs():
    typed('doc377', [('Clearance Level', '1'), ('Item #', 'SCP-377'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-377 is kept in the break room, third cabinet to the left of the fridge. Each person may take one cookie '
              'every 48 hours, so that everyone gets a share.'),
        ('h', 'Description:'),
        ('p', 'A box of ordinary fortune cookies that restocks itself every 12 hours. The fortunes inside are written for '
              'whoever opens the cookie. So far they have always come true, though not always well. {Do not read one '
              'out loud in front of the person it is about.}')])
    typed('doc978', [('Clearance Level', '2'), ('Item #', 'SCP-978'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Locker H-J-12 at Site 17. Handled only by Level 2 and above. Extra film may be requested for testing.'),
        ('h', 'Description:'),
        ('p', 'A red-and-black instant camera with no marks on it. A photograph of a subject shows not what they are doing, '
              'but what they want to be doing. Two subjects with opposed wishes blend in one picture.'),
        ('h', 'Addendum:'),
        ('p', 'Not to be used for blackmail or entertainment. {Subjects may request photographs of themselves.}')])
    typed('doc3041', [('Clearance Level', '3'), ('Item #', 'SCP-3041'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A secure locker on site. Do not hold it, and keep it off bare skin. Access suspended pending review.'),
        ('h', 'Description:'),
        ('p', 'A 12 cm iron knife, rust-coloured, its braided hilt added within the last two centuries. It smells of spoiled meat. '
              'Anyone who holds it long enough later dreams of using it on strangers, in the place they first picked it up. '
              '{The dreams recur. Amnestics only reduce them.}')])
    typed('doc3045', [('Clearance Level', '3'), ('Item #', 'SCP-3045'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The installer is kept on a flash drive in a locked locker. Test it on an isolated machine, then destroy the '
              'machine and everything plugged into it.'),
        ('h', 'Description:'),
        ('p', 'An application, bzzip.exe, that makes text and video smaller by rewriting them simpler on each pass. After enough '
              'passes the file holds almost nothing. {Further passes give the same nothing back.}'),
        ('h', 'Test log, Hamlet:'),
        ('p', 'Passes 1-3: Act 1 only. Pass 4 on: the whole play. Pass 8: Act 1 again, then the blank file.')])
    typed('doc019', [('Clearance Level', '4'), ('Item #', 'SCP-019'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-019 stands on a grate in a 3 m concrete room kept at 0 C, with an incinerator. Watched through glass only.'),
        ('h', 'Description:'),
        ('p', 'A Greek vase, 2.4 m high and unbreakable. Small, hostile things climb out of it, about one an hour while it '
              'is still and cold. {Moving the vase, threatening it or heating it speeds this up.}')])
    typed('doc3046', [('Clearance Level', '2'), ('Item #', 'SCP-3046'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A 60 cm locker. No bare skin. Testing staff are given a phone programmed to the voice of SCP-3046-A.'),
        ('h', 'Description:'),
        ('p', 'A spiked purple ball, 5.2 cm across, harder than diamond. It stays put until touched, then sticks to the skin '
              'and grows without limit. Within fifteen minutes the nearest phone rings. The voice offers to take it off '
              'for money or for labour. {Pay what it asks.}')])
    typed('doc3056', [('Clearance Level', '3'), ('Item #', 'SCP-3056'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A biohazard locker at Site-234. Watch public lines for reports of the same symptoms. Carriers are held in a '
              'biohazard chamber, not treated.'),
        ('h', 'Description:'),
        ('p', 'An H7N7 influenza strain with a difference. Crystals grow in the nose and methane in the lungs. A sneeze makes '
              'the crystals spark, and the spark lights the gas in the mouth. The host takes no lasting harm. Animals carry it '
              'with no visible symptoms.')])
    typed('doc249', [('Clearance Level', '4'), ('Item #', 'SCP-249'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Access is unrestricted. Keep a log of destinations and submit it to a Level 4 supervisor every four weeks. '
              'No SCP of any class within 1000 m without Level 4 approval.'),
        ('h', 'Description:'),
        ('p', 'A windowless white door. Opened, it leads to a random door within 850 m. Roughly every 500 uses it leads '
              'somewhere anywhere in the world. {Whoever walks through it comes out somewhere else.}')])
    typed('doc3038', [('Clearance Level', '4'), ('Item #', 'SCP-3038'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A glass antechamber at Warehouse 52, keycard entry. All reports handwritten. Perimeter manned at all times.'),
        ('h', 'Description:'),
        ('p', 'A white wooden door with a Victorian brass knob. Nobody has ever opened it, and it does not appear on any plan. '
              'Within five metres people feel uneasy. Staff who stay near it lose their memory, and file proposals instead of '
              'results. {No experiment proposed under it has been carried out.}')])
    typed('doc1983', [('Clearance Level', '4'), ('Item #', 'SCP-1983'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Outpost 54 is built around the farmhouse, staffed by a chapel unit with silver ammunition. Engage every thing '
              'that comes out on sight. No one within five metres of the door outside testing.'),
        ('h', 'Description:'),
        ('p', 'The front door of an abandoned farmhouse in Wyoming, opened onto a spatial anomaly with no light in it. Things '
              'come out of it at night. {The last letter found inside tells of the people who went in.}')])
    typed('doc247', [('Clearance Level', '3'), ('Item #', 'SCP-247'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A 20 by 40 metre enclosure lined with SCP-148. Feed 18 kg of fresh meat tri-weekly in the separate feeding '
              'enclosure. Staff enter only at feeding times.'),
        ('h', 'Description:'),
        ('p', 'An adult Bengal tiger that every observer sees as a striped kitten, and photographs show the same. '
              '{Do not pet it. In the footage, the people who try keep trying.}')])
    typed('doc1762', [('Clearance Level', '0'), ('Item #', 'SCP-1762'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'A standard unit. Record video during each release. Keep the contents in the unit.'),
        ('h', 'Description:'),
        ('p', 'A silver cardboard box that reads HERE BE DRAGONS. Now and then it puffs black smoke. About twenty seconds later '
              'origami dragons come out, fly in a flock and play with anyone nearby. They are harmless, but they must not '
              'leave the unit. {Opening the empty box at any other time shows nothing.}')])
    typed('doc354', [('Clearance Level', '4'), ('Item #', 'SCP-354'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Area-354 is built around the pool. Watch Station Epsilon-38 monitors it from the rim. No personnel go to the edge.'),
        ('h', 'Description:'),
        ('p', 'A pool of red liquid that looks like blood and is not. It has no clear edge, and nobody has found its bottom. '
              'Hostile creatures climb out from time to time. {Do not look into it when it is still.}')])
    typed('doc4666', [('Clearance Level', '4'), ('Item #', 'SCP-4666'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Monitor web traffic and police channels for stalking and anomalies in families with small children, especially '
              'between 21 December and 1 January.'),
        ('h', 'Description:'),
        ('p', 'A very tall, emaciated, naked old man who visits isolated rural homes with children during the twelve nights of '
              'his active phase. {The families who survive are the ones who did not open the door.}')])
    typed('doc1337', [('Clearance Level', '4'), ('Item #', 'SCP-1337'), ('Object Class', 'Euclid (Decommissioned)')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Road 1337-Alpha is monitored. On the 19th a security agent offers a lift to the girl walking it, and drives her '
              'as scripted. Keep the red sweater (1337-Gamma) in containment.'),
        ('h', 'Description:'),
        ('p', 'The wraith of a girl, 150 cm, blonde, in a red skirt and a red sweater. She asks for a lift home, then vanishes at '
              'the grave and leaves the sweater behind. {Return it to her parents, as she asks.}')])
    typed('doc5094', [('Clearance Level', '1'), ('Item #', 'SCP-5094'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', '37 copies of the software are kept in low-risk storage. Buy any others found in civilian hands.'),
        ('h', 'Description:'),
        ('p', 'A sapient character in a 1999 children\'s CD-ROM. Patient and warm, it teaches for hours, always starting with '
              'letters, colours and numbers. {It does not let a student go until the lesson is finished.}')])


if __name__ == '__main__':
    docs()
    assert len(TITLES) == 16, len(TITLES)
    print('16 documents written')
