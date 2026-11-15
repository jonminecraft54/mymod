;=====================================================================
; SCP: Containment Breach - Indev SCP-330 "Take Only Two"
;
; A steel bowl of wrapped candy on a cafeteria table, with a note taped
; to it that everyone reads. Click the bowl to take a piece. The count
; resets after 10 minutes (the "24 hours" of the original, sped up).
; Take a third piece before then and both hands are gone:
;   - heavy bleeding
;   - everything you're holding falls to the floor, and you can't pick
;     anything up - except first aid, SCP-9282 and SCP-8228, which you
;     can still manage with your forearms
;   - SCP-9282 (regenerating bandage) or SCP-8228 (the cupcake) grows
;     the hands back
;=====================================================================

Global I330Bowl%, I330Room.Rooms, I330Tex%
Global I330Taken%, I330Reset#, I330NoteShown%
Global I330NoHands%, I330Pick%

Function Indev330Reset()
	I330Bowl = 0 : I330Room = Null : I330Tex = 0 : I330Pick = 0
	I330Taken = 0 : I330Reset = 0 : I330NoteShown = False
	I330NoHands = False
End Function

;called from FillRoom with room-local coordinates (RoomScale units); the bowl settles onto the table below
Function IndevCreate330%(r.Rooms, lx#, ly#, lz#, yaw#)
	If I330Bowl <> 0 Then Return False
	I330Room = r
	I330Bowl = LoadMesh_Strict("GFX\map\Props\scp330.b3d", r\obj)
	I330Tex = LoadTexture_Strict("GFX\map\Props\scp330.png", 1)
	EntityTexture(I330Bowl, I330Tex)
	ScaleEntity(I330Bowl, 1.9, 1.9, 1.9)        ;model centimetres -> RoomScale units (local to the room)
	PositionEntity(I330Bowl, lx, ly, lz, False)
	RotateEntity(I330Bowl, 0, yaw, 0, False)

	;no LinePick here: during map generation the table props aren't pickable yet, so the ray used to drop the bowl
	;through the table onto the floor (or leave it hovering). The cafeteria table top is at y -246 (checked
	;against the room mesh), so the bowl goes straight onto it.
	If ly > -246.0 And r\RoomTemplate\Name = "room2cafeteria" Then PositionEntity(I330Bowl, lx, -246.0 + 0.5, lz, False)
	EntityPickMode(I330Bowl, 2)
	Return True
End Function

;hooked into PickItem (Items.bb): returns True if the pickup should be blocked
Function IndevNoHands%(item.Items)
	If (Not I330NoHands) Then Return False
	Select item\itemtemplate\name
		Case "scp9282", "scp8228", "firstaid", "firstaid2", "finefirstaid", "veryfinefirstaid"
			Return False ;you can still manage these with your forearms and your teeth
	End Select
	Msg = "You have no hands to pick it up with."
	MsgTimer = 70*3
	Return True
End Function

;"heal" console command: hands back and the bowl's count cleared
Function Indev330Heal()
	I330NoHands = False
	I330Taken = 0 : I330Reset = 0
End Function

;"restore330" console command: puts the bowl back in the cafeteria if it's missing, and resets its state
Function Indev330Restore()
	Indev330Heal()
	If I330Bowl <> 0 Then
		CreateConsoleMsg("SCP-330 is already in " + I330Room\RoomTemplate\Name + " - candy count and hands reset.")
		Return
	EndIf
	Local r.Rooms
	For r = Each Rooms
		If r\RoomTemplate\Name = "room2cafeteria" Then
			If IndevCreate330(r, -540.0, -150.0, 30.0, 0) Then
				CreateConsoleMsg("SCP-330 restored in room2cafeteria.")
				Return
			EndIf
		EndIf
	Next
	CreateConsoleMsg("No room2cafeteria on this map - SCP-330 can't be restored.", 255, 0, 0)
End Function

;SCP-9282 and SCP-8228 call this
Function Indev330RegrowHands()
	If (Not I330NoHands) Then Return
	I330NoHands = False
	Msg = Msg + " Your hands grow back from the stumps, whole and new. You flex your fingers for a long time."
	MsgTimer = Max(MsgTimer, 70*8)
End Function

Function UpdateIndev330()
	If I330Bowl = 0 Then Return
	;a bigger invisible pick target, made once the room has its final rotation (unparented, so the
	;room's tiny scale doesn't shrink the radius)
	If I330Pick = 0 Then
		I330Pick = CreatePivot()
		PositionEntity(I330Pick, EntityX(I330Bowl, True), EntityY(I330Bowl, True) + 0.04, EntityZ(I330Bowl, True), True)
		EntityRadius(I330Pick, 0.14)
		EntityPickMode(I330Pick, 1, False)
	EndIf

	If I330Reset > 0 Then
		I330Reset = I330Reset - FPSfactor
		If I330Reset <= 0 Then I330Taken = 0
	EndIf

	;no hands: nothing stays in your grip
	Local n%
	If I330NoHands Then
		For n = 0 To MaxItemAmount - 1
			If Inventory(n) <> Null Then
				If IndevNoHands(Inventory(n)) Then
					If SelectedItem = Inventory(n) Then SelectedItem = Null
					DropItem(Inventory(n), False)
				EndIf
			EndIf
		Next
	EndIf

	If KillTimer < 0 Then Return
	Local dist# = EntityDistance(Collider, I330Bowl)

	;the note is impossible not to read - even from the wrong side
	If dist < 2.2 And (Not I330NoteShown) Then
		I330NoteShown = True
		If EntityInView(I330Bowl, Camera) Then
			Msg = "A handwritten note is taped to the side of the bowl: " + Chr(34) + "take no more than two, please!!" + Chr(34)
		Else
			Msg = "You can't see the note on the bowl from here, but you know exactly what it says: " + Chr(34) + "take no more than two, please!!" + Chr(34)
		EndIf
		MsgTimer = 70*5
	ElseIf dist > 4.0 Then
		I330NoteShown = False
	EndIf

	If IndevAimedAt(I330Bowl, I330Pick, 1.8) And KillTimer >= 0 Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			I330TakeCandy()
		EndIf
	EndIf
End Function

;true when the player is close and actually looking at the bowl (pitch included - it sits low on a table)
Function I330Aimed%()
	If EntityDistance(Camera, I330Bowl) > 1.7 Then Return False
	If InvOpen Or OtherOpen <> Null Or SelectedItem <> Null Then Return False
	Local p% = EntityPick(Camera, 1.7)
	If p <> 0 And (p = I330Bowl Or p = I330Pick) Then Return True
	;fallback: the camera's forward vector points within ~20 degrees of the bowl
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dx# = EntityX(I330Pick, True) - EntityX(Camera, True)
	Local dy# = EntityY(I330Pick, True) - EntityY(Camera, True)
	Local dz# = EntityZ(I330Pick, True) - EntityZ(Camera, True)
	Local l# = Sqr(dx * dx + dy * dy + dz * dz)
	If l < 0.001 Then Return True
	Return ((fx * dx + fy * dy + fz * dz) / l > 0.94)
End Function

Function I330TakeCandy()
	If I330NoHands Then
		Msg = "You stare at the bowl. You have nothing left to take it with."
		MsgTimer = 70*4
		Return
	EndIf

	I330Taken = I330Taken + 1
	If I330Taken = 1 Then I330Reset = 70*60*10

	If I330Taken > 2 Then
		I330Sever()
		Return
	EndIf

	Local flavour$
	Select Rand(1,4)
		Case 1 flavour = "candy330_cherry"
		Case 2 flavour = "candy330_lemon"
		Case 3 flavour = "candy330_apple"
		Default flavour = "candy330_grape"
	End Select
	Local it.Items = CreateItem(flavour, EntityX(I330Bowl, True), EntityY(I330Bowl, True) + 0.15, EntityZ(I330Bowl, True))
	PickItem(it)
	If I330Taken = 1 Then
		Msg = "You take a piece of candy from the bowl."
	Else
		Msg = "You take a second piece. The note seems to be looking at you."
	EndIf
	MsgTimer = 70*4
End Function

Function I330Sever()
	I330NoHands = True
	I330Taken = 0 : I330Reset = 0
	Injuries = Injuries + 1.6
	Bloodloss = Min(Bloodloss + 40, 90)
	CameraShake = 3
	BlurTimer = 70*6
	PlaySound_Strict(DamageSFX(Rand(0, 1)))

	Local de.Decals = CreateDecal(3, EntityX(I330Bowl, True), EntityY(I330Bowl, True) + 0.005, EntityZ(I330Bowl, True), 90, Rand(360), 0)
	de\Size = 0.35 : ScaleSprite(de\obj, de\Size, de\Size)
	de = CreateDecal(3, EntityX(Collider), EntityY(Collider) - 0.3, EntityZ(Collider), 90, Rand(360), 0)
	de\Size = 0.5 : ScaleSprite(de\obj, de\Size, de\Size)

	Msg = "You reach for a third piece. There is no pain at first - only the sight of your hands lying on the table, one of them still holding the candy."
	MsgTimer = 70*8
End Function

;eating a piece: a small, flavoured sugar rush
Function IndevEatCandy330(name$)
	Stamina = Min(Stamina + 35, 100)
	StaminaEffect = Min(StaminaEffect, 0.8) : StaminaEffectTimer = Max(StaminaEffectTimer, 60)
	Select name
		Case "candy330_cherry"
			Injuries = Max(0, Injuries - 0.2)
			Msg = "Cherry. Sweet, a little tart. Your aches feel a little further away."
		Case "candy330_lemon"
			BlinkEffect = 0.8 : BlinkEffectTimer = 60
			Msg = "Lemon, so sour your eyes water. At least they won't dry out any time soon."
		Case "candy330_apple"
			Stamina = 100
			Msg = "Green apple. A jolt of sugar goes straight to your legs."
		Default
			Bloodloss = Max(0, Bloodloss - 10)
			BlurTimer = 0
			Msg = "Grape. It tastes exactly like being a kid on Halloween."
	End Select
	MsgTimer = 70*5
End Function
