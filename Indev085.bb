;=====================================================================
; SCP: Containment Breach - Indev SCP-085 "Hand-drawn 'Cassy'"
; Indev SCP-1155 "Predatory Portrait"
;
; --- SCP-085 ---
;   A pen-and-ink drawing of a young woman on a folded sheet of graph
;   paper. She moves between drawings. If you use her from the inventory
;   she draws you a small map on the blank back of the sheet: the room
;   names of every room adjacent to the one you are in. She stops
;   drawing after a while - the paper only has so much room.
;
;   Purpose:     an information tool
;   Effect:      a HUD map of adjacent rooms, up on screen for 8 seconds
;   Drawback:    each use costs 1 charge (item state); 3 charges total.
;                every use also draws over her, which she doesn't like
;                (stress +5)
;   Reason to carry: you are lost and don't have the S-NAV
;   Spawn:       research laboratories (room2testroom, testroom3x3)
;
; --- SCP-1155 ---
;   A found-object painting in the offices. Looks like a childrens'
;   playground poster. Every time nobody is looking at it, the children
;   in it change what they are doing - louder, more of them, closer to
;   the viewer. Direct eye contact resets the painting and freezes it,
;   but leaves you feeling watched.
;
;   Environmental only. No item. No inventory slot.
;   Effect:      stress rises quickly while it is off-screen and near
;   Drawback:    forcing yourself to look at it rises stress a little
;                too, but far less. So the correct play is to look.
;   Reason:      cognitohazard practice; also the only fear source in
;                the office rooms
;   Vanilla-first: reuses IndevStress, IndevCogOn (the CF-1 glasses
;                filter it), and the existing IndevPillMsg pattern.
;   Spawn:       one instance, in the first room2offices the map has
;=====================================================================

;--------------------------------------------------------------- SCP-085
Global I085Map$, I085MapTimer#

Function Indev085Reset()
	I085Map = "" : I085MapTimer = 0
End Function

Function IndevUse085(it.Items)
	SelectedItem = Null
	If it\state >= 3 Then
		IndevPillMsg("The paper is full of tiny scribbled maps. She has run out of room and refuses to draw another one. There is a small face in the corner glaring at you.", 6)
		Return
	EndIf
	it\state = it\state + 1
	IndevStress = Min(100, IndevStress + 5)

	;compose a room-name map of the adjacent rooms
	Local names$ = ""
	If PlayerRoom <> Null Then
		Local dirs$[4]
		dirs[0] = "E" : dirs[1] = "S" : dirs[2] = "W" : dirs[3] = "N"
		Local i%
		For i = 0 To 3
			If PlayerRoom\Adjacent[i] <> Null Then
				If PlayerRoom\Adjacent[i]\RoomTemplate <> Null Then
					names = names + dirs[i] + ": " + PlayerRoom\Adjacent[i]\RoomTemplate\Name + " | "
				EndIf
			EndIf
		Next
		If names = "" Then names = "she draws a shrug. no rooms adjacent."
	EndIf
	I085Map = names
	I085MapTimer = 70.0 * 8.0

	IndevPillMsg("She sighs, unfolds the paper, and draws you a small map on the back in tight pen-strokes. She writes: " + Chr(34) + names + Chr(34) + "  then closes the paper.", 8)
End Function

Function DrawIndev085()
	If I085MapTimer <= 0 Then Return
	I085MapTimer = Max(0, I085MapTimer - FPSfactor)
	SetFont Font1
	Color 30, 30, 30
	Rect 20, GraphicHeight - 60, GraphicWidth - 40, 40, True
	Color 220, 220, 200
	Text 30, GraphicHeight - 50, "SCP-085: " + I085Map, False, False
	Color 255, 255, 255
End Function

;----------------------------------------------------------------- SCP-914
Function IndevRefine085(item.Items, setting$, x#, y#, z#)
	Local it2.Items, de.Decals
	Select setting
		Case "rough"
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			EntityColor(de\obj, 240, 240, 220)
			de\Size = 0.22 : ScaleSprite(de\obj, de\Size, de\Size)
			RemoveItem(item)
			Msg = "The paper comes out shredded. A small figure at the bottom of the last strip is very angry with you." : MsgTimer = 70*5
		Case "coarse"
			IndevRefineSetGrade(item, -1)
			If item\state > 1 Then item\state = item\state - 1
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			Msg = "The paper comes out folded once too many times. She is smaller now." : MsgTimer = 70*4
		Case "fine", "very fine"
			item\state = 0 ;charges reset
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			Msg = "The paper comes out unfolded and clean. She has redrawn herself on the fresh sheet, and looks less tired." : MsgTimer = 70*5
		Default
			it2 = CreateItem("drawing", x, y, z)
			RemoveItem(item)
			Msg = "The paper comes out as an ordinary child's drawing. She is not in it." : MsgTimer = 70*4
	End Select
End Function

;--------------------------------------------------------------- SCP-1155
Global I1155Room.Rooms, I1155Obj%, I1155Checked%, I1155LastSeen#

Function Indev1155Reset()
	;the anchor pivot is a child of the room and gets torn down with it when the
	;map is rebuilt for a new run, so we do NOT FreeEntity it here - the handle
	;in I1155Obj is already stale by the time this runs. FreeEntity on a stale
	;handle is what crashed InitNewGame on 2026-09-23. Just drop the reference.
	I1155Obj = 0 : I1155Room = Null : I1155Checked = False : I1155LastSeen = 0
End Function

;pick one room2offices to place the painting in, once per run
Function Indev1155Place()
	If I1155Checked Then Return
	I1155Checked = True
	Local r.Rooms
	For r = Each Rooms
		If r\RoomTemplate <> Null Then
			If r\RoomTemplate\Name = "room2offices" Then
				;a wall poster: use a small anchor pivot at the wall spot. The "painting" is invisible
				;in this build - the effect (stress swap on/off screen) is entirely mechanical, and its
				;presence is announced by the document on the desk.
				I1155Obj = CreatePivot(r\obj)
				PositionEntity(I1155Obj, r\x + 400.0 * RoomScale, r\y + 150.0 * RoomScale, r\z + 300.0 * RoomScale, True)
				I1155Room = r
				;drop the doc1155 file on the office desk so the mechanic is discoverable
				Local it.Items = CreateItem("doc1155", r\x + 100.0 * RoomScale, r\y + 120.0 * RoomScale, r\z + 200.0 * RoomScale)
				EntityParent(it\collider, r\obj)
				Exit
			EndIf
		EndIf
	Next
End Function

Function UpdateIndev1155()
	Indev1155Place()
	If I1155Obj = 0 Or I1155Room = Null Then Return
	If KillTimer < 0 Or PlayerRoom <> I1155Room Then Return
	If IndevCogOn Then Return ;CF-1 glasses filter it - vanilla-first

	Local d# = EntityDistance(Collider, I1155Obj)
	If d > 4.5 Then Return

	If EntityVisible(Collider, I1155Obj) Then
		I1155LastSeen = 0
		IndevStress = Min(100, IndevStress + FPSfactor * 0.02) ;small
	Else
		I1155LastSeen = I1155LastSeen + FPSfactor
		IndevStress = Min(100, IndevStress + FPSfactor * 0.10) ;bigger while off-screen
		If I1155LastSeen > 70 * 4 And I1155LastSeen < 70 * 4 + FPSfactor Then
			Msg = "Something behind you moves. When you turn, the poster is the only thing that could have made the sound. The children on it are laughing."
			MsgTimer = 70 * 5
		EndIf
	EndIf
End Function
