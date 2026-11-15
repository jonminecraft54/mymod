"""The notes of the forty-fifth batch: SCP-939 summarised in our own words from scp-wiki.wikidot.com/scp-939
(CC BY-SA 3.0), and original notes for the Morgue, the Off-Shoot Hall and the damaged wing."""
from make_docs2 import typed

TITLES = {'docb45_939': 'SCP-939 Summary (Old Chamber)', 'docb45_morgue': 'Autopsy Log', 'docb45_offshoot': 'Maintenance Ticket: Off-Shoot Halls',
          'docb45_collapse': 'Structural Damage Report'}
DOCS = list(TITLES)


def docs():
    typed('docb45_939', [('Clearance Level', '4'), ('Item #', 'SCP-939'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'Pack predators about 2.2 m tall standing upright, with translucent red skin, no eyes and no brain '
              'case, long jaws lined with faintly glowing red teeth, and spines along the back that feel the air '
              'move. They lure prey by imitating human voices - usually the voices of people they have killed - and '
              'breathe out an amnesiac that makes victims forget why they should not follow the voice.'),
        ('p', 'This pit was their first containment chamber, watched from the gallery above. It was abandoned when '
              'the pack was moved. The voices were not.'),
        ('p', 'If someone in the pit calls for help: there is no one in the pit.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-939 (CC BY-SA 3.0).')])
    typed('docb45_morgue', [('Area', 'Light Containment'), ('Document', 'Autopsy log')], [
        ('h', 'Table 2'),
        ('p', 'Subject D-____, brought down from Heavy Containment at 04:10, presumed dead (no pulse, no breath, '
              'flat EEG). Y-incision begun 04:40.'),
        ('p', '04:52 - subject moved. 04:53 - subject screamed. Restraints held. Procedure halted. The doctor on '
              'duty has asked not to be identified in this log. The subject is still on table 2.')])
    typed('docb45_offshoot', [('Area', 'Light Containment'), ('Document', 'Maintenance ticket')], [
        ('h', 'Off-Shoot Halls - open since last year'),
        ('p', 'Lighting: dead along the whole hall, bulbs replaced twice, both times dead by morning. Floor: '
              'subsidence - holes open overnight, do not step on any dark patch. Door at the end of the west '
              'spoke: jammed and HOT, small flames at the seam, nothing burning behind it.'),
        ('p', 'Do not walk the halls alone. Something old likes it dark.')])
    typed('docb45_collapse', [('Area', 'Heavy Containment'), ('Document', 'Structural damage report')], [
        ('h', 'Wing H-7'),
        ('p', 'Ceiling collapse in the east hall: a turbine housing came down through two floors. Rubble in the '
              'corner rooms, windows cracked by the shock. Further falls likely. Do not stand under the hole.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
