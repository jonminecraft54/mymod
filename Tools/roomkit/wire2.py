"""Hook IndevAnnex2.bb and the five Indev-zone rooms into the game sources and data files.
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
    bak = p + '.bak_annex2'
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write(text.encode('latin-1'))


def after_line(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.index(nl, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


def before_line(text, anchor, block, marker, nl):
    if marker in text:
        return text, False
    i = text.index(anchor)
    j = text.rfind(nl, 0, i) + len(nl)
    return text[:j] + block.replace('\n', nl) + text[j:], True


done = []
ROOMS = (('room2blockhall', 'IndevFillBlockHall', 'UpdateIndevBlockHall', 'Containment Block D: SCP-017, lamp circuit lever'),
         ('room1testcage', 'IndevFillTestCage', 'UpdateIndevTestCage', 'Test Chamber 4-A: SCP-131-A, cage lock lever'),
         ('room2liftshaft', 'IndevFillLiftShaft', 'UpdateIndevLiftShaft', 'Maintenance Shaft 4: freight lift, fan, SCP-131-B'),
         ('room2cobserve', 'IndevFillCObserve', 'UpdateIndevCObserve', 'Observation 4-C: SCP-999'),
         ('room1store4', 'IndevFillStore4', 'UpdateIndevStore4', 'Stores 4: supplies, jammed crate'))

# ------------------------------------------------------------------ Main.bb
t, nl = load('Main.bb')
t, c = after_line(t, 'Include "IndevAnnex.bb"', 'Include "IndevAnnex2.bb"\n', 'Include "IndevAnnex2.bb"', nl)
done.append(('Main include', c))
ev = ''.join('\tCreateEvent("%s", "%s", 0) ;Indev: %s (IndevAnnex2.bb)\n' % (n, n, note) for n, _, _, note in ROOMS)
t, c = after_line(t, 'CreateEvent("room1whitedoor", "room1whitedoor", 0)', ev, 'CreateEvent("room2blockhall"', nl)
done.append(('Main events', c))
T7, T8 = '\t' * 7, '\t' * 8
al = (T7 + 'Case "blockhall", "blockd", "017", "scp-017", "scp017"\n' + T8 + 'roomName = "room2blockhall"\n'
      + T7 + 'Case "testcage", "131", "scp-131", "scp131", "eyepods"\n' + T8 + 'roomName = "room1testcage"\n'
      + T7 + 'Case "liftshaft", "shaft", "shaft4"\n' + T8 + 'roomName = "room2liftshaft"\n'
      + T7 + 'Case "cobserve", "999", "scp-999", "scp999", "observation"\n' + T8 + 'roomName = "room2cobserve"\n'
      + T7 + 'Case "store4", "stores", "stores4"\n' + T8 + 'roomName = "room1store4"\n')
t, c = after_line(t, 'roomName = "room1whitedoor"', al, 'roomName = "room2blockhall"', nl)
done.append(('Main aliases', c))
save('Main.bb', t)

# ------------------------------------------------------------------ MapSystem.bb / UpdateEvents.bb
t, nl = load('MapSystem.bb')
fr = ''.join('\t\tCase "%s"\n\t\t\t;[Block]\n\t\t\t%s(r) ;Indev: %s (IndevAnnex2.bb)\n\t\t\t;[End Block]\n' % (n, f, note)
             for n, f, _, note in ROOMS)
t, c = before_line(t, 'Case "room2catwalk"', fr, 'IndevFillBlockHall(r)', nl)
done.append(('MapSystem FillRoom', c))
save('MapSystem.bb', t)

t, nl = load('UpdateEvents.bb')
ue = ''.join('\t\t\tCase "%s"\n\t\t\t\t;[Block]\n\t\t\t\t%s(e) ;Indev (IndevAnnex2.bb)\n\t\t\t\t;[End Block]\n' % (n, u)
             for n, _, u, _ in ROOMS)
t, c = before_line(t, 'Case "room2catwalk"', ue, 'UpdateIndevBlockHall(e)', nl)
done.append(('UpdateEvents', c))
save('UpdateEvents.bb', t)

# ------------------------------------------------------------------ NPCs.bb: SCP-173 stands still while an Eye Pod watches it
t, nl = load('NPCs.bb')
if 'Indev131Watches(n)' not in t:
    T = '\t' * 7
    a = T + 'If NoTarget Then move = True' + nl
    i = t.index(a)
    j = t.index(T + 'If move=False Then' + nl, i)
    hook = (a + T + ';Indev: an Eye Pod (SCP-131) is staring at it - it stays put, without the player-is-looking effects' + nl
            + T + 'If move = True Then' + nl
            + T + '\tIf Indev131Watches(n) Then move = 2' + nl
            + T + 'EndIf' + nl)
    mid = t[i + len(a):j]
    new_if = (T + 'If move = 2 Then' + nl + T + '\tn\\State = Max(0, n\\State - FPSfactor / 20)' + nl
              + T + 'ElseIf move=False Then' + nl)
    t = t[:i] + hook + mid + new_if + t[j + len(T + 'If move=False Then' + nl):]
    done.append(('NPCs 173 hook', True))
save('NPCs.bb', t)

# ------------------------------------------------------------------ Indev.bb reset / IndevHazards.bb update chain
t, nl = load('Indev.bb')
t, c = after_line(t, '\tIndev140Reset()', '\tIndevAnnex2Reset()\n', 'IndevAnnex2Reset()', nl)
done.append(('Indev reset', c))
save('Indev.bb', t)
t, nl = load('IndevHazards.bb')
t, c = after_line(t, '\tUpdateIndev140()', '\tUpdateIndev131()\n', 'UpdateIndev131()', nl)
done.append(('IndevHazards update', c))
save('IndevHazards.bb', t)

# ------------------------------------------------------------------ Data
t, nl = load(r'Data\rooms.ini')
if '[room2blockhall]' not in t:
    def room(name, descr, shape, pos):
        return ('\n[%s]\ndescr=%s\nmesh path=GFX\\map\\%s.rmesh\nshape = %s\ncommonness = 0\ndisabledecals = true\n'
                'zone1=4\nset room=%s\nset room priority=15000\n' % (name, descr, name, shape, pos))
    add = '\n;INDEV ANNEX ROOMS, SECOND BATCH - Indev zone (generated meshes, IndevAnnex2.bb)\n;=================================================\n'
    add += room('room2blockhall', 'Containment Block D (Indev). SCP-017 in a floodlit block standing in a sunken floor; ramps, walkways, a lamp circuit that fails.', '2', '0.3')
    add += room('room1testcage', 'Test Chamber 4-A (Indev). SCP-131-A in a wire cage, a control office up a flight of steps.', '1', '0.35')
    add += room('room2liftshaft', 'Maintenance Shaft 4 (Indev). A freight lift down a pipe shaft with an extractor fan; SCP-131-B hides at the bottom.', '2', '0.75')
    add += room('room2cobserve', 'Observation 4-C (Indev). An eight-sided tunnel turning past the window of the SCP-999 holding room.', '2C', '0.5')
    add += room('room1store4', 'Stores 4 (Indev). A brick storeroom with stalls, shelving and a jammed crate.', '1', '0.85')
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('rooms.ini', True))
save(r'Data\rooms.ini', t)

t, nl = load(r'Data\items.ini')
if '[doc017]' not in t:
    add = ''
    for n in ('doc017', 'doc131', 'doc999'):
        add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVpaper.png\n'
                'document = GFX\\items\\%s.jpg\nscale = 0.003\nsound = 0\n' % (n, n))
    for n in ('doc017b', 'doc131b', 'doc999b'):
        add += ('\n[%s]\ngroup = paper\nmodel = GFX\\items\\paper.x\ninvicon = GFX\\items\\INVnote.png\n'
                'document = GFX\\items\\%s.jpg\nscale = 0.003\ntexture override = GFX\\items\\notetexture.jpg\nsound = 0\n' % (n, n))
    t = t.rstrip('\r\n') + nl + add.replace('\n', nl)
    done.append(('items.ini', True))
save(r'Data\items.ini', t)

t, nl = load(r'Data\strings.ini')
names = ('doc017 = Document SCP-017\ndoc017b = Block D Lamp Log\ndoc131 = Document SCP-131\n'
         'doc131b = Eye Pod Handler Note\ndoc999 = Document SCP-999\ndoc999b = Stores 4 Issue Note\n')
t, c = after_line(t, 'docmaint = Electrical Centre Standing Notice', names, 'doc017 = Document SCP-017', nl)
done.append(('strings.ini', c))
save(r'Data\strings.ini', t)

for d in done:
    print(d)
