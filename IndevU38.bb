;=====================================================================
; SCP: Containment Breach - Indev: the thirty-eighth batch - Corridor L-40, the display hall, the D-block social
;
;   room2b40infhall  the long hallway: walking north you are put back 600 units (two pillar bays - the pattern
;                    repeats exactly), three times, before the doors with the two big windows let you reach them
;   room2b40display  SCP-1148: in the lit half of its chamber, exposure builds (faster while you look at the
;                    window): paranoia, then figures in the reflection, then you are turned to face it and drawn
;                    towards it - reach the glass and you are pulled in. Walk out of the lit half to break it.
;                    SCP-1039: in the display hall it takes one item from your inventory now and then; it turns up
;                    at the doll's feet. Seven pending-classification objects in the cases, each with its own quirk.
;   room2b40party    the holiday social (music SFX\Music\SCP-x1x.ogg): look at the birthday cake too long - dread,
;                    then you eat a slice. SCP-1117-1, the table in the vault, does the same. Either makes you
;                    SCP-1117-3: plates of food turn up when you are tired; your stamina ceiling sinks over time;
;                    an ordinary ration makes you violently ill (the second one stops your heart). SCP-500 cures it.
;   Summaries of scp-wiki.wikidot.com/scp-1039, -1148, -1117 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I38Loops%, I38InHall%, I38PrevZ#
Global I38Mirror#, I38MirrorStage%, I38Eye% = 0, I38EyeT#
Global I38Gaze#, I38CakeCD#, I38Fed#, I38FoodT#, I38Rations%, I38Taken%
Global I38InParty%

Function Indev38Reset(newGame%)
	If newGame Then
		I38Fed = 0 : I38Rations = 0 : I38Taken = 0
	EndIf
	I38Loops = 0 : I38InHall = False : I38PrevZ = -9999 : I38Mirror = 0 : I38MirrorStage = 0 : I38EyeT = 0
	I38Gaze = 0 : I38CakeCD = 0 : I38FoodT = 70 * 90 : I38InParty = False
End Function

;nothing runtime-only in these rooms: everything is baked (the generated FillRoom calls this)
Function IndevU38Dress(r.Rooms)
End Function

Function UpdateIndevU38(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b40infhall" : U38Hall(e)
		Case "room2b40display" : U38Display(e)
		Case "room2b40party" : U38Party(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- the long hallway
Function U38Hall(e.Events)
	Local r.Rooms = e\room, lx#, lz#
	If PlayerRoom <> r Then
		If I38InHall Then I38Loops = 0
		I38InHall = False : I38PrevZ = -9999
		Return
	EndIf
	I38InHall = True
	lx = U37LX(r)
	lz = U37LZ(r)
	If I38Loops < 3 And lz > 380 And lz < 560 And I38PrevZ > -9000 And lz > I38PrevZ And Abs(lx) < 300 Then
		IxPlace(Collider, r, lx, U37LY(r), lz - 600)
		ResetEntity(Collider)
		I38Loops = I38Loops + 1
		LightBlink = 1.4
		lz = lz - 600
		Select I38Loops
			Case 1 : IS16Tell("The doors at the end don't seem any closer. That pillar - didn't you just pass that pillar?", 6)
			Case 2
				IndevStress = Min(100, IndevStress + 8)
				IS16Tell("Same shutter. Same scuff on the floor. The lights hum. The doors are right there, and you are back where you were.", 7)
			Default : IS16Tell("You keep walking. This time the windows in the doors get bigger as you go.", 6)
		End Select
	EndIf
	I38PrevZ = lz
	If IS10Press(r\Objects[U38_INF_ENDDOOR], 2.0) Then
		IS16Tell("Through the two big windows: more hallway. Pillars, shutters, lights. It looks exactly like this side.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- display hall
Function U38Display(e.Events)
	Local r.Rooms = e\room, lx#, lz#, k%, wx#, wz#, dx#, dz#, d#, n%, it.Items, pick%
	If I38Eye <> 0 And I38EyeT > 0 Then
		I38EyeT = I38EyeT - FPSfactor
		If I38EyeT <= 0 Then HideEntity(I38Eye)
	EndIf
	If PlayerRoom <> r Then
		I38Mirror = Max(0, I38Mirror - FPSfactor * 2)
		Return
	EndIf
	lx = U37LX(r)
	lz = U37LZ(r)
	;---------------- SCP-1148
	If lx > -640 And lx < -256 And KillTimer >= 0 Then
		If EntityInView(r\Objects[U38_DSP_WINDOW], Camera) Then
			I38Mirror = I38Mirror + FPSfactor
		Else
			I38Mirror = I38Mirror + FPSfactor * 0.3
		EndIf
	Else
		I38Mirror = Max(0, I38Mirror - FPSfactor * 2)
		If I38Mirror = 0 Then I38MirrorStage = 0
	EndIf
	If I38Mirror > 70 * 25 And I38MirrorStage < 1 Then
		I38MirrorStage = 1
		IndevStress = Min(100, IndevStress + 10)
		IS16Tell("It's just a window. Your reflection, the lit room behind you. You can't see through it. You can't stop looking at it. Something is watching you from behind it.", 8)
	EndIf
	If I38Mirror > 70 * 40 And I38MirrorStage < 2 Then
		I38MirrorStage = 2
		IS16Tell("In the reflection, behind your shoulder: a man in a black hood. You turn. Nobody. In the glass, something with wings, gone when you look at it.", 8)
	EndIf
	If I38MirrorStage >= 2 And I38EyeT <= 0 And Rand(160) = 1 Then
		If I38Eye = 0 Then
			I38Eye = IS10Quad(60, 30, True, False)
			k = LoadTexture_Strict("GFX\map\indev_b36eyes.png", 2)
			If k <> 0 Then
				EntityTexture(I38Eye, k)
				FreeTexture(k)
			EndIf
			EntityFX(I38Eye, 1 + 8)
		EndIf
		IxPlace(I38Eye, r, -636, Rnd(120, 260), Rnd(-240, 240))
		RotateEntity(I38Eye, 0, EntityYaw(r\obj, True) + 90, 0, True)
		ShowEntity(I38Eye)
		I38EyeT = 50
	EndIf
	If I38Mirror > 70 * 55 And lx > -640 And lx < -256 And KillTimer >= 0 Then
		If I38MirrorStage < 3 Then
			I38MirrorStage = 3
			IS16Tell("You need to close the window. Draw a blind. There is no blind. Your feet are already moving. WALK AWAY FROM IT.", 8)
		EndIf
		TFormPoint(-640, 0, lz, r\obj, 0)
		wx = TFormedX() : wz = TFormedZ()
		dx = wx - EntityX(Collider, True) : dz = wz - EntityZ(Collider, True)
		d = Max(0.001, Sqr(dx * dx + dz * dz))
		RotateEntity(Collider, EntityPitch(Collider), CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(Collider), 25.0), 0)
		TranslateEntity(Collider, dx / d * 0.006 * FPSfactor, 0, dz / d * 0.006 * FPSfactor)
		CameraShake = Max(CameraShake, 0.3)
		If lx < -640 + 70 Then
			DeathMSG = "Subject D-9341 was recorded walking up to SCP-1148-1 and pressing both hands to the glass. The footage shows the subject's reflection lean out to meet them. The subject has not been recovered."
			Kill()
		EndIf
	EndIf
	;---------------- SCP-1039: one item at a time, now and then
	If lx > 256 Then
		If e\EventState3 = 0 Then e\EventState3 = 70 * Rnd(30, 60)  ;a grace period the first time in
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rnd(40, 80)
			If WearingHazmat = 0 Then
				For k = 0 To MaxItemAmount - 1
					If Inventory(k) <> Null And Inventory(k) <> SelectedItem Then n = n + 1
				Next
				If n > 0 Then
					pick = Rand(1, n) : n = 0
					For k = 0 To MaxItemAmount - 1
						If Inventory(k) <> Null And Inventory(k) <> SelectedItem Then
							n = n + 1
							If n = pick Then it = Inventory(k) : Exit
						EndIf
					Next
					If it <> Null Then
						DropItem(it, False)
						If it\Picked = False Then
							PositionEntity(it\collider, EntityX(r\Objects[U38_DSP_DROP], True) + Rnd(-0.15, 0.15), EntityY(r\Objects[U38_DSP_DROP], True) + 0.1, EntityZ(r\Objects[U38_DSP_DROP], True) + Rnd(0, 0.15), True)
							ResetEntity(it\collider)
							I38Taken = I38Taken + 1
							IS16Tell("Your pack is lighter. Something is missing - you had it a second ago. On the plinth in the middle of the hall, the doll's cloth belly is lumpy.", 7)
						EndIf
					EndIf
				EndIf
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[U38_DSP_DOLL], 1.6) Then
		IS16Tell("SCP-1039: a cloth doll with a painted ribcage and a clay skull. Its belly bulges. Whatever it took from you is lying at its feet - for now.", 7)
	EndIf
	For k = 0 To 6
		If IS10Press(r\Objects[U38_DSP_CASE0 + k], 1.4) Then U38Case(k)
	Next
End Function

;the seven pending-classification objects: a line each, and a small quirk
Function U38Case(k%)
	Select k
		Case 0
			IndevRelieveStress(4)
			IS16Tell("PENDING 38-01, a music box. It's silent while you look. You turn away - a few notes of a lullaby. You turn back. Silent.", 7)
		Case 1 : IS16Tell("PENDING 38-02, a snow globe of a little station platform. Nobody has shaken it. It's snowing.", 6)
		Case 2 : IS16Tell("PENDING 38-03, a typewriter. The paper reads: 'VISITOR AT CASE 3. VISITOR IS READING THIS.' The keys haven't moved.", 7)
		Case 3 : IS16Tell("PENDING 38-04, a rubber duck in a dry case, dripping. A small puddle under it is labelled 'DO NOT MOP'.", 6)
		Case 4
			IS16Tell("PENDING 38-05, a white ceramic mask. You can feel its warmth through the glass, like a face.", 6)
			IndevStress = Min(100, IndevStress + 3)
		Case 5 : IS16Tell("PENDING 38-06, a teapot. A card says it pours cold tea, always, from any temperature. Someone has added: 'mint'.", 6)
		Default : IS16Tell("PENDING 38-07, a pocket watch. Its second hand sweeps the wrong way round. Your own watch, for a moment, too.", 6)
	End Select
End Function

;--------------------------------------------------------------------------------------------- the party
Function U38Party(e.Events)
	Local r.Rooms = e\room, d#
	If PlayerRoom <> r Then
		I38InParty = False
		I38Gaze = 0
		Return
	EndIf
	I38InParty = True
	ShouldPlay = 26                                           ;SFX\Music\SCP-x1x.ogg
	If I38CakeCD > 0 Then I38CakeCD = I38CakeCD - FPSfactor
	d = EntityDistance(Collider, r\Objects[U38_PTY_CAKE])
	If d < 3.5 And I38CakeCD <= 0 And KillTimer >= 0 And EntityInView(r\Objects[U38_PTY_CAKE], Camera) Then
		I38Gaze = I38Gaze + FPSfactor
		If I38Gaze > 70 * 6 And I38Gaze - FPSfactor <= 70 * 6 Then
			IndevStress = Min(100, IndevStress + 10)
			CameraShake = 1.0
			IS16Tell("A birthday cake. Pink candles, a jam layer, buttercream. Nobody knows who brought it. The longer you look, the more it feels like it's looking back into you. Dread, thick and sweet.", 8)
		EndIf
		If I38Gaze > 70 * 12 Then
			I38Gaze = 0 : I38CakeCD = 70 * 60
			U38Eat("You have a slice of it on a paper plate. You don't remember cutting it. It's the best thing you have ever eaten. You have another.")
		EndIf
	Else
		I38Gaze = Max(0, I38Gaze - FPSfactor * 2)
	EndIf
	If IS10Press(r\Objects[U38_PTY_TABLE], 1.8) Then
		U38Eat("SCP-1117-1: roast meat, warm bread, fruit, dishes you don't know the names of. You only meant to look. The plate you emptied is full again.")
		IS16Give("food1117", r\Objects[U38_PTY_TABLE])
	EndIf
End Function

;eating SCP-1117-2: it heals and fills you - and makes you SCP-1117-3
Function U38Eat(txt$)
	Injuries = Max(0, Injuries - 0.4)
	Stamina = 100
	If I38Fed <= 0 Then
		I38Fed = 1
		I38FoodT = 70 * 120
	Else
		I38Fed = I38Fed + 70 * 60
	EndIf
	IS16Tell(txt, 8)
End Function

;an ordinary ration once SCP-1117 has you (IndevRations.bb): returns True when it was handled here
Function U38Ration%(it.Items)
	If I38Fed <= 0 Then Return False
	I38Rations = I38Rations + 1
	RemoveItem(it)
	SelectedItem = Null
	If I38Rations >= 2 Then
		DeathMSG = "Subject D-9341 collapsed after eating a standard ration. Cause of death: cardiac arrhythmia, with severe depletion of phosphate, magnesium and calcium. Subject had previously been exposed to SCP-1117."
		Kill()
	Else
		Injuries = Injuries + 1.0
		BlurTimer = 70 * 8 : CameraShake = 2.0
		IS16Tell("It tastes of ash and wet cardboard. You're sick on the floor, again and again. Your heart stutters. Nothing tastes right but the food that finds you.", 8)
	EndIf
	Return True
End Function

;SCP-1117-2 as an item
Function IndevUse38(it.Items)
	Select it\itemtemplate\name
		Case "food1117"
			RemoveItem(it)
			SelectedItem = Null
			U38Eat("A plate of food that was never cooked here. Hot, perfect. You feel strong, for a while.")
			Return
	End Select
	SelectedItem = Null
End Function

;SCP-500 (IndevPills.bb)
Function Indev38Cure()
	If I38Fed > 0 Then IS16Tell("The craving lifts. For the first time in days, a ration sounds like food.", 6)
	I38Fed = 0 : I38Rations = 0
End Function

;called from IndevOutdoorFrame (IndevU26.bb): Corridor L-40's haze hides how long it really is
Function U38Frame()
	If I38InHall Then
		CameraFogMode(Camera, 1)
		CameraFogRange(Camera, 0.6, 3.3)
		CameraFogColor(Camera, 22, 22, 24)
		CameraClsColor(Camera, 22, 22, 24)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev38()
	Local cap#
	If I38Fed > 0 And KillTimer >= 0 Then
		I38Fed = I38Fed + FPSfactor
		cap = Max(15, 100 - I38Fed / (70.0 * 10))
		Stamina = Min(Stamina, cap)
		If I38Fed > 70 * 60 * 6 And I38Fed - FPSfactor <= 70 * 60 * 6 Then IS16Tell("You are so tired. Every step costs something. You're hungry - and you know food will turn up. It always does.", 7)
		If I38Fed > 70 * 60 * 20 Then
			DeathMSG = "Subject D-9341 was found asleep against a wall and could not be woken. Cause of death: unexplained exhaustion. Subject had been exposed to SCP-1117."
			Kill()
		EndIf
		I38FoodT = I38FoodT - FPSfactor
		If I38FoodT <= 0 And Stamina < 40 Then
			I38FoodT = 70 * Rnd(90, 150)
			IS16Give("food1117", Collider)
			IS16Tell("You're hungry - and there, by your feet, a plate of food. Steaming. You didn't hear anyone.", 6)
		EndIf
	EndIf
End Function
