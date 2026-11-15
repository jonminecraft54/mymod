;=====================================================================
; SCP: Containment Breach - Indev room2newoffices2 + SCP-005 + SCP-1471
;
;   room2newoffices2: an office corridor (walls at x -224 / 224) with
;     NE office   (doorway z 352..544)   - plain door. Keypad note, battery, first aid
;     SE office   (doorway z -672..-480) - KEYPAD door, code on the note. SCP-005 + its document
;     W  office   (doorway x -478, z -96..96, behind the open lobby) - LEVEL 3 keycard door.
;                 SCP-1471's phone + its document
;
;   SCP-005 "Skeleton Key": select it like a keycard. Any card reader accepts it (level 6),
;     and while it's in your hand, keypads within reach unlock (the code is gone for good).
;     Lockdown-locked doors still don't open - it's a key, not a crowbar.
;
;   SCP-1471 "MalO ver1.0.0": use the phone and the app installs itself. From then on
;     SCP-1471-A - a black-furred figure with a canine skull - turns up behind you
;     now and then, out of sight. Turn around and see it and it's gone. It never hurts
;     you, but being watched is stressful. SCP-914 Rough/Coarse destroys the phone and
;     ends it; the app can't be uninstalled.
;=====================================================================

Global I1471On%, I1471Fig%, I1471Skull%, I1471State%, I1471T#, I1471Seen#, I1471Count%, I1471Check#
Global INoteOff2.Items, INoteOff2Room.Rooms

Function IndevOffices2Reset()
	;(the figure is unparented and survives map changes; hide it, keep the handle)
	If I1471Fig <> 0 Then HideEntity(I1471Fig)
	I1471On = False : I1471State = 0 : I1471T = 70*60 : I1471Seen = 0 : I1471Count = 0
End Function

Function IndevOffices2Code%()
	Local c% = (AccessCode * 13 + 2205) Mod 10000
	If c < 1000 Then c = c + 1000
	If c = AccessCode Or c = Indev914Code() Then c = c + 7
	Return c
End Function

;called from FillRoom
Function IndevFillOffices2(r.Rooms)
	Local d.Doors, it.Items
	;NE office - plain door
	d = CreateDoor(r\zone, r\x + 240.0 * RoomScale, r\y, r\z + 448.0 * RoomScale, 90, r, False, False, 0)
	d\AutoClose = False
	;SE office - keypad
	d = CreateDoor(r\zone, r\x + 240.0 * RoomScale, r\y, r\z - 576.0 * RoomScale, 90, r, False, False, 0, Str(IndevOffices2Code()))
	d\AutoClose = False
	;W office - level 3 keycard
	d = CreateDoor(r\zone, r\x - 478.0 * RoomScale, r\y, r\z, 90, r, False, False, 3)
	d\AutoClose = False

	;NE office desk (top y 120)
	;(the big desk by the door: top y 120, x 640..980, z 640..760 - measured on the mesh)
	it = CreateItem("noteoffices2", r\x + 820.0 * RoomScale, r\y + 123.0 * RoomScale, r\z + 700.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	INoteOff2 = it : INoteOff2Room = r
	it = CreateItem("bat", r\x + 900.0 * RoomScale, r\y + 123.0 * RoomScale, r\z + 690.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("firstaid", r\x + 600.0 * RoomScale, r\y + 20.0 * RoomScale, r\z + 500.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	;SE office desk
	it = CreateItem("scp005", r\x + 742.0 * RoomScale, r\y + 130.0 * RoomScale, r\z - 620.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("doc005", r\x + 742.0 * RoomScale, r\y + 130.0 * RoomScale, r\z - 740.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	;W office desk
	it = CreateItem("scp1471", r\x - 1091.0 * RoomScale, r\y + 130.0 * RoomScale, r\z + 160.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("doc1471", r\x - 1091.0 * RoomScale, r\y + 130.0 * RoomScale, r\z + 40.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

;the keypad note must be findable: if it ever ends up under the desk / in the floor before it's
;been picked up, put it back on the desk top
Function UpdateIndevNoteOff2()
	If INoteOff2 = Null Or INoteOff2Room = Null Then Return
	If INoteOff2\Picked Then INoteOff2 = Null : Return
	If PlayerRoom <> INoteOff2Room Then Return
	TFormPoint(EntityX(INoteOff2\collider, True), EntityY(INoteOff2\collider, True), EntityZ(INoteOff2\collider, True), 0, INoteOff2Room\obj)
	If TFormedY() < 100.0 Then
		TFormPoint(820.0, 124.0, 700.0, INoteOff2Room\obj, 0)
		PositionEntity(INoteOff2\collider, TFormedX(), TFormedY(), TFormedZ(), True)
		ResetEntity(INoteOff2\collider)
		INoteOff2\DropSpeed = 0
	EndIf
End Function

;----------------------------------------------------------------- SCP-005

Function UpdateIndev005()
	If SelectedItem = Null Then Return
	If SelectedItem\itemtemplate\name <> "scp005" Then Return
	Local d.Doors, n% = 0
	For d = Each Doors
		If d\Code <> "" And (Not d\locked) Then
			If d\buttons[0] <> 0 Then
				If EntityDistance(Collider, d\buttons[0]) < 1.6 Or EntityDistance(Collider, d\buttons[1]) < 1.6 Then
					d\Code = ""
					n = n + 1
				EndIf
			EndIf
		EndIf
	Next
	If n > 0 Then
		PlaySound_Strict(KeyCardSFX1)
		Msg = "You hold the key up to the keypad. Something inside it clicks, and the light turns green. It won't ask for a code again."
		MsgTimer = 70*6
	EndIf
End Function

;----------------------------------------------------------------- SCP-1471

Function IndevUse1471(it.Items)
	SelectedItem = Null
	If I1471On Then
		IndevPillMsg("The MalO icon is the only thing on the home screen. You try to uninstall it. The phone says: " + Chr(34) + "Why?" + Chr(34), 6)
		IndevStress = Min(100, IndevStress + 5)
		Return
	EndIf
	I1471On = True
	it\state = 1 ;(stored on the phone item, so saves remember the app is installed)
	I1471T = 70 * Rnd(25, 40)
	PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
	IndevPillMsg("You tap the only app on the screen: MalO ver1.0.0. A dog's skull stares out of the display for a moment, then the phone goes black. You have the feeling you just made a friend.", 8)
End Function

Function I1471Make()
	If I1471Fig <> 0 Then Return
	I1471Fig = CopyEntity(ClassDObj)
	Local sc# = 0.62 / MeshWidth(I1471Fig)   ;a head taller than a person
	ScaleEntity(I1471Fig, sc, sc, sc)
	EntityFX(I1471Fig, 1)
	INR65ColorAll(I1471Fig, 10, 9, 9)
	MeshCullBox(I1471Fig, -MeshWidth(ClassDObj), -MeshHeight(ClassDObj), -MeshDepth(ClassDObj)*4, MeshWidth(ClassDObj)*2, MeshHeight(ClassDObj)*2, MeshDepth(ClassDObj)*8)
	;the skull: a pale elongated head with a snout, black eye pits
	I1471Skull = CreateSphere(10)
	EntityColor(I1471Skull, 215, 210, 195)
	EntityFX(I1471Skull, 1)
	Local snout% = CreateSphere(8, I1471Skull)
	ScaleEntity(snout, 0.55, 0.5, 0.9)
	PositionEntity(snout, 0, -0.35, 0.95)
	EntityColor(snout, 205, 200, 185) : EntityFX(snout, 1)
	Local k%, eye%
	For k = 0 To 1
		eye = CreateSphere(6, I1471Skull)
		ScaleEntity(eye, 0.22, 0.25, 0.1)
		PositionEntity(eye, -0.38 + 0.76 * k, 0.1, 0.88)
		EntityColor(eye, 0, 0, 0) : EntityFX(eye, 1)
	Next
	ScaleEntity(I1471Skull, 0.13, 0.14, 0.15)
	HideEntity(I1471Fig) : HideEntity(I1471Skull)
End Function

Function I1471Hide()
	If I1471Fig <> 0 Then HideEntity(I1471Fig) : HideEntity(I1471Skull)
	I1471State = 0
	I1471T = 70 * Rnd(45, 100)
	I1471Seen = 0
End Function

;try to stand it behind the player, on a floor, with a clear line to the camera, out of view
Function I1471Place%()
	Local tries%, a#, dist#, x#, z#, fy#, p%
	I1471Make()
	For tries = 1 To 8
		a = EntityYaw(Camera, True) + 180 + Rnd(-50, 50)
		dist = Rnd(2.5, 5.5)
		x = EntityX(Collider, True) - Sin(a) * dist
		z = EntityZ(Collider, True) + Cos(a) * dist
		If LinePick(x, EntityY(Camera, True), z, 0, -3.0, 0) <> 0 Then
			fy = PickedY()
			p = CreatePivot()
			PositionEntity(p, x, fy + 1.5, z, True)
			If EntityVisible(Camera, p) And (Not EntityInView(p, Camera)) And Abs(fy - (EntityY(Collider, True) - 0.3)) < 0.8 Then
				FreeEntity(p)
				PositionEntity(I1471Fig, x, fy, z, True)
				PointEntity(I1471Fig, Collider)
				RotateEntity(I1471Fig, 0, EntityYaw(I1471Fig, True), 0, True)
				PositionEntity(I1471Skull, x, fy + 1.78, z, True)
				RotateEntity(I1471Skull, 10, EntityYaw(I1471Fig, True), 0, True)
				ShowEntity(I1471Fig) : ShowEntity(I1471Skull)
				Return True
			EndIf
			FreeEntity(p)
		EndIf
	Next
	Return False
End Function

Function UpdateIndev1471()
	;after loading a save: the app is on if an installed phone (item state 1) still exists anywhere
	If Not I1471On Then
		I1471Check = I1471Check - FPSfactor
		If I1471Check > 0 Then Return
		I1471Check = 70
		Local ph.Items
		For ph = Each Items
			If ph\itemtemplate\name = "scp1471" And ph\state >= 1 Then
				I1471On = True : I1471T = 70 * Rnd(30, 60)
				Exit
			EndIf
		Next
		If Not I1471On Then Return
	EndIf
	If KillTimer < 0 Or PlayerRoom = Null Then
		If I1471State = 1 Then I1471Hide()
		Return
	EndIf
	Select I1471State
		Case 0
			I1471T = I1471T - FPSfactor
			If I1471T <= 0 Then
				If I1471Place() Then
					I1471State = 1 : I1471T = 70*14 : I1471Seen = 0
				Else
					I1471T = 70*5
				EndIf
			EndIf
		Case 1
			;looked at it? it lingers for a heartbeat, then it's gone
			Local seen% = False
			If BlinkTimer > -6 Then
				If EntityInView(I1471Skull, Camera) Then seen = EntityVisible(Camera, I1471Skull)
			EndIf
			If seen Then
				If I1471Seen = 0 Then
					I1471Count = I1471Count + 1
					IndevStress = Min(100, IndevStress + 6)
					HeartBeatVolume = Max(HeartBeatVolume, 0.5) : HeartBeatRate = Max(HeartBeatRate, 110)
					If I1471Count = 1 Then
						Msg = "There's something standing behind you. Black fur. A dog's skull where the face should be. It's watching you - "
						MsgTimer = 70*5
					ElseIf Rand(3) = 1 Then
						Msg = "It's there again. It tilts its skull, like it's worried about you."
						MsgTimer = 70*4
					EndIf
				EndIf
				I1471Seen = I1471Seen + FPSfactor
				If I1471Seen > 70*0.4 Then I1471Hide()
			Else
				I1471T = I1471T - FPSfactor
				;keep facing the player while it waits
				PointEntity(I1471Fig, Collider)
				RotateEntity(I1471Fig, 0, EntityYaw(I1471Fig, True), 0, True)
				RotateEntity(I1471Skull, 10, EntityYaw(I1471Fig, True), 0, True)
				If I1471T <= 0 Or EntityDistance(I1471Fig, Collider) > 9.0 Then I1471Hide()
			EndIf
	End Select
End Function

Function IndevRefine1471(item.Items, setting$, x#, y#, z#)
	Local de.Decals
	Select setting
		Case "rough", "coarse"
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			de\Size = 0.15 : ScaleSprite(de\obj, de\Size, de\Size)
			RemoveItem(item)
			If I1471On Then
				I1471On = False
				I1471Hide()
			EndIf
		Default
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
	End Select
End Function
