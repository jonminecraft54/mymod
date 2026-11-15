"""The notes of the outdoor expansion (batch 26). Original wording; no real place names."""
from make_docs2 import typed

TITLES = {'doc26_exit': 'Surface Checkpoint Log', 'doc26_shed': 'Utility Shed Checklist', 'doc26_trail': 'Note Left in the Clearing',
          'doc26_lab': 'Forest Laboratory Report', 'doc26_sec': 'Security Control Incident', 'doc26_drain': 'Drainage Chamber Notice',
          'doc26_obs': 'Observation Room Log'}


def docs():
    typed('doc26_exit', [('Clearance Level', '2'), ('Item #', 'Surface'), ('Object Class', 'Log')], [
        ('h', 'Checkpoint log'),
        ('p', '06:10 Fog. Rain since midnight. 07:40 Supply truck turned back, road blocked by a fallen tree. 11:15 Lift '
              'up and down twice, empty both times. Nobody pressed it.'),
        ('p', '{Do not go past the tree line after dark. The floodlights do not reach.}')])
    typed('doc26_shed', [('Clearance Level', '1'), ('Item #', 'Utility shed'), ('Object Class', 'Checklist')], [
        ('h', 'Generator checklist'),
        ('p', 'Fuel: half. Oil: fine. Pull-start sticks in the wet. If the facility loses power, this generator runs '
              'the lift and the floodlights - nothing else. Panel: keep the cover shut, the rain gets in.')])
    typed('doc26_trail', [('Clearance Level', '0'), ('Item #', '-'), ('Object Class', 'Handwritten')], [
        ('h', 'Found under a rock'),
        ('p', 'If you are reading this, you got out too. Do not follow the road east - it loops back. Do not follow the '
              'lights in the trees. They are not lights.'),
        ('p', '{The rest of the page is too wet to read.}')])
    typed('doc26_lab', [('Clearance Level', '2'), ('Item #', 'Forest lab'), ('Object Class', 'Report')], [
        ('h', 'Sample report'),
        ('p', 'Soil, moss and needle samples from the surface. Moss from the north fence grows 4 cm a day and only on '
              'the side facing the facility. Samples sealed. Cabinet 3. Do not open in a warm room.')])
    typed('doc26_sec', [('Clearance Level', '3'), ('Item #', 'Security control'), ('Object Class', 'Incident')], [
        ('h', 'Incident'),
        ('p', 'All monitors cracked at once at 02:14, from the inside. The cameras kept recording. Footage shows the '
              'control room empty, then full of people we do not employ, then empty again.'),
        ('p', '{The console still sparks. Mind your hands.}')])
    typed('doc26_drain', [('Clearance Level', '1'), ('Item #', 'Drainage'), ('Object Class', 'Notice')], [
        ('h', 'Notice'),
        ('p', 'Rainwater from the surface collects here and is pumped out. In heavy rain the channel fills to the '
              'grates. If you hear dripping when it is not raining, report it and leave.')])
    typed('doc26_obs', [('Clearance Level', '2'), ('Item #', 'Observation'), ('Object Class', 'Log')], [
        ('h', 'Watch log'),
        ('p', 'Rain. Fog. Trees. Rain. 14:00 a figure between the third and fourth trees from the left. 14:01 gone. '
              '14:30 a figure between the second and third trees. It is getting closer to the window.')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
