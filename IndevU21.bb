;=====================================================================
; SCP: Containment Breach - Indev: twenty-first batch, four containment blocks of four cells, sixteen SCPs
;
;   Every block has the same layout (Tools\roomkit\rooms_b21.py); slot k holds the pivot of the block's k-th SCP.
;   IndevU21Four() names the SCPs of a block; IndevU21Side() runs one SCP. Most are "look at it and
;   click" (IS10Press); a few act on their own while you are close (1171, 507, 2521, 343, 1437, 2006, 151).
;
;   Per cell: a countdown in Indev21St(block, cell) and once-flags "a?".."d?"; EventState3 is a shared cooldown. The SCP texts are summaries of SCP Wiki articles (CC BY-SA 3.0).
;   Every event returns at once when the player is not in its room.
;=====================================================================

Global Indev21Uses%

Function IndevU21Dress(r.Rooms)
	IndevScpDressList(r, IndevU21Four(r\RoomTemplate\Name)) ;real models for the SCPs that have one (IndevScpProps.bb)
End Function

;the four SCPs of a block in slot order (east south, east north, west south, west north), as "a|b|c|d"
Function IndevU21Four$(name$)
	Select name
		Case "room2b21block1" : Return "038|063|1171|507"
		Case "room2b21block2" : Return "2521|343|1437|1609"
		Case "room2b21block3" : Return "2006|120|093|1981"
		Case "room2b21block4" : Return "151|050|216|662"
	End Select
	Return ""
End Function

Function UpdateIndevU21(e.Events)
	Local four$, k%, s%
	If PlayerRoom <> e\room Then Return
	four = IndevU21Four(e\room\RoomTemplate\Name)
	If four = "" Then Return
	If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
	For s = 0 To 3
		k = Instr(four, "|")
		If k = 0 Then
			IndevU21Side(e, four, s)
		Else
			IndevU21Side(e, Left(four, k - 1), s)
			four = Mid(four, k + 1)
		EndIf
	Next
End Function

;the countdown or counter of one cell, kept per block (1-4) and cell (0-3)
Dim Indev21St#(4, 3)

Function IndevU21Get#(e.Events, side%)
	Return Indev21St(Int(Right(e\room\RoomTemplate\Name, 1)), side)
End Function

Function IndevU21Set(e.Events, side%, v#)
	Indev21St(Int(Right(e\room\RoomTemplate\Name, 1)), side) = v
End Function

;a once-only flag for one side
Function IndevU21Once%(e.Events, side%, f$)
	Local key$ = Chr(97 + side) + f
	If IAxFlag(e, key) Then Return False
	IAxSetFlag(e, key)
	Return True
End Function

Function IndevU21Side(e.Events, scp$, side%)
	Local r.Rooms = e\room, p% = r\Objects[side], d#, st#, n.NPCs, k%
	d = EntityDistance(Collider, p)
	Select scp
		Case "038"
			If IS10Press(p, 2.5) Then
				Indev21Uses = Indev21Uses + 1
				If IndevU21Once(e, side, "f") Then
					IS16Give("bat", p)
					IS16Tell("You press a battery to the bark. By the time you look up, the tree has fruited: a second battery.", 7)
				Else
					IS16Tell("The tree is resting. The new buds are not ripe yet.", 4)
				EndIf
			EndIf
		Case "063"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				Injuries = Injuries + 0.2
				IS16Tell("You brush the bristles with a finger. There is a little less finger now.", 6)
			EndIf
		Case "1171"
			;the frost writes a new line every eight seconds while you are near the window
			If d < 3.0 Then
				st = IndevU21Get(e, side) - FPSfactor
				If st <= 0 Then
					st = 70 * 8
					k = Rand(4)
					Indev21Uses = Indev21Uses + 1
					Select k
						Case 1 : IS16Tell("Letters form in the frost on the glass: HUMANS GO AWAY", 6)
						Case 2 : IS16Tell("The frost writes: WHY ARE YOU HERE", 6)
						Case 3 : IS16Tell("The frost writes: PLEASE. WE ARE AFRAID OF YOU", 6)
						Case 4 : IS16Tell("The frost writes: THE OTHER ONE LEFT. YOU SHOULD TOO", 6)
					End Select
				EndIf
				IndevU21Set(e, side, st)
			EndIf
		Case "507"
			;he stands in his cell and now and then drops out of this world, and back in
			n = r\NPC[side]
			If IndevU21Once(e, side, "n") Then
				r\NPC[side] = IS16Person(r, side, 90)
				IndevU21Set(e, side, 70 * Rand(25, 50))
				Return
			EndIf
			st = IndevU21Get(e, side) - FPSfactor
			If st <= 0 Then
				st = 70 * Rand(25, 50)
				IS10Sound("SFX\Indev\poof.wav", p, 8.0, 0.8)
				Indev21Uses = Indev21Uses + 1
				If n <> Null Then
					RemoveNPC(n)
					r\NPC[side] = Null
					If d < 6.0 Then IS16Tell("SCP-507 is gone, in the middle of a word.", 4)
				Else
					r\NPC[side] = IS16Person(r, side, 90)
					If d < 6.0 Then IAxSay("SCP-507", "Don't ask. There were bees. Big ones.", 5)
				EndIf
			EndIf
			IndevU21Set(e, side, st)
			If r\NPC[side] <> Null And d < 4.0 Then IAxFace(r\NPC[side], Collider)
		Case "2521"
			;come too close and it takes the words away
			If d < 2.5 And IndevU21Once(e, side, "t") Then
				Indev21Uses = Indev21Uses + 1
				IndevStress = IndevStress + 15 : If IndevStress > 100 Then IndevStress = 100
				IS10Sound("SFX\Indev\timewarp.wav", p, 6.0, 0.8)
				IS16Tell("|  oo  |  ooooo  |  oo  |  o  |  (it is only pictures now)", 6)
			EndIf
		Case "343"
			If IndevU21Once(e, side, "n") Then
				r\NPC[side] = IS16Person(r, side, 90)
				IAxSkin(r\NPC[side], "GFX\npcs\indev_archivist.jpg")
			EndIf
			If r\NPC[side] <> Null Then
				If d < 4.0 Then IAxFace(r\NPC[side], Collider)
				If d < 2.2 And MsgTimer <= 0 And Rand(400) = 1 Then
					Indev21Uses = Indev21Uses + 1
					Select Rand(3)
						Case 1 : IAxSay("SCP-343", "Sit, if you like. The chair is real. Most things here are.", 6)
						Case 2 : IAxSay("SCP-343", "You are wondering whether I could open the door. I could. I like the company.", 7)
						Case 3 : IAxSay("SCP-343", "Do give your mother a call when you are out of here. She worries.", 6)
					End Select
				EndIf
			EndIf
		Case "1437"
			If d < 4.0 Then
				st = IndevU21Get(e, side) - FPSfactor
				If st <= 0 Then
					st = 70 * Rand(15, 30)
					IS10Sound("SFX\Indev\wind.wav", p, 8.0, 0.6)
				EndIf
				IndevU21Set(e, side, st)
			EndIf
			If IS10Press(p, 2.5) Then
				Indev21Uses = Indev21Uses + 1
				IS16Tell("You look down the hole. There is a sky down there, and something in it, looking back up.", 6)
			EndIf
		Case "1609"
			If IS10Press(p, 2.5) Then
				Indev21Uses = Indev21Uses + 1
				Injuries = Injuries + 0.4
				IS16Tell("You kick the splinters aside. Some of them are now in your leg, and they did not get there by flying.", 7)
			EndIf
		Case "2006"
			If d < 3.0 And IndevU21Once(e, side, "s") Then
				Indev21Uses = Indev21Uses + 1
				IS10Sound("SFX\Indev\scream457.wav", p, 8.0, 1.0)
				IndevStress = IndevStress + 10 : If IndevStress > 100 Then IndevStress = 100
				IS16Tell("Something huge and toothy unfolds from the cabinet, roars - and then asks, quite shyly, whether that was scary.", 8)
			EndIf
		Case "120"
			;the real SCP-120 is in its own outbuilding now (room2b29pool, IndevU29.bb): this is the training replica
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				IS16Tell("A training replica of SCP-120: the same pink plastic, plain water, no glow. The real one is kept in its fortified outbuilding in the Entrance Zone.", 7)
			EndIf
		Case "151"
			;look at the painting too long and your lungs fill
			If IS16Aim(p, 4.0, 0.95) Then
				st = IndevU21Get(e, side) + FPSfactor
				If st > 70 * 5 Then
					st = 0
					Indev21Uses = Indev21Uses + 1
					Injuries = Injuries + 0.15
					BlurTimer = 400
					IS16Tell("You cough up seawater. You have not been near the sea.", 5)
				EndIf
				IndevU21Set(e, side, st)
			Else
				IndevU21Set(e, side, 0)
			EndIf
		Case "050"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				If IndevU21Once(e, side, "w") Then
					IS16Tell("You trick the trophy's last owner's note out of the way and lift it. It is yours now. You did not want it.", 7)
				Else
					IS16Tell("The trophy is still yours. Somebody will have to outwit you to be rid of it.", 5)
				EndIf
			EndIf
		Case "216"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				If e\EventState3 > 0 Then
					IS16Tell("You try another combination. The safe opens on a long dark corridor, and you shut it quickly.", 6)
				Else
					e\EventState3 = 70 * 120
					Select Rand(3)
						Case 1 : IS16Give("firstaid", p)
						Case 2 : IS16Give("bat", p)
						Case 3 : IS16Give("key2", p)
					End Select
					IS16Tell("You turn the dial to a number you just made up. The safe opens; there is something in it for you.", 6)
				EndIf
			EndIf
		Case "662"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				IS10Sound("SFX\Indev\bells.wav", p, 6.0, 0.7)
				Stamina = 100
				IndevStress = IndevStress - 10 : If IndevStress < 0 Then IndevStress = 0
				IAxSay("Mr. Deeds", "You rang? A cup of tea, and a moment's rest. There. Do mind the stairs.", 7)
			EndIf
		Case "093"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				IS10Sound("SFX\Indev\timewarp.wav", p, 6.0, 0.8)
				BlurTimer = 500
				IS16Tell("The red disc is warm. For a moment the room is grey and empty and burnt, then it is not.", 7)
			EndIf
		Case "1981"
			If IS10Press(p, 2.0) Then
				Indev21Uses = Indev21Uses + 1
				IS10Sound("SFX\Indev\uvhum.wav", p, 6.0, 0.6)
				IndevStress = IndevStress + 5 : If IndevStress > 100 Then IndevStress = 100
				IS16Tell("The tape plays a speech you have never heard. The man on the screen keeps talking, whatever happens to him.", 7)
			EndIf
	End Select
End Function

;SCP-120: send the player to the middle of a random ordinary room of the same zone
Function IndevU21Elsewhere()
	Local r.Rooms, n%, pick%, z% = PlayerRoom\zone
	For r = Each Rooms
		If r <> PlayerRoom And r\zone = z And Left(r\RoomTemplate\Name, 5) = "room2" Then n = n + 1
	Next
	If n = 0 Then
		IS16Tell("You step into the pool. Your feet get wet. Nothing else happens.", 5)
		Return
	EndIf
	pick = Rand(1, n) : n = 0
	For r = Each Rooms
		If r <> PlayerRoom And r\zone = z And Left(r\RoomTemplate\Name, 5) = "room2" Then
			n = n + 1
			If n = pick Then Exit
		EndIf
	Next
	PositionEntity(Collider, EntityX(r\obj), EntityY(r\obj) + 0.7, EntityZ(r\obj))
	ResetEntity(Collider)
	DropSpeed = 0
	UpdateDoors()
	UpdateRooms()
	IS16Tell("You step into the paddling pool and out of somewhere else entirely.", 6)
End Function
