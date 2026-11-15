;=====================================================================
; SCP: Containment Breach - Indev: the thirty-ninth batch - three very big rooms and five new SCPs
;
;   room2b41research   SCP-586: near it, every message you read has a word swapped for a wrong one (IS16Tell)
;                      SCP-1176: drain its honey from the sarcophagus faucet - eat it and you find out whether
;                      you are compatible (a full heal) or not (violently sick); it is fixed the first time
;   room2b41warehouse  SCP-1370: open its case and it attacks you, loudly and badly, then calms down
;                      SCP-1562: climb the slide; go down crouched (head-first) and you vanish into a cramped
;                      tunnel - and come out somewhere else in the facility. Standing, it is just a slide.
;   room2b41testcon    SCP-1013: meet its eyes (through the window too) and you are paralysed for a few seconds;
;                      inside the chamber it bites while you can't move, and the bites calcify
;   Summaries of scp-wiki.wikidot.com/scp-586, -1013, -1176, -1370, -1562 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I39Near586%, I39HoneyCD#, I39Compat%
Global I39Para#, I39ParaCD#, I39PX#, I39PZ#, I39Look#, I39Calc#
Global I39Robot#, I39RobotN%

Function Indev39Reset(newGame%)
	If newGame Then
		I39Compat = 0 : I39Calc = 0 : I39RobotN = 0
	EndIf
	I39Near586 = False : I39HoneyCD = 0 : I39Para = 0 : I39ParaCD = 0 : I39Look = 0 : I39Robot = 0
End Function

Function IndevU39Dress(r.Rooms)
End Function

Function UpdateIndevU39(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b41research" : U39Research(e)
		Case "room2b41warehouse" : U39Warehouse(e)
		Case "room2b41testcon" : U39Test(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- SCP-586
Function U39Typo$(txt$)
	Local n%, k%, i%, w%, out$, word$, c$
	If Not I39Near586 Then Return txt
	;count words, pick one, swap it
	For i = 1 To Len(txt)
		If Mid(txt, i, 1) = " " Then n = n + 1
	Next
	If n < 2 Then Return txt
	k = Rand(1, n)
	For i = 1 To Len(txt)
		c = Mid(txt, i, 1)
		If c = " " Then
			If w = k And Len(word) > 2 Then
				Select Rand(8)
					Case 1 : word = "horse"
					Case 2 : word = "teapot"
					Case 3 : word = "garden"
					Case 4 : word = "spoon"
					Case 5 : word = "umbrella"
					Case 6 : word = "pickle"
					Case 7 : word = "lamp"
					Default : word = "cabbage"
				End Select
			EndIf
			out = out + word + " "
			word = ""
			w = w + 1
		Else
			word = word + c
		EndIf
	Next
	Return out + word
End Function

;--------------------------------------------------------------------------------------------- research
Function U39Research(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then
		I39Near586 = False
		Return
	EndIf
	I39Near586 = (EntityDistance(Collider, r\Objects[U39_RES_S586]) < 4.0)
	If I39HoneyCD > 0 Then I39HoneyCD = I39HoneyCD - FPSfactor
	If IS10Press(r\Objects[U39_RES_S586], 1.6) Then
		IS16Tell("SCP-586: a lump of pale green metal on a plinth. It looks like a piece of garden hose. No - that's not the word you meant.", 7)
	EndIf
	If IS10Press(r\Objects[U39_RES_S1176], 2.0) Then
		IS16Tell("SCP-1176 lies under a skin of golden honey in its sarcophagus, wrapped and dark. Its brain is asleep. The honey level creeps up while you watch.", 7)
	EndIf
	If IS10Press(r\Objects[U39_RES_FAUCET], 1.4) Then
		If I39HoneyCD > 0 Then
			IS16Tell("The faucet drips. The jar under it has a while to fill.", 4)
		Else
			I39HoneyCD = 70 * 90
			IS16Give("honey1176", r\Objects[U39_RES_FAUCET])
			IS16Tell("You open the faucet. Thick golden honey runs into a jar. The label on the jar: NOT A FOOD PRODUCT. INEDIBLE.", 7)
		EndIf
	EndIf
End Function

Function IndevUse39(it.Items)
	Select it\itemtemplate\name
		Case "honey1176"
			RemoveItem(it)
			SelectedItem = Null
			If I39Compat = 0 Then
				I39Compat = 2
				If Rand(3) = 1 Then I39Compat = 1
			EndIf
			If I39Compat = 1 Then
				Injuries = 0 : Bloodloss = 0 : Stamina = 100
				IS16Tell("Sweet, heavy, clover and something older. Warmth floods out to your fingertips. Every ache is gone. You are, it seems, compatible.", 8)
			Else
				Injuries = Injuries + 0.4
				BlurTimer = 70 * 6 : CameraShake = 1.5
				IS16Tell("Your throat closes on it. You bring it all back up, gasping. Whatever you are, you are not compatible.", 7)
			EndIf
			Return
	End Select
	SelectedItem = Null
End Function

;--------------------------------------------------------------------------------------------- warehouse
Function U39Warehouse(e.Events)
	Local r.Rooms = e\room, rr.Rooms, n%, pick%
	If PlayerRoom <> r Then Return
	;SCP-1370 on the loose for a few seconds
	If I39Robot > 0 Then
		I39Robot = I39Robot - FPSfactor
		If EntityDistance(Collider, r\Objects[U39_WHB_R1370]) < 2.5 And Rand(40) = 1 Then
			Injuries = Injuries + 0.05
			CameraShake = 1.0
			IS10Sound("SFX\Indev\clicks.wav", r\Objects[U39_WHB_R1370], 4.0, 1.0)
		EndIf
		If I39Robot <= 0 Then IS16Tell("SCP-1370 topples over, rights itself, and climbs back into its case. 'YOU FOUGHT WITH HONOUR,' it says, to the wall.", 7)
	EndIf
	If IS10Press(r\Objects[U39_WHB_R1370], 1.6) Then
		I39RobotN = I39RobotN + 1
		If I39Robot <= 0 Then
			I39Robot = 70 * 8
			Select I39RobotN
				Case 1 : IS16Tell("You lift the lid. 'I AM SCP-1370. I HAVE COME TO DESTROY YOU, SCP. PREPARE FOR COMBAT.' It flails at your shins with a pair of pliers.", 8)
				Case 2 : IS16Tell("'YOU AGAIN. SCP. MY OLD NEMESIS.' It throws a screwdriver. Badly.", 6)
				Default : IS16Tell("'EN GARDE.' It falls over. It gets up. 'THAT WAS A FEINT.'", 6)
			End Select
		EndIf
	EndIf
	;SCP-1562
	If IS10Press(r\Objects[U39_WHB_SLIDE], 1.8) Then
		If Crouch Then
			For rr = Each Rooms
				If rr <> r And Left(rr\RoomTemplate\Name, 5) = "room2" Then n = n + 1
			Next
			pick = Rand(1, Max(1, n)) : n = 0
			For rr = Each Rooms
				If rr <> r And Left(rr\RoomTemplate\Name, 5) = "room2" Then
					n = n + 1
					If n = pick Then Exit
				EndIf
			Next
			IndevStress = Min(100, IndevStress + 20)
			BlurTimer = 70 * 6 : LightBlink = 3.0
			If rr <> Null Then
				PositionEntity(Collider, EntityX(rr\obj), EntityY(rr\obj) + 0.7, EntityZ(rr\obj))
				ResetEntity(Collider)
				UpdateDoors()
				UpdateRooms()
			EndIf
			IS16Tell("Head first, arms at your sides. The end of the slide never comes. A tunnel, small, cramped, dark, going on and on - then light, and a floor that isn't the warehouse.", 9)
		Else
			IS16Tell("You go down feet first, like anyone would. Metal, cold, a bump at the end. Nothing happens. (The sign says: DO NOT GO DOWN HEAD-FIRST.)", 7)
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- SCP-1013
Function U39Test(e.Events)
	Local r.Rooms = e\room, n.NPCs, lx#, inside%
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		n = CreateNPC(NPCtypeD, EntityX(r\Objects[U39_TST_DCLASS], True), EntityY(r\Objects[U39_TST_DCLASS], True) + 0.3, EntityZ(r\Objects[U39_TST_DCLASS], True))
		n\State = 0 : r\NPC[0] = n
		RotateEntity(n\Collider, 0, 90, 0)
		n = CreateNPC(NPCtypeD, EntityX(r\Objects[U39_TST_DCLASS], True),EntityY(r\Objects[U39_TST_DCLASS], True) + 0.3, EntityZ(r\Objects[U39_TST_DCLASS], True) + 1.0)
		n\State = 0 : r\NPC[1] = n
		RotateEntity(n\Collider, 0, 270, 0)
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U39_TST_GUARD], True), EntityY(r\Objects[U39_TST_GUARD], True) + 0.35, EntityZ(r\Objects[U39_TST_GUARD], True))
		n\State = 9 : r\NPC[2] = n
		RotateEntity(n\Collider, 0, 270, 0)
	EndIf
	U37Pin(r\NPC[0], r\Objects[U39_TST_DCLASS], 0.0, 0.3)
	U37Pin(r\NPC[1], r\Objects[U39_TST_DCLASS], 1.0, 0.3)
	U37Pin(r\NPC[2], r\Objects[U39_TST_GUARD], 0.0, 0.35)
	If PlayerRoom <> r Then
		I39Look = 0
		Return
	EndIf
	lx = U37LX(r)
	inside = (lx > 444)
	If I39ParaCD > 0 Then I39ParaCD = I39ParaCD - FPSfactor
	;paralysed: you can't move; inside the chamber, it bites
	If I39Para > 0 Then
		I39Para = I39Para - FPSfactor
		PositionEntity(Collider, I39PX, EntityY(Collider, True), I39PZ, True)
		Stamina = 0
		If inside And Rand(90) = 1 Then
			I39Calc = I39Calc + 1
			Injuries = Injuries + 0.5
			CameraShake = 2.0
			IS16Tell("A serrated beak in your calf. You can't even flinch. Where it bit, the skin is turning hard and white.", 6)
			If I39Calc >= 4 Then
				DeathMSG = "Subject D-9341 was recovered from the SCP-1013 test chamber fully calcified. SCP-1013 was observed feeding on the remains."
				Kill()
			EndIf
		EndIf
		If I39Para <= 0 Then
			I39ParaCD = 70 * 15
			IS16Tell("Feeling floods back into your arms, legs, everything at once. Don't look at it. Don't look at it.", 5)
		EndIf
		Return
	EndIf
	;eye contact
	;outside the chamber only a long stare from right at the window counts - walking through the hall never
	;locks you up; inside the chamber, a moment's eye contact is enough
	Local nearWin% = (lx > 250), need# = 45, dist# = EntityDistance(Collider, r\Objects[U39_TST_LIZARD])
	If Not inside Then need = 80
	If I39ParaCD <= 0 And KillTimer >= 0 And (inside Or nearWin) And dist < 7.0 And EntityInView(r\Objects[U39_TST_LIZARD], Camera) Then
		I39Look = I39Look + FPSfactor
		If I39Look > need Then
			I39Look = 0
			I39Para = 70 * 5
			If Not inside Then I39Para = 70 * 2.5
			I39PX = EntityX(Collider, True) : I39PZ = EntityZ(Collider, True)
			BlurTimer = 70 * 5
			IS16Tell("Its eyes meet yours - a rooster's head on a reptile, the frill flaring. Pain stabs through every muscle. You can't move.", 7)
		EndIf
	Else
		I39Look = Max(0, I39Look - FPSfactor)
	EndIf
	If IS10Press(r\Objects[U39_TST_WINDOW], 2.0) Then
		IS16Tell("The test chamber. Two D-class stand with their backs to the far corner, very carefully looking at the floor. Something small moves in the grit.", 7)
	EndIf
End Function
