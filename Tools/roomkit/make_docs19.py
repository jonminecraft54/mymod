"""The notes of the nineteenth batch, drawn by make_docs2.typed(). Original wording; SCP-H09 is our own provisional
concept, not an official designation."""
from make_docs2 import typed

TITLES = {
    'doc19off': 'Office 19-A Memo', 'doc19hoist': 'Hoist Operating Card', 'doc19store': 'Storage B Manifest',
    'doc19h09': 'SCP-H09 Provisional File', 'doc19cell': 'Cell Block D Roster', 'doc19gal': 'Observation Duty Sheet',
}


def docs():
    typed('doc19off', [('Clearance Level', '2'), ('Item #', 'Office 19-A'), ('Object Class', 'Memo')], [
        ('h', 'To whoever has this desk next'),
        ('p', 'The two photographs on the wall are of the river by the old site. Please leave them up. Dr. Hale asked for '
              'them every morning until the transfer, and he still asks for them on the intercom.'),
        ('p', '{The intercom in this office has been disconnected since March.}')])
    typed('doc19hoist', [('Clearance Level', '2'), ('Item #', 'Hoist'), ('Object Class', 'Procedure')], [
        ('h', 'Hoist operation'),
        ('p', '1. Close the cage. 2. Press HOIST once. 3. Do not press DOOR while the cage is moving. The pit below holds '
              'the overflow cell and nothing else.'),
        ('h', 'Remarks:'),
        ('p', '{If the pit lamp is already on when you arrive, go back up.}')])
    typed('doc19store', [('Clearance Level', '1'), ('Item #', 'Storage B'), ('Object Class', 'Manifest')], [
        ('h', 'Shutter bays'),
        ('p', 'B-1 to B-6: spare furniture, filing, two crates of light bulbs. B-7: sealed. B-8: sealed. Shutters are not '
              'motorised. Report any shutter that is heard moving.')])
    typed('doc19h09', [('Clearance Level', '3'), ('Item #', 'SCP-H09'), ('Object Class', 'Euclid (provisional)')], [
        ('h', 'Description'),
        ('p', 'SCP-H09 is a mural of the Foundation emblem drawn in light on the far wall of its chamber. No tube, wire '
              'or paint has been found. The emblem slowly melts and redraws itself in other colours.'),
        ('p', 'On rare occasions the emblem appears behind bars. Staff who see this report the feeling of being on the '
              'wrong side of them.'),
        ('h', 'Containment'),
        ('p', 'Keep the chamber lights off. Do not stay longer than needed. {Do not try to read it.}')])
    typed('doc19cell', [('Clearance Level', '1'), ('Item #', 'Cell Block D'), ('Object Class', 'Roster')], [
        ('h', 'Occupancy'),
        ('p', 'D-19A: vacant, cleaned. D-19B: vacant. The knocking from D-19B is the pipes. Maintenance has checked the '
              'pipes twice. Please do not log it again.')])
    typed('doc19gal', [('Clearance Level', '2'), ('Item #', 'Observation'), ('Object Class', 'Duty sheet')], [
        ('h', 'Gallery duty'),
        ('p', 'One guard on the balcony at all times. Class-D wait on the floor for testing and do not climb the rail. '
              'Testing is cancelled until further notice; they are to wait anyway.')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
