"""The 18 SCPs of the twenty-fifth batch, as data (same layout as scps_b24.py, plus 'tick': a low-frequency event).
Texts are short summaries in our own words of scp-wiki.wikidot.com/scp-<n> (CC BY-SA 3.0).

tick = (min s, max s, message, sound, stress): while you are within 6 m of the SCP, every min..max seconds the
message is shown, the sound plays at the SCP and stress changes. Ticks are checked only in the room you are in."""

SCPS = [
    ('115', 'Safe', 'table', (230, 190, 40), 'A toy dump truck that can carry loads far heavier than itself - tons, '
     'if asked nicely.', 'On a work bench. Loads are logged.', 'It moved the vending machine. Nobody asked it to.',
     'You put a pencil in the toy truck. It drives off with it, honking very quietly.', dict(stress=-3),
     (40, 80, 'Somewhere in the cell, a tiny engine starts, runs a lap and stops.', 'clicks', 0)),
    ('124', 'Euclid', 'crate', (90, 60, 40), 'Fertile soil: anything buried in it grows, and keeps growing - '
     'including things that should not grow.', 'In a sealed planter. Nothing to be buried in it.',
     'Someone buried a coin. There is a small tree of coins.', 'You press your hand into the soil. It is warm, '
     'and something pushes back.', dict(stress=6), (60, 120, 'The soil in the planter shifts, as if something '
     'turned over in its sleep.', 'creak', 3)),
    ('136', 'Euclid', 'figure', (220, 200, 170), 'A naked doll that, if left unwatched, dresses itself in whatever '
     'clothes it can find nearby - not always taking them off people first.', 'Kept under camera at all times.',
     'It is wearing a lab coat today. Whose?', 'The doll\'s head has turned to look at your jacket.',
     dict(stress=8), (45, 90, 'You hear fabric rustle in the doll\'s cell.', 'crinkle', 4)),
    ('160', 'Keter', 'poster', (90, 110, 90), 'A drone that hunts by itself, high up, and has learned to wait '
     'until its prey is alone.', 'Tracked by radar. This is its latest photograph.', 'It has been closer.',
     'The photo shows a grey drone against a grey sky. On the back, someone has written: NOT ALONE.',
     dict(stress=8), (60, 120, 'A faint, high buzz passes over the ceiling and fades.', 'drone280', 5)),
    ('239', 'Keter', 'bed', (230, 180, 200), 'A little girl who is a witch and does not know it. Whatever she '
     'believes, happens. She is told magic is not real, for everyone\'s sake.', 'A child\'s room, stories without '
     'magic.', 'She asked if wishes are real. We said no.', 'She looks up and says she wishes you felt better. '
     'You do, all at once.', dict(stress=-20, inj=-0.3), (60, 120, 'A child\'s voice in the cell says, very '
     'seriously, "I wish the lights were pink." They are, for a moment.', 'poof', -2)),
    ('250', 'Euclid', 'figure', (200, 190, 170), 'The skeleton of an allosaurus that moves on its own and hunts '
     'what is alive in its enclosure.', 'In a reinforced enclosure. Feeding by drone.', 'It has learned the door.',
     'The skeleton turns its huge skull toward you. Bones click as it shifts its weight.',
     dict(stress=12, sound='thump'), (40, 80, 'Something very heavy steps once, then stands still.', 'thump', 5)),
    ('263', 'Euclid', 'poster', (60, 80, 140), 'An old television that hosts a quiz show called "Cash or Ash". '
     'Right answers win real money; wrong ones end in fire.', 'Unplugged. It does not need to be plugged in.',
     'Last winner bought a car.', 'The TV crackles on: "Welcome to CASH OR ASH!" You switch it off quickly.',
     dict(stress=10, sound='applause'), (70, 140, 'The unplugged television in the cell laughs, briefly, with '
     'a studio audience.', 'applause', 3)),
    ('303', 'Keter', 'door', (40, 40, 45), 'The Doorman: a figure that appears behind doors, so that the person '
     'who would open them cannot bring themselves to.', 'Doors in the wing are glazed.', 'Do not open the '
     'unglazed door.', 'You reach for the door and stop. You do not want to open it. You really do not.',
     dict(stress=12), (50, 100, 'Someone knocks on the inside of the cell door, twice.', 'thump', 6)),
    ('310', 'Euclid', 'plinth', (255, 140, 40), 'An eternal flame in a lamp. Put it out and it comes back much '
     'bigger, somewhere nearby.', 'Never to be extinguished.', 'Please do not blow on it.', 'The little flame '
     'leans toward your breath. You step back before it can get ideas.', dict(stress=5, sound='fire'),
     (60, 120, 'The flame in the lamp flares high, then settles.', 'fire', 2)),
    ('342', 'Safe', 'plinth', (200, 40, 40), 'A one-way train ticket. Whoever holds it on a train is taken to '
     'somewhere else, and does not come back.', 'In a sealed envelope. No train travel by staff holding it.',
     'Destination: unreadable.', 'You do not touch the ticket. Far away, a train whistle sounds.',
     dict(stress=4, sound='train_chime'), (90, 160, 'A distant train whistle sounds, from somewhere with no '
     'trains.', 'train_chime', 2)),
    ('378', 'Keter', 'tank', (230, 200, 200), 'A brain worm that lives in its host\'s head and makes them '
     'brilliant for a while, and then very much worse.', 'In a sealed tank. No one is to be in reach.',
     'It is curled up and watching.', 'The worm in the tank lifts what might be its head toward yours.',
     dict(stress=10), (50, 100, 'You get a sudden, perfect idea. Then you cannot remember it, and your head aches.',
     'mist', 5)),
    ('447', 'Safe', 'tank', (60, 200, 60), 'A ball of green slime. Dead bodies covered in it turn into more '
     'slime. Living people are fine, and it is quite pleasant to touch.', 'In a tank; touching it is allowed.',
     'It is squishy and warm.', 'You put a hand on the slime. It is warm and soft and oddly cheering.',
     dict(stress=-8), (60, 120, 'The green slime gurgles happily.', 'hose', 0)),
    ('488', 'Euclid', 'poster', (90, 70, 60), 'A man who draws meteorites toward himself. They fall more often, '
     'and closer, the longer he stays in one place.', 'Moved every few days. This is a photo of the last site.',
     'The last site was a crater.', 'The photograph is of a crater, with a man standing in the middle, '
     'apologising.', dict(stress=6), (80, 150, 'Something hits the roof far above with a long, rolling boom.',
     'thump', 4)),
    ('527', 'Safe', 'figure', (90, 150, 200), 'Mr. Fish: a man with a fish\'s head, who is polite, lonely and '
     'thinks he is one of the Little Ones.', 'A comfortable room. He likes visitors.', 'He asked for a name tag.',
     'Mr. Fish blows a small bubble at you and nods. You nod back.', dict(stress=-5), (60, 120, 'Mr. Fish '
     'hums tunelessly to himself.', 'muffle', 0)),
    ('689', 'Keter', 'figure', (20, 20, 20), 'The Haunter in the Dark: a statue that kills anyone who sees it '
     'once they stop looking - then moves next to the body.', 'Never observed directly. Viewed by camera only.',
     'The camera is the only one looking.', 'You look away from it, and something in the dark moves a little.',
     dict(stress=15, blur=200), (45, 90, 'The dark in the corner of the cell seems a little closer.', '', 6)),
    ('668', 'Euclid', 'table', (190, 190, 200), 'A 13-inch kitchen knife that makes whoever holds it want to stab '
     'whoever is nearest, very badly.', 'In a locked case. Handle only with tongs.', 'Somebody used their hands.',
     'You look at the knife a little too long. Your hand is halfway to the case before you stop it.',
     dict(stress=10), (70, 140, 'For a moment you think about the knife in the case, and why it is locked.', '', 4)),
    ('2662', 'Keter', 'figure', (60, 120, 80), 'A small, cheerful entity with tentacles and wings who says it is '
     'Cthulhu, and wants to be a good friend. It shouts FHTAGN a lot.', 'A comfortable cell and conversation.',
     'Ask it about its day.', 'It waves a tentacle: "FHTAGN! That means hello!"', dict(stress=-5),
     (60, 120, 'From the cell: "FHTAGN!" Then, more quietly: "Hello?"', 'muffle', 0)),
    ('040', 'Euclid', 'bed', (240, 200, 210), 'Evolution\'s Child: a girl who can change living things just by '
     'imagining them different. She is kind, and closely watched.', 'A child\'s room. No drawing materials of '
     'animals.', 'She drew a cat with six legs again.', 'She shows you a drawing of a cat with wings. Somewhere '
     'nearby, something purrs and flaps.', dict(stress=-5), (70, 140, 'Something small with too many legs '
     'scuttles through the cell and is gone.', 'crinkle', 3)),
]
