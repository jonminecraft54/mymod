# CBRE-EX rooms from reference images 51–59

The rooms are in `Tools\cbre\out\`. Each one is a `.vmf` file for CBRE-EX v2.2.1, plus a `_preview.jpg` that shows the same brushes baked with lights. In the previews, prop models show as tan boxes; CBRE shows the real models.

| File | Reference | Shape | What's in it |
|---|---|---|---|
| room2cbre_storage | 51 | room2 | White hall with a black beamed ceiling. Shelving bays with crates and boxfiles, pilasters, riveted band, baseboards, Foundation banner, red poster and logo, benches, camera over the door, LCZ signs, vents, 8 fixtures |
| room2cbre_office | 52 | room2 | Corridor with a glazed partition (mullions, wooden lower wall) into a carpeted office. T-bar ceiling with 4 light panels, 2 desks (monitor, keyboard, chair, mug, lamp), filing cabinets, bookshelf, whiteboard, wall monitor, painting, wainscot |
| room2cbre_gallery | 53 | room2 | Upper balcony walkway with railing, mullions and transom over a chamber 384 units below. 3 columns, consoles, hazard test pad, 3 spotlights, a 24-step stair with railing, pipes, camera |
| room2cbre_hczmachine | 54, 59 | room2 | HCZ corridor: 14 concrete pilasters with caps, beams, wall lamp heads, grated trench with yellow edges, hazard baseboard. Machine window (frame, mullions, glass) into a hall with 3 tanks on plinths, pipes, an electrical box and an orange light. Cable tray, 2 pipe runs |
| room2cbre_hoist | 55 | room2 | Control room: console desk under a 1280-wide window, 4 consoles with seats, control panels, electrical box. Shaft from −1024 to +768 with a gantry beam, trolley, chains, platform with a crate, guide rails, hazard bands, spotlights and a red pit glow |
| room2cbre_shutters | 56 | room2 | Concrete corridor with 6 bays behind roll-up shutters (one half open over crates). Each shutter has a housing, guide rails, bollards and floor markings. Beams, cable tray, pipe, yellow centre line, camera |
| room2cbre_dclass | 57 | room2 | Cell corridor with 4 cells. Each cell has a bed, toilet, sink (with pedestal and mirror), vent, own light, steel door frame, number sign 1–4 and D-class sign |
| room4cbre_pillar | 58 | room4 | 4-way junction around an octagonal pillar (plinth, metal ring, riveted band, capital). Zone signs on the pillar, radial beams, coffer beams, 4 ceiling panels, fixtures in every arm, signs, vents, camera |

All brushes, textures and entities are standard CBRE ones; nothing is a custom format or command.

## What the files use (all standard CBRE-EX features)

- **Brushes (solids)**: everything you can walk on or see is a convex brush, made the same way as the Block tool's boxes and the Cylinder tool's prisms.
  - Walls with doorways are split into separate brushes around the opening, as you would by hand with the Clip tool.
- **Materials**: texture names from the game's `GFX\map` folder, e.g. `whitewall`, `tilefloor`, `concretefloor`, `metal`, `scpcb_rivetband`, `scpcb_lightpanel`, `heavy_containment_wall_1789291243567`. CBRE lists them once that folder is a texture directory.
- **Tool textures**:
  - Signs and posters are 1–2 unit thin brushes. Only their front face has the picture.
  - Their other five faces use `tooltextures/remove_face`, which CBRE's RMesh export leaves out.
- **Entities** (CBRE's built-in point entities, with the same keys CBRE writes):
  - `light`: `color`, `intensity`, `range`, `hassprite`.
  - `spotlight`: the same keys plus `angles`, `innerconeangle` and `outerconeangle`.
  - `waypoint`: the NPC path network.
  - `soundemitter`: `sound` is the index of the ambient sound, `range` is how far it carries.
  - `model`: `file`, `angles`, `scale`. Files are in `GFX\map\Props`: `crate1.x`, `scpcb_bench.x`, `monitor.x`, `keyboard.x`, `officeseat_a.x`, `scpcb_cabinet.x`, `dclass_bed.x`, `dclass_toilet.x`, `dclass_sink.x`, `scpcb_console.x`, `lamp1.x`, `mug.x` and others.
- **Units**: SCP:CB room units.
  - One room cell is 2048 × 2048, centred on 0, with the floor at height 0.
  - CBRE is Z-up: the game's "up" is CBRE's Z, and the RMesh export swaps it back.
  - Doorways are 192 × 320 holes at the cell edges (z = ±1024, and x = ±1024 for the room4).

## Setting up CBRE-EX (once)

1. Start `CBRE-EX.exe` from `C:\Users\Computer\Downloads\Amensia\cbre\CBRE-EX.v2.2.1`.
2. Open **Tools → Options** (Settings) and go to the **Directories** tab:
   - **Texture directories**: add `I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map`.
   - **Model directories**: add `I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map\Props`.
3. Save the options and restart CBRE so it indexes the textures.

## Opening and checking a room

1. **File → Open**, then choose e.g. `Tools\cbre\out\room2cbre_storage.vmf`. CBRE reads `.vmf` with its VMF provider.
2. In the 3D view, switch to *Textured* (or *Lightmapped* to preview the lights).
3. Check for pink/black "missing" faces. If you see any, the texture directory from step 2 above isn't set.
4. Optional: change anything you like.
   - **Block tool**: new brushes.
   - **Clip tool**: cut a brush.
   - **Texture Application** (Shift+A): retexture faces.
   - **Entity tool**: add more `light`/`waypoint`/`model` entities.
   - Keep new brushes convex and don't leave gaps the player can see through.
5. **File → Save As** `.cbr` (CBRE's own format) so later edits keep everything.

## Exporting to the game

1. **File → Export**, choose **RMesh** and save it as `GFX\map\<roomname>.rmesh`, e.g. `GFX\map\room2cbre_storage.rmesh`. That's where this mod keeps its other rooms; any path works as long as `rooms.ini` points to it.
   - CBRE bakes the lightmaps during export and writes them next to the rmesh as `<name>_lm*.png`.
   - The `light`, `spotlight`, `waypoint`, `soundemitter` and `model` entities go into the rmesh, and the game loads them like the original rooms' entities.
2. Add the room to `Data\rooms.ini`, using the same style as the existing entries:
   ```ini
   [room2cbre_storage]
   descr=LCZ storage hall: shelving, benches, the Foundation banner.
   mesh path=GFX\map\room2cbre_storage.rmesh
   shape = 2
   commonness = 20
   zone1=1
   ```
   - `shape=4` for `room4cbre_pillar`.
   - `zone1=1` is LCZ, `2` is HCZ, `3` is EZ. Put `room2cbre_hczmachine` in `zone1=2`.
   - `commonness=0` with `disabledecals` etc. if you only want to place it by code.
3. Doors are placed by the game at each doorway, the same as every other room2/room4. Nothing extra is needed.

## Changing the rooms by script instead of in CBRE

`Tools\cbre\rooms_cbre.py` defines each room in Python.

- Building blocks:
  - `shell` (hall), `trims` (baseboard and band), `fixture` (light housing plus `light` entity), `pilaster`.
  - `beam_x`/`beam_z`, `pipe_x`/`pipe_z` (with clamp collars), `cable_tray_z`, `railing_x`/`railing_z`.
  - `shelving`, `desk`, `bench`, `camera`, `vent_x`.
- Regenerate everything with:
  ```bash
  python "I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\Tools\cbre\rooms_cbre.py"
  ```
  - Add `--nopreview` to skip the renders.
  - Add a room name to build only that room.
- `cbre_vmf.py` writes the VMF:
  - It orients every face so its normal points out of its brush (CBRE's `(p3−p1)×(p2−p1)` rule).
  - It picks Hammer-style world-aligned texture axes and scales each texture to the size the game's rooms use.
- Before writing, the brushes were checked: no flat brushes, no degenerate or inward planes, no missing textures or models.
