;=====================================================================
; SCP: Containment Breach - Indev SCP-202
;
;   A purple FOB watch that is really a compass for "magic" - anything
;   anomalous. Open it (use it from the inventory) and its face comes up
;   in the corner of the screen with a needle pointing at the nearest
;   anomaly: SCP-173, 106, 096, 122, 330, 718, 719, 738, 993.
;
;   Hold it open right next to one and it starts to extract. The energy
;   goes into you: once the watch is full you "transform" for a while -
;   no fatigue, wounds closing, eyes that barely need to blink - but your
;   mind bends with it, and when it wears off you crash. Every
;   transformation leaves less of you behind; the fourth is the last.
;=====================================================================

Global I202Open%, I202Charge#, I202Power#, I202Uses%, I202MsgStage%, I202Whisper#
Global I202HudImg%, I202Target%, I202TargetDist#, I202TargetName$

Function Indev202Reset()
	I202Open = 0 : I202Charge = 0 : I202Power = 0 : I202Uses = 0 : I202MsgStage = 0 : I202Whisper = 0
	I202Target = 0 : I202TargetDist = 0 : I202TargetName = ""
End Function

;consider one candidate anomaly for the needle
Function I202Consider(ent%, name$)
	If ent = 0 Then Return
	Local d# = EntityDistance(Collider, ent)
	If I202Target = 0 Or d < I202TargetDist Then
		I202Target = ent : I202TargetDist = d : I202TargetName = name
	EndIf
End Function

Function I202FindTarget()
	I202Target = 0 : I202TargetDist = 0 : I202TargetName = ""
	If Curr173 <> Null Then I202Consider(Curr173\Collider, "173")
	If Curr106 <> Null Then
		If Curr106\State <= 0 And (Not Curr106\Idle) And (Not Contained106) Then I202Consider(Curr106\Collider, "106")
	EndIf
	If Curr096 <> Null Then I202Consider(Curr096\Collider, "096")
	I202Consider(I122Obj, "122")
	I202Consider(I330Bowl, "330")
	If I718Alive Then I202Consider(I718Stalk, "718")
	I202Consider(I719TV, "719")
	I202Consider(I738Desk, "738")
	I202Consider(I993TV, "993")
End Function

;called every frame while the watch is selected (from IndevUsePill, during the 2D pass): draws the compass
Function IndevUse202(it.Items)
	I202Open = 2

	If I202HudImg = 0 Then
		I202HudImg = LoadImageHUDScaled("GFX\items\scp202_hud.png")
		MaskImage(I202HudImg, 0, 0, 0)
	EndIf
	Local w% = ImageWidth(I202HudImg), h% = ImageHeight(I202HudImg)
	Local x% = HUDEndX - w - 20 * HUDScale, y% = HUDEndY - h - 20 * HUDScale
	DrawImage(I202HudImg, x, y)

	Local cx# = x + w * 150.0 / 300.0, cy# = y + h * 200.0 / 360.0
	Local len# = w * 118.0 / 300.0
	Local ang#

	If I202Target <> 0 Then
		ang = -DeltaYaw(Camera, I202Target)                ;0 = straight ahead, positive = to the right
		;extraction makes the needle shiver against the target
		If I202TargetDist < 2.5 Then ang = ang + Rnd(-6, 6) * (1.0 - I202TargetDist / 2.5)
	Else
		ang = Sin(MilliSecs() / 9.0) * 170                 ;nothing nearby: it spins lazily
	EndIf

	;needle: a few parallel lines so it reads at any resolution
	Local ex# = cx + Sin(ang) * len, ey# = cy - Cos(ang) * len
	Local i%
	Color 235, 90, 235
	For i = -1 To 1
		Line(cx + i, cy, ex + i, ey)
		Line(cx, cy + i, ex, ey + i)
	Next
	;the pink jewel pulses faster the closer the target is
	Local pulse# = 1.0
	If I202Target <> 0 Then pulse = 0.5 + 0.5 * Sin(MilliSecs() * (0.2 + 1.5 / Max(1.0, I202TargetDist)))
	Color 230, 70 + 100 * pulse, 230
	Local r# = w * (0.018 + 0.012 * pulse)
	Oval(cx - r, cy - r, r * 2, r * 2, True)

	;charge ring along the bottom
	If I202Charge > 0 Then
		Color 120, 60, 150
		Rect(x + w * 0.2, y + h - 8 * HUDScale, w * 0.6, 5 * HUDScale, False)
		Color 225, 80, 225
		Rect(x + w * 0.2, y + h - 8 * HUDScale, w * 0.6 * I202Charge / 100.0, 5 * HUDScale, True)
	EndIf
End Function

Function UpdateIndev202()
	If KillTimer < 0 Then I202Open = 0 : Return
	Local dt# = FPSfactor / 70.0

	If I202Open > 0 Then
		I202Open = I202Open - 1
		I202FindTarget()

		;extraction: only right up close
		;the MJOLNIR is immune to dark magic: its refractive coating scatters the pull
		If I202Target <> 0 And I202TargetDist < 2.5 And IndevMjolnirOn And I202MsgStage = 0 Then
			I202MsgStage = -1 : Msg = "The watch strains toward the " + I202Label() + ", but the armour's coating shimmers and whatever it pulls just scatters." : MsgTimer = 70*5
		EndIf
		If I202Target <> 0 And I202TargetDist < 2.5 And I202Power <= 0 And (Not IndevMjolnirOn) Then
			I202Charge = Min(100, I202Charge + dt * 9.0 * (1.0 - I202TargetDist / 2.5) + dt * 1.0)
			If I202TargetName = "122" And Rand(90) = 1 Then I122Flicker = Max(I122Flicker, 70*0.4)   ;its light gutters
			If I202MsgStage = 0 And I202Charge > 10 Then
				I202MsgStage = 1 : Msg = "The watch hums in your hand. The needle presses against the pin, trembling." : MsgTimer = 70*4
			ElseIf I202MsgStage = 1 And I202Charge > 40 Then
				I202MsgStage = 2 : Msg = "Warmth crawls up your arm from the watch. Something is being pulled out of the " + I202Label() + " - and into you." : MsgTimer = 70*5
				BlurTimer = Max(BlurTimer, 70*1)
			ElseIf I202MsgStage = 2 And I202Charge > 75 Then
				I202MsgStage = 3 : Msg = "You should close it. You don't want to close it." : MsgTimer = 70*4
				CameraShake = Max(CameraShake, 0.5)
			EndIf
			If I202Charge >= 100 Then I202Transform()
		EndIf
	Else
		;closed: the pull fades back out
		I202Charge = Max(0, I202Charge - dt * 2.0)
		If I202Charge < 5 Then I202MsgStage = 0
	EndIf

	;transformed
	If I202Power > 0 Then
		I202Power = I202Power - FPSfactor
		Stamina = 100
		Injuries = Max(0, Injuries - dt * 0.01)
		Bloodloss = Max(0, Bloodloss - dt * 0.4)
		IndevBlinkModify(0.5, 1)
		IndevStress = Max(IndevStress, 35 + 10 * I202Uses)     ;it doesn't feel like calm
		I202Whisper = I202Whisper - FPSfactor
		If I202Whisper <= 0 And MsgTimer <= 0 Then
			Select Rand(1, 5)
				Case 1 Msg = "More. There's more of it out there. You can feel where."
				Case 2 Msg = "Your reflection in the watch glass doesn't look quite like you."
				Case 3 Msg = "You haven't been tired in a long time. You don't remember what tired was."
				Case 4 Msg = "Everything in this facility is full of it. Why should they have it?"
				Default Msg = "Your hands look longer than they used to."
			End Select
			MsgTimer = 70*4
			I202Whisper = 70 * Rnd(35, 60)
		EndIf
		If I202Power <= 0 Then I202Crash()
	EndIf
End Function

Function I202Label$()
	Select I202TargetName
		Case "173" Return "sculpture"
		Case "106" Return "old man"
		Case "096" Return "pale thing"
		Case "122" Return "night light"
		Case "330" Return "bowl"
		Case "718" Return "eye"
		Case "719" Return "television"
		Case "738" Return "table"
		Case "993" Return "television"
	End Select
	Return "thing"
End Function

Function I202Transform()
	I202Uses = I202Uses + 1
	I202Charge = 0 : I202MsgStage = 0
	If I202Uses >= 4 Then
		DeathMSG = "Subject D-9341 was found holding SCP-202 open. The subject had undergone extensive physical and mental alteration and was no longer responsive to verbal commands. Termination was authorised after it attempted to reach SCP-" + I202TargetName + " through a sealed door."
		Kill()
		Return
	EndIf
	I202Power = 70 * (150 - 20 * (I202Uses - 1))
	I202Whisper = 70 * 20
	CameraShake = 2 : BlurTimer = 70*3
	LightFlash = 1.5
	Select I202Uses
		Case 1 Msg = "The watch goes cold. You don't. It pours through you - your heart slows, your legs stop aching, your eyes feel wide open. You feel incredible."
		Case 2 Msg = "It floods in again, easier this time. Your fingers ache as they stretch. You don't mind."
		Default Msg = "It comes into you like it's coming home. There isn't much left that it has to push aside."
	End Select
	MsgTimer = 70*8
End Function

Function I202Crash()
	Stamina = 0
	Injuries = Injuries + 0.2 * I202Uses
	IndevStress = Min(100, IndevStress + 20 + 10 * I202Uses)
	BlurTimer = 70*5 : CameraShake = 1.5
	Select I202Uses
		Case 1 Msg = "It drains out of you all at once. You sag against the wall, shaking, and your first thought is where to find more."
		Case 2 Msg = "The crash is worse this time. Your hands don't quite go back to the shape they were."
		Default Msg = "Empty again. You can't remember your own name for a moment. You remember exactly where the nearest anomaly is."
	End Select
	MsgTimer = 70*7
End Function
