"""Hook IndevAnnex.bb and the six rooms into the game sources and data files.
Safe to run twice: every insertion is skipped when its marker is already there."""
import os
import shutil

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"


def load(rel):
    raw = open(os.path.join(ROOT, rel), 'rb').read()
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    return raw.decode('latin-1'), nl.decode()


def save(rel, text):
    p = os.path.join(ROOT, rel)
    bak = p + '.bak_annex'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


def insert_after(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.index(nl, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


def insert_before(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.rfind(nl, 0, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


done = []

# ------------------------------------------------------------------ Main.bb
t, nl = load('Main.bb')
t, c = insert_after(t, 'Include "Indev140.bb"', 'Include "IndevAnnex.bb"\n', 'Include "IndevAnnex.bb"', nl)
done.append(('Main include', c))
ev = ('\tCreateEvent("room2catwalk", "room2catwalk", 0) ;Indev: Service Atrium lift + SCP-079 recall (IndevAnnex.bb)\n'
      '\tCreateEvent("room2cmaint", "room2cmaint", 0) ;Indev: sector relay lever (IndevAnnex.bb)\n'
      '\tCreateEvent("room2ventcore", "room2ventcore", 0) ;Indev: SCP-015 vent core, fan + particulate (IndevAnnex.bb)\n'
      '\tCreateEvent("room2archive", "room2archive", 0) ;Indev: Records Annex, Dr. Imre (IndevAnnex.bb)\n'
      '\tCreateEvent("room2overlook", "room2overlook", 0) ;Indev: Lower Gallery lift + SCP-106 (IndevAnnex.bb)\n'
      '\tCreateEvent("room1whitedoor", "room1whitedoor", 0) ;Indev: SCP-055 (IndevAnnex.bb)\n')
t, c = insert_after(t, 'CreateEvent("room2newroom8", "room2newroom8", 0)', ev, 'CreateEvent("room2catwalk"', nl)
done.append(('Main events', c))
al = ('\t\t\t\t\t\t\tCase "catwalk", "atrium", "bridge"\n\t\t\t\t\t\t\t\troomName = "room2catwalk"\n'
      '\t\t\t\t\t\t\tCase "cmaint", "maint", "electrical"\n\t\t\t\t\t\t\t\troomName = "room2cmaint"\n'
      '\t\t\t\t\t\t\tCase "ventcore", "015", "scp-015", "scp015", "pipes"\n\t\t\t\t\t\t\t\troomName = "room2ventcore"\n'
      '\t\t\t\t\t\t\tCase "archive", "annex"\n\t\t\t\t\t\t\t\troomName = "room2archive"\n'
      '\t\t\t\t\t\t\tCase "overlook", "gallery"\n\t\t\t\t\t\t\t\troomName = "room2overlook"\n'
      '\t\t\t\t\t\t\tCase "055", "scp-055", "scp055", "whitedoor"\n\t\t\t\t\t\t\t\troomName = "room1whitedoor"\n')
anchor = 'Case "140", "scp-140", "scp140", "chronicle", "records"'
i = t.index(anchor)
j = t.index('roomName = "room2clipboardtextroom"', i)
if 'roomName = "room2catwalk"' not in t:
    k = t.index(nl, j) + len(nl)
    t = t[:k] + al.replace('\n', nl) + t[k:]
    done.append(('Main aliases', True))
# the two code notes: copy the note914 block
if 'Case "note055"' not in t:
    i = t.index('Case "note914"')
    ls = t.rfind(nl, 0, i) + len(nl)
    e = t.index('CopyRectStretch', i)
    le = t.index(nl, e) + len(nl)
    blk = t[ls:le]
    b1 = blk.replace('"note914"', '"note055"').replace('Indev914Code()', 'Indev055Code()')
    b2 = blk.replace('"note914"', '"note055self"').replace('Indev914Code()', 'AccessCode')
    assert b1 != blk and 'AccessCode' in b2
    t = t[:ls] + b1 + b2 + t[ls:]
    done.append(('Main notes', True))
save('Main.bb', t)

# ------------------------------------------------------------------ MapSystem.bb
t, nl = load('MapSystem.bb')
fr = ''
for name, fn, note in (('room2catwalk', 'IndevFillCatwalk', 'Service Atrium 2-C: lift, loft, duct fan'),
                       ('room2cmaint', 'IndevFillCMaint', 'maintenance corner: electrical centre, relay lever'),
                       ('room2ventcore', 'IndevFillVentCore', 'SCP-015 vent core: fan, lever, wheel, lockers'),
                       ('room2archive', 'IndevFillArchive', 'Records Annex 3-C: ceiling fan, SCP-055 file'),
                       ('room2overlook', 'IndevFillOverlook', 'Lower Gallery: lift, office, pit'),
                       ('room1whitedoor', 'IndevFillWhiteDoor', 'SCP-055 chamber: keypad door')):
    fr += '\t\tCase "%s"\n\t\t\t;[Block]\n\t\t\t%s(r) ;Indev: %s (IndevAnnex.bb)\n\t\t\t;[End Block]\n' % (name, fn, note)
t, c = insert_before(t, 'Case "room2newroom8"', fr, 'IndevFillCatwalk(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

# ------------------------------------------------------------------ UpdateEvents.bb
t, nl = load('UpdateEvents.bb')
ue = ''
for name, fn in (('room2catwalk', 'UpdateIndevCatwalk'), ('room2cmaint', 'UpdateIndevCMaint'),
                 ('room2ventcore', 'UpdateIndevVentCore'), ('room2archive', 'UpdateIndevArchive'),
                 ('room2overlook', 'UpdateIndevOverlook'), ('room1whitedoor', 'UpdateIndevWhiteDoor')):
    ue += '\t\t\tCase "%s"\n\t\t\t\t;[Block]\n\t\t\t\t%s(e) ;Indev (IndevAnnex.bb)\n\t\t\t\t;[End Block]\n' % (name, fn)
i = t.index('\t\t\tCase "2935"' + nl)
if 'UpdateIndevCatwalk(e)' not in t:
    t = t[:i] + ue.replace('\n', nl) + t[i:]
    done.append(('UpdateEvents', True))
save('UpdateEvents.bb', t)

# ------------------------------------------------------------------ Data
t, nl = load(r'Data\rooms.ini')
if '[room2catwalk]' not in t:
    def room(name, descr, shape, zone, pos):
        return ('\n[%s]\ndescr=%s\nmesh path=GFX\\map\\%s.rmesh\nshape = %s\ncommonness = 0\ndisabledecals = true\n'
                'zone1=%d\nset room=%s\nset room priority=15000\n' % (name, descr, name, shape, zone, pos))
    add = '\n;INDEV ANNEX ROOMS (generated meshes, IndevAnnex.bb)\n;=================================================\n'
    add += room('room2catwalk', 'Service Atrium 2-C (Indev). A hall with a bridge overhead, a lift up to it and the Upper Store behind a Level 2 door.', '2', 1, '0.35')
    add += room('room2cmaint', 'Maintenance corner (Indev). Electrical Centre 2-C with the sector relay lever, and a janitor closet.', '2C', 1, '0.6')
    add += room('room2ventcore', 'Ventilation Core / SCP-015 annex (Indev). Pipes, black particulate and the extraction fan that clears it.', '2', 2, '0.75')
    add += room('room2archive', 'Records Annex 3-C (Indev). Filing stacks, Dr. Imre and the SCP-055 file.', '2', 3, '0.35')
    add += room('room2overlook', 'Lower Gallery (Indev). An office corridor over a records pit one storey down; a lift goes down to it.', '2', 3, '0.65')
    add += room('room1whitedoor', 'SCP-055 containment chamber (Indev). A dark empty room and a doorway of white light.', '1', 3, '0.5')
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

t, nl = load(r'Data\items.ini')
if '[doc015]' not in t:
    add = ''
    for n in ('doc015', 'doc055', 'docatrium', 'docgallery', 'docmaint'):
        add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
    for n in ('doc015b', 'note055', 'note055self'):
        add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVnote.png\n'
                'document = GFX\\items\\%s.jpg\nscale = 0.003\ntexture override = GFX\\items\\notetexture.jpg\nsound = 0\n' % (n, n))
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('items.ini', True))
save(r'Data\items.ini', t)

t, nl = load(r'Data\strings.ini')
names = ('doc015 = Document SCP-015\ndoc015b = Vent Core Handover Note\ndoc055 = Document SCP-055\n'
         'note055 = Note from Dr. Imre\nnote055self = Note in Your Own Handwriting\n'
         'docatrium = Work Order 2C-114\ndocgallery = Lower Gallery Closure Notice\n'
         'docmaint = Electrical Centre Standing Notice\n')
t, c = insert_after(t, 'doc140 = Document SCP-140', names, 'doc015 = Document SCP-015', nl)
done.append(('strings.ini', c))
save(r'Data\strings.ini', t)

for d in done:
    print(d)
