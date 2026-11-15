;=====================================================================
; SCP: Containment Breach - Indev: twenty-sixth batch, the outdoor expansion (unnamed)
;
;   room2b26exit     the checkpoint terminal (click); the lift up to the surface. On the surface: grey fog, an
;                    overcast sky and rain (IndevOutdoorFrame, called every frame from the main loop after the
;                    game sets its own fog), wind every 15-30 s, now and then something between the trees, a note
;                    in the clearing, and the shed's generator (click to start it).
;   room2b26labs     the lab terminal (click); the ward creaks; the control room's console sparks every 20-40 s.
;   room2b26utility  the drainage chamber drips every 15-25 s; the power panel (click); the observation room's
;                    window - every minute or two, a figure between the trees, a little closer each time.
;
;   Everything returns at once outside its room; the weather costs one quad and a fog setting.
;=====================================================================

Global Indev26Rain%, Indev26Outside%, Indev26Events%

Function IndevU26Dress(r.Rooms)
End Function

;true while the player stands on the surface of the exit room
Function IndevU26OnSurface%()
	If PlayerRoom = Null Then Return False
	If PlayerRoom\RoomTemplate\Name <> "room2b26exit" Then Return False
	Return EntityY(Collider) > EntityY(PlayerRoom\obj) + 900 * RoomScale
End Function

;called from the main loop right after the game sets fog and sky: on the surface, grey fog, an overcast sky
;and the rain overlay; anywhere else the overlay is hidden and the game's own settings stand
Function IndevOutdoorFrame()
	Local tex%
	U33Frame() ;SCP-4890's purple space (IndevU33.bb)
	U36Frame() ;SCP-1479's night fog, SCP-1200's glow (IndevU36.bb)
	U37Frame() ;SCP-028's still yard, the archive's dust, the reactor's blue (IndevU37.bb)
	U38Frame() ;Corridor L-40's haze (IndevU38.bb)
	U45Frame() ;the Off-Shoot Hall's darkness (IndevU45.bb)
	Indev26Outside = IndevU26OnSurface()
	If Not Indev26Outside Then
		If Indev26Rain <> 0 Then HideEntity(Indev26Rain)
		Return
	EndIf
	CameraFogMode(Camera, 1)
	CameraFogRange(Camera, 1.5, 20.0)
	CameraFogColor(Camera, 118, 124, 128)
	CameraClsColor(Camera, 118, 124, 128)
	CameraRange(Camera, 0.05, 24.0)
	AmbientLight(Max(Brightness, 70), Max(Brightness, 72), Max(Brightness, 76))
	If Indev26Rain = 0 Then
		;a rain-streak quad just in front of the camera, its texture scrolled down every frame
		Indev26Rain = IS10Quad(1.0, 1.0, False, False)
		tex = LoadTexture_Strict("GFX\map\indev_o_rain.png", 2)
		ScaleTexture(tex, 0.5, 0.5)
		EntityTexture(Indev26Rain, tex)
		FreeTexture(tex)
		EntityFX(Indev26Rain, 1 + 8)
		EntityBlend(Indev26Rain, 3)
		EntityAlpha(Indev26Rain, 0.55)
		EntityOrder(Indev26Rain, -2)
		EntityParent(Indev26Rain, Camera)
		RotateEntity(Indev26Rain, -90, 0, 0)
		PositionEntity(Indev26Rain, 0, 0, 0.3)
		ScaleEntity(Indev26Rain, 0.9, 1.0, 0.6)
	EndIf
	ShowEntity(Indev26Rain)
	PositionTexture(GetEntityBrush0Tex(Indev26Rain), 0, (MilliSecs() Mod 700) / 700.0)
End Function

;the first texture of an entity's first surface, so its offset can be moved
Function GetEntityBrush0Tex%(m%)
	Local s% = GetSurface(m, 1), b% = GetSurfaceBrush(s), t% = GetBrushTexture(b, 0)
	FreeBrush(b)
	Return t
End Function

Function UpdateIndevU26(e.Events)
	If PlayerRoom <> e\room Then Return
	Select e\room\RoomTemplate\Name
		Case "room2b26exit"
			UpdateU26Exit(e)
		Case "room2b26labs"
			UpdateU26Labs(e)
		Case "room2b26utility"
			UpdateU26Utility(e)
	End Select
End Function

;EventState: wind countdown. EventState3: the trees countdown (EventState2 is the lift's). Flags: g generator started, c clearing seen.
Function UpdateU26Exit(e.Events)
	Local r.Rooms = e\room
	IndevLiftTick(e) ;the lift up to the surface
	If IS10Press(r\Objects[U26_EXT_TERMINAL], 2.0) Then
		IS16Tell("CHECKPOINT: lift to surface OPERATIONAL. Floodlights: GENERATOR. Weather: rain, fog. Personnel outside: 0. Last badge out: yours?", 7)
	EndIf
	If Not Indev26Outside Then Return
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(15, 30)
		IS10Sound("SFX\Indev\wind.wav", r\Objects[U26_EXT_OUTSIDE], 30.0, 0.6)
	EndIf
	If e\EventState3 <= 0 Then e\EventState3 = 70 * Rand(60, 120)
	e\EventState3 = e\EventState3 - FPSfactor
	If e\EventState3 <= 0 Then
		Indev26Events = Indev26Events + 1
		IS10Sound("SFX\Indev\thump.wav", r\Objects[U26_EXT_CLEARING], 40.0, 0.5)
		If MsgTimer <= 0 Then
			Select Rand(3)
				Case 1 : IS16Tell("Something moves between the trees, keeping pace with you.", 5)
				Case 2 : IS16Tell("A branch cracks somewhere out in the fog. Then another, closer.", 5)
				Case 3 : IS16Tell("For a moment the rain stops, and the forest is very quiet.", 5)
			End Select
		EndIf
	EndIf
	If (Not IAxFlag(e, "c")) And EntityDistance(Collider, r\Objects[U26_EXT_CLEARING]) < 3.0 Then
		IAxSetFlag(e, "c")
		IS16Tell("A clearing. Someone camped here, not long ago. There is a note under a rock.", 6)
	EndIf
	If IS10Press(r\Objects[U26_EXT_GENERATOR], 2.0) Then
		If IAxFlag(e, "g") Then
			IS16Tell("The generator is running. It is the loudest thing for miles.", 4)
		Else
			IAxSetFlag(e, "g")
			Indev26Events = Indev26Events + 1
			IS10Sound("SFX\Indev\buzzer.wav", r\Objects[U26_EXT_GENERATOR], 12.0, 0.9)
			IS16Tell("Third pull, and the generator coughs into life. Out by the checkpoint, the floodlights buzz brighter.", 7)
		EndIf
	EndIf
	If IS10Press(r\Objects[U26_EXT_CAR], 2.0) Then
		IS16Tell("The car is unlocked and empty. Keys in the ignition, a cold coffee, a map with this road circled. The engine won't turn over.", 7)
	EndIf
End Function

;EventState: the spark countdown.
Function UpdateU26Labs(e.Events)
	Local r.Rooms = e\room
	If IS10Press(r\Objects[U26_LAB_LABTERM], 2.0) Then
		IS16Tell("LAB TERMINAL: sample 3 (moss, north fence) - growth +4 cm/day. Sample 7 (needles) - warm to the touch. Sample 9: MISSING.", 7)
	EndIf
	If EntityDistance(Collider, r\Objects[U26_LAB_SPARK]) < 6.0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 70 * Rand(20, 40)
			Indev26Events = Indev26Events + 1
			IS10Sound("SFX\Indev\zap.wav", r\Objects[U26_LAB_SPARK], 8.0, 0.7)
			If MsgTimer <= 0 Then IS16Tell("The broken console spits sparks. One of the cracked monitors flickers on, shows an empty room, and dies.", 5)
		EndIf
	EndIf
	If (Not IAxFlag(e, "w")) And EntityDistance(Collider, r\Objects[U26_LAB_WARD]) < 3.0 Then
		IAxSetFlag(e, "w")
		IS10Sound("SFX\Indev\creak.wav", r\Objects[U26_LAB_WARD], 8.0, 0.7)
		IS16Tell("One of the ward's beds creaks, as if someone just got up from it.", 5)
	EndIf
End Function

;EventState: the drip countdown. EventState2: the figure countdown. EventState3: how many times it has been seen.
Function UpdateU26Utility(e.Events)
	Local r.Rooms = e\room
	If EntityDistance(Collider, r\Objects[U26_UTL_DRIP]) < 7.0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 70 * Rand(15, 25)
			IS10Sound("SFX\Indev\hose.wav", r\Objects[U26_UTL_DRIP], 8.0, 0.4)
		EndIf
	EndIf
	If IS10Press(r\Objects[U26_UTL_POWER], 2.0) Then
		IS10Sound("SFX\Indev\buzzer.wav", r\Objects[U26_UTL_POWER], 6.0, 0.7)
		IS16Tell("The panel hums: MAIN - ON. SURFACE LIFT - ON. FLOODLIGHTS - GENERATOR. DRAINAGE PUMP - FAULT.", 6)
	EndIf
	If EntityDistance(Collider, r\Objects[U26_UTL_OBS]) < 5.0 Then
		If e\EventState2 <= 0 Then e\EventState2 = 70 * Rand(30, 60)
		e\EventState2 = e\EventState2 - FPSfactor
		If e\EventState2 <= 0 Then
			e\EventState2 = 70 * Rand(60, 120)
			e\EventState3 = e\EventState3 + 1
			Indev26Events = Indev26Events + 1
			If MsgTimer <= 0 Then
				If e\EventState3 < 3 Then
					IS16Tell("Through the rain on the window: a figure between the trees. You blink, and it's gone.", 5)
				Else
					IndevStress = Min(100, IndevStress + 10)
					IS16Tell("The figure is at the edge of the trees now, much closer than before. It is facing the window.", 6)
				EndIf
			EndIf
		EndIf
	EndIf
End Function
