"""Documents for the Annex rooms.
   Typed sheets are assembled like the earlier Indev documents: clean paper tiled from doc1471.jpg,
   the logo block and the CONFIDENTIAL footer lifted from doc008.jpg, Courier text, orange marker.
   Notes are ruled paper with handwriting; the two code notes leave a box at (205..365, 397..465)
   because Main.bb prints the run's code at 285,431 on those."""
import os
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ITEMS = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\items"
F = r"C:\Windows\Fonts"
W, H = 581, 819
MARK = (255, 170, 60)


def paper():
    src = Image.open(os.path.join(ITEMS, 'doc1471.jpg')).convert('RGB')
    patch = src.crop((20, 640, 560, 800))
    im = Image.new('RGB', (W, H))
    for y in range(0, H, patch.height):
        for x in range(0, W, patch.width):
            p = patch if (y // patch.height) % 2 == 0 else patch.transpose(Image.FLIP_TOP_BOTTOM)
            im.paste(p, (x, y))
    d8 = Image.open(os.path.join(ITEMS, 'doc008.jpg')).convert('RGB')
    im.paste(d8.crop((0, 0, 270, 100)), (0, 0))
    im.paste(d8.crop((0, 758, 581, 819)), (0, 758))
    return im


def typed(name, fields, blocks):
    im = paper()
    d = ImageDraw.Draw(im)
    reg = ImageFont.truetype(os.path.join(F, 'cour.ttf'), 14)
    bold = ImageFont.truetype(os.path.join(F, 'courbd.ttf'), 14)
    y = 15
    for k, v in fields:
        d.text((289, y), k, font=bold, fill=(30, 30, 30))
        d.text((549, y), v, font=reg, fill=(30, 30, 30), anchor='ra')
        y += 24
    cw = d.textlength('M', font=reg)
    cols = int((549 - 32) // cw)
    y = 118
    for kind, text in blocks:
        if kind == 'h':
            d.text((32, y), text, font=bold, fill=(20, 20, 20))
            y += 24
            continue
        indent = 2 if kind == 'b' else 0
        raw = text
        plain = raw.replace('{', '').replace('}', '')
        lines = textwrap.wrap(plain, cols - indent)
        # map highlight state back onto the wrapped lines
        marks = []
        on = False
        for ch in raw:
            if ch == '{':
                on = True
            elif ch == '}':
                on = False
            else:
                marks.append(on)
        pos = 0
        for li, line in enumerate(lines):
            # textwrap drops the spaces at line breaks: resync on the plain text
            while plain[pos:pos + len(line)] != line:
                pos += 1
            x0 = 32 + (indent * cw if (kind == 'b' and li > 0) else 0)
            run = None
            for ci in range(len(line)):
                if marks[pos + ci]:
                    if run is None:
                        run = ci
                elif run is not None:
                    d.rectangle([x0 + run * cw - 1, y - 1, x0 + ci * cw, y + 16], fill=MARK)
                    run = None
            if run is not None:
                d.rectangle([x0 + run * cw - 1, y - 1, x0 + len(line) * cw, y + 16], fill=MARK)
            d.text((x0, y), line, font=reg, fill=(25, 25, 25))
            pos += len(line)
            y += 18
        y += 10
    assert y < 752, (name, y)
    im.save(os.path.join(ITEMS, name + '.jpg'), quality=90)
    return im


def ruled():
    rng = np.random.default_rng(55)
    a = np.zeros((H, W, 3)) + np.array([236.0, 230.0, 212.0])
    a += rng.normal(0, 3.0, (H, W, 1))
    blot = np.asarray(Image.fromarray((rng.random((H // 16, W // 16)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(float)
    a += ((blot - 128) / 128.0 * 5)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for y in range(120, H, 38):
        d.line([(28, y), (556, y)], fill=(150, 162, 200), width=2)
    d.line([(78, 0), (78, H)], fill=(205, 90, 90), width=2)
    d.rectangle([0, 0, 4, H], fill=(206, 200, 184))
    return im


def note(name, rows, sign=None, box=False):
    """rows: {row index: text}; row r sits on the rule at y = 120 + 38 r."""
    im = ruled()
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(F, 'segoesc.ttf'), 19)
    ink = (38, 46, 96)
    for r, text in rows.items():
        assert d.textlength(text, font=f) < 470, (name, text)
        d.text((92, 120 + 38 * r - 30), text, font=f, fill=ink)
    if box:
        d.rectangle([205, 397, 365, 465], outline=(120, 130, 170), width=2)
    if sign:
        d.text((540, 120 + 38 * 17 - 28), sign, font=ImageFont.truetype(os.path.join(F, 'segoesc.ttf'), 17), fill=ink, anchor='ra')
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    im.save(os.path.join(ITEMS, name + '.jpg'), quality=90)
    return im


if __name__ == '__main__':
    typed('doc015', [('Clearance Level', '3'), ('Item #', 'SCP-015'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-015 Annex B (Ventilation Core, Heavy Containment) is entered with a respirator. '
              '{No tool of any kind} - wrench, cutter, key or valve handle - is to touch the pipework.'),
        ('p', 'The extraction fan of the core is left running. If it trips, the black particulate SCP-015 '
              'vents fills the hall in minutes. Restart it from the manual start lever on the south wall.'),
        ('h', 'Description:'),
        ('p', 'SCP-015 is a mass of pipes, vents and boilers that grows while nobody is watching it. It has '
              'pushed some 40 m of new pipe through the east wall of the core. The pipes are bone, wood, '
              'pressed ash, glass and steel. They carry oil, seawater, mercury, rats and one fluid that '
              'has not been identified.'),
        ('p', 'Struck, cut or turned, the mass answers with a jet from the nearest joint. It answers a '
              'running fan the same way for the first seconds - {keep west of the piers} until it settles. '
              'Eleven staff have been lost.'),
        ('h', 'Addendum 015-B:'),
        ('p', 'The red hand wheel on stub 7 was not fitted by Engineering. It was simply there one morning. '
              '{It is not to be turned.}'),
    ])
    typed('doc055', [('Clearance Level', '4'), ('Item #', 'SCP-055'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The object is held in the shielded cell behind the white door at the far end of its chamber. '
              'The chamber is in the Entrance Zone because every order to move it to Heavy Containment has '
              'been forgotten before it was carried out.'),
        ('p', 'Nobody recalls setting the keypad code. Staff who must enter write the reason on a forearm '
              'first, and carry paper.'),
        ('h', 'Description:'),
        ('p', 'SCP-055 is a self-keeping secret. What is learned about it cannot be remembered once the '
              'observer looks away. Every statement on file describes what it is not. It is not round. '
              'It is not dangerous to look at. It is not safe.'),
        ('p', 'Staff leaving the cell report lost time and no memory of the interior. Most come out holding '
              'a note in their own handwriting. {The notes are usually right.}'),
        ('h', 'Addendum 055-3:'),
        ('p', 'Entry is survivable. Repeated entry is not. Staff who went in a third time came out with '
              'injuries nobody could account for, or did not come out. {Two visits per person.}'),
    ])
    typed('docatrium', [('Document', 'Work Order'), ('Ref.', '2C-114'), ('Issued by', 'Maintenance')], [
        ('h', 'Service Atrium 2-C - Upper Store'),
        ('p', 'The lift to the gallery is back in service. Call it from either landing; it only ever serves '
              'the two stops.'),
        ('p', 'The loft door at the far end of the bridge now takes a {Level 2 card}. Too many torches were '
              'walking off.'),
        ('h', 'Restocked this week:'),
        ('b', '- 9V batteries, eye drops, one first-aid kit'),
        ('b', '- one hand radio, on the crate'),
        ('h', 'Note for anyone working up there:'),
        ('p', 'SCP-079 has been seen to recall this lift while staff are on the bridge. If the call panels '
              'go dead, do not force the doors. {Wait. It loses interest after about half a minute.}'),
        ('p', 'The duct fan on the west wall is not a fault. It is supposed to sound like that.'),
    ])
    typed('docgallery', [('Document', 'Closure Notice'), ('Ref.', 'LG-07'), ('Issued by', 'Site Security')], [
        ('h', 'Lower Gallery - closed to all staff'),
        ('p', 'Dr. Vasko did not come up for the evening count. The lift was found at B1 with its door open '
              'and a night-vision set missing from the store.'),
        ('p', 'There is a patch of black corrosion on the gallery floor, between the partitions, that was '
              'not there on Monday. It is larger each time it is checked.'),
        ('h', 'If you must go down:'),
        ('b', '- {Do not stand on the patch and do not touch what is lying on it.}'),
        ('b', '- If the old man comes up through it, put the partitions between you and him. He walks in '
              'straight lines and he does not hurry.'),
        ('b', '- {Call the lift before you go near the body}, not after. It takes its time.'),
        ('p', 'Records staff: Dr. Imre has the office key and will not go down either.'),
    ])
    typed('docmaint', [('Document', 'Standing Notice'), ('Ref.', 'EC-2C'), ('Issued by', 'Engineering')], [
        ('h', 'Electrical Centre 2-C - sector relay'),
        ('p', 'The lever on the north wall isolates the remote door relays of this sector. With the lever '
              'DOWN the control room cannot drive doors, lights or alarms here until the relays re-arm.'),
        ('p', 'Engineering use it before working on door motors. Since the breach Security use it for '
              'another reason: {whatever is sitting in the control room cannot drive them either.} It buys '
              'a few quiet minutes. Push the lever back up afterwards or it will not re-arm.'),
        ('h', 'Respirators:'),
        ('p', 'The masks on the west shelf are signed out to the Ventilation Core in Heavy Containment. The '
              'extraction fan there has tripped twice this month. {Do not go into the core without one.}'),
    ])
    note('doc015b', {
        0: 'Vent core - handover, if anyone reads this',
        1: 'Fan tripped when the lockdown hit. Black',
        2: 'stuff coming off stub 7 ever since. You',
        3: "can't see the far door through it.",
        5: 'Start lever is on the south wall, left of',
        6: 'the tunnel. It sticks. Shove it RIGHT UP.',
        8: "When the fan spins up the pipes don't",
        9: 'like it. Stub 7 spits for a bit. Stand',
        10: 'WEST of the piers till it stops.',
        12: 'My card is in the locker by the south',
        13: "door, right-hand side. Didn't want it on",
        14: 'me if that thing grabs me.',
    }, sign='- M. Halloran, Plant')
    note('note055', {
        0: 'Found this on the back of my hand again.',
        1: 'I have washed it off four times.',
        2: 'I do not know what it opens.',
        4: 'Code:',
        10: "It is filed under U for Unknown, which is",
        11: "where I keep the other thing I can't",
        12: 'remember filing.',
        14: "If you work out what it is for, don't tell",
        15: "me. It won't stick.",
    }, sign='- A. Imre, Records', box=True)
    note('note055self', {
        0: 'YOU wrote this. You will not remember.',
        1: 'It is not round.',
        3: 'The keypad office on the personnel',
        4: 'corridor (Entrance Zone):',
        10: 'You checked it twice. Trust it.',
        12: 'Your legs hurt because you stood still',
        13: 'for a long time. That is all it was.',
        15: 'ONE more visit. Not two. Count them.',
    }, box=True)
    prev = Image.new('RGB', (W * 4, H))
    for i, n in enumerate(('doc015', 'doc055', 'docgallery', 'note055self')):
        prev.paste(Image.open(os.path.join(ITEMS, n + '.jpg')), (i * W, 0))
    prev.save('out/docs_preview.png')
    print('docs written')
