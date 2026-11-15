;=====================================================================
; SCP: Containment Breach - Indev SCP-122
;
;   A plastic star night light plugged into a wall of the medical bay.
;   While it's powered and you're in the same room: stress melts away,
;   new stress barely builds, sanity recovers and paranoia fades.
;
;   Click it to unplug / plug it back in. It flickers now and then
;   (nobody has done the maintenance), and a facility power outage
;   (secondary lighting off) leaves it unpowered.
;=====================================================================

Global I122Obj%, I122Glow%, I122Light%, I122Room.Rooms, I122Pick%
Global I122Plugged% = True, I122Flicker#, I122NextFlicker#, I122Inside%, I122Seen%

Function Indev122Reset()
	I122Obj = 0 : I122Glow = 0 : I122Light = 0 : I122Room = Null : I122Pick = 0
	I122Plugged = True : I122Flicker = 0 : I122NextFlicker = 70*40 : I122Inside = False : I122Seen = False
End Function

;called from FillRoom with room-local coordinates of the wall surface (RoomScale units) and the yaw
;that turns the star's face away from the wall
Function IndevCreate122%(r.Rooms, lx#, ly#, lz#, yaw#)
	If I122Obj <> 0 Then Return False
	I122Room = r
	I122Obj = LoadMesh_Strict("GFX\map\Props\scp122.b3d", r\obj)
	EntityTexture(I122Obj, LoadTexture_Strict("GFX\map\Props\scp122.png", 1))
	ScaleEntity(I122Obj, 0.28, 0.28, 0.28)            ;model millimetres -> RoomScale units, a little oversized so it reads
	PositionEntity(I122Obj, lx, ly, lz, False)
	RotateEntity(I122Obj, 0, yaw, 0, False)
	EntityPickMode(I122Obj, 2)

	;(the halo sprite is made on the first frame, unparented - sprites ignore the room's tiny scale and a
	;child sprite ended up filling the whole screen; no real light either, the dynamic light washed out the room)
	Return True
End Function

Function I122SetLit(lit%)
	If I122Obj = 0 Then Return
	If lit Then
		EntityFX(I122Obj, 1)                           ;glows from inside
		EntityColor(I122Obj, 255, 255, 255)
		If I122Glow <> 0 Then ShowEntity(I122Glow)
	Else
		EntityFX(I122Obj, 0)
		EntityColor(I122Obj, 150, 165, 160)
		If I122Glow <> 0 Then HideEntity(I122Glow)
	EndIf
End Function

;powered: plugged in and the facility has power
Function I122Powered%()
	Return (I122Plugged And SecondaryLightOn > 0.3)
End Function

;true while SCP-122 is actively calming the player (Indev stress/blink code asks this)
Function Indev122Calming%()
	If I122Obj = 0 Or PlayerRoom = Null Then Return False
	Return (PlayerRoom = I122Room And I122Powered() And I122Flicker <= 0)
End Function

Function UpdateIndev122()
	If I122Obj = 0 Then Return

	;the halo pick target, made once the room has its final rotation
	If I122Pick = 0 Then
		I122Pick = CreatePivot()
		PositionEntity(I122Pick, EntityX(I122Obj, True), EntityY(I122Obj, True), EntityZ(I122Obj, True), True)
		EntityRadius(I122Pick, 0.1)
		EntityPickMode(I122Pick, 1, False)

		;small, faint teal halo just in front of the star (world units)
		TFormVector(0, 0, 1, I122Obj, 0)
		Local nx# = TFormedX(), nz# = TFormedZ(), nl# = Sqr(nx * nx + nz * nz)
		If nl > 0 Then nx = nx / nl : nz = nz / nl
		I122Glow = CreateSprite()
		PositionEntity(I122Glow, EntityX(I122Obj, True) + nx * 0.03, EntityY(I122Obj, True), EntityZ(I122Obj, True) + nz * 0.03, True)
		EntityTexture(I122Glow, LightSpriteTex(2))
		EntityBlend(I122Glow, 3)
		EntityFX(I122Glow, 1)
		EntityColor(I122Glow, 45, 120, 110)
		ScaleSprite(I122Glow, 0.12, 0.12)
		If I122Room <> Null Then EntityParent(I122Glow, I122Room\obj, True) ;hidden together with the room
		I122SetLit(I122Powered())
	EndIf

	;flickering: short dropouts every so often
	If I122Flicker > 0 Then
		I122Flicker = I122Flicker - FPSfactor
		I122SetLit(I122Powered() And (Rand(3) = 1 Or I122Flicker <= 0))
	ElseIf I122Powered() Then
		I122NextFlicker = I122NextFlicker - FPSfactor
		If I122NextFlicker <= 0 Then
			I122Flicker = 70 * Rnd(0.3, 0.9)
			I122NextFlicker = 70 * Rnd(35, 90)
		EndIf
	EndIf
	If I122Flicker <= 0 Then I122SetLit(I122Powered())

	;entering / leaving its room
	Local inside% = (PlayerRoom = I122Room)
	If inside And (Not I122Inside) Then
		If I122Powered() Then
			If Not I122Seen Then
				Msg = "A little star-shaped night light glows on the wall. Your shoulders drop. For the first time in a while, you feel safe."
				I122Seen = True
			Else
				Msg = "The star's soft light is still there. You breathe out."
			EndIf
			MsgTimer = 70*6
		EndIf
	EndIf
	I122Inside = inside

	If inside And KillTimer >= 0 Then
		If I122Powered() And I122Flicker <= 0 Then
			;comfort: sanity comes back, SCP-718's paranoia eases
			If Sanity < 0 Then Sanity = Min(0, Sanity + FPSfactor * 2.5)
			If I718Host = False And I718Sanity < 100 Then I718Sanity = Min(100, I718Sanity + FPSfactor / 70.0 * 3.0)
		EndIf

		;plug / unplug
		If IndevAimedAt(I122Obj, I122Pick, 1.8) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				I122Plugged = (Not I122Plugged)
				If I122Plugged Then
					If SecondaryLightOn > 0.3 Then
						Msg = "You push the night light back into the socket. It blinks, then glows. The room is warm again."
					Else
						Msg = "You push it back in, but there's no power. The star stays dark."
					EndIf
				Else
					Msg = "You pull the night light out of the socket. The room is suddenly much colder, and much bigger."
					IndevStress = Min(100, IndevStress + 15)
				EndIf
				MsgTimer = 70*5
				PlaySound_Strict(ButtonSFX)
			EndIf
		EndIf
	EndIf
End Function

Function I122Aimed%()
	If EntityDistance(Camera, I122Pick) > 1.5 Then Return False
	If InvOpen Or OtherOpen <> Null Or SelectedItem <> Null Then Return False
	Local p% = EntityPick(Camera, 1.5)
	If p <> 0 And (p = I122Obj Or p = I122Pick) Then Return True
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dx# = EntityX(I122Pick, True) - EntityX(Camera, True)
	Local dy# = EntityY(I122Pick, True) - EntityY(Camera, True)
	Local dz# = EntityZ(I122Pick, True) - EntityZ(Camera, True)
	Local l# = Sqr(dx * dx + dy * dy + dz * dz)
	If l < 0.001 Then Return True
	Return ((fx * dx + fy * dy + fz * dz) / l > 0.95)
End Function
