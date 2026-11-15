;=====================================================================
; SCP: Containment Breach - Indev: nineteenth batch, six rooms from the reference images of 23 Oct 2026
;
;   room2b19office   a researcher by the desk; he faces you and talks when you come near.
;   room2b19gallery  two Class-D waiting on the floor and an attendant on the balcony; they face you.
;   room2b19hoist    the HOIST panel: pressing it sounds the hoist and lights the red lamp in the pit.
;   room2b19storage  every 30 to 70 s, while you are in the corridor, one of the shutters rattles.
;   room2b19h09      SCP-H09: the neon emblem redraws itself every few seconds while you are in the chamber;
;                    now and then it shows itself behind bars (stress +5).
;   room2b19cells    knocking from cell D-19B, every 20 to 50 s while you are in the block.
;
;   IndevU19Data.bb is generated (Tools\roomkit\gen_b19.py). Counters for the room test are Indev19*.
;   Every event returns at once when the player is not in its room, so idle rooms cost nothing.
;=====================================================================

Global Indev19Glows%, Indev19Bars%, Indev19Rattles%, Indev19Knocks%, Indev19Hoist%

Function IndevU19Dress(r.Rooms)
	Local m%, tex%, k%
	Select r\RoomTemplate\Name
		Case "room2b19h09"
			;the emblem: three frames and the barred one, all on the far wall, one shown at a time (a vertical quad already faces along x)
			For k = 0 To 3
				m = IS10Quad(150.0, 150.0, True, False)
				IS10OnPivot(m, r\Objects[U19_H09_MURAL])
				PositionEntity(m, -10 * RoomScale, 0, 0)
				If k < 3 Then
					tex = LoadTexture_Strict("GFX\map\indev_h09_" + k + ".png")
				Else
					tex = LoadTexture_Strict("GFX\map\indev_h09_x.png")
				EndIf
				EntityTexture(m, tex)
				FreeTexture(tex)
				EntityFX(m, 1 + 16)
				If k > 0 Then HideEntity(m)
				r\Objects[U19_H09_MURAL0 + k] = m
			Next
			;its glow on the room, a single small light
			m = CreateLight(2)
			LightRange(m, 3.0)
			LightColor(m, 200, 40, 40)
			EntityParent(m, r\Objects[U19_H09_MURAL])
			PositionEntity(m, -60 * RoomScale, 0, 0)
			r\Objects[U19_H09_GLOW] = m
	End Select
End Function

Function UpdateIndevU19(e.Events)
	If PlayerRoom <> e\room Then Return
	Select e\room\RoomTemplate\Name
		Case "room2b19office"
			UpdateU19Doctor(e)
		Case "room2b19gallery"
			UpdateU19Gallery(e)
		Case "room2b19hoist"
			UpdateU19Hoist(e)
		Case "room2b19storage"
			UpdateU19Shutters(e)
		Case "room2b19h09"
			UpdateU19Mural(e)
		Case "room2b19cells"
			UpdateU19Knock(e)
	End Select
End Function

;the researcher in Office 19-A. Flag n: he has been made.
Function UpdateU19Doctor(e.Events)
	Local r.Rooms = e\room, n.NPCs, d#
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, U19_OFF_DOCTOR, 90)
		IAxSkin(r\NPC[0], "GFX\npcs\indev_archivist.jpg")
	EndIf
	n = r\NPC[0]
	If n = Null Then Return
	d = EntityDistance(n\Collider, Collider)
	If d < 4.0 Then IAxFace(n, Collider)
	If d < 2.2 And MsgTimer <= 0 And Rand(500) = 1 Then
		Select Rand(3)
			Case 1
				IAxSay("Researcher", "Have you seen the transfer order? It should be on the desk. It has been on the desk since March.", 7)
			Case 2
				IAxSay("Researcher", "Leave the photographs up. The river is still there. I checked, on the intercom.", 6)
			Case 3
				IAxSay("Researcher", "The chamber with the emblem - don't look at it too long. It learns which colours you like.", 7)
		End Select
	EndIf
End Function

;the gallery: two Class-D on the floor, an attendant on the balcony. Flag n: they have been made.
Function UpdateU19Gallery(e.Events)
	Local r.Rooms = e\room, k%
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, U19_GAL_DCLASS0, 120)
		r\NPC[1] = IS16Person(r, U19_GAL_DCLASS1, 200)
		r\NPC[2] = IS16Person(r, U19_GAL_GUARD, 270)
		IAxSkin(r\NPC[2], "GFX\npcs\indev_attendant.jpg")
	EndIf
	For k = 0 To 2
		If r\NPC[k] <> Null Then
			If EntityDistance(r\NPC[k]\Collider, Collider) < 5.0 Then IAxFace(r\NPC[k], Collider)
		EndIf
	Next
	If MsgTimer <= 0 And Rand(900) = 1 Then
		If r\NPC[0] <> Null Then
			If EntityDistance(r\NPC[0]\Collider, Collider) < 2.5 Then IAxSay("Class-D", "They said the test was cancelled. They said wait anyway. So we wait.", 6)
		EndIf
	EndIf
End Function

;the HOIST panel. EventState: frames the pit lamp stays lit.
Function UpdateU19Hoist(e.Events)
	Local r.Rooms = e\room
	IndevLiftTick(e) ;the lift down to the pit
	If IS10Press(r\Objects[U19_HST_HOIST], 2.5) Then
		Indev19Hoist = Indev19Hoist + 1
		IS10Sound("SFX\Indev\buzzer.wav", r\Objects[U19_HST_HOIST], 6.0, 0.8)
		IS16Tell("The hoist motor turns over somewhere below. The pit lamp is already on.", 6)
	EndIf
End Function

;Storage B: a shutter rattles. Flag k: the countdown has started.
Function UpdateU19Shutters(e.Events)
	Local r.Rooms = e\room
	If Not IAxFlag(e, "k") Then
		IAxSetFlag(e, "k")
		e\EventState = 70 * Rand(15, 30)
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(30, 70)
		Indev19Rattles = Indev19Rattles + 1
		IS10Sound("SFX\Indev\shutter.wav", r\Objects[U19_STO_SHUT0 + Rand(0, 3)], 10.0, 0.7)
	EndIf
End Function

;SCP-H09. EventState: the frame shown (0-2, 3 = barred). EventState2: frames until it redraws.
Function UpdateU19Mural(e.Events)
	Local r.Rooms = e\room, nxt%
	e\EventState2 = e\EventState2 - FPSfactor
	If e\EventState2 > 0 Then Return
	HideEntity(r\Objects[U19_H09_MURAL0 + Int(e\EventState)])
	If Rand(12) = 1 And e\EventState < 3 Then
		nxt = 3
		Indev19Bars = Indev19Bars + 1
		IndevStress = IndevStress + 5 : If IndevStress > 100 Then IndevStress = 100
		IS10Sound("SFX\Indev\zap.wav", r\Objects[U19_H09_MURAL], 8.0, 0.6)
		If MsgTimer <= 0 Then IS16Tell("For a moment the emblem is behind bars - or you are.", 5)
		e\EventState2 = 70 * 1.5
	Else
		nxt = (Int(e\EventState) + 1) Mod 3
		Indev19Glows = Indev19Glows + 1
		e\EventState2 = 70 * Rand(3, 6)
	EndIf
	e\EventState = nxt
	ShowEntity(r\Objects[U19_H09_MURAL0 + nxt])
	If nxt = 3 Then
		LightColor(r\Objects[U19_H09_GLOW], 120, 200, 80)
	Else
		LightColor(r\Objects[U19_H09_GLOW], 200, 40 + nxt * 30, 40)
	EndIf
End Function

;Cell Block D: knocking from D-19B. Flag k: the countdown has started.
Function UpdateU19Knock(e.Events)
	Local r.Rooms = e\room
	If Not IAxFlag(e, "k") Then
		IAxSetFlag(e, "k")
		e\EventState = 70 * Rand(10, 20)
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(20, 50)
		Indev19Knocks = Indev19Knocks + 1
		IS10Sound("SFX\Indev\thump.wav", r\Objects[U19_CEL_KNOCK], 10.0, 0.8)
	EndIf
End Function
