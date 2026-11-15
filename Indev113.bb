;=====================================================================
; SCP: Containment Breach - Indev SCP-113 "The Jasper Stone"
;
;   A small polished red stone. Use it from the inventory with bare hands
;   and it bonds to your palm and runs its four stages:
;     1  (0.2 s)  it fuses to the skin - a burn; it can't be let go of
;     2  (20 s)   nausea, stinging, blurred vision
;     3  (60 s)   the transformation; the last 20 seconds are agony,
;                 and if you're already badly hurt the shock can kill you
;     4           it lets go and goes inert; your biological sex has changed
;   While it's bonded the stone can't be dropped or used again.
;   It won't react again for 60 seconds. After that every new exposure
;   has a failure chance (25%, growing fast with each use and slowly
;   forgiven with time) that tears you up from the inside - often fatal.
;   A hazmat suit or MJOLNIR armour counts as gloves: nothing happens.
;=====================================================================

Global I113Stage%, I113T#, I113Uses%, I113LastUse#, I113Fail%, I113Next#

Function Indev113Reset()
	I113Stage = 0 : I113T = 0 : I113Uses = 0 : I113LastUse = 0 : I113Fail = False : I113Next = 0
	IndevFemale = False : IndevGenderShown = False
End Function

;called when the stone is used from the inventory
Function IndevUse113(it.Items)
	SelectedItem = Null
	If I113Stage > 0 Then
		IndevPillMsg("The stone is still fused to your palm. It isn't done with you.", 4)
		Return
	EndIf
	If WearingHazmat > 0 Or IndevMjolnirOn Then
		IndevPillMsg("You turn the stone over in your gloved fingers. Smooth, warm, and completely inert through the material.", 5)
		Return
	EndIf
	If I113LastUse > 0 Then
		IndevPillMsg("You press the stone to your palm. Nothing. It's cold and dead - for now.", 4)
		Return
	EndIf

	;chance the transformation goes wrong: none on a first exposure, then 25% and climbing
	Local failChance# = 0
	If I113Uses > 0 Then failChance = Min(95, 25.0 * (1.6 ^ (I113Uses - 1)))
	I113Fail = (Rnd(100) < failChance)
	I113Uses = I113Uses + 1

	I113Stage = 1 : I113T = 14    ;0.2 seconds
	Injuries = Injuries + 0.25
	PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage1.ogg"))
	CameraShake = Max(CameraShake, 1.5)
	IndevPillMsg("The moment the stone touches your skin it BITES. It's fused to your palm, and the skin around it is burning.", 5)
End Function

;the bonded stone can't leave the inventory: put it back if it was dropped
Function Indev113Hold()
	Local n%, have% = False, i.Items
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "scp113" Then have = True : Exit
		EndIf
	Next
	If have Then Return
	For i = Each Items
		If i\itemtemplate\name = "scp113" And (Not i\Picked) Then
			If EntityDistance(i\collider, Collider) < 3.0 Then
				PickItem(i)
				If MsgTimer < 70 Then IndevPillMsg("You try to shake it off. It doesn't come away from your hand.", 3)
				Return
			EndIf
		EndIf
	Next
End Function

Function UpdateIndev113()
	If I113LastUse > 0 Then I113LastUse = I113LastUse - FPSfactor
	If I113Uses > 0 And I113Stage = 0 Then
		;time forgives: slowly lose one exposure's worth of risk every 5 minutes without contact
		I113Next = I113Next + FPSfactor
		If I113Next > 70*300 Then I113Next = 0 : I113Uses = Max(1, I113Uses - 1)
	EndIf
	If I113Stage = 0 Then Return
	If KillTimer < 0 Then I113Stage = 0 : Return

	Indev113Hold()
	I113T = I113T - FPSfactor

	Select I113Stage
		Case 1
			If I113T <= 0 Then
				I113Stage = 2 : I113T = 70*20
				IndevPillMsg("A low hum passes through your whole body from the stone. Your stomach lurches.", 5)
			EndIf
		Case 2
			BlurTimer = Max(BlurTimer, 70*0.5)
			If Rand(200) = 1 Then CameraShake = Max(CameraShake, 0.8)
			If I113T < 70*10 And I113T + FPSfactor >= 70*10 Then
				PlaySound_Strict(LoadTempSound("SFX\SCP\294\Vomit.ogg"))
				IndevPillMsg("You double over and throw up. Pins and needles sting across every inch of your skin.", 5)
				Stamina = Max(0, Stamina - 40)
			EndIf
			If I113T <= 0 Then
				I113Stage = 3 : I113T = 70*60
				IndevPillMsg("Something is changing inside you. You can feel it moving through your cells.", 5)
			EndIf
		Case 3
			IndevStress = Min(100, IndevStress + FPSfactor / 70.0 * 0.5)
			Stamina = Min(Stamina, 50)
			If I113T < 70*20 Then
				;the last twenty seconds
				If I113T + FPSfactor >= 70*20 Then
					PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage" + Rand(2, 4) + ".ogg"))
					IndevPillMsg("Every nerve in your body lights up at once. You can't think. You can't even scream.", 6)
				EndIf
				CameraShake = Max(CameraShake, 2.0)
				BlurTimer = Max(BlurTimer, 70*1)
				IndevBlinkModify(2.0, 1)
				Stamina = 0
				HeartBeatVolume = Max(HeartBeatVolume, 0.6) : HeartBeatRate = Max(HeartBeatRate, 150)
				;shock kills the already badly hurt
				If Injuries > 3.0 Or Bloodloss > 70 Then
					IndevPillDeath("Subject D-9341 died of shock during the third stage of exposure to SCP-113. The subject was already severely injured at the time of contact.")
					I113Stage = 0
					Return
				EndIf
			EndIf
			If I113T <= 0 Then
				I113Stage = 0 : I113T = 0 : I113LastUse = 70*60
				If I113Fail Then
					Injuries = Injuries + 3.2
					Bloodloss = Bloodloss + 60
					CameraShake = 4
					PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage" + Rand(1, 4) + ".ogg"))
					If Injuries > 4.0 Or Bloodloss >= 100 Then
						IndevPillDeath("Subject D-9341 was found dead holding SCP-113. Autopsy shows massive bone, organ and tissue damage consistent with a failed transformation after repeated exposure. Cause of death: organ trauma and internal bleeding.")
						Return
					EndIf
					IndevPillMsg("Something goes wrong. White-hot pain tears through your bones and organs. The stone drops away. You're bleeding badly on the inside.", 8)
				Else
					PlaySound_Strict(LoadTempSound("SFX\SCP\1162\BodyHorrorExchange" + Rand(1, 4) + ".ogg"))
					IndevGenderSwap() ;the HUD icon (IndevSide.bb)
					If I113Uses = 1 Then
						IndevPillMsg("The pain stops. The stone falls away, cold and dull. Your body is different now - your biological sex has changed. You're still you.", 8)
					Else
						IndevPillMsg("It stops. The stone drops from your palm, inert. Your body has changed back again. You feel wrung out.", 7)
					EndIf
					Injuries = Injuries + 0.2
				EndIf
				IndevRelieveStress(10)
			EndIf
	End Select
End Function

;SCP-914: rough/coarse grinds it to red grit, anything else gives it back unchanged
Function IndevRefine113(item.Items, setting$, x#, y#, z#)
	Local it2.Items, d.Decals
	If I113Stage > 0 Then
		it2 = CreateItem("scp113", x, y, z)   ;(can't happen normally - it's stuck to your hand)
		RemoveItem(item)
		Return
	EndIf
	Select setting
		Case "rough", "coarse"
			d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
			EntityColor(d\obj, 150, 50, 25)
			d\Size = 0.08 : ScaleSprite(d\obj, d\Size, d\Size)
			it2 = CreateItem("scp113", x, y, z)   ;the grit fuses back into the stone
		Default
			it2 = CreateItem("scp113", x, y, z)
	End Select
	RemoveItem(item)
End Function
