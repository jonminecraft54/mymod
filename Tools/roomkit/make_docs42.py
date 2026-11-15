"""The notes of the forty-second batch: SCP-127, -439, -1577, -154, -4139 and -466 summarised in our own words
from scp-wiki.wikidot.com (CC BY-SA 3.0), and a block directory for the panopticon."""
from make_docs2 import typed

TITLES = {'docb42_127': 'SCP-127 Summary', 'docb42_439': 'SCP-439 Summary', 'docb42_1577': 'SCP-1577 Summary',
          'docb42_154': 'SCP-154 Summary', 'docb42_4139': 'SCP-4139 Summary', 'docb42_466': 'SCP-466 Summary',
          'docb42_blocks': 'Block Directory'}
DOCS = list(TITLES)
TITLES.update({'flare1577': 'SCP-1577-1 (Flare Gun)', 'bracelets154': 'SCP-154 (Bronze Bracelets)'})
SRC = lambda n: 'Summary of scp-wiki.wikidot.com/%s (CC BY-SA 3.0).' % n


def docs():
    typed('docb42_127', [('Clearance Level', '3'), ('Item #', 'SCP-127'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'It looks like a compact submachine gun. Under the steel and polymer shell, the whole weapon is '
              'organic and alive. It fires teeth - human-like, but from no species on Earth. It groans when you '
              'switch it between single shot and automatic.'),
        ('p', 'A magazine holds about sixty. It takes three to five days to grow more. The magazine cannot be '
              'removed. It needs only water, calcium and protein. Kept in the Toy Box armory.'),
        ('p', SRC('scp-127'))])
    typed('docb42_439', [('Clearance Level', '3'), ('Item #', 'SCP-439'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A greyish, see-through insect like an earwig, 2.5 cm long. Awake, it pinches. Its danger is how it '
              'nests: it waits, hidden, until a human falls asleep, and climbs into their mouth. Only humans.'),
        ('p', 'Do not doze near the terrarium. Do not sit still near it for long. Keep the lid on.'),
        ('p', SRC('scp-439'))])
    typed('docb42_1577', [('Clearance Level', '3'), ('Item #', 'SCP-1577'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'SCP-1577-1 is an old flare gun of the kind the RAF carried from just before the Second World War, '
              'its serial number deliberately worn away. Its flares burn far hotter, brighter and longer than they '
              'should, and it never misfires.'),
        ('p', 'Exactly one hour after it is fired, SCP-1577-2 appears: an old four-engined transport aircraft, '
              'coming in as if to land where the flare was fired.'),
        ('p', 'Test firings are done in the empty test room only. Do not fire it indoors anywhere else.'),
        ('p', SRC('scp-1577'))])
    typed('docb42_154', [('Clearance Level', '2'), ('Item #', 'SCP-154'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'A pair of plain bronze bracelets. Wear both on one arm, hold the pose of drawing a bow and '
              'concentrate, and a large, faint, incorporeal bow forms in your hand while the bracelets glow. It can '
              'be drawn and loosed like a real bow until the pose or the concentration breaks.'),
        ('p', 'Stored in the Vault; not under active research.'),
        ('p', SRC('scp-154'))])
    typed('docb42_4139', [('Clearance Level', '3'), ('Item #', 'SCP-4139'), ('Object Class', 'Euclid')], [
        ('h', 'Description'),
        ('p', 'A white single-door fridge with a combination lock and no electrics. Six crude drawings on magnets '
              '(SCP-4139-1 to -6) - a picnic, a space trip, and others - act as its control panel: how they are '
              'arranged on the door changes what it does. With all six attached it is just a fridge at 1.6 C.'),
        ('p', 'Do not rearrange the drawings. Whoever did it last is why the Vault smells of the sea.'),
        ('p', SRC('scp-4139'))])
    typed('docb42_466', [('Clearance Level', '4'), ('Item #', 'SCP-466'), ('Object Class', 'Keter')], [
        ('h', 'Description'),
        ('p', 'Possibly a pathogen and its human host, or just the host. The host (SCP-466-2) grows ever more blood '
              'vessels, broad and visible under the skin, slowly eroding muscle and organs. They shift, painfully.'),
        ('p', 'Threaten it and the vessels tear out through the skin and reach several metres to constrict whatever '
              'threatened it. E-Block is reached only through the long tunnel, which is wired to be collapsed.'),
        ('p', SRC('scp-466'))])
    typed('docb42_blocks', [('Area', 'Heavy Containment'), ('Document', 'Block directory')], [
        ('h', 'Where things are'),
        ('p', 'B: Mass humanoid containment (the Panopticon) - cells round an observation tower. C: The Toy Box - '
              'non-humanoid chambers, each with its own small lab; test rooms; the armory. D: The Vault - stored '
              'items not under research, sensitive archives, backup servers. E: The Cellar - hostile anomalies, at '
              'the end of the tunnel. Do not go to E.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
