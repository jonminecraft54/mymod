"""The notes of the forty-sixth batch: the alternate timeline (all original writing)."""
from make_docs2 import typed

TITLES = {'docb46_timeline': 'Incident Summary: The First Breach', 'docb46_radio': 'Checkpoint 9 Radio Log',
          'docb46_sector': 'Memo: Removal of Sector R', 'docb46_lift': 'Personnel Lift Notice', 'docb46_173': 'SCP-173 Old Cell Procedure'}
DOCS = list(TITLES)


def docs():
    typed('docb46_timeline', [('Clearance Level', '4'), ('Document', 'Incident summary'), ('Status', 'Sealed')], [
        ('h', 'The First Breach'),
        ('p', 'Years before the events now on record, a cascade failure took the power, the doors and the gas '
              'systems of the lower levels at once. Eleven anomalies left containment within the hour.'),
        ('p', 'The lower levels were sealed rather than recovered. The upper site was rebuilt on top of them and '
              'staff were told the lower complex had been decommissioned. It was not. It was closed with people '
              'still inside.'),
        ('p', 'Any record that disagrees with this summary is to be treated as the official version.')])
    typed('docb46_radio', [('Post', 'Checkpoint 9'), ('Document', 'Radio log')], [
        ('h', 'Last entries'),
        ('p', '02:14 - Team relieved early, ordered to the lift. 02:20 - Lift did not return. 02:31 - Miller still '
              'on channel 4 from the lower complex, says the doors down there are on old codes.'),
        ('p', '02:40 - Checkpoint abandoned. Radio left on so Miller has someone to talk to.')])
    typed('docb46_sector', [('Area', 'Research'), ('Document', 'Internal memo')], [
        ('h', 'Sector R'),
        ('p', 'Sector R is to be removed from all site plans, door rosters and maintenance schedules, effective '
              'immediately. The sector does not exist. Staff assigned to it have been reassigned.'),
        ('p', 'Dr. Harrison has declined reassignment.')])
    typed('docb46_lift', [('Area', 'Light Containment'), ('Document', 'Notice')], [
        ('h', 'Personnel Lift'),
        ('p', 'This lift serves the lower complex for authorised personnel only. The car calls itself; do not hold '
              'the doors. If the car arrives with the lights off, wait for the next one.')])
    typed('docb46_173', [('Clearance Level', '2'), ('Item #', 'SCP-173'), ('Area', 'Old cell')], [
        ('h', 'Cell entry procedure (old cell)'),
        ('p', 'Cell entry is made by no fewer than three personnel. Eye contact with the object is kept at all times. '
              'Before blinking, say so out loud and wait for the others to confirm they are looking.'),
        ('p', 'The lights in this cell are on an old circuit and fail. If the lights fail, nobody is looking.'),
        ('p', 'Old Site card in the desk drawer opens the old-pattern readers in the sealed wings.')])


if __name__ == '__main__':
    docs()
    print(DOCS)

