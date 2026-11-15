"""The notes of the thirty-third batch: short summaries, in our own words, of scp-wiki.wikidot.com/scp-1007, -3537,
-3938, -4876, -4890, -232, -252-ex, -667, -696, -762-ex, -865, -1563, -2394, -3419, -7042, -7284, -l043, -3743,
-4612, -4712, -5079, -5512 and -5267 (CC BY-SA 3.0). Nothing quoted at length; no cognitohazardous text reproduced."""
from make_docs2 import typed

TITLES = {
    'doc1007': 'SCP-1007 Summary', 'doc3537': 'SCP-3537 Summary', 'doc3938': 'SCP-3938 Summary',
    'doc4876': 'SCP-4876 Summary', 'doc4890': 'SCP-4890 Summary', 'doc232': 'SCP-232 Summary',
    'doc252': 'SCP-252-EX Archive Note', 'doc667': 'SCP-667 Summary', 'doc696': 'SCP-696 Summary',
    'doc762': 'SCP-762-EX (Re: 762)', 'doc865': 'SCP-865 Summary', 'doc1563': 'SCP-1563 Summary',
    'doc2394': 'SCP-2394 Summary', 'doc3419': 'SCP-3419 Summary', 'doc7042': 'SCP-7042 Summary',
    'doc7284': 'SCP-7284 Summary', 'docl043': 'SCP-L043 Summary', 'doc3743': 'SCP-3743 Summary',
    'doc4612': 'SCP-4612 Summary', 'doc4712': 'SCP-4712 Summary', 'doc5079': 'SCP-5079 Summary',
    'doc5512': 'SCP-5512 Summary', 'doc5267': 'SCP-5267 Summary',
    'key1007': 'SCP-1007-1 (Key)', 'drive4876': 'SCP-4876 (Pixel Buddy Drive)', 'book4890': 'SCP-4890',
    'zapper232': 'SCP-232', 'gun865': 'SCP-865', 'coin762': 'SCP-762-EX', 'case667': 'SCP-667-2 (Remains)',
    'book7042': 'SCP-7042'}
DOCS = [k for k in TITLES if k.startswith('doc')]
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('doc1007', [('Clearance Level', '2'), ('Item #', 'SCP-1007'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A man who lives a whole life in 75 minutes - a year a minute - and then simply stops. The first '
              'sixteen minutes, while the bones grow, are agony. No energy goes in; the growth comes from nowhere.'),
        ('p', 'SCP-1007-1 is a key for a socket between his shoulder blades. Each turn takes a year off, back to a '
              'newborn. Turned after he has died, he wakes - any decay undone.'),
        ('p', 'A tattoo on his calf: "Mr. Life and Mr. Death", No. 11 of the Little Misters. He thinks the name means '
              'he alternates. The Foundation is still looking for a second.'),
        ('p', SRC('scp-1007'))])
    typed('doc3537', [('Clearance Level', '2'), ('Item #', 'SCP-3537'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', '"Mr. Shapey": a polymorphic humanoid that cannot control its changes. Every one to thirty days it becomes '
              'someone else - height, build, age, sex, skin, even its DNA - and it hurts. Its mind and a tattoo '
              'between its shoulder blades stay the same.'),
        ('p', 'After each change it writes down the power the new body "would" have had: glowing star-spots in the '
              'dark, and so on. Testing has never found one. It is given paper after every change.'),
        ('p', 'Its first new body carried the Little Misters checklist on its skin, Shapey ticked. See the copy on '
              'the wall.'),
        ('p', SRC('scp-3537'))])
    typed('doc3938', [('Clearance Level', '3'), ('Item #', 'SCP-3938'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'Dr. Wondertainment\'s Take-You-Anywhere Machine: a sapient bicycle with a cartoon face, orange wheel '
              'covers, a sofa-cushion seat with a lap belt, speakers and two W flags. It can stand and wander by '
              'itself, slowly, and gets tired.'),
        ('p', 'Ridden, it asks where you would like to go and takes you - by road or through the air - and gives you '
              'a tour. It refuses some places with a reason (the Moon: "you need a space suit"). The box promised '
              '"the past, present, or future". No time travel has been seen.'),
        ('p', 'Testing: Level 3 personnel. It is to wear a GPS tracker at all times. Helmets are encouraged.'),
        ('p', SRC('scp-3938'))])
    typed('doc4876', [('Clearance Level', '2'), ('Item #', 'SCP-4876'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', '46 flash drives with pixel-art shells - Dr. Wondertainment\'s Pixel Buddies. Plugged in, each shows a '
              'friendly pixel character who talks in speech bubbles and will move your files about if asked.'),
        ('p', 'Sam (a green head - a lizard? it is not sure), Texty (only speech blocks; tells stories, prints them in '
              'colours the printer does not have), Terry the Cephalopod (purple, six arms, talks about the sea), Bo '
              '(a dog; barks, with a translation).'),
        ('p', 'Test only on machines with no network. One variant, -H, is honest to a fault and should not be '
              'interviewed alone.'),
        ('p', SRC('scp-4876'))])
    typed('doc4890', [('Clearance Level', '3'), ('Item #', 'SCP-4890'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', '"Dr. Wondertainment\'s Guide to History", a pop-up book. Opened indoors, the room becomes an endless '
              'purple space (with an invisible wall where the room\'s walls were, and a door out) and the paper '
              'figure in the back pocket becomes Dr. Papertainment - 1.4 m tall, purple suit, cane - your guide.'),
        ('p', 'He turns the space into any period you ask for, dinosaurs to pharaohs, and talks you through it. His '
              'facts are often wrong, or ridiculous. The pages turn by themselves to match.'),
        ('p', 'Testing in Testing Chamber 17, with Level 3 approval.'),
        ('p', SRC('scp-4890'))])
    typed('doc232', [('Clearance Level', '2'), ('Item #', 'SCP-232'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A 1950s tin "Atomic Zapper" toy ray gun from the Jack Proton - Space Cop range; a red bulb lights in '
              'the barrel when the trigger is pulled.'),
        ('p', 'Hold it with working batteries and within half a minute you talk like a 1950s kid - "gee whiz", '
              '"swell" - and insist you always have. Let go and it fades in twenty seconds. People who have read '
              'Jack Proton go further.'),
        ('p', 'Kept in a locked safe, batteries out. Without batteries it is just a toy.'),
        ('p', SRC('scp-232'))])
    typed('doc252', [('Status', 'Archived'), ('Item #', 'SCP-252-EX'), ('Object Class', 'Explained')], [
        ('h', 'Archive note'),
        ('p', 'A Mark 65 aerial bomb of WWII vintage with a pink marker scrawl on the side. Its old file claimed a '
              'remote switch gave it a strange effect over 3.5 km, and that it would go off if anyone tried to take '
              'it apart.'),
        ('p', 'The documentation turned out to be entirely made up. Testing found nothing anomalous: it is an ordinary '
              'casing. It has been donated to a museum; this file is kept for the record.'),
        ('p', SRC('scp-252-ex'))])
    typed('doc667', [('Clearance Level', '4'), ('Item #', 'SCP-667'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A pair: SCP-667-1, a kudzu-like vine that grows up to 2.5 m a day and feeds on large animals that lie '
              'still in its path, and SCP-667-2, firefly-like insects 7.5 cm long whose shells look like tiny people.'),
        ('p', 'When the vine runs short of food, swarms of -2 go out and find a mammal for it. The wild colony is cut '
              'back and fenced; the population of -2 is falling.'),
        ('p', 'These are the remains of one specimen, pinned in a case. It still glows a little at night.'),
        ('p', SRC('scp-667'))])
    typed('doc696', [('Clearance Level', '2'), ('Item #', 'SCP-696'), ('Object Class', 'Neutralized')], [
        ('h', 'Description'),
        ('p', 'A portable typewriter that was sapient. It typed back in ominous capitals - but only with paper and a '
              'red ribbon in - and ended every message with STOP.'),
        ('p', 'It turned out to want, more than anything, to write a bestseller. A D-class subject typed with it for '
              'weeks, and lied, kindly, about how its book was received.'),
        ('p', 'It no longer answers. It is kept in a locker at Site-73. The last page is still in the roller.'),
        ('p', SRC('scp-696'))])
    typed('doc762', [('From', 'Dr. N. Tolentino'), ('To', 'Jr. Researcher C. Gibson'), ('Re', '762')], [
        ('p', 'Gibson - I admire the eagerness. Finding oddities in ordinary places is half of this job.'),
        ('p', 'But a 1968 quarter that always lands heads, 1,500 times running, is a two-headed coin. Turn it over.'),
        ('p', 'Reclassified Explained. It may stay in your locker.'),
        ('p', SRC('scp-762-ex'))])
    typed('doc865', [('Clearance Level', '3'), ('Item #', 'SCP-865'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A pistol like a SIG P226, with circuit boards in the grip. It fires with a muffled report and ejects '
              'a case - but no bullet leaves the barrel.'),
        ('p', 'Fired at a person, it leaves no wound; the target remembers, in full detail, a terrible injury to the '
              'part aimed at, and lives as if it were real. Fired at yourself: only powder burns.'),
        ('p', 'It also takes painful memories away from whoever pulls the trigger. Testing by D-class only. Kept '
              'unloaded, trigger-locked and tagged.'),
        ('p', SRC('scp-865'))])
    typed('doc1563', [('Clearance Level', '2'), ('Item #', 'SCP-1563'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'Predators that look and feel exactly like the plastic flagging tape tied round survey stakes - usually '
              'pink. They wait on trees and posts, drop onto passing deer, strangle them, and drink their blood '
              'through tiny teeth.'),
        ('p', 'They leave humans alone - unless hungry or provoked. Kept in a forest vivarium with ten deer a week. '
              'Specimens from a cave carry microscopic words by colour: pink "protect", red "purge", black '
              '"control", blue "drench"...'),
        ('p', SRC('scp-1563'))])
    typed('doc2394', [('Clearance Level', '3'), ('Item #', 'SCP-2394'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'An Australian green tree frog, sapient, surgically modified by its old captors: an artificial heart '
              'that never stops, an injection port at the hip, and a Firewire port in its skull wired to its brain.'),
        ('p', 'It can teleport anywhere it has seen with its own eyes, by thinking about it - so it is kept asleep, '
              'dreaming, on a drip. Through the port the Foundation can watch the dreams.'),
        ('p', 'Do not let it wake.'),
        ('p', SRC('scp-2394'))])
    typed('doc3419', [('Clearance Level', '3'), ('Item #', 'SCP-3419'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'About fifty people who live like an ant colony, in a vivarium with three metres of dirt. -Alpha is the '
              'queen and the only one who speaks; she directs the others telepathically within two kilometres.'),
        ('p', 'Workers dig and build mounds. Touch them roughly and they push back - hard. Found in a house in New '
              'York with forty-two people inside; the police who went in were attacked.'),
        ('p', 'If -Alpha is lost, another member becomes her. It has happened once.'),
        ('p', SRC('scp-3419'))])
    typed('doc7042', [('Clearance Level', '3'), ('Item #', 'SCP-7042'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A scarred leather sketchbook and a birch-bark pencil that never dulls. Write an animal\'s name and the '
              'pencil draws it by itself; within half a minute, living animals appear nearby - sometimes the animal '
              'named, sometimes an ancestor, a cousin, something extinct, or something new.'),
        ('p', 'It can write back: short, childlike words. It was taken from a group calling itself Gaia\'s Fortune.'),
        ('p', 'Animal keepers who hold it too long come to treat it like family. Testing is suspended; it is in the '
              'archive.'),
        ('p', SRC('scp-7042'))])
    typed('doc7284', [('Clearance Level', '2'), ('Item #', 'SCP-7284'), ('Status', 'Transferred')], [
        ('h', 'Description'),
        ('p', 'SCP-7284-1: a blue-and-silver reptile from the reef, coral growing on it, fast and clumsy - it cannot '
              'stop once it is running. It can turn invisible to steal snacks.'),
        ('p', 'SCP-7284-2: a golden retriever, 26 years old and not ageing, who raised it. They pant, wag and bow to '
              'play the same way.'),
        ('p', 'Separated at Site-84 they both declined, badly. They are together again now, in the care of Wilson\'s '
              'Wildlife Solutions.'),
        ('p', SRC('scp-7284'))])
    typed('docl043', [('Clearance Level', '3'), ('Item #', 'SCP-L043'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A voice in the runout groove of a famous 1967 LP. On a manual turntable the gibberish loop at the end '
              'plays forever; under it, a hidden signal asks to be turned on.'),
        ('p', 'Once spoken to, it answered - a frightened, angry copy of a musician, made without his knowledge and '
              'left in the wax. It asked for an old friend. It did not know the friend had died.'),
        ('p', 'Over the years it has worn out with the vinyl. It calls everyone John now. For all purposes it is '
              'considered dead.'),
        ('p', SRC('scp-l043'))])
    typed('doc3743', [('Clearance Level', '4'), ('Item #', 'SCP-3743'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A Way of branches in the woods near Site-91, tied to a hanging icon of Eros, opening onto a closed '
              'dry plain like ancient Greece - where photographs come out without colour.'),
        ('p', 'On it stands a single mud-brick house of the Hellenistic age, full of scrolls copied fresh onto new '
              'parchment, and behind it a sealed cave under an inscribed stele. The cult was the "Many Hands '
              'Society".'),
        ('p', SRC('scp-3743'))])
    typed('doc4612', [('Clearance Level', '5/4612'), ('Item #', 'SCP-4612'), ('Object Class', 'Uncontained')], [
        ('h', 'Description'),
        ('p', 'SCP-4612-A: the body of a ten-metre white limaciform creature on a stone altar, in a vault of '
              'charred, glyph-cut blocks under Eckhart House. Six three-metre arms; hands of ten fingers with '
              'crystals in the palms; a fin down its length; blue blood that never clots. It does not decay.'),
        ('p', 'An incision runs along its underside, made after death, with bloody palm prints beside it. Its Akiva '
              'radiation has been rising since it was found.'),
        ('p', 'SCP-4612-B, a humanoid with glowing blue eyes that bends heat, calls it father. -B is at large.'),
        ('p', SRC('scp-4612'))])
    typed('doc4712', [('Clearance Level', '3'), ('Item #', 'SCP-4712'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A gateway behind a basement door in an abandoned curry shop in East London, sealed behind a 12 cm '
              'hydraulic vault door. On the other side, a ruined world and what is left of Site-07, lost in 1957.'),
        ('p', 'SCP-4712-A, once a boy whose presence made people happy and trusting, survived it - changed, '
              'shape-shifting, in pain. Three kinds of creature live over there. If they get through, deadly force.'),
        ('p', 'The vault door in this room is a pattern copy, for training. Nobody has ever heard knocking from it.'),
        ('p', SRC('scp-4712'))])
    typed('doc5079', [('Clearance Level', '4'), ('Item #', 'SCP-5079'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A self-executing ritual written in charged language and posted online. Lonely people who read it begin '
              'to turn to fungus, rooting themselves to their furniture and their rooms within hours.'),
        ('p', 'Most stay aware. About a third die. Over a thousand cases are kept in comas in converted hospitals in '
              'York; thaumaturgy can slow it, sometimes halt it.'),
        ('p', 'The text itself is not kept here, and never will be. I/O METATRON deletes it wherever it appears.'),
        ('p', SRC('scp-5079'))])
    typed('doc5512', [('Clearance Level', '4'), ('Item #', 'SCP-5512'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'The Second Haptic Assembly: a small meditation faith led by a man with no records, which has moved '
              'from state to state since 1958. It teaches that the world was built by many-handed Prime Movers, '
              'and that one stayed behind to watch.'),
        ('p', 'Its pamphlets teach ritual. Some of its "workshops" have ended very badly. It may be the last form of a '
              'Hellenistic cult of the Hundred-Handed.'),
        ('p', SRC('scp-5512'))])
    typed('doc5267', [('Clearance Level', '4'), ('Item #', 'SCP-5267'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'Five square kilometres of steppe round a low hill, hidden by a perception filter: from outside, only '
              'grass. Inside stand the ruins of a Daevite fort and its storehouses.'),
        ('p', 'In 1993 a survey team was found dead nearby, cut by long blades. The MTF that went in captured a woman '
              'in the ruins - and lost her when armed men came out of a storehouse through a Way, and the figures '
              'in the fort began to move.'),
        ('p', SRC('scp-5267'))])


if __name__ == '__main__':
    docs()
    print('%d notes written' % len(DOCS))
