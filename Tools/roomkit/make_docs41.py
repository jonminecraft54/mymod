"""The notes of the forty-first batch: memos, minutes and logs found in the staff, medical, security and
recreation rooms (all original writing)."""
from make_docs2 import typed

TITLES = {'docb41_break': 'Break Room Memo', 'docb41_minutes': 'Meeting Minutes', 'docb41_testlog': 'Unfinished Test Log',
          'docb41_dclass': 'D-Class Orientation Sheet', 'docb41_gym': 'Note Found in the Gymnasium'}
DOCS = list(TITLES)


def docs():
    typed('docb41_break', [('Area', 'Entrance Zone'), ('Document', 'Memo')], [
        ('h', 'To all staff'),
        ('p', 'Whoever keeps leaving SCP-860 on the counter while they get coffee: it is a containment breach every '
              'time you do it. It is a key, not a bottle opener.'),
        ('p', 'The microwave is not to be used for samples. The vending machine has been refilled. It is still '
              'not giving change.')])
    typed('docb41_minutes', [('Area', 'Entrance Zone'), ('Document', 'Meeting minutes (unfinished)')], [
        ('h', 'Weekly site briefing'),
        ('p', '1. Containment review - deferred. 2. Budget - deferred. 3. The projector keeps showing a face during '
              'presentations. IT says the projector is not connected to anything.'),
        ('p', '4. Dr. ____ reports that SCP-079 has asked, through the projector, to be invited to these meetings. '
              'Request denied. 5. Meeting ended early when the lights'),
        ('p', '[The page ends here.]')])
    typed('docb41_testlog', [('Area', 'Light Containment'), ('Document', 'Test log, half typed')], [
        ('h', 'Test 41-B'),
        ('p', 'Subject: D-9341. Procedure: subject is brought to the research lab and shown the x-ray of specimen '
              '3. Subject is asked to count the ribs. Result: subject counted'),
        ('p', '[The rest of the page is blank. There is coffee on the keyboard, still warm.]')])
    typed('docb41_dclass', [('Area', 'Light Containment'), ('Document', 'Orientation sheet')], [
        ('h', 'Welcome, D-class personnel'),
        ('p', 'Your designation is printed at the top of this sheet. Remember it. Do what you are told. Do not '
              'look at anything you are told not to look at. Blink when you are told to blink.'),
        ('p', 'There are fourteen of these sheets in this block, each with a different number. Someone has crossed '
              'out the number on this one and written yours.')])
    typed('docb41_gym', [('Area', 'Light Containment'), ('Document', 'Torn notebook page')], [
        ('h', 'Gymnasium'),
        ('p', 'We barricaded the gym. Eleven of us - three guards, five researchers, three D. The guards say they '
              'will let more in if they close the doors behind them.'),
        ('p', 'Something big went past the far doors an hour ago. It didn\'t come in. It was laughing. If you are '
              'reading this, we went out the back. Close the doors.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
