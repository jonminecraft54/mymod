"""SCP-112-PT's note: a short summary in our own words of scp-pt-br.wikidot.com/scp-112-pt (CC BY-SA 3.0)."""
from make_docs2 import typed

TITLES = {'doc22_112': 'SCP-112-PT Summary'}


def docs():
    typed('doc22_112', [('Clearance Level', '2'), ('Item #', 'SCP-112-PT'), ('Object Class', 'Safe')], [
        ('h', 'Description'),
        ('p', 'SCP-112-PT is a human skeleton in the decayed robes of a 4th-century bishop, believed to be the remains '
              'of Saint Nicholas. It does not decay.'),
        ('p', 'Now and then the remains manifest SCP-112-PT-1, the spirit of an old man with a long white beard. It is '
              'intelligent and polite, stays near the remains, offers gifts and help, and fades within two hours. Its '
              'gifts are not always what was expected.'),
        ('h', 'Containment'),
        ('p', 'The reliquary is kept in a decorated chamber, which appears to keep SCP-112-PT-1 calm. Gifts are to be '
              'logged before use.'),
        ('p', '{He asked whether you had been good this year. Answer honestly.}'),
        ('p', 'Summary of scp-pt-br.wikidot.com/scp-112-pt (CC BY-SA 3.0).')])


if __name__ == '__main__':
    docs()
    print('1 note written')
