"""The notes of the forty-seventh batch: the legacy rooms of the Indev zone (all original writing)."""
from make_docs2 import typed

TITLES = {'docb47_orient': 'New Personnel Orientation', 'docb47_meeting': 'Meeting Minutes: Wing Review',
          'docb47_medical': 'Medical Bay Standing Orders', 'docb47_cores': 'Core Chambers: Interim Notes'}
DOCS = list(TITLES)


def docs():
    typed('docb47_orient', [('Area', 'Starting room'), ('Document', 'Orientation sheet')], [
        ('h', 'Welcome to the site'),
        ('p', 'Collect the equipment laid out for you before leaving this room: one gas mask, one battery for your '
              'equipment, and this sheet. Do not leave anything behind. Nobody will bring it to you later.'),
        ('p', 'Doors in this wing open with the red button beside them. If a door does not open, it is not meant to.'),
        ('p', 'If you hear something moving in the walls, keep walking.')])
    typed('docb47_meeting', [('Area', 'Conference room'), ('Document', 'Minutes')], [
        ('h', 'Wing review'),
        ('p', '1. The older chambers are to stay in service until the new wing is finished. Agreed.'),
        ('p', '2. The old man in the lower chamber still walks straight through anything in his way. Nobody has '
              'found a wall he will go around. Re-routing corridors instead.'),
        ('p', '3. Chairs keep being found knocked over in this room overnight. Not discussed further.')])
    typed('docb47_medical', [('Area', 'Medical bay'), ('Document', 'Standing orders')], [
        ('h', 'Standing orders'),
        ('p', 'Patients from the core chambers are treated here and nowhere else. Do not move them through the '
              'main corridors.'),
        ('p', 'Burns from the lower chamber look like corrosion and spread for several hours. Clean, dress, observe. '
              'Report any patient who says they can hear a bell.')])
    typed('docb47_cores', [('Clearance Level', '3'), ('Area', 'Core chambers'), ('Document', 'Interim notes')], [
        ('h', 'The first chambers'),
        ('p', 'Bay 1: the bell. Keep it on its pedestal. Do not ring it, and do not let anyone talk you into it.'),
        ('p', 'Bay 2: the refining machine. Input booth left, output booth right. Settings dial on the front panel.'),
        ('p', 'Bay 3: the old man. He moves in a straight line toward whoever he is following and does not go '
              'around anything. The floor of his chamber has to be replaced every month.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
