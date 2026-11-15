"""The notes of the seventeenth batch (The Forgotten Hotel): a guest register page, a housekeeping note and the
clerk's note, drawn by make_docs2.typed(). Wording is original to this game."""
from make_docs2 import typed

TITLES = {
    'doc17reg': 'Guest Register, Floor H', 'doc17hk': 'Housekeeping Note, H-16', 'doc17cl': 'Desk Note, Lift Lobby',
}


def docs():
    typed('doc17reg', [('Clearance Level', '1'), ('Item #', 'H-17 (proposed)'), ('Object Class', 'Unknown')], [
        ('h', 'Guest register, floor H'),
        ('p', 'Room H-16: guests change every season. Room H-17: last entry 1971. There has been no check-out. '
              'Every name is in pencil, and the handwriting is the same in every line.'),
        ('h', 'Remarks:'),
        ('p', '{The last entry reads: "Will be back for the number."} Do not reserve room H-17. It is not in service.')])
    typed('doc17hk', [('Clearance Level', '1'), ('Item #', 'H-16'), ('Object Class', 'Housekeeping')], [
        ('h', 'Room H-16, daily'),
        ('p', 'Make the bed. Replace the towels. Check the dresser drawer, which is always full of postcards and never '
              'has the same ones twice.'),
        ('h', 'Please note:'),
        ('p', 'Do not enter room H-17. If the number on any door changes while you are walking past it, do not stop. '
              '{Do not count the doors on the floor. The count is wrong, and the floor will tell you so.}')])
    typed('doc17cl', [('Clearance Level', '2'), ('Item #', 'Lift Lobby'), ('Object Class', 'Desk')], [
        ('h', 'Desk note'),
        ('p', 'The key for room H-17 is on the bed in room H-17, where it has always been. The desk does not issue it. '
              'Please do not take it, and do not sign for it.'),
        ('p', 'The lift goes down to the laundry and stops there. It does not go to any other floor, however many '
              'times you press the button. {Please do not ask it to.}')])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
