;=====================================================================
; SCP: Containment Breach - Indev: eighteenth batch, The Hollowcrest (six original hotel rooms)
;
;   room2hcrecep     the night counter: the ledger, the anomaly register and a keycard. Nothing scripted.
;   room2hcguest117  Guest Room 117: its telephone is not connected, and it rings ~8 s after you come in.
;   room2hcservice   the service lift: its floor display shows G or S, and flips now and then while you stand near it.
;   room2hcboiler    the control panel: the gauge reads 90 with the boiler off. Clicking the panel says so.
;   room2hckitchen   the fridge: while you are alone in the kitchen it clicks on its own, every 40 to 90 seconds.
;   room2hcballroom  the footsteps: while you are alone in the ballroom they come from the far end, every 25 to 60 s.
;
;   IndevU18Data.bb is generated (Tools\roomkit\gen_b18.py): the U18_* constants, the FillRoom table and the events.
;   The flags and countdowns are in the event, as in the other batches (see IAxFlag and IS13Drop).
;=====================================================================

Function IndevU18Dress(r.Rooms)
	Local m%, tex%
	Select r\RoomTemplate\Name
		Case "room2hcservice"
			;the floor display: a G quad (shown) and an S quad (hidden), hung beside the lift door
			m = IS10Quad(60.0, 60.0, True, False)
			IS10OnPivot(m, r\Objects[U18_SVC_DISPLAY])
			tex = LoadTexture_Strict("GFX\map\indev_svc_G.png")
			EntityTexture(m, tex)
			FreeTexture(tex)
			r\Objects[U18_SVC_DISPLAYG] = m
			m = IS10Quad(60.0, 60.0, True, False)
			IS10OnPivot(m, r\Objects[U18_SVC_DISPLAY])
			tex = LoadTexture_Strict("GFX\map\indev_svc_S.png")
			EntityTexture(m, tex)
			FreeTexture(tex)
			HideEntity(m)
			r\Objects[U18_SVC_DISPLAYS] = m
	End Select
End Function

Function UpdateIndevU18(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2hcguest117"
			UpdateU18Phone(e)
		Case "room2hcservice"
			IndevLiftTick(e) ;the service lift
			UpdateU18Display(e)
		Case "room2hcboiler"
			UpdateU18Panel(e)
		Case "room2hckitchen"
			UpdateU18Fridge(e)
		Case "room2hcballroom"
			UpdateU18Echo(e)
	End Select
End Function

;the telephone in Guest Room 117 rings once, about eight seconds after you come in. Flag i: you are in the room.
;flag p: it has rung. EventState: the countdown, in frames.
Function UpdateU18Phone(e.Events)
	Local r.Rooms = e\room, ph% = r\Objects[U18_GST_PHONE]
	If PlayerRoom <> r Then
		If IAxFlag(e, "i") Then IS13Drop(e, "i")
		Return
	EndIf
	If Not IAxFlag(e, "i") Then
		IAxSetFlag(e, "i")
		If Not IAxFlag(e, "p") Then e\EventState = 70 * 8
	EndIf
	If e\EventState > 0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 0
			IAxSetFlag(e, "p")
			Indev18Rings = Indev18Rings + 1
			IS10Sound("SFX\Indev\doorbell.wav", ph, 6.0, 1.0)
			IS16Tell("The telephone rings. It is not connected to anything. Nobody is on the line, and somebody is breathing, far off, in a building with a great many doors.", 9)
		EndIf
	EndIf
End Function

;the service lift's floor display: when you stand within three metres of it, it now and then flips between G and S.
;EventState: 0 the G is showing, 1 the S is showing.  EventState3: frames until the next chance to flip (EventState2 is the lift's).
Function UpdateU18Display(e.Events)
	Local r.Rooms = e\room, pv% = r\Objects[U18_SVC_DISPLAY], g% = r\Objects[U18_SVC_DISPLAYG], s% = r\Objects[U18_SVC_DISPLAYS]
	If PlayerRoom <> r Then Return
	e\EventState3 = e\EventState3 - FPSfactor
	If e\EventState3 <= 0 And EntityDistance(Collider, pv) < 3.0 Then
		e\EventState3 = Rand(120, 400)
		If Rand(3) = 1 Then
			Indev18Flips = Indev18Flips + 1
			If e\EventState = 0 Then
				e\EventState = 1
				HideEntity(g)
				ShowEntity(s)
			Else
				e\EventState = 0
				HideEntity(s)
				ShowEntity(g)
			EndIf
		EndIf
	EndIf
End Function

;the panel in the boiler chamber: pressing it tells you what the gauge says
Function UpdateU18Panel(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U18_BLR_PANEL]
	If PlayerRoom <> r Then Return
	If IS10Press(p, 2.5) Then
		Indev18Panel = Indev18Panel + 1
		IS16Tell("The gauge reads ninety. The boiler has been off since 1984, and the panel under your hand is warm.", 8)
	EndIf
End Function

;the fridge in the cold kitchen clicks on its own while you are alone in the room. Flag k: started.
Function UpdateU18Fridge(e.Events)
	Local r.Rooms = e\room, f% = r\Objects[U18_KIT_FRIDGE]
	If PlayerRoom <> r Then Return
	If Not IAxFlag(e, "k") Then
		IAxSetFlag(e, "k")
		e\EventState = 70 * Rand(20, 40)
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(40, 90)
		Indev18Clicks = Indev18Clicks + 1
		IS10Sound("SFX\Indev\clicks.wav", f, 8.0, 0.8)
	EndIf
End Function

;footsteps in the ballroom, from one of three places, while you are alone in it. Flag k: started.
Function UpdateU18Echo(e.Events)
	Local r.Rooms = e\room, pv%, pick%
	If PlayerRoom <> r Then Return
	If Not IAxFlag(e, "k") Then
		IAxSetFlag(e, "k")
		e\EventState = 70 * Rand(25, 60)
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(25, 60)
		pick = Rand(0, 2)
		If pick = 0 Then
			pv = r\Objects[U18_BAL_ECHO0]
		ElseIf pick = 1 Then
			pv = r\Objects[U18_BAL_ECHO1]
		Else
			pv = r\Objects[U18_BAL_ECHO2]
		EndIf
		Indev18Echoes = Indev18Echoes + 1
		IS10Sound("SFX\Indev\thump.wav", pv, 25.0, 0.5)
	EndIf
End Function
