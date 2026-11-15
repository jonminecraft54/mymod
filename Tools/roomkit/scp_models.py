r"""Real models for the SCPs of the containment blocks (batches 20, 21, 24, 25), instead of coloured boxes.

MESHES: num -> (file, size of its longest side in room units, y of its base above the floor, x offset towards the cell's far wall)
        A mesh from the game's own GFX\items or GFX\map\props, scaled at load so it is that tall.
NPCS:   num -> skin texture: the SCP is a figure (the Class-D model with that skin) standing in its cell, made
        the first time you enter the room so it costs nothing elsewhere.
The rooms (rooms_b24.py, rooms_b25.py) leave out the coloured stand-in of every SCP listed here; gen_models.py
writes the Blitz table IndevScpModels.bb from this file."""

MESHES = {
    # batch 20 / 21 (cells built by rooms_b20 / rooms_b21; their own props stay, the model sits on them)
    '458': (r'GFX\items\scp458.b3d', 50, 82, 0),
    '113': (r'GFX\items\scp113.b3d', 16, 100, 0),
    '662': (r'GFX\items\513.x', 30, 90, 0),
    '1981': (r'GFX\map\props\tv993.b3d', 60, 80, 120),
    '241': (r'GFX\map\props\scpcb_book.x', 30, 50, 60),
    '261': (r'GFX\map\props\scpcb_vending.x', 220, 0, 140),
    # batch 24
    '101': (r'GFX\items\wallet.b3d', 34, 90, 0),
    '262': (r'GFX\items\hazmat.b3d', 60, 0, 0),
    '300': (r'GFX\items\indevwater.b3d', 36, 90, 0),
    '426': (r'GFX\items\electronics.x', 40, 90, 0),
    '432': (r'GFX\map\props\cabinet_a.x', 200, 0, 120),
    '504': (r'GFX\map\props\crate1.x', 90, 0, 60),
    '1230': (r'GFX\map\props\scpcb_book.x', 30, 90, 0),
    '409': (r'GFX\map\props\Tank1.x', 170, 0, 40),
    '018': (r'GFX\map\props\crate3.x', 90, 0, 60),
    # batch 25
    '124': (r'GFX\map\props\crate2.x', 90, 0, 60),
    '250': (r'GFX\items\HGIB_Skull1.b3d', 70, 0, 0),
    '263': (r'GFX\map\props\tv993.b3d', 60, 0, 120),
    '310': (r'GFX\map\props\lamp1.x', 60, 90, 0),
    '342': (r'GFX\items\paper.x', 26, 90, 0),
    '378': (r'GFX\map\props\Tank2.x', 170, 0, 40),
    '447': (r'GFX\map\props\Tank1.x', 170, 0, 40),
    # batch 27: SCP-2107's vending machine (not an SCP itself)
    'v2107': (r'GFX\map\props\scpcb_vending.x', 220, 0, 0),
    # batch 28: SCP-983, the birthday monkey, on its pedestal (make_scp983.py)
    'm983': (r'GFX\map\props\scp983.b3d', 95, 108, 0),
}

NPCS = {
    '027': r'GFX\npcs\classd2.jpg',
    '181': r'GFX\npcs\indev_tech.jpg',
    '134': r'GFX\npcs\classd3.jpg',
    '191': r'GFX\npcs\indev_attendant.jpg',
    '847': r'GFX\map\wood.jpg',
    '239': r'GFX\npcs\classd1.jpg',
    '527': r'GFX\map\indev_b25_527.png',
    '689': r'GFX\map\indev_b25_689.png',
    '2662': r'GFX\map\indev_b25_2662.png',
    '040': r'GFX\npcs\classd3.jpg',
}

# the kinds whose coloured stand-in is replaced (a bed or a plinth stays: the model sits on it)
REPLACED = set(MESHES) | set(NPCS)
