"""SCP:CB .rmesh reader / writer (mirrors LoadRMesh / ReadMesh in MapSystem.bb)."""
import struct


class R:
    def __init__(self, data):
        self.d = data
        self.p = 0

    def i(self):
        v = struct.unpack_from('<i', self.d, self.p)[0]
        self.p += 4
        return v

    def b(self):
        v = self.d[self.p]
        self.p += 1
        return v

    def f(self):
        v = struct.unpack_from('<f', self.d, self.p)[0]
        self.p += 4
        return v

    def s(self):
        n = self.i()
        v = self.d[self.p:self.p + n].decode('latin-1')
        self.p += n
        return v


def read_rmesh(path):
    r = R(open(path, 'rb').read())
    out = {'header': r.s(), 'version': -1}
    hdr = out['header']
    trig = hdr in ('RoomMesh.HasTriggerBox', 'RM')
    if hdr == 'RM':
        out['version'] = r.b()

    def mesh():
        m = {'tex': []}
        for j in range(2):
            fl = r.b()
            m['tex'].append((fl, r.s()) if fl else (0, ''))
        nv = r.i()
        vs = []
        for _ in range(nv):
            x, y, z = r.f(), r.f(), r.f()
            u0, v0, u1, v1 = r.f(), r.f(), r.f(), r.f()
            cr, cg, cb = r.b(), r.b(), r.b()
            vs.append((x, y, z, u0, v0, u1, v1, cr, cg, cb))
        nt = r.i()
        ts = [(r.i(), r.i(), r.i()) for _ in range(nt)]
        m['verts'] = vs
        m['tris'] = ts
        return m

    out['meshes'] = [mesh() for _ in range(r.i())]
    out['nocoll'] = []
    if out['version'] >= 0:
        out['nocoll'] = [mesh() for _ in range(r.i())]

    def coll():
        nv = r.i()
        vs = [(r.f(), r.f(), r.f()) for _ in range(nv)]
        nt = r.i()
        ts = [(r.i(), r.i(), r.i()) for _ in range(nt)]
        return {'verts': vs, 'tris': ts}

    out['hidden'] = [coll() for _ in range(r.i())]
    out['triggers'] = []
    if trig:
        for _ in range(r.i()):
            surfs = [coll() for _ in range(r.i())]
            out['triggers'].append((surfs, r.s()))
    ents = []
    for _ in range(r.i()):
        t = r.s()
        e = {'class': t}
        if t == 'screen':
            e['pos'] = (r.f(), r.f(), r.f())
            e['img'] = r.s()
        elif t == 'waypoint':
            e['pos'] = (r.f(), r.f(), r.f())
        elif t == 'light':
            e['pos'] = (r.f(), r.f(), r.f())
            e['range'] = r.f()
            e['color'] = r.s()
            e['intensity'] = r.f()
        elif t == 'spotlight':
            e['pos'] = (r.f(), r.f(), r.f())
            e['range'] = r.f()
            e['color'] = r.s()
            e['intensity'] = r.f()
            e['angles'] = r.s()
            e['inner'] = r.i()
            e['outer'] = r.i()
        elif t == 'soundemitter':
            e['pos'] = (r.f(), r.f(), r.f())
            e['sound'] = r.i()
            e['range'] = r.f()
        elif t == 'playerstart':
            e['pos'] = (r.f(), r.f(), r.f())
            e['angles'] = r.s()
        elif t == 'model':
            e['file'] = r.s()
            e['pos'] = (r.f(), r.f(), r.f())
            e['rot'] = (r.f(), r.f(), r.f())
            e['scale'] = (r.f(), r.f(), r.f())
        elif t == 'item':
            e['pos'] = (r.f(), r.f(), r.f())
            e['name'] = r.s()
            if out['version'] < 0:
                e['tempname'] = r.s()
            e['customangle'] = r.b()
            e['angle'] = (r.f(), r.f(), r.f())
            e['state'] = (r.f(), r.f())
            e['chance'] = r.f()
        elif t == 'door':
            e['pos'] = (r.f(), r.f(), r.f())
            e['dir'] = r.i()
            if out['version'] >= 1:
                e['index'] = r.i()
            e['keycard'] = r.i()
            e['code'] = r.s()
            e['angle'] = r.f()
            e['open'] = r.b()
            if out['version'] >= 0:
                e['locked'] = r.b()
                e['deletehalf'] = r.b()
            e['remote'] = r.b()
            if out['version'] >= 0:
                e['btn'] = [r.f() for _ in range(12)]
        else:
            raise ValueError('unknown point entity %r at %d' % (t, r.p))
        ents.append(e)
    out['ents'] = ents
    out['trailing'] = len(r.d) - r.p
    return out


# ---------------------------------------------------------------- writer

class W:
    def __init__(self):
        self.b = bytearray()

    def i(self, v):
        self.b += struct.pack('<i', int(v))

    def by(self, v):
        self.b.append(int(v) & 255)

    def f(self, v):
        self.b += struct.pack('<f', float(v))

    def s(self, v):
        raw = v.encode('latin-1')
        self.i(len(raw))
        self.b += raw


def write_rmesh(path, meshes, hidden, ents, triggers=()):
    """meshes: list of dict(lm=str|None, tex=str, alpha=bool, verts=[(x,y,z,u,v,lu,lv,r,g,b)], tris=[(a,b,c)])
    hidden: list of dict(verts=[(x,y,z)], tris=[...])
    Written as the classic 'RoomMesh.HasTriggerBox' layout (version -1), which every loader in the game accepts."""
    w = W()
    w.s('RoomMesh.HasTriggerBox' if triggers else 'RoomMesh')
    w.i(len(meshes))
    for m in meshes:
        if m.get('alpha'):
            w.by(0)
            w.by(3)
            w.s(m['tex'])
        else:
            if m.get('lm'):
                w.by(2)       # lightmap layer (uses the 2nd UV set)
                w.s(m['lm'])
            else:
                w.by(0)
            w.by(1)           # opaque diffuse
            w.s(m['tex'])
        w.i(len(m['verts']))
        for v in m['verts']:
            w.f(v[0]); w.f(v[1]); w.f(v[2])
            w.f(v[3]); w.f(v[4]); w.f(v[5]); w.f(v[6])
            w.by(v[7]); w.by(v[8]); w.by(v[9])
        w.i(len(m['tris']))
        for t in m['tris']:
            w.i(t[0]); w.i(t[1]); w.i(t[2])
    w.i(len(hidden))
    for h in hidden:
        w.i(len(h['verts']))
        for v in h['verts']:
            w.f(v[0]); w.f(v[1]); w.f(v[2])
        w.i(len(h['tris']))
        for t in h['tris']:
            w.i(t[0]); w.i(t[1]); w.i(t[2])
    if triggers:
        w.i(len(triggers))
    for surfs, name in triggers:
        w.i(len(surfs))
        for h in surfs:
            w.i(len(h['verts']))
            for v in h['verts']:
                w.f(v[0]); w.f(v[1]); w.f(v[2])
            w.i(len(h['tris']))
            for t in h['tris']:
                w.i(t[0]); w.i(t[1]); w.i(t[2])
        w.s(name)
    w.i(len(ents))
    for e in ents:
        c = e['class']
        w.s(c)
        if c == 'waypoint':
            for k in e['pos']: w.f(k)
        elif c == 'light':
            for k in e['pos']: w.f(k)
            w.f(e['range']); w.s(e['color']); w.f(e['intensity'])
        elif c == 'spotlight':
            for k in e['pos']: w.f(k)
            w.f(e['range']); w.s(e['color']); w.f(e['intensity'])
            w.s(e['angles']); w.i(e['inner']); w.i(e['outer'])
        elif c == 'soundemitter':
            for k in e['pos']: w.f(k)
            w.i(e['sound']); w.f(e['range'])
        elif c == 'model':
            w.s(e['file'])
            for k in e['pos']: w.f(k)
            for k in e['rot']: w.f(k)
            for k in e['scale']: w.f(k)
        elif c == 'screen':
            for k in e['pos']: w.f(k)
            w.s(e['img'])
        else:
            raise ValueError(c)
    w.s('EOF')
    open(path, 'wb').write(bytes(w.b))


if __name__ == '__main__':
    import sys
    from collections import Counter
    for p in sys.argv[1:]:
        m = read_rmesh(p)
        print('==', p, m['header'], 'ver', m['version'], 'trailing', m['trailing'])
        allv = [v for me in m['meshes'] for v in me['verts']]
        xs = [v[0] for v in allv]; ys = [v[1] for v in allv]; zs = [v[2] for v in allv]
        print('  bounds x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f' % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
        for me in m['meshes']:
            cols = Counter((v[7], v[8], v[9]) for v in me['verts']).most_common(2)
            us = [v[3] for v in me['verts']]; lus = [v[5] for v in me['verts']]
            print('  mesh tex', me['tex'], 'v', len(me['verts']), 't', len(me['tris']), 'col', cols,
                  'u %.2f..%.2f lu %.2f..%.2f' % (min(us), max(us), min(lus), max(lus)))
        print('  nocoll', len(m['nocoll']), 'hidden', len(m['hidden']), 'trig', [t[1] for t in m['triggers']])
        print('  ents', Counter(e['class'] for e in m['ents']))
        for e in m['ents']:
            if e['class'] in ('light', 'spotlight', 'model', 'soundemitter', 'door'):
                print('   ', e)
