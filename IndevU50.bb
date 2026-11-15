;=====================================================================
; SCP: Containment Breach - Indev batch 50: the research complex (rooms by Tools\roomkit\rooms_b50.py, slot table in
; the generated IndevU50Data.bb) - three SCP encounters and five random facility incidents.
;
;   SCP-061 (Research Laboratory 02): a little box that gives orders you can't hear. Within its range it makes you
;           stand still, turn round, or walk towards it. Its switch is by the south door - turn it off first.
;   SCP-162 (Experimental Observation Room, in the pit): the ball of hooks. Get too close and you're caught; move
;           and the hooks dig in (blood, injuries); stand still a few seconds and they let go.
;   SCP-020 (Small Specimen Storage, north-west corner): the unseen mold. Breathe near it without a gas mask or a
;           hazmat suit and you start to cough, then it starts to hurt. Leave and it slowly clears.
;
; Random incidents (IndevB50Frame, every few minutes, anywhere ordinary): a power fluctuation, a ventilation
; failure, a burst pipe, a PA announcement, a door that opens or shuts by itself. One at a time, never in the
; special areas, cheap (nothing is created except one puddle decal).
;=====================================================================

Global I61On% = True, I61Next#, I61Cmd%, I61T#, I61Hint%
Global I162Hooked%, I162Still#, I162Warn%
Global I020Exp#, I020Msg%
Global I50Timer# = -1, I50Vent#

Function Indev50Reset(newGame%)
	I61On = True : I61Next = 0 : I61Cmd = 0 : I61T = 0 : I61Hint = 0
	I162Hooked = False : I162Still = 0 : I162Warn = 0
	I020Exp = 0 : I020Msg = 0
	I50Timer = 70 * 60 * Rnd(4, 7) : I50Vent = 0
End Function

;SCP-162: a dark core and a few dozen barbed hooks sticking out every way (built once per room, from primitives)
Function I162Build%(p%)
	Local t% = LoadTexture_Strict("GFX\map\dirtymetal.jpg", 1)
	Local ball% = CreateSphere(8)
	ScaleMesh(ball, 0.22, 0.22, 0.22)
	EntityTexture(ball, t)
	EntityColor(ball, 70, 62, 58)
	Local k%, h%
	For k = 1 To 46
		h = CreateCone(4)
		ScaleMesh(h, 0.012, 0.16, 0.012)
		PositionMesh(h, 0, 0.3, 0)
		RotateMesh(h, Rnd(-180, 180), Rnd(-180, 180), Rnd(-180, 180))
		PaintMesh(h, GetEntityBrush(ball))
		AddMesh(h, ball)
		FreeEntity(h)
	Next
	FreeTexture(t)
	PositionEntity(ball, EntityX(p, True), EntityY(p, True) + 0.45, EntityZ(p, True), True)
	EntityParent(ball, p)
	Return ball
End Function

Function IndevU50Dress(r.Rooms)
	If r\RoomTemplate\Name = "room2b50observe" Then r\Objects[U50_OBS_SLOTS] = I162Build(r\Objects[U50_OBS_HOOKS])
End Function

Function UpdateIndevU50(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then
		If r\RoomTemplate\Name = "room2b50observe" Then I162Hooked = False
		Return
	EndIf
	Select r\RoomTemplate\Name
		Case "room2b50lab02" : U50Lab(e, r)
		Case "room2b50observe" : U50Hooks(e, r)
		Case "room2b50chem"
			If e\EventState = 0 Then
				e\EventState = 1
				IS16Tell("Chemical storage. A sharp, clean smell. One of the overhead lines has been patched with tape.", 5)
			EndIf
		Case "room2b50office"
			If e\EventState = 0 Then
				e\EventState = 1
				IS16Tell("A researchers' office. Three desks, three cold cups of coffee.", 4)
			EndIf
		Case "room2b50specimen"
			If e\EventState = 0 Then
				e\EventState = 1
				IS16Tell("Specimen storage. The far corner looks damp, though nothing's dripping.", 5)
			EndIf
			;SCP-020: breathing near the corner
			Local d# = EntityDistance(Collider, r\Objects[U50_SPC_MOLD])
			If d < 3.2 And WearingGasMask = 0 And WearingHazmat = 0 Then
				I020Exp = I020Exp + FPSfactor * (3.2 - d)
			EndIf
	End Select
End Function

;---------------------------------------------------------------- SCP-061
Function U50Lab(e.Events, r.Rooms)
	Local dev% = r\Objects[U50_L02_DEV61], sw% = r\Objects[U50_L02_SW61]
	If IS10Press(sw, 1.2) Then
		I61On = Not I61On
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If I61On Then
			IS16Tell("You flip the switch. A small green light comes on across the room.", 4)
		Else
			IS16Tell("You flip the switch labelled 061. The faint pressure in your ears is gone.", 4)
		EndIf
	EndIf
	If Not I61On Then Return
	Local d# = EntityDistance(Collider, dev)
	If I61Hint = 0 And d < 7 Then
		I61Hint = 1
		IS16Tell("A faint pressure in your ears, like the moment before a sneeze. There's a small grey box on the far bench.", 5)
	EndIf
	If KillTimer < 0 Then Return
	If I61Cmd > 0 Then
		I61T = I61T - FPSfactor
		Select I61Cmd
			Case 1 ;stand still
				CurrSpeed = 0
				PositionEntity(Collider, EntityX(Collider), EntityY(Collider), EntityZ(Collider))
			Case 2 ;turn around
				TurnEntity(Collider, 0, 3.0 * FPSfactor, 0)
			Case 3 ;come here
				Local dx# = EntityX(dev, True) - EntityX(Collider, True), dz# = EntityZ(dev, True) - EntityZ(Collider, True)
				Local l# = Sqr(dx * dx + dz * dz)
				If l > 0.9 Then TranslateEntity(Collider, dx / l * 0.012 * FPSfactor, 0, dz / l * 0.012 * FPSfactor, True)
				RotateEntity(Collider, 0, VectorYaw(dx, 0, dz), 0, True)
		End Select
		If I61T <= 0 Then I61Cmd = 0
		Return
	EndIf
	If d < 5.5 Then
		I61Next = I61Next - FPSfactor
		If I61Next <= 0 Then
			I61Next = 70 * Rnd(5, 9)
			I61Cmd = Rand(1, 3)
			Select I61Cmd
				Case 1 : I61T = 70 * 3 : IS16Tell("You stop. You don't decide to - you just stop, and wait.", 3)
				Case 2 : I61T = 60 : IS16Tell("You turn round to face the wall. It seems important.", 3)
				Default : I61T = 70 * 2.5 : IS16Tell("You find yourself walking towards the grey box.", 3)
			End Select
			IndevStress = Min(100, IndevStress + 4)
		EndIf
	EndIf
End Function

;---------------------------------------------------------------- SCP-162
Function U50Hooks(e.Events, r.Rooms)
	Local ball% = r\Objects[U50_OBS_SLOTS]
	If ball = 0 Then Return
	TurnEntity(ball, 0, 0.05 * FPSfactor, 0)
	If e\EventState = 0 Then
		e\EventState = 1
		IS16Tell("An observation gallery over a sunken test chamber. Down in the pit sits a dark, bristling ball.", 5)
	EndIf
	If KillTimer < 0 Then Return
	Local d# = EntityDistance(Collider, ball)
	If Not I162Hooked Then
		If d < 0.95 Then
			I162Hooked = True : I162Still = 0 : I162Warn = 0
			Injuries = Injuries + 0.15
			PlaySound_Strict(LoadTempSound("SFX\Character\D9341\BloodDrip" + Rand(0, 3) + ".ogg"))
			IS16Tell("Hooks snag your clothes, your arm, your leg. The ball rolls with you. DON'T PULL.", 5)
		EndIf
		Return
	EndIf
	;caught: moving drags the hooks in, standing still lets them loosen
	If CurrSpeed > 0.004 Then
		I162Still = 0
		Injuries = Injuries + 0.0025 * FPSfactor
		Bloodloss = Bloodloss + 0.04 * FPSfactor
		If I162Warn = 0 Then
			I162Warn = 1
			IS16Tell("The barbs dig in deeper with every step. Stand still.", 3)
		EndIf
		;it comes with you
		PointEntity(ball, Collider)
		MoveEntity(ball, 0, 0, Min(0.006 * FPSfactor, Max(0, d - 0.6)))
	Else
		I162Still = I162Still + FPSfactor
		If I162Still > 70 * 4 Then
			I162Hooked = False
			IS16Tell("One by one the hooks slacken and slide out. You step back, very slowly.", 5)
			;let you get clear before it can catch you again
			TFormVector(0, 0, -0.5, Collider, 0)
			TranslateEntity(Collider, TFormedX(), 0, TFormedZ(), True)
		EndIf
	EndIf
	If Injuries > 4 And KillTimer >= 0 Then
		DeathMSG = "Subject D-9341 was found in Test Chamber B entangled in SCP-162. Cause of death: blood loss from several hundred lacerations. He did not stop pulling."
		Kill()
	EndIf
End Function

;---------------------------------------------------------------- every frame (Main.bb): SCP-020 and the incidents
Function IndevB50Frame()
	;SCP-020 exposure: coughing, then harm; clears slowly once you're away from it (UpdateIndevU50 adds to it)
	If I020Exp > 0 Then
		I020Exp = Max(0, I020Exp - FPSfactor * 0.6)
		If I020Exp > 70 * 4 And I020Msg = 0 Then
			I020Msg = 1 : IS16Tell("Your throat itches. You cough, and cough again.", 4)
		ElseIf I020Exp > 70 * 10 And I020Msg = 1 Then
			I020Msg = 2 : IS16Tell("Every breath feels furry. Something is growing in there. Get out, find a mask.", 5)
		EndIf
		If I020Exp > 70 * 10 Then
			Injuries = Injuries + 0.0008 * FPSfactor
			BlurTimer = Max(BlurTimer, 200)
			Stamina = Min(Stamina, 50)
		EndIf
		If I020Exp < 70 * 2 Then I020Msg = 0
	EndIf
	If I50Vent > 0 Then
		I50Vent = I50Vent - FPSfactor
		Stamina = Max(0, Stamina - 0.03 * FPSfactor)
		If I50Vent <= 0 Then IS16Tell("Somewhere above, a fan coughs back to life. The air starts to move again.", 4)
	EndIf
	;the incidents
	If I50Timer < 0 Then I50Timer = 70 * 60 * Rnd(4, 7)
	If IndevTestOn And GetCLIInt("testinc", 0) > 0 And I50Timer > 70 Then I50Timer = 70
	If KillTimer < 0 Or PlayerRoom = Null Or B87In Then Return
	I50Timer = I50Timer - FPSfactor
	If I50Timer > 0 Then Return
	I50Timer = 70 * 60 * Rnd(4, 8)
	Local which% = Rand(1, 5)
	Select PlayerRoom\RoomTemplate\Name
		Case "pocketdimension", "dimension1499", "gatea", "exit1", "173", "start", "room860", "room2scp087b"
			Return
	End Select
	If IndevTestOn And GetCLIInt("testinc", 0) > 0 Then which = GetCLIInt("testinc", 0) : IndevTestLog("INCIDENT " + which)
	Select which
		Case 1 ;power fluctuation
			LightBlink = Rnd(3, 6)
			PlaySound_Strict(LoadTempSound("SFX\Indev\buzzer.wav"))
			IS16Tell("The lights stutter and die for a moment. Somewhere a generator labours, then catches.", 5)
		Case 2 ;ventilation failure
			I50Vent = 70 * 45
			PlaySound_Strict(LoadTempSound("SFX\Room\Intro\173Vent.ogg"))
			IS16Tell("The ventilation stops with a clank. The air goes still and warm, and breathing takes more effort.", 5)
		Case 3 ;burst pipe
			Local de.Decals = CreateDecal(0, EntityX(Collider) + Rnd(-0.8, 0.8), EntityY(Collider) - 0.3, EntityZ(Collider) + Rnd(-0.8, 0.8), 90, Rand(360), 0)
			de\Size = Rnd(0.5, 0.8) : ScaleSprite(de\obj, de\Size, de\Size)
			EntityColor(de\obj, 90, 110, 120) : EntityAlpha(de\obj, 0.6)
			PlaySound_Strict(LoadTempSound("SFX\Room\Intro\173Vent.ogg"))
			IS16Tell("A pipe bursts somewhere overhead with a bang and a hiss. Water spatters down near you.", 5)
		Case 4 ;PA announcement
			PlaySound_Strict(LoadTempSound("SFX\Indev\buzzer.wav"))
			Select Rand(1, 5)
				Case 1 : IS16Tell("PA: " + Chr(34) + "Research staff are reminded that all incidents must be logged on the weekly summary." + Chr(34), 6)
				Case 2 : IS16Tell("PA: " + Chr(34) + "Maintenance to Chemical Storage. Maintenance to Chemical Storage." + Chr(34), 5)
				Case 3 : IS16Tell("PA: " + Chr(34) + "Will the duty researcher for Test Chamber B report to the observation gallery." + Chr(34), 6)
				Case 4 : IS16Tell("PA: " + Chr(34) + "This is a test of the public address system. This is only a test." + Chr(34), 5)
				Default : IS16Tell("PA: static, then a voice, very calm: " + Chr(34) + "...do not use the stairs in the..." + Chr(34) + " - and nothing.", 6)
			End Select
		Default ;a door that opens or shuts by itself
			Local d.Doors, best.Doors, bd# = 6.0, dd#
			For d = Each Doors
				If d\KeyCard = 0 And d\Code = "" And (Not d\Locked) And d\obj <> 0 And d\buttons[0] <> 0 Then
					dd = EntityDistance(d\frameobj, Collider)
					If dd < bd And dd > 1.5 Then bd = dd : best = d
				EndIf
			Next
			If best <> Null Then
				UseDoor(best, False, True)
				IS16Tell("Behind you a door moves on its own - a hiss of hydraulics, then nothing. Nobody there.", 5)
			Else
				LightBlink = Rnd(1, 2)
			EndIf
	End Select
End Function
