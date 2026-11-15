"""The notes of the thirty-eighth batch: SCP-1039, SCP-1148 and SCP-1117 summarised in our own words from
scp-wiki.wikidot.com (CC BY-SA 3.0), a maintenance report on the long hallway, and the temporary containment
register for the display hall."""
from make_docs2 import typed

TITLES = {'docb38_1039': 'SCP-1039 Summary', 'docb38_1148': 'SCP-1148 Summary', 'docb38_1117': 'SCP-1117 Summary',
          'docb38_hall': 'Maintenance Report: Corridor L-40', 'docb38_register': 'Temporary Containment Register'}
DOCS = list(TITLES)
TITLES['food1117'] = 'SCP-1117-2 (A Plate of Food)'
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('docb38_1039', [('Clearance Level', '3'), ('Item #', 'SCP-1039'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A doll about 30 cm tall: a sack of tightly woven cloth with a crude ribcage painted on the chest and '
              'a misshapen clay skull for a head. A symbol nobody has translated is marked on its back.'),
        ('p', 'From time to time, one item within roughly 40 metres of it vanishes from wherever it was and turns up '
              'inside the doll\'s hollow body. Only one item at a time; the timing follows no pattern found so far.'),
        ('p', 'Staff leave everything they carry in a locked container outside the radius. Anything missing is '
              'looked for in SCP-1039 first - and only then reported as theft.'),
        ('p', SRC('scp-1039'))])
    typed('docb38_1148', [('Clearance Level', '3'), ('Item #', 'SCP-1148'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'SCP-1148 is not the window but the reflection held on it (SCP-1148-1). It looks like an ordinary '
              'reflection, yet nothing can be seen through the glass from the lit side. From the dark side there '
              'is no reflection and no effect.'),
        ('p', 'The window is set in a wall that splits a containment room in two: the entrance half brightly lit, '
              'the far half kept dark. The difference in light must never be allowed to drop.'),
        ('p', 'After long exposure, viewers feel watched and cannot stop looking. Then they glimpse figures in the '
              'reflection - a hooded man, a winged shape, a pair of eyes - that vanish when looked at directly. Then '
              'they want to go to the glass. Up close, something pulls them in. Nobody has been recovered.'),
        ('p', 'Do not stay in the lit half longer than you must.'),
        ('p', SRC('scp-1148'))])
    typed('docb38_1117', [('Clearance Level', '3'), ('Item #', 'SCP-1117'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'SCP-1117-1 is an old wooden dining table, always covered in food and drink (SCP-1117-2) that '
              'replaces itself as it is eaten - dishes from every cuisine, and always delicious, even served '
              'somewhere else.'),
        ('p', 'Anyone who eats it becomes SCP-1117-3: when they are hungry, the food simply turns up near them, '
              'and nothing else tastes right. Over days their energy drains away until they die of exhaustion or a '
              'harmless infection. Made to eat ordinary food once the effect has set in, they suffer violent nausea '
              'and fatal heart rhythm problems.'),
        ('p', 'Note from the holiday social: a birthday cake nobody brought appeared on the buffet. Whoever looks '
              'at it long enough eats a slice. Treat it as SCP-1117-2.'),
        ('p', SRC('scp-1117'))])
    typed('docb38_hall', [('Area', 'Light Containment'), ('Document', 'Maintenance report')], [
        ('h', 'Corridor L-40'),
        ('p', 'Complaint: staff walking north report reaching the double doors with the two big windows "after much '
              'too long". Some passed the same pillar several times.'),
        ('p', 'Measured length: 21 metres. Measured walking time: up to four minutes.'),
        ('p', 'Recommendation: keep walking. Do not run. The doors are there the third or fourth time.')])
    typed('docb38_register', [('Area', 'Entrance Zone'), ('Document', 'Temporary containment register')], [
        ('h', 'Display hall - pending classification'),
        ('p', '38-01 music box, plays only when nobody is watching. 38-02 snow globe, always snowing. 38-03 '
              'typewriter, types its own containment log. 38-04 rubber duck, never dry. 38-05 ceramic mask, warm. '
              '38-06 teapot, pours cold tea. 38-07 pocket watch, runs backwards.'),
        ('p', 'SCP-1039 is kept on the open plinth in the middle of the hall. EMPTY YOUR POCKETS AT THE DOOR.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
