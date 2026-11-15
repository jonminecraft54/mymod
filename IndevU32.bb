;=====================================================================
; SCP: Containment Breach - Indev: the thirty-second batch - Gate V, the underground emergency exit
;
;   room2b32gatev (Entrance Zone). The heavy GATE V door opens two ways:
;     a Level 4 / 5 / 6 keycard at the reader      - quietly
;     the break-glass emergency release           - for anyone, and alarm circuit 7-V calls the response unit
;   Behind it a stairwell 1024 deep, a bulkhead tunnel with the circuit's breaker box (cut it before you reach
;   the atrium and nobody comes), and the exit atrium: the console, and the open vault hatch onto the mountains.
;   The endings:
;     V1  you walk out of the hatch with no one waiting - snow, sky, nobody following
;     V2  Nine-Tailed Fox are waiting at the hatch (the alarm called them) and you walk into them: recontained
;     V3  you fired the seal charges at the console with Nine-Tailed Fox at the hatch: the outer passage comes
;         down on them, and you climb out through the dust, and Gate V is gone
;=====================================================================

Global I32Open%      ;0 locked, 1 opened by keycard, 2 opened by the emergency release
Global I32Alarm%     ;circuit 7-V is live
Global I32MTF%       ;the response unit is at the hatch
Global I32Charge#, I32Blown%, I32Siren#, I32Uses%
Global I32Lock#      ;frames until the lockdown after the break-glass release (I32Open 3 = locked down)
Global I32SirenCHN%  ;the one siren channel (never two at once)
Global I32Exit%, I32ExitT#, I32ExitEnd$, I32WindCHN%   ;the walk out of the hatch, before the ending screen

;the siren: started only when it is not already sounding
Function U32Siren()
	If I32SirenCHN <> 0 Then
		If ChannelPlaying(I32SirenCHN) Then Return
	EndIf
	I32SirenCHN = PlaySound_Strict(LoadTempSound("SFX\Alarm\Alarm2_1.ogg"))
	If I32SirenCHN <> 0 Then ChannelVolume(I32SirenCHN, 0.45 * SFXVolume)
End Function

Function U32SirenStop()
	If I32SirenCHN <> 0 Then
		If ChannelPlaying(I32SirenCHN) Then StopChannel(I32SirenCHN)
		I32SirenCHN = 0
	EndIf
End Function
Dim I32Fig%(2)

Function Indev32Reset(newGame%)
	Local k%
	If newGame Then
		I32Open = 0 : I32Alarm = False : I32MTF = False : I32Blown = False : I32Lock = 0
	EndIf
	I32Charge = 0 : I32Siren = 0
	I32Exit = False : I32ExitT = 0 : I32ExitEnd = ""
	U32SirenStop()
	;I32Fig() is not cleared: the room sets it when it is built, and a quick load keeps the room (and the figures)
End Function

Function IndevU32Dress(r.Rooms)
	Local k%, m%
	If r\RoomTemplate\Name <> "room2b32gatev" Then Return
	;the heavy GATE V door, between the antechamber and the stairwell
	r\RoomDoors[0] = CreateDoor(r\zone, r\x + 780.0 * RoomScale, r\y, r\z - 548.0 * RoomScale, 0, r, False, 2, 0)
	r\RoomDoors[0]\AutoClose = False : r\RoomDoors[0]\open = False : r\RoomDoors[0]\locked = True
	IndevButtonsToWall(r\RoomDoors[0])
	If I32Open > 0 Then r\RoomDoors[0]\locked = False : r\RoomDoors[0]\open = True
	U30Prop(r, r\Objects[U32_GV_HATCH], "GFX\map\props\gatev_hatch.b3d", 1.0, True)
	For k = 0 To 2
		m = U30Prop(r, r\Objects[U32_GV_MTF0 + k], "GFX\map\props\gatev_mtf.b3d", 1.0, True)
		If m <> 0 Then
			TurnEntity(m, 0, -90, 0)
			If I32MTF And (Not I32Blown) Then ShowEntity(m) Else HideEntity(m)
		EndIf
		I32Fig(k) = m
	Next
End Function

Function U32HasCard%()
	Return (U30Has("keygatev") <> Null Or U30Has("key4") <> Null Or U30Has("key5") <> Null Or U30Has("key6") <> Null)
End Function

Function UpdateIndevU32(e.Events)
	Local r.Rooms = e\room, d.Doors = r\RoomDoors[0], lx#, ly#, lz#, k%, inShaft%, inTunnel%
	;keep the world in step with the state (after a load the room is rebuilt before the side save is read)
	If d <> Null Then
		If I32Open = 1 Or I32Open = 2 Then
			If d\locked Then d\locked = False : d\open = True
		ElseIf I32Open = 3 Then
			If d\open Or (Not d\locked) Then d\open = False : d\locked = True
		EndIf
	EndIf
	For k = 0 To 2
		If I32Fig(k) <> 0 Then
			If I32MTF And (Not I32Blown) Then
				ShowEntity(I32Fig(k))
			Else
				HideEntity(I32Fig(k))
			EndIf
		EndIf
	Next
	;the lockdown: two minutes after the glass, the gate shuts and locks
	If I32Lock > 0 Then
		I32Lock = I32Lock - FPSfactor
		If (I32Lock < 70 * 60 And I32Lock + FPSfactor >= 70 * 60) Then IS16Tell("PA: 'Gate V lockdown in sixty seconds.'", 4)
		If (I32Lock < 70 * 10 And I32Lock + FPSfactor >= 70 * 10) Then IS16Tell("PA: 'Gate V lockdown in ten seconds.'", 4)
		If I32Lock <= 0 Then
			I32Lock = 0 : I32Open = 3
			If d <> Null Then d\open = False : d\locked = True
			If PlayerRoom = r Then IS16Tell("GATE V LOCKDOWN. The heavy door grinds shut and the reader goes red.", 6)
		EndIf
	EndIf
	If PlayerRoom <> r Then
		U32SirenStop()
		Return
	EndIf
	;no site announcements in here: stop one that was already playing
	If IntercomStreamCHN <> 0 Then
		StopStream_Strict(IntercomStreamCHN) : IntercomStreamCHN = 0
	EndIf
	If I32Exit Then
		U32ExitScene(e)
		Return
	EndIf
	TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
	lx = TFormedX() : ly = TFormedY() : lz = TFormedZ()
	inShaft = (lz < -556 And lx > 256 And ly < 300)
	inTunnel = (lx > 760 And lz > -556 And ly < -600)
	;event: the stairwell lights
	If inShaft Then
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rnd(10, 25)
			LightBlink = Rnd(1.0, 2.0)
			IS10Sound("SFX\Indev\uvhum.wav", Collider, 6.0, 0.5)
		EndIf
	EndIf
	;event: footsteps on the landing above (once)
	If inShaft And ly < -450 And (Not IAxFlag(e, "f")) Then
		IAxSetFlag(e, "f")
		IS10Sound("SFX\Indev\thump.wav", Collider, 8.0, 0.4)
		IS16Tell("Footsteps on the landing above you. They stop when you stop. Nobody looks over the rail.", 6)
	EndIf
	;event: a steam pipe bursts in the tunnel (once)
	If inTunnel And lz > 250 And (Not IAxFlag(e, "s")) Then
		IAxSetFlag(e, "s")
		Local p.Particles, i%
		TFormPoint(860, -1024 + 240, 330, r\obj, 0)
		For i = 0 To 11
			p = CreateParticle(TFormedX() + Rnd(-0.2, 0.2), TFormedY(), TFormedZ() + Rnd(-0.2, 0.2), 6, 0.25, -0.05, 120)
		Next
		IS10Sound("SFX\General\Hiss.ogg", Collider, 6.0, 0.9)
		BlurTimer = Max(BlurTimer, 70 * 3)
		If Abs(lz - 330) < 120 Then Injuries = Injuries + 0.1
		IS16Tell("A pipe joint over the tunnel blows: a roar of scalding steam. Then just the hiss, and the drip.", 6)
	EndIf
	;event: the response unit on the radio
	If I32MTF And (Not I32Blown) And (Not IAxFlag(e, "r")) Then
		IAxSetFlag(e, "r")
		IAxSay("MTF radio", "Epsilon-11, in position at the Gate V hatch. Whoever comes out of that tunnel, we take them.", 8)
	EndIf
	If I32Open = 2 And (Not I32Alarm) And (Not I32MTF) And ly < -600 And (Not IAxFlag(e, "q")) Then
		IAxSetFlag(e, "q")
		IAxSay("MTF radio", "Control, circuit 7-V just dropped. Probably a fault. Holding at the Gate B checkpoint.", 8)
	EndIf
	;the gate
	If IS10Press(r\Objects[U32_GV_READER], 1.4) Then
		If I32Open = 1 Or I32Open = 2 Then
			IS16Tell("GATE V: OPEN.", 2)
		ElseIf U32HasCard() Then
			I32Open = 1 : I32Uses = I32Uses + 1
			If d <> Null Then d\locked = False : d\open = True
			IS10Sound("SFX\Indev\beep.wav", r\Objects[U32_GV_READER], 4.0, 0.9)
			If U30Has("keygatev") <> Null Then
				IS16Tell("GATE V ACCESS CARD ACCEPTED. The heavy door grinds aside onto a stairwell going down.", 6)
			Else
				IS16Tell("LEVEL 4 CLEARANCE ACCEPTED. GATE V: OPEN. The heavy door grinds aside onto a stairwell going down.", 6)
			EndIf
		Else
			IS16Tell("GATE V - UNDERGROUND EMERGENCY EXIT. GATE V ACCESS CARD OR LEVEL 4 CLEARANCE REQUIRED. A sticker under the reader: 'Card held by the Site Director - Administration.'", 7)
		EndIf
	EndIf
	If IS10Press(r\Objects[U32_GV_GLASS], 1.4) Then
		If I32Open = 3 Then
			IS16Tell("The release is spent - only a Level 4 card opens the gate now.", 4)
		ElseIf I32Open > 0 Then
			IS16Tell("The glass is already broken - or never needed to be.", 3)
		Else
			I32Open = 2 : I32Alarm = True : I32Uses = I32Uses + 1
			I32Lock = 70 * 120
			If d <> Null Then d\locked = False : d\open = True
			U32Siren()
			IS16Tell("Glass breaks. GATE V EMERGENCY RELEASE - CIRCUIT 7-V: SECURITY RESPONSE DISPATCHED TO THE EXIT HATCH.", 7)
		EndIf
	EndIf
	;the siren, while circuit 7-V is live
	If I32Alarm Then
		U32Siren()
	Else
		U32SirenStop()
	EndIf
	;the breaker in the tunnel
	If IS10Press(r\Objects[U32_GV_BREAKER], 1.6) Then
		If I32Alarm Then
			I32Alarm = False : I32Uses = I32Uses + 1
			IS10Sound("SFX\Indev\thump.wav", r\Objects[U32_GV_BREAKER], 5.0, 1.0)
			If I32MTF Then
				IS16Tell("You throw the breaker. The siren dies - but the response unit is already at the hatch.", 6)
			Else
				IS16Tell("You throw the breaker down. The siren dies mid-wail. Circuit 7-V: OFF. Nobody is coming.", 6)
			EndIf
		Else
			IS16Tell("CIRCUIT 7-V. The breaker is down. The tunnel is quiet.", 4)
		EndIf
	EndIf
	;into the atrium: if the alarm is live, they are already there
	If ly < -600 And lx < 744 And lz > 200 And I32Alarm And (Not I32MTF) Then
		I32MTF = True
		For k = 0 To 2
			If I32Fig(k) <> 0 Then ShowEntity(I32Fig(k))
		Next
		IS16Tell("Shapes against the light of the hatch. Nine-Tailed Fox - they were waiting for whoever came out.", 7)
	EndIf
	;the console: the seal charges
	If IS10Press(r\Objects[U32_GV_CONSOLE], 1.8) Then
		If I32Blown Then
			IS16Tell("SEAL CHARGES: FIRED. OUTER PASSAGE: COLLAPSED. There is a gap at the top of the rubble. Daylight.", 6)
		ElseIf I32Charge > 0 Then
			IS16Tell("The countdown is running.", 2)
		ElseIf I32MTF Then
			I32Charge = 70 * 5
			I32Uses = I32Uses + 1
			IS16Tell("HOSTILES AT HATCH - SEAL CHARGES ARMED. FIVE SECONDS. Get back from the hatch!", 5)
		Else
			IS16Tell("GATE V STATUS: HATCH OPEN. SEAL CHARGES ARMED. DETONATE ONLY IF HOSTILES ARE AT THE HATCH.", 6)
		EndIf
	EndIf
	If I32Charge > 0 Then
		I32Charge = I32Charge - FPSfactor
		If I32Charge <= 0 Then
			I32Charge = 0 : I32Blown = True
			CameraShake = 6.0 : LightFlash = 2.5 : BlurTimer = 70 * 4
			IS10Sound("SFX\Indev\thump.wav", r\Objects[U32_GV_PORTAL], 30.0, 1.0)
			For k = 0 To 2
				If I32Fig(k) <> 0 Then HideEntity(I32Fig(k))
			Next
			IS16Tell("The charges go off over the hatch. Rock and dust come down on the shapes in the light. When it clears there is a gap at the top - and daylight.", 9)
		EndIf
	EndIf
	;through the hatch: the end
	;the unit at the hatch stops you before you reach them (they stand at x -930)
	If I32MTF And (Not I32Blown) And lx < -800 And lz > 480 And lz < 800 And ly < -600 And SelectedEnding = "" And (Not I32Exit) Then lx = -999
	If lx < -935 And lz > 520 And lz < 760 And ly < -600 And SelectedEnding = "" Then
		If I32MTF And (Not I32Blown) Then
			I32ExitEnd = "V2"
		ElseIf I32Blown Then
			I32ExitEnd = "V3"
		Else
			I32ExitEnd = "V1"
		EndIf
		I32Exit = True : I32ExitT = 0
		U32SirenStop()
		Select I32ExitEnd
			Case "V2"
				PlaySound_Strict(LoadTempSound("SFX\Ending\GateA\STOPRIGHTTHERE.ogg"))
				IS16Tell("'STOP RIGHT THERE!' Rifles come up all at once. Lights in your eyes.", 5)
			Case "V3"
				I32WindCHN = PlaySound_Strict(LoadTempSound("SFX\Indev\wind.wav"))
				IS16Tell("You climb the rubble into the dust and the cold. Above you, a ragged slot of daylight.", 5)
			Default
				I32WindCHN = PlaySound_Strict(LoadTempSound("SFX\Indev\wind.wav"))
				IS16Tell("Cold air hits you like a wall. Snow. Sky. Nobody.", 5)
		End Select
	EndIf
End Function

;the few seconds between the hatch and the ending screen: you walk out (or are stopped), then the ending
Function U32ExitScene(e.Events)
	Local r.Rooms = e\room, vx#, vz#, p.Particles
	I32ExitT = I32ExitT + FPSfactor
	UnableToMove = True
	Select I32ExitEnd
		Case "V2"
			;stopped dead: rifle lights in your eyes, then a hood
			LightFlash = Min(LightFlash + 0.01 * FPSfactor, 0.5)
			If I32ExitT > 70 * 2.4 Then BlinkTimer = -10 ;the hood
		Default
			;walking out into the white
			TFormVector(-1, 0, 0, r\obj, 0)
			vx = TFormedX() : vz = TFormedZ()
			TranslateEntity(Collider, vx * 0.0035 * FPSfactor / Max(Sqr(vx * vx + vz * vz), 0.001), 0, vz * 0.0035 * FPSfactor / Max(Sqr(vx * vx + vz * vz), 0.001))
			LightFlash = Min(LightFlash + 0.025 * FPSfactor, 3.0)
			BlurTimer = Max(BlurTimer, 70)
			If I32ExitEnd = "V3" And Rand(1, 4) = 1 Then
				p = CreateParticle(EntityX(Camera) + Rnd(-0.6, 0.6), EntityY(Camera) + Rnd(-0.2, 0.4), EntityZ(Camera) + Rnd(-0.6, 0.6), 6, 0.3, -0.01, 80)
			EndIf
	End Select
	If I32ExitT > 70 * 3.2 And SelectedEnding = "" Then
		SelectedEnding = I32ExitEnd
		UnableToMove = False
		GodMode = 0 : NoClip = 0
		KillTimer = -0.1
		DeathMSG = ""
		Kill()
	EndIf
End Function

;drawn over the ending screen (Main.bb, DrawEnding) while it fades in
Function IndevDrawEndingV()
	Local l1$, l2$, l3$, y%
	Select Lower(SelectedEnding)
		Case "v1"
			l1 = "The vault hatch opens onto a mountainside. Wind, snow, a sky you had forgotten."
			l2 = "Nobody is waiting. Nobody follows. You walk downhill until the facility"
			l3 = "is only a scar in the snow behind you."
		Case "v2"
			l1 = "Nine-Tailed Fox were waiting at the hatch. They had been told to expect someone."
			l2 = "Subject D-9341 was returned to the Light Containment Zone within the hour."
			l3 = "Gate V was logged as tested and fully functional."
		Default
			l1 = "The seal charges brought the outer passage down on the response unit."
			l2 = "You climbed out through the dust at the top of the rubble, into the snow."
			l3 = "Gate V no longer exists. Neither, as far as the Foundation knows, do you."
	End Select
	If Lower(Left(SelectedEnding, 1)) <> "v" Then Return
	y = GraphicHeight * 0.64 ;under the logo, above the subtitles
	SetFont Font1
	Color 0, 0, 0
	Text GraphicWidth / 2 + 2, y + 2, l1, True
	Text GraphicWidth / 2 + 2, y + 24 * MenuScale + 2, l2, True
	Text GraphicWidth / 2 + 2, y + 48 * MenuScale + 2, l3, True
	Color 235, 235, 235
	Text GraphicWidth / 2, y, l1, True
	Text GraphicWidth / 2, y + 24 * MenuScale, l2, True
	Text GraphicWidth / 2, y + 48 * MenuScale, l3, True
End Function
