;=====================================================================
; SCP: Containment Breach - Indev "Annex" rooms, second batch (Indev zone)
;
;   room2blockhall  Containment Block D. SCP-017 hangs in a floodlit cage inside
;                   the block. Step down into the pit and the lamp circuit trips:
;                   the lamps fail one bank at a time until the fallen lever on the
;                   north wall is pushed back up. All lamps out = the pit is its shadow.
;   room1testcage   Test Chamber 4-A. SCP-131-A in a wire cage; the cage lock is the
;                   lever in the control office up the steps.
;   room2liftshaft  Maintenance Shaft 4. Freight lift down a pipe shaft with a big
;                   extractor fan at the top; SCP-131-B is hiding at the bottom.
;   room2cobserve   Observation 4-C. SCP-999 in its holding room: visit it and stress,
;                   sanity and small injuries are put right (two minute cooldown).
;   room1store4     Stores 4. Supplies, and a jammed crate to lean on.
;
;   SCP-131 "the Eye Pods" are companions: click one and it follows the trail you
;   walk. While a pod can see SCP-173, SCP-173 does not move (hook in NPCs.bb).
;   A pod blinks for about a second in every twenty, the two never together, and
;   both hide (and watch nothing) while SCP-106 is close.
;
;   Uses the helpers in IndevAnnex.bb. Handles live in r\Objects / r\RoomDoors,
;   progress in the room events. The pods cross rooms, so they are the one thing
;   that needs globals (below); whether a pod follows is the "f" flag of its home
;   room's event, so it is saved with the game.
;=====================================================================

Type I131Crumb
	Field x#, y#, z#
End Type

Global I131PodA%, I131PodB%       ;the two pod entities (kept in step with r\Objects by their rooms)
Global I131FollowA%, I131FollowB%
Global I131WarnT#, I131Fear%

Function IndevAnnex2Reset()
	Delete Each I131Crumb
	I131PodA = 0 : I131PodB = 0
	I131FollowA = False : I131FollowB = False
	I131WarnT = 0 : I131Fear = False
End Function

;---------------------------------------------------------------------
; SCP-131
;---------------------------------------------------------------------

Function IAx131Make%(r.Rooms, lx#, ly#, lz#, skin$)
	Local pod% = LoadMesh_Strict("GFX\npcs\scp131.b3d")
	Local s# = 78.0 * RoomScale
	If skin <> "" Then
		Local tex% = LoadTexture_Strict(skin)
		EntityTexture(pod, tex)
		FreeTexture(tex)
	EndIf
	ScaleEntity(pod, s, s, s)
	PositionEntity(pod, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
	EntityParent(pod, r\obj)
	RotateEntity(pod, 0, 180, 0)
	EntityPickMode(pod, 1, False)
	EntityRadius(pod, 0.14)
	Return pod
End Function

;put a pod back where it lives (new game state after a quick-load, or it never left)
Function IAx131Home(pod%, r.Rooms, lx#, ly#, lz#)
	If pod = 0 Then Return
	If GetParent(pod) = r\obj Then Return
	If GetParent(pod) <> 0 Then EntityParent(pod, 0)
	TFormPoint(lx, ly, lz, r\obj, 0)
	PositionEntity(pod, TFormedX(), TFormedY(), TFormedZ(), True)
	EntityParent(pod, r\obj)
	RotateEntity(pod, 0, 180, 0)
End Function

;can this pod see the entity right now? phase offsets the blink so the two never blink together
Function IAx131Sees%(pod%, ent%, phase%)
	If pod = 0 Or ent = 0 Then Return False
	If I131Fear Then Return False
	If ((MilliSecs() + phase) Mod 20000) < 1100 Then Return False
	If EntityDistance(pod, ent) > 8.0 Then Return False
	Local pv% = CreatePivot()
	PositionEntity(pv, EntityX(pod, True), EntityY(pod, True) + 0.2, EntityZ(pod, True))
	Local vis% = EntityVisible(pv, ent)
	FreeEntity(pv)
	Return vis
End Function

;called by SCP-173's update: True = a pod is watching it, it may not move
Function Indev131Watches%(n.NPCs)
	If n = Null Then Return False
	If I131PodA <> 0 Then
		If IAx131Sees(I131PodA, n\Collider, 0) Then Return True
	EndIf
	If I131PodB <> 0 Then
		If IAx131Sees(I131PodB, n\Collider, 9000) Then Return True
	EndIf
	Return False
End Function

;one following pod: walk along the crumbs the player dropped, stop `behind` crumbs short
Function IAx131Follow(pod%, behind%)
	Local c.I131Crumb, best.I131Crumb, bd# = 100000.0, d#, idx% = 0, bi% = 0, n% = 0, i%
	If pod = 0 Then Return
	If GetParent(pod) <> 0 Then EntityParent(pod, 0)
	Local px# = EntityX(pod, True), py# = EntityY(pod, True), pz# = EntityZ(pod, True)

	For c = Each I131Crumb
		d = (c\x - px) * (c\x - px) + (c\y - py) * (c\y - py) * 4.0 + (c\z - pz) * (c\z - pz)
		If d < bd Then bd = d : best = c : bi = idx
		idx = idx + 1
	Next
	n = idx
	If best = Null Then Return

	;lost the trail (a lift, a teleport, a loaded game): catch up out of sight, behind the player
	If bd > 36.0 Or EntityDistance(pod, Collider) > 11.0 Then
		c = Last I131Crumb
		For i = 1 To behind
			If Before c <> Null Then c = Before c
		Next
		PositionEntity(pod, c\x, c\y, c\z, True)
		Return
	EndIf

	If I131Fear Then Return ;cowering: it does not move

	Local tx#, tz#, ty#
	If (n - 1 - bi) > behind Then
		c = After best
		If c = Null Then Return
		tx = c\x : ty = c\y : tz = c\z
		Local dx# = tx - px, dz# = tz - pz
		Local l# = Sqr(dx * dx + dz * dz)
		Local sp# = 0.034 * FPSfactor
		If EntityDistance(pod, Collider) > 4.0 Then sp = sp * 1.6
		If l > 0.001 Then
			If l < sp Then sp = l
			PositionEntity(pod, px + dx / l * sp, CurveValue(ty, py, 6.0), pz + dz / l * sp, True)
			RotateEntity(pod, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(pod, True), 6.0), 0, True)
		EndIf
	Else
		;close enough: look at whatever matters
		Local look% = Collider
		If Curr173 <> Null Then
			If EntityDistance(pod, Curr173\Collider) < 9.0 Then look = Curr173\Collider
		EndIf
		RotateEntity(pod, 0, CurveAngle(VectorYaw(EntityX(look, True) - px, 0, EntityZ(look, True) - pz), EntityYaw(pod, True), 10.0), 0, True)
	EndIf
End Function

;per-frame: the trail, the two followers, their warnings (called from the Indev update chain)
Function UpdateIndev131()
	Local c.I131Crumb, n% = 0, far%
	If KillTimer < 0 Then Return
	If (Not I131FollowA) And (Not I131FollowB) Then
		Delete Each I131Crumb
		Return
	EndIf

	;drop a crumb every 0.35 units the player moves (floor height, not collider height)
	Local fx# = EntityX(Collider, True), fy# = EntityY(Collider, True) - 0.3, fz# = EntityZ(Collider, True)
	c = Last I131Crumb
	far = True
	If c <> Null Then
		If (c\x - fx) * (c\x - fx) + (c\y - fy) * (c\y - fy) + (c\z - fz) * (c\z - fz) < 0.35 * 0.35 Then far = False
	EndIf
	If far Then
		c = New I131Crumb
		c\x = fx : c\y = fy : c\z = fz
		For c = Each I131Crumb
			n = n + 1
		Next
		If n > 70 Then Delete First I131Crumb
	EndIf

	;SCP-106 close and hunting: the pods cower and watch nothing
	Local fear% = False
	If Curr106 <> Null Then
		If Curr106\State <= 0 And EntityDistance(Collider, Curr106\Collider) < 6.0 Then fear = True
	EndIf
	If fear And (Not I131Fear) Then
		Msg = "The Eye Pods flatten themselves against the floor and screw their eyes shut."
		MsgTimer = 70 * 5
	EndIf
	I131Fear = fear

	If I131FollowA Then IAx131Follow(I131PodA, 3)
	If I131FollowB Then IAx131Follow(I131PodB, 5)

	;the squeal when SCP-173 is near one of them
	If I131WarnT > 0 Then I131WarnT = I131WarnT - FPSfactor
	If I131WarnT <= 0 And Curr173 <> Null And (Not I131Fear) Then
		Local saw% = False
		If I131FollowA Then
			If IAx131Sees(I131PodA, Curr173\Collider, 0) Then saw = True
		EndIf
		If (Not saw) And I131FollowB Then
			If IAx131Sees(I131PodB, Curr173\Collider, 9000) Then saw = True
		EndIf
		If saw Then
			I131WarnT = 70 * 25
			PlaySound_Strict(LoadTempSound("SFX\SCP\066\Notes" + Rand(1, 6) + ".ogg"))
			If Not EntityInView(Curr173\obj, Camera) Then
				Msg = "The Eye Pod squeals and swings round to stare at something behind you."
				MsgTimer = 70 * 5
			EndIf
		EndIf
	EndIf
End Function

;clicking a pod that is still at home: it joins you. Returns True when it did.
Function IAx131Adopt%(e.Events, pod%, name$)
	If pod = 0 Then Return False
	If IAxFlag(e, "f") Then Return False
	If Not IndevAimedAt(pod, pod, 1.5) Then Return False
	DrawHandIcon = True
	If Not MouseHit1 Then Return False
	MouseHit1 = False
	IAxSetFlag(e, "f")
	EntityParent(pod, 0)
	PlaySound_Strict(LoadTempSound("SFX\SCP\066\Notes" + Rand(1, 6) + ".ogg"))
	Msg = name + " looks you up and down, squeaks once, and rolls after you."
	MsgTimer = 70 * 6
	IndevRelieveStress(8)
	Return True
End Function

;=====================================================================
; room1testcage - Test Chamber 4-A
;   Objects: 0 lever base, 1 lever handle, 2 duct fan, 3 SCP-131-A     RoomDoors[0]: cage gate
;   EventStr: "f" the pod follows, "o" the bolt message was shown
;=====================================================================

Function IndevFillTestCage(r.Rooms)
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + 256.0 * RoomScale, r\y, r\z + 416.0 * RoomScale, 90, r, False, False)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = False : r\RoomDoors[0]\locked = True

	IAxLever(r, 0, -355.0, 342.0, 631.0, 0, False)
	r\Objects[2] = IAxFan(r, "GFX\map\indev_fan.b3d", 684.0, 400.0, -320.0, 70.0, 90)
	r\Objects[3] = IAx131Make(r, 505.0, 76.0, 545.0, "")

	IAxItem(r, "doc131", -500.0, 272.0, 210.0)
	IAxItem(r, "doc131b", -330.0, 272.0, 210.0)
	IAxItem(r, "bat", -612.0, 372.0, 450.0)
End Function

Function UpdateIndevTestCage(e.Events)
	Local r.Rooms = e\room
	I131PodA = r\Objects[3]
	I131FollowA = IAxFlag(e, "f")
	If Not I131FollowA Then IAx131Home(r\Objects[3], r, 505.0, 76.0, 545.0)
	If r\Objects[2] <> 0 And r\dist < 10.0 Then TurnEntity(r\Objects[2], 0, 0, 5.0 * FPSfactor)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	;the cage lock
	Local up% = UpdateLever(r\Objects[1])
	If r\RoomDoors[0] <> Null Then
		If up Then
			r\RoomDoors[0]\locked = False
			If Not IAxFlag(e, "o") Then
				IAxSetFlag(e, "o")
				PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
				Msg = "Below the window, the bolt on the cage gate draws back."
				MsgTimer = 70 * 5
			EndIf
		ElseIf Not r\RoomDoors[0]\open Then
			r\RoomDoors[0]\locked = True
		EndIf
	EndIf

	;the pod on the table (only from inside the cage - the mesh is in the way otherwise)
	If Not I131FollowA Then
		IAxLocal(r)
		If TFormedX() > 262.0 And TFormedZ() > 198.0 And TFormedY() < 150.0 Then
			IAx131Adopt(e, r\Objects[3], "SCP-131-A")
			I131FollowA = IAxFlag(e, "f")
		EndIf
	EndIf
End Function

;=====================================================================
; room2liftshaft - Maintenance Shaft 4
;   Objects: 0 corridor lift pivot, 1 shaft-foot lift pivot, 2 extractor fan, 3 SCP-131-B, 4-5 floor vents
;   EventState fan timer, EventState2 lift, EventState3 fan speed
;   EventStr: "f" the pod follows, "n" the fan is running, "m" first look at the pod
;=====================================================================

Function IndevFillLiftShaft(r.Rooms)
	IAxElevator(r, 216.0, 0.0, -320.0, 520.0, 240.0, -320.0, 216.0, -704.0, -320.0, 520.0, -464.0, -320.0)

	r\Objects[2] = IAxFan(r, "GFX\map\indev_fan.b3d", -512.0, 590.0, 0.0, 250.0, 0)
	RotateEntity(r\Objects[2], 90, 0, 0)
	r\Objects[3] = IAx131Make(r, -610.0, -704.0, 330.0, "GFX\npcs\scp131b.png")
	r\Objects[4] = IAxPivot(r, -470.0, -694.0, -120.0)
	r\Objects[5] = IAxPivot(r, -600.0, -694.0, 120.0)

	IAxItem(r, "18vbat", -794.0, -603.0, -360.0)
	IAxItem(r, "gasmask", -794.0, -529.0, -200.0)
	IAxItem(r, "firstaid", -560.0, -603.0, 448.0)
	IAxItem(r, "eyedrops", -420.0, -529.0, 448.0)
	IAxItem(r, "bat", -70.0, -624.0, 415.0)
	IAxItem(r, "indevration", 10.0, -624.0, 415.0)
End Function

Function UpdateIndevLiftShaft(e.Events)
	Local r.Rooms = e\room
	Local p.Particles, src%
	I131PodB = r\Objects[3]
	I131FollowB = IAxFlag(e, "f")
	If Not I131FollowB Then IAx131Home(r\Objects[3], r, -610.0, -704.0, 330.0)

	;the extractor fan cuts in and out on its own (same rhythm as the vanilla fan room)
	Local target# = 0.0
	If IAxFlag(e, "n") Then target = 7.0
	If r\dist < 16.0 Then
		If e\EventState <= 0 Then
			e\EventState = Rand(18, 34) * 70
			If IAxFlag(e, "n") Then
				e\EventStr = Replace(e\EventStr, "n", "")
				If PlayerRoom = r Then PlaySound2(LoadTempSound("SFX\ambient\Room ambience\FanOff.ogg"), Camera, r\Objects[2], 14.0)
			Else
				IAxSetFlag(e, "n")
				If PlayerRoom = r Then PlaySound2(LoadTempSound("SFX\ambient\Room ambience\FanOn.ogg"), Camera, r\Objects[2], 14.0)
			EndIf
		Else
			e\EventState = e\EventState - FPSfactor
		EndIf
	EndIf
	e\EventState3 = CurveValue(target, e\EventState3, 150.0)
	If PlayerRoom <> r Then Return

	If r\Objects[2] <> 0 Then
		TurnEntity(r\Objects[2], 0, 0, e\EventState3 * FPSfactor)
		If e\EventState3 > 0.2 Then r\SoundCHN = LoopSound2(RoomAmbience[9], r\SoundCHN, Camera, r\Objects[2], 12.0, e\EventState3 / 7.0)
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	;vapour off the floor vents; the fan draws it up the shaft when it runs
	If Rand(5) = 1 Then
		src = r\Objects[4 + Rand(0, 1)]
		If src <> 0 Then
			p = CreateParticle(EntityX(src, True) + Rnd(-0.12, 0.12), EntityY(src, True), EntityZ(src, True) + Rnd(-0.12, 0.12), 0, Rnd(0.18, 0.32), -0.02 - e\EventState3 * 0.02, 320)
			p\speed = Rnd(0.002, 0.005) + e\EventState3 * 0.0012
			p\SizeChange = 0.004
			p\Achange = -0.003
			p\A = 0.75
			EntityColor(p\obj, 46, 46, 50)
			EntityAlpha(p\obj, p\A)
			RotateEntity(p\pvt, Rnd(-90, -70), Rnd(360), 0)
		EndIf
	EndIf

	;SCP-131-B behind the crates at the foot of the shaft
	If Not I131FollowB Then
		IAxLocal(r)
		If TFormedY() < -500.0 Then
			If (Not IAxFlag(e, "m")) And EntityDistance(Collider, r\Objects[3]) < 3.0 Then
				IAxSetFlag(e, "m")
				Msg = "Something small and yellow is wedged between the crates, watching you with one very large eye."
				MsgTimer = 70 * 6
			EndIf
			IAx131Adopt(e, r\Objects[3], "SCP-131-B")
			I131FollowB = IAxFlag(e, "f")
		EndIf
	EndIf
End Function

;=====================================================================
; room2blockhall - Containment Block D, SCP-017
;   Objects: 0 lever base, 1 lever handle, 2 SCP-017 (sprite in the cage)
;   EventState 0 lamps lit, 1 the circuit is failing, 2 reset for good, 3 every lamp out
;   EventState2 banks that have failed (0-6), EventState3 timer
;=====================================================================

Function IndevFillBlockHall(r.Rooms)
	Local spr%, tex%
	IAxLever(r, 0, 0.0, -66.0, 631.0, 0, True)

	spr = CreateSprite()
	tex = LoadTexture_Strict("GFX\map\indev_017.png", 1 + 2)
	EntityTexture(spr, tex)
	FreeTexture(tex)
	ScaleSprite(spr, 0.1, 0.2)
	EntityFX(spr, 1)
	PositionEntity(spr, r\x, r\y - 122.0 * RoomScale, r\z, True)
	EntityParent(spr, r\obj)
	r\Objects[2] = spr

	IAxItem(r, "doc017", 260.0, 0.0, -800.0)
	IAxItem(r, "doc017b", 200.0, -176.0, 595.0)
	IAxItem(r, "key3", 280.0, -176.0, 595.0)
	IAxItem(r, "finefirstaid", -360.0, -161.0, 609.0)
	IAxItem(r, "18vbat", -240.0, -95.0, 609.0)
End Function

Function IAxBlockLamps(r.Rooms, lit%)
	;put the fallen lever back / drop it, and show or hide the thing in the cage
	If r\Objects[1] <> 0 Then
		If lit Then
			RotateEntity(r\Objects[1], 80, EntityYaw(r\Objects[1]), 0)
		Else
			RotateEntity(r\Objects[1], -80, EntityYaw(r\Objects[1]), 0)
		EndIf
	EndIf
End Function

Function UpdateIndevBlockHall(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then
		;walking out with the circuit down: the automatic reset catches it
		If e\EventState = 1 Or e\EventState = 3 Then
			e\EventState = 0 : e\EventState2 = 0 : e\EventState3 = 0
			SecondaryLightOn = 1.0
			IAxBlockLamps(r, True)
			If r\Objects[2] <> 0 Then ShowEntity(r\Objects[2])
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return

	Local up% = UpdateLever(r\Objects[1])
	IAxLocal(r)
	Local ly# = TFormedY()

	Select e\EventState
		Case 0
			If ly < -150.0 Then
				e\EventState = 1 : e\EventState2 = 0 : e\EventState3 = 70 * 4
				IAxBlockLamps(r, False)
				LightBlink = 1.5
				PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
				Msg = "A relay drops out somewhere overhead. On the far wall of the pit a lever falls, and the lamps on the block begin to go."
				MsgTimer = 70 * 7
				IndevStress = Min(100, IndevStress + 10)
			EndIf

		Case 1
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 Then
				e\EventState2 = e\EventState2 + 1
				e\EventState3 = 70 * 4
				LightBlink = Max(LightBlink, 0.8)
				PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
				If e\EventState2 >= 6 Then
					e\EventState = 3
					e\EventState3 = 70 * 10
					If r\Objects[2] <> 0 Then HideEntity(r\Objects[2])
					Msg = "The last lamp goes out. The cage is empty."
					MsgTimer = 70 * 6
				Else
					Msg = "Another bank of lamps dies. " + Int(6 - e\EventState2) + " of 6 still burning."
					MsgTimer = 70 * 3
				EndIf
			EndIf
			SecondaryLightOn = CurveValue(1.0 - e\EventState2 * 0.1, SecondaryLightOn, 20.0)
			IndevStress = Min(100, IndevStress + 0.012 * FPSfactor)
			If up And e\EventState = 1 Then
				e\EventState = 2
				PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
				Msg = "The lamps strike again, one bank after another. The thing in the cage has not moved. You think."
				MsgTimer = 70 * 7
				IndevRelieveStress(15)
			EndIf

		Case 2
			If SecondaryLightOn < 0.995 Then SecondaryLightOn = CurveValue(1.0, SecondaryLightOn, 20.0)

		Case 3
			SecondaryLightOn = CurveValue(0.0, SecondaryLightOn, 10.0)
			e\EventState3 = e\EventState3 - FPSfactor
			If ly < -100.0 Then
				;still in the pit: the whole pit is its shadow
				If e\EventState3 < 70 * 8.5 Then
					DeathMSG = "Subject D-9341 entered the pit of Containment Block D during a lamp circuit failure. "
					DeathMSG = DeathMSG + "No remains were recovered. SCP-017 was found in its cage when the circuit was restored."
					PlaySound_Strict(LoadTempSound("SFX\Room\Blackout.ogg"))
					Kill()
				EndIf
			Else
				IndevStress = Min(100, IndevStress + 0.05 * FPSfactor)
				Sanity = Max(Sanity - 0.3 * FPSfactor, -1000)
				If e\EventState3 <= 0 Then
					;the standby circuit relights the block
					e\EventState = 0 : e\EventState2 = 0
					IAxBlockLamps(r, True)
					If r\Objects[2] <> 0 Then ShowEntity(r\Objects[2])
					SecondaryLightOn = 1.0
					LightBlink = 2.0
					Msg = "The standby circuit cuts in. The lamps come back, and it is hanging in its cage again as if it never left."
					MsgTimer = 70 * 7
				EndIf
			EndIf
	End Select
End Function

;=====================================================================
; room2cobserve - Observation 4-C, SCP-999
;   Objects: 0 SCP-999      RoomDoors[0]: holding room door
;   EventState cooldown until it can help again, EventState2 wobble clock
;=====================================================================

Function IndevFillCObserve(r.Rooms)
	Local i%, blob%
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + 352.0 * RoomScale, r\y, r\z + 224.0 * RoomScale, 0, r, False, False)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = False
	;both buttons on the window side of the door: the other side has no wall to sit on inside the room
	For i = 0 To 1
		PositionEntity(r\RoomDoors[0]\buttons[i], r\x + 496.0 * RoomScale, EntityY(r\RoomDoors[0]\buttons[i], True), EntityZ(r\RoomDoors[0]\buttons[i], True), True)
	Next

	blob = LoadMesh_Strict("GFX\npcs\scp999.b3d")
	ScaleEntity(blob, 150.0 * RoomScale, 150.0 * RoomScale, 150.0 * RoomScale)
	PositionEntity(blob, r\x + 576.0 * RoomScale, r\y, r\z + 540.0 * RoomScale, True)
	EntityParent(blob, r\obj)
	EntityAlpha(blob, 0.93)
	EntityShininess(blob, 0.7)
	EntityPickMode(blob, 1, False)
	EntityRadius(blob, 0.3)
	r\Objects[0] = blob

	IAxItem(r, "doc999", 700.0, 0.0, 110.0)
End Function

Function UpdateIndevCObserve(e.Events)
	Local r.Rooms = e\room
	Local blob% = r\Objects[0]
	If e\EventState > 0 Then e\EventState = Max(0, e\EventState - FPSfactor)
	If PlayerRoom <> r Or blob = 0 Then Return
	If KillTimer < 0 Then Return

	;it never quite holds still
	e\EventState2 = e\EventState2 + FPSfactor
	Local s# = 150.0 * RoomScale
	ScaleEntity(blob, s * (1.0 + 0.04 * Sin(e\EventState2 * 2.3)), s * (1.0 + 0.08 * Sin(e\EventState2 * 3.1 + 40)), s * (1.0 + 0.04 * Cos(e\EventState2 * 2.3)), True)

	;inside its room it oozes over to whoever came in
	IAxLocal(r)
	Local lx# = TFormedX(), lz# = TFormedZ()
	TFormPoint(EntityX(blob, True), EntityY(blob, True), EntityZ(blob, True), 0, r\obj)
	Local bx# = TFormedX(), bz# = TFormedZ()
	If lx > 230.0 And lx < 922.0 And lz > 262.0 And lz < 826.0 Then
		Local dx# = lx - bx, dz# = lz - bz
		Local l# = Sqr(dx * dx + dz * dz)
		If l > 110.0 Then
			bx = Min(Max(bx + dx / l * 1.5 * FPSfactor, 320.0), 850.0)
			bz = Min(Max(bz + dz / l * 1.5 * FPSfactor, 340.0), 680.0)
			TFormPoint(bx, 0, bz, r\obj, 0)
			PositionEntity(blob, TFormedX(), TFormedY(), TFormedZ(), True)
		EndIf

		If IndevAimedAt(blob, blob, 1.6) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				If e\EventState <= 0 Then
					e\EventState = 70 * 120
					IndevRelieveStress(100)
					Sanity = Min(Sanity + 500, 0)
					Injuries = Max(0, Injuries - 0.35)
					Stamina = 100
					BlurTimer = 0
					Msg = "SCP-999 pours itself over your boots and hums. For the first time today your hands stop shaking."
					MsgTimer = 70 * 7
				Else
					Msg = "It pats your knee with a pseudopod. It needs a little while before it can do that again."
					MsgTimer = 70 * 5
				EndIf
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room1store4 - Stores 4
;   Objects: 0 ceiling fan, 1 the jammed crate
;   EventState how long the lid has been leaned on, EventStr "p" = opened
;=====================================================================

Function IndevFillStore4(r.Rooms)
	r\Objects[0] = IAxFan(r, "GFX\map\indev_ceilfan.b3d", 0.0, 294.0, -200.0, 140.0, 0)
	r\Objects[1] = IAxPivot(r, -64.0, 70.0, 490.0)

	IAxItem(r, "doc999b", 360.0, 80.0, -665.0)
	IAxItem(r, "indevration", -600.0, 88.0, -420.0)
	IAxItem(r, "bat", -600.0, 148.0, -260.0)
	IAxItem(r, "syringe", -600.0, 88.0, 60.0)
	IAxItem(r, "firstaid", -560.0, 101.0, 596.0)
	IAxItem(r, "eyedrops", -400.0, 175.0, 596.0)
	IAxItem(r, "18vbat", 230.0, 101.0, 596.0)
	IAxItem(r, "bat", 400.0, 175.0, 596.0)
	IAxItem(r, "gasmask", 580.0, 134.0, 520.0)
	IAxItem(r, "vest", 580.0, 204.0, 580.0)
End Function

Function UpdateIndevStore4(e.Events)
	Local r.Rooms = e\room
	Local it.Items
	If r\Objects[0] <> 0 And r\dist < 10.0 Then TurnEntity(r\Objects[0], 0, 2.0 * FPSfactor, 0)
	If PlayerRoom <> r Or r\Objects[1] = 0 Then Return
	If KillTimer < 0 Then Return
	If IAxFlag(e, "p") Then Return

	If IndevAimedAt(r\Objects[1], r\Objects[1], 1.2) Then
		DrawHandIcon = True
		Msg = "The crate lid is jammed. Hold left-click to lean on it (" + Int(Min(e\EventState / (70 * 2.0) * 100, 100)) + "%)."
		MsgTimer = 70 * 2
		If MouseDown1 Then
			e\EventState = e\EventState + FPSfactor
			If e\EventState > 70 * 2.0 Then
				IAxSetFlag(e, "p")
				PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
				Select Rand(3)
					Case 1 it = IAxItem(r, "finefirstaid", -64.0, 0.0, 400.0)
					Case 2 it = IAxItem(r, "nvgoggles", -64.0, 0.0, 400.0)
					Case 3 it = IAxItem(r, "key2", -64.0, 0.0, 400.0)
				End Select
				Msg = "The hasp gives and the lid bangs back. Something slides out onto the floor."
				MsgTimer = 70 * 5
			EndIf
		Else
			e\EventState = Max(0, e\EventState - FPSfactor * 2.0)
		EndIf
	Else
		e\EventState = Max(0, e\EventState - FPSfactor * 2.0)
	EndIf
End Function
