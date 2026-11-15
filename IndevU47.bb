;=====================================================================
; SCP: Containment Breach - Indev batch 47: the legacy rooms of the Indev zone (rooms built by
; Tools\roomkit\rooms_b47.py, slot table in the generated IndevU47Data.bb) and the old door button.
;
;   room2closetsolderones  the old starting room (gear table, the white doorway)
;   room2oldconference     the early conference room
;   room2oldmedibay        the first medical bay
;   room2oldcores          the early core chambers (the bell, the refining machine, the old man's chamber)
;
; Every plain door in the Indev zone (rooms.ini zone 4) already uses the old door slab (door.x, door.jpg);
; IndevOldButtonOBJ gives those doors the old button as well: a dark steel box with a round red push button.
;=====================================================================

Global IndevOldButtonOBJ%
Global U47Seen%[4]

Function Indev47Reset(newGame%)
	Local i%
	For i = 0 To 3
		U47Seen[i] = False
	Next
End Function

;the old door button, built once (it lives as long as the other door meshes; CopyEntity it, never free it)
;same size and facing as GFX\map\Button.x, so CreateDoor's 0.03 scale and positions fit it
Function IndevOldButton%()
	If IndevOldButtonOBJ <> 0 Then Return IndevOldButtonOBJ
	Local plate% = CreateCube()
	ScaleMesh(plate, 1.4, 2.55, 0.7)
	PositionMesh(plate, 0, 0.85, -0.7)
	Local b% = CreateBrush(62, 64, 66)
	BrushShininess(b, 0.3)
	PaintMesh(plate, b)
	FreeBrush(b)
	Local btn% = CreateCylinder(14)
	ScaleMesh(btn, 0.8, 0.3, 0.8)
	RotateMesh(btn, 90, 0, 0)
	PositionMesh(btn, 0, 0.85, -1.65)
	b = CreateBrush(190, 28, 22)
	BrushShininess(b, 0.6)
	PaintMesh(btn, b)
	FreeBrush(b)
	AddMesh(btn, plate)
	FreeEntity(btn)
	HideEntity(plate)
	IndevOldButtonOBJ = plate
	Return plate
End Function

Function IndevU47Dress(r.Rooms)
End Function

Function U47Once(i%, txt$)
	If U47Seen[i] Then Return
	U47Seen[i] = True
	IS16Tell(txt, 6)
End Function

Function UpdateIndevU47(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	Select r\RoomTemplate\Name
		Case "room2closetsolderones"
			U47Once(0, "An old room. Someone laid equipment out on the table for you and never came back for it.")
			;the white doorway: the closer you get, the more it hurts to look at
			If EntityDistance(r\Objects[U47_OSR_GLOW], Camera) < 2.0 And EntityInView(r\Objects[U47_OSR_GLOW], Camera) Then
				BlurTimer = Max(BlurTimer, 300)
			EndIf
		Case "room2oldconference"
			U47Once(1, "Someone knocked a chair over. Nobody picked it up.")
		Case "room2oldmedibay"
			U47Once(2, "The old medical bay. The beds are still made.")
		Case "room2oldcores"
			U47Once(3, "The first containment chambers. Three bays, three things nobody wanted near the new wing.")
			If EntityDistance(r\Objects[U47_OCO_PIT], Collider) < 1.6 Then
				If Rand(240) = 1 Then IS16Tell("The floor here is soft, like wet cardboard.", 3)
			EndIf
	End Select
End Function
