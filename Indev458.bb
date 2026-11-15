;=====================================================================
; SCP: Containment Breach - Indev SCP-458 "The Never-Ending Pizza Box"
;
;   A pizza box on a table in room2newcaferoom (lower cafeteria). Use it and
;   you eat a slice of your favourite pizza, hot and fresh:
;     stamina refilled, stress eased, a little healing, bleeding slowed.
;   It always regrows - but take more than 3 slices within a minute and the
;   box stays empty for 2 minutes (and you feel a bit sick).
;   SCP-914: Rough/Coarse - squashed cardboard and grease, the box is gone.
;            1:1 - unchanged.  Fine/Very Fine - extra toppings: next slice heals more.
;
;   Also placed here: one SCP-3521 capsule (the banana pill, IndevPills.bb) on
;   another table, with its effect now taking 30 seconds to kill.
;=====================================================================

Global I458Slices%, I458Window#, I458Empty#, I458Deluxe%
Global I458Pill.Items, I458Room.Rooms

Global I458Checked%

Function Indev458Reset()
	I458Slices = 0 : I458Window = 0 : I458Empty = 0 : I458Deluxe = False
	I458Checked = False
End Function

;maps generated before these items existed (older saves) never ran IndevFill458: the first time the
;player walks into room2newcaferoom, spawn whatever is missing (pizza box, document, capsule)
Function I458CheckRoom()
	If I458Checked Then Return
	If PlayerRoom = Null Then Return
	If PlayerRoom\RoomTemplate\Name <> "room2newcaferoom" Then Return
	I458Checked = True
	Local r.Rooms = PlayerRoom, i.Items, havePizza% = False, havePill% = False, haveDoc% = False, it.Items
	For i = Each Items
		Select i\itemtemplate\name
			Case "scp458" havePizza = True
			Case "doc458" haveDoc = True
			Case "scp3521"
				;(only the capsule belonging to this room counts, not the one in room2sroom)
				If i\Picked Then
					havePill = True
				ElseIf EntityDistance(i\collider, r\obj) < 12.0 Then
					havePill = True
				EndIf
		End Select
	Next
	;(the room is already rotated now, so room-local spots go through TFormPoint)
	If Not havePizza Then
		TFormPoint(0.0, -238.0, 200.0, r\obj, 0)
		it = CreateItem("scp458", TFormedX(), TFormedY(), TFormedZ())
		EntityParent(it\collider, r\obj)
	EndIf
	If Not haveDoc Then
		TFormPoint(0.0, -240.0, 20.0, r\obj, 0)
		it = CreateItem("doc458", TFormedX(), TFormedY(), TFormedZ())
		EntityParent(it\collider, r\obj)
	EndIf
	If Not havePill Then
		TFormPoint(40.0, -243.0, 330.0, r\obj, 0)
		it = CreateItem("scp3521", TFormedX(), TFormedY(), TFormedZ())
		EntityParent(it\collider, r\obj)
		I458Pill = it : I458Room = r
	EndIf
End Function

;called from FillRoom (room2newcaferoom). Table tops at y -246, measured on the room mesh.
Function IndevFill458(r.Rooms)
	Local it.Items
	;centre table (x -87..88, z -64..384)
	it = CreateItem("scp458", r\x + 0.0 * RoomScale, r\y - 238.0 * RoomScale, r\z + 200.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("doc458", r\x + 0.0 * RoomScale, r\y - 240.0 * RoomScale, r\z + 20.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	;a single yellow capsule someone left next to the pizza box (same table, clear of the box)
	it = CreateItem("scp3521", r\x + 40.0 * RoomScale, r\y - 243.0 * RoomScale, r\z + 330.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	I458Pill = it : I458Room = r

	;commissary items on the same table (IndevRations.bb)
	it = CreateItem("indevration", r\x - 60.0 * RoomScale, r\y - 243.0 * RoomScale, r\z + 320.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("indevwater", r\x - 40.0 * RoomScale, r\y - 240.0 * RoomScale, r\z + 100.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

Function IndevUse458(it.Items)
	SelectedItem = Null
	If I458Empty > 0 Then
		IndevPillMsg("You open the box. It's empty - just crumbs and a grease stain. It'll come back. You ate too fast.", 5)
		Return
	EndIf
	If I458Window <= 0 Then I458Slices = 0
	I458Window = 70*60
	I458Slices = I458Slices + 1

	PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))
	Stamina = 100
	IndevRelieveStress(12)
	If I458Deluxe Then
		Injuries = Max(0, Injuries - 0.5)
		Bloodloss = Max(0, Bloodloss - 25)
		I458Deluxe = False
		IndevPillMsg("You open the box: a huge slice with every topping you've ever liked. You eat it in four bites and feel properly human again.", 6)
	Else
		Injuries = Max(0, Injuries - 0.2)
		Bloodloss = Max(0, Bloodloss - 10)
		Select Rand(4)
			Case 1 IndevPillMsg("You open the box. Your favourite pizza, exactly how you like it, still steaming. You eat a slice. The facility feels a little less awful.", 6)
			Case 2 IndevPillMsg("Another slice. The pizza is whole again the moment you look back into the box.", 5)
			Case 3 IndevPillMsg("It's the pizza from your birthday when you were eight. You don't know how you know that.", 5)
			Default IndevPillMsg("Hot, cheesy, perfect. You feel your hands stop shaking.", 4)
		End Select
	EndIf

	If I458Slices > 3 Then
		I458Empty = 70*120
		I458Slices = 0
		BlurTimer = 70*3
		Stamina = 50
		IndevPillMsg("That one was one too many. Your stomach groans, and when you look into the box, it's empty.", 6)
	EndIf
End Function

Function UpdateIndev458()
	I458CheckRoom()
	If I458Window > 0 Then I458Window = I458Window - FPSfactor
	If I458Empty > 0 Then I458Empty = I458Empty - FPSfactor
	;the capsule is tiny: if it ever drops under the table / through the floor before it's picked
	;up, put it back next to the pizza box
	If I458Pill <> Null And I458Room <> Null Then
		If I458Pill\Picked Then
			I458Pill = Null
		ElseIf PlayerRoom = I458Room Then
			TFormPoint(EntityX(I458Pill\collider, True), EntityY(I458Pill\collider, True), EntityZ(I458Pill\collider, True), 0, I458Room\obj)
			If TFormedY() < -270.0 Then
				TFormPoint(40.0, -242.0, 330.0, I458Room\obj, 0)
				PositionEntity(I458Pill\collider, TFormedX(), TFormedY(), TFormedZ(), True)
				ResetEntity(I458Pill\collider)
				I458Pill\DropSpeed = 0
			EndIf
		EndIf
	EndIf
End Function

Function IndevRefine458(item.Items, setting$, x#, y#, z#)
	Local de.Decals
	Select setting
		Case "rough", "coarse"
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			EntityColor(de\obj, 160, 120, 60)
			de\Size = 0.3 : ScaleSprite(de\obj, de\Size, de\Size)
			RemoveItem(item)
		Case "fine", "very fine"
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
			I458Deluxe = True
			I458Empty = 0
			Msg = "The box comes out warm, and it smells incredible."
			MsgTimer = 70*4
		Default
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
	End Select
End Function
