;=====================================================================
; SCP: Containment Breach - Indev armour meter
;
;   A HUD bar in the bottom-right corner, mirroring the stamina bar on
;   the left (same size and row), shown only while armour is worn:
;     MJOLNIR Type 1   a recharging shield - deflecting a bullet or soaking
;                      up an injury drains it, it refills after a few
;                      seconds without being hurt, and the armour protects
;                      less as it runs low
;     heavy vest 70 / vest 40 / hazmat suit 25   (fixed protection)
;   It hides while a held item (radio, navigator, SCP-202...) is drawn in
;   that corner, so the two never overlap.
;=====================================================================

Global IndevArmor# = 100, IndevArmorMax#, IndevArmorShown#, IndevArmorRegenT#
Global ArmorMeterIMG% = 0, ArmorIcon% = 0

Function IndevArmorReset()
	IndevArmor = 100 : IndevArmorMax = 0 : IndevArmorShown = 0 : IndevArmorRegenT = 0
End Function

;how much of the MJOLNIR's protection is left (0..1)
Function IndevMjShieldFrac#()
	Return Max(0, Min(1, IndevArmor / 100.0))
End Function

;the shield took a hit: drain it and restart the recharge delay
Function IndevArmorHit(amount#)
	IndevArmor = Max(0, IndevArmor - amount)
	IndevArmorRegenT = 70*4
End Function

Function UpdateIndevArmor()
	If IndevMjolnirOn Then
		IndevArmorMax = 100
		If IndevArmorRegenT > 0 Then
			IndevArmorRegenT = IndevArmorRegenT - FPSfactor
		ElseIf IndevArmor < 100 Then
			IndevArmor = Min(100, IndevArmor + FPSfactor / 70.0 * 12.0)
			If IndevArmor >= 100 And MsgTimer <= 0 Then Msg = "SHIELDS RECHARGED." : MsgTimer = 70*2
		EndIf
	Else
		If WearingVest = 2 Then
			IndevArmorMax = 70
		ElseIf WearingVest = 1 Then
			IndevArmorMax = 40
		ElseIf WearingHazmat > 0 Then
			IndevArmorMax = 25
		Else
			IndevArmorMax = 0
		EndIf
		IndevArmor = IndevArmorMax
	EndIf
	IndevArmorShown = IndevArmorShown + (IndevArmor - IndevArmorShown) * Min(1.0, FPSfactor / 70.0 * 6.0)
End Function

;drawn from DrawHUD. Bottom-right, on the same row as the stamina bar, icon box on the outer side
Function DrawIndevArmorBar(width%)
	If IndevArmorMax <= 0 Then Return
	If SelectedItem <> Null Or I202Open > 0 Then Return      ;that corner is in use

	If ArmorMeterIMG = 0 Then ArmorMeterIMG = LoadImageHUDScaled("GFX\armormeter.png")
	If ArmorIcon = 0 Then ArmorIcon = LoadImageHUDScaled("GFX\armoricon.png")

	Local iconX% = HUDEndX - 50 * HUDScale
	Local x% = iconX - 30 * HUDScale - width
	Local y% = HUDEndY - 55 * HUDScale

	DrawBar(ArmorMeterIMG, x, y, width, IndevArmorShown / 100.0)

	Color 0, 0, 0
	Rect(iconX, y, 30 * HUDScale, 30 * HUDScale)
	If IndevMjolnirOn And IndevArmor < 25 Then
		Color 120 + Int(60 * Sin(MilliSecs() / 4.0)), 20, 30
		Rect(iconX - 3, y - 3, 30 * HUDScale + 6, 30 * HUDScale + 6)
	EndIf
	Color 255, 255, 255
	Rect(iconX - 1, y - 1, 30 * HUDScale + 2, 30 * HUDScale + 2, False)
	DrawImage ArmorIcon, iconX, y
End Function
