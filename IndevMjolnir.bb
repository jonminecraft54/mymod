;=====================================================================
; SCP: Containment Breach - Indev MJOLNIR Type 1 powered armour
;
;   Worn from the inventory like the ballistic vest (it takes a while to
;   climb into half a ton of armour). While worn:
;     - durability: most gunfire glances off; other injuries and blood
;       loss are cut hard
;     - strength/speed: stamina drains much slower and recovers faster
;     - reflexes: the neural link steadies your eyes (slower blinking)
;     - hardened: radiation almost entirely blocked, filters stop the
;       SCP-214/217 viruses and SCP-718's fluid
;     - immune to dark magic: SCP-202 can't pull anything out
;   It can't be combined with the vest or a hazmat suit.
;   (IndevMjolnirOn is declared in Main.bb next to the other Wearing*
;   flags, because NPCs.bb reads it for gunfire.)
;=====================================================================

Global IndevMjPrevInj#, IndevMjPrevBlood#, IndevMjPrevStamina#

Function IndevMjolnirReset()
	IndevMjolnirOn = False
	IndevMjPrevInj = 0 : IndevMjPrevBlood = 0 : IndevMjPrevStamina = 100
End Function

;called every frame while the armour is selected in the inventory
Function IndevUseMjolnir(it.Items)
	If (Not IndevMjolnirOn) And (WearingVest > 0 Or WearingHazmat > 0) Then
		Msg = "You'd have to take off what you're wearing first. The MJOLNIR's bodysuit goes on against the skin."
		MsgTimer = 70*4
		SelectedItem = Null
		Return
	EndIf

	CurrSpeed = CurveValue(0, CurrSpeed, 5.0)
	DrawItemUseProgress(it)
	it\state = Min(it\state + FPSfactor / 5.0, 100)
	If it\state < 100 Then Return

	it\state = 0
	If IndevMjolnirOn Then
		IndevMjolnirOn = False
		Msg = "The armour hisses and unseals plate by plate. You step out of it. Half a ton heavier on the floor than it ever felt on you."
		DropItem(it)
	Else
		IndevMjolnirOn = True
		IndevMjPrevInj = Injuries : IndevMjPrevBlood = Bloodloss : IndevMjPrevStamina = Stamina
		Msg = "The plates lock around you and the neural link wakes. The weight vanishes. Readouts bloom straight into your mind: MJOLNIR-1 ONLINE."
		PlaySound_Strict(PickSFX(2))
		If WearingNightVision Then CameraFogFar = StoredCameraFogFar
		WearingNightVision = 0
	EndIf
	MsgTimer = 70*6
	SelectedItem = Null
End Function

Function UpdateIndevMjolnir()
	If (Not IndevMjolnirOn) Then Return

	;taken off by being dropped / lost
	Local n%, have% = False
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "mjolnir" Then have = True : Exit
		EndIf
	Next
	If (Not have) Or KillTimer < 0 Then
		IndevMjolnirOn = False
		Return
	EndIf

	;durability: only a fraction of any new injury or bleeding gets through the Dragonium and the gel layer
	Local pass# = 0.35 + 0.55 * (1.0 - IndevMjShieldFrac())      ;an empty shield lets most of it through
	If Injuries > IndevMjPrevInj Then
		IndevArmorHit((Injuries - IndevMjPrevInj) * (1.0 - pass) * 60.0)
		Injuries = IndevMjPrevInj + (Injuries - IndevMjPrevInj) * pass
	EndIf
	If Bloodloss > IndevMjPrevBlood Then
		IndevArmorHit((Bloodloss - IndevMjPrevBlood) * 0.6)
		Bloodloss = IndevMjPrevBlood + (Bloodloss - IndevMjPrevBlood) * Min(1.0, pass + 0.05)
	EndIf
	IndevMjPrevInj = Injuries : IndevMjPrevBlood = Bloodloss

	;strength and speed: the exoskeleton does the work
	If Stamina < IndevMjPrevStamina Then Stamina = IndevMjPrevStamina + (Stamina - IndevMjPrevStamina) * 0.35
	Stamina = Min(100, Stamina + FPSfactor * 0.08)
	IndevMjPrevStamina = Stamina

	;reflexes: the neural interface keeps the eyes steady
	IndevBlinkModify(0.85, 1)
End Function

;gunfire (NPCs.bb Shoot): most rounds glance off the shell. True = the hit was absorbed
Function IndevMjolnirDeflect%()
	If (Not IndevMjolnirOn) Then Return False
	If IndevArmor < 15 Then Return False         ;shield down: rounds go straight through
	If Rand(10) = 1 Then Return False           ;a lucky shot finds a joint
	IndevArmorHit(15)
	CameraShake = Max(CameraShake, 0.6)
	If MsgTimer <= 0 Or Rand(3) = 1 Then
		Select Rand(1, 3)
			Case 1 Msg = "A round sparks off the MJOLNIR's shell."
			Case 2 Msg = "The refractive coating flares as a bullet glances away."
			Default Msg = "Impact on the chest plate. SHIELDS NOMINAL flickers across your mind."
		End Select
		MsgTimer = 70*2
	EndIf
	Return True
End Function
