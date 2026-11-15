;=====================================================================
; SCP: Containment Breach - Indev: the forty-sixth batch - the alternate timeline. Years before the breach on record
; the lower levels failed and were sealed with people inside; the upper site was built over them.
;
;   room2b49checkpoint  Checkpoint 9, abandoned. The radio is still on: Officer Miller, from the lower complex.
;                       Variation (EventState2): 1 Miller answers; 2 static and a dead channel; 3 someone else answers
;   room2b49hidden      Sector R. Dr. Harrison (reused clerk NPC, pinned) explains the timeline, one line per talk
;   room2b49perslift    the personnel lift down to the lower complex; Officer Miller (reused guard, pinned) holds
;                       the platform and tells you where to go, depending on the best keycard you carry
;   room2b49sealed      the sealed wing: dust, the stopped calendar; on the first visit a chance SCP-106 is down here
; All writing original. Reuses the guard and clerk models and AI (pinned, no new AI).
;=====================================================================

Global I46Harrison% = 0, I46Radio% = 0

Function Indev46Reset(newGame%)
	I46Harrison = 0 : I46Radio = 0
End Function

Global I46StepT#, I46Seen%

;the old cell: the big containment door (locked, the event opens it) and the old statue - a plain copy of the
;SCP-173 mesh, tinted to the old v0.1 look, parented to the room so it rotates with it. Not the real SCP-173 NPC.
Function IndevU46Dress(r.Rooms)
	Local d.Doors, o%, sc#
	If r\RoomTemplate\Name <> "room2scp173oldercell" Then Return
	d = CreateDoor(r\zone, r\x + 452 * RoomScale, r\y, r\z, 90, r, False, True, 0)
	d\AutoClose = False : d\locked = True
	;no buttons: they float off the thick cell wall, and only the event opens this door
	Local i%
	For i = 0 To 1
		If d\buttons[i] <> 0 Then
			FreeEntity(d\buttons[i])
			d\buttons[i] = 0
		EndIf
	Next
	r\RoomDoors[0] = d
	o = LoadMesh_Strict("GFX\npcs\173_2.b3d")
	sc = GetModdedINIFloat("DATA\NPCs.ini", "SCP-173", "scale") / MeshDepth(o)
	If sc <= 0 Then sc = 0.35 / MeshDepth(o) * 6.0
	ScaleEntity(o, sc, sc, sc)
	EntityColor(o, 255, 238, 210)
	PositionEntity(o, r\x + 820 * RoomScale, r\y, r\z, True)
	RotateEntity(o, 0, 90, 0, True)
	EntityParent(o, r\obj)
	r\Objects[U46_O73_SLOTS] = o
End Function

;is the old statue being looked at?
Function U46Old173Seen%(o%)
	If LightBlink > 0 Then Return False
	If Not (BlinkTimer < -16 Or BlinkTimer > -6) Then Return False
	If EntityDistance(o, Collider) > 14 Then Return False
	Return EntityInView(o, Camera)
End Function

Function U46Old173Face(o%)
	Local y# = EntityY(o, True)
	PointEntity(o, Collider)
	RotateEntity(o, 0, EntityYaw(o, True), 0, True)
End Function

;the statue appears behind a D-class in the dark and breaks his neck
Function U46Old173Kill(r.Rooms, n.NPCs)
	Local o% = r\Objects[U46_O73_SLOTS]
	If n = Null Then Return
	If n\IsDead Then Return
	TFormPoint(0, 0, -0.45, n\Collider, 0)
	PositionEntity(o, TFormedX(), r\y, TFormedZ(), True)
	PointEntity(o, n\Collider)
	RotateEntity(o, 0, EntityYaw(o, True), 0, True)
	PlaySound2(NeckSnapSFX(Rand(0, 2)), Camera, n\Collider, 10.0)
	n\State = 3
	SetNPCFrame(n, 19)
	n\IsDead = True
End Function

;------------------------------------------------------------------------------------------- the old SCP-173 cell
;EventState 1 = people made; EventState2 = phase (0 waiting, 1 the intro, 2 the statue is loose); EventState3 = clock
Function U46Old173(e.Events)
	Local r.Rooms = e\room, n.NPCs, o% = r\Objects[U46_O73_SLOTS], t#, k%, d#, dx#, dz#, stp#
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		For k = 0 To 1
			n = CreateNPC(NPCtypeD, EntityX(r\Objects[U46_O73_DCL1 + k], True), EntityY(r\Objects[U46_O73_DCL1 + k], True) + 0.5, EntityZ(r\Objects[U46_O73_DCL1 + k], True))
			n\State = 0
			RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) - 90, 0)
			r\NPC[k] = n
		Next
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U46_O73_GUARD], True), EntityY(r\Objects[U46_O73_GUARD], True) + 0.5, EntityZ(r\Objects[U46_O73_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) - 90, 0)
		r\NPC[2] = n
	EndIf
	U46Pin(r\NPC[2], r\Objects[U46_O73_GUARD], 0.5)
	If e\EventState2 = 0 Then
		For k = 0 To 1
			U46Pin(r\NPC[k], r\Objects[U46_O73_DCL1 + k], 0.5)
		Next
	EndIf
	If PlayerRoom <> r Or o = 0 Then Return
	Select e\EventState2
		Case 0
			;the classic intro starts the moment you walk into the chamber
			If Abs(U37LZ(r)) < 900 Then
				e\EventState2 = 1 : e\EventState3 = 0
				PlaySound_Strict(LoadTempSound("SFX\Indev\intro\intro1.ogg"))
			EndIf
		Case 1
			t = e\EventState3
			e\EventState3 = e\EventState3 + FPSfactor
			If t < 70 * 6 And e\EventState3 >= 70 * 6 Then
				PlaySound_Strict(LoadTempSound("SFX\Indev\intro\intro2.ogg"))
				If r\RoomDoors[0] <> Null Then
					r\RoomDoors[0]\locked = False
					UseDoor(r\RoomDoors[0], False, True)
					r\RoomDoors[0]\locked = True
				EndIf
				For k = 0 To 1
					If r\NPC[k] <> Null Then
						PointEntity(r\NPC[k]\Collider, r\Objects[U46_O73_CELL1 + k])
						RotateEntity(r\NPC[k]\Collider, 0, EntityYaw(r\NPC[k]\Collider), 0)
						r\NPC[k]\State = 1
					EndIf
				Next
			EndIf
			If t < 70 * 9 And e\EventState3 >= 70 * 9 And r\NPC[1] <> Null Then
				r\NPC[1]\State = 0
				PlaySound2(LoadTempSound("SFX\Indev\intro\refuse" + Rand(1, 3) + ".ogg"), Camera, r\NPC[1]\Collider, 10.0)
			EndIf
			If t < 70 * 13 And e\EventState3 >= 70 * 13 Then
				PlaySound_Strict(LoadTempSound("SFX\Indev\intro\intro3.ogg"))
				If r\NPC[1] <> Null Then r\NPC[1]\State = 1
			EndIf
			;the D-class stop in front of the statue
			For k = 0 To 1
				n = r\NPC[k]
				If n <> Null Then
					If n\State = 1 And (Not n\IsDead) Then
						PointEntity(n\Collider, r\Objects[U46_O73_CELL1 + k])
						RotateEntity(n\Collider, 0, EntityYaw(n\Collider), 0)
						If EntityDistance(n\Collider, r\Objects[U46_O73_CELL1 + k]) < 0.4 Then
							n\State = 0
							PointEntity(n\Collider, o)
							RotateEntity(n\Collider, 0, EntityYaw(n\Collider), 0)
						EndIf
					EndIf
				EndIf
			Next
			;the lights fail. twice.
			If t < 70 * 24 And e\EventState3 >= 70 * 24 Then
				LightBlink = 3.0
				U46Old173Kill(r, r\NPC[0])
			EndIf
			If t < 70 * 26.5 And e\EventState3 >= 70 * 26.5 Then
				LightBlink = 3.0
				U46Old173Kill(r, r\NPC[1])
			EndIf
			If e\EventState3 >= 70 * 28.5 Then
				PlaySound_Strict(LoadTempSound("SFX\Indev\intro\Alarm2.ogg"))
				IS16Tell("The alarm. On the balcony the guard is shouting into his radio. The statue is no longer in its cell.", 6)
				e\EventState2 = 2
				I46StepT = 70
			EndIf
		Case 2
			;loose: it moves only when nobody is looking - a blink is enough
			I46Seen = U46Old173Seen(o)
			I46StepT = I46StepT - FPSfactor
			If (Not I46Seen) And I46StepT <= 0 Then
				I46StepT = 20
				dx = EntityX(Collider, True) - EntityX(o, True)
				dz = EntityZ(Collider, True) - EntityZ(o, True)
				d = Sqr(dx * dx + dz * dz)
				If d < 0.9 Then
					If KillTimer >= 0 Then
						PlaySound_Strict(NeckSnapSFX(Rand(0, 2)))
						DeathMSG = "Subject D-9341 was found in the old SCP-173 chamber with a broken neck. The two D-class assigned to the cell entry that morning were found beside the door."
						Kill()
					EndIf
				Else
					stp = Min(d - 0.6, 1.3)
					TranslateEntity(o, dx / d * stp, 0, dz / d * stp, True)
					U46Old173Face(o)
				EndIf
			EndIf
	End Select
End Function

;U37Pin only checks x/z, so an NPC that sank through the floor stayed sunk: this also catches a drop in height
Function U46Pin(n.NPCs, p%, dy#)
	Local x#, y#, z#
	If n = Null Or p = 0 Then Return
	If n\IsDead Then Return
	x = EntityX(p, True) : y = EntityY(p, True) : z = EntityZ(p, True)
	If Abs(EntityX(n\Collider, True) - x) + Abs(EntityZ(n\Collider, True) - z) > 0.25 Or EntityY(n\Collider, True) < y - 0.15 Then
		PositionEntity(n\Collider, x, y + dy, z, True)
		ResetEntity(n\Collider)
	EndIf
End Function

Function U46Talk(r.Rooms, k%, p%, dist#)
	If r\NPC[k] = Null Then Return False
	If r\NPC[k]\IsDead Then Return False
	Return IS10Press(p, dist)
End Function

Function UpdateIndevU46(e.Events)
	Local r.Rooms = e\room, n.NPCs, lx#, ly#, best%
	If r\RoomTemplate\Name = "room2scp173oldercell" Then
		U46Old173(e)
		Return
	EndIf
	If e\EventState2 = 0 And r\RoomTemplate\Name <> "room2b49perslift" Then e\EventState2 = Rand(1, 3)
	;the people are made once, the first time the room is near
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		Select r\RoomTemplate\Name
			Case "room2b49hidden"
				n = CreateNPC(NPCtypeClerk, EntityX(r\Objects[U46_SCR_HARRISON], True), EntityY(r\Objects[U46_SCR_HARRISON], True) + 0.5, EntityZ(r\Objects[U46_SCR_HARRISON], True))
				n\State = 0 : n\State2 = 0
				RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
				r\NPC[0] = n
			Case "room2b49perslift"
				n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U46_PEL_MILLER], True), EntityY(r\Objects[U46_PEL_MILLER], True) + 0.35, EntityZ(r\Objects[U46_PEL_MILLER], True))
				n\State = 9
				RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
				r\NPC[0] = n
			Case "room2b49sealed"
				If Rand(100) <= 35 Then e\EventState3 = 70 * 8 Else e\EventState3 = -1
		End Select
	EndIf
	Select r\RoomTemplate\Name
		Case "room2b49hidden"
			U46Pin(r\NPC[0], r\Objects[U46_SCR_HARRISON], 0.5)
		Case "room2b49perslift"
			U46Pin(r\NPC[0], r\Objects[U46_PEL_MILLER], 0.5)
	End Select
	If PlayerRoom <> r Then Return
	lx = U37LX(r) : ly = U37LY(r)
	Select r\RoomTemplate\Name
		;---------------- checkpoint 9
		Case "room2b49checkpoint"
			If e\EventState3 = 0 Then
				e\EventState3 = 1
				IS16Tell("Checkpoint 9. Coats on the hooks, a game of cards left mid-hand. Somewhere a radio hisses.", 6)
			EndIf
			If IS10Press(r\Objects[U46_CP9_RADIO], 1.5) Then
				I46Radio = I46Radio + 1
				Select e\EventState2
					Case 1
						Select I46Radio Mod 4
							Case 1 : IAxSay("Radio (Miller)", "Checkpoint nine? Someone's actually there? This is Miller, lower complex. Don't come down without a card - the doors here run on the old codes.", 8)
							Case 2 : IAxSay("Radio (Miller)", "Personnel lift is in Light Containment, the hall with the benches. I'm holding the platform at the bottom. I'll be the one not shooting at you.", 8)
							Case 3 : IAxSay("Radio (Miller)", "Look for Sector R. It's not on your maps. Harrison's in there. He knows what happened the first time.", 8)
							Default : IAxSay("Radio (Miller)", "...the team? They went down before me. I'm still looking.", 6)
						End Select
					Case 2
						IS16Tell("Static on every channel. Then, for a second, under the static: breathing. Then nothing.", 6)
					Default
						IndevStress = Min(100, IndevStress + 6)
						IAxSay("Radio", "Miller's not here any more. You can come down anyway. We'll wait.", 6)
				End Select
			EndIf
			If IS10Press(r\Objects[U46_CP9_CARDS], 1.4) Then
				IS16Tell("Four hands dealt, three picked up. The fourth player never sat down.", 5)
			EndIf
		;---------------- sector R
		Case "room2b49hidden"
			If e\EventState3 = 0 Then
				e\EventState3 = 1
				IS16Tell("The dust is ankle-deep and unbroken - except for one path of footprints, back and forth, between the terminal and the map.", 7)
			EndIf
			If U46Talk(r, 0, r\Objects[U46_SCR_HARRISON], 1.6) Then
				I46Harrison = I46Harrison + 1
				Select I46Harrison
					Case 1 : IAxSay("Dr. Harrison", "A visitor. You're not on the roster, so you must be real. Sit, if you can find a clean chair.", 7)
					Case 2 : IAxSay("Dr. Harrison", "This is not the first breach. The first one happened years ago, down below. Power, doors and gas all failed in the same minute.", 9)
					Case 3 : IAxSay("Dr. Harrison", "They didn't clean it up. They poured a floor over it and built the site you know on top. The lower complex is still down there.", 9)
					Case 4 : IAxSay("Dr. Harrison", "Sector R was the team that asked questions about it. So Sector R was removed. From the maps, the rosters, the budget. Not from the building.", 9)
					Case 5 : IAxSay("Dr. Harrison", "What's happening above us now is the same failure, coming back up. Take the personnel lift. Find Miller. Get out the old way.", 9)
					Default : IAxSay("Dr. Harrison", "Go. Someone has to remember this happened twice.", 5)
				End Select
			EndIf
			If IS10Press(r\Objects[U46_SCR_MAP], 1.8) Then
				IS16Tell("The site plan. A whole sector below Light Containment is blacked out in marker: SECTOR R - REMOVED. Beneath it, scratched into the paint, a lift shaft.", 7)
			EndIf
			If IS10Press(r\Objects[U46_SCR_TERMINAL], 1.6) Then
				IS16Tell("The terminal wakes up. LAST LOGIN: HARRISON. The date it shows is years before you were brought here.", 7)
			EndIf
		;---------------- the personnel lift
		Case "room2b49perslift"
			e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
			If IS10Press(r\Objects[U46_PEL_NOTICE], 1.6) Then
				IS16Tell("PERSONNEL LIFT - LOWER COMPLEX. Under it, in pencil: if the car comes with the lights off, wait for the next one.", 6)
			EndIf
			If ly < -300 And e\EventState3 = 0 Then
				e\EventState3 = 1
				IS16Tell("The lower complex. Older concrete, older lamps, and dust no one has walked through in years.", 6)
			EndIf
			If U46Talk(r, 0, r\Objects[U46_PEL_MILLER], 1.8) Then
				best = U43BestCard()
				If best < 3 Then
					IAxSay("Officer Miller", "Miller, security. You're the one off the radio. Nothing down here opens below a Level 3 card. Try the offices upstairs, people left in a hurry.", 9)
				ElseIf best < 5 Then
					IAxSay("Officer Miller", "That card will get you through the upper wings. Head for Heavy Containment. Stay away from anywhere dark you can hear dripping in.", 9)
				Else
					IAxSay("Officer Miller", "A high-clearance card. Then you can reach the exits. Go. I'm staying until my team comes back up.", 8)
				EndIf
			EndIf
			If IS10Press(r\Objects[U46_PEL_BLAST], 1.8) Then
				IS16Tell("The blast door to the rest of the lower complex. Welded shut from this side. Something has been scratching at it from the other.", 7)
			EndIf
		;---------------- the sealed wing
		Case "room2b49sealed"
			If e\EventState3 > 0 Then
				e\EventState3 = e\EventState3 - FPSfactor
				If e\EventState3 <= 0 Then
					e\EventState3 = -1
					U45Summon106(r\Objects[U46_SLD_SPAWN106])
				EndIf
			EndIf
			If IS10Press(r\Objects[U46_SLD_CALENDAR], 1.4) Then
				Select e\EventState2
					Case 1 : IS16Tell("A wall calendar, years out of date. One day is circled: INSPECTION. It is the day the wing was sealed.", 6)
					Case 2 : IS16Tell("A wall calendar, years out of date. Every day after one date has been crossed out by hand - for months.", 6)
					Default : IS16Tell("A wall calendar, years out of date. Someone has written today's date on it. The ink is still wet.", 6)
				End Select
			EndIf
			If IS10Press(r\Objects[U46_SLD_SEAL], 1.8) Then
				IS16Tell("SEALED BY ORDER. The bolts are rusted into the frame. Behind it the air hums, very low, as if machines down there never stopped.", 7)
			EndIf
	End Select
End Function
