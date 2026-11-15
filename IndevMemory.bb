;=====================================================================
; SCP: Containment Breach - Indev memory meter: the Class-D has Alzheimer's disease
;
;   D-9341 came to the Foundation with Alzheimer's disease. A 0-100 value with its own HUD bar (a lavender bar
;   with a brain icon, one row above the stress meter), read as the 7 stages of the disease:
;
;     Stage 1   0-14  no impairment          nothing you can notice yet
;     Stage 2  15-29  very mild decline      forgetting a word, where you put something
;     Stage 3  30-44  mild decline           getting lost in familiar places, forgetting new names, losing focus
;     Stage 4  45-59  moderate decline       forgetting recent events, asking the same thing twice, numbers and
;                                            step-by-step tasks get hard (keypad digits swim), denial
;     Stage 5  60-74  moderately severe      confused about where and when you are; items misplaced in the
;                                            inventory, in places that make no sense
;     Stage 6  75-89  severe                 delusions (something was stolen), anxiety and mood swings, wandering,
;                                            not recognising people
;     Stage 7  90-100 very severe            the body forgets too: stamina is capped and drains faster, stumbles
;
;   It starts at 10 and rises slowly - about a point every 50 seconds, twice as fast under heavy stress (70+).
;   Effects are small and spaced minutes apart; the stage is announced when it changes.
;   Preserved skills: while you read a document the decline pauses and the mind steadies (reading is one of
;   the skills the disease takes last). Medicine: an ordinary pill slows the decline for five minutes; SCP-500
;   cures it - the bar drops to zero and stops rising.
;=====================================================================

Global IndevMemory#, IndevMemoryShown#, IndevMemoryNext#, IndevMemoryCured%, IndevMemoryStage%, IndevMemorySlow#
Global IndevMemoryLast$, IndevMemoryRead%
Global MemoryMeterIMG% = 0, MemoryIcon% = 0

Function IndevMemoryReset()
	IndevMemory = 10 : IndevMemoryShown = 10 : IndevMemoryNext = 70 * 60 : IndevMemoryCured = False
	IndevMemoryStage = 1 : IndevMemorySlow = 0 : IndevMemoryLast = "" : IndevMemoryRead = False
End Function

;SCP-500: called from the pill's use code in Main.bb
Function IndevMemoryCure()
	IndevMemory = 0 : IndevMemoryShown = 0 : IndevMemoryCured = True : IndevMemoryStage = 1
End Function

;an ordinary pill: slows the decline for five minutes (Main.bb, Case "pill")
Function IndevMemoryMedicine()
	IndevMemorySlow = 70 * 300
End Function

Function IndevMemoryStageOf%(v#)
	If v < 15 Then Return 1
	If v < 30 Then Return 2
	If v < 45 Then Return 3
	If v < 60 Then Return 4
	If v < 75 Then Return 5
	If v < 90 Then Return 6
	Return 7
End Function

Function IndevMemoryStageName$(s%)
	Select s
		Case 1 : Return "Stage 1: no impairment"
		Case 2 : Return "Stage 2: very mild cognitive decline"
		Case 3 : Return "Stage 3: mild cognitive decline"
		Case 4 : Return "Stage 4: moderate cognitive decline"
		Case 5 : Return "Stage 5: moderately severe cognitive decline"
		Case 6 : Return "Stage 6: severe cognitive decline"
	End Select
	Return "Stage 7: very severe cognitive decline"
End Function

Function UpdateIndevMemory()
	Local dt# = FPSfactor / 70.0, rate#, st%, reading%
	If KillTimer < 0 Then Return

	;preserved skills: reading a document holds the decline still
	reading = False
	If SelectedItem <> Null Then
		If SelectedItem\itemtemplate\group = "paper" Then reading = True
	EndIf
	If reading And (Not IndevMemoryRead) And IndevMemory >= 30 And MsgTimer <= 0 Then
		IndevMemoryTell("You can still read. The words hold still, and for a while so do you.")
	EndIf
	IndevMemoryRead = reading

	If (Not IndevMemoryCured) And (Not reading) Then
		rate = 0.02
		If IndevStress >= 70 Then rate = rate * 2
		If IndevMemorySlow > 0 Then
			rate = rate * 0.25
			IndevMemorySlow = IndevMemorySlow - FPSfactor
		EndIf
		IndevMemory = Min(100, IndevMemory + dt * rate)
	EndIf
	IndevMemoryShown = IndevMemoryShown + (IndevMemory - IndevMemoryShown) * Min(1.0, dt * 3.0)

	;the stage, announced when it changes
	st = IndevMemoryStageOf(IndevMemory)
	If st <> IndevMemoryStage Then
		IndevMemoryStage = st
		If st > 1 Then IndevMemoryTell("Alzheimer's - " + IndevMemoryStageName(st) + ".")
	EndIf

	;stage 7: the body forgets too - stamina is capped at 50 and drains faster
	If st >= 7 Then
		If Stamina > 50 Then Stamina = 50
		StaminaEffect = Max(StaminaEffect, 1.5)
		StaminaEffectTimer = Max(StaminaEffectTimer, 0.5)
	EndIf
	If st < 2 Then Return

	IndevMemoryNext = IndevMemoryNext - FPSfactor
	If IndevMemoryNext > 0 Then Return
	;every 3-4 minutes at stage 2, about every 70 s at stage 7
	IndevMemoryNext = 70 * Rnd(150, 210) * (1.3 - IndevMemory / 100.0)
	If reading Then Return
	IndevMemoryEffect(Rand(2, st))
End Function

;one symptom of the given stage (the caller picks this stage or an earlier one)
Function IndevMemoryEffect(s%)
	Local a%, b%, it.Items, n.NPCs, near%
	Select s
		Case 2
			Select Rand(1, 3)
				Case 1 : IndevMemoryTell("There's a word for that thing on the wall. It's... it's gone.")
				Case 2 : IndevMemoryTell("You pat your pockets. Where did you put it? Oh. There.")
				Default : IndevMemoryTell("You stop. What were you doing just now?")
			End Select
		Case 3
			BlurTimer = Max(BlurTimer, 70)
			Select Rand(1, 3)
				Case 1 : IndevMemoryTell("You've walked this corridor before. Haven't you? Which way was out?")
				Case 2 : IndevMemoryTell("Someone told you their name a few minutes ago. It's gone.")
				Default : IndevMemoryTell("You can't keep your mind on the task. What was the task?")
			End Select
		Case 4
			;asking the same thing twice: the last thought comes back, word for word
			If IndevMemoryLast <> "" And Rand(2) = 1 Then
				IndevMemoryTell(IndevMemoryLast)
			Else
				Select Rand(1, 3)
					Case 1 : IndevMemoryTell("The numbers on the keypad swim. Was it 1-4 or 4-1? Was it even a 4?")
					Case 2 : IndevMemoryTell("What happened in the last room? You were just there.")
					Default : IndevMemoryTell("You're fine. You're fine. Nothing is wrong with you.")
				End Select
			EndIf
		Case 5
			;items misplaced, in places that make no sense
			a = Rand(0, MaxItemAmount - 1)
			b = Rand(0, MaxItemAmount - 1)
			If a <> b And (Inventory(a) <> Null Or Inventory(b) <> Null) And Rand(2) = 1 Then
				it = Inventory(a)
				Inventory(a) = Inventory(b)
				Inventory(b) = it
				IndevMemoryTell("You were sure you put that somewhere else.")
			Else
				BlurTimer = Max(BlurTimer, 70 * 2)
				Select Rand(1, 3)
					Case 1 : IndevMemoryTell("Where is this? How did you get here?")
					Case 2 : IndevMemoryTell("What day is it? It feels like Tuesday. It's felt like Tuesday for a long time.")
					Default : IndevMemoryTell("Your number. You know your number. D-9... D-9-something.")
				End Select
			EndIf
		Case 6
			Select Rand(1, 4)
				Case 1
					IndevMemoryTell("Someone has taken your things. Someone has been in your pockets. ...No. They're all there.")
				Case 2
					IndevStress = Min(100, IndevStress + 15)
					IndevMemoryTell("A wave of fear comes from nowhere, and then anger, and then nothing.")
				Case 3
					;wandering: the body turns while the mind is elsewhere
					RotateEntity(Collider, 0, EntityYaw(Collider) + Rnd(-60, 60), 0)
					IndevMemoryTell("Where were you going? You were sure, a moment ago.")
				Default
					near = False
					For n = Each NPCs
						If EntityDistance(n\Collider, Collider) < 4.0 Then
							near = True
							Exit
						EndIf
					Next
					If near Then
						IndevMemoryTell("That face. You know that face. Don't you?")
					Else
						IndevMemoryTell("You call out a name. You don't know whose it is.")
					EndIf
			End Select
		Default
			;stage 7: a stumble
			CameraShake = Max(CameraShake, 1.0)
			CurrSpeed = 0
			IndevMemoryTell("Your legs forget the next step. You catch yourself on the wall.")
	End Select
End Function

Function IndevMemoryTell(txt$)
	Msg = txt
	MsgTimer = 70 * 5
	IndevMemoryLast = txt
End Function

;drawn from DrawHUD, one row above the stress meter, the same size and spacing as the other bars
Function DrawIndevMemoryBar(x%, width%)
	If MemoryMeterIMG = 0 Then MemoryMeterIMG = LoadImageHUDScaled("GFX\memorymeter.png")
	If MemoryIcon = 0 Then MemoryIcon = LoadImageHUDScaled("GFX\memoryicon.png")

	Local y% = HUDEndY - 175 * HUDScale
	DrawBar(MemoryMeterIMG, x, y, width, IndevMemoryShown / 100.0)

	Color 0, 0, 0
	Rect(x - 50 * HUDScale, y, 30 * HUDScale, 30 * HUDScale)
	If IndevMemoryStage >= 5 Then
		Color 120 + Int(50 * Sin(MilliSecs() / 8.0)), 80, 170
		Rect(x - 50 * HUDScale - 3, y - 3, 30 * HUDScale + 6, 30 * HUDScale + 6)
	EndIf
	Color 255, 255, 255
	Rect(x - 50 * HUDScale - 1, y - 1, 30 * HUDScale + 2, 30 * HUDScale + 2, False)
	DrawImage MemoryIcon, x - 50 * HUDScale, y
	;the stage number, small, just after the bar
	Color 190, 170, 230
	Text(x + width + 8 * HUDScale, y + 8 * HUDScale, IndevMemoryStage)
	Color 255, 255, 255
End Function
