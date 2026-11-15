;=====================================================================
; SCP: Containment Breach - Indev: the forty-fourth batch - the early SCP-1074 room and five distinctive sites
;
;   room2b46old1074  the early SCP-1074 event: the painting tipped against the wall beside the dead researcher -
;                    look at it too long and the room swims, your heart races, and you collapse
;   room2b46cryo     Pod 4 knocks; the cryo hall is so cold your stamina will not recover past half
;   room2b46theatre  the PA microphone; murmurs from an empty gallery; applause when you step onto the stage
;   room2b46gravity  floating crates; on the chamber floor you move a third faster (IndevSpeedMul); the field
;                    switch drops everything
;   room2b46geology  tremors every minute or so; the crystal hums - it soothes and gives you headaches
;   room2b46o5vault  the records terminal: a Level 5 card or better gets you the index card
;=====================================================================

Global I44Gaze#, I44GazeCD#, I44Faints%
Global I44Grav%, I44Field% = True, I44Bob#
Global I44Murmur%, I44Applause%, I44Tremor#, I44O5%, I44Cold#
Dim I44Crate%(5), I44CrateX#(5), I44CrateY#(5), I44CrateZ#(5)

Function Indev44Reset(newGame%)
	If newGame Then
		I44Faints = 0 : I44O5 = False
	EndIf
	I44Gaze = 0 : I44GazeCD = 0 : I44Grav = False : I44Field = True
	I44Murmur = False : I44Applause = False : I44Tremor = 70 * 40 : I44Cold = 0
End Function

;the multiplier IndevSpeedMul gets through U36SpeedMul (IndevU36.bb)
Function U44SpeedMul#()
	If I44Grav And I44Field Then Return 1.33
	Return 1.0
End Function

;the floating crates of the gravity chamber (runtime, so they can bob and fall)
Function IndevU44Dress(r.Rooms)
	Local k%, tex%
	If r\RoomTemplate\Name <> "room2b46gravity" Then Return
	tex = LoadTexture_Strict("GFX\map\indev_b35crate.png", 1)
	For k = 0 To 5
		I44Crate(k) = CreateCube()
		ScaleEntity(I44Crate(k), 40 * RoomScale, 40 * RoomScale, 40 * RoomScale)
		If tex <> 0 Then EntityTexture(I44Crate(k), tex)
		I44CrateX(k) = 420 + (k Mod 3) * 210 : I44CrateZ(k) = -500 + (k / 3) * 1000 + Rnd(-120, 120)
		I44CrateY(k) = 200 + Rnd(0, 300)
		IxPlace(I44Crate(k), r, I44CrateX(k), I44CrateY(k), I44CrateZ(k))
		TurnEntity(I44Crate(k), Rnd(360), Rnd(360), Rnd(360))
		EntityParent(I44Crate(k), r\obj, True)
	Next
	If tex <> 0 Then FreeTexture(tex)
End Function

Function UpdateIndevU44(e.Events)
	Local r.Rooms = e\room, lx#, k%, d#, y#
	If e\EventState = 0 And r\dist < 12 And r\RoomTemplate\Name = "room2b46old1074" Then
		e\EventState = 1
		r\NPC[0] = U41Body(r, r\Objects[U44_O74_BODY], 200)
	EndIf
	;the crates float whether or not you are in the room (as long as it is near)
	If r\RoomTemplate\Name = "room2b46gravity" And r\dist < 10 And I44Crate(0) <> 0 Then
		I44Bob = I44Bob + FPSfactor
		For k = 0 To 5
			If I44Field Then
				y = I44CrateY(k) + Sin(I44Bob * 1.2 + k * 60) * 30
				TurnEntity(I44Crate(k), 0.1 * FPSfactor, 0.15 * FPSfactor, 0)
			Else
				y = 40
			EndIf
			IxPlace(I44Crate(k), r, I44CrateX(k), y, I44CrateZ(k))
		Next
	EndIf
	If PlayerRoom <> r Then
		If r\RoomTemplate\Name = "room2b46gravity" Then I44Grav = False
		Return
	EndIf
	lx = U37LX(r)
	Select r\RoomTemplate\Name
		;---------------- the early SCP-1074 room
		Case "room2b46old1074"
			If I44GazeCD > 0 Then I44GazeCD = I44GazeCD - FPSfactor
			d = EntityDistance(Collider, r\Objects[U44_O74_PAINTING])
			If d < 3.0 And I44GazeCD <= 0 And KillTimer >= 0 And EntityInView(r\Objects[U44_O74_PAINTING], Camera) Then
				I44Gaze = I44Gaze + FPSfactor
				If I44Gaze > 70 * 4 And I44Gaze - FPSfactor <= 70 * 4 Then
					IndevStress = Min(100, IndevStress + 10)
					BlurTimer = 70 * 3
					IS16Tell("The painting is beautiful. That's all it is - and it is so beautiful your eyes sting. Your heart is going much too fast.", 7)
				EndIf
				If I44Gaze > 70 * 8 Then
					I44Gaze = 0 : I44GazeCD = 70 * 25 : I44Faints = I44Faints + 1
					Stamina = 0 : BlurTimer = 70 * 7 : CameraShake = 3.0
					Injuries = Injuries + 0.35
					IS16Tell("The room swims, colours too bright, and the floor comes up to meet you. When you can see again you're lying next to him, reaching for the painting just as he was.", 9)
				EndIf
			Else
				I44Gaze = Max(0, I44Gaze - FPSfactor * 2)
			EndIf
		;---------------- cryo
		Case "room2b46cryo"
			If lx > 256 Then
				Stamina = Min(Stamina, 55)
				I44Cold = I44Cold + FPSfactor
				If I44Cold > 70 * 20 Then
					I44Cold = 0
					IS16Tell("Your breath fogs. The LN2 lines tick. You can't get your breath back properly in this cold.", 4)
				EndIf
			EndIf
			If IS10Press(r\Objects[U44_CRY_POD4], 1.8) Then
				CameraShake = 1.0
				IndevStress = Min(100, IndevStress + 8)
				IS16Tell("POD 4 - OCCUPANT: DECEASED. Behind the frost, a dark shape. You put your hand on the glass. From inside, three knocks answer it.", 8)
			EndIf
		;---------------- the theatre
		Case "room2b46theatre"
			If lx > 256 And (Not I44Murmur) Then
				I44Murmur = True
				IS16Tell("As you step in, a murmur runs round the gallery - an audience settling in their seats. Every seat you can see is empty.", 7)
			EndIf
			If EntityDistance(Collider, r\Objects[U44_THT_STAGE]) < 1.2 And (Not I44Applause) Then
				I44Applause = True
				IndevStress = Min(100, IndevStress + 6)
				IS16Tell("You step into the light. From the empty gallery, slow, polite applause.", 6)
			EndIf
			If IS10Press(r\Objects[U44_THT_MIC], 1.4) Then
				IS16Tell("You key the microphone. Your voice booms round the empty theatre: '...hello?' The gallery answers, all at once, in whispers: 'Begin.'", 8)
			EndIf
		;---------------- gravity
		Case "room2b46gravity"
			I44Grav = (lx > 256)
			If IS10Press(r\Objects[U44_GRV_FIELD], 1.8) Then
				I44Field = 1 - I44Field
				CameraShake = 2.0
				If I44Field Then
					IS16Tell("FIELD: ON. A hum climbs out of the floor rings. Through the feed, the crates lift off the floor and drift upward.", 6)
				Else
					IS16Tell("FIELD: OFF. On the feed, every crate in the chamber drops at once. The bang comes through the wall a moment later.", 6)
				EndIf
			EndIf
			If I44Grav And I44Field And e\EventState3 = 0 Then
				e\EventState3 = 1
				IS16Tell("Your next step goes much too far. You weigh almost nothing. Stopping is going to be the hard part.", 6)
			EndIf
		;---------------- geology
		Case "room2b46geology"
			I44Tremor = I44Tremor - FPSfactor
			If I44Tremor <= 0 Then
				I44Tremor = 70 * Rnd(40, 75)
				CameraShake = 2.5
				Select Rand(3)
					Case 1 : IS16Tell("A tremor rolls through the rock. Dust sifts down from the cavern roof.", 4)
					Case 2 : IS16Tell("The ground shudders. The seismograph needle swings, and the crystal brightens for a moment.", 4)
					Default : IS16Tell("Deep below, something shifts. The crystal's hum climbs half a tone and stays there.", 4)
				End Select
			EndIf
			If EntityDistance(Collider, r\Objects[U44_GEO_CRYSTAL]) < 2.0 And Rand(300) = 1 Then
				IndevRelieveStress(3)
				BlurTimer = Max(BlurTimer, 70)
				IS16Tell("The crystal's hum is in your teeth. It's calming. Your head aches.", 4)
			EndIf
			If IS10Press(r\Objects[U44_GEO_SEISMO], 1.8) Then
				IS16Tell("The seismograph trace: a tremor every few minutes, all centred on the crystal, each a little stronger than the last.", 6)
			EndIf
		;---------------- the O5 vault
		Case "room2b46o5vault"
			If IS10Press(r\Objects[U44_O5V_TERMINAL], 1.6) Then
				If U43BestCard() >= 5 And (Not I44O5) Then
					I44O5 = True
					IS16Give("docb44_o5", r\Objects[U44_O5V_TERMINAL])
					IS16Tell("CLEARANCE ACCEPTED. The terminal prints an index card and pushes it out of a slot. Everything else on the screen is black bars.", 7)
				ElseIf I44O5 Then
					IS16Tell("The terminal shows the same black bars. One line is readable: VOLUME 1 - CHECKED OUT.", 5)
				Else
					IS16Tell("O5 RECORDS - ACCESS DENIED. Insert O5 or delegate authorisation. (A Level 5 card or better might do.)", 6)
				EndIf
			EndIf
	End Select
End Function
