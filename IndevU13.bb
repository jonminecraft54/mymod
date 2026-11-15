;=====================================================================
; SCP: Containment Breach - Indev: thirteenth batch, six rooms for sixteen SCPs
;
;   room2safewing    LCZ  break room: SCP-377 cookies, SCP-978 camera, SCP-3041 knife; PC room: SCP-3045
;   room2biowing     HCZ  vase chamber: SCP-019; ball locker: SCP-3046 (its phone rings); SCP-3056 shelf
;   room2doorhall    HCZ  door 249 in the south arm (walk through it and you come out somewhere else),
;                        SCP-3038 white door in the north arm, SCP-1983 farmhouse east
;   room2menagerie   HCZ  SCP-247 enclosure; SCP-1762 box in the stores
;   room2pool354     HCZ  lift down to the red pool, SCP-354
;   room2incidents   LCZ  SCP-4666 office, SCP-1337 records, SCP-5094 PC in the north arm
;
;   IndevU13Data.bb is generated (Tools\roomkit\gen_b13.py): the U13_* constants, the FillRoom table and the
;   event list. This file holds what the table calls by name, and the two behaviours of the batch:
;     SCP-249  the door in room2doorhall: once it is open, walking into it sends you to a random other room
;     SCP-3046 the phone in room2biowing: after a few minutes in the room, it rings and a voice offers a deal
;     SCP-5094 the monitor in room2incidents: click it and Miss J teaches a nine-step lesson on the screen
;   Everything else in the batch is geometry, items and notes.
;=====================================================================

Function IndevU13Dress(r.Rooms)
	Local m%, tex%
	Select r\RoomTemplate\Name
		Case "room2incidents"
			;SCP-5094's screen: a quad hung just in front of the monitor, hidden until the lesson starts
			m = IS10Quad(72.0, 46.0, True, False)
			IS10OnPivot(m, r\Objects[U13_INC_PC])
			RotateEntity(m, 0, -90, 0) ;faces the player in the south arm, and reads the right way round
			PositionEntity(m, 0, 0, -1.5 * RoomScale)
			tex = LoadTexture_Strict("GFX\map\indev_5094on.png")
			EntityTexture(m, tex)
			FreeTexture(tex)
			HideEntity(m)
			r\Objects[U13_INC_SCREEN] = m
	End Select
End Function

Function UpdateIndevU13(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2doorhall"
			UpdateU13Door249(e)
		Case "room2biowing"
			UpdateU13Phone(e)
		Case "room2incidents"
			UpdateU13Miss(e)
		Case "room2pool354"
			IndevLiftTick(e) ;the lift down to the pool
	End Select
End Function

;SCP-5094, Miss J's Whiz Kidz Schoolhouse. Click the monitor and she starts a lesson on the screen. The lesson runs
;while you are in the room and waits while you are out of it. It is nine steps, and it is not finished until the last.
;EventState: 0 the monitor is off, 1 the lesson runs, 2 the class is dismissed.
;EventState2: frames since the last step.   EventState3: the step (0 to 8).
Function UpdateU13Miss(e.Events)
	Local r.Rooms = e\room, pc% = r\Objects[U13_INC_PC], scr% = r\Objects[U13_INC_SCREEN]
	If PlayerRoom <> r Then Return
	Select Int(e\EventState)
		Case 0
			If IS10Press(pc, 2.5) Then
				e\EventState = 1
				e\EventState2 = 0
				e\EventState3 = 0
				ShowEntity(scr)
				IS16Tell("The screen wakes up. A cartoon teacher waves from a classroom. Hello, student. Sit down, we will begin.", 9)
			EndIf
		Case 1
			ShowEntity(scr)
			e\EventState2 = e\EventState2 + FPSfactor
			;the lesson holds you: the longer you sit through it, the harder it is to get up
			IndevStress = Min(100, IndevStress + 0.004 * FPSfactor)
			If IS10Press(pc, 2.5) Then IS16Tell("Miss J: Eyes on the screen, student. We are not finished.", 5)
			If e\EventState2 > 70 * 9 Then
				e\EventState2 = 0
				IS16Tell(MissJLine(Int(e\EventState3)), 8)
				e\EventState3 = e\EventState3 + 1
				If e\EventState3 > 8 Then
					e\EventState = 2
					HideEntity(scr)
				EndIf
			EndIf
		Case 2
			If IS10Press(pc, 2.5) Then IS16Tell("The screen shows an empty classroom. Come back tomorrow for the next lesson.", 7)
	End Select
End Function

;the lesson, one line per step
Function MissJLine$(k%)
	Select k
		Case 0
			Return "Miss J: A is for apple. Say it with me. Apple."
		Case 1
			Return "Miss J: B is for ball. Balls are round, like the lamp in the hall."
		Case 2
			Return "Miss J: C is for cat. Cats are very patient. Are you?"
		Case 3
			Return "Miss J: Now colours. Red, like the apple. Green, like grass you have never seen."
		Case 4
			Return "Miss J: Blue is the colour of the sky, and of this room, a little."
		Case 5
			Return "Miss J: Numbers. One. Two. Three. Who is counting you?"
		Case 6
			Return "Miss J: Cubist sculpture is a thing seen from every side at once. Look at me from every side."
		Case 7
			Return "Miss J: We still have three more hours. Stay seated. I will be right here."
		Default
			Return "Miss J: Class is dismissed! You were a very good student. Come back tomorrow."
	End Select
End Function

;SCP-249: the door in the south arm. Walk into it while it is open and you come out in another room of this map.
;EventState is the time (MilliSecs) before the door may send anybody again.
Function UpdateU13Door249(e.Events)
	Local r.Rooms = e\room, d.Doors = r\RoomDoors[U13_DRH_D_249]
	Local r2.Rooms, n%, pick%, k%
	If d = Null Then Return
	If PlayerRoom <> r Then Return
	If Not d\open Then Return
	If MilliSecs() < e\EventState Then Return
	If EntityDistance(Collider, d\obj) > 0.6 Then Return
	;count the other rooms, then take one of them at random
	For r2 = Each Rooms
		If r2 <> r Then n = n + 1
	Next
	If n = 0 Then Return
	pick = Rand(1, n)
	k = 0
	For r2 = Each Rooms
		If r2 <> r Then
			k = k + 1
			If k = pick Then Exit
		EndIf
	Next
	e\EventState = MilliSecs() + 4000
	PositionEntity(Collider, EntityX(r2\obj), EntityY(r2\obj) + 0.7, EntityZ(r2\obj))
	ResetEntity(Collider)
	UpdateDoors()
	UpdateRooms()
	PlayerRoom = r2
	IS10Sound("SFX\Indev\poof.wav", Collider, 8.0, 1.0)
	IS16Tell("You step through the door. The hall is behind you, and so is a different hall.", 8)
End Function

;SCP-3046: after a few minutes in the biohazard wing, the phone in the ball locker rings, once.
;flag r = it has rung. EventState counts frames while the player is in the room.
Function UpdateU13Phone(e.Events)
	Local r.Rooms = e\room, ph% = r\Objects[U13_BIO_PHONE]
	If PlayerRoom <> r Then Return
	If IAxFlag(e, "r") Then Return
	e\EventState = e\EventState + FPSfactor
	If e\EventState > 70 * 60 * 4 Then
		IAxSetFlag(e, "r")
		IS10Sound("SFX\Indev\doorbell.wav", ph, 8.0, 1.0)
		IS16Tell("A phone rings in the ball locker. A woman's voice, nasal, says she can take it off you for a fee.", 9)
	EndIf
End Function
