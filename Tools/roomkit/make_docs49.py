"""The note of the forty-ninth batch: SCP-087-B (original writing)."""
from make_docs2 import typed

TITLES = {'docb49_087b': 'SCP-087-B Stairwell Notice'}
DOCS = list(TITLES)


def docs():
    typed('docb49_087b', [('Item #', 'SCP-087-B'), ('Area', 'Light Containment'), ('Document', 'Notice')], [
        ('h', 'The stairwell'),
        ('p', 'The doorway in this room opens onto narrow brick hallways and stairs that only go down. The layout is '
              'different every time and nobody has found the bottom. There are no lights below; bring your own.'),
        ('p', 'Personnel who went down report numbered plates on the walls, the sound of someone walking a floor '
              'behind them, and a figure that stands at the end of the hallways and is gone when you get there.'),
        ('p', 'The deeper you go, the less it bothers to leave. Past a point it stops waiting for you to look away.'),
        ('p', 'Survivors came back through a door that should not have been there. It was never on the same floor twice.')])


if __name__ == '__main__':
    docs()
    print(DOCS)
