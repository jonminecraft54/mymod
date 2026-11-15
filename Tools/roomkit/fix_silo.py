"""Repair room2newroom8 (the Omega Silo): an invisible collision floor under the sunk lower level, so nothing falls
through the seams between its floor pieces, and waypoints down the lower tunnel so SCP-173 (and other NPCs) can
path through it. The meshes, lights and models are copied unchanged. The original is kept as .bak_silo.
   python fix_silo.py"""
import os
import shutil
import struct
from rmesh import read_rmesh, write_rmesh, W

PATH = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map\room2newroom8.rmesh'
SRC = PATH + '.bak_silo'


def slab(x0, z0, x1, z1, y):
    """a horizontal quad, both windings (collision from either side)"""
    v = [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)]
    return {'verts': v, 'tris': [(0, 1, 2), (0, 2, 3), (0, 2, 1), (0, 3, 2)]}


def main():
    if not os.path.exists(SRC):
        shutil.copy2(PATH, SRC)
    d = read_rmesh(SRC)
    assert d['header'] == 'RoomMesh' and not d['hidden'] and not d['trailing']
    w = W()
    w.s('RoomMesh')
    w.i(len(d['meshes']))
    for m in d['meshes']:
        for fl, name in m['tex']:
            w.by(fl)
            if fl:
                w.s(name)
        w.i(len(m['verts']))
        for v in m['verts']:
            for k in v[:7]:
                w.f(k)
            w.by(v[7]); w.by(v[8]); w.by(v[9])
        w.i(len(m['tris']))
        for t in m['tris']:
            for k in t:
                w.i(k)
    hidden = [slab(-304, -1024, 1780, 1024, -34.0)]   # under the whole lower level (floors at 0 and -32)
    w.i(len(hidden))
    for h in hidden:
        w.i(len(h['verts']))
        for v in h['verts']:
            for k in v:
                w.f(k)
        w.i(len(h['tris']))
        for t in h['tris']:
            for k in t:
                w.i(k)
    ents = list(d['ents'])
    have = [e['pos'] for e in ents if e['class'] == 'waypoint']
    for p in ((448.0, 4.0, 0.0), (640.0, 4.0, 0.0), (1040.0, 4.0, 0.0), (1180.0, 4.0, 0.0), (1300.0, 4.0, 0.0),
              (1650.0, 4.0, 0.0), (200.0, 4.0, 0.0)):
        if all(abs(p[0] - q[0]) + abs(p[2] - q[2]) > 60 or abs(p[1] - q[1]) > 200 for q in have):
            ents.append({'class': 'waypoint', 'pos': p})
    tmp = PATH + '.tmp'
    write_rmesh(tmp, [], [], ents)
    raw = open(tmp, 'rb').read()
    os.remove(tmp)
    head = 4 + len('RoomMesh') + 4 + 4                          # header string, 0 meshes, 0 hidden
    out = bytes(w.b) + raw[head:]
    open(PATH, 'wb').write(out)
    e = read_rmesh(PATH)
    print('meshes', len(e['meshes']), 'hidden', len(e['hidden']), 'waypoints', sum(1 for x in e['ents'] if x['class'] == 'waypoint'),
          'ents', len(e['ents']), '(was', len(d['ents']), ')')


if __name__ == '__main__':
    main()
