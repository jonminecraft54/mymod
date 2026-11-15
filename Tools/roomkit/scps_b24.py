"""The 25 SCPs of the twenty-fourth batch, as data. Used by rooms_b24.py (props), make_docs24.py (notes) and
gen_b24.py (the generated Blitz table IndevU24Table.bb). Texts are short summaries in our own words of the SCP Wiki
articles (scp-wiki.wikidot.com/scp-<n>, CC BY-SA 3.0).

Each entry: num, object class, prop, colour (r, g, b), description, containment, remark, click message, effect.
prop: 'plinth' (a small object on a plinth), 'table', 'crate', 'poster' (a framed picture), 'door', 'bed', 'tank',
      'figure' (a tall object), 'none'.
effect keys: stress, inj (injuries), stam (set stamina), give (item), blur (frames), sound (SFX\\Indev\\<name>.wav),
      once (True: the click works once), near (a message shown once when you first come within 2.5 m)."""

SCPS = [
    ('018', 'Euclid', 'crate', (220, 40, 40), 'A red rubber ball that speeds up every time it bounces, gaining energy '
     'from nowhere. Left alone it can smash through walls.', 'Kept in a padded crate. Do not drop it.',
     'The crate is dented from the inside.', 'You lift the lid an inch. Something inside hits it hard enough to slam '
     'it shut again.', dict(stress=5, sound='thump')),
    ('027', 'Keter', 'plinth', (70, 60, 50), 'A man who draws vermin - flies, rats, cockroaches - to himself and '
     'everything near him. He calls himself the Vermin God.', 'Kept sealed. Pest control on call.',
     'Do not open the hatch. You can hear them anyway.', 'Flies pour out of the vent the moment you touch the '
     'hatch. You slam it.', dict(stress=10, sound='foxhiss', blur=200)),
    ('101', 'Euclid', 'plinth', (110, 80, 50), 'A hungry leather bag. It eats what is put in it and grows more '
     'dangerous if it is not fed.', 'Fed 3 kg of raw meat every 48 hours. Never put a hand in.',
     'Feeding is late again.', 'The bag yawns open towards your hand. You pull back in time - nearly.',
     dict(inj=0.3, sound='creak')),
    ('134', 'Safe', 'bed', (200, 170, 230), 'A child whose eyes hold tiny stars, real ones, that drift out of the '
     'sockets now and then.', 'Kept comfortable. Supervised play.', 'She asked for a telescope.',
     'She shows you a star drifting out of one eye. It is very small, and very hot, and beautiful.',
     dict(stress=-10)),
    ('181', 'Euclid', 'figure', (240, 220, 120), 'A man of impossible luck: things simply go his way, often in odd '
     'ways, and not always to the good of those nearby.', 'A comfortable room, a deck of cards and a supervisor.',
     'Do not play cards with him.', 'He tosses you a coin without looking. It lands on its edge and stays there. '
     'Your next breath comes easier.', dict(stam=100, stress=-5)),
    ('262', 'Euclid', 'figure', (90, 90, 120), 'A coat with several arms that come out of its sleeves when it is '
     'worn, and help or hold the wearer as they see fit.', 'Kept on a hanger in a locked case.',
     'It prefers to be worn.', 'One of the empty sleeves reaches out and pats your shoulder. Then it grips, '
     'briefly, too hard.', dict(inj=0.1, stress=5)),
    ('300', 'Safe', 'plinth', (140, 200, 230), 'A glass bottle holding a whole small world, with a sky and weather '
     'that change on their own.', 'On a shelf. Not to be shaken.', 'It is raining in there today.',
     'You peer into the bottle. A tiny storm is crossing a tiny sea. Watching it is oddly calming.',
     dict(stress=-8)),
    ('314', 'Euclid', 'table', (150, 150, 160), 'A knife that only exists while it is moving. When it stops it '
     'vanishes, and it can cut through nearly anything.', 'Kept moving on a turntable at all times.',
     'If the turntable stops, leave.', 'The turntable stutters. For a moment the knife is not there - then it '
     'is, in the table, inches from your hand.', dict(stress=10, sound='zap')),
    ('387', 'Safe', 'table', (230, 70, 50), 'A set of toy bricks that come alive when built into figures. The '
     'figures act out little lives on the table.', 'In a play room. Builds are logged.', 'Do not build anything big.',
     'You snap two bricks together. The little figure you made waves at you and runs off behind a box.',
     dict(stress=-5)),
    ('423', 'Euclid', 'poster', (200, 190, 150), 'A character who inserts himself into written stories, usually '
     'as a helpful man named Ted. He wants to be written into something real.', 'Kept on paper, in a sealed folder.',
     'He has been in this note already.', 'You read the framed page. Halfway down, a man called Ted walks into '
     'the story and waves at you. He was not there before.', dict(stress=5)),
    ('426', 'Euclid', 'plinth', (180, 180, 185), 'A toaster that can only be spoken about in the first person. '
     'People who spend too long near it come to believe that they are a toaster.', 'Exposure limited to 2 hours.',
     'I am a toaster. (Please note the pronoun rule is not optional.)', 'I am a toaster. I am a toaster. You step '
     'back and shake your head - you are not a toaster.', dict(stress=8, near='Everyone here is a toaster. No - I '
     'am a toaster. That came out wrong.')),
    ('432', 'Euclid', 'door', (120, 90, 60), 'A cabinet whose door opens on to an endless dark maze of metal '
     'corridors. Something lives in there.', 'Locked. Exploration suspended.', 'Something scratched back.',
     'You open the cabinet. The corridor inside goes on far past the back of the wall. Something far down it '
     'starts walking toward you. You close it.', dict(stress=12, sound='creak')),
    ('504', 'Safe', 'crate', (220, 50, 40), 'Tomatoes that hate bad jokes: tell one near them and they fire '
     'themselves at the teller at deadly speed.', 'In a greenhouse crate. No comedy in the wing.',
     'Whoever wrote the pun on the door has been reassigned.', 'You say something you think is funny. A tomato '
     'disagrees, at speed.', dict(inj=0.4, sound='thump')),
    ('524', 'Safe', 'bed', (230, 230, 230), 'Walter, a white rabbit who will eat anything at all - wood, metal, '
     'and once, a researcher\'s keycard.', 'A hutch with a lot of hay. Keycards are not to be brought in.',
     'Walter ate the last keycard.', 'Walter hops over and chews your sleeve, and then, thoughtfully, a button.',
     dict(stress=-5)),
    ('847', 'Euclid', 'figure', (210, 200, 180), 'A wooden mannequin that moves when no one is looking, and '
     'cheats at chess.', 'In a locked room with a camera. Always observed.', 'It moved again.',
     'The mannequin is a little closer than it was. Its head has turned toward you.', dict(stress=10, near='The '
     'wooden mannequin was facing the wall when you came in. It is not now.')),
    ('871', 'Safe', 'table', (240, 210, 170), 'Cakes that copy themselves: every cake left uneaten is replaced by '
     'several more, until they fill the room.', 'Staff eat the cakes. Daily.', 'Your turn to eat the cake.',
     'You eat a slice. It is very good cake. Two more appear behind it.', dict(stam=100, inj=-0.1)),
    ('1230', 'Safe', 'plinth', (60, 90, 140), 'A book about dreams: whoever reads it to sleep lives out a '
     'heroic adventure in their dreams, as the hero.', 'Lent by request.', 'Somebody dog-eared page nine.',
     'You read the first lines and for a moment you are a knight on a cliff above a burning sea. Then you are '
     'back, feeling braver.', dict(stress=-15, blur=150)),
    ('1733', 'Safe', 'poster', (120, 70, 40), 'A video of a basketball season opener in which, every time it is '
     'played, the players and the crowd seem more aware of the camera.', 'Played once a year, on opening day.',
     'They waved at the camera last time.', 'The frozen frame on the screen is of a basketball court. Every '
     'player in it is looking straight at you.', dict(stress=8)),
    ('2030', 'Keter', 'poster', (240, 200, 40), 'A comedy game show called LAUGH IS FUN, broadcast from nowhere. '
     'Its host is very dangerous, and very upbeat.', 'Signals jammed. Do not laugh.', 'Do not laugh.',
     'The screen lights up: LAUGH IS FUN! The audience laughs. You do not.', dict(stress=12, sound='applause')),
    ('2317', 'Keter', 'door', (60, 60, 70), 'A door to another world, where something enormous is chained. The '
     'chains are breaking, one every few years.', 'The door is locked. Monthly rituals only.', 'Four chains left.',
     'Behind the door, very far down, something huge pulls once at its chains.', dict(stress=15, sound='drone280')),
    ('409', 'Keter', 'tank', (150, 220, 240), 'A crystal that turns anything that touches it into more crystal, '
     'living people included, slowly and painfully.', 'In a sealed tank. No touching. Ever.',
     'There is a crystal fingerprint on the glass.', 'You touch the tank glass. A thread of crystal creeps over '
     'your fingertip; you scrape it off, and some of the finger with it.', dict(inj=0.5, sound='zap')),
    ('191', 'Safe', 'bed', (160, 160, 170), 'A child whose body was rebuilt with machines. She is gentle, and '
     'she is frightened of being switched off.', 'A child\'s room. Maintenance every month.',
     'She likes it when you say goodnight.', 'She looks up from her colouring and asks, in a voice with a click in '
     'it, whether you are here to switch her off. You say no.', dict(stress=-5)),
    ('2399', 'Keter', 'poster', (200, 60, 40), 'A broken war machine on Jupiter, watching Earth. It is waiting '
     'until it is repaired.', 'Observed from orbit. The picture is the latest.', 'It moved its eye last week.',
     'The photo shows the red machine under Jupiter\'s clouds. In the corner, you are fairly sure, it is looking '
     'back.', dict(stress=10)),
    ('1000', 'Keter', 'figure', (90, 70, 50), 'Bigfoot - a whole people, once far more than us, who live in hiding '
     'and remember what we took from them.', 'A cast of a footprint, kept for study.', 'The cast is fresh.',
     'You touch the footprint cast. It is warm, as if the foot was in it a minute ago.', dict(stress=6)),
    ('087', 'Euclid', 'none', (30, 30, 30), 'A stairwell that goes down further than it should, with a child '
     'crying somewhere below and something with a face that is not a face.', 'Locked. Exploration only with a '
     'light and a tether.', 'Do not go down the stairs.', 'You look down the stairwell. Far below, someone is '
     'crying, and a pale face is looking up.', dict(stress=15, sound='scream457', near='Somewhere far down the '
     'stairs, a child is crying.')),
]
