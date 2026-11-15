;=====================================================================
; SCP: Containment Breach - Indev condition meters
;
;   A compact stack of slim meters on the right edge of the screen, above
;   the armour bar (so nothing overlaps the blink/stamina/stress bars on
;   the left or the armour bar in the corner):
;     Health         overall condition (injuries + blood loss)
;     Bleeding       injury severity
;     Radiation      accumulated exposure (fades slowly)
;     Geiger         radiation detected right now (flickers, clicks)
;     Infection      SCP-008, SCP-214/217 viruses, SCP-718 blisters
;     Cognitohazard  SCP-718's stare, the SCP-096 photo, SCP-895, lost sanity
;     Memetic        SCP-993 / SCP-719 broadcasts, SCP-738, SCP-513, SCP-990, SCP-693
;   Health is always shown; the others only appear while they read
;   something (and linger a few seconds), so the HUD stays quiet.
;   Console: "meters" toggles showing every meter all the time.
;   The stack hides while a held item or SCP-202 is drawn in that corner.
;=====================================================================

Const IMETERS% = 7
Global IMeterVal#[IMETERS], IMeterShown#[IMETERS], IMeterHold#[IMETERS], IMeterIcon%[IMETERS]
Global IMeterAll% = False
Global IndevRadDose#, IndevGeigerRate#

Function IndevMetersReset()
	Local i%
	For i = 0 To IMETERS - 1
		IMeterVal[i] = 0 : IMeterShown[i] = 0 : IMeterHold[i] = 0
	Next
	IndevRadDose = 0 : IndevGeigerRate = 0
End Function

;called from IHzIrradiate: raw = what the detector sees, absorbed = what got through the protection
Function IndevMeterRadiation(raw#, absorbed#)
	IndevGeigerRate = Max(IndevGeigerRate, raw)
	IndevRadDose = Min(100, IndevRadDose + absorbed * FPSfactor / 70.0 * 400.0)
End Function

Function IMClamp#(v#)
	Return Max(0.0, Min(1.0, v))
End Function

Function UpdateIndevMeters()
	Local dt# = FPSfactor / 70.0, v#

	;0 health
	IMeterVal[0] = IMClamp(1.0 - Max(Bloodloss / 100.0, Injuries / 5.0))
	;1 bleeding / injury severity
	IMeterVal[1] = IMClamp(Max(Injuries / 3.0, Bloodloss / 100.0))
	;2 radiation dose: fades slowly once you're out of it
	If KillTimer < 0 Then IndevRadDose = 0
	IndevRadDose = Max(0, IndevRadDose - dt * 0.15)
	IMeterVal[2] = IMClamp(IndevRadDose / 100.0)
	;3 geiger: live reading with a little needle jitter
	If IndevGeigerRate > 0.00005 Then
		IMeterVal[3] = IMClamp(Sqr(IndevGeigerRate / 0.02) + Rnd(-0.06, 0.06))
	Else
		IMeterVal[3] = 0
	EndIf
	IndevGeigerRate = IndevGeigerRate * Max(0, 1.0 - dt * 4.0)
	;4 infection
	v = Infect / 100.0
	v = Max(v, Virus214Stage / 6.0)
	v = Max(v, Virus217Stage / 6.0)
	If I718Blister > 0 Then v = Max(v, 0.5)
	If I718Host Then v = 1.0
	IMeterVal[4] = IMClamp(v)
	;5 cognitohazard
	v = I718Stare / 40.0
	If Indev096PhotoTimer > 0 Then v = Max(v, 0.85)
	If Sanity < -50 Then v = Max(v, (-Sanity - 50) / 800.0)
	If PlayerRoom <> Null Then
		If PlayerRoom\RoomTemplate\Name = "coffin" And CoffinDistance < 8.0 Then v = Max(v, 1.0 - CoffinDistance / 8.0)
	EndIf
	If IndevCogOn Then v = v * 0.6
	IMeterVal[5] = IMClamp(v)
	;6 memetic
	v = 0
	If I993TV <> 0 And PlayerRoom <> Null And PlayerRoom = I993Room Then
		If I993State > 0 Then
			v = 1.0
		ElseIf (Not I993Off) Then
			v = 0.25
		EndIf
	EndIf
	If I719TV <> 0 And I719On And (Not I719Dead) And PlayerRoom <> Null And PlayerRoom = I719Room Then v = Max(v, 0.45)
	If I738State > 0 Then v = Max(v, 0.6)
	If Indev513Active Then v = Max(v, 0.7)
	If Indev990State > 0 Then v = Max(v, 0.8)
	If I113Stage > 0 Then v = Max(v, 0.3 + 0.2 * I113Stage)
	If Doll693Stage() = 1 Then v = Max(v, 0.2 * Doll693Hold())
	If Doll693Stage() = 2 Then v = Max(v, 0.9 * Doll693Hold())
	IMeterVal[6] = IMClamp(v + Rnd(-0.03, 0.03) * (v > 0))

	Local i%
	For i = 0 To IMETERS - 1
		If IMeterVal[i] > 0.01 Then IMeterHold[i] = 70 * 4 Else IMeterHold[i] = Max(0, IMeterHold[i] - FPSfactor)
		IMeterShown[i] = IMeterShown[i] + (IMeterVal[i] - IMeterShown[i]) * Min(1.0, dt * 5.0)
	Next
End Function

;drawn from DrawHUD
Function DrawIndevMeters()
	If SelectedItem <> Null Or I202Open > 0 Then Return
	If IMeterIcon[0] = 0 Then
		IMeterIcon[0] = LoadImageHUDScaled("GFX\meter_health.png")
		IMeterIcon[1] = LoadImageHUDScaled("GFX\meter_bleeding.png")
		IMeterIcon[2] = LoadImageHUDScaled("GFX\meter_radiation.png")
		IMeterIcon[3] = LoadImageHUDScaled("GFX\meter_geiger.png")
		IMeterIcon[4] = LoadImageHUDScaled("GFX\meter_infection.png")
		IMeterIcon[5] = LoadImageHUDScaled("GFX\meter_cognito.png")
		IMeterIcon[6] = LoadImageHUDScaled("GFX\meter_memetic.png")
	EndIf

	Local barW% = 140 * HUDScale, barH% = 8 * HUDScale, rowStep% = 22 * HUDScale
	Local barX% = HUDEndX - 20 * HUDScale - barW
	Local iconX% = barX - 24 * HUDScale
	;first row sits above the armour row (HUDEndY-55)
	Local y% = HUDEndY - 90 * HUDScale
	Local i%, f#, segs%, s%, segW#

	For i = 0 To IMETERS - 1
		If i = 0 Or IMeterAll Or IMeterHold[i] > 0 Or IMeterShown[i] > 0.01 Then
			f = IMClamp(IMeterShown[i])
			;frame
			Color 0, 0, 0
			Rect(barX - 2, y + 4 * HUDScale - 2, barW + 4, barH + 4)
			Color 150, 150, 150
			Rect(barX - 2, y + 4 * HUDScale - 2, barW + 4, barH + 4, False)
			;segmented fill, like the stock bars
			segs = 20 : segW = Float(barW) / segs
			Select i
				Case 0 ;health: green -> red as it drops
					Color 200 - 150 * f, 60 + 150 * f, 50
				Case 1 Color 170, 20, 20
				Case 2 Color 170, 200, 40
				Case 3 Color 230, 200, 40
				Case 4 Color 80, 170, 70
				Case 5 Color 150, 80, 200
				Default Color 60, 170, 200
			End Select
			If i = 0 And f < 0.25 And (MilliSecs() Mod 700) < 350 Then Color 230, 30, 30
			For s = 0 To Int(f * segs + 0.5) - 1
				Rect(barX + s * segW + 1, y + 4 * HUDScale, Max(1, segW - 2), barH)
			Next
			;icon
			Color 0, 0, 0
			Rect(iconX, y, 16 * HUDScale, 16 * HUDScale)
			Color 255, 255, 255
			Rect(iconX - 1, y - 1, 16 * HUDScale + 2, 16 * HUDScale + 2, False)
			DrawImage IMeterIcon[i], iconX, y
			y = y - rowStep
		EndIf
	Next
	Color 255, 255, 255
End Function
