;=====================================================================
; SCP: Containment Breach - Indev zone filler rooms in the v0.1 style
;
;   24 generated rooms (11 hallways, 4 corners, 4 T junctions, 3 crossroads,
;   2 dead ends). They are ordinary random filler for the Indev zone - the map
;   picks them by commonness like any vanilla hallway.
;
;   What a room needs created (items, doors, fans, a lift, an NPC spot) is in
;   IndevV01Data.bb, which Tools\roomkit\gen_v01.py writes from the same Python
;   that builds the meshes. This file holds the helpers that table calls and
;   the one shared event ("v01room") that every v0.1 room gets:
;     - the fans turn
;     - room2v_lift: the lift to its basement store
;     - room2v_guard: a guard still at his post behind the hatch
;     - room1v_173: a guard up on the gallery of the old SCP-173 yard
;     - room2v_lockers / room2v_medbay: a body
;   No globals. Objects[0..1] lift pivots, [2] duct fan, [3] ceiling fan,
;   [4] NPC spot; NPC[0] the room's NPC; EventState 1 = NPC placed,
;   EventState2 lift, EventState3 pause between the guard's lines.
;=====================================================================

Function IV1Item(r.Rooms, name$, lx#, ly#, lz#, chance%)
	If chance < 100 Then
		If Rand(100) > chance Then Return
	EndIf
	IAxItem(r, name, lx, ly, lz)
End Function

Function IV1Door(r.Rooms, lx#, ly#, lz#, angle%, key%)
	Local d.Doors = CreateDoor(r\zone, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, angle, r, False, False, key)
	d\AutoClose = False : d\open = False
	IndevButtonsToWall(d) ;out of the thick side-room walls (IndevAnnex.bb)
End Function

Function UpdateIndevV01(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, tex%, d#

	If r\dist < 10.0 Then
		If r\Objects[2] <> 0 Then TurnEntity(r\Objects[2], 0, 0, 5.0 * FPSfactor)
		If r\Objects[3] <> 0 Then TurnEntity(r\Objects[3], 0, 2.0 * FPSfactor, 0)
	EndIf
	If PlayerRoom <> r Then Return

	;the lift (only room2v_lift has one)
	If r\Objects[0] <> 0 And r\Objects[1] <> 0 Then
		If r\RoomDoors[0] <> Null And r\RoomDoors[1] <> Null Then
			e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
		EndIf
	EndIf
	If KillTimer < 0 Then Return
	If r\Objects[4] = 0 Then Return

	;---- the room's NPC, placed the first time the player walks in
	If e\EventState = 0 Then
		e\EventState = 1
		Select r\RoomTemplate\Name
			Case "room2v_guard", "room1v_173"
				n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[4], True), EntityY(r\Objects[4], True) + 0.35, EntityZ(r\Objects[4], True))
				n\State = 9
				;the booth is on the +x side of its hallway, the gallery on the -x side of the yard: both face inwards
				If r\RoomTemplate\Name = "room2v_guard" Then
					RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
				Else
					RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) - 90, 0)
				EndIf
				r\NPC[0] = n
			Case "room2v_lockers"
				;a researcher sitting against the cabinets
				n = CreateNPC(NPCtypeD, EntityX(r\Objects[4], True), EntityY(r\Objects[4], True) + 0.5, EntityZ(r\Objects[4], True))
				RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
				n\State = 3
				SetNPCFrame(n, 40)
				n\IsDead = True
				r\NPC[0] = n
			Case "room2v_medbay"
				n = CreateNPC(NPCtypeD, EntityX(r\Objects[4], True), EntityY(r\Objects[4], True) + 0.5, EntityZ(r\Objects[4], True))
				RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 200, 0)
				n\State = 3
				SetNPCFrame(n, 19)
				n\IsDead = True
				r\NPC[0] = n
		End Select
	EndIf

	n = r\NPC[0]
	If n = Null Then Return
	Select r\RoomTemplate\Name
		Case "room2v_lockers"
			IAxSkin(n, "GFX\npcs\scientist.jpg")
		Case "room2v_medbay"
			IAxSkin(n, "GFX\npcs\body1.jpg")
		Case "room2v_guard"
			;he watches you (state 9 turns his head) and has a few things to say through the hatch
			n\State = 9
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
			d = EntityDistance(n\Collider, Collider)
			If d < 2.4 And e\EventState3 <= 0 And MsgTimer <= 0 Then
				Select Rand(4)
					Case 1 IAxSay("Guard", "Post's closed. Nothing goes through this hatch until somebody upstairs says so.", 6)
					Case 2 IAxSay("Guard", "You're not on my list. Then again nobody's on my list any more.", 6)
					Case 3 IAxSay("Guard", "Keep walking. And if you see the statue, don't blink for me either.", 6)
					Case 4 IAxSay("Guard", "Radio's been dead for an hour. I'm staying where the wall is thick.", 6)
				End Select
				e\EventState3 = 70 * 40
			EndIf
		Case "room1v_173"
			n\State = 9
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
			IAxLocal(r)
			If TFormedZ() > -300.0 And e\EventState3 <= 0 And MsgTimer <= 0 Then
				Select Rand(3)
					Case 1 IAxSay("Guard", "Yard's empty. They moved the sculpture out years ago - this is just where they used to do it.", 7)
					Case 2 IAxSay("Guard", "Three of you went in there at a time. One to clean, two to watch. Usually worked.", 7)
					Case 3 IAxSay("Guard", "I'm not coming down. You can't make me come down.", 5)
				End Select
				e\EventState3 = 70 * 50
			EndIf
	End Select
End Function
