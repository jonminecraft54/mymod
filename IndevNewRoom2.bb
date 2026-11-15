;=====================================================================
; SCP: Containment Breach - Indev event: room2newroom2 "Remote Detonation"
;
;   room2newroom2 shares its upper floor with the stock room2nuke (the remote
;   detonation wall with its ALPHA / OMEGA levers at x -975, the elevator door
;   at x 680 and the office door at x -544), so those props are placed with the
;   same coordinates. The ground floor has its own layout: a corridor, a side
;   passage and the lower elevator cabin (door at x 1192).
;
;   1  the player walks in: Dr. Voss (researcher) and Miller (Class-D) come
;      in from the south entrance and wait in the corridor
;   2  close up they explain: both warheads were armed before the lockdown,
;      the detonation panel is upstairs, the elevator is the only way up
;   3  they walk to the elevator and wait there
;   4  upstairs SCP-079 greets the player on the intercom. Pull BOTH levers
;      down to OFF to disarm the warheads (the PA confirms it)
;      - coming back down before that: Voss sends the player back up
;   5  back downstairs after disarming: they thank the player
;   6  they walk out of the room and are removed - the event is finished
;   Upstairs: the detonation log and a level 3 keycard.
;   Event states live in the "room2newroom2" event, so they are saved.
;=====================================================================

Global INR2Room.Rooms, INR2E.Events
Global INR2Doc.NPCs, INR2D.NPCs, INR2Step%, INR2DStep%, INR2LineT#, INR2Line%
Global INR2Nags%, INR2NagT#, INR2StuckT#, INR2Warned%

;walking routes (room-local x/z), measured on the room mesh with a clearance of ~35 units
Dim INR2PathDoc#(4, 1), INR2PathD#(4, 1)

;EventState:  0 idle, 1 walking in, 2 talk, 3 waiting at the elevator, 4 disarm upstairs,
;             5 thank-you, 6 leaving, 7 done
;EventState3: bit 1 = intercom played, bit 2 = warheads disarmed

Function IndevNewRoom2Reset()
	INR2Room = Null : INR2E = Null
	INR2Doc = Null : INR2D = Null : INR2Step = 0 : INR2DStep = 0 : INR2LineT = 0 : INR2Line = 0
	INR2Nags = 0 : INR2NagT = 0 : INR2StuckT = 0 : INR2Warned = False
End Function

;called from FillRoom
Function IndevFillNewRoom2(r.Rooms)
	Local it.Items, d.Doors, n%, i%
	INR2Room = r
	INR2PathDoc(0, 0) = 80 : INR2PathDoc(0, 1) = -860
	INR2PathDoc(1, 0) = 200 : INR2PathDoc(1, 1) = -580
	INR2PathDoc(2, 0) = 600 : INR2PathDoc(2, 1) = -100
	INR2PathDoc(3, 0) = 1000 : INR2PathDoc(3, 1) = 120
	INR2PathD(0, 0) = 0 : INR2PathD(0, 1) = -900
	INR2PathD(1, 0) = 440 : INR2PathD(1, 1) = -260
	INR2PathD(2, 0) = 600 : INR2PathD(2, 1) = -180
	INR2PathD(3, 0) = 1000 : INR2PathD(3, 1) = -140

	;elevator: ground door (open) + cabin, upper door (closed) + cabin - same spots as room2nuke
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + 1192.0 * RoomScale, r\y, r\z, 90, r, True, 3)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = True
	r\RoomDoors[1] = CreateDoor(r\zone, r\x + 680.0 * RoomScale, r\y + 1504.0 * RoomScale, r\z, 90, r, False, 3)
	r\RoomDoors[1]\AutoClose = False : r\RoomDoors[1]\open = False
	r\Objects[4] = CreatePivot()
	PositionEntity(r\Objects[4], r\x + 1496.0 * RoomScale, r\y + 240.0 * RoomScale, r\z, True)
	EntityParent(r\Objects[4], r\obj)
	r\Objects[5] = CreatePivot()
	PositionEntity(r\Objects[5], r\x + 984.0 * RoomScale, r\y + 1744.0 * RoomScale, r\z, True)
	EntityParent(r\Objects[5], r\obj)

	;the upstairs office door
	d = CreateDoor(r\zone, r\x - 544.0 * RoomScale, r\y + 1504.0 * RoomScale, r\z + 738.0 * RoomScale, 90, r, False, False)
	d\AutoClose = False : d\open = False
	PositionEntity(d\buttons[0], EntityX(d\buttons[0], True), EntityY(d\buttons[0], True), r\z + 608.0 * RoomScale, True)
	PositionEntity(d\buttons[1], EntityX(d\buttons[1], True), EntityY(d\buttons[1], True), r\z + 608.0 * RoomScale, True)

	;the two warhead levers on the detonation wall (0 = ALPHA, 1 = OMEGA), start ON (armed)
	For n = 0 To 1
		r\Objects[n * 2] = CopyEntity(LeverBaseOBJ)
		r\Objects[n * 2 + 1] = CopyEntity(LeverOBJ)
		r\Levers[n] = r\Objects[n * 2 + 1]
		For i = 0 To 1
			ScaleEntity(r\Objects[n * 2 + i], 0.04, 0.04, 0.04)
			PositionEntity(r\Objects[n * 2 + i], r\x - 975.0 * RoomScale, r\y + 1712.0 * RoomScale, r\z - (502.0 - 132.0 * n) * RoomScale, True)
			EntityParent(r\Objects[n * 2 + i], r\obj)
		Next
		RotateEntity(r\Objects[n * 2], 0, -90 - 180, 0)
		RotateEntity(r\Objects[n * 2 + 1], 80, -90 - 180 - 180, 0)
		EntityPickMode(r\Objects[n * 2 + 1], 1, False)
		EntityRadius(r\Objects[n * 2 + 1], 0.1)
	Next

	;upstairs, on the open floor across the atrium (clear for 120+ units around)
	it = CreateItem("docdetonation", r\x - 760.0 * RoomScale, r\y + 1520.0 * RoomScale, r\z + 720.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("key3", r\x - 700.0 * RoomScale, r\y + 1520.0 * RoomScale, r\z - 100.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

Function INR2World(lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, INR2Room\obj, 0)
End Function

Function INR2LocalY#()
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, INR2Room\obj)
	Return TFormedY()
End Function

;walk an NPC toward a room-local point; True once it's there. If it's caught on a corner for a
;few seconds (and the player isn't watching from close by) it's put on the spot.
Function INR2WalkTo%(n.NPCs, lx#, lz#, run% = False)
	If n = Null Then Return True
	INR2World(lx, 0, lz)
	Local tx# = TFormedX(), tz# = TFormedZ()
	Local dx# = tx - EntityX(n\Collider, True), dz# = tz - EntityZ(n\Collider, True)
	If dx * dx + dz * dz < 0.3 * 0.3 Then
		n\State = 0
		Return True
	EndIf
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
	If run Then n\State = 2 Else n\State = 1
	If n\CurrSpeed < 0.004 Then
		INR2StuckT = INR2StuckT + FPSfactor
		If INR2StuckT > 70*4 And EntityDistance(n\Collider, Collider) > 3.0 Then
			PositionEntity(n\Collider, tx, EntityY(n\Collider, True) + 0.05, tz, True)
			ResetEntity(n\Collider)
			INR2StuckT = 0
		EndIf
	Else
		INR2StuckT = Max(0, INR2StuckT - FPSfactor * 0.5)
	EndIf
	Return False
End Function

;follow a route; True at the end
Function INR2Follow%(n.NPCs, doc%, reverse%)
	If n = Null Then Return True
	Local stp%
	If doc Then stp = INR2Step Else stp = INR2DStep
	If stp > 3 Then
		n\State = 0
		Return True
	EndIf
	Local k% = stp
	If reverse Then k = 3 - stp
	Local lx#, lz#
	If doc Then
		lx = INR2PathDoc(k, 0) : lz = INR2PathDoc(k, 1)
	Else
		lx = INR2PathD(k, 0) : lz = INR2PathD(k, 1)
	EndIf
	If INR2WalkTo(n, lx, lz) Then
		If doc Then INR2Step = INR2Step + 1 Else INR2DStep = INR2DStep + 1
	EndIf
	Return False
End Function

Function INR2Face(n.NPCs, ent%)
	If n = Null Then Return
	n\State = 0
	Local dx# = EntityX(ent, True) - EntityX(n\Collider, True), dz# = EntityZ(ent, True) - EntityZ(n\Collider, True)
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
End Function

Function INR2Say(who$, txt$, secs#)
	Msg = who + ": " + Chr(34) + txt + Chr(34)
	MsgTimer = 70 * secs
	INR2LineT = 70 * secs
End Function

Function INR2Spawn.NPCs(npctype%, lx#, lz#)
	INR2World(lx, 40, lz)
	Local n.NPCs = CreateNPC(npctype, TFormedX(), TFormedY() + 0.3, TFormedZ())
	n\State = 0 : n\State2 = 0
	RotateEntity(n\Collider, 0, EntityYaw(INR2Room\obj, True), 0)
	Return n
End Function

Function INR2RemoveNPCs()
	If INR2Doc <> Null Then RemoveNPC(INR2Doc) : INR2Doc = Null
	If INR2D <> Null Then RemoveNPC(INR2D) : INR2D = Null
End Function

Function UpdateIndevNewRoom2()
	If INR2Room = Null Then Return
	If INR2E = Null Then
		Local e.Events
		For e = Each Events
			If e\EventName = "room2newroom2" Then INR2E = e : Exit
		Next
		If INR2E = Null Then Return
	EndIf

	;away from the room: nobody keeps walking into walls
	If PlayerRoom <> INR2Room Then
		If INR2Doc <> Null Then INR2Doc\State = 0
		If INR2D <> Null Then INR2D\State = 0
		;on their way out when the player left: finish it out of sight
		If INR2E\EventState = 6 Then INR2RemoveNPCs() : INR2E\EventState = 7
		Return
	EndIf
	If KillTimer < 0 Then Return

	;the elevator and the two warhead levers work at any stage
	INR2E\EventState2 = UpdateElevators(INR2E\EventState2, INR2Room\RoomDoors[0], INR2Room\RoomDoors[1], INR2Room\Objects[4], INR2Room\Objects[5], INR2E)
	Local alpha% = UpdateLever(INR2Room\Objects[1])
	Local omega% = UpdateLever(INR2Room\Objects[3])
	Local disarmed% = ((Int(INR2E\EventState3) And 2) <> 0)
	If (Not disarmed) And (Not alpha) And (Not omega) Then
		INR2E\EventState3 = Int(INR2E\EventState3) Or 2
		disarmed = True
		PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
		Msg = "PA System: " + Chr(34) + "Remote detonation override accepted. Alpha and Omega warheads: DISARMED." + Chr(34)
		MsgTimer = 70*7
		IndevRelieveStress(30)
	EndIf

	Local ly# = INR2LocalY(), d#
	;after loading a save the two NPCs are ordinary NPCs again - skip the parts that need them
	If INR2E\EventState >= 1 And INR2E\EventState <= 3 And (INR2Doc = Null Or INR2D = Null) Then INR2E\EventState = 4
	If INR2E\EventState >= 5 And INR2E\EventState <= 6 And INR2Doc = Null And INR2D = Null Then INR2E\EventState = 7

	Select INR2E\EventState
		Case 0 ;the player walks in: the two of them arrive from the south entrance
			If ly > 1200 Then
				INR2E\EventState = 4
			Else
				INR2Doc = INR2Spawn(NPCtypeClerk, 60.0, -900.0)
				INR2D = INR2Spawn(NPCtypeD, -20.0, -940.0)
				INR2Step = 0 : INR2DStep = 0 : INR2Nags = 0 : INR2NagT = 0
				INR2E\EventState = 1
			EndIf

		Case 1 ;walking in, then waiting in the corridor for the player
			Local docThere% = INR2WalkTo(INR2Doc, 120.0, -560.0)
			Local dThere% = INR2WalkTo(INR2D, 20.0, -620.0)
			If docThere Then INR2Face(INR2Doc, Collider)
			If dThere Then INR2Face(INR2D, Collider)
			If ly > 1200 Then
				INR2E\EventState = 4
			ElseIf docThere And dThere Then
				d = EntityDistance(INR2Doc\Collider, Collider)
				INR2NagT = INR2NagT - FPSfactor
				If d < 3.2 Then
					INR2E\EventState = 2 : INR2Line = 0 : INR2LineT = 0
				ElseIf INR2NagT <= 0 And INR2Nags < 3 And d < 10.0 Then
					INR2Nags = INR2Nags + 1 : INR2NagT = 70*10
					INR2Say("Dr. Voss", "Hey! You, over here - don't run. We need a hand, and you need a way out.", 4)
				EndIf
			EndIf

		Case 2 ;the talk
			INR2Face(INR2Doc, Collider)
			INR2Face(INR2D, Collider)
			INR2LineT = INR2LineT - FPSfactor
			If INR2LineT <= 0 Then
				Select INR2Line
					Case 0 INR2Say("Dr. Voss", "Somebody armed both warheads right before the lockdown. The remote detonation panel is upstairs.", 6)
					Case 1 INR2Say("Miller", "And the stairwell's sealed. That elevator's the only way up. Last time something knocked on the roof.", 6)
					Case 2 INR2Say("Dr. Voss", "Pull BOTH levers on the panel down to OFF. Alpha and Omega. Then come straight back.", 6)
					Case 3 INR2Say("Miller", "Better you than me, orange. There's a keycard up there too, grab it.", 4)
					Case 4 INR2Say("Dr. Voss", "We'll wait by the elevator. Go.", 3)
					Default
						INR2E\EventState = 3 : INR2Step = 0 : INR2DStep = 0
				End Select
				INR2Line = INR2Line + 1
			EndIf

		Case 3 ;walking over to the elevator and waiting there
			Local a% = INR2Follow(INR2Doc, True, False)
			Local b% = INR2Follow(INR2D, False, False)
			If a Then INR2Face(INR2Doc, Collider)
			If b Then INR2Face(INR2D, Collider)
			If ly > 1200 Then
				INR2E\EventState = 4
				INR2Warned = False
			EndIf

		Case 4 ;upstairs - disarm the warheads
			If INR2Doc <> Null Then INR2Face(INR2Doc, Collider)
			If INR2D <> Null Then INR2Face(INR2D, Collider)
			If ly > 1200 Then
				If (Int(INR2E\EventState3) And 1) = 0 Then
					INR2E\EventState3 = Int(INR2E\EventState3) Or 1
					LightBlink = 3.0
					PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
					Msg = "Intercom: " + Chr(34) + "Remote detonation terminal accessed. Alpha and Omega warheads: ARMED. Have a nice day." + Chr(34)
					MsgTimer = 70*7
				EndIf
				INR2Warned = False
			ElseIf ly < 200 And ((Int(INR2E\EventState3) And 1) <> 0) Then
				If disarmed Then
					If INR2Doc <> Null Or INR2D <> Null Then
						INR2E\EventState = 5 : INR2Line = 0 : INR2LineT = 0
					Else
						INR2E\EventState = 7
					EndIf
				ElseIf (Not INR2Warned) And INR2Doc <> Null Then
					INR2Warned = True
					INR2Say("Dr. Voss", "They're still armed! Both levers - all the way down to OFF. Go back up!", 5)
				EndIf
			EndIf

		Case 5 ;the thank-you
			INR2Face(INR2Doc, Collider)
			INR2Face(INR2D, Collider)
			INR2LineT = INR2LineT - FPSfactor
			If INR2LineT <= 0 Then
				Select INR2Line
					Case 0 INR2Say("Dr. Voss", "Disarmed. You actually did it. I didn't think you'd come back down.", 5)
					Case 1 INR2Say("Miller", "Did you hear the voice up there? That wasn't anybody on staff.", 4)
					Case 2 INR2Say("Dr. Voss", "Keep the keycard. Head for the Entrance Zone. We're going the other way. Good luck.", 5)
					Default
						INR2E\EventState = 6 : INR2Step = 0 : INR2DStep = 0
				End Select
				INR2Line = INR2Line + 1
			EndIf

		Case 6 ;they leave the way they came
			Local a2% = INR2Follow(INR2Doc, True, True)
			Local b2% = INR2Follow(INR2D, False, True)
			If a2 And INR2Doc <> Null Then
				If INR2WalkTo(INR2Doc, 60.0, -960.0) Then RemoveNPC(INR2Doc) : INR2Doc = Null
			EndIf
			If b2 And INR2D <> Null Then
				If INR2WalkTo(INR2D, -20.0, -980.0) Then RemoveNPC(INR2D) : INR2D = Null
			EndIf
			If INR2Doc = Null And INR2D = Null Then INR2E\EventState = 7

		Case 7 ;finished - nothing else happens in this room
	End Select
End Function
