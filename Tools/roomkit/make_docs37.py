"""The notes of the thirty-seventh batch: SCP-028 summarised in our own words from scp-wiki.wikidot.com/scp-028
(CC BY-SA 3.0), and facility notices for the reactor, the archive, the cell block and the balcony hall."""
from make_docs2 import typed

TITLES = {'docb37_028': 'SCP-028 Summary', 'docb37_reactor': 'Reactor Hall Safety Notice',
          'docb37_archive': 'Deep Archive Shelf Notice', 'docb37_cells': 'D-Block Cell Rules',
          'docb37_hall': 'Balcony Hall Guard Roster'}
DOCS = list(TITLES)


def docs():
    typed('docb37_028', [('Clearance Level', '3'), ('Item #', 'SCP-028'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'SCP-028 has no physical form at all. It is an effect: a cube a little over two metres across, centred '
              'on a fixed point in an abandoned storage yard outside a mine. Moving objects, or digging out the '
              'ground under it, changes nothing. No instrument detects it.'),
        ('p', 'A few seconds after stepping into it, a person simply knows something - completely and perfectly. '
              'What they learn is random: a phone book, where someone left their keys, how to rebuild an engine. '
              'Larger insights hit harder. Some subjects did not survive what they learned.'),
        ('p', 'Re-entering repeats the effect, but after two exposures the migraines and dizziness grow worse each '
              'time. The yard is enclosed in a sealed concrete room. Personnel who enter without authorisation are '
              'detained indefinitely.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-028 (CC BY-SA 3.0).')])
    typed('docb37_reactor', [('Area', 'Heavy Containment'), ('Document', 'Reactor hall safety notice')], [
        ('h', 'Read before entering the hall'),
        ('p', 'The blue light over the pool is Cherenkov radiation. If you can see it you are being dosed. The '
              'dosimeters on the gantry are calibrated for staff in hazmat suits only.'),
        ('p', 'Unprotected, the hall dose is lethal in under one minute. Suited staff: 15 minutes maximum per shift.'),
        ('p', 'The service lift is slow by design (shielded cab). Wait for the bell. Retrieved samples from the pool '
              'floor - including the SCP-006 concentrate - are kept in the sealed tray at the bottom.'),
        ('p', 'Do not lean on the gantry rails.')])
    typed('docb37_archive', [('Area', 'Entrance Zone'), ('Document', 'Deep archive notice')], [
        ('h', 'Motorised shelving'),
        ('p', 'The shelves move on their own schedule to reach the requested file. The safety beam has been '
              'faulty since the breach. Never stand in an aisle that is closing.'),
        ('p', 'If you hear the motors, step into the widest gap and stay still. The shelves are tall enough to hide '
              'a person from anyone at the end of the room - this is not why they were built.'),
        ('p', 'Dust masks are in the cabinet by the door.')])
    typed('docb37_cells', [('Area', 'Light Containment'), ('Document', 'D-block cell rules')], [
        ('h', 'Rules'),
        ('p', '1. Lights out at 22:00. 2. Shutters stay down outside escort hours. 3. One cot, one sink, one toilet: '
              'report damage. 4. Nothing under the cot. Guards will check under the cot.'),
        ('p', 'Cell 6 is out of use. If someone in Cell 6 answers when you knock, do not answer back.')])
    typed('docb37_hall', [('Area', 'Light Containment'), ('Document', 'Guard roster')], [
        ('h', 'Balcony hall'),
        ('p', 'One guard on the balcony at all times, one on the floor. Patrol: balcony west to east, down the '
              'stairs, the length of the hall, back up by the lift. The lift is for staff and stretchers only.'),
        ('p', 'The offices on the balcony stay locked. Level 2 card for the supply room.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
