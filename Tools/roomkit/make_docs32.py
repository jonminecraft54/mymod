"""The notes of the thirty-second batch, Gate V (written for the mod)."""
from make_docs2 import typed

TITLES = {'docgatev': 'Gate V Evacuation Protocol', 'docgatev2': 'Maintenance Note: Circuit 7-V'}
DOCS = list(TITLES)


def docs():
    typed('docgatev', [('Clearance Level', '4'), ('Facility', 'Gate V'), ('Type', 'Emergency exit')], [
        ('h', 'Gate V - underground emergency exit'),
        ('p', 'Gate V is the site\'s last-resort evacuation route: a stairwell down 1024 units from the Entrance '
              'Zone, a bulkhead tunnel, and an atrium ending in a vault hatch that opens on the mountainside, well '
              'outside the perimeter of Gates A and B.'),
        ('p', 'Opening: the Gate V access card, or a Level 4 keycard, at the reader opens the gate quietly. The one '
              'Gate V card is kept by the Site Director, in the Site-42 administration wing. The break-glass '
              'emergency release opens it for anyone - and trips alarm circuit 7-V, which sends the nearest MTF '
              'unit to the exit hatch to wait for whoever comes out.'),
        ('p', 'The atrium console can fire the seal charges over the hatch. They are for hostile entities at the '
              'exit. Firing them collapses the outer passage. It cannot be reopened.'),
        ('p', '{Gate V is not a drill route. Nobody has used it in eleven years.}')])
    typed('docgatev2', [('From', 'Maintenance'), ('Re', 'Alarm circuit 7-V'), ('Status', 'Unresolved')], [
        ('h', 'The breaker in the tunnel'),
        ('p', 'The breaker box for circuit 7-V is still in the Gate V tunnel, halfway along, on the left. If the '
              'circuit is cut before anyone reaches the atrium, the response unit is never called.'),
        ('p', 'We asked for it to be moved to the security office three times. It is still in the tunnel.'),
        ('p', '{Do not tell the D-class.}')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
