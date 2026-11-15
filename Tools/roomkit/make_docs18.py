"""The notes of The Hollowcrest (batch 18), drawn by make_docs2.typed(). Original wording; the SCP-H entries are
our own provisional concepts, not official designations."""
from make_docs2 import typed

TITLES = {
    'doc18led': 'Night Reception Ledger', 'doc18g117': 'Guest Card, Room 117', 'doc18boil': 'Boiler Log, Basement',
    'doc18kit': 'Kitchen Inventory', 'doc18ball': 'Ballroom Programme', 'doc18hc': 'Hollowcrest Anomaly Register',
}


def docs():
    typed('doc18led', [('Clearance Level', '1'), ('Item #', 'Reception'), ('Object Class', 'Ledger')], [
        ('h', 'Guests, this season'),
        ('p', 'Room 102: Mr. and Mrs. Calder, two nights. Room 117: E. Marsh, checked in, no check-out. Room 214: vacant, '
              'please do not let it be booked. Room 9: nothing written.'),
        ('h', 'Remarks:'),
        ('p', '{Room 117 is still paid up. The desk has not been able to find out by whom.}')])
    typed('doc18g117', [('Clearance Level', '1'), ('Item #', 'Room 117'), ('Object Class', 'Guest card')], [
        ('h', 'Guest card'),
        ('p', 'The telephone in this room is not connected. Please do not lift the receiver. If it rings, please let it. '
              'The desk will not answer calls to this room.'),
        ('h', 'Notes:'),
        ('p', 'Keycard in the top drawer of the desk. {Return it to the desk, not to the room.}')])
    typed('doc18boil', [('Clearance Level', '2'), ('Item #', 'Boiler'), ('Object Class', 'Log')], [
        ('h', 'Boiler log'),
        ('p', 'Boiler off since the last winter of the hotel. The gauge still reads 90 each morning. Nobody has written '
              'the reading down since 1984, when the gauge was painted over.'),
        ('p', '{The panel is warm to the touch. It was warm in the morning too.}')])
    typed('doc18kit', [('Clearance Level', '1'), ('Item #', 'Kitchen'), ('Object Class', 'Inventory')], [
        ('h', 'Stock, cold kitchen'),
        ('p', 'Fridge 1: eggs (none), milk (none), a jar labelled ROOM 117. Shelf 3: two maintenance keys, one for the '
              'ballroom, one for the boiler. Fridge 2 is not on this list because it is not ours.'),
        ('h', 'Please note:'),
        ('p', 'Do not leave the fridge running with the door open when you are alone in the kitchen. It starts again on '
              'its own.')])
    typed('doc18ball', [('Clearance Level', '1'), ('Item #', 'Ballroom'), ('Object Class', 'Programme')], [
        ('h', 'Programme, last dance'),
        ('p', 'Opening waltz. Second waltz. The gentlemen will dance with the gentlemen, if they must. Interval. The band '
              'will play until the last guest has gone home.'),
        ('h', 'Remarks:'),
        ('p', '{No guest has gone home. The band has not stopped since the programme was printed.}')])
    typed('doc18hc', [('Clearance Level', '4'), ('Item #', 'Register'), ('Object Class', 'Provisional')], [
        ('h', 'Hollowcrest anomaly register (provisional, not official designations)'),
        ('p', 'SCP-H01 The Repeating Hall: corridors rearrange themselves between visits.'),
        ('p', 'SCP-H02 The Unoccupied Guest: moves furniture in rooms that nobody has been in.'),
        ('p', 'SCP-H03 The Unlisted Floor: a lift that stops at a level not on the building plan.'),
        ('p', 'SCP-H04 The Ringing Line: a telephone that rings when a guest is in the room.'),
        ('p', 'SCP-H05 The Cold Appliance: fridges that start again when nobody is near.'),
        ('p', 'SCP-H06 The False Reflection: a pool whose surface shows lights that are not there.'),
        ('p', 'SCP-H07 The Silent Attendant: a figure in the laundry that is gone when approached.'),
        ('p', 'SCP-H08 The Shifting Blueprint: a maintenance passage that is drawn differently on each plan.')])


if __name__ == '__main__':
    docs()
    assert len(TITLES) == 6
    print('6 notes written')
