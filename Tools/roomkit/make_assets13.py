"""Textures of the thirteenth batch: the red pool of SCP-354 (GFX\\map\\indev_redpool.png, RGBA, a fluid sheet).
   python make_assets13.py            writes the texture (the notes are make_docs13.py)"""
import numpy as np
from PIL import Image
from make_assets5 import save_map

N = 128


def redpool():
    rng = np.random.default_rng(354)
    # two octaves of noise give slow darker and brighter patches, the way a viscous surface reads
    base = rng.random((N // 8, N // 8))
    up = np.kron(base, np.ones((8, 8)))
    fine = rng.random((N, N))
    k = 0.6 * up + 0.4 * fine
    r = (120 + 90 * k).astype(np.uint8)
    g = (6 + 14 * k).astype(np.uint8)
    b = (8 + 12 * k).astype(np.uint8)
    a = (150 + 60 * k).astype(np.uint8)
    im = Image.fromarray(np.dstack([r, g, b, a]), 'RGBA')
    save_map(im, 'indev_redpool.png')


if __name__ == '__main__':
    redpool()
    print('indev_redpool.png written')
