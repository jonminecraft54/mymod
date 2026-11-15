# Generates VMF sign brushes UV-mapped onto the Indev sign atlas (512x512).
import os
TEX = "miscsigns10"   # atlas file: GFX/map/miscsigns10.jpg
S = 0.25              # hammer units per texture pixel
T = 1                 # sign thickness
SIGNS = [  # name, left, top, right, bottom (pixels)
 ("scp993",10,10,130,50),("scp1074",136,10,256,50),("scp113",262,10,378,50),("scp693",384,10,502,50),
 ("scp719",10,58,130,100),("scp718",136,58,256,100),("scp738",262,58,378,100),("scp330",384,58,502,100),
 ("dr_reyes",12,108,162,150),("dr_okafor",170,108,338,150),("dr_voss",346,108,502,150),
 ("dr_harlan",10,158,162,200),("tech_hale",170,158,338,200),("scp122",346,158,502,200),
 ("silo_hall",10,208,250,270),("launch_control",258,208,502,270),
 ("records_room",10,278,250,340),("painting_storage",258,278,502,340),
 ("lockers",10,348,160,390),("boiler_room",168,348,336,390),("no_entry",344,348,502,390),
 ("indev_sector",8,398,504,500),
]
fid = [0]
def nid(): fid[0]+=1; return fid[0]
def side(p, ua, va):
    return f'''		side
		{{
			"id" "{nid()}"
			"plane" "({p[0]}) ({p[1]}) ({p[2]})"
			"material" "{TEX}"
			"uaxis" "[{ua}] {S}"
			"vaxis" "[{va}] {S}"
			"rotation" "0"
			"lightmapscale" "16"
			"smoothing_groups" "0"
		}}
'''
def brush(name, l, t, r, b, ox, oz):
    w, h = (r-l)*S, (b-t)*S
    x0, x1, y0, y1, z0, z1 = ox, ox+w, 0, T, oz, oz+h
    uo = l - x0/S; vo = t + z1/S          # front face shows exact atlas rect
    f = lambda *a: " ".join(f"{v:g}" for v in a)
    U = f"1 0 0 {uo:g}"; V = f"0 0 -1 {vo:g}"
    faces = [
     ((f(x0,y1,z1),f(x1,y1,z1),f(x1,y0,z1)), "1 0 0 0", "0 -1 0 0"),
     ((f(x0,y0,z0),f(x1,y0,z0),f(x1,y1,z0)), "1 0 0 0", "0 -1 0 0"),
     ((f(x0,y1,z1),f(x0,y0,z1),f(x0,y0,z0)), "0 1 0 0", "0 0 -1 0"),
     ((f(x1,y1,z0),f(x1,y0,z0),f(x1,y0,z1)), "0 1 0 0", "0 0 -1 0"),
     ((f(x1,y1,z1),f(x0,y1,z1),f(x0,y1,z0)), U, V),
     ((f(x1,y0,z0),f(x0,y0,z0),f(x0,y0,z1)), U, V),   # front (-Y)
    ]
    return f'\tsolid\n\t{{\n\t\t"id" "{nid()}"\n' + "".join(side(*x) for x in faces) + '\t}\n'
def vmf(solids):
    return ('versioninfo\n{\n\t"editorversion" "400"\n\t"mapversion" "1"\n\t"formatversion" "100"\n\t"prefab" "0"\n}\n'
            'world\n{\n\t"id" "1"\n\t"mapversion" "1"\n\t"classname" "worldspawn"\n\t"skyname" "sky_day01_01"\n'
            + "".join(solids) + '}\n')
out = os.path.dirname(os.path.abspath(__file__))
allb, x, z, rowh = [], 0, 0, 0
for n,l,t,r,b in SIGNS:
    fid[0] = 1
    open(os.path.join(out, f"sign_{n}.vmf"), "w").write(vmf([brush(n,l,t,r,b,-(r-l)*S/2,0)]))
for n,l,t,r,b in SIGNS:
    if x + (r-l)*S > 140: x, z = 0, z - rowh - 8; rowh = 0
    allb.append(brush(n,l,t,r,b,x,z-(b-t)*S)); x += (r-l)*S + 8; rowh = max(rowh,(b-t)*S)
fid[0] = 1
open(os.path.join(out, "indev_signs_all.vmf"), "w").write(vmf(allb))
print("done", len(SIGNS))
