;=====================================================================
; SCP: Containment Breach - Indev stress meter
;
;   A 0-100 stress value with its own HUD bar above the blink meter.
;   Stress builds from what's happening around you (SCP-173 in sight,
;   SCP-106 close, SCP-096 hunting, SCP-718's stare, SCP-895, lost
;   sanity, bad wounds) and drains off when things are quiet.
;
;   The effects are deliberately small and occasional, not constant:
;     40+  a faint heartbeat
;     60+  now and then a short blur, a small tremor, a sharp breath
;     80+  rarely, an intrusive thought; stamina comes back slower
;=====================================================================

Global IndevStress#, IndevStressNext#, IndevStressShown#
Global StressMeterIMG% = 0, StressIcon% = 0

Function IndevStressReset()
	IndevStress = 0 : IndevStressNext = 70*20 : IndevStressShown = 0
End Function

;quick relief (SCP-348 soup, SCP-330 candy, ...)
Function IndevRelieveStress(amount#)
	IndevStress = Max(0, IndevStress - amount)
End Function

Function UpdateIndevStress()
	If KillTimer < 0 Then IndevStress = 0 : Return
	Local dt# = FPSfactor / 70.0
	Local gain# = 0.0, d#

	;SCP-173 in view and close
	If Curr173 <> Null Then
		d = EntityDistance(Collider, Curr173\Collider)
		If d < 8.0 Then
			If EntityInView(Curr173\obj, Camera) And EntityVisible(Curr173\Collider, Collider) Then gain = gain + 5.0 * (1.0 - d / 8.0) + 1.0
		EndIf
	EndIf
	;SCP-106 anywhere near
	If Curr106 <> Null Then
		If Curr106\State <= 0 And (Not Curr106\Idle) And (Not Contained106) Then
			d = EntityDistance(Collider, Curr106\Collider)
			If d < 10.0 Then gain = gain + 6.0 * (1.0 - d / 10.0)
		EndIf
	EndIf
	;SCP-096 screaming / hunting
	If Curr096 <> Null Then
		If Curr096\State >= 1 And Curr096\State <= 4 Then gain = gain + 3.0
	EndIf
	;SCP-718 staring, SCP-895 nearby
	If I718StareStage > 0 Then gain = gain + 1.5 * I718StareStage
	;(CoffinDistance keeps stale values from other rooms, so only count it inside SCP-895's room)
	If PlayerRoom <> Null Then
		If PlayerRoom\RoomTemplate\Name = "coffin" And CoffinDistance < 8.0 Then gain = gain + 3.0 * (1.0 - CoffinDistance / 8.0)
	EndIf
	;the body: bad wounds, heavy bleeding
	If Injuries > 1.5 Then gain = gain + 1.0
	If Bloodloss > 40 Then gain = gain + 1.0

	;the Cognitive Filter Glasses dull all of it a bit
	If IndevCogOn Then gain = gain * 0.6
	;SCP-122: in the night light's room, almost nothing gets under your skin
	Local calm122% = Indev122Calming()
	If calm122 Then gain = gain * 0.15

	;lost sanity keeps a floor under stress until it recovers
	;(tiny dips from a glance at a monitor shouldn't pin the bar; it only counts once it is real)
	Local floorStress# = 0
	If Sanity < -80 Then floorStress = Min(90, (-Sanity - 80) / 8.0)

	If gain > 0 Then
		IndevStress = Min(100, IndevStress + gain * dt)
	Else
		;calming down: faster when crouched and standing still
		Local calm# = 1.2
		If Crouch And CurrSpeed < 0.001 Then calm = 3.0
		If calm122 Then calm = 6.0
		IndevStress = Max(0, IndevStress - calm * dt)
	EndIf
	If calm122 Then floorStress = 0
	IndevStress = Max(IndevStress, floorStress)

	;the bar eases toward the value so it doesn't jitter
	IndevStressShown = IndevStressShown + (IndevStress - IndevStressShown) * Min(1.0, dt * 3.0)

	If IndevStress < 40 Then Return

	;40+: a faint heartbeat that grows with it
	HeartBeatVolume = Max(HeartBeatVolume, (IndevStress - 40.0) / 150.0)
	HeartBeatRate = Max(HeartBeatRate, 75 + IndevStress * 0.5)

	;80+: stamina comes back a little slower
	If IndevStress >= 80 And Stamina < 100 Then Stamina = Max(0, Stamina - FPSfactor * 0.03)

	;occasional small moments, spaced well apart
	IndevStressNext = IndevStressNext - FPSfactor
	If IndevStressNext > 0 Or IndevStress < 60 Then Return
	IndevStressNext = 70 * Rnd(25, 45) * (1.4 - IndevStress / 100.0)

	Select Rand(1, 3)
		Case 1
			BlurTimer = Max(BlurTimer, 70*0.8)
		Case 2
			CameraShake = Max(CameraShake, 0.35)
		Default
			Local ch% = PlaySound_Strict(BreathSFX(0, Rand(1, 3)))
			ChannelVolume(ch, 0.5 * SFXVolume)
	End Select

	If IndevStress >= 80 And Rand(3) = 1 And MsgTimer <= 0 Then
		Select Rand(1, 6)
			Case 1 Msg = "You could swear something moved at the edge of your vision."
			Case 2 Msg = "Your hands won't stop shaking."
			Case 3 Msg = "Was that a footstep behind you?"
			Case 4 Msg = "You realise you've been holding your breath."
			Case 5 Msg = "Keep moving. Don't think about it."
			Default Msg = "The silence feels like it's listening."
		End Select
		MsgTimer = 70*4
	EndIf
End Function

;drawn from DrawHUD, one row above the blink meter, same size and spacing as the other two bars
Function DrawIndevStressBar(x%, width%)
	If StressMeterIMG = 0 Then StressMeterIMG = LoadImageHUDScaled("GFX\stressmeter.png")
	If StressIcon = 0 Then StressIcon = LoadImageHUDScaled("GFX\stressicon.png")

	Local y% = HUDEndY - 135 * HUDScale
	DrawBar(StressMeterIMG, x, y, width, IndevStressShown / 100.0)

	Color 0, 0, 0
	Rect(x - 50 * HUDScale, y, 30 * HUDScale, 30 * HUDScale)
	;a dull red frame when it's high, like the eye irritation warning on the blink icon
	If IndevStress >= 70 Then
		Color 120 + Int(60 * Sin(MilliSecs() / 6.0)), 20, 40
		Rect(x - 50 * HUDScale - 3, y - 3, 30 * HUDScale + 6, 30 * HUDScale + 6)
	EndIf
	Color 255, 255, 255
	Rect(x - 50 * HUDScale - 1, y - 1, 30 * HUDScale + 2, 30 * HUDScale + 2, False)
	DrawImage StressIcon, x - 50 * HUDScale, y
End Function
