"""The SCP-5094 monitor screen of the fifteenth batch (GFX\\map\\indev_5094on.png): a bright children's title card
for Miss J's schoolhouse, drawn here. The lesson text itself is in IndevU13.bb.
   python make_assets16.py"""
from PIL import Image, ImageDraw, ImageFont
from make_assets5 import save_map

FONT = r"C:\Windows\Fonts\arialbd.ttf"


def screen():
    W, H = 256, 160
    im = Image.new('RGB', (W, H), (70, 190, 210))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, 26], fill=(240, 200, 40))
    d.text((W // 2, 13), "Miss J's Whiz Kidz", font=ImageFont.truetype(FONT, 16), fill=(60, 30, 20), anchor='mm')
    # the teacher: a stylised cut-out, a bow in her hair, a board behind her
    d.rectangle([160, 40, 240, 120], fill=(250, 250, 240), outline=(60, 30, 20), width=2)
    for k, y in enumerate((58, 74, 90)):
        d.line([(170, y), (230, y)], fill=(120, 120, 150), width=2)
    d.polygon([(60, 150), (70, 80), (110, 80), (120, 150)], fill=(230, 80, 150))     # dress
    d.ellipse([72, 44, 108, 84], fill=(240, 200, 170))                             # face
    d.polygon([(82, 46), (98, 46), (104, 36), (76, 36)], fill=(210, 40, 60))         # bow
    d.ellipse([82, 58, 86, 62], fill=(40, 30, 30))
    d.ellipse([94, 58, 98, 62], fill=(40, 30, 30))
    d.arc([84, 66, 96, 76], 0, 180, fill=(180, 60, 60), width=2)
    d.text((8, H - 14), "LESSON 1: LETTERS", font=ImageFont.truetype(FONT, 12), fill=(20, 20, 40), anchor='lm')
    save_map(im, 'indev_5094on.png')


if __name__ == '__main__':
    screen()
    print('indev_5094on.png written')
