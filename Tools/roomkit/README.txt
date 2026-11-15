roomkit - generates SCP:CB rooms (.rmesh + baked lightmap) from Python

  python build_all.py --game --views     rebuild all six Annex rooms into GFX\map (previews go to out\)
  python room_catwalk.py                 build one room into out\ and render test views
  python make_signs.py                   GFX\map\indev_signs.png (+ signs.json, the UV rects)
  python make_fans.py                    GFX\map\indev_fan.b3d / indev_ceilfan.b3d / indev_fan.png
  python make_docs2.py                   the eight documents in GFX\items
  python make_npctex.py                  GFX\npcs\indev_tech.jpg / indev_archivist.jpg

Run everything from this folder. Needs Python 3 with numpy and Pillow.

roomkit.py   surfaces, walls with door holes, boxes, pipes, lightmap baker, .rmesh writer, preview renderer
parts.py     shared pieces: door recess, elevator shaft, railings, shelves, cabinets, lights, signs
rmesh.py     .rmesh reader / writer (mirrors LoadRMesh in MapSystem.bb)
anchors.json the room-unit coordinates IndevAnnex.bb uses (doors, lift pivots, item spots)
wire.py      how the rooms were hooked into Main.bb / MapSystem.bb / UpdateEvents.bb / Data\*.ini

Conventions: 2048 units per map cell, door holes 192 x 320 on the cell edge, y up.
Room shapes: 1 = door on -z, 2 = doors on -z and +z, 2C = -z and +x, 3 = -z, +x, -x.

Fifth batch - ten containment rooms for sixteen SCPs (IndevS16.bb)
  python make_assets3.py      labels, name plates, exhibit textures, NPC skins, the 16 typed documents
  python make_models3.py      GFX\npcs: indev_bear.b3d, scp1515.b3d, scp1513.b3d, scp1513b.b3d
  python make_docs4.py        the 16 handwritten notes (doc<number>b)
  python gen_s16.py --game    builds the rooms, writes IndevS16Data.bb (slot constants + FillRoom table)
  python wire5.py             hooks (backups *.bak_s16); safe to run twice
  python check_s16.py         re-parses the rooms, checks every file / item the batch names exists
  python views_s16.py         extra preview renders into out\
rooms_s16.py holds the rooms. named() / ndoor() / reserve() give a thing a name; gen_s16.py turns the
names into r\Objects[] / r\RoomDoors[] slots and S16_* constants, so IndevS16.bb has no coordinates.

Sixth batch - seven rooms for thirteen SCPs (IndevS13.bb)
  python make_assets4.py      labels, door plates, name plates, packaging sheet, materials, NPC skins, 26 documents
  python make_models4.py      GFX\npcs\scp1145.b3d (the teddy), scp1080t.b3d (the pallet)
  python gen_b6.py --game     builds the rooms (rooms_b6.py), writes IndevS13Data.bb (S13_* constants)
  python wire6.py             hooks (backups *.bak_s13); safe to run twice
  python check_s16.py b6_names.txt IndevS13.bb IndevS13Data.bb     the same file / item check
gen_s16.blitz() now takes a prefix and file names, so both batches share one table writer.

Seventh batch - ten rooms for ten SCPs (IndevS10.bb)
  python make_sfx5.py         SFX\Indev\*.wav: synthesised train, barks, applause, buzzer, wind, puppet voices, jukebox
  python make_assets5.py      labels, door plates, name plates, printed props, neon sheet, materials, views, NPC skins, 23 documents
  python make_models5.py      GFX\npcs: scp052.b3d + scp052d.b3d (the R4 car and a door leaf), scp953f, indev_dog,
                              scp6096, scp1269 + scp1269f, scp3325 + scp3325j, indev_shade, indev_cart, scp482
  python view_models.py       out\models5.png: offline renders of those models
  python gen_b7.py --game     builds the rooms (rooms_b7.py), writes IndevS10Data.bb (S10_* constants)
  python wire7.py             hooks (backups *.bak_s10); safe to run twice
  python check_s16.py b7_names.txt IndevS10.bb IndevS10Data.bb     the same file / item check
  python views_b7.py          extra preview renders into out\b7_views.jpg
gen_b7.py has its own table writer (a copy of gen_s16.blitz) because its doors can start open or use the
old Indev door panel: ndoor(..., old=True, start_open=True) in rooms_b7.py.

Eighth batch - five rooms for eight SCPs (IndevS08.bb)
  python make_sfx6.py         SFX\Indev\*.wav: marshmallow choir, Geiger counters, criticality flash, bells, teletype, fire ...
  python make_assets6.py      labels, door plates, name plates, printed props, neon sheet, materials, Santa skins, 17 documents
  python make_models6.py      GFX\npcs: scp956, indev_unicycle, scp4255s (the sleigh), indev_reindeer, scp1225, indev_parcel
  python gen_b8.py --game     builds the rooms (rooms_b8.py), writes IndevS08Data.bb (S08_* constants)
  python wire8.py             hooks (backups *.bak_s08); safe to run twice
  python check_s16.py b8_names.txt IndevS08.bb IndevS08Data.bb     the same file / item check
  python views_b8.py          extra preview renders into out\b8_views.jpg
gen_b7.blitz() now takes a prefix, file and event name like gen_s16.blitz(), so gen_b8 shares it.

Ninth batch - four rooms for four SCPs (IndevS04.bb)
  python make_sfx7.py         SFX\Indev\*.wav: the fire's scream, mist, hose, shutter, clicks, UV hum, page, drone, poof
  python make_assets7.py      labels, door plates, name plates, printed props, neon sheet, fireproof board, char messages, 2 skins, 8 documents
  python make_models7.py      GFX\npcs: scp457, scp0161, scp152, scp280, scp280e   (add "view" for out\models7.png)
  python gen_b9.py --game     builds the rooms (rooms_b9.py), writes IndevS04Data.bb (S04_* constants)
  python wire9.py             hooks (backups *.bak_s04); safe to run twice
  python check_s16.py b9_names.txt IndevS04.bb IndevS04Data.bb     the same file / item check
  python views_b9.py          extra preview renders into out\b9_views.jpg
rooms_b9.py adds box_room() (a rectangular room with holes in any wall), doorway() (the lining of a door
through a thick wall) and BandMat (a wall material whose dark band stays at one height). The previewer now
blends any texture that has transparent pixels, not only glass.png.
