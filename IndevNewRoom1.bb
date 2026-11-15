;=====================================================================
; SCP: Containment Breach - Indev event: room2newroom1 "Sublevel Blackout"
;
;   room2newroom1: a corridor, a tall hall behind a doorway (local x -224),
;   and a ramp from that doorway down to a sunken sublevel (floor y -384).
;
;   1  when the player walks into the room, a researcher (Dr. Harlan) and a
;      Class-D (Rodriguez) walk in from the far entrance and stop by the hall
;   2  when the player comes close they talk to the player (a short scene)
;   3  Rodriguez walks through the doorway and down the ramp into the sublevel
;   4  when he reaches the bottom - or the player goes down first - the
;      lights die. In the dark Rodriguez screams and is gone; only blood is left
;   5  the generator brings the lights back; Harlan panics and runs out of the room
;   The sublevel holds a maintenance log and a first aid kit.
;   Runs once per map.
;=====================================================================

Global INR1Room.Rooms, INR1State%, INR1Timer#, INR1Next#
Global INR1Doc.NPCs, INR1D.NPCs, INR1DStep%, INR1DocStep%
Global INR1Line%, INR1LineT#

Const INR1_TALKLINES% = 7

Function IndevNewRoom1Reset()
	INR1Room = Null : INR1State = 0 : INR1Timer = 0 : INR1Next = 0
	INR1Doc = Null : INR1D = Null : INR1DStep = 0 : INR1DocStep = 0
	INR1Line = 0 : INR1LineT = 0
End Function

;called from FillRoom
Function IndevFillNewRoom1(r.Rooms)
	Local it.Items
	INR1Room = r : INR1State = 0
	;sublevel floor at y -384, spots checked against the room mesh (clear for 290+ units around)
	it = CreateItem("docsublevel", r\x - 1200.0 * RoomScale, r\y - 370.0 * RoomScale, r\z + 600.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("firstaid", r\x - 1000.0 * RoomScale, r\y - 364.0 * RoomScale, r\z - 700.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

;room-local (unrotated, RoomScale units) -> world
Function INR1World(lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, INR1Room\obj, 0)
End Function

Function INR1LocalY#()
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, INR1Room\obj)
	Return TFormedY()
End Function

;walk an NPC toward a room-local point; True once it's there
Function INR1WalkTo%(n.NPCs, lx#, lz#, run% = False)
	If n = Null Then Return True
	INR1World(lx, 0, lz)
	Local tx# = TFormedX(), tz# = TFormedZ()
	Local dx# = tx - EntityX(n\Collider, True), dz# = tz - EntityZ(n\Collider, True)
	If dx * dx + dz * dz < 0.35 * 0.35 Then
		n\State = 0
		Return True
	EndIf
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 10.0), 0)
	If run Then n\State = 2 Else n\State = 1
	Return False
End Function

Function INR1Face(n.NPCs, ent%)
	If n = Null Then Return
	Local dx# = EntityX(ent, True) - EntityX(n\Collider, True), dz# = EntityZ(ent, True) - EntityZ(n\Collider, True)
	RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 8.0), 0)
End Function

Function INR1Spawn.NPCs(npctype%, lx#, lz#)
	INR1World(lx, 40, lz)
	Local n.NPCs = CreateNPC(npctype, TFormedX(), TFormedY() + 0.3, TFormedZ())
	n\State = 0 : n\State2 = 0
	RotateEntity(n\Collider, 0, EntityYaw(INR1Room\obj, True), 0)
	Return n
End Function

Function INR1Say(who$, txt$, secs#)
	Msg = who + ": " + Chr(34) + txt + Chr(34)
	MsgTimer = 70 * secs
	INR1LineT = 70 * secs
End Function

Function UpdateIndevNewRoom1()
	If INR1Room = Null Then Return
	If KillTimer < 0 Then Return
	Local d#

	Select INR1State
		Case 0 ;waiting for the player
			If PlayerRoom <> INR1Room Then Return
			If INR1LocalY() < -250.0 Then
				INR1StartBlackout() ;straight down to the sublevel, nobody around to meet
				Return
			EndIf
			;the two of them walk in from the far entrance of the corridor
			INR1Doc = INR1Spawn(NPCtypeClerk, 420.0, -960.0)
			INR1D = INR1Spawn(NPCtypeD, 560.0, -1000.0)
			INR1State = 1

		Case 1 ;walking to the hall doorway
			Local docThere% = INR1WalkTo(INR1Doc, 120.0, -260.0)
			Local dThere% = INR1WalkTo(INR1D, 240.0, -130.0)
			If docThere Then INR1Face(INR1Doc, Collider)
			If dThere Then INR1Face(INR1D, Collider)
			If INR1LocalY() < -250.0 Then INR1StartBlackout() : Return
			If docThere And dThere Then
				d = EntityDistance(INR1Doc\Collider, Collider)
				If d < 3.5 Then
					INR1State = 2 : INR1Line = 0 : INR1LineT = 0
				ElseIf MsgTimer <= 0 And d < 9.0 Then
					INR1Say("Dr. Harlan", "You. Over here. Yes, you - come here, I won't bite.", 4)
				EndIf
			EndIf

		Case 2 ;the talk
			INR1Face(INR1Doc, Collider)
			INR1Face(INR1D, Collider)
			If INR1LocalY() < -250.0 Then INR1StartBlackout() : Return
			INR1LineT = INR1LineT - FPSfactor
			If INR1LineT <= 0 Then
				Select INR1Line
					Case 0 INR1Say("Dr. Harlan", "D-9341? The doors opened for everyone, didn't they. Doesn't matter now.", 5)
					Case 1 INR1Say("Dr. Harlan", "The lights in Sublevel B keep failing. The breaker's down that ramp. Rodriguez is going to reset it.", 6)
					Case 2 INR1Say("Rodriguez", "Why me? Every time the lights go out down there, something moves. I've heard it.", 5)
					Case 3 INR1Say("Dr. Harlan", "It's the ventilation. Go. And you - there's a first aid kit down there by the pipes if you need one.", 6)
					Case 4 INR1Say("Rodriguez", "...Fine. If I'm not back in five minutes, don't come looking.", 5)
					Case 5 INR1Say("Dr. Harlan", "Whatever happens, keep your eyes open. Both of you.", 4)
					Default
						INR1State = 3 : INR1DStep = 0
				End Select
				INR1Line = INR1Line + 1
			EndIf

		Case 3 ;Rodriguez goes down
			INR1Face(INR1Doc, INR1D\Collider)
			Select INR1DStep
				Case 0 If INR1WalkTo(INR1D, -120.0, 0.0) Then INR1DStep = 1   ;the doorway
				Case 1 If INR1WalkTo(INR1D, -340.0, 0.0) Then INR1DStep = 2   ;top of the ramp
				Case 2 If INR1WalkTo(INR1D, -1060.0, 0.0) Then INR1DStep = 3  ;bottom of the ramp
				Case 3 If INR1WalkTo(INR1D, -1150.0, 420.0) Then INR1DStep = 4 ;the breaker
				Case 4 INR1StartBlackout()
			End Select
			If INR1LocalY() < -250.0 Then INR1StartBlackout()

		Case 4 ;the blackout
			INR1Timer = INR1Timer - FPSfactor
			LightBlink = Max(LightBlink, 3.5) ;near pitch black, with the odd flicker
			If INR1Doc <> Null Then INR1Doc\State = 0
			If INR1D <> Null Then INR1D\State = 0
			INR1Next = INR1Next - FPSfactor
			If INR1Next <= 0 Then
				INR1Next = 70 * Rnd(1.8, 3.0)
				Select Rand(1, 3)
					Case 1 PlaySound_Strict(LoadTempSound("SFX\General\BodyFall.ogg"))
					Case 2 PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
					Default CameraShake = Max(CameraShake, 0.3)
				End Select
			EndIf
			;halfway through the dark, Rodriguez is taken
			If INR1Timer < 70*6 And INR1Timer + FPSfactor >= 70*6 Then
				If INR1D <> Null Then
					PlaySound2(LoadTempSound("SFX\SCP\173\NeckSnap" + Rand(1, 3) + ".ogg"), Camera, INR1D\Collider, 12.0)
					Local de.Decals = CreateDecal(3, EntityX(INR1D\Collider), EntityY(INR1D\Collider) - 0.3, EntityZ(INR1D\Collider), 90, Rnd(360), 0)
					de\Size = 0.6 : ScaleSprite(de\obj, de\Size, de\Size)
					RemoveNPC(INR1D) : INR1D = Null
					Msg = "A short, wet crack somewhere in the dark. Someone was screaming. Now they aren't."
				Else
					Msg = "Somewhere above you, something heavy scrapes across concrete. Then silence."
				EndIf
				MsgTimer = 70*4
			EndIf
			If INR1Timer <= 0 Then
				INR1State = 5 : INR1Timer = 70*3
				LightBlink = 0
				PlaySound_Strict(LoadTempSound("SFX\General\GeneratorOn.ogg"))
				Msg = "A generator coughs into life. The lights stutter back on, dimmer than before."
				MsgTimer = 70*4
			EndIf

		Case 5 ;Harlan loses it and runs
			INR1Timer = INR1Timer - FPSfactor
			If INR1Doc = Null Then
				INR1State = 6
			ElseIf INR1Timer > 0 Then
				INR1Doc\State = 0
				If INR1Timer < 70*2 And INR1Timer + FPSfactor >= 70*2 Then INR1Say("Dr. Harlan", "Rodriguez? RODRIGUEZ! Oh god. Oh god, no -", 4)
			Else
				If INR1WalkTo(INR1Doc, 420.0, -1000.0, True) Or EntityDistance(INR1Doc\Collider, Collider) > 14.0 Then
					RemoveNPC(INR1Doc) : INR1Doc = Null
					INR1State = 6
				EndIf
			EndIf

		Case 6 ;done for this map
	End Select
End Function

Function INR1StartBlackout()
	If INR1State >= 4 Then Return
	INR1State = 4 : INR1Timer = 70*10 : INR1Next = 70*1.5
	PlaySound_Strict(LoadTempSound("SFX\Room\Blackout.ogg"))
	LightBlink = 10.0
	IndevStress = Min(100, IndevStress + 20)
	If INR1D <> Null Then
		INR1Say("Rodriguez", "Found the breaker - wait, what's th-", 3)
	Else
		Msg = "A heavy clunk echoes through the sublevel. Every light goes out at once."
		MsgTimer = 70*5
	EndIf
	;somewhere close by in the dark, stone starts moving
	If Curr173 <> Null Then
		If Curr173\Idle = 0 And EntityDistance(Curr173\Collider, Collider) > 16.0 Then IndevPlace173(8.0, 16.0, False, False)
	EndIf
End Function
