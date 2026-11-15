"""The sixteen notes of the twenty-first batch: short summaries in our own words of SCP Wiki articles
(scp-wiki.wikidot.com, CC BY-SA 3.0); each note names its source."""
from make_docs20 import note

DATA = [
    ('038', 'Safe', 'A tree that grows a perfect copy of anything pressed against its bark, as fruit, in a few hours.',
     'Fenced. Nothing living is to be pressed against it.', 'Somebody tried a keycard. It worked.'),
    ('063', 'Safe', 'An ordinary-looking toothbrush that destroys any organic matter its bristles touch - '
     '"the world\'s best toothbrush".', 'Kept in a locked case. Handle only by the handle.', 'Do not brush your teeth with it.'),
    ('1171', 'Euclid', 'A window in an abandoned house. Whatever is on the other side writes in the frost on the glass. '
     'It asks people to leave, and it is afraid of us.', 'The house is watched. Talking through the glass is allowed '
     'with permission.', 'It wrote HUMANS GO AWAY. It also wrote PLEASE.'),
    ('507', 'Safe', 'A man who drops into other dimensions at random and comes back some time later, '
     'usually annoyed.', 'A standard room. He is not to be blamed for the absences.', 'If he vanishes mid-sentence, wait.'),
    ('2521', 'Keter', 'A creature that takes away anything about itself that is written in words. The file is written '
     'in pictures for that reason.', 'Nothing may be written about it. Nothing.', '| ●● | ●●●●● | ●● | ● |'),
    ('343', 'Safe', 'An old man who says he is God, and can be seen differently by everyone. He is polite, and '
     'leaves the cell when he likes.', 'Visits by appointment. He keeps the appointments.', 'He asked after your mother.'),
    ('1437', 'Euclid', 'A hole in the ground that opens on to another world, from which things now and then fall up.',
     'A fence and a camera. Nothing is to be thrown in.', 'Something threw a stone back.'),
    ('1609', 'Keter', 'The remains of a chair. Whole, it was gentle and moved itself to tired people. Broken, it comes '
     'back into the body of anyone who threatens it.', 'Kept in pieces. Not to be approached with a weapon.',
     'It used to be a chair. Please sit somewhere else.'),
    ('2006', 'Keter', 'A being that wants to be frightening and takes whatever shape it thinks scares you most. Its '
     'idea of what is scary comes from films.', 'It is shown old monster films, which keeps it busy and harmless.',
     'If it asks whether it is scary, say yes.'),
    ('120', 'Safe', 'An inflatable paddling pool. Anyone who steps into it is sent somewhere else at random.',
     'Deflated when not in use. It is inflated for this wing.', 'Shoes off. You may need them where you land.'),
    ('151', 'Euclid', 'A painting of a breaking wave. People who look at it for some time feel their lungs fill '
     'with seawater, and can drown in a dry room.', 'Covered. Viewing for testing only.', 'Do not look at it for long.'),
    ('050', 'Euclid', 'A golden trophy engraved "to the cleverest". It changes hands by tricks: whoever outwits its '
     'holder becomes its owner, whether they want it or not.', 'Kept by whoever was last clever enough.', 'Nobody wants it.'),
    ('216', 'Safe', 'A safe with a combination lock that opens on to a different set of contents for each combination.',
     'Combinations are logged. Unknown combinations are not to be tried alone.', 'Some combinations open on things '
     'that open back.'),
    ('662', 'Safe', 'A small hand bell. Ringing it brings Mr. Deeds, a polite butler who will do almost anything '
     'asked of him within reason.', 'In a box. Requests to Mr. Deeds are logged.', 'Say please. He notices.'),
    ('093', 'Euclid', 'A red disc that, carried in front of a mirror, lets the bearer step into a grey, empty world '
     'that looks like ours after something terrible.', 'Mirrors are kept out of the cell.', 'Nobody has come back '
     'and been the same.'),
    ('1981', 'Euclid', 'A videotape of a speech by a former US president. Each time it is played the speech is '
     'different, and the speaker is hurt in ways he does not seem to notice.', 'Played only for testing.',
     'It is never the same tape twice.'),
]
TITLES = {'doc21_' + n: 'SCP-%s Summary' % n for n, *_ in DATA}


def docs():
    for n, cls, desc, cont, rem in DATA:
        note('doc21_' + n, n, cls, desc, cont, rem)


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(TITLES))
