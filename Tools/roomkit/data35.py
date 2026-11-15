"""Batch 35: the twenty-three SCPs of the cell block and the bunker, one row each - summaries of the
scp-wiki.wikidot.com articles in our own words (CC BY-SA 3.0). Same columns as data34.py; the table continues the
batch-34 numbering at index 100 in the game (IndevU34.bb's arrays)."""

U = []


def add(num, cls, room, slot, unit, title, text, fx='', model=None, item=None):
    U.append(dict(num=num, cls=cls, room=room, slot=slot, unit=unit, title=title, text=text, fx=fx, model=model, item=item))


# ---------------------------------------------------------------------------------------------- E: the cell block
add('746', 'Euclid', 'E', 'E', 'cell', 'The bird man',
    'A small avian humanoid, red-faced, beaked, in black feathers and a leg brace. It watches you between the bars, head on one side.', 'stress 4')
add('886', 'Safe', 'E', 'E', 'cell', 'The women and the goats',
    'Identical Irish women and identical Irish goats, each one born to replace the last. The goat in the corner chews and stares.', 'calm')
add('799', 'Euclid', 'E', 'E', 'cell', 'The blankets',
    'Soft, warm, knitted blankets that are alive. They creep towards body heat and they are always hungry.', '*')
add('060', 'Keter', 'E', 'E', 'screen', 'The white oaks',
    'Seventeen white oaks in Minnesota. Burn one and a 2.3 m skeleton walks out of the fire. Do not burn them.', 'stress 6')
add('646', 'Euclid', 'E', 'E', 'screen', 'The grey thing',
    'A translucent grey creature 5.6 m long, 3.5 tonnes, seven pairs of limbs. Photographs only: it does not fit in here.', 'stress 8')
add('478', 'Euclid', 'E', 'E', 'tank', 'The dark moths',
    'Small dark moth-shapes that never eat or sleep and hunt the young. They beat against the glass when you come close.', '*')
add('366', 'Euclid', 'E', 'E', 'tank', 'The parasite',
    'A sealed specimen jar: an endoparasite of possibly extraterrestrial origin, at its egg stage. It is not hatching. Probably.', 'stress 6')
add('1429', 'Euclid', 'E', 'E', 'tank', 'The blue amoebae',
    'Nine glowing blue amoebae, 5 mm across, with no DNA. Living tissue that touches them starts to change.', '*')
add('1779', 'Euclid', 'E', 'E', 'tank', 'The coin-eater',
    'A scaleless nocturnal reptile with a feathery mane that eats only metal coins. It is looking at your pockets.', '*', model='scp1779')
add('3369', 'Euclid', 'E', 'E', 'screen', 'The anecdote',
    'A joke that, once understood, plants another mind in yours. The screen shows only its first word. Don\'t ask for the rest.', '*')
add('569', 'Euclid', 'E', 'C', 'floor', 'The marble heads',
    'Three of the forty-six: floating marble heads of a bald man, drifting, switching between joy and distress.', '*', model='scp569')
add('517', 'Safe', 'E', 'C', 'floor', 'Grandmother Predictions',
    'A fortune-telling machine: an old-woman puppet behind glass, an electric candle. The power cord is cut. The candle is lit.', '*', model='scp517')
add('2890', 'Safe', 'E', 'C', 'item', 'The top hat',
    'A black silk top hat from Wilson and Sons, c. 1890, a crown sewn in the lining. Put it on a figure and the figure lives.', '', item='hat2890')

# ---------------------------------------------------------------------------------------------- F: the bunker
add('1579', 'Safe', 'F', 'C', 'floor', 'The cedar giant',
    'A 3.4 m carved cedar figure, damaged, green with moss that never dries out. It does not rot, and it resists fire.', '*', model='scp1579')
add('806', 'Safe', 'F', 'C', 'floor', 'The projector',
    'A 1900s film projector with a lens of shaved precious stones and an LED array. It plays any film. It shows more than the film.', '*', model='scp806')
add('1512-EX', 'Explained', 'F', 'C', 'floor', 'The organ printer',
    'A modified CNC machine that prints human organs from stem cells. Once anomalous; now just very good engineering. Explained.', '', model='scp1512')
add('2816', 'Safe', 'F', 'C', 'item', 'The paintbrushes',
    'Slightly radioactive brushes. Paint something new and it\'s fine. Copy a famous painting and the copy moves when nobody is looking.', '', item='brush2816')
add('1388', 'Safe', 'F', 'C', 'item', 'SUPER POWERS',
    '"One Size Fits All Superoos": comic-book superhero briefs that stretch to fit anyone. Wear them and you get a power. A small one.', '', item='briefs1388')
add('1912', 'Euclid', 'F', 'C', 'item', 'The pocket watch',
    'A 19th-century pocket watch, finished after its maker died, taken from a militant environmentalist cult. It ticks backwards.', '', item='watch1912')
add('2581', 'Euclid', 'F', 'E', 'case', 'The greeting cards',
    'Greeting cards: get a few thousand together and something happens. These forty are kept far apart from any others.', 'stress 3')
add('3337', 'Safe', 'F', 'E', 'screen', 'May 23rd',
    'Every May 23rd, a gallery of modern art somewhere in the US with one controversial piece. Something happens there.', '')
add('5069', 'Safe', 'F', 'E', 'case', 'The film cans',
    'Eight sealed film cans (1977-1982) by an anomalous artist. They are not shown here. They are not shown anywhere.', '')
add('1479', 'Euclid', 'F', 'E', 'screen', 'The utility room',
    'A basement utility room in a closed coal plant that holds 144 km2 of taiga. Cold air leaks under the door on the photograph.', '*')

ROOMS = {'E': 'room2b35cellblock', 'F': 'room2b35bunker'}
ITEMS35 = [u['item'] for u in U if u['item']]
OFFSET = 100

if __name__ == '__main__':
    import collections
    print(collections.Counter((u['room'], u['slot']) for u in U), len(U))
