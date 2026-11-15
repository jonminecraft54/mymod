"""SCP-983's notes: a summary of scp-wiki.wikidot.com/scp-983 (CC BY-SA 3.0), and Document 135r (our own wording)."""
from make_docs2 import typed

TITLES = {'doc983': 'SCP-983 Summary', 'doc135r': 'Document 135r: Sing-Along Guidelines'}


def docs():
    typed('doc983', [('Clearance Level', '2'), ('Item #', 'SCP-983'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'SCP-983 is a 1940s wind-up monkey in a faded ringmaster\'s vest, a tarnished brass bell in its left hand and '
              'a brass striking rod in its right. It has no seams or openings, yet it speaks and sings.'),
        ('p', 'It is harmless unless handled by someone on their birthday. Then it backflips and sings "A RING DING DING '
              'DING IT\'S YOUR BIRTHDAY!" every three to four seconds, ringing its bell; each verse ages its owner about '
              'a year. Singing along in time stops it: "BIRTHDAY!", a backflip, and a gumdrop drops from the bell.'),
        ('p', 'A perfect sing-along gives a crystal-clear, faintly glowing candy; a near-perfect one a clear candy. Both '
              'restore the years lost. Other attempts give coloured candies. A black candy is never to be eaten.'),
        ('h', 'Containment'),
        ('p', 'Do not handle SCP-983 on your birthday. If you do, follow Document 135r in Emergency Kit 135r by the door.'),
        ('p', 'Summary of scp-wiki.wikidot.com/scp-983 (CC BY-SA 3.0).')])
    typed('doc135r', [('Clearance Level', '1'), ('Item #', '135r'), ('Object Class', 'Procedure')], [
        ('h', 'If SCP-983 starts singing for you'),
        ('p', '1. Do not panic. Do not put it down and walk away: it keeps singing, and you keep ageing.'),
        ('p', '2. Sing along. Every verse ends "IT\'S YOUR BIRTHDAY!" - join in exactly on that line (click as the line '
              'comes). Too early or too late does not count.'),
        ('p', '3. Six verses in a row, in time, and it stops. The better your timing, the better the candy.'),
        ('p', '4. Clear candy: eat it, it gives the years back. Coloured candy: ask first. Black candy: DO NOT EAT.'),
        ('p', '{The board by the door lists today\'s birthdays. Check it. Every time.}')])


if __name__ == '__main__':
    docs()
    print('2 notes written')
