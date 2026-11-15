;=====================================================================
; SCP: Containment Breach - Indev SCP-109 "The Infinite Canteen"
;
;   A WW2 US army canteen that never runs dry. Kept on the pedestal in
;   room1newscproom. Use it from the inventory to drink:
;     - stamina refilled, blur and dizziness cleared, stress eased
;     - bleeding slowed and minor injuries soothed, radiation dose flushed
;   The water doesn't stop when you do. Every drink within about 12 seconds
;   of the last one fills your lungs a bit more:
;     2nd quick drink: you splutter        3rd: coughing fit, choking
;     4th: you can't breathe - drowning on dry land (death)
;   Lungs clear by themselves after a while.
;   SCP-914: Rough - the canteen bursts and floods the output booth (gone)
;            1:1   - an ordinary empty canteen... that's still SCP-109
;            Fine / Very Fine - it comes out ice-cold (no change in use)
;=====================================================================

Global I109Lungs#, I109LastDrink#, I109Drinks%

Function Indev109Reset()
	I109Lungs = 0 : I109LastDrink = 0 : I109Drinks = 0
End Function

;called from FillRoom
Function IndevFill109(r.Rooms)
	Local it.Items
	;on top of the metal pedestal in the storage cell (top at y 169, checked against the room mesh)
	;on the pedestal of the north cell of the rebuilt room (Tools\roomkit\room_scpstorage.py)
	it = CreateItem("scp109", r\x + 0.0 * RoomScale, r\y + 185.0 * RoomScale, r\z + 880.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	;the document on the floor next to the pedestal
	it = CreateItem("doc109", r\x + 130.0 * RoomScale, r\y + 15.0 * RoomScale, r\z + 880.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

;used from the inventory
Function IndevUse109(it.Items)
	SelectedItem = Null
	If WearingGasMask > 0 Or WearingHazmat > 0 Then
		IndevPillMsg("You can't drink with the mask on. Water sloshes faintly inside the canteen - it sounds full. It always sounds full.", 5)
		Return
	EndIf

	Local quick% = (I109LastDrink > 0)
	I109LastDrink = 70*12
	If quick Then I109Drinks = I109Drinks + 1 Else I109Drinks = 1

	PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))

	;the good part: always happens
	Stamina = 100
	BlurTimer = 0
	CameraShake = 0
	Injuries = Max(0, Injuries - 0.15)
	Bloodloss = Max(0, Bloodloss - 15)
	IndevStress = Max(0, IndevStress - 8)
	IndevRadDose = Max(0, IndevRadDose - 10)

	Select I109Drinks
		Case 1
			I109Lungs = Max(I109Lungs, 0)
			IndevPillMsg("You unscrew the cap and drink. Cold, clean water - the best you've ever tasted. You feel steadier.", 5)
		Case 2
			I109Lungs = I109Lungs + 35
			PlaySound_Strict(LoadTempSound("SFX\SCP\294\cough.ogg"))
			IndevPillMsg("You drink again. It keeps coming after you swallow - you splutter and have to pull it away from your mouth.", 5)
		Case 3
			I109Lungs = I109Lungs + 45
			PlaySound_Strict(LoadTempSound("SFX\SCP\294\retch1.ogg"))
			CameraShake = 2
			BlurTimer = 70*3
			Stamina = 20
			IndevPillMsg("Water floods your throat faster than you can swallow. You're choking. STOP DRINKING.", 6)
		Default
			PlaySound_Strict(LoadTempSound("SFX\SCP\294\retch2.ogg"))
			IndevPillDeath("Subject D-9341 was found in a dry corridor with SCP-109 still clutched in one hand. Autopsy found the lungs completely filled with fresh water. Cause of death: drowning.")
	End Select
End Function

Function UpdateIndev109()
	If I109LastDrink > 0 Then
		I109LastDrink = I109LastDrink - FPSfactor
		If I109LastDrink <= 0 Then I109Drinks = 0
	EndIf
	If I109Lungs <= 0 Then Return
	If KillTimer < 0 Then I109Lungs = 0 : Return
	;water on the lungs: short of breath, coughing now and then, clears slowly
	I109Lungs = Max(0, I109Lungs - FPSfactor * 0.03)
	Stamina = Min(Stamina, 100 - I109Lungs)
	If Rand(Int(Max(90, 900 - I109Lungs * 8))) = 1 Then
		PlaySound_Strict(LoadTempSound("SFX\SCP\294\cough.ogg"))
		CameraShake = Max(CameraShake, 0.6)
	EndIf
	If I109Lungs <= 0 Then IndevPillMsg("You cough up the last of the water. Breathing is easy again.", 4)
End Function

;SCP-914
Function IndevRefine109(item.Items, setting$, x#, y#, z#)
	Local it2.Items, de.Decals
	Select setting
		Case "rough"
			;it bursts: water everywhere in the output booth, no canteen
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			de\Size = 0.6 : EntityAlpha(de\obj, 0.5) : ScaleSprite(de\obj, de\Size, de\Size)
			RemoveItem(item)
		Case "1:1", "coarse"
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
		Default
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
			Msg = "Frost forms on the canteen as it comes out of the machine."
			MsgTimer = 70*3
	End Select
End Function
