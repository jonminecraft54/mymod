;=====================================================================
; SCP: Containment Breach - Indev "Annex" rooms
;
;   Six rooms built from reference shots (meshes + baked lightmaps are
;   generated, see Changelog). Every room has a reason to go in:
;
;   room2catwalk   LCZ  Service Atrium 2-C. A bridge over the hall, a lift
;                       up to it, the Upper Store behind a Level 2 door.
;                       SCP-079 recalls the lift once while you are up there.
;   room2cmaint    LCZ  Maintenance corner. Electrical Centre (Level 2):
;                       respirators for the vent core, and the sector relay
;                       lever that keeps SCP-079 quiet for a few minutes.
;   room2ventcore  HCZ  Ventilation Core / SCP-015 annex. Black particulate
;                       blocks the hall until the extraction fan is started
;                       (or you wear a mask). The pipes answer the fan.
;   room2archive   EZ   Records Annex 3-C. Dr. Imre, the SCP-055 file.
;   room2overlook  EZ   Lower Gallery. Lift down to the pit, a body on a
;                       corrosion patch, and what made the patch.
;   room1whitedoor EZ   SCP-055. The white door. Two visits per person.
;
;   Nothing here needs a new global: entity handles live in r\Objects[],
;   r\RoomDoors[] and r\NPC[] (the save restores those), progress lives in
;   the room's event (EventState / EventState2 / EventState3 / EventStr).
;   Coordinates are room units measured on the generated meshes.
;=====================================================================

;---------------------------------------------------------------------
; shared helpers
;---------------------------------------------------------------------

Function IAxItem.Items(r.Rooms, name$, lx#, ly#, lz#)
	Local it.Items = CreateItem(name, r\x + lx * RoomScale, r\y + (ly + 16.0) * RoomScale, r\z + lz * RoomScale)
	EntityParent(it\collider, r\obj)
	Return it
End Function

Function IAxPivot%(r.Rooms, lx#, ly#, lz#)
	Local p% = CreatePivot()
	PositionEntity(p, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
	EntityParent(p, r\obj)
	Return p
End Function

;the player in room units: read TFormedX() / TFormedY() / TFormedZ() afterwards
Function IAxLocal(r.Rooms)
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, r\obj)
End Function

;elevator between two stops. Both doors sit in walls that run along z (door angle 90).
;RoomDoors[0] / Objects[0] = the stop that starts open, RoomDoors[1] / Objects[1] = the other one.
;moves a lift made by IAxElevator: call it every frame from the room's event while the player is in the room.
;The lift keeps its state in EventState2, so a lift room's own code must not use EventState2.
;a door's buttons onto the face of the wall it is in. The game puts them 0.1 in front of and behind the door,
;which is inside the 64-unit walls of the side rooms. From 0.6 out, a short ray back toward the door finds the
;wall's face and the button goes just in front of it; if nothing is hit the button stays where it was.
Function IndevButtonsToWall(d.Doors)
	Local i%, b%, nx#, nz#, l#, fx#, fz#, bx#, by#, bz#, side#, dot#
	If d = Null Then Return
	If d\frameobj = 0 Then Return
	TFormVector(0, 0, 1, d\frameobj, 0)
	nx = TFormedX() : nz = TFormedZ()
	l = Sqr(nx * nx + nz * nz)
	If l < 0.0001 Then Return
	nx = nx / l : nz = nz / l
	fx = EntityX(d\frameobj, True) : fz = EntityZ(d\frameobj, True)
	For i = 0 To 1
		b = d\buttons[i]
		If b <> 0 Then
			bx = EntityX(b, True) : by = EntityY(b, True) : bz = EntityZ(b, True)
			dot = (bx - fx) * nx + (bz - fz) * nz
			side = 1 : If dot < 0 Then side = -1
			EntityPickMode(b, 0)
			If LinePick(bx - dot * nx + side * 0.6 * nx, by, bz - dot * nz + side * 0.6 * nz, -side * 0.6 * nx, 0, -side * 0.6 * nz) <> 0 Then
				PositionEntity(b, PickedX() + side * 0.012 * nx, by, PickedZ() + side * 0.012 * nz, True)
			EndIf
			EntityPickMode(b, 2)
		EndIf
	Next
End Function

Function IndevLiftTick(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If r\RoomDoors[0] = Null Or r\RoomDoors[1] = Null Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
End Function

Function IAxElevator(r.Rooms, ax#, ay#, az#, apx#, apy#, apz#, bx#, by#, bz#, bpx#, bpy#, bpz#)
	Local i%, k%
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + ax * RoomScale, r\y + ay * RoomScale, r\z + az * RoomScale, 90, r, True, 3)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = True
	r\RoomDoors[1] = CreateDoor(r\zone, r\x + bx * RoomScale, r\y + by * RoomScale, r\z + bz * RoomScale, 90, r, False, 3)
	r\RoomDoors[1]\AutoClose = False : r\RoomDoors[1]\open = False
	;call buttons: 128 units along the wall from the door centre, on both faces of the wall
	For k = 0 To 1
		Local dz# = az
		If k = 1 Then dz = bz
		For i = 0 To 1
			PositionEntity(r\RoomDoors[k]\buttons[i], EntityX(r\RoomDoors[k]\buttons[i], True), EntityY(r\RoomDoors[k]\buttons[i], True), r\z + (dz + 128.0) * RoomScale, True)
		Next
		IndevButtonsToWall(r\RoomDoors[k])
	Next
	r\Objects[0] = IAxPivot(r, apx, apy, apz)
	r\Objects[1] = IAxPivot(r, bpx, bpy, bpz)
End Function

;lever: base in Objects[slot], handle in Objects[slot + 1]. baseYaw 0 = on a wall that faces -z,
;90 = faces +x, 180 = faces +z (same convention as the other Indev rooms).
Function IAxLever(r.Rooms, slot%, lx#, ly#, lz#, baseYaw#, up%)
	Local i%
	r\Objects[slot] = CopyEntity(LeverBaseOBJ)
	r\Objects[slot + 1] = CopyEntity(LeverOBJ)
	For i = 0 To 1
		ScaleEntity(r\Objects[slot + i], 0.04, 0.04, 0.04)
		PositionEntity(r\Objects[slot + i], r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
		EntityParent(r\Objects[slot + i], r\obj)
	Next
	RotateEntity(r\Objects[slot], 0, baseYaw, 0)
	If up Then
		RotateEntity(r\Objects[slot + 1], 80, baseYaw + 180, 0)
	Else
		RotateEntity(r\Objects[slot + 1], -80, baseYaw + 180, 0)
	EndIf
	EntityPickMode(r\Objects[slot + 1], 1, False)
	EntityRadius(r\Objects[slot + 1], 0.1)
	r\Levers[0] = r\Objects[slot + 1] ;so the save keeps its position
End Function

;a fan rotor (indev_fan.b3d spins round its local z, indev_ceilfan.b3d round its local y)
Function IAxFan%(r.Rooms, file$, lx#, ly#, lz#, radius#, yaw#)
	Local f% = LoadMesh_Strict(file)
	ScaleEntity(f, radius * RoomScale, radius * RoomScale, radius * RoomScale)
	PositionEntity(f, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
	EntityParent(f, r\obj)
	RotateEntity(f, 0, yaw, 0)
	EntityFX(f, 16)
	Return f
End Function

;staff NPC on the Class-D body with one of the Indev skins
Function IAxSkin(n.NPCs, file$)
	If n = Null Then Return
	If n\texture = file Then Return
	Local tex% = LoadTexture_Strict(file)
	EntityTexture(n\obj, tex)
	FreeTexture(tex)
	n\texture = file
End Function

Function IAxSpawn.NPCs(r.Rooms, lx#, ly#, lz#, skin$)
	TFormPoint(lx, ly + 40.0, lz, r\obj, 0)
	Local n.NPCs = CreateNPC(NPCtypeD, TFormedX(), TFormedY() + 0.3, TFormedZ())
	n\State = 0 : n\State2 = 0
	RotateEntity(n\Collider, 0, EntityYaw(r\obj, True), 0)
	IAxSkin(n, skin)
	Return n
End Function

Function IAxFace(n.NPCs, ent%)
	If n = Null Then Return
	n\State = 0
	Local dx# = EntityX(ent, True) - EntityX(n\Collider, True), dz# = EntityZ(ent, True) - EntityZ(n\Collider, True)
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
End Function

Function IAxSay(who$, txt$, secs#)
	Msg = who + ": " + Chr(34) + txt + Chr(34)
	MsgTimer = 70 * secs
End Function

Function IAxFlag%(e.Events, f$)
	Return Instr(e\EventStr, f) > 0
End Function

Function IAxSetFlag(e.Events, f$)
	If Instr(e\EventStr, f) = 0 Then e\EventStr = e\EventStr + f
End Function

;keypad code of the SCP-055 chamber: follows the run's access code, so it is different every game
Function Indev055Code%()
	Local c% = (AccessCode * 5 + 550) Mod 10000
	If c < 1000 Then c = c + 1000
	If c = AccessCode Or c = HARPCODE Or c = Indev914Code() Or c = Indev268Code() Then c = c + 7
	Return c
End Function

;=====================================================================
; room2catwalk - Service Atrium 2-C
;   Objects: 0 lower lift pivot, 1 upper lift pivot, 2 duct fan
;   EventState2 lift, EventState3 SCP-079 recall timer, EventStr "b" = recall happened
;=====================================================================

Function IndevFillCatwalk(r.Rooms)
	Local d.Doors
	IAxElevator(r, 440.0, 0.0, -448.0, 744.0, 240.0, -448.0, 440.0, 352.0, 448.0, 744.0, 592.0, 448.0)

	;the Upper Store, Level 2
	d = CreateDoor(r\zone, r\x - 448.0 * RoomScale, r\y + 352.0 * RoomScale, r\z, 90, r, False, False, 2)
	d\AutoClose = False : d\open = False

	r\Objects[2] = IAxFan(r, "GFX\map\indev_fan.b3d", -456.0, 528.0, -480.0, 70.0, 90)

	IAxItem(r, "docatrium", 300.0, 0.0, -250.0)
	IAxItem(r, "bat", -952.0, 450.0, -160.0)
	IAxItem(r, "eyedrops", -952.0, 520.0, 160.0)
	IAxItem(r, "firstaid", -710.0, 450.0, 284.0)
	IAxItem(r, "radio", -700.0, 428.0, -64.0)
End Function

Function UpdateIndevCatwalk(e.Events)
	Local r.Rooms = e\room
	If r\Objects[2] <> 0 And r\dist < 12.0 Then TurnEntity(r\Objects[2], 0, 0, 5.0 * FPSfactor)
	If PlayerRoom <> r Then Return

	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)

	If e\EventState3 > 0 Then
		;SCP-079 is holding the lift
		e\EventState3 = e\EventState3 - FPSfactor
		r\RoomDoors[0]\locked = True : r\RoomDoors[1]\locked = True
		If Rand(260) = 1 Then LightBlink = Max(LightBlink, Rnd(0.4, 1.2))
		If e\EventState3 <= 0 Then
			e\EventState3 = 0
			PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
			Msg = "The call panels light up again. Whatever was holding the lift has let go of it."
			MsgTimer = 70 * 6
		EndIf
	ElseIf Not IAxFlag(e, "b") Then
		;first time out on the middle of the bridge
		IAxLocal(r)
		If TFormedY() > 300.0 And Abs(TFormedX()) < 150.0 And Abs(TFormedZ()) < 110.0 Then
			IAxSetFlag(e, "b")
			e\EventState3 = 70 * 28
			LightBlink = 4.0
			PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
			Msg = "Intercom: " + Chr(34) + "Service lift 2-C recalled. You were not expected on the bridge." + Chr(34)
			MsgTimer = 70 * 7
			IndevStress = Min(100, IndevStress + 12)
		EndIf
	EndIf
End Function

;=====================================================================
; room2cmaint - maintenance corner, Electrical Centre 2-C
;   Objects: 0 lever base, 1 lever handle
;   EventState relay cooldown, EventState2 1 = the lever was up last frame
;=====================================================================

Function IndevFillCMaint(r.Rooms)
	Local d.Doors
	d = CreateDoor(r\zone, r\x, r\y, r\z + 224.0 * RoomScale, 0, r, False, False, 2)
	d\AutoClose = False : d\open = False
	d = CreateDoor(r\zone, r\x - 224.0 * RoomScale, r\y, r\z - 400.0 * RoomScale, 90, r, False, False)
	d\AutoClose = False : d\open = False

	IAxLever(r, 0, 0.0, 190.0, 791.0, 0, True)

	IAxItem(r, "gasmask", -374.0, 101.0, 380.0)
	IAxItem(r, "bat", -374.0, 101.0, 520.0)
	IAxItem(r, "18vbat", -374.0, 175.0, 600.0)
	IAxItem(r, "docmaint", 325.0, 80.0, 340.0)
	If Rand(2) = 1 Then IAxItem(r, "eyedrops", -600.0, 101.0, -520.0)
	If Rand(2) = 1 Then IAxItem(r, "firstaid", -405.0, 144.0, -555.0)
	IAxItem(r, "bat", -600.0, 175.0, -300.0)
End Function

Function UpdateIndevCMaint(e.Events)
	Local r.Rooms = e\room
	If e\EventState > 0 Then e\EventState = Max(0, e\EventState - FPSfactor)
	If PlayerRoom <> r Then Return
	If r\Objects[1] = 0 Then Return

	Local up% = UpdateLever(r\Objects[1])
	If e\EventState2 = 0 And up Then
		e\EventState2 = 1
	ElseIf e\EventState2 = 1 And (Not up) Then
		;pulled down: the sector's remote relays drop out
		e\EventState2 = 0
		If e\EventState <= 0 Then
			e\EventState = 70 * 60 * 4
			Indev079Timer = Max(Indev079Timer, 70 * 60 * 6)
			LightBlink = 1.5
			PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
			Msg = "The relay bank drops out with a bang. For a few minutes nothing in the control room can reach this sector."
			MsgTimer = 70 * 7
			IndevRelieveStress(10)
		Else
			Msg = "The relays are still out. Pulling the lever again does nothing until they re-arm."
			MsgTimer = 70 * 5
		EndIf
	EndIf
End Function

;=====================================================================
; room2ventcore - Ventilation Core / SCP-015 annex
;   Objects: 0 fan, 1 lever base, 2 lever handle, 3 valve wheel, 4-6 smoke sources,
;            7 burst joint, 8-10 lockers, 11 Halloran's spot
;   NPC[0]: Halloran
;   EventState 0 fan tripped (smoke), 1 spinning up (the pipes answer), 2 running (clear)
;   EventState2 fan speed, EventState3 spin-up timer
;   EventStr: "v" wheel turned, "a" "b" "c" lockers opened, "1".."4" Halloran's lines, "t" thanks
;=====================================================================

Function IndevFillVentCore(r.Rooms)
	Local base%, w%, hub%, spoke%
	r\Objects[0] = IAxFan(r, "GFX\map\indev_fan.b3d", -790.0, 320.0, 0.0, 150.0, 90)
	IAxLever(r, 1, -440.0, 190.0, -439.0, 180, False)

	;the red hand wheel on stub 7 (it turns round the stub, which runs along x)
	base = CreatePivot()
	w = CreateCylinder(16, True, base)
	ScaleEntity(w, 0.11, 0.016, 0.11)
	EntityColor(w, 150, 20, 15)
	EntityShininess(w, 0.4)
	hub = CreateCylinder(8, True, w)
	ScaleEntity(hub, 0.3, 1.8, 0.3)
	EntityColor(hub, 60, 60, 60)
	spoke = CreateCube(w)
	ScaleEntity(spoke, 0.95, 0.6, 0.07)
	EntityColor(spoke, 120, 15, 10)
	spoke = CreateCube(w)
	ScaleEntity(spoke, 0.07, 0.6, 0.95)
	EntityColor(spoke, 120, 15, 10)
	PositionEntity(base, r\x + 532.0 * RoomScale, r\y + 178.0 * RoomScale, r\z - 200.0 * RoomScale, True)
	RotateEntity(base, 0, 0, 90, True)
	EntityPickMode(w, 2)
	EntityParent(base, r\obj)
	r\Objects[3] = w

	r\Objects[4] = IAxPivot(r, 330.0, 30.0, 200.0)
	r\Objects[5] = IAxPivot(r, 420.0, 230.0, 60.0)
	r\Objects[6] = IAxPivot(r, 520.0, 40.0, -60.0)
	r\Objects[7] = IAxPivot(r, 470.0, 190.0, 60.0)
	r\Objects[8] = IAxPivot(r, -226.0, 150.0, -720.0)
	r\Objects[9] = IAxPivot(r, 226.0, 150.0, -720.0)
	r\Objects[10] = IAxPivot(r, 226.0, 150.0, 720.0)
	r\Objects[11] = IAxPivot(r, -540.0, 0.0, 150.0)

	IAxItem(r, "doc015", -380.0, 80.0, 370.0)
	IAxItem(r, "doc015b", -300.0, 80.0, 370.0)
End Function

;black particulate: a few slow dark puffs round the leaking stub
Function IAxSmoke(r.Rooms, amount#)
	Local p.Particles, src%, i%
	If Rand(100) > Int(amount * 34.0) Then Return
	src = r\Objects[4 + Rand(0, 2)]
	If src = 0 Then Return
	p = CreateParticle(EntityX(src, True) + Rnd(-0.5, 0.5), EntityY(src, True) + Rnd(0.0, 0.3), EntityZ(src, True) + Rnd(-0.5, 0.5), 0, Rnd(0.35, 0.6), -0.03, 300)
	p\speed = Rnd(0.001, 0.004)
	p\SizeChange = 0.004
	p\Achange = -0.0032
	p\A = 0.9
	EntityColor(p\obj, 14, 13, 13)
	EntityAlpha(p\obj, p\A)
	RotateEntity(p\pvt, Rnd(-70, -20), Rnd(360), 0)
End Function

;a jet out of the joint on stub 7
Function IAxBurst(r.Rooms, src%, hurt#)
	Local j%, pp.Particles
	Local px# = EntityX(src, True), py# = EntityY(src, True), pz# = EntityZ(src, True)
	For j = 0 To 9
		pp = CreateParticle(px + Rnd(-0.15, 0.15), py + Rnd(-0.1, 0.2), pz + Rnd(-0.15, 0.15), 0, Rnd(0.15, 0.3), -0.2, 150)
		pp\speed = Rnd(0.006, 0.016) : pp\SizeChange = 0.012 : pp\Achange = -0.007
		EntityColor(pp\obj, 30, 26, 22)
		RotateEntity(pp\pvt, Rnd(-30, 20), Rnd(360), 0)
	Next
	PlaySound2(HissSFX, Camera, src, 8.0)
	If EntityDistance(Collider, src) < 1.5 Then
		Injuries = Injuries + hurt
		BlurTimer = 70 * 3
		CameraShake = Max(CameraShake, 1.2)
		Msg = "Something hot and black hits you from the pipe joint. Get clear of the stub."
		MsgTimer = 70 * 4
	EndIf
End Function

Function UpdateIndevVentCore(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, it.Items, i%, d#

	;the fan turns whether or not anyone is in the room
	If e\EventState >= 1 Then
		e\EventState2 = CurveValue(9.0, e\EventState2, 120.0)
	Else
		e\EventState2 = CurveValue(0.0, e\EventState2, 90.0)
	EndIf
	If r\dist < 12.0 Then
		If r\Objects[0] <> 0 Then
			TurnEntity(r\Objects[0], 0, 0, e\EventState2 * FPSfactor)
			If e\EventState2 > 0.3 Then r\SoundCHN = LoopSound2(RoomAmbience[9], r\SoundCHN, Camera, r\Objects[0], 7.0, e\EventState2 / 9.0)
		EndIf
		If e\EventState = 0 Then
			IAxSmoke(r, 1.0)
		ElseIf e\EventState = 1 Then
			IAxSmoke(r, Max(0.0, e\EventState3 / (70.0 * 14.0)))
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	IAxLocal(r)
	Local lx# = TFormedX(), lz# = TFormedZ()

	;---- the particulate: everything east of the piers, until the fan has cleared it
	If e\EventState < 2 And lx > -130.0 And Abs(lz) < 340.0 Then
		If WearingGasMask = 0 And WearingHazmat = 0 Then
			Injuries = Injuries + 0.0007 * FPSfactor
			BlurTimer = Max(BlurTimer, 70 * 4)
			Stamina = Max(0, Stamina - 0.12 * FPSfactor)
			IndevStress = Min(100, IndevStress + 0.02 * FPSfactor)
			If Rand(110) = 1 Then
				If CoughCHN = 0 Then
					CoughCHN = PlaySound_Strict(CoughSFX(Rand(0, 2)))
				ElseIf Not ChannelPlaying(CoughCHN) Then
					CoughCHN = PlaySound_Strict(CoughSFX(Rand(0, 2)))
				EndIf
			EndIf
			If Not IAxFlag(e, "s") Then
				IAxSetFlag(e, "s")
				Msg = "The black dust is in your eyes and throat at once. You cannot stay in this without a respirator."
				MsgTimer = 70 * 6
			EndIf
		EndIf
	EndIf

	;---- the start lever
	Local up% = UpdateLever(r\Objects[2])
	Select e\EventState
		Case 0
			If up Then
				e\EventState = 1
				e\EventState3 = 70 * 14
				PlaySound2(LoadTempSound("SFX\ambient\Room ambience\FanOn.ogg"), Camera, r\Objects[0], 10.0)
				Msg = "The extraction fan shudders and starts to turn. Somewhere in the pipes, something knocks back."
				MsgTimer = 70 * 6
			EndIf
		Case 1
			;SCP-015 answers the fan: the joint on stub 7 spits every second or so
			e\EventState3 = e\EventState3 - FPSfactor
			If Rand(75) = 1 Then IAxBurst(r, r\Objects[7], 0.14)
			If Rand(300) = 1 Then LightBlink = Max(LightBlink, Rnd(0.3, 0.9))
			If e\EventState3 <= 0 Then
				e\EventState = 2
				Msg = "The air clears from the west side first. The pipes knock twice more and go quiet."
				MsgTimer = 70 * 6
				IndevRelieveStress(15)
			EndIf
		Case 2
			If Not up Then
				e\EventState = 0
				PlaySound2(LoadTempSound("SFX\ambient\Room ambience\FanOff.ogg"), Camera, r\Objects[0], 10.0)
				Msg = "The fan winds down. Within a breath the stub is venting again."
				MsgTimer = 70 * 5
			EndIf
	End Select

	;---- the red wheel (Addendum 015-B)
	If r\Objects[3] <> 0 Then
		If IndevAimedAt(r\Objects[3], r\Objects[3], 1.3) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				If Not IAxFlag(e, "v") Then
					IAxSetFlag(e, "v")
					TurnEntity(r\Objects[3], 0, 70, 0)
					PlaySound2(LeverSFX, Camera, r\Objects[3], 3.0)
					PlaySound_Strict(LoadTempSound("SFX\Room\TunnelBurst.ogg"))
					IAxBurst(r, r\Objects[3], 0.45)
					CameraShake = 3.0
					IndevStress = Min(100, IndevStress + 20)
					Msg = "You turn the red wheel a quarter-turn. The pipe turns it back, and answers."
					MsgTimer = 70 * 6
				Else
					Msg = "The wheel will not move again. It is warm."
					MsgTimer = 70 * 4
				EndIf
			EndIf
		EndIf
	EndIf

	;---- the tunnel lockers
	For i = 0 To 2
		If r\Objects[8 + i] <> 0 Then
			If (Not IAxFlag(e, Chr(97 + i))) And IndevAimedAt(r\Objects[8 + i], r\Objects[8 + i], 1.1) Then
				DrawHandIcon = True
				If MouseHit1 Then
					MouseHit1 = False
					IAxSetFlag(e, Chr(97 + i))
					PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
					TFormPoint(EntityX(r\Objects[8 + i], True), EntityY(r\Objects[8 + i], True), EntityZ(r\Objects[8 + i], True), 0, r\obj)
					Local ix# = TFormedX() * 0.72, iz# = TFormedZ()
					Select i
						Case 0
							it = IAxItem(r, "bat", ix, 10.0, iz)
							Msg = "The locker door swings out. A battery rolls off the shelf."
						Case 1
							it = IAxItem(r, "key3", ix, 10.0, iz)
							Msg = "Halloran's locker. A Level 3 card on a lanyard drops out of a boot."
						Case 2
							it = IAxItem(r, "firstaid", ix, 10.0, iz)
							Msg = "The locker door swings out. Someone kept a first-aid kit in here."
					End Select
					MsgTimer = 70 * 5
				EndIf
			EndIf
		EndIf
	Next

	;---- Halloran, the plant technician, on the west side
	n = r\NPC[0]
	If n = Null Then
		n = IAxSpawn(r, -540.0, 0.0, 150.0, "GFX\npcs\indev_tech.jpg")
		r\NPC[0] = n
	EndIf
	IAxSkin(n, "GFX\npcs\indev_tech.jpg")
	d = EntityDistance(n\Collider, Collider)
	If d < 6.0 Then
		IAxFace(n, Collider)
	Else
		n\State = 0
	EndIf
	If d < 2.6 And MsgTimer <= 0 Then
		If e\EventState = 2 Then
			If Not IAxFlag(e, "t") Then
				IAxSetFlag(e, "t")
				IAxSay("Halloran", "That's it running. My card's in the locker by the south door, right-hand side. Take it - I'm not walking past that thing.", 8)
			EndIf
		ElseIf Not IAxFlag(e, "1") Then
			IAxSetFlag(e, "1")
			IAxSay("Halloran", "Mask on if you've got one. That black stuff is coming off the pipes, not the vents.", 6)
		ElseIf Not IAxFlag(e, "2") Then
			IAxSetFlag(e, "2")
			IAxSay("Halloran", "Fan tripped when the lockdown hit. Start lever's on the south wall, left of the tunnel. Shove it right up.", 7)
		ElseIf Not IAxFlag(e, "3") Then
			IAxSetFlag(e, "3")
			IAxSay("Halloran", "When it spins up the pipes spit. Stay this side of the piers till it stops.", 6)
		ElseIf Not IAxFlag(e, "4") Then
			IAxSetFlag(e, "4")
			IAxSay("Halloran", "And don't touch the red wheel. We didn't fit it.", 5)
		EndIf
	EndIf
End Function

;=====================================================================
; room2archive - Records Annex 3-C
;   Objects: 0 ceiling fan, 1 Dr. Imre's spot      NPC[0]: Dr. Imre
;   EventState line counter, EventState3 pause between lines
;=====================================================================

Function IndevFillArchive(r.Rooms)
	r\Objects[0] = IAxFan(r, "GFX\map\indev_ceilfan.b3d", 576.0, 336.0, 0.0, 150.0, 0)
	r\Objects[1] = IAxPivot(r, 760.0, 0.0, 0.0)
	IAxItem(r, "doc055", 236.0, 109.0, -180.0)
	IAxItem(r, "bat", 580.0, 180.0, 300.0)
	IAxItem(r, "eyedrops", 760.0, 109.0, -668.0)
End Function

Function UpdateIndevArchive(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, d#
	If r\Objects[0] <> 0 And r\dist < 10.0 Then TurnEntity(r\Objects[0], 0, 2.2 * FPSfactor, 0)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	n = r\NPC[0]
	If n = Null Then
		n = IAxSpawn(r, 760.0, 0.0, 0.0, "GFX\npcs\indev_archivist.jpg")
		r\NPC[0] = n
	EndIf
	IAxSkin(n, "GFX\npcs\indev_archivist.jpg")
	d = EntityDistance(n\Collider, Collider)
	If d < 7.0 Then
		IAxFace(n, Collider)
	Else
		n\State = 0
	EndIf

	If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
	If d < 2.8 And e\EventState3 <= 0 And e\EventState < 6 Then
		Select e\EventState
			Case 0 IAxSay("Dr. Imre", "Don't - I'm not armed. I'm Records. I only file things.", 5)
			Case 1 IAxSay("Dr. Imre", "The east stacks are still in order. I can't say the same for the Lower Gallery. Vasko went down there. I heard the lift come back up empty.", 8)
			Case 2 IAxSay("Dr. Imre", "There's a number on my hand again. I copied it onto a slip in my office - Lower Gallery corridor, the only office door.", 7)
			Case 3 IAxSay("Dr. Imre", "It opens the white chamber, I think. I don't remember what is in it. Nobody does. That is rather the point of it.", 7)
			Case 4 IAxSay("Dr. Imre", "If you go in, the file says you'll come out holding a note. Believe the note. And count your visits - two. Not three.", 8)
			Case 5 IAxSay("Dr. Imre", "I'll be here. Somebody has to know where everything is.", 5)
		End Select
		e\EventState = e\EventState + 1
		e\EventState3 = MsgTimer + 70
	EndIf
End Function

;=====================================================================
; room2overlook - Lower Gallery
;   Objects: 0 corridor lift pivot, 1 pit lift pivot, 2 the body's spot    NPC[0]: Dr. Vasko's body
;   EventState 0 untouched, 1 body placed, 2 SCP-106 is coming up, 3 over
;   EventState2 lift, EventState3 delay before SCP-106 surfaces
;=====================================================================

Function IndevFillOverlook(r.Rooms)
	Local d.Doors
	IAxElevator(r, -216.0, 0.0, 400.0, -520.0, 240.0, 400.0, -216.0, -448.0, -400.0, -520.0, -208.0, -400.0)

	d = CreateDoor(r\zone, r\x - 224.0 * RoomScale, r\y, r\z - 400.0 * RoomScale, 90, r, False, False)
	d\AutoClose = False : d\open = False

	r\Objects[2] = IAxPivot(r, 470.0, -448.0, 250.0)

	IAxItem(r, "note055", -650.0, 80.0, -390.0)
	IAxItem(r, "docgallery", -650.0, 80.0, -440.0)
	IAxItem(r, "bat", -395.0, 168.0, -176.0)
	IAxItem(r, "finefirstaid", 810.0, -340.0, -510.0)
	IAxItem(r, "eyedrops", 450.0, -368.0, -340.0)
	IAxItem(r, "nvgoggles", 420.0, -448.0, 190.0)
End Function

Function UpdateIndevOverlook(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, de.Decals, tex%
	If PlayerRoom <> r Then Return

	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	;the body on the pit floor, and the patch it is lying on
	If e\EventState = 0 Then
		n = CreateNPC(NPCtypeD, EntityX(r\Objects[2], True), EntityY(r\Objects[2], True) + 0.5, EntityZ(r\Objects[2], True))
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 130, 0)
		n\State = 3
		SetNPCFrame(n, 19)
		n\IsDead = True
		r\NPC[0] = n
		de = CreateDecal(0, EntityX(r\Objects[2], True), EntityY(r\Objects[2], True) + 0.005, EntityZ(r\Objects[2], True), 90, Rand(360), 0)
		de\Size = 0.55
		ScaleSprite(de\obj, de\Size, de\Size)
		EntityParent(de\obj, r\obj)
		e\EventState = 1
	EndIf
	If r\NPC[0] <> Null Then IAxSkin(r\NPC[0], "GFX\npcs\body1.jpg")

	IAxLocal(r)
	Local ly# = TFormedY()
	Select e\EventState
		Case 1
			If ly < -250.0 And EntityDistance(Collider, r\Objects[2]) < 1.5 Then
				e\EventState = 2
				e\EventState3 = 70 * 4
				LightBlink = 5.0
				PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
				IndevStress = Min(100, IndevStress + 15)
				Msg = "The stain under the body is wet. It is wider than it was when you came down."
				MsgTimer = 70 * 6
			EndIf
		Case 2
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 Then
				e\EventState = 3
				If Curr106 <> Null And (Not Contained106) Then
					If Curr106\State > 0 Then
						PositionEntity(Curr106\Collider, EntityX(r\Objects[2], True), EntityY(r\Objects[2], True), EntityZ(r\Objects[2], True))
						ResetEntity(Curr106\Collider)
						Curr106\State = -0.1
						ShowEntity(Curr106\obj)
					EndIf
				EndIf
			EndIf
	End Select
End Function

;=====================================================================
; room1whitedoor - SCP-055
;   RoomDoors[0]: the keypad door       Objects: 0 where you come round, 1 the white door
;   EventState visits so far, EventState2 > 0 while the white-out runs
;=====================================================================

Function IndevFillWhiteDoor(r.Rooms)
	r\RoomDoors[0] = CreateDoor(r\zone, r\x, r\y, r\z - 768.0 * RoomScale, 0, r, False, False, 0, Str(Indev055Code()))
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = False
	r\Objects[0] = IAxPivot(r, 0.0, 0.0, -600.0)
	r\Objects[1] = IAxPivot(r, 0.0, 150.0, 960.0)
End Function

Function UpdateIndevWhiteDoor(e.Events)
	Local r.Rooms = e\room
	Local it.Items
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If e\EventState2 > 0 Then
		;coming round outside, in the dark
		e\EventState2 = e\EventState2 - FPSfactor
		LightFlash = Max(LightFlash, e\EventState2 / 70.0)
		Return
	EndIf

	IAxLocal(r)
	If TFormedZ() > 906.0 And Abs(TFormedX()) < 84.0 Then
		e\EventState = e\EventState + 1
		e\EventState2 = 70 * 3
		LightFlash = 4.0
		BlinkTimer = -10
		PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))

		If e\EventState >= 3 Then
			DeathMSG = "Subject D-9341 was found seated against the far wall of an Entrance Zone chamber, facing a doorway. "
			DeathMSG = DeathMSG + "The attending staff could not agree on the cause of death, the name of the chamber, or why they had gone in to look."
			Kill()
			Return
		EndIf

		PositionEntity(Collider, EntityX(r\Objects[0], True), EntityY(r\Objects[0], True) + 0.4, EntityZ(r\Objects[0], True))
		ResetEntity(Collider)
		DropSpeed = 0
		Stamina = Min(Stamina, 20)
		IndevStress = Min(100, IndevStress + 18)
		If e\EventState = 1 Then
			it = CreateItem("note055self", EntityX(Collider), EntityY(Collider) + 0.1, EntityZ(Collider))
			EntityType(it\collider, HIT_ITEM)
			Msg = "You are standing in the dark with your back to the white door. Your legs ache. A sheet of paper slides out of your hand."
		Else
			Injuries = Injuries + 0.6
			BlurTimer = 70 * 8
			it = CreateItem("key4", EntityX(Collider), EntityY(Collider) + 0.1, EntityZ(Collider))
			EntityType(it\collider, HIT_ITEM)
			Msg = "The dark again. Your forearm is bleeding from two cuts you made yourself: a tally. Something plastic falls out of your sleeve."
		EndIf
		MsgTimer = 70 * 8
	EndIf
End Function

;a door that starts closing without a sound (events, lockdowns and scripts often set d\open = False directly instead
;of going through UseDoor, which is what plays the sound) gets the normal close sound. Doors whose own sound is
;already playing are left alone, so nothing plays twice.
Function IndevDoorCloseSound(d.Doors)
	Local was% = d\IndevWasOpen
	d\IndevWasOpen = d\open
	If (Not was) Or d\open Then Return
	If d\openstate < 150 Then Return
	If d\dist > 8.0 Then Return
	If d\SoundCHN <> 0 Then
		If ChannelPlaying(d\SoundCHN) Then Return
	EndIf
	d\SoundCHN = PlaySound2(CloseDoorSFX(Max(0, Min(d\dir, 3)), Rand(0, 2)), Camera, d\obj)
End Function
