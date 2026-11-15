"""Build the four deep storage rooms of batch 34 and write everything derived from them:
     GFX\\map\\<room>.rmesh + lightmap      (with --game, otherwise into out\\)
     IndevU35Data.bb                        generated: slot constants, FillRoom, events - and the SCP table (number,
                                            class, title, text, side effect) and every unit's pivot and models
     b35_rooms.ini.txt / b35_names.txt
   python gen_b35.py --game"""
import os
import sys
import time
import roomkit
import rooms_b35
from gen_b7 import blitz
from data35 import U, OFFSET

LM_MAX = 2048
SCALE = {'scp1445': 0.8, 'scp3085': 0.9}


def bstr(s):
    return '"' + s.replace('"', "'") + '"'


def ini(rooms):
    out = ['', ';INDEV THIRTY-FIFTH BATCH - STORAGE AREAS 10-11 (generated, Tools\\roomkit\\gen_b35.py, IndevU35.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b35_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b35_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


def units_code(rooms):
    L = ['', ';the SCP table (data34.py): number, class, title, text, side effect', 'Function IndevU35Table()']
    for i, u in enumerate(U):
        L.append('\tU34Num(%d) = %s : U34Cls(%d) = %s : U34Title(%d) = %s' % (i + OFFSET, bstr(u['num']), i + OFFSET, bstr(u['cls']), i + OFFSET, bstr(u['title'])))
        L.append('\tU34Text(%d) = %s : U34Fx(%d) = %s' % (i + OFFSET, bstr(u['text']), i + OFFSET, bstr(u['fx'])))
    L += ['\tU34Count = Max(U34Count, %d)' % (len(U) + OFFSET), 'End Function', '',
          ';every unit: its interaction pivot, and its runtime models (U34Unit / U34Model in IndevU35.bb)',
          'Function IndevU35Units(r.Rooms)', '\tSelect r\\RoomTemplate\\Name']
    for R, *_ in rooms:
        L.append('\t\tCase "%s"' % R.name)
        for (idx, p, m, yaw) in R.units:
            L.append('\t\t\tU34Unit(r, %d, %.1f, %.1f, %.1f)' % (idx + OFFSET, p[0], p[1], p[2]))
            model = U[idx]['model']
            if model and m is not None:
                for mm in (m if isinstance(m, list) else [m]):
                    L.append('\t\t\tU34Model(r, %d, "GFX\\map\\props\\%s.b3d", %.1f, %.1f, %.1f, %d, %.2f)'
                             % (idx + OFFSET, model, mm[0], mm[1], mm[2], yaw, SCALE.get(model, 1.0)))
    L += ['\tEnd Select', 'End Function', '']
    return '\n'.join(L)


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b35.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b35_%s.png' % R.name, size=(768, 432))
        built.append(ret)
        print('  %s  %d surfaces  %d units  lightmap %d  %.0fs' % (R.name, len(R.surfs), len(R.units), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U35', FNAME='IndevU35Data.bb', EVENT='u35room', gen='gen_b35.py', src='rooms_b35.py',
              what='The two storage rooms of the thirty-fifth batch')
        p = os.path.join(roomkit.ROOT if hasattr(roomkit, 'ROOT') else r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9', 'IndevU35Data.bb')
        if not os.path.exists(p):
            p = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\IndevU35Data.bb'
        open(p, 'a', encoding='latin-1').write(units_code(built).replace('\n', '\r\n'))
        ini(built)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))
