;=====================================================================
; SCP: Containment Breach - Indev blinking
;
;   Two multipliers layered on top of the vanilla blink timer (and on
;   top of eyedrops' BlinkEffect, which still works as before):
;     IndevBlinkMul       how fast the meter drains (>1 = blink sooner)
;     IndevBlinkCloseMul  how fast a blink finishes (<1 = eyes stay shut longer)
;
;   Player condition: stress, exhaustion, blood loss, heavy injuries,
;   calm crouching. SCP effects: SCP-718's stare, SCP-096's rage, SCP-719's
;   heat, and several pills. Everything is recalculated every frame and
;   eases in and out, so it never snaps.
;=====================================================================

Global IndevBlinkMul# = 1.0, IndevBlinkCloseMul# = 1.0
Global IndevBlinkTarget# = 1.0, IndevBlinkCloseTarget# = 1.0
Global IndevBlinkReason$, IndevBlinkLastReason$, IndevBlinkMsgT#
Global IndevBlink718Held#

;temporary modifier any Indev effect can push: strongest one wins until it runs out
Global IndevBlinkTempMul# = 1.0, IndevBlinkTempT#

Function IndevBlinkReset()
	IndevBlinkMul = 1.0 : IndevBlinkCloseMul = 1.0
	IndevBlinkTarget = 1.0 : IndevBlinkCloseTarget = 1.0
	IndevBlinkReason = "" : IndevBlinkLastReason = "" : IndevBlinkMsgT = 0
	IndevBlink718Held = 0
	IndevBlinkTempMul = 1.0 : IndevBlinkTempT = 0
End Function

;e.g. IndevBlinkModify(1.5, 20) = blink 50% more often for 20 seconds
Function IndevBlinkModify(mul#, seconds#)
	If IndevBlinkTempT <= 0 Or Abs(mul - 1.0) >= Abs(IndevBlinkTempMul - 1.0) Then
		IndevBlinkTempMul = mul
		IndevBlinkTempT = seconds * 70
	EndIf
End Function

Function UpdateIndevBlink()
	Local mul# = 1.0, closeMul# = 1.0, reason$ = ""

	;---------------- player condition
	;nervous blinking under stress
	If IndevStress >= 80 Then
		mul = mul * 1.3 : reason = "stress"
	ElseIf IndevStress >= 60 Then
		mul = mul * 1.15
	EndIf
	;worn out: eyes dry out faster and blinks get heavy
	If Stamina < 25 Then
		mul = mul * 1.2 : closeMul = closeMul * 0.85
		If reason = "" Then reason = "tired"
	EndIf
	;losing blood: slow, heavy blinks
	If Bloodloss > 40 Then
		mul = mul * 1.15 : closeMul = closeMul * (1.0 - Min(0.35, (Bloodloss - 40) / 150.0))
		reason = "blood"
	EndIf
	If Injuries > 1.5 Then mul = mul * 1.1
	;crouched and still: calm, steady eyes
	If Crouch And CurrSpeed < 0.001 And IndevStress < 40 Then mul = mul * 0.85

	;---------------- SCP effects
	;SCP-718: once it has you, you can't look away - and you pay for it after
	;(the stare stage never goes back down on its own, so also require being in the eye's sight right now)
	Local held718% = False
	If I718StareStage >= 2 And I718Eye <> 0 And I718Alive Then
		If EntityDistance(I718Eye, Camera) < 7.0 Then held718 = EntityVisible(I718Eye, Camera)
	EndIf
	If held718 Then
		mul = mul * 0.45 : reason = "718"
		IndevBlink718Held = IndevBlink718Held + FPSfactor
	ElseIf IndevBlink718Held > 0 Then
		EyeIrritation = Max(EyeIrritation, Min(IndevBlink718Held * 0.3, 70*6))
		IndevBlink718Held = 0
		Msg = "You finally tear your eyes away. They're burning."
		MsgTimer = 70*4
	EndIf
	;SCP-096 raging somewhere: panic blinking
	If Curr096 <> Null Then
		If Curr096\State >= 1 And Curr096\State <= 4 Then mul = mul * 1.25
	EndIf
	;SCP-719 running hot nearby: dry, stinging eyes
	If I719On And I719TV <> 0 Then
		If EntityDistance(Collider, I719TV) < 4.0 And I719T > 60 Then mul = mul * 1.2
	EndIf
	;pills
	If Pill7521Timer > 0 Then mul = mul * 1.4 : If reason = "" Then reason = "dry"
	If Pill4257Timer > 0 Then mul = mul * 0.6 : reason = "focus"     ;space drive: locked straight ahead
	If Pill3866Timer > 0 Then mul = mul * 0.7 : closeMul = closeMul * 0.7   ;slowed heart, slowed everything
	If Pill484Timer > 0 Then mul = mul * 0.85                           ;sharpened eyes
	If Spring006BTimer > 0 Then mul = mul * 0.8                        ;SCP-006-B vitality
	;the Cognitive Filter Glasses keep dust and glare off the eyes
	If IndevCogOn Then mul = mul * 0.9

	;temporary modifier pushed by other effects
	If IndevBlinkTempT > 0 Then
		IndevBlinkTempT = IndevBlinkTempT - FPSfactor
		mul = mul * IndevBlinkTempMul
		If IndevBlinkTempT <= 0 Then IndevBlinkTempMul = 1.0
	EndIf

	IndevBlinkTarget = Max(0.3, Min(2.5, mul))
	IndevBlinkCloseTarget = Max(0.5, Min(1.0, closeMul))

	;ease toward the target over about a second
	Local k# = Min(1.0, FPSfactor / 70.0)
	IndevBlinkMul = IndevBlinkMul + (IndevBlinkTarget - IndevBlinkMul) * k
	IndevBlinkCloseMul = IndevBlinkCloseMul + (IndevBlinkCloseTarget - IndevBlinkCloseMul) * k

	;a quiet one-line hint the first time a new cause kicks in (not spammed)
	IndevBlinkMsgT = IndevBlinkMsgT - FPSfactor
	If reason <> IndevBlinkLastReason Then
		If reason <> "" And IndevBlinkMsgT <= 0 And MsgTimer <= 0 Then
			Select reason
				Case "tired" Msg = "Your eyes feel heavy and dry."
				Case "blood" Msg = "Each blink takes a little longer than the last."
				Case "stress" Msg = "You can't stop blinking."
				Case "dry" Msg = "Your eyes are painfully dry."
				Case "focus" Msg = "You stare straight ahead. Blinking feels optional."
				Default Msg = ""
			End Select
			If Msg <> "" Then MsgTimer = 70*3 : IndevBlinkMsgT = 70*45
		EndIf
		IndevBlinkLastReason = reason
	EndIf
End Function
