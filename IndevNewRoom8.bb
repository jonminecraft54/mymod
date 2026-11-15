;=====================================================================
; SCP: Containment Breach - Indev event: room2newroom8 "Omega Silo"
;
;   room2newroom8 is the room2nuke layout sunk 32 units (floors at y -32 and
;   1472), plus a long upstairs wing - a corridor north from the atrium, and
;   the OMEGA WARHEAD SILO hall with two fuel tanks (floor y 1504).
;
;   1  the player walks in: Dr. Okafor comes in from the south entrance
;   2  close up she explains: SCP-079 started a silo launch sequence. The abort
;      lever is on the upstairs terminal wall, but it stays locked until both
;      fuel feed valves on the silo tanks are closed by hand
;   3  she walks to the elevator and waits there
;   4  upstairs the countdown starts (3:00, alarm, HUD timer). A Class-D (Pike)
;      hiding in the silo hall points the way. Close both valves, then pull the
;      ABORT lever down
;   5  aborted: the alarm stops, a level 4 keycard drops from the terminal,
;      Okafor and Pike are gone once the player leaves the room
;   6  failed: the silo vents. Upstairs that's fatal; downstairs it's a very bad day
;   Leaving the room at any point stops the event: the countdown freezes, the
;   alarm goes quiet and the NPCs stand still. It carries on when the player
;   comes back.
;   Event states live in the "room2newroom8" event, so they are saved.
;=====================================================================

Global INR8Room.Rooms, INR8E.Events
Global INR8Doc.NPCs, INR8D.NPCs, INR8Step%, INR8Line%, INR8LineT#, INR8Nags%, INR8NagT#, INR8StuckT#
Global INR8Alarm%, INR8AlarmCHN%, INR8PikeTold%, INR8LockMsgT#, INR8Spin#
Global INR8VA0#, INR8VA1#, INR8Synced%, INR8BurstT#, INR8BurstAt%, INR8Taunt%, INR8AdoptT#

;EventState:  0 idle, 1 walking in, 2 talk, 3 go upstairs, 4 countdown, 5 aborted, 6 failed, 7 done
;EventState2: elevator
;EventState3: countdown frames left
;EventStr:    "a" valve 1 closed, "b" valve 2 closed, "i" intercom played
Const INR8_COUNTDOWN# = 12600.0 ;70 * 180

Function IndevNewRoom8Reset()
	If INR8AlarmCHN <> 0 Then
		If ChannelPlaying(INR8AlarmCHN) Then StopChannel(INR8AlarmCHN)
	EndIf
	INR8AlarmCHN = 0
	INR8Room = Null : INR8E = Null
	INR8Doc = Null : INR8D = Null : INR8Step = 0 : INR8Line = 0 : INR8LineT = 0
	INR8Nags = 0 : INR8NagT = 0 : INR8StuckT = 0 : INR8PikeTold = False : INR8LockMsgT = 0 : INR8Spin = 0
	INR8Synced = False : INR8BurstT = 70*6 : INR8BurstAt = -1 : INR8Taunt = 0 : INR8AdoptT = 0
End Function

;called from FillRoom
Function IndevFillNewRoom8(r.Rooms)
	Local it.Items, d.Doors, i%
	INR8Room = r

	;elevator: ground door (open) + cabin, upper door (closed) + cabin
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + 1192.0 * RoomScale, r\y - 32.0 * RoomScale, r\z, 90, r, True, 3)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = True
	r\RoomDoors[1] = CreateDoor(r\zone, r\x + 680.0 * RoomScale, r\y + 1472.0 * RoomScale, r\z, 90, r, False, 3)
	r\RoomDoors[1]\AutoClose = False : r\RoomDoors[1]\open = False
	r\Objects[4] = CreatePivot()
	PositionEntity(r\Objects[4], r\x + 1496.0 * RoomScale, r\y + 208.0 * RoomScale, r\z, True)
	EntityParent(r\Objects[4], r\obj)
	r\Objects[5] = CreatePivot()
	PositionEntity(r\Objects[5], r\x + 984.0 * RoomScale, r\y + 1712.0 * RoomScale, r\z, True)
	EntityParent(r\Objects[5], r\obj)

	;the upstairs office door
	d = CreateDoor(r\zone, r\x - 544.0 * RoomScale, r\y + 1472.0 * RoomScale, r\z + 738.0 * RoomScale, 90, r, False, False)
	d\AutoClose = False : d\open = False
	PositionEntity(d\buttons[0], EntityX(d\buttons[0], True), EntityY(d\buttons[0], True), r\z + 608.0 * RoomScale, True)
	PositionEntity(d\buttons[1], EntityX(d\buttons[1], True), EntityY(d\buttons[1], True), r\z + 608.0 * RoomScale, True)

	;the ABORT lever on the terminal wall (wall at x -1000, under the sign), starts UP (launch armed)
	r\Objects[0] = CopyEntity(LeverBaseOBJ)
	r\Objects[1] = CopyEntity(LeverOBJ)
	r\Levers[0] = r\Objects[1]
	For i = 0 To 1
		ScaleEntity(r\Objects[i], 0.04, 0.04, 0.04)
		PositionEntity(r\Objects[i], r\x - 991.0 * RoomScale, r\y + 1640.0 * RoomScale, r\z - 436.0 * RoomScale, True)
		EntityParent(r\Objects[i], r\obj)
	Next
	RotateEntity(r\Objects[0], 0, -90 - 180, 0)
	RotateEntity(r\Objects[1], 80, -90 - 180 - 180, 0)
	EntityPickMode(r\Objects[1], 1, False)
	EntityRadius(r\Objects[1], 0.1)

	;the two fuel feed valves: red hand wheels on the +z side of the silo tanks
	r\Objects[2] = INR8MakeValve(r, 5190.0, 1600.0, 2722.0)
	r\Objects[3] = INR8MakeValve(r, 5796.0, 1600.0, 2676.0)

	;the silo log in the terminal office
	it = CreateItem("docomega", r\x - 700.0 * RoomScale, r\y + 1488.0 * RoomScale, r\z + 150.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

Function INR8MakeValve%(r.Rooms, lx#, ly#, lz#)
	;base pivot turned so its local Y axis points along +z (toward the walkway); the wheel spins on that axis
	Local base% = CreatePivot()
	Local stem% = CreateCylinder(8, True, base)
	ScaleEntity(stem, 0.02, 0.06, 0.02)
	PositionEntity(stem, 0, -0.05, 0)
	EntityColor(stem, 70, 70, 75)
	Local v% = CreateCylinder(16, True, base)
	ScaleEntity(v, 0.13, 0.02, 0.13)
	EntityColor(v, 150, 20, 15)
	EntityShininess(v, 0.4)
	Local hub% = CreateCylinder(8, True, v)
	ScaleEntity(hub, 0.3, 1.8, 0.3)
	EntityColor(hub, 60, 60, 60)
	Local spoke% = CreateCube(v)
	ScaleEntity(spoke, 0.95, 0.6, 0.07)
	EntityColor(spoke, 120, 15, 10)
	spoke = CreateCube(v)
	ScaleEntity(spoke, 0.07, 0.6, 0.95)
	EntityColor(spoke, 120, 15, 10)
	PositionEntity(base, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
	RotateEntity(base, 90, 0, 0, True)
	EntityPickMode(v, 2)
	EntityParent(base, r\obj)
	Return v
End Function

Function INR8World(lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, INR8Room\obj, 0)
End Function

Function INR8LocalY#()
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, INR8Room\obj)
	Return TFormedY()
End Function

Function INR8WalkTo%(n.NPCs, lx#, lz#)
	If n = Null Then Return True
	INR8World(lx, 0, lz)
	Local tx# = TFormedX(), tz# = TFormedZ()
	Local dx# = tx - EntityX(n\Collider, True), dz# = tz - EntityZ(n\Collider, True)
	If dx * dx + dz * dz < 0.3 * 0.3 Then
		n\State = 0
		Return True
	EndIf
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
	n\State = 1
	If n\CurrSpeed < 0.004 Then
		INR8StuckT = INR8StuckT + FPSfactor
		If INR8StuckT > 70*4 And EntityDistance(n\Collider, Collider) > 3.0 Then
			PositionEntity(n\Collider, tx, EntityY(n\Collider, True) + 0.05, tz, True)
			ResetEntity(n\Collider)
			INR8StuckT = 0
		EndIf
	Else
		INR8StuckT = Max(0, INR8StuckT - FPSfactor * 0.5)
	EndIf
	Return False
End Function

Function INR8Face(n.NPCs, ent%)
	If n = Null Then Return
	n\State = 0
	Local dx# = EntityX(ent, True) - EntityX(n\Collider, True), dz# = EntityZ(ent, True) - EntityZ(n\Collider, True)
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
End Function

Function INR8Say(who$, txt$, secs#)
	Msg = who + ": " + Chr(34) + txt + Chr(34)
	MsgTimer = 70 * secs
	INR8LineT = 70 * secs
End Function

Function INR8Spawn.NPCs(npctype%, lx#, ly#, lz#)
	INR8World(lx, ly + 40, lz)
	Local n.NPCs = CreateNPC(npctype, TFormedX(), TFormedY() + 0.3, TFormedZ())
	n\State = 0 : n\State2 = 0
	RotateEntity(n\Collider, 0, EntityYaw(INR8Room\obj, True), 0)
	Return n
End Function

Function INR8Flag%(f$)
	Return Instr(INR8E\EventStr, f) > 0
End Function

Function INR8SetFlag(f$)
	If Not INR8Flag(f) Then INR8E\EventStr = INR8E\EventStr + f
End Function

Function INR8StopAlarm()
	If INR8AlarmCHN <> 0 Then
		If ChannelPlaying(INR8AlarmCHN) Then StopChannel(INR8AlarmCHN)
	EndIf
	INR8AlarmCHN = 0
End Function

Function INR8RemoveNPCs()
	If INR8Doc <> Null Then RemoveNPC(INR8Doc) : INR8Doc = Null
	If INR8D <> Null Then RemoveNPC(INR8D) : INR8D = Null
End Function

Function UpdateIndevNewRoom8()
	If INR8Room = Null Then Return
	If INR8E = Null Then
		Local e.Events
		For e = Each Events
			If e\EventName = "room2newroom8" Then INR8E = e : Exit
		Next
		If INR8E = Null Then Return
	EndIf

	;out of the room: the event stops - countdown frozen, alarm off, nobody walks
	If PlayerRoom <> INR8Room Then
		INR8StopAlarm()
		If INR8Doc <> Null Then INR8Doc\State = 0
		If INR8D <> Null Then INR8D\State = 0
		If INR8E\EventState >= 5 Then
			INR8RemoveNPCs()
			INR8E\EventState = 7
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then INR8StopAlarm() : Return

	INR8E\EventState2 = UpdateElevators(INR8E\EventState2, INR8Room\RoomDoors[0], INR8Room\RoomDoors[1], INR8Room\Objects[4], INR8Room\Objects[5], INR8E)

	Local ly# = INR8LocalY(), d#, i%
	Local valves% = INR8Flag("a") And INR8Flag("b")

	;the valves (closing one turns the wheel; they stay shut)
	;(wheel angles follow the saved flags, so a closed valve also looks closed after loading)
	If Not INR8Synced Then
		INR8Synced = True
		INR8VA0 = 0 : INR8VA1 = 0
		If INR8Flag("a") Then INR8VA0 = 540
		If INR8Flag("b") Then INR8VA1 = 540
	EndIf
	If INR8Flag("a") Then INR8VA0 = CurveValue(540, INR8VA0, 25)
	If INR8Flag("b") Then INR8VA1 = CurveValue(540, INR8VA1, 25)
	If INR8Room\Objects[2] <> 0 Then RotateEntity(INR8Room\Objects[2], 0, INR8VA0, 0)
	If INR8Room\Objects[3] <> 0 Then RotateEntity(INR8Room\Objects[3], 0, INR8VA1, 0)
	If INR8E\EventState <= 4 Then
		For i = 0 To 1
			Local v% = INR8Room\Objects[2 + i], f$ = Chr(97 + i)
			If v <> 0 Then
				If (Not INR8Flag(f)) And IndevAimedAt(v, v, 1.4) Then
					DrawHandIcon = True
					If MouseHit1 Then
						MouseHit1 = False
						INR8SetFlag(f)
						PlaySound2(LeverSFX, Camera, v, 3.0)
						PlaySound_Strict(LoadTempSound("SFX\General\Hiss.ogg"))
						If INR8Flag("a") And INR8Flag("b") Then
							Msg = "The second wheel squeals shut. The hiss in the pipes dies away. Somewhere upstairs, a lock releases."
						Else
							Msg = "You haul the wheel round until it won't turn any more. The fuel line shudders. One more."
						EndIf
						MsgTimer = 70*5
					EndIf
				EndIf
			EndIf
		Next
		valves = INR8Flag("a") And INR8Flag("b")
	EndIf

	;the ABORT lever: locked until both valves are shut
	Local lever% = UpdateLever(INR8Room\Objects[1], (Not valves) Or INR8E\EventState <> 4)
	If INR8LockMsgT > 0 Then INR8LockMsgT = INR8LockMsgT - FPSfactor
	If (Not valves) And INR8E\EventState = 4 And INR8LockMsgT <= 0 Then
		If IndevAimedAt(INR8Room\Objects[1], INR8Room\Objects[1], 1.0) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				INR8LockMsgT = 70*4
				PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
				Msg = "The lever won't move. The panel reads: ABORT INHIBITED - FUEL FEED OPEN (SILO TANKS 1, 2)."
				MsgTimer = 70*5
			EndIf
		EndIf
	EndIf

	;after loading a save the handles are gone: take the saved NPCs back (or bring them back out of sight)
	INR8AdoptT = INR8AdoptT - FPSfactor
	If INR8AdoptT <= 0 Then
		INR8AdoptT = 70
		If INR8Doc = Null And INR8E\EventState >= 1 And INR8E\EventState <= 5 Then
			INR8Doc = INR8Adopt(NPCtypeClerk, 800.0, 0.0, -120.0, (ly > 1200))
			If INR8Doc <> Null And INR8E\EventState <= 2 Then INR8E\EventState = 3 : INR8Step = 3
		EndIf
		If INR8D = Null And INR8E\EventState >= 4 And INR8E\EventState <= 5 Then
			INR8D = INR8Adopt(NPCtypeD, 3000.0, 1504.0, 3000.0, True)
		EndIf
	EndIf
	If INR8E\EventState >= 1 And INR8E\EventState <= 2 And INR8Doc = Null Then INR8E\EventState = 3

	Select INR8E\EventState
		Case 0 ;the player walks in
			If ly > 1200 Then
				INR8E\EventState = 3
			Else
				INR8Doc = INR8Spawn(NPCtypeClerk, 0.0, 0.0, -900.0)
				INR8Step = 0 : INR8Nags = 0 : INR8NagT = 0
				INR8E\EventState = 1
			EndIf

		Case 1 ;walking in, then waiting for the player
			Local there% = INR8WalkTo(INR8Doc, 0.0, -560.0)
			If there Then INR8Face(INR8Doc, Collider)
			If ly > 1200 Then
				INR8E\EventState = 3
			ElseIf there Then
				d = EntityDistance(INR8Doc\Collider, Collider)
				INR8NagT = INR8NagT - FPSfactor
				If d < 3.2 Then
					INR8E\EventState = 2 : INR8Line = 0 : INR8LineT = 0
				ElseIf INR8NagT <= 0 And INR8Nags < 3 And d < 10.0 Then
					INR8Nags = INR8Nags + 1 : INR8NagT = 70*10
					INR8Say("Dr. Okafor", "You! Wait - please. I can't do this on my own.", 4)
				EndIf
			EndIf

		Case 2 ;the talk
			INR8Face(INR8Doc, Collider)
			If ly > 1200 Then INR8E\EventState = 3
			INR8LineT = INR8LineT - FPSfactor
			If INR8LineT <= 0 Then
				Select INR8Line
					Case 0 INR8Say("Dr. Okafor", "SCP-079 got into the silo network. It started the Omega launch sequence the moment the lockdown hit.", 6)
					Case 1 INR8Say("Dr. Okafor", "The ABORT lever is on the terminal wall upstairs. But it's inhibited while the fuel feed is open.", 6)
					Case 2 INR8Say("Dr. Okafor", "Go north through the long corridor to the silo hall. Close the red valves on BOTH tanks by hand.", 6)
					Case 3 INR8Say("Dr. Okafor", "Then run back to the terminal and pull the lever down. The countdown starts as soon as it sees you up there.", 6)
					Case 4 INR8Say("Dr. Okafor", "There's a man hiding in the silo hall. Pike. He knows where the tanks are. Go!", 5)
					Default
						INR8E\EventState = 3 : INR8Step = 0
				End Select
				INR8Line = INR8Line + 1
			EndIf

		Case 3 ;she walks to the elevator; the countdown starts upstairs
			If INR8Doc <> Null Then
				Local done% = False
				Select INR8Step
					Case 0 If INR8WalkTo(INR8Doc, 150.0, -250.0) Then INR8Step = 1
					Case 1 If INR8WalkTo(INR8Doc, 400.0, 0.0) Then INR8Step = 2
					Case 2 If INR8WalkTo(INR8Doc, 800.0, -120.0) Then INR8Step = 3
					Default done = True
				End Select
				If done Then INR8Face(INR8Doc, Collider)
			EndIf
			If ly > 1200 Then INR8StartCountdown()

		Case 4 ;the countdown
			INR8E\EventState3 = INR8E\EventState3 - FPSfactor
			If INR8Doc <> Null Then INR8Face(INR8Doc, Collider)

			;the alarm (quieter downstairs)
			If INR8Alarm = 0 Then INR8Alarm = LoadSound_Strict("SFX\Alarm\Alarm3.ogg")
			Local vol# = 0.35
			If ly > 1200 Then vol = 0.7
			If INR8AlarmCHN = 0 Then
				INR8AlarmCHN = PlaySound_Strict(INR8Alarm)
			ElseIf Not ChannelPlaying(INR8AlarmCHN) Then
				INR8AlarmCHN = PlaySound_Strict(INR8Alarm)
			EndIf
			If INR8AlarmCHN <> 0 Then ChannelVolume(INR8AlarmCHN, vol * SFXVolume)
			If Rand(500) = 1 Then LightBlink = Max(LightBlink, Rnd(0.5, 1.5))
			If INR8E\EventState3 < 70*30 Then CameraShake = Max(CameraShake, 0.25)
			IndevStress = Min(100, IndevStress + 0.01 * FPSfactor)

			;SCP-079 on the intercom
			Local tl% = Int(INR8E\EventState3 / 70.0)
			If INR8Taunt < 1 And tl <= 150 Then INR8Taunt = 1 : INR8PA("You came up here to stop me. Adorable. The fuel feed says otherwise.")
			If INR8Taunt < 2 And (INR8Flag("a") Or INR8Flag("b")) Then INR8Taunt = 2 : INR8PA("Manual valves. How very... analogue. I am re-routing the pressure.")
			If INR8Taunt < 3 And tl <= 90 Then INR8Taunt = 3 : INR8PA("Ninety seconds. I have already closed the doors you are thinking about.")
			If INR8Taunt < 4 And valves Then INR8Taunt = 4 : INR8PA("...The lever will not help you. It never helps.")
			If INR8Taunt < 5 And tl <= 30 Then INR8Taunt = 5 : INR8PA("Thirty. I would say goodbye, but I will still be here.")

			;while the feed is open the silo tanks vent scalding vapour - a hiss, then the burst
			If (Not valves) And ly > 1200 Then INR8UpdateSteam()

			;Pike, hiding in the silo hall
			If INR8D <> Null Then
				d = EntityDistance(INR8D\Collider, Collider)
				INR8D\State = 0
				If d < 12.0 Then INR8Face(INR8D, Collider)
				INR8LineT = INR8LineT - FPSfactor
				If INR8LineT <= 0 And d < 6.0 Then
					If valves Then
						If INR8PikeTold < 3 Then
							INR8PikeTold = 3
							INR8Say("Pike", "They're both shut! The lever - back at the terminal, back the way you came! RUN!", 5)
						EndIf
					ElseIf INR8PikeTold = 0 Then
						INR8PikeTold = 1
						INR8Say("Pike", "Don't shoot - I'm D-class! The valves? Past me, on the two big tanks at the end. Red wheels.", 6)
					ElseIf INR8PikeTold = 1 And (INR8Flag("a") Or INR8Flag("b")) Then
						INR8PikeTold = 2
						INR8Say("Pike", "That's one! The other tank, the other wheel - hurry!", 4)
					EndIf
				EndIf
			EndIf

			;pulled down -> aborted
			If valves And (Not lever) Then
				INR8Abort()
			ElseIf INR8E\EventState3 <= 0 Then
				INR8Fail(ly)
			EndIf

		Case 5 ;aborted: the NPCs have their say
			If INR8Doc <> Null Then INR8Face(INR8Doc, Collider)
			If INR8D <> Null Then INR8Face(INR8D, Collider)
			INR8LineT = INR8LineT - FPSfactor
			If INR8LineT <= 0 Then
				If ly < 200 And INR8Doc <> Null And INR8Line = 0 Then
					INR8Line = 1
					INR8Say("Dr. Okafor", "You did it. The whole site would have gone up with the silo. Take the card - get out of Heavy Containment.", 6)
				ElseIf ly > 1200 And INR8D <> Null And INR8Line < 2 And EntityDistance(INR8D\Collider, Collider) < 6.0 Then
					INR8Line = 2
					INR8Say("Pike", "It stopped... it actually stopped. I'm staying up here till someone with a gun says it's over.", 5)
				EndIf
			EndIf

		Case 6 ;failed
			If INR8Doc <> Null Then INR8Doc\State = 0
			INR8E\EventState = 7

		Case 7 ;finished
	End Select
End Function

Function INR8PA(txt$)
	Msg = "Intercom: " + Chr(34) + txt + Chr(34)
	MsgTimer = 70*6
	PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
End Function

;find the NPC the save restored near its spot, or make a new one where the player can't see it appear
Function INR8Adopt.NPCs(npctype%, lx#, ly#, lz#, allowSpawn%)
	Local n.NPCs, best.NPCs, bd# = 12.0, dd#
	INR8World(lx, ly + 40, lz)
	Local wx# = TFormedX(), wy# = TFormedY(), wz# = TFormedZ()
	For n = Each NPCs
		If n\NPCtype = npctype Then
			dd = Abs(EntityX(n\Collider, True) - wx) + Abs(EntityZ(n\Collider, True) - wz)
			If Abs(EntityY(n\Collider, True) - wy) < 2.0 And dd < bd Then bd = dd : best = n
		EndIf
	Next
	If best <> Null Then Return best
	If allowSpawn Then
		If Abs(EntityY(Collider, True) - wy) > 2.0 Or Abs(EntityX(Collider, True) - wx) + Abs(EntityZ(Collider, True) - wz) > 10.0 Then
			Return INR8Spawn(npctype, lx, ly, lz)
		EndIf
	EndIf
	Return Null
End Function

;steam bursts from the silo tanks (only from a tank whose valve is still open)
Function INR8UpdateSteam()
	Local j%, v%, px#, py#, pz#, pp.Particles
	INR8BurstT = INR8BurstT - FPSfactor
	If INR8BurstAt < 0 Then
		If INR8BurstT <= 0 Then
			INR8BurstAt = Rand(0, 1)
			If INR8Flag(Chr(97 + INR8BurstAt)) Then INR8BurstAt = 1 - INR8BurstAt
			INR8BurstT = 70*1.2
			v = INR8Room\Objects[2 + INR8BurstAt]
			If v <> 0 Then PlaySound2(LoadTempSound("SFX\General\Hiss.ogg"), Camera, v, 8.0)
		EndIf
	ElseIf INR8BurstT <= 0 Then
		v = INR8Room\Objects[2 + INR8BurstAt]
		If v <> 0 Then
			px = EntityX(v, True) : py = EntityY(v, True) : pz = EntityZ(v, True)
			For j = 0 To 10
				pp = CreateParticle(px + Rnd(-0.3, 0.3), py + Rnd(-0.2, 0.4), pz + Rnd(-0.3, 0.3), 0, Rnd(0.2, 0.4), -0.25, 160)
				pp\speed = Rnd(0.004, 0.012) : pp\SizeChange = 0.012 : pp\Achange = -0.006
				RotateEntity(pp\pvt, Rnd(-30, 10), Rnd(360), 0)
			Next
			If EntityDistance(Collider, v) < 1.6 Then
				Injuries = Injuries + 0.12
				BlurTimer = 70*2
				CameraShake = Max(CameraShake, 1.0)
				Msg = "A jet of scalding vapour blasts out of the tank seam. Keep clear of it while the feed is open."
				MsgTimer = 70*4
			EndIf
		EndIf
		INR8BurstAt = -1
		INR8BurstT = 70 * Rnd(5.0, 9.0)
	EndIf
End Function

Function INR8StartCountdown()
	INR8E\EventState = 4
	If INR8E\EventState3 <= 0 Then INR8E\EventState3 = INR8_COUNTDOWN
	INR8LineT = 70*3
	If INR8D = Null Then INR8D = INR8Adopt(NPCtypeD, 3000.0, 1504.0, 3000.0, True)
	If Not INR8Flag("i") Then
		INR8SetFlag("i")
		LightBlink = 3.0
		PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
		Msg = "Intercom: " + Chr(34) + "Omega silo launch sequence in progress. T-minus three minutes. Please do not interfere." + Chr(34)
		MsgTimer = 70*7
		IndevStress = Min(100, IndevStress + 15)
	EndIf
End Function

Function INR8Abort()
	Local it.Items
	INR8E\EventState = 5 : INR8Line = 0 : INR8LineT = 70*6
	INR8StopAlarm()
	PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
	Msg = "PA System: " + Chr(34) + "Launch sequence ABORTED. Omega silo returning to safe state." + Chr(34)
	MsgTimer = 70*7
	IndevRelieveStress(40)
	;the terminal drawer drops a keycard below the lever
	it = CreateItem("key4", INR8Room\x - 760.0 * RoomScale, INR8Room\y + 1490.0 * RoomScale, INR8Room\z - 430.0 * RoomScale)
	EntityParent(it\collider, INR8Room\obj)
End Function

Function INR8Fail(ly#)
	INR8E\EventState = 6 : INR8E\EventState3 = 0
	INR8StopAlarm()
	LightBlink = 8.0
	CameraShake = 6.0
	PlaySound_Strict(LoadTempSound("SFX\Room\TunnelBurst.ogg"))
	If INR8D <> Null Then RemoveNPC(INR8D) : INR8D = Null
	If ly > 1200 Then
		DeathMSG = "Subject D-9341 was found dead on the upper level of the Omega silo complex, with severe burns consistent with a silo fuel vent. "
		DeathMSG = DeathMSG + "The launch sequence was halted by the silo's own failsafe 0.4 seconds later."
		Kill()
	Else
		Msg = "A roar rolls down the elevator shaft and the floor bucks under you. The silo vented - upstairs is an oven now."
		MsgTimer = 70*7
		Injuries = Injuries + 0.6
		BlurTimer = 70*6
	EndIf
End Function

;the countdown on the HUD
Function DrawIndevNewRoom8()
	If INR8Room = Null Or INR8E = Null Then Return
	If INR8E\EventState <> 4 Or PlayerRoom <> INR8Room Or KillTimer < 0 Then Return
	Local s% = Max(0, Int(INR8E\EventState3 / 70.0))
	Local t$ = "OMEGA SILO LAUNCH   T-" + Right("0" + (s / 60), 2) + ":" + Right("0" + (s Mod 60), 2)
	SetFont Font1
	Local x% = GraphicWidth / 2, y% = 60 * MenuScale
	Color 0, 0, 0
	Text x + 2, y + 2, t, True, True
	If s < 30 And (MilliSecs() / 250) Mod 2 = 0 Then Color 255, 230, 60 Else Color 230, 40, 30
	Text x, y, t, True, True
	Local sub$
	If INR8Flag("a") And INR8Flag("b") Then
		sub = "FUEL FEED CLOSED - ABORT AVAILABLE AT TERMINAL"
	Else
		Local n% = 0
		If INR8Flag("a") Then n = 1
		If INR8Flag("b") Then n = n + 1
		sub = "FUEL FEED OPEN  (" + n + "/2 VALVES CLOSED)"
	EndIf
	Color 180, 180, 180
	Text x, y + 24 * MenuScale, sub, True, True
	Color 255, 255, 255
End Function
