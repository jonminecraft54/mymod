"""Three rooms built from the reference photos (the tenth batch, code in IndevT10.bb).

  room2researchoffice  LCZ  Research Office, from photo 1: two desks' worth of furniture, filing cabinets, a
                            pendant over the desk, a keycard and a note on the desk saying why the team left
  room2medexam         LCZ  Medical Examination, from photo 6: tiled exam room with a steel table, toilet,
                            sink, cabinets and a broken monitor; a patient record and first aid on the table
  room2liftlobby       HCZ  Lift Lobby, from photo 7: a round pillar in the hub, a lift on the west side that
                            goes down to a basement hall with a maintenance note by the bench

Same conventions as rooms_b9.py: the corridor cell (junction) and the side rooms (annex) share the 2048 cell,
doors are door_op() holes in the hub walls, and gen_b10.py turns the room keys into T10_* constants."""
from rooms_b9 import *

D = -704.0          # the lower level of the lift lobby (the same offset the other lift rooms use)


def R_(name, amb=11):
    """Built at 6 units per luxel, twice the lightmap density of the older batches (12): sharper light and
    shadow, and the atlas still stays at or under the 2048 cap that gen_b10.py enforces."""
    return Room(name, luxel=6.0, ambient=amb, fill=0.14)

# the handwritten notes of this batch (make_docs10.py writes them to GFX\items)
TEXTS = {
    'docres1b': ({0: 'Research Office 2 - last entry', 1: 'Samples signed out to Lab 4 at 22:10.',
                  2: 'Nobody signed them back in.', 4: 'The desk lamp still works. Nobody',
                  5: 'wants to turn it off.', 7: 'We stopped sleeping here after the',
                  8: 'window started answering the typing.', 10: 'Pack the notebooks. Leave the',
                  11: 'cabinet. The key stays on the desk.'}, '- Dr. Hale, R&D'),
    'docmed1b': ({0: 'Medical Bay record - incomplete', 1: 'Patient D-2291. Male, 34.',
                  2: 'Arrived 03:40 after the east wing alarm.', 4: 'Vitals normal. Bruise on the left hand,',
                  5: 'shaped like a handprint from inside.', 7: 'Asked for the scale. Weighed 14 kg less',
                  8: 'than the admission sheet says.', 10: 'Discharged himself at 04:12.',
                  11: 'The incident report was never filed.'}, '- Nurse Olund'),
    'docelev1b': ({0: 'Lift 3 - maintenance log', 1: 'Cabin stops at the basement hall only',
                   2: 'when someone holds the call button.', 4: 'Do not ride it alone after the 22:00 check.',
                   6: 'The cabin came up with its doors open,', 7: 'empty, and the light inside was on.',
                   9: 'Replaced the cable. Did not fix the', 10: 'stop. Stop is not a fault.'}, '- Maint. crew B'),
}


def room2researchoffice():
    """Photo 1: a box-shaped office with filing cabinets along the back wall, a desk under a pendant lamp,
    the keycard and the note on the desk, and a battery on the floor by the door."""
    R = R_('room2researchoffice', amb=11)
    junction(R, 'NS', 'lcz', openings={'hubE': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', 192, +1, -400, 400, 520, 352, 'std', door=0)
    # the cabinets run along the north wall, drawers facing into the room
    cabinet_row(R, (300.0, 360.0), (520.0, 360.0), 0, 'S', w=56.0)
    # the desk against the east wall, the chair in front of it
    dtop = desk(R, 600, -170, 740, 170, 0)
    chair(R, 540, 0, 'E')
    pendant(R, 650, 0, 352, power=110, rng=640)
    ceil_light(R, 470, 0, 352, size=48, power=80, rng=680, color=(255, 250, 236))
    plate7(R, 'level2', x1, -210, 'W', yc=250, w=170)
    # the things to find
    item(R, 'docres1b', 630, dtop, -60)
    item(R, 'key2', 690, dtop, 70)
    item(R, 'bat', 340, 0, -300)
    return (R, 'ROF', 'Research Office (Light Containment): an office with filing cabinets and a desk. A keycard and a note explain why the team left.',
            1, 0.6, ((300, 165, -300), (640, 150, 0)))


def room2medexam():
    """Photo 6: a tiled exam room on the west side of the corridor. Steel table, toilet, sink, a cabinet
    run and a counter with a dead monitor."""
    R = R_('room2medexam', amb=11)
    junction(R, 'NS', 'lcz', openings={'hubW': [door_op(0)]})
    x0, z0, x1, z1 = annex(R, 'x', -192, -1, -400, 400, 520, 352, 'med', door=0)
    # exam table in the middle, steel top
    ttop = table(R, -700, -110, -520, 110, 0, h=80, top=WHITE)
    # toilet and tank in the far corner, a basin on a pedestal by the far wall
    R.tube((-740, 0, 300), (-740, 40, 300), 26, WHITE, sides=12, caps=True, lux=12)
    R.box(-772, 40, 270, -744, 110, 330, WHITE, skip='B', lux=10)
    R.box(-772, 80, -330, -700, 92, -190, WHITE, skip='B', lux=10)
    R.tube((-740, 0, -260), (-740, 80, -260), 8, WHITE, sides=6, lux=10)
    # cabinets along the north wall
    cabinet_row(R, (-500.0, 360.0), (-300.0, 360.0), 0, 'S', w=56.0)
    # the counter with a dead monitor
    R.box(-420, 0, -360, -300, 90, -250, DIRTY, skip='B', top=METAL, lux=10)
    R.box(-400, 90, -340, -330, 150, -300, DARK, lux=10)
    ceil_light(R, -520, 0, 352, size=40, power=76, rng=640, color=(240, 250, 255))
    ceil_light(R, -380, -250, 352, size=40, power=60, rng=520, color=(240, 250, 255))
    plate7(R, 'mopp', -640, 398, 'S', yc=300, w=170)
    # the things to find: the patient record and supplies on the steel table
    item(R, 'firstaid', -660, ttop, 40)
    item(R, 'docmed1b', -600, ttop, -40)
    item(R, 'syringe', -560, ttop, 60)
    return (R, 'MED', 'Medical Examination (Light Containment): a tiled exam room with a steel table. A patient record and first aid on the table.',
            1, 0.5, ((-250, 160, 300), (-650, 110, 0)))


def room2liftlobby():
    """Photo 7: the hub is the lobby, with a round pillar in the middle. A lift on the west wall goes down
    to the basement hall, a plain room with a bench and a maintenance log by the lift door."""
    R = R_('room2liftlobby', amb=9)
    AW = wmat('hcz', 384)
    junction(R, 'NS', 'hcz', hub=(-352, -512, 352, 512), hh=352, openings={'hubW': [door_op(0)]})
    # the round pillar in the middle of the lobby (the corridor walks round it)
    R.prism(octo(0, 0, 90), 0, 352, wmat('hcz', 352), caps='TB')
    # the lift: upper stop in the lobby, lower stop in the basement hall
    lift(R, -352, -1, 0, 0, 0, D, AW)
    sign_at(R, 'elevator', -352, -250, 'E', 150, 50, 250)
    plate7(R, 'three', -352, 300, 'E', yc=250, w=200)
    ceil_light(R, -200, -300, 352, size=48, power=80, rng=700, color=(255, 240, 220))
    ceil_light(R, 200, 300, 352, size=48, power=80, rng=700, color=(255, 240, 220))
    # ---- the basement hall, below the lobby's east half
    X0, X1, ZH, HH = -352.0, 760.0, 600.0, 384.0
    out = [(X0, -ZH), (X0, ZH), (X1, ZH), (X1, -ZH)]
    BW = wmat('dark', HH).but(v0=D + HH)
    R.walls(out, D, D + HH, BW, holes={0: [span(out[0], (X0, -96), (X0, 96)) + (D, D + 320)]})
    R.rect_floor(X0, -ZH, X1, ZH, D, HCZFLOOR)
    R.rect_ceil(X0, -ZH, X1, ZH, D + HH, DIRTY)
    plate7(R, 'level2', X0, 300, 'E', yc=D + 240, w=170)
    doorplate7(R, 'decon', X1, 0, 'W', yc=D + 258)
    crate(R, 560, D, 420, yaw=10, kind=1)
    R.box(480, D, -580, 700, D + 46, -520, WOOD, skip='B', lux=10)
    ceil_light(R, 200, 0, D + HH, size=48, power=70, rng=760, color=(232, 240, 255))
    red_lamp(R, 600, -400, D + HH, power=50, rng=500)
    # the things to find: the maintenance log on the bench by the lift
    item(R, 'docelev1b', 520, D + 46, -550)
    return (R, 'LOB', 'Lift Lobby (Heavy Containment): a lobby with a round pillar and a lift down to a basement hall with a maintenance log.',
            2, 0.3, ((250, 165, 380), (-100, 120, -200)))


ALL = [room2researchoffice, room2medexam, room2liftlobby]
