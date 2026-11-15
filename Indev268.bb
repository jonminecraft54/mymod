;=====================================================================
; SCP: Containment Breach - Indev SCP-268 "Cap of Neglect"
;
;   Chamber T6, the sealed side room of room2newroomtest6. The chamber
;   door is a KEYPAD door (Indev268Code()); the code is on a note on the
;   desk in the west hall of the same room. The fez stands on a display
;   plinth, its document on the floor beside it.
;
;   Worn from the inventory. While it is on, nobody registers you:
;     - security cameras never confirm a sighting, so MTF is never told
;       where you are (PlayerDetected / MTF_CameraCheckDetected stay off)
;     - being unobserved is restful: stress bleeds away
;   It does NOT work on SCP-173, which reacts to being looked at rather
;   than to being remembered. The file says so. People still die to it.
;
;   The cost is time. Past two minutes the effect starts running inward
;   and you begin to forget yourself:
;     2:00  the edges go soft - blur, and the fez no longer comes off
;           on the first tug (you have to hold it)
;     3:00  you lose your own name
;     4:10  you are forgotten entirely (death)
;   Taking it off clears the whole thing instantly - it never accumulates.
;
;   SCP-914: Rough/Coarse tear the felt apart, 1:1 gives it back, Fine and
;            Very Fine hand back a fez that nobody, including you, can see
;            the point of - it works exactly the same.
;
;   Worn state is stored on the item (it\state = 1) so saves remember it,
;   the same trick SCP-1471's phone uses.
;=====================================================================

Global I268On%, I268Worn#, I268Pull#, I268Stage%, I268Check#
Global I268Note.Items, I268NoteRoom.Rooms

Const I268_SOFT# = 70.0 * 120.0    ;the edges go soft, and it stops coming off easily
Const I268_NAME# = 70.0 * 180.0    ;you lose your name
Const I268_GONE# = 70.0 * 250.0    ;you are forgotten

Function Indev268Reset()
	I268On = False : I268Worn = 0 : I268Pull = 0 : I268Stage = 0 : I268Check = 0
	I268Note = Null : I268NoteRoom = Null
End Function

;the chamber keypad code: its own number, never the same as the other two Indev codes
Function Indev268Code%()
	Local c% = (AccessCode * 7 + 2680) Mod 10000
	If c < 1000 Then c = c + 1000
	If c = AccessCode Or c = Indev914Code() Or c = IndevOffices2Code() Then c = c + 13
	Return c
End Function

;---------------------------------------------------------------------
; the room (called from FillRoom)
;---------------------------------------------------------------------

;room2newroomtest6, measured on the room mesh:
;  main corridor  x -224..224, doorways at both ends of the cell (z +-1024)
;  Chamber T6     x 480..1024, z -252..252, its doorway at x 416..480, z -96..96
;  west hall      x -2300..-300, entered through the two openings at x -224 (z +-704..832)
;  desk in the west hall: top y 144, x -1837..-1689, z -20..120
Function IndevFillTest6(r.Rooms)
	Local d.Doors, it.Items

	;--- Chamber T6: keypad door in the chamber doorway
	d = CreateDoor(r\zone, r\x + 448.0 * RoomScale, r\y, r\z, 90, r, False, False, 0, Str(Indev268Code()))
	d\AutoClose = False

	;--- the display plinth (authored in room units, top at y 169)
	r\Objects[2] = LoadMesh_Strict("GFX\map\Props\indevplinth.b3d")
	PositionEntity(r\Objects[2], r\x + 880.0 * RoomScale, r\y, r\z, True)
	ScaleEntity(r\Objects[2], RoomScale, RoomScale, RoomScale, True)
	EntityType(r\Objects[2], HIT_MAP)
	EntityParent(r\Objects[2], r\obj)

	;--- SCP-268 on top of it, its file on the floor in front
	it = CreateItem("scp268", r\x + 880.0 * RoomScale, r\y + 178.0 * RoomScale, r\z)
	EntityParent(it\collider, r\obj)
	it = CreateItem("doc268", r\x + 720.0 * RoomScale, r\y + 15.0 * RoomScale, r\z + 120.0 * RoomScale)
	EntityParent(it\collider, r\obj)

	;--- the keypad note on the desk in the west hall, with a few oddments
	it = CreateItem("note268", r\x - 1763.0 * RoomScale, r\y + 148.0 * RoomScale, r\z + 50.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	I268Note = it : I268NoteRoom = r
	it = CreateItem("bat", r\x - 1700.0 * RoomScale, r\y + 148.0 * RoomScale, r\z - 4.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("firstaid", r\x - 1640.0 * RoomScale, r\y + 20.0 * RoomScale, r\z + 200.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

;---------------------------------------------------------------------
; the Level 5 card reader on Chamber T6's wing
;---------------------------------------------------------------------

;The only standard door frames in room2newroomtest6 are the chamber doorway (which holds the
;keypad) and the two ends of the corridor, and those two are filled in by CreateDoors() after
;FillRoom has already run. So the corridor door is upgraded in place afterwards instead.
Function IndevKeycardDoor(d.Doors, lvl%)
	If d = Null Then Return
	If d\KeyCard = lvl Then Return ;already done (a quick load re-runs this with the doors still in memory)
	Local i%, px#, py#, pz#, ry#
	d\KeyCard = lvl
	d\Code = ""
	For i = 0 To 1
		If d\buttons[i] <> 0 Then
			px = EntityX(d\buttons[i], True)
			py = EntityY(d\buttons[i], True)
			pz = EntityZ(d\buttons[i], True)
			ry = EntityYaw(d\buttons[i], True)
			FreeEntity(d\buttons[i])
			d\buttons[i] = CopyEntity(ButtonKeyOBJ)
			ScaleEntity(d\buttons[i], 0.03, 0.03, 0.03)
			PositionEntity(d\buttons[i], px, py, pz, True)
			RotateEntity(d\buttons[i], 0, ry, 0, True)
			EntityParent(d\buttons[i], d\frameobj)
			EntityPickMode(d\buttons[i], 2)
		EndIf
	Next
End Function

;called right after CreateDoors/ConnectAdjacentRooms, once the corridor doors exist
Function IndevSetupTest6Doors()
	Local r.Rooms, i%, n%
	For r = Each Rooms
		If r\RoomTemplate <> Null Then
			If r\RoomTemplate\Name = "room2newroomtest6" Then
				;whichever ends this corridor actually has: -z first, then -x, +z, +x
				For i = 1 To 4
					n = (i Mod 4)
					If r\AdjDoor[n] <> Null Then
						IndevKeycardDoor(r\AdjDoor[n], 5)
						Exit
					EndIf
				Next
			EndIf
		EndIf
	Next
End Function

;the note is the only way through the keypad, so put it back on the desk if it ever falls off
Function UpdateIndev268Note()
	If I268Note = Null Or I268NoteRoom = Null Then Return
	If I268Note\Picked Then I268Note = Null : Return
	If PlayerRoom <> I268NoteRoom Then Return
	TFormPoint(EntityX(I268Note\collider, True), EntityY(I268Note\collider, True), EntityZ(I268Note\collider, True), 0, I268NoteRoom\obj)
	If TFormedY() < 120.0 Then
		TFormPoint(-1763.0, 149.0, 50.0, I268NoteRoom\obj, 0)
		PositionEntity(I268Note\collider, TFormedX(), TFormedY(), TFormedZ(), True)
		ResetEntity(I268Note\collider)
		I268Note\DropSpeed = 0
	EndIf
End Function

;---------------------------------------------------------------------
; wearing it
;---------------------------------------------------------------------

;called every frame while SCP-268 is selected in the inventory
Function IndevUse268(it.Items)
	If Not I268On Then
		I268On = True
		I268Worn = 0 : I268Stage = 0 : I268Pull = 0
		it\state = 1
		Msg = "You put the fez on. Nothing happens, and that is exactly what is supposed to happen - the facility has just stopped keeping track of you."
		MsgTimer = 70*7
		SelectedItem = Null
		Return
	EndIf

	;taking it off. Easy at first; once it has started working on you, you have to hold on to the idea
	If I268Worn < I268_SOFT Then
		Indev268TakeOff(it, "You lift the fez off. The corridor feels louder at once, as though a room full of people just remembered you were standing in it.")
		Return
	EndIf

	CurrSpeed = CurveValue(0, CurrSpeed, 5.0)
	DrawItemUseProgress(it)
	I268Pull = Min(I268Pull + FPSfactor / 3.0, 100.0)
	If I268Pull < 100 Then Return
	Indev268TakeOff(it, "You get both hands to it and pull. It comes off. You remember your name on the third try: D-9341.")
End Function

Function Indev268TakeOff(it.Items, txt$)
	I268On = False
	I268Worn = 0 : I268Stage = 0 : I268Pull = 0
	it\state = 0
	BlurTimer = 0
	Msg = txt
	MsgTimer = 70*6
	SelectedItem = Null
End Function

Function UpdateIndev268()
	UpdateIndev268Note()

	;after loading a save: it is still on if a worn fez (item state 1) exists
	If Not I268On Then
		I268Check = I268Check - FPSfactor
		If I268Check > 0 Then Return
		I268Check = 70
		Local f.Items
		For f = Each Items
			If f\itemtemplate\name = "scp268" And f\state >= 1 Then
				I268On = True : I268Worn = 0 : I268Stage = 0 : I268Pull = 0
				Exit
			EndIf
		Next
		If Not I268On Then Return
	EndIf

	If KillTimer < 0 Then I268On = False : Return

	;dropped, refined away or otherwise no longer on you
	Local n%, worn.Items = Null
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "scp268" And Inventory(n)\state >= 1 Then worn = Inventory(n) : Exit
		EndIf
	Next
	If worn = Null Then
		;it left your hands with the "worn" mark still on it - clear it so it isn't picked up again as worn
		Local lost.Items
		For lost = Each Items
			If lost\itemtemplate\name = "scp268" Then lost\state = 0
		Next
		I268On = False : I268Worn = 0 : I268Stage = 0 : I268Pull = 0
		Return
	EndIf

	;--- nobody registers you
	PlayerDetected = False
	MTF_CameraCheckDetected = False
	IndevStress = Max(0, IndevStress - FPSfactor * 0.025)

	;--- and then it starts running inward
	I268Worn = I268Worn + FPSfactor

	If I268Stage < 1 And I268Worn > 70*60 Then
		I268Stage = 1
		Msg = "A minute under the fez. Nothing has looked at you since you put it on. Not the cameras, not the doors, not the dark."
		MsgTimer = 70*5
	EndIf
	If I268Stage < 2 And I268Worn > I268_SOFT Then
		I268Stage = 2
		Msg = "Two minutes. The edges of things have gone soft. You reach up to take the fez off and your hand doesn't quite believe there is a fez."
		MsgTimer = 70*6
	EndIf
	If I268Stage < 3 And I268Worn > I268_NAME Then
		I268Stage = 3
		Msg = "Three minutes. You cannot remember your own number. You cannot remember which way you came in. TAKE IT OFF."
		MsgTimer = 70*7
		PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Breath.ogg"))
	EndIf

	If I268Worn > I268_SOFT Then
		BlurTimer = Max(BlurTimer, (I268Worn - I268_SOFT) * 0.35)
		If I268Worn > I268_NAME Then CameraShake = Max(CameraShake, (I268Worn - I268_NAME) / (70.0 * 40.0))
	EndIf

	If I268Worn > I268_GONE Then
		I268On = False
		IndevPillDeath("Recovery of SCP-268 from Chamber T6 corridor. The fez was found on the floor. No personnel are recorded as having removed it from containment and no personnel are recorded as missing. The file is closed.")
	EndIf
End Function

;---------------------------------------------------------------------
; SCP-914 (called from IndevRefinePill)
;---------------------------------------------------------------------

Function IndevRefine268(item.Items, setting$, x#, y#, z#)
	Local it2.Items, de.Decals
	Select setting
		Case "rough", "coarse"
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			EntityColor(de\obj, 104, 68, 44)
			de\Size = 0.28 : ScaleSprite(de\obj, de\Size, de\Size)
			If item\state >= 1 Then I268On = False : I268Worn = 0 : I268Stage = 0
			RemoveItem(item)
			Msg = "The fez comes out as a heap of brown felt and one black thread. You find it hard to care, and then hard to remember what you put in."
			MsgTimer = 70*6
		Default
			it2 = CreateItem("scp268", x, y, z)
			RemoveItem(item)
			Msg = "The fez comes out brushed and pressed. You look at it for a while before you can work out why you were interested in it."
			MsgTimer = 70*5
	End Select
End Function
