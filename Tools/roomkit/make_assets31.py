r"""Textures of the thirty-first batch (original, drawn here): name plates, the SCP-467 signs (no communication
devices, today's guard), the SCP-198 digital scale and Containment Protocol 198 card, the SCP-207 locker label and the
"clear drinks only" vending notice, the SCP-178 Class 3 container label and the Incident 178-14-Alpha warning, the
SCP-1650 seizure tag, the SCP-1079 watchlist notice.
   python make_assets31.py"""
import os
from PIL import Image, ImageDraw
from make_assets5 import MAPDIR
from make_assets30 import F, FR, FM, plate, emblem

PLATES31 = [('SCP-467', 'CONFESSIONAL BOOTH'), ('DR. RIGHTS', 'SENIOR RESEARCHER'), ('RESEARCH', 'OPEN OFFICE'),
            ('STAFF BREAK', 'SECRETARIAL / SECURITY'), ('SCP-198', 'SECURE ROOM'), ('SCP-207', 'BIO-CONTAINMENT'),
            ('SCP-178', 'CLASS 3 CONTAINER'), ('SCP-1079 / 1650', 'LOCKER / ARTIFACT UNIT'),
            ('DR. ICEBERG', 'RESEARCHER'), ('ITEM WING', 'ANOMALOUS OBJECTS')]


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def sign(w, h, bg, rows, border=(255, 255, 255)):
    im = Image.new('RGB', (w, h), bg)
    d = ImageDraw.Draw(im)
    d.rectangle([5, 5, w - 6, h - 6], outline=border, width=5)
    y = 0
    tot = sum(s for _, s, _ in rows) * 1.3
    y = (h - tot) / 2
    for t, s, c in rows:
        d.text((w / 2, y + s * 0.65), t, font=F(s), fill=c, anchor='mm')
        y += s * 1.3
    return im


if __name__ == '__main__':
    sheet = Image.new('RGB', (1024, 640))
    for i, (a, b) in enumerate(PLATES31):
        sheet.paste(plate(a, b), ((i % 2) * 512, (i // 2) * 128))
    save(sheet, 'indev_plates31.png')
    save(sign(512, 256, (170, 20, 20), [('NO COMMUNICATION DEVICES', 34, (255, 255, 255)),
                                        ('BEYOND THIS POINT', 34, (255, 255, 255)),
                                        ('phones / pagers / radios: leave at the guard post', 20, (255, 220, 220))]), 'indev_467nodev.png')
    save(sign(384, 256, (30, 40, 36), [("TODAY'S GUARD", 30, (230, 240, 230)), ('(changed daily)', 18, (180, 200, 180)),
                                       ('USE FOR PERSONAL', 22, (240, 200, 120)), ('REASONS DISCOURAGED', 22, (240, 200, 120))],
               border=(140, 170, 140)), 'indev_467roster.png')
    log = Image.new('RGB', (512, 384), (240, 238, 228))
    d = ImageDraw.Draw(log)
    d.text((256, 26), 'TEST LOG 467 - SUMMARY', font=F(26), fill=(20, 20, 20), anchor='mm')
    rows = ['caller: mother - disappointed, blames herself', 'caller: victim\'s family - learning to forgive',
            'caller: researcher next door - "your haircut"', 'caller: own voice - forgotten events',
            'caller: victim - screaming, five minutes', 'HOLIDAYS: more distressing calls,', 'calls from self, the dead, the non-existent']
    for k, r in enumerate(rows):
        d.text((24, 70 + k * 42), r, font=F(19, FM), fill=(150, 30, 30) if k >= 5 else (30, 30, 30))
    save(log, 'indev_467log.png')
    sc = Image.new('RGB', (256, 160), (20, 26, 20))
    d = ImageDraw.Draw(sc)
    d.text((128, 30), 'SCP-198 CASE', font=F(22), fill=(140, 240, 150), anchor='mm')
    d.text((128, 84), '1.284 kg', font=F(46), fill=(140, 240, 150), anchor='mm')
    d.text((128, 134), 'NO DEVIATION', font=F(20), fill=(140, 240, 150), anchor='mm')
    save(sc, 'indev_198scale.png')
    save(sign(384, 384, (240, 236, 220), [('CONTAINMENT', 30, (150, 20, 20)), ('PROTOCOL 198', 30, (150, 20, 20)),
                                          ('weight alarm = breach', 20, (30, 30, 30)), ('do NOT handle SCP-198', 20, (30, 30, 30)),
                                          ('D-class or robotics only', 20, (30, 30, 30)), ('seal the wing, find the holder', 20, (30, 30, 30))],
               border=(150, 20, 20)), 'indev_198proto.png')
    save(sign(384, 192, (210, 200, 40), [('SCP-207', 36, (20, 20, 20)), ('WATERPROOF LOCKER - CLASS 2 CHEM', 18, (20, 20, 20)),
                                         ('KEY: HEAD RESEARCHER, BIO-CONTAINMENT', 16, (20, 20, 20))], border=(20, 20, 20)), 'indev_207lock.png')
    save(sign(384, 192, (250, 250, 250), [('CLEAR DRINKS ONLY', 30, (20, 60, 160)),
                                          ('any coloured drink will be investigated', 16, (60, 60, 60))], border=(20, 60, 160)), 'indev_207clear.png')
    save(sign(384, 192, (60, 64, 70), [('SCP-178', 40, (255, 255, 255)), ('CLASS 3 ANOMALOUS OBJECT CONTAINER', 16, (220, 220, 220)),
                                       ('TWO ARMED L3 GUARDS', 16, (240, 200, 120))], border=(240, 200, 120)), 'indev_178lock.png')
    save(sign(384, 256, (20, 20, 20), [('LEVEL 4 PERSONNEL:', 24, (255, 80, 60)), ('READING INCIDENT', 26, (255, 255, 255)),
                                       ('REPORT 178-14-ALPHA', 26, (255, 255, 255)), ('IS MANDATORY', 26, (255, 255, 255)),
                                       ('DO NOT TOUCH WHAT YOU SEE', 18, (255, 200, 60))], border=(255, 80, 60)), 'indev_178warn.png')
    save(sign(256, 160, (230, 214, 170), [('SEIZED - MC&D', 22, (120, 30, 20)), ('"Horizon Initiative" sale', 16, (40, 30, 20)),
                                          ('MTF ALPHA-12', 18, (40, 30, 20))], border=(120, 30, 20)), 'indev_1650tag.png')
    save(sign(384, 192, (255, 170, 210), [('WATCHLIST', 30, (120, 20, 80)), ('Dr. Wondertainment products', 18, (60, 20, 40)),
                                          ('intercept every shipment', 18, (60, 20, 40))], border=(120, 20, 80)), 'indev_1079watch.png')
    print('batch 31 textures written')
