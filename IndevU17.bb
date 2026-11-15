;=====================================================================
; SCP: Containment Breach - Indev: seventeenth batch, The Forgotten Hotel (anomalous room H-17)
;
;   room2hotelcorr  HCZ  floor H. Room H-16 is a plain guest room. Room H-17 (west) is the anomaly: walk in and its
;                        number changes for a moment, the phone on its dresser rings once, and its lamp flickers while
;                        you stay. Footsteps come up the corridor, a long way off, when you are alone in it.
;   room2hotellift  HCZ  lift lobby. The clerk talks when you come near. The lift goes down to the laundry.
;
;   IndevU17Data.bb is generated (Tools\roomkit\gen_b17.py): the U17_* constants, the FillRoom table and the events.
;   This file holds what the table calls by name, and the scripted parts: H-17, the footsteps, the clerk.
;=====================================================================

Function IndevU17Dress(r.Rooms)
	Local l%, m%, tex%
	Select r\RoomTemplate\Name
		Case "room2hotelcorr"
			;the flickering lamp of room H-17: a point light, hidden until the player is in the room
			l = CreateLight(2)
			EntityParent(l, r\Objects[U17_COR_LIGHT17])
			LightRange(l, 900.0 * RoomScale)
			LightColor(l, 255, 226, 170)
			HideEntity(l)
			r\Objects[U17_COR_LIGHTM] = l
			;the number over H-17's door: two plates on one pivot, one shown at a time. H-17 is up; H-71 while you pass
			m = IS10Quad(110.0, 55.0, True, False)
			IS10OnPivot(m, r\Objects[U17_COR_DOORPLATE])
			tex = LoadTexture_Strict("GFX\map\indev_h17_door.png")
			EntityTexture(m, tex)
			FreeTexture(tex)
			r\Objects[U17_COR_PLATE17] = m
			m = IS10Quad(110.0, 55.0, True, False)
			IS10OnPivot(m, r\Objects[U17_COR_DOORPLATE])
			tex = LoadTexture_Strict("GFX\map\indev_h71_door.png")
			EntityTexture(m, tex)
			FreeTexture(tex)
			HideEntity(m)
			r\Objects[U17_COR_PLATE71] = m
	End Select
End Function

Function UpdateIndevU17(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2hotelcorr"
			UpdateU17Corridor(e)
		Case "room2hotellift"
			IndevLiftTick(e) ;the lift down to the laundry
			UpdateU17Lobby(e)
	End Select
End Function

;room H-17 is the annex behind the west hub door: x < -256 in room units, and |z| < 400.
;EventState: the phone's countdown in frames (0 = not counting)   EventState2: frames until the lamp next changes
;EventState3: frames until the next footsteps.   flags: i inside H-17 now, p the phone has rung.
Function UpdateU17Corridor(e.Events)
	Local r.Rooms = e\room, l% = r\Objects[U17_COR_LIGHTM], ph% = r\Objects[U17_COR_PHONE], far% = r\Objects[U17_COR_FAR]
	Local p17% = r\Objects[U17_COR_PLATE17], p71% = r\Objects[U17_COR_PLATE71]
	Local inside%, near%, px#, pz#
	If PlayerRoom <> r Then
		HideEntity(l)
		Return
	EndIf
	IAxLocal(r)
	px = TFormedX() : pz = TFormedZ()
	inside = (px < -256.0 And Abs(pz) < 400.0)
	;the number over the door reads H-71 while you pass it, and goes back to H-17 once you are clear
	near = (px > -260.0 And px < -140.0 And Abs(pz) < 150.0)
	If near Then
		If Not IAxFlag(e, "x") Then
			IAxSetFlag(e, "x")
			HideEntity(p17)
			ShowEntity(p71)
			Indev17Flips = Indev17Flips + 1
		EndIf
	ElseIf IAxFlag(e, "x") Then
		IS13Drop(e, "x")
		HideEntity(p71)
		ShowEntity(p17)
	EndIf
	If inside Then
		If Not IAxFlag(e, "i") Then
			IAxSetFlag(e, "i")
			IS16Tell("The number on the door reads H-17. For a moment, as you pass it, it reads H-71.", 8)
			IndevStress = Min(100, IndevStress + 5)
			If Not IAxFlag(e, "p") Then e\EventState = 70 * 10
		EndIf
		;the phone rings once, ten seconds after you come in
		If e\EventState > 0 Then
			e\EventState = e\EventState - FPSfactor
			If e\EventState <= 0 Then
				IAxSetFlag(e, "p")
				Indev17Rings = Indev17Rings + 1
				IS10Sound("SFX\Indev\doorbell.wav", ph, 6.0, 1.0)
				IS16Tell("The phone on the dresser rings once. When you pick it up, nobody is on the line, and somebody is breathing a long way off, in a building with a great many doors.", 9)
			EndIf
		EndIf
		;the lamp flickers: on and off at random while you stay
		e\EventState2 = e\EventState2 - FPSfactor
		If e\EventState2 <= 0 Then
			e\EventState2 = Rand(4, 30)
			If Rand(2) = 1 Then
				ShowEntity(l)
			Else
				HideEntity(l)
			EndIf
			Indev17Flicks = Indev17Flicks + 1
		EndIf
	Else
		If IAxFlag(e, "i") Then IS13Drop(e, "i")
		HideEntity(l)
		;footsteps, a long way up the corridor, when you are alone in it
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rand(15, 40)
			Indev17Steps = Indev17Steps + 1
			IS10Sound("SFX\Indev\thump.wav", far, 25.0, 0.5)
		EndIf
	EndIf
End Function

;the clerk, behind the desk. He talks when you come near, and turns to you.
Function UpdateU17Lobby(e.Events)
	Local r.Rooms = e\room, n.NPCs, d#
	If PlayerRoom <> r Then Return
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, U17_LOB_CLERK, 180)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_tech.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Clerk", "Room H-17 is not in service. It has not been in service since the rooms were numbered.", 7)
				Case 2
					IAxSay("Clerk", "Sign for your key. Not that one. The one with the number you keep reading.", 6)
				Case 3
					IAxSay("Clerk", "The lift goes down to the laundry. It goes nowhere else. Please do not ask it to.", 6)
			End Select
		EndIf
	EndIf
End Function
