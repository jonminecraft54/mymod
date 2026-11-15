"""The notes of the thirty-ninth batch: SCP-1013, -586, -1176, -1370 and -1562 summarised in our own words from
scp-wiki.wikidot.com (CC BY-SA 3.0)."""
from make_docs2 import typed

TITLES = {'docb39_1013': 'SCP-1013 Summary', 'docb39_586': 'SCP-586 Summary', 'docb39_1176': 'SCP-1176 Summary',
          'docb39_1370': 'SCP-1370 Summary', 'docb39_1562': 'SCP-1562 Summary'}
DOCS = list(TITLES)
TITLES['honey1176'] = 'SCP-1176-1 (A Jar of Honey)'
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('docb39_1013', [('Clearance Level', '4'), ('Item #', 'SCP-1013'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'A small reptile, 60 cm long with a tail twice that, and the head of a rooster: a serrated beak, a '
              'wattle, a bony frill it can flare. It hunts by eye contact alone.'),
        ('p', 'Meet its eyes and a stabbing pain runs through every major muscle; within three seconds you are '
              'paralysed, for about eight minutes. It then bites, and the bitten flesh begins to calcify. It feeds '
              'on the calcified remains.'),
        ('p', 'Visual-hazard procedures apply. Do not look at it - not through the window, not on camera.'),
        ('p', SRC('scp-1013'))])
    typed('docb39_586', [('Clearance Level', '2'), ('Item #', 'SCP-586'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A lump of smelted, pale green metal. Anything written about it comes out with at least one word '
              'replaced by a wrong one - this summary included, if you are standing near it.'),
        ('p', 'Asked to describe it in a sentence, people produce things like "it looks like a piece of garden '
              'horse". Copying a sentence that is not about it works fine.'),
        ('p', SRC('scp-586'))])
    typed('docb39_1176', [('Clearance Level', '3'), ('Item #', 'SCP-1176'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'The mummified body of a man who died about a thousand years ago, kept in its sarcophagus, fully '
              'submerged in a golden fluid (SCP-1176-1) chemically identical to clover honey. Its brain shows the '
              'electrical activity of deep sleep.'),
        ('p', 'It sweats SCP-1176-1 constantly, faster when not submerged. The excess is drained daily from the '
              'faucet on the sarcophagus. SCP-1176-1 is not food. It is not to be eaten by anyone who is not '
              'compatible with it, and requests to issue it as an emergency ration are denied.'),
        ('p', SRC('scp-1176'))])
    typed('docb39_1370', [('Clearance Level', '2'), ('Item #', 'SCP-1370'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A self-aware robot about a metre tall, built from tools and electrical parts, with no power source. '
              'Its head is a voltmeter soldered on upside down, which looks like a friendly smile.'),
        ('p', 'It is hostile to anything it thinks is sapient - people, animals, cameras - and announces itself '
              'loudly before it attacks. It balances badly. Cover its head and it calms down.'),
        ('p', 'It lives in a glass case. Put it back when you are done with it.'),
        ('p', SRC('scp-1370'))])
    typed('docb39_1562', [('Clearance Level', '3'), ('Item #', 'SCP-1562'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A metal playground slide, 2.2 m high and 3.4 m long, from an abandoned playground where children '
              'went missing.'),
        ('p', 'Slide down it head-first on your stomach, arms at your sides, and you vanish about 15 cm before the '
              'end. Any other way down is just a slide. Lifelines are cut. The vanished can be talked to by radio: '
              'they describe a small, cramped tunnel. None has been brought back.'),
        ('p', 'TESTING SUSPENDED. Do not crouch at the top.'),
        ('p', SRC('scp-1562'))])


if __name__ == '__main__':
    docs()
    print(DOCS)
