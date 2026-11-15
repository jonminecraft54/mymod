"""Documents for the Indev-zone batch (SCP-017, SCP-131, SCP-999). Same layouts as make_docs2.py."""
import os
from PIL import Image
from make_docs2 import typed, note, ITEMS, W, H

if __name__ == '__main__':
    typed('doc017', [('Clearance Level', '4'), ('Item #', 'SCP-017'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-017 is kept in an acrylic cage hung in the middle of Containment Block D. The arc lamps on '
              'the outside of the block and the flood panels inside it are never switched off. {Nothing may '
              'cast a shadow on the cage.}'),
        ('p', 'The lamp circuit drops out when anyone steps down into the pit round the block. It fails one '
              'bank at a time. Reset it at the lever on the north wall of the pit; the lever falls when the '
              'circuit trips and has to be pushed back up.'),
        ('h', 'Description:'),
        ('p', 'SCP-017 is a figure about 80 cm tall with the build of a small child. It has no surface that '
              'can be found, only a shroud of shadow. When a shadow falls on it, it leaps at whatever cast '
              'the shadow and closes over it. The object is not seen again. SCP-017 then goes back to where '
              'it was.'),
        ('h', 'Addendum 017-D:'),
        ('p', 'With every lamp out, the whole pit is its shadow. {Staff who are still below when the last '
              'lamp fails are not recovered.} Staff on the walkways have been left alone.'),
    ])
    typed('doc131', [('Clearance Level', '1'), ('Item #', 'SCP-131'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-131-A and SCP-131-B live in Test Chamber 4-A and may leave it with an escort. During the '
              'lockdown SCP-131-A is caged for its own safety; the cage lock is the lever in the control '
              'office. SCP-131-B was last seen heading down Maintenance Shaft 4.'),
        ('h', 'Description:'),
        ('p', 'The "Eye Pods" are two teardrop-shaped creatures about 30 cm tall, one burnt orange, one '
              'mustard yellow. Each has a single blue eye and rolls on a wheel-like foot. They attach '
              'themselves to anyone who is gentle with them and follow that person about.'),
        ('p', 'They stare at anything dangerous and hardly blink. {While a pod is looking at SCP-173, '
              'SCP-173 does not move.} A pod does blink - about one second in every twenty - and two pods '
              'never blink together.'),
        ('p', 'They squeal when SCP-173 is near. They hide from SCP-106 and watch nothing until it has gone.'),
    ])
    typed('doc999', [('Clearance Level', '1'), ('Item #', 'SCP-999'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-999 is kept in the holding room off Observation 4-C. The door is not locked. Any member '
              'of staff may visit; nobody has ever had to be told to.'),
        ('h', 'Description:'),
        ('p', 'SCP-999 is a mass of translucent orange slime weighing about 54 kg, with the temperament of '
              'a puppy. It crawls to whoever comes in and climbs on them.'),
        ('p', 'Contact produces calm and mild euphoria that outlast the visit. {Stress readings of staff '
              'fall to baseline}, shaking stops and minor injuries are reported as feeling better. It '
              'tires: it needs about two minutes between visitors before it can do it again.'),
        ('h', 'Addendum 999-4:'),
        ('p', 'During the lockdown three staff sat with SCP-999 instead of evacuating. All three were '
              'found calm.'),
    ])
    note('doc017b', {
        0: 'Block D lamp log - read before you go down',
        1: 'The circuit drops every time someone',
        2: 'walks down the ramp. Maintenance say',
        3: "it's the floor sensor. I say it knows.",
        5: 'You get about half a minute. The lamps',
        6: 'go one bank at a time. Count them.',
        8: 'Lever is on the NORTH wall, past the',
        9: 'block. It will have fallen. Push it up.',
        11: 'Reset FIRST. Then the shelves. Not the',
        12: 'other way round.',
        14: 'If the last lamp goes and you are still',
        15: 'down there, there is nothing to write.',
    }, sign='- K. Osei')
    note('doc131b', {
        0: 'If you take the Pods with you:',
        1: 'They follow whoever is kind to them.',
        2: 'Let A out first - lever in the office.',
        4: 'They squeal when the statue is close.',
        5: 'Believe them. Turn round slowly.',
        7: 'They blink. Not often, not together,',
        8: 'but do not make them your only eyes.',
        10: "They won't ride a lift. They catch up.",
        12: 'Do not let the old man near them. They',
        13: 'hide, and then nobody is watching',
        14: 'anything.',
    }, sign='- Dr. H. Marsh, 4-A')
    note('doc999b', {
        0: 'Stores 4 - issue note',
        1: 'The thing in 4-C has been fed. It will',
        2: 'tell you it has not.',
        4: 'If your hands are shaking, go and sit',
        5: 'with it for two minutes. It works. It',
        6: 'has worked on all of us.',
        8: 'The long green crate in the middle',
        9: "stall is jammed. Lean on the lid - don't",
        10: 'use a bar, you will only bend the hasp.',
        12: 'Sign out what you take. Somebody will',
        13: 'want to know where it all went.',
    }, sign='- Stores')
    prev = Image.new('RGB', (W * 3, H))
    for i, n in enumerate(('doc017', 'doc131', 'doc131b')):
        prev.paste(Image.open(os.path.join(ITEMS, n + '.jpg')), (i * W, 0))
    prev.save('out/docs3_preview.png')
    print('docs written')
