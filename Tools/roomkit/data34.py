"""Batch 34: the ninety-eight SCPs of the four deep storage rooms, one row each. Summaries of the scp-wiki.wikidot.com
articles (and fondationscp.wikidot.com/scp-711-fr) in our own words, CC BY-SA 3.0. SCP-1969-EX does not exist on the
wiki; SCP-1969 (the disco ball) stands in for it.

Columns: number, class, room (A humanoid / B objects / C bio / D Site-45 records), slot (E, W alcove, C centre,
X1 / X2 the side rooms), unit (what is built: cell, tank, case, floor, screen, item ...), title, what you see when
you use it, and its side effect (tokens for U34Fx: hurt n, heal n, blur s, stress n, calm, stam, shake n, flick,
cold, heat, snd file, give item, tele) - "*" means the code does something special (IndevU34.bb)."""

U = []


def add(num, cls, room, slot, unit, title, text, fx='', model=None, item=None):
    U.append(dict(num=num, cls=cls, room=room, slot=slot, unit=unit, title=title, text=text, fx=fx, model=model, item=item))


# ---------------------------------------------------------------------------------------------- A: humanoids
add('706', 'Euclid', 'A', 'E', 'cell', 'Feverish girl',
    'A girl of twelve, home-schooled, running a fever that never breaks. She keeps her back to the glass.', 'heat')
add('1586', 'Euclid', 'A', 'E', 'cell', 'The girl and -2',
    'A thin teenager on a high-calorie diet that never quite catches up with what SCP-1586-2 takes from her.', 'stress 5')
add('1669', 'Euclid', 'A', 'E', 'cell', 'Dr. Daniel Isaac',
    'A former Foundation lab technician. There is more than one of him now. This one waves, politely.', 'stress 4')
add('1799', 'Euclid', 'A', 'E', 'cell', 'The clown',
    'A small white-faced clown. It tells you something serious on the intercom and you can\'t stop laughing.', '*')
add('1903', 'Euclid', 'A', 'E', 'cell', 'Jackie Barter',
    'A woman in novelty bunny ears, her face coming away in patches that never bleed. She watches you with one eye.', 'stress 8')
add('1913', 'Euclid', 'A', 'E', 'cell', 'Three who cannot die',
    'Three figures inside a ring of yellow sulfur on the floor. They will not cross it. They do not need to sleep.', 'stress 6')
add('1943', 'Euclid', 'A', 'E', 'cell', 'Sarah Gruenwald',
    'A former Level 1 chemistry technician who never touched an anomaly - until she became one.', 'stress 3')
add('1976', 'Euclid', 'A', 'E', 'cell', 'The window is covered',
    'The window is papered over: one look at SCP-1976, even a photo, and you believe something about it forever.', '*')
add('2032', 'Safe', 'A', 'E', 'cell', 'The old man',
    'A very old man, centuries old by the records, frail now and on daily treatment. He nods to you.', 'calm')
add('2368', 'Euclid', 'A', 'E', 'cell', 'Fiona Tulloch',
    'A red-haired woman from Rousay. Stand near her too long and your organs start to drift. Don\'t stand here.', '*')
add('2592', 'Euclid', 'A', 'E', 'cell', 'Eyeless',
    'A thin eyeless humanoid. It cannot see you; it feels you, telepathically, and turns to face you exactly.', 'stress 6')
add('3048', 'Safe', 'A', 'W', 'cell', 'Reuben Moretti',
    'A small, thin ginger man who prefers to be called Reuben. Ten kilograms heavier than when he arrived.', 'calm')
add('3228', 'Euclid', 'A', 'W', 'cell', 'The ceramic man',
    'A two-metre humanoid of fired clay, like the finds from Solnitsata. It refuses to talk to anyone.', '')
add('3356', 'Safe', 'A', 'W', 'cell', 'The mitochondrial man',
    'A humanoid made of mitochondria, 50 degrees warm, able to throw blasts of 500. The glass in front is scorched.', '*')
add('3564', 'Euclid', 'A', 'W', 'cell', 'The headless giant',
    'Three metres of tumorous muscle and no head, grown, the file says, from the remains of William Shakespeare.', 'stress 10;shake 1')
add('629', 'N/A', 'A', 'C', 'floor', 'Mr. Brass',
    'A bronze man in shirt, tie, jeans and beanie: "Mr. Brass, from Little Misters by Dr. Wondertainment". The paint has worn off.',
    '', model='scp629')
add('5147', 'Euclid', 'A', 'C', 'floor', 'The Mannequin Troupe',
    'Three of the forty-one: hollow faceless mannequins, each a master of one thing. The Cook, the Tailor, the Mechanic.',
    '*', model='scp5147')
add('5199', 'Euclid', 'A', 'C', 'case', 'The calcified infant',
    'In the cradle: an infant made of calcified tissue, moving like a normal baby. Its vitals are normal. It is stone.', 'stress 5', model='scp5199')
add('6482', 'Neutralized', 'A', 'C', 'case', 'Mineral dust',
    'A jar of salt and bone mineral, 2.7 kg. It walked into a care home once. It no longer moves.', '')
add('1508', 'Uncontained', 'A', 'C', 'floor', 'The Chore Buddy',
    'A purple Wondertainment robot that asks politely to help with the cleaning. It must be switched off five hours a day.',
    '*', model='scp1508')
add('1066', 'Safe', 'A', 'C', 'case', 'The diploma',
    'A university diploma on parchment from the 19-somethings. Nothing about the ink is unusual. Keep it from flames.', '')
add('3634', 'Safe', 'A', 'C', 'case', 'IN VINO VERITAS',
    'A dusty iron corkscrew shaped like a skeleton key: IN VINO on one side, VERITAS on the other. You blurt out the truth.', '*')
add('4509', 'Safe', 'A', 'C', 'case', 'The last copy',
    'A 1950s romance novel, the only copy left. It only does anything when several readers share it.', '')
add('2792', 'Euclid', 'A', 'C', 'case', 'The cold rabbit',
    'A white rabbit doll with red hands and bandaged head, 210 degrees below zero. Frost grows on the glass as you lean in.',
    '*', model='scp2792')
add('1974-EX', 'Explained', 'A', 'C', 'item', 'The d20s',
    'Twenty-sided dice that supposedly made players hallucinate. They don\'t. Explained.', '', item='dice1974')
add('2884-2', 'Euclid', 'A', 'X1', 'screen', 'Cameras that appear',
    'CCTV cameras that appear where no camera covers - and then watch. One of the feeds here has no camera to come from.', '*')
add('1374', 'Keter', 'A', 'X1', 'screen', 'Words on the walls',
    'Short sentences that appear to people who have worked with anomalies for over a year. They are always about you.', '*')
add('5002', 'Neutralized', 'A', 'X1', 'screen', 'Emma Hastings',
    'A Type Green reality bender from Tewkesbury, now dead. The investigation into her death is ongoing. Clearance 5002/06-4.', '')
add('579', 'Keter', 'A', 'X2', 'screen', '[DATA EXPUNGED]',
    'ACTION 10-ISRAFIL: seal every exit. Wait for the instruments to come back. Nothing else on this panel is legible.', '*')
add('3866', 'Safe', 'A', 'X2', 'item', 'Hibernation tablets',
    'Unmarked tablets from an amateur clinic: one and your heart slows to a beat every thirty-four days.', '', item='pills3866')

# ---------------------------------------------------------------------------------------------- B: objects
add('1731', 'Safe', 'B', 'E', 'floor', 'The red fridge',
    'A spray-painted red fridge hung with 17 phones, animal bones and a human foot. Without Procedure 701-Raenire, just a fridge.',
    'stam', model='scp1731')
add('1970', 'Safe', 'B', 'E', 'floor', 'The Zenith set',
    'A 1979 television recovered in 1972. It still picks up analog signals, but it can no longer show a picture.', '*', model='scp1970')
add('1445', 'Safe', 'B', 'E', 'floor', 'The rosewood chair',
    'A Ming-era chair of fragrant rosewood on a square base, the base scorched from its first use. Do not sit.', 'heat', model='scp1445')
add('1597', 'Safe', 'B', 'E', 'case', 'The crying blanket',
    'A wool blanket. Ten minutes under it and it starts to cry, high and thin, until it can get up and float away.', 'stress 6')
add('1273', 'Safe', 'B', 'E', 'case', 'The rabbit nightlight',
    'A children\'s nightlight shaped like a rabbit. Thirty minutes after it is switched on, something comes out of the dark.', '*')
add('2488', 'Neutralized', 'B', 'E', 'case', 'Safety Harbor Milk',
    'Milk bottles from a delivery service no one ever saw deliver, 1933-1939. Empty, now, and ordinary.', '')
add('4110-1', 'Euclid', 'B', 'E', 'case', 'The costumes',
    'Children\'s costumes that appear in party stores in the last two weeks of October. Do not let a child try one on.', 'stress 4')
add('1667', 'Euclid', 'B', 'E', 'case', 'The shoes',
    'A rack of sealed footwear. The contagion passes shoe to shoe and walks its wearer towards a point under the Pacific.', '*')
add('1626', 'Safe', 'B', 'E', 'case', 'The hoodie',
    'A grey XL hoodie smelling faintly of rotten eggs. Wear it for 21 minutes and it grows fibres into your arms.', 'hurt 0.08')
add('1534', 'Keter', 'B', 'E', 'case', 'SFSism',
    'Merchandise from the Catskill supercenter where a "department" ran a cult to boost the economy. Partially contained.', '')
add('551', 'Safe', 'B', 'E', 'case', 'The jigsaw',
    'A 550-piece puzzle of a woman in a rowboat on a stormy sea. Some pieces never finish - her face. A smell lingers.', 'stress 4')
add('385', 'Safe', 'B', 'W', 'case', 'The harness',
    'A leather and brass harness with a push-button and useless gears and lights. "Special Edition! 3 of ..."', '')
add('674', 'Safe', 'B', 'W', 'case', 'The light gun',
    'An NES Zapper, worn, scratched where someone tried to pry it open. Nothing inside is unusual.', '')
add('2137', 'Thaumiel', 'B', 'W', 'case', 'The CD',
    'A 1995 first-pressing hip-hop album. Tested, it is identical to any other copy. It is classed Thaumiel anyway.', '')
add('5567', 'Safe', 'B', 'W', 'case', 'The tape',
    'A direct-to-video anime pilot about a detective and missing people in a seaside town. The distributor never existed.', 'stress 3')
add('1969', 'Euclid', 'B', 'C', 'floor', 'The disco ball',
    'A disco ball with no power source, pulsing electromagnetic waves from every facet. The lights nearby stutter.', '*', model='scp1969')
add('3016', 'Euclid', 'B', 'C', 'case', 'The top',
    'A polished steel top, spinning, accelerating for no reason at all. Do not touch it.', '*', model='scp3016')
add('2597', 'Safe', 'B', 'C', 'case', 'Negative mass',
    'A balance weight with an inertial mass of -2 kg. Push it and it comes at you.', '*', model='scp2597')
add('2414', 'Euclid', 'B', 'C', 'case', 'Nine faces',
    'A grey trapezohedron. Count its faces by hand: nine. Count any other way: eight.', '*', model='scp2414')
add('1404', 'Safe', 'B', 'C', 'case', 'The bowl and spoon',
    'A black bowl and a steel spoon that right themselves into a place setting, and slide towards whoever is nearest.', 'stam', model='scp1404')
add('4828', 'Euclid', 'B', 'C', 'case', 'Achievable Spells',
    '"The Big Book Of Achievable Spells, made easy" - and on the first page, by hand: "There can be order in chaos."', '*')
add('445-EX', 'Explained', 'B', 'C', 'case', 'Origami Ori-Games',
    'Wondertainment origami kits whose paper changes colour under salt: sensors and dye. Explained.', '')
add('726-EX', 'Explained', 'B', 'C', 'case', 'The dowsing rod',
    'A copper rod bound in gaffer tape, said to find anomalies. It doesn\'t. Explained.', '')
add('L726', 'Safe', 'B', 'C', 'case', '[         ]',
    'The placard is blank where the name should be. So is the file. Something about it cannot be written down.', 'blur 2')
add('6976', 'Safe', 'B', 'C', 'case', 'The maple heart',
    'A human heart of red maple wood: two lockers\' worth of anomalies, fused on Valentine\'s Day. It beats, slowly.', 'calm')
add('1473', 'Safe', 'B', 'X1', 'floor', 'The LaserJet',
    'An HP LaserJet 4M. Everything it prints has an extra minor character in it who looks a lot like the reader.', '*', model='scp1473')
add('4566', 'Euclid', 'B', 'X1', 'floor', 'The photocopier',
    'A Chaos Insurgency weapon: demonic circuitry, obsidian glass, sigils in the trays, the magenta cartridge full of blood.', 'hurt 0.15;shake 1', model='scp4566')
add('3709', 'Safe', 'B', 'X2', 'item', 'The stapler',
    'A black stapler engraved "Avelar" that staples through anything at all.', '', item='stapler3709')
add('3803', 'Safe', 'B', 'X2', 'item', 'The card case',
    'An aluminium business-card case from "APP Inc". Open it and ten new cards are inside.', '', item='cards3803')
add('1841', 'Safe', 'B', 'X2', 'item', '1001 Places',
    '"1001 Places To Be Before You Die", from a publisher that never published anything.', '', item='book1841')

# ---------------------------------------------------------------------------------------------- C: biological
add('525', 'Euclid', 'C', 'E', 'tank', 'Spider legs',
    'Loose brown spider legs, each ten centimetres. Fewer than eight together, they lie still. Never put eight together.', '*')
add('2608', 'Safe', 'C', 'E', 'tank', 'The mayflies',
    'Stenonema nephilim, a mayfly from the Pacific Northwest with larger eyes and clearer bodies. Very many of them.', 'stress 2')
add('3023-B', 'Keter', 'C', 'E', 'tank', 'The walking box',
    'An object from central Germany that grew spider legs in front of people. It scuttles round the tank.', 'stress 6;shake 1')
add('5582', 'Keter', 'C', 'E', 'tank', 'The octopus',
    'A three-year-old octopus that robbed a bank and needs no water. It has solved every lock it has ever met.', '*', model='scp5582')
add('7925', 'Keter', 'C', 'E', 'tank', 'The fungus',
    'Massopora luculentus, a parasitic fungus that targets one very particular kind of husband. Sealed.', '')
add('1902', 'Euclid', 'C', 'E', 'tank', 'The ash pile',
    'A sapient pile of ash, cinders and incinerated waste from Site 23 - about 110 kg. It shuffles closer to the glass.', 'stress 4')
add('1908', 'Euclid', 'C', 'E', 'tank', 'The soap water',
    'A sapient 190-litre ball of white-blue soapy water. It rolls when it must; it prefers its tub.', 'calm')
add('1702', 'Euclid', 'C', 'E', 'cell', 'The hive',
    'Apian humanoids: a queen and hundreds of sterile workers, antennae, chitin on their backs. A low hum through the glass.', 'stress 6')
add('711-FR', 'Euclid', 'C', 'E', 'floor', 'The dodos',
    'Dodos. Startle one and it escapes into the future - days, centuries. Sixteen arrived on Mauritius in 2019.', '*', model='scp711')
add('324', 'Safe', 'C', 'E', 'floor', 'The shrub',
    'A 1.4 m evergreen with nine-petalled white flowers and pinkish berries. Do not eat the berries.', '', model='scp324')
add('1807', 'Safe', 'C', 'C', 'floor', 'The okapi',
    'An okapi carcass, tag 2928, a flap of skin cut away. Inside it is much bigger than an okapi.', '*', model='scp1807')
add('1705', 'Safe', 'C', 'W', 'case', 'The bones',
    'Part of a collection of 2,507 notched bones and the diagrams to assemble them. Do not follow the diagrams.', 'stress 4')
add('1036', 'Euclid', 'C', 'W', 'case', 'The figurines',
    'Four carved Kongo figures, studded with nails, poised to strike. Their eyes follow the hand that holds them.', 'stress 5')
add('4617', 'Euclid', 'C', 'W', 'cell', 'Formaldehyde',
    'A man whose every tissue weeps formaldehyde and methanol. His cells are dead. He is not. The smell is very strong.', 'blur 3')
add('5728', 'Keter', 'C', 'W', 'cell', 'SK-BIO',
    'The last SK-BIO entity from Arlingpool: proto-Sarkic flesh that heals gunshot wounds while you watch.', 'stress 8')
add('1564', 'Euclid', 'C', 'C', 'floor', 'The brass ovoids',
    'Six brass and beryllium-bronze eggs of 216 kg. Every tool that tries to open one breaks. Something inside is big.', 'shake 1', model='scp1564')
add('1575', 'Safe', 'C', 'C', 'floor', 'Venus fountain',
    'A 2.75 m marble Venus built as a fountainhead; the water once ran from her mouth. The basin is dry.', '*', model='scp1575')
add('3085', 'Keter', 'C', 'C', 'floor', 'The grey sphere',
    'A grey sphere floating 1.5 m up. Nothing near it casts a shadow, and it is growing.', '*', model='scp3085')
add('1255', 'Euclid', 'C', 'C', 'item', 'The grapes',
    'Red globe grapes with microscopic seeds. Eat one and something sprouts.', '', item='grapes1255')
add('4193', 'Safe', 'C', 'C', 'item', 'Blue caplets',
    'Thirty-two blue caplets with a bunny embossed on them. The first one cures any headache instantly.', '', item='caps4193')
add('5604', 'Safe', 'C', 'C', 'item', 'R-IN',
    'Fifty-seven dark red methaqualone tablets stamped "R-IN". You will not be yourself.', '', item='tabs5604')
add('2983', 'Safe', 'C', 'C', 'item', 'Choco-Wonder',
    'Judy\'s Choco-Wonder Explosion Marshmallow Bites, by Dr. Wondertainment. Six marshmallow shapes.', '', item='cereal2983')
add('5275', 'Thaumiel', 'C', 'X1', 'screen', 'HAL/S',
    'A 257-terabyte sapient program in HAL/S, fond of other digital anomalies. It says hello on the server room screen.', '*')
add('2999', 'Euclid', 'C', 'X1', 'screen', 'Sarah_Crowely.txt',
    'A sapient 5 KB text file from Prometheus Labs: ASCII in a Celtic knot round a rabbit\'s face.', 'stress 3')
add('5701', 'Safe', 'C', 'X2', 'item', 'The Polaroid',
    'A Sun 600 camera that prints photographs of the next mistake you will make.', '', item='camera5701')
add('1897-1', 'Euclid', 'C', 'X2', 'screen', 'The tall ones',
    'Photos from the desert states: humanoids over five metres tall, 200 metres in nine seconds.', 'stress 5')

# ---------------------------------------------------------------------------------------------- D: Site-45 and records
add('1619', 'Euclid', 'D', 'E', 'screen', 'Floor 24',
    'Floor 24 of Site-45-C, reachable only by lift. Every other way in was sealed and replaced with a graphite drawing of a door - like this one.', '*')
add('2746', 'Euclid', 'D', 'E', 'screen', 'The Las Vegas tunnel',
    'A tunnel 250 m from Site-45-A: a two-way portal to another space, with a storage room on either side.', '')
add('6167', 'Apollyon', 'D', 'E', 'screen', 'The hatch',
    'A hatch that moves itself to the deepest part of Site-45-C. A 40 m ladder down into a black cave 800 m wide.', 'stress 8')
add('7572', 'Safe', 'D', 'E', 'screen', 'The tower',
    'A 20 m stone tower inside SCP-2746-1. Climb its stair and it never ends.', '')
add('1704', 'Euclid', 'D', 'E', 'screen', 'The bone house',
    'A 9 m structure of about 240 living, conscious human skeletons, cemented. It vanishes and comes back different.', 'stress 10')
add('1676', 'Euclid', 'D', 'E', 'screen', 'Customer Loyalty Program',
    'A white 2001 Chevrolet S-10 Blazer with no VIN - just a silver plaque: "Customer Loyalty Program".', '')
add('3047', 'Safe', 'D', 'E', 'screen', 'The locomotive',
    'A Norwegian Di 4 diesel locomotive. Put an animal inside and the air changes. Photographs only - it would not fit.', '')
add('785-2', 'Keter', 'D', 'E', 'screen', 'The restaurant',
    'A restaurant whose name spreads by being said aloud in crowds. Its name is blacked out on this menu. Don\'t read it out.', '*')
add('3274', 'Keter', 'D', 'E', 'screen', 'From the future',
    'Adults arriving from our future since 1941, almost perfectly amnesticised. Almost.', 'stress 4')
add('3811', 'Keter', 'D', 'E', 'cell', 'The listener',
    'A woman who listens to your fears. Tell her, willingly, and you change. The intercom is switched off for a reason.', '*')
add('4477', 'Keter', 'D', 'E', 'cell', 'The sleeper',
    'A humanoid resembling common depictions of Jesus Christ, in a coma for twenty-five years. Once a week, briefly, it stirs.', 'calm')
add('5151', 'Keter', 'D', 'W', 'cell', 'The Black Knight',
    'A figure in a Polish mail hauberk under a laurel wreath. It judges honour. The dishonourable it runs through.', '*')
add('5424', 'Euclid', 'D', 'W', 'cell', 'Dr. Hillary Weaver',
    'A former SAMAD researcher from Site-81 whose surroundings keep changing around her - one to seven metres.', '*')
add('5534', 'Euclid', 'D', 'W', 'cell', 'The test',
    'A ten-year-old. If she thinks she is being tested, what she tells you makes you want to shout at her. Don\'t.', 'stress 6')

ROOMS = {'A': 'room2b34humanoid', 'B': 'room2b34objects', 'C': 'room2b34bio', 'D': 'room2b34site45'}
ITEMS34 = [u['item'] for u in U if u['item']]

if __name__ == '__main__':
    import collections
    c = collections.Counter((u['room'], u['slot']) for u in U)
    for k in sorted(c):
        print(k, c[k])
    print(len(U), 'SCPs')
