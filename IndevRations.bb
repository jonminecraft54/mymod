;=====================================================================
; SCP: Containment Breach - Indev commissary items
;
;   Emergency Ration (indevration): a Foundation-issue meal-in-a-pouch.
;     Eating it restores a little health and stamina.
;
;   Water Bottle (indevwater): a 500 ml commissary bottle. Drinking it
;     gives back a little stamina and a touch of stress relief.
;
;   Both are one-shot items - they leave your inventory after use.
;
;   SCP-914:
;     Rough / Coarse - crushed (dust) or mangled ("Worn", weaker)
;     Fine / Very Fine - upgraded: ration becomes a fine first-aid kit;
;                        water bottle becomes a full first-aid kit
;                        (very fine gives finefirstaid). A 1 in 5 chance
;                        on Very Fine still turns the ration to dust.
;=====================================================================

Function IndevUseRation(it.Items)
	If Not CanUseItem(False, False, True) Then Return
	If U38Ration(it) Then Return ;SCP-1117-3 cannot eat ordinary food (IndevU38.bb)
	Injuries = Max(0, Injuries - 0.5)
	Bloodloss = Max(0, Bloodloss - 5)
	Stamina = Min(100, Stamina + 30)
	IndevRelieveStress(2)
	Select Rand(1, 4)
		Case 1 IndevPillMsg("The ration is dry, salty and about the density of packed clay. It sits in your stomach like an anchor, and you feel steadier for it.", 5)
		Case 2 IndevPillMsg("You tear the pouch open and eat without looking at it. Whatever it is, it's food. You feel a little better.", 5)
		Case 3 IndevPillMsg("Type B. Compressed protein bar, one biscuit, one square of chocolate that's older than you are. It works.", 5)
		Default IndevPillMsg("You chew through the ration in silence. The pouch says 1200 kcal. You believe it.", 5)
	End Select
	PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))
	RemoveItem(it)
	SelectedItem = Null
End Function

Function IndevUseWater(it.Items)
	If Not CanUseItem(False, False, True) Then Return
	If WearingGasMask > 0 Or WearingHazmat > 0 Then
		IndevPillMsg("You can't drink through the mask. You put the bottle away again.", 4)
		Return
	EndIf
	Stamina = Min(100, Stamina + 20)
	IndevRelieveStress(3)
	;a small nudge on the SCP-109-style water flag: it thins whatever's on the lungs a bit
	If I109Lungs > 0 Then I109Lungs = Max(0, I109Lungs - 6)
	Select Rand(1, 3)
		Case 1 IndevPillMsg("You crack the seal and drink half the bottle in one go. Clean, faintly plasticky. You feel less brittle.", 5)
		Case 2 IndevPillMsg("Cold spring water. Your throat had been dry longer than you had noticed.", 5)
		Default IndevPillMsg("You drink slowly. It's just water and it's exactly what you needed.", 4)
	End Select
	PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))
	RemoveItem(it)
	SelectedItem = Null
End Function

;----------------------------------------------------------------- SCP-914 recipes

Function IndevRefineRation(item.Items, setting$, x#, y#, z#)
	Local it2.Items
	Select setting
		Case "rough"
			IndevRefineDust(x, z, 78, 82, 52)
			RemoveItem(item)
			Msg = "The ration comes out as brown crumbs across the output tray. There is more of it, and less of it, than went in." : MsgTimer = 70*4
		Case "coarse"
			IndevRefineSetGrade(item, -1)
			If item\state > 0 Then item\state = item\state * 0.5
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			Msg = "The wrapper comes out crushed and the ration inside is half of what it was, but you could still eat it." : MsgTimer = 70*4
		Case "fine"
			it2 = CreateItem("firstaid", x, y, z)
			RemoveItem(item)
			Msg = "The pouch is gone. A field first aid kit sits in the tray - the Foundation apparently refines calories all the way to sutures." : MsgTimer = 70*5
		Case "very fine"
			If Rand(5) = 1 Then
				IndevRefineDust(x, z, 220, 220, 180)
				RemoveItem(item)
				Msg = "914 takes the ration too far. Fine white powder in the tray, and a smell of burnt toast." : MsgTimer = 70*4
			Else
				it2 = CreateItem("finefirstaid", x, y, z)
				RemoveItem(item)
				Msg = "The pouch is gone. A sealed field-surgery kit sits in the tray, unbranded, still warm." : MsgTimer = 70*5
			EndIf
		Default
			;1:1: reworked into the other commissary item
			it2 = CreateItem("indevwater", x, y, z)
			RemoveItem(item)
			Msg = "The ration comes out as a bottle of water, sealed and cold." : MsgTimer = 70*4
	End Select
End Function

Function IndevRefineWater(item.Items, setting$, x#, y#, z#)
	Local it2.Items
	Select setting
		Case "rough"
			IndevRefineDust(x, z, 180, 200, 220)
			RemoveItem(item)
			Msg = "The bottle comes out crushed flat and empty. A wet stain spreads across the output tray." : MsgTimer = 70*4
		Case "coarse"
			IndevRefineSetGrade(item, -1)
			If item\state > 0 Then item\state = item\state * 0.5
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			Msg = "The bottle comes out half empty. It's still sealed." : MsgTimer = 70*4
		Case "fine", "very fine"
			it2 = CreateItem("firstaid", x, y, z)
			RemoveItem(item)
			Msg = "The bottle is gone. A field first aid kit sits in the tray." : MsgTimer = 70*5
		Default
			it2 = CreateItem("indevration", x, y, z)
			RemoveItem(item)
			Msg = "The bottle comes out as a ration pouch, dry and dense." : MsgTimer = 70*4
	End Select
End Function
