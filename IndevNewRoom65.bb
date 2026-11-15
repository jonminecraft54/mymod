;=====================================================================
; SCP: Containment Breach - Indev event: room2newroom65 "Dead Circuit"
;
;   room2newroom65: an upper storage corridor (floor y 0) with stairs going
;   west down to a dark lower level (floor y -384 / -401): locker rows, an
;   office, a boiler corner and a west records room.
;
;   1  the player walks in upstairs: Dr. Reyes is waiting by the stairs
;   2  close up she explains: the lower level lost power, the Hollow came
;      out with the dark. Three breaker levers down there bring the lights
;      back - and light is the one thing it can't stand
;   3  downstairs the hunt is on: the Hollow (a pitch-black man-shape) only
;      moves while nobody is looking at it. Stare it down and it flinches away,
;      turn your back and it closes in. Three catches and it's over.
;      Pull all three breakers UP: west records room, south wall, north-east wall
;   4  all breakers on: the generator kicks in and the Hollow burns off in the
;      light. Back upstairs Reyes hands over her night vision goggles
;   5  done
;   Leaving the room stops the event: the Hollow is gone, nothing moves, the
;   breakers stay as they were. It carries on when the player comes back.
;   Event states live in the "room2newroom65" event, so they are saved.
;=====================================================================

Global INR65Room.Rooms, INR65E.Events, INR65Doc.NPCs
Global INR65Line%, INR65LineT#, INR65Nags%, INR65NagT#, INR65AdoptT#, INR65Synced%
Global INR65Hollow%, INR65Head%, INR65HState%, INR65HCool#, INR65HGaze#, INR65HJump#, INR65HWp%, INR65HNear#
Global INR65Whisper#, INR65Wind#, INR65SafeX#, INR65SafeY#, INR65SafeZ#, INR65HasSafe%
Global INR65Tob.NPCs, INR65Hale.NPCs, INR65TobT#, INR65TobLine%, INR65HaleT#, INR65HaleLine%, INR65TobStep%

;EventState:  0 idle, 1 Reyes waits, 2 talk, 3 the hunt, 4 power restored, 5 done
;EventState3: times the Hollow has caught the player
;EventStr:    "1" "2" "3" breakers on, "g" goggles given
Dim INR65Wp#(9, 2)

Function IndevNewRoom65Reset()
	INR65Room = Null : INR65E = Null : INR65Doc = Null
	INR65Line = 0 : INR65LineT = 0 : INR65Nags = 0 : INR65NagT = 0 : INR65AdoptT = 0 : INR65Synced = False
	;(the Hollow belonged to the old map and was freed with it)
	INR65Hollow = 0 : INR65Head = 0
	INR65HState = 0 : INR65HCool = 70*4 : INR65HGaze = 0 : INR65HJump = 0 : INR65HWp = 8 : INR65HNear = 0 : INR65Whisper = 0
	INR65Wind = 0 : INR65HasSafe = False
	INR65Tob = Null : INR65Hale = Null : INR65TobT = 0 : INR65TobLine = 0 : INR65HaleT = 0 : INR65HaleLine = 0 : INR65TobStep = 0
End Function

;called from FillRoom
Function IndevFillNewRoom65(r.Rooms)
	Local it.Items
	INR65Room = r

	;the lower level's walkable spots (the mesh's own waypoints, clear for 180+ units)
	INR65SetWp(0, -1152, -384, 4)
	INR65SetWp(1, -1024, -384, 516)
	INR65SetWp(2, -1024, -384, -508)
	INR65SetWp(3, -1317, -384, 383)
	INR65SetWp(4, -1313, -384, -693)
	INR65SetWp(5, -2160, -401, -868)
	INR65SetWp(6, -2150, -401, 540)
	INR65SetWp(7, -2227, -401, -132)
	INR65SetWp(8, -2643, -401, -134)
	INR65SetWp(9, -2708, -401, 250)

	;the three breakers, down (OFF). Walls measured on the mesh, levers 9 units off the wall
	INR65MakeLever(r, 0, -2938.0, -230.0, -300.0, 90)  ;west records room, wall x -2947
	INR65MakeLever(r, 1, -2200.0, -230.0, -1115.0, 180) ;south wall z -1124
	INR65MakeLever(r, 2, -930.0, -214.0, 983.0, 0)      ;north-east wall z 992

	it = CreateItem("docnightshift", r\x - 2643.0 * RoomScale, r\y - 385.0 * RoomScale, r\z - 20.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("firstaid", r\x - 1152.0 * RoomScale, r\y - 370.0 * RoomScale, r\z + 120.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

Function INR65SetWp(i%, x#, y#, z#)
	INR65Wp(i, 0) = x : INR65Wp(i, 1) = y : INR65Wp(i, 2) = z
End Function

;baseYaw: the yaw that points the base into the wall
Function INR65MakeLever(r.Rooms, n%, lx#, ly#, lz#, baseYaw#)
	Local i%
	r\Objects[n * 2] = CopyEntity(LeverBaseOBJ)
	r\Objects[n * 2 + 1] = CopyEntity(LeverOBJ)
	r\Levers[n] = r\Objects[n * 2 + 1]
	For i = 0 To 1
		ScaleEntity(r\Objects[n * 2 + i], 0.04, 0.04, 0.04)
		PositionEntity(r\Objects[n * 2 + i], r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, True)
		EntityParent(r\Objects[n * 2 + i], r\obj)
	Next
	RotateEntity(r\Objects[n * 2], 0, baseYaw, 0)
	RotateEntity(r\Objects[n * 2 + 1], -80, baseYaw + 180, 0)
	EntityPickMode(r\Objects[n * 2 + 1], 1, False)
	EntityRadius(r\Objects[n * 2 + 1], 0.1)
End Function

Function INR65World(lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, INR65Room\obj, 0)
End Function

Function INR65LocalY#()
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, INR65Room\obj)
	Return TFormedY()
End Function

Function INR65Face(n.NPCs, ent%)
	If n = Null Then Return
	n\State = 0
	Local dx# = EntityX(ent, True) - EntityX(n\Collider, True), dz# = EntityZ(ent, True) - EntityZ(n\Collider, True)
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
End Function

Function INR65Say(who$, txt$, secs#)
	Msg = who + ": " + Chr(34) + txt + Chr(34)
	MsgTimer = 70 * secs
	INR65LineT = 70 * secs
End Function

Function INR65Flag%(f$)
	Return Instr(INR65E\EventStr, f) > 0
End Function

Function INR65SetFlag(f$)
	If Not INR65Flag(f) Then INR65E\EventStr = INR65E\EventStr + f
End Function

Function INR65Breakers%()
	Local n% = 0
	If INR65Flag("1") Then n = n + 1
	If INR65Flag("2") Then n = n + 1
	If INR65Flag("3") Then n = n + 1
	Return n
End Function

;Reyes: take back the one the save restored, or bring her back where the player can't see it
Function INR65GetDoc.NPCs()
	Local n.NPCs, wx#, wy#, wz#
	INR65World(0, 40, -200)
	wx = TFormedX() : wy = TFormedY() : wz = TFormedZ()
	For n = Each NPCs
		If n\NPCtype = NPCtypeClerk Then
			If Abs(EntityY(n\Collider, True) - wy) < 2.0 And Abs(EntityX(n\Collider, True) - wx) + Abs(EntityZ(n\Collider, True) - wz) < 6.0 Then Return n
		EndIf
	Next
	If Abs(EntityY(Collider, True) - wy) > 1.2 Or Abs(EntityX(Collider, True) - wx) + Abs(EntityZ(Collider, True) - wz) > 10.0 Then
		n = CreateNPC(NPCtypeClerk, wx, wy + 0.3, wz)
		n\State = 0 : n\State2 = 0
		RotateEntity(n\Collider, 0, EntityYaw(INR65Room\obj, True) + 90, 0)
		Return n
	EndIf
	Return Null
End Function

;room-local position of the player
Function INR65PlayerLocal()
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, INR65Room\obj)
End Function

;inside the room's whole mesh (upper corridor + the lower level that sticks out of the cell)?
Function INR65InArea%()
	If INR65Room = Null Then Return False
	INR65PlayerLocal()
	If TFormedX() < -3010 Or TFormedX() > 830 Then Return False
	If TFormedZ() < -1180 Or TFormedZ() > 1030 Then Return False
	If TFormedY() < -900 Or TFormedY() > 720 Then Return False
	;only the lower level is outside the normal cell; up top the usual room switching is fine
	If TFormedX() > -1000 And TFormedY() > -200 Then Return False
	Return True
End Function

;called from UpdateRooms: on the lower level this room stays the player's room, so it is never hidden
;(a hidden room has no collision - that's what dropped the player through the floor)
Function IndevForcePlayerRoom65%()
	If INR65Room = Null Then Return False
	If PlayerRoom = Null Then Return False
	If PlayerRoom <> INR65Room And EntityDistance(Collider, INR65Room\obj) > 14.0 Then Return False
	If Not INR65InArea() Then Return False
	PlayerRoom = INR65Room
	ShowEntity(INR65Room\obj)
	Return True
End Function

;fall safety: remember where the player last stood on a floor of this room, put them back if they drop out
Function INR65FallSafety()
	INR65PlayerLocal()
	Local lx# = TFormedX(), ly# = TFormedY(), lz# = TFormedZ()
	If ly < -560 Then
		If INR65HasSafe Then
			PositionEntity(Collider, INR65SafeX, INR65SafeY + 0.1, INR65SafeZ, True)
		Else
			INR65World(-1152, -330, 4)
			PositionEntity(Collider, TFormedX(), TFormedY(), TFormedZ(), True)
		EndIf
		ResetEntity(Collider)
		DropSpeed = 0
		CurrSpeed = 0
		Return
	EndIf
	If DropSpeed > -0.01 And DropSpeed < 0.01 And (ly > -420 And ly < -300 Or ly > -20 And ly < 120) Then
		INR65SafeX = EntityX(Collider, True) : INR65SafeY = EntityY(Collider, True) : INR65SafeZ = EntityZ(Collider, True)
		INR65HasSafe = True
	EndIf
End Function

;find an NPC of this type the save restored near a room-local spot, or make one where the player can't see it happen
Function INR65FindOrSpawn.NPCs(npctype%, lx#, ly#, lz#, yawOff#)
	Local n.NPCs, wx#, wy#, wz#
	INR65World(lx, ly + 40, lz)
	wx = TFormedX() : wy = TFormedY() : wz = TFormedZ()
	For n = Each NPCs
		If n\NPCtype = npctype And n <> INR65Doc And n <> INR65Tob And n <> INR65Hale Then
			If Abs(EntityY(n\Collider, True) - wy) < 1.2 And Abs(EntityX(n\Collider, True) - wx) + Abs(EntityZ(n\Collider, True) - wz) < 4.0 Then Return n
		EndIf
	Next
	If Abs(EntityY(Collider, True) - wy) > 1.2 Or Abs(EntityX(Collider, True) - wx) + Abs(EntityZ(Collider, True) - wz) > 9.0 Then
		n = CreateNPC(npctype, wx, wy + 0.3, wz)
		n\State = 0 : n\State2 = 0
		RotateEntity(n\Collider, 0, EntityYaw(INR65Room\obj, True) + yawOff, 0)
		Return n
	EndIf
	Return Null
End Function

;walk toward a room-local point (short, open stretches only); True when there
Function INR65WalkTo%(n.NPCs, lx#, lz#)
	If n = Null Then Return True
	INR65World(lx, 0, lz)
	Local dx# = TFormedX() - EntityX(n\Collider, True), dz# = TFormedZ() - EntityZ(n\Collider, True)
	If dx * dx + dz * dz < 0.3 * 0.3 Then n\State = 0 : Return True
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
	n\State = 1
	Return False
End Function

;the next breaker still down, as a direction the NPCs can give
Function INR65NextBreaker$()
	If Not INR65Flag("3") Then Return "the north-east wall, just past the bottom of the stairs"
	If Not INR65Flag("2") Then Return "the south wall, through the lockers"
	If Not INR65Flag("1") Then Return "the records room at the far west end"
	Return ""
End Function

;Technician Hale (upstairs by the crates) and Tobias (a Class-D hiding on the lower level)
Function INR65UpdateHelpers(ly#)
	Local d#
	If INR65E\EventState < 5 Then
		If INR65Hale = Null Then INR65Hale = INR65FindOrSpawn(NPCtypeClerk, 560.0, 0.0, 20.0, -90)
		If INR65Tob = Null And INR65E\EventState <= 3 Then INR65Tob = INR65FindOrSpawn(NPCtypeD, -2150.0, -401.0, 540.0, 180)
	EndIf

	If INR65Hale <> Null Then
		d = EntityDistance(INR65Hale\Collider, Collider)
		INR65Hale\State = 0
		If d < 8.0 Then INR65Face(INR65Hale, Collider)
		INR65HaleT = INR65HaleT - FPSfactor
		If INR65HaleT <= 0 And d < 3.0 And MsgTimer <= 0 Then
			INR65HaleT = 70*12
			If INR65E\EventState >= 4 Then
				Msg = "Technician Hale: " + Chr(34) + "Generator's holding at ninety percent. Don't go back down there anyway." + Chr(34)
			ElseIf INR65HaleLine = 0 Then
				INR65HaleLine = 1
				Msg = "Technician Hale: " + Chr(34) + "I tried the breakers myself. Got halfway down the stairs and it was standing at the bottom. Just... standing." + Chr(34)
			Else
				Msg = "Technician Hale: " + Chr(34) + "Breakers on so far: " + INR65Breakers() + " of 3. Next one's on " + INR65NextBreaker() + "." + Chr(34)
			EndIf
			MsgTimer = 70*6
		EndIf
	EndIf

	If INR65Tob <> Null Then
		d = EntityDistance(INR65Tob\Collider, Collider)
		If INR65E\EventState >= 4 Then
			;lights on: he makes for the stairs and is gone
			Select INR65TobStep
				Case 0 If INR65WalkTo(INR65Tob, -2000.0, 584.0) Then INR65TobStep = 1 ;through the gap in the wall at x -1592
				Case 1 If INR65WalkTo(INR65Tob, -1450.0, 584.0) Then INR65TobStep = 2
				Case 2 If INR65WalkTo(INR65Tob, -1152.0, 4.0) Then INR65TobStep = 3
				Default
					If d > 6.0 Or (Not EntityInView(INR65Tob\Collider, Camera)) Then RemoveNPC(INR65Tob) : INR65Tob = Null
			End Select
			If INR65Tob <> Null And INR65TobLine < 9 And d < 5.0 Then
				INR65TobLine = 9
				Msg = "Tobias: " + Chr(34) + "Lights! You did it! I'm not staying down here another second." + Chr(34)
				MsgTimer = 70*4
			EndIf
		Else
			INR65Tob\State = 0
			If d < 8.0 Then INR65Face(INR65Tob, Collider)
			INR65TobT = INR65TobT - FPSfactor
			If INR65TobT <= 0 And d < 3.5 And MsgTimer <= 0 Then
				INR65TobT = 70*9
				Select INR65TobLine
					Case 0 Msg = "Tobias: " + Chr(34) + "Shh! Don't - don't look away from the dark. It's out there. It was standing where you are an hour ago." + Chr(34)
					Case 1 Msg = "Tobias: " + Chr(34) + "When you blink, it gets closer. Stare at it and it goes. Count to three in your head." + Chr(34)
					Default Msg = "Tobias: " + Chr(34) + "The next breaker's on " + INR65NextBreaker() + ". I'm not moving till the lights come on." + Chr(34)
				End Select
				If INR65TobLine < 2 Then INR65TobLine = INR65TobLine + 1
				MsgTimer = 70*6
			EndIf
		EndIf
	EndIf
End Function

Function UpdateIndevNewRoom65()
	If INR65Room = Null Then Return
	If INR65E = Null Then
		Local e.Events
		For e = Each Events
			If e\EventName = "room2newroom65" Then INR65E = e : Exit
		Next
		If INR65E = Null Then Return
	EndIf

	;out of the room: the event stops - the Hollow is gone and nobody moves
	If PlayerRoom <> INR65Room And (Not INR65InArea()) Then
		INR65HideHollow(70*4)
		INR65Wind = 0
		If INR65Doc <> Null Then INR65Doc\State = 0
		If INR65Hale <> Null Then INR65Hale\State = 0
		If INR65Tob <> Null Then INR65Tob\State = 0
		If INR65E\EventState = 5 Then
			If INR65Doc <> Null Then RemoveNPC(INR65Doc) : INR65Doc = Null
			If INR65Hale <> Null Then RemoveNPC(INR65Hale) : INR65Hale = Null
			If INR65Tob <> Null Then RemoveNPC(INR65Tob) : INR65Tob = Null
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return
	INR65FallSafety()

	Local ly# = INR65LocalY(), d#, i%

	;breakers: levers stay where the saved flags say
	If Not INR65Synced Then
		INR65Synced = True
		For i = 0 To 2
			If INR65Flag(Str(i + 1)) Then RotateEntity(INR65Room\Objects[i * 2 + 1], 80, EntityYaw(INR65Room\Objects[i * 2 + 1]), 0)
		Next
	EndIf
	For i = 0 To 2
		Local lv% = INR65Room\Objects[i * 2 + 1]
		If lv <> 0 Then
			Local on% = UpdateLever(lv, INR65Flag(Str(i + 1)))
			If on And (Not INR65Flag(Str(i + 1))) Then
				INR65SetFlag(Str(i + 1))
				PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
				LightBlink = 1.0
				Select INR65Breakers()
					Case 1 Msg = "The breaker thunks into place. Somewhere a single tube light buzzes on, then dies again. Two more."
					Case 2 Msg = "Second breaker. The emergency lights stutter. Something in the dark makes a sound like a held breath. One more."
					Default Msg = "The last breaker slams home."
				End Select
				MsgTimer = 70*5
				If INR65E\EventState < 3 Then INR65E\EventState = 3
			EndIf
		EndIf
	Next

	;Reyes after loading a save
	INR65AdoptT = INR65AdoptT - FPSfactor
	If INR65AdoptT <= 0 And INR65Doc = Null And INR65E\EventState >= 1 And INR65E\EventState <= 4 Then
		INR65AdoptT = 70
		If Not (INR65E\EventState = 4 And INR65Flag("g")) Then INR65Doc = INR65GetDoc()
		If INR65Doc <> Null And INR65E\EventState <= 2 Then INR65E\EventState = 3
	EndIf

	If INR65E\EventState >= 1 Then INR65UpdateHelpers(ly)

	Select INR65E\EventState
		Case 0 ;the player walks in
			If ly < -200 Then
				INR65E\EventState = 3
				Msg = "It's cold down here, and so dark the stair rail disappears under your hand."
				MsgTimer = 70*5
			Else
				INR65World(0, 40, -200)
				INR65Doc = CreateNPC(NPCtypeClerk, TFormedX(), TFormedY() + 0.3, TFormedZ())
				INR65Doc\State = 0 : INR65Doc\State2 = 0
				INR65Nags = 0 : INR65NagT = 0
				INR65E\EventState = 1
			EndIf

		Case 1 ;Reyes waits by the stairs
			INR65Face(INR65Doc, Collider)
			If ly < -200 Then
				INR65E\EventState = 3
			ElseIf INR65Doc <> Null Then
				d = EntityDistance(INR65Doc\Collider, Collider)
				INR65NagT = INR65NagT - FPSfactor
				If d < 3.2 Then
					INR65E\EventState = 2 : INR65Line = 0 : INR65LineT = 0
				ElseIf INR65NagT <= 0 And INR65Nags < 3 And d < 10.0 Then
					INR65Nags = INR65Nags + 1 : INR65NagT = 70*10
					INR65Say("Dr. Reyes", "Don't go down those stairs. Not yet. Come here first.", 4)
				EndIf
			EndIf

		Case 2 ;the talk
			INR65Face(INR65Doc, Collider)
			If ly < -200 Then INR65E\EventState = 3
			INR65LineT = INR65LineT - FPSfactor
			If INR65LineT <= 0 Then
				Select INR65Line
					Case 0 INR65Say("Dr. Reyes", "The lower level lost power when the breach started. Something came out of the dark with it. We call it the Hollow.", 6)
					Case 1 INR65Say("Dr. Reyes", "It only moves when nobody is looking at it. Keep your eyes on it and it backs off. Turn around and it's on you.", 6)
					Case 2 INR65Say("Dr. Reyes", "There are three breaker levers down there. Records room at the far end, the south wall, the north-east wall. Pull them UP.", 7)
					Case 3 INR65Say("Dr. Reyes", "Light burns it away. Get all three on and I'll give you my night vision goggles. Deal?", 5)
					Case 4 INR65Say("Dr. Reyes", "And whatever you do - don't blink when it's close.", 4)
					Default
						INR65E\EventState = 3
				End Select
				INR65Line = INR65Line + 1
			EndIf

		Case 3 ;the hunt
			If INR65Doc <> Null Then INR65Face(INR65Doc, Collider)
			If ly < -200 Then
				INR65UpdateHollow()
			Else
				INR65HideHollow(70*3)
			EndIf
			If INR65Breakers() >= 3 Then INR65Restore()

		Case 4 ;power's back: Reyes pays up
			INR65HideHollow(70*60)
			If INR65Doc <> Null Then
				INR65Face(INR65Doc, Collider)
				If (Not INR65Flag("g")) And EntityDistance(INR65Doc\Collider, Collider) < 3.0 Then
					INR65SetFlag("g")
					Local it.Items = CreateItem("nvgoggles", EntityX(INR65Doc\Collider, True), EntityY(INR65Doc\Collider, True) + 0.1, EntityZ(INR65Doc\Collider, True))
					INR65Say("Dr. Reyes", "The lights are on. I heard it scream all the way up here. Here - the goggles. You earned them.", 6)
					INR65E\EventState = 5
				EndIf
			ElseIf Not INR65Flag("g") Then
				INR65SetFlag("g")
				INR65World(0, 30, -200)
				it = CreateItem("nvgoggles", TFormedX(), TFormedY(), TFormedZ())
				INR65E\EventState = 5
			EndIf

		Case 5 ;done
	End Select
End Function

Function INR65Restore()
	Local j%, pp.Particles
	INR65E\EventState = 4
	PlaySound_Strict(LoadTempSound("SFX\General\GeneratorOn.ogg"))
	LightBlink = 0
	If INR65Hollow <> 0 And INR65HState = 1 Then
		For j = 0 To 14
			pp = CreateParticle(EntityX(INR65Hollow, True) + Rnd(-0.2, 0.2), EntityY(INR65Hollow, True) + Rnd(0.1, 1.6), EntityZ(INR65Hollow, True) + Rnd(-0.2, 0.2), 0, Rnd(0.15, 0.35), -0.2, 180)
			pp\speed = Rnd(0.002, 0.008) : pp\SizeChange = 0.01 : pp\Achange = -0.005
			pp\R = 30 : pp\G = 30 : pp\B = 30
			RotateEntity(pp\pvt, Rnd(-60, 0), Rnd(360), 0)
		Next
		PlaySound2(LoadTempSound("SFX\General\Hiss.ogg"), Camera, INR65Hollow, 10.0)
	EndIf
	INR65HideHollow(70*60)
	Msg = "A generator roars. Every light on the level snaps on at once - and something at the edge of the room shrieks and comes apart like smoke."
	MsgTimer = 70*7
	IndevRelieveStress(40)
End Function

;----------------------------------------------------------------- the Hollow

Function INR65ColorAll(ent%, r%, g%, b%)
	Local i%
	If EntityClass(ent) = "Mesh" Then EntityColor(ent, r, g, b)
	For i = 1 To CountChildren(ent)
		INR65ColorAll(GetChild(ent, i), r, g, b)
	Next
End Function

Function INR65HideHollow(cool#)
	If INR65Hollow <> 0 And INR65HState = 1 Then HideEntity(INR65Hollow) : HideEntity(INR65Head)
	INR65Wind = 0
	INR65HState = 0
	INR65HCool = Max(INR65HCool, cool)
	INR65HGaze = 0
End Function

;put it on waypoint i, standing on the floor, facing the player
Function INR65PlaceHollow(i%)
	If INR65Hollow = 0 Then
		INR65Hollow = CopyEntity(ClassDObj)
		Local sc# = 0.5 / MeshWidth(INR65Hollow)
		ScaleEntity(INR65Hollow, sc, sc, sc)
		EntityFX(INR65Hollow, 1)
		INR65ColorAll(INR65Hollow, 14, 14, 18)
		MeshCullBox(INR65Hollow, -MeshWidth(ClassDObj), -MeshHeight(ClassDObj), -MeshDepth(ClassDObj)*4, MeshWidth(ClassDObj)*2, MeshHeight(ClassDObj)*2, MeshDepth(ClassDObj)*8)
		INR65Head = CreatePivot()
		;two pale pinprick eyes, so it can be spotted in the dark
		Local k%, eye%
		For k = 0 To 1
			eye = CreateSprite(INR65Head)
			ScaleSprite(eye, 0.018, 0.012)
			EntityFX(eye, 1 + 8)
			EntityColor(eye, 230, 235, 255)
			EntityOrder(eye, -1)
			PositionEntity(eye, -0.06 + 0.12 * k, 0.12, 0)
		Next
		;parented to the room so it goes away with the map
		EntityParent(INR65Hollow, INR65Room\obj, True)
		EntityParent(INR65Head, INR65Room\obj, True)
	EndIf
	INR65HWp = i
	INR65World(INR65Wp(i, 0), INR65Wp(i, 1), INR65Wp(i, 2))
	PositionEntity(INR65Hollow, TFormedX(), TFormedY(), TFormedZ(), True)
	INR65FaceHollow()
	ShowEntity(INR65Hollow)
	ShowEntity(INR65Head)
	INR65HState = 1
End Function

Function INR65FaceHollow()
	Local dx# = EntityX(Collider, True) - EntityX(INR65Hollow, True), dz# = EntityZ(Collider, True) - EntityZ(INR65Hollow, True)
	RotateEntity(INR65Hollow, 0, VectorYaw(dx, 0, dz) + 180, 0, True)
	PositionEntity(INR65Head, EntityX(INR65Hollow, True), EntityY(INR65Hollow, True) + 1.4, EntityZ(INR65Hollow, True), True)
	RotateEntity(INR65Head, 0, EntityYaw(INR65Hollow, True) + 180, 0, True)
End Function

;can the camera see waypoint i's head height?
Function INR65WpVisible%(i%)
	INR65World(INR65Wp(i, 0), INR65Wp(i, 1) + 340, INR65Wp(i, 2))
	Local p% = CreatePivot()
	PositionEntity(p, TFormedX(), TFormedY(), TFormedZ(), True)
	Local v% = EntityVisible(Camera, p) And EntityInView(p, Camera)
	Local dd# = EntityDistance(p, Collider)
	FreeEntity(p)
	If dd < 4.0 Then Return True
	Return v
End Function

Function INR65UpdateHollow()
	Local i%, d#, best%, bd#, dd#
	If INR65HState = 0 Then
		INR65HCool = INR65HCool - FPSfactor
		If INR65HCool > 0 Then Return
		;appear somewhere out of sight, not too close
		best = -1 : bd = 0
		For i = 0 To 9
			INR65World(INR65Wp(i, 0), INR65Wp(i, 1), INR65Wp(i, 2))
			dd = Abs(TFormedX() - EntityX(Collider, True)) + Abs(TFormedZ() - EntityZ(Collider, True))
			If dd > 7.0 And (Not INR65WpVisible(i)) Then
				If best = -1 Or Rand(3) = 1 Then best = i
			EndIf
		Next
		If best = -1 Then INR65HCool = 70 : Return
		INR65PlaceHollow(best)
		INR65HJump = 70*3 : INR65HGaze = 0
		Return
	EndIf

	INR65FaceHollow()
	d = EntityDistance(INR65Hollow, Collider)

	;the dark gets worse the closer it is
	If d < 6.0 Then
		If Rand(Int(Max(8, d * 25))) = 1 Then LightBlink = Max(LightBlink, Rnd(0.3, 1.2))
		IndevStress = Min(100, IndevStress + 0.03 * FPSfactor)
	ElseIf Rand(700) = 1 Then
		LightBlink = Max(LightBlink, Rnd(0.3, 0.8))
	EndIf

	;is the player looking at it? (eyes open, in view, nothing in between)
	Local seen% = False
	If BlinkTimer > -6 And d < 14.0 Then
		If EntityInView(INR65Head, Camera) Then seen = EntityVisible(Camera, INR65Head)
	EndIf

	If seen Then
		If INR65Wind > 0 Then INR65HGaze = 70*3 ;caught it reaching for you
		INR65Wind = 0
		INR65HGaze = INR65HGaze + FPSfactor
		If INR65HGaze > 70*2.5 Then
			;stared down: it flinches back into the dark
			PlaySound2(LoadTempSound("SFX\General\Hiss.ogg"), Camera, INR65Hollow, 8.0, 0.7)
			Msg = "It twitches under your stare, folds in on itself and is simply not there any more."
			MsgTimer = 70*3
			INR65HideHollow(70 * Rnd(6, 10))
		EndIf
		Return
	EndIf
	INR65HGaze = Max(0, INR65HGaze - FPSfactor * 0.5)

	;not watched: close in. In the open it glides straight at the player, otherwise it jumps between spots
	Local los% = EntityVisible(INR65Head, Camera)
	If d < 8.0 And los Then
		Local dx# = EntityX(Collider, True) - EntityX(INR65Hollow, True), dz# = EntityZ(Collider, True) - EntityZ(INR65Hollow, True)
		Local l# = Sqr(dx * dx + dz * dz)
		If l > 0.01 Then
			Local spd# = Min(0.045 * FPSfactor, Max(0, l - 0.9))
			TranslateEntity(INR65Hollow, dx / l * spd, 0, dz / l * spd, True)
		EndIf
		INR65FaceHollow()
		INR65Whisper = INR65Whisper - FPSfactor
		If INR65Whisper <= 0 Then
			INR65Whisper = 70*4
			PlaySound2(LoadTempSound("SFX\General\BodyFall.ogg"), Camera, INR65Hollow, 6.0, 0.4)
		EndIf
		;within arm's reach it winds up first - a loud breath, one second to turn around
		If l < 1.3 Then
			If INR65Wind <= 0 Then
				INR65Wind = 70*1.1
				PlaySound2(LoadTempSound("SFX\General\Hiss.ogg"), Camera, INR65Hollow, 5.0, 1.0)
				CameraShake = Max(CameraShake, 0.8)
				Msg = "Cold breath on the back of your neck. TURN AROUND."
				MsgTimer = 70*2
			Else
				INR65Wind = INR65Wind - FPSfactor
				If INR65Wind <= 0 Then INR65Catch()
			EndIf
		EndIf
	Else
		INR65HJump = INR65HJump - FPSfactor
		If INR65HJump <= 0 Then
			INR65HJump = 70 * Rnd(2.0, 3.5)
			;the unseen spot closest to the player, but not on top of them
			best = -1 : bd = 999
			For i = 0 To 9
				INR65World(INR65Wp(i, 0), INR65Wp(i, 1), INR65Wp(i, 2))
				dd = Abs(TFormedX() - EntityX(Collider, True)) + Abs(TFormedZ() - EntityZ(Collider, True))
				If dd > 3.0 And dd < bd And i <> INR65HWp And (Not INR65WpVisible(i)) Then best = i : bd = dd
			Next
			If best >= 0 Then INR65PlaceHollow(best)
		EndIf
	EndIf
End Function

Function INR65Catch()
	INR65E\EventState3 = INR65E\EventState3 + 1
	PlaySound_Strict(LoadTempSound("SFX\General\Slash" + Rand(1, 2) + ".ogg"))
	CameraShake = 3.0
	BlurTimer = 70*4
	LightBlink = 4.0
	If INR65E\EventState3 >= 3 Then
		DeathMSG = "Subject D-9341 was found on the lower level of the storage block after power was restored. No external injuries. "
		DeathMSG = DeathMSG + "The body was cold to the touch and the eyes were completely black. Recommend the level be kept lit at all times."
		Kill()
	Else
		;numbing cold rather than wounds: the player never bleeds out because of it
		Injuries = Min(Injuries + 0.25, Max(Injuries, 0.9))
		Stamina = 0
		IndevStress = Min(100, IndevStress + 25)
		If INR65E\EventState3 = 1 Then
			Msg = "Something cold pushes straight through you. For a second you can't remember what light looks like."
		Else
			Msg = "It gets you again. Your fingers are numb and grey. Once more and you won't be walking out of here."
		EndIf
		MsgTimer = 70*6
	EndIf
	INR65HideHollow(70*15)
End Function
