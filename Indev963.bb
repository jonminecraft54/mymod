;=====================================================================
; SCP: Containment Breach - Indev SCP-963 "Immortality" + SCP-2295 "The Bear with a Heart of Patchwork"
;
;   Both live in room1newscproom: SCP-963 on the pedestal with the padded plate,
;   SCP-2295 in the open toy chest.
;
;   SCP-963 (carried in the inventory):
;     When something would kill the player, the mind of a former host takes the hit
;     instead - the player collapses, and gets up again healed.
;     It needs 2 minutes to "settle" between saves. The first two saves work.
;     The third time there's nothing of D-9341 left to bring back.
;     Using it shows how much of you is still you.
;
;   SCP-2295 (use it from the inventory):
;     Hurt or bleeding: it stitches felt into your wounds - injuries and
;     bleeding healed completely. Then it needs 4 minutes to repair itself.
;     Unhurt, or while it's repairing: it just hugs you (stress relief).
;
;   SCP-914: the amulet always comes out untouched (something in it finds that funny).
;            Rough/Coarse tear the bear apart - it stitches itself back up, slowly.
;            Fine/Very Fine: freshly restuffed, ready to help straight away.
;=====================================================================

Global I963Saves%, I963Cool#, I963Wake#
Global I2295Cool#, I2295Item.Items

Function Indev963Reset()
	I963Saves = 0 : I963Cool = 0 : I963Wake = 0
	I2295Cool = 0 : I2295Item = Null
End Function

;called from FillRoom
Function IndevFill963(r.Rooms)
	Local it.Items
	;SCP-963 on the padded plate of the middle pedestal (top y 161)
	;the three cell doors of the rebuilt room (Tools\roomkit\room_scpstorage.py): SCP-963 west, SCP-2295 east, SCP-109 north
	IV1Door(r, -480.0, 0.0, 376.0, 90, 0)
	IV1Door(r, 480.0, 0.0, 320.0, 90, 0)
	IV1Door(r, 0.0, 0.0, 672.0, 0, 0)
	it = CreateItem("scp963", r\x - 752.0 * RoomScale, r\y + 175.0 * RoomScale, r\z + 376.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("doc963", r\x - 630.0 * RoomScale, r\y + 15.0 * RoomScale, r\z + 376.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	;SCP-2295 inside the open wooden chest (chest floor y 162)
	it = CreateItem("scp2295", r\x + 754.0 * RoomScale, r\y + 172.0 * RoomScale, r\z + 319.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	I2295Item = it
	it = CreateItem("doc2295", r\x + 640.0 * RoomScale, r\y + 15.0 * RoomScale, r\z + 319.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

Function IndevHasItem%(name$)
	Local n%
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = name Then Return True
		EndIf
	Next
	Return False
End Function

;----------------------------------------------------------------- SCP-963

;called at the top of Kill(): True means the death was taken by the amulet
Function Indev963Intercept%()
	If KillTimer < 0 Then Return False
	If Not IndevHasItem("scp963") Then Return False
	If I963Cool > 0 Then Return False

	I963Saves = I963Saves + 1
	If I963Saves >= 3 Then
		DeathMSG = "Subject D-9341 was found unconscious, uninjured, holding SCP-963. On waking, the subject gave the name of a researcher listed as deceased since 1998, "
		DeathMSG = DeathMSG + "thanked security for 'the loan of the body' and asked for coffee. D-9341 is considered deceased."
		Return False
	EndIf

	;saved: the body is patched up, the mind takes the hit
	DeathMSG = ""
	Injuries = 0
	Bloodloss = 0
	Stamina = 0
	BlurTimer = 70*8
	LightBlink = 6.0
	CameraShake = 4.0
	CurrSpeed = 0
	I963Cool = 70*120
	I963Wake = 70*3
	If Infect > 0 Then Infect = 0
	IndevStress = Min(100, IndevStress + 30)
	PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage" + Rand(1, 4) + ".ogg"))
	If I963Saves = 1 Then
		IndevPillMsg("Everything goes black - and then you're getting up off the floor. The amulet is warm. A voice that isn't yours says: " + Chr(34) + "Well, that was close. You're welcome." + Chr(34), 8)
	Else
		IndevPillMsg("You die. You're sure of it. Then you stand up again, and for a moment you can't remember your own number. " + Chr(34) + "Once more and I keep the body, kid." + Chr(34), 8)
	EndIf
	Return True
End Function

Function IndevUse963(it.Items)
	SelectedItem = Null
	Select I963Saves
		Case 0 IndevPillMsg("The amulet is heavier than it looks. When you touch it, you have the strangest feeling that someone is reading over your shoulder.", 6)
		Case 1 IndevPillMsg("You look at the red stone and grin - except you didn't mean to grin. Half of you is someone else now.", 6)
		Default IndevPillMsg("You can barely remember being D-9341. Your hand keeps reaching for a lab coat you've never owned. One more death and you're gone.", 7)
	End Select
	If I963Cool > 0 Then
		Msg = Msg + "  (It's still cold - not ready.)"
	EndIf
End Function

;----------------------------------------------------------------- SCP-2295

Function IndevUse2295(it.Items)
	SelectedItem = Null
	If I2295Cool > 0 Then
		IndevRelieveStress(8)
		IndevPillMsg("The bear is still sewing its own chest shut with a tiny needle. It pauses to give you a hug with one arm.", 5)
		Return
	EndIf
	If Injuries > 0.15 Or Bloodloss > 5 Then
		Injuries = 0
		Bloodloss = 0
		BlurTimer = 70*2
		I2295Cool = 70*240
		IndevRelieveStress(20)
		PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
		IndevPillMsg("The bear opens its chest, pulls out a piece of red felt and stitches it into you. It tickles. Your wounds are gone.", 7)
	Else
		IndevRelieveStress(15)
		IndevPillMsg("You're not hurt. The bear hugs you anyway. It's surprisingly warm.", 4)
	EndIf
End Function

Function UpdateIndev963()
	;the bear sits down inside the chest: the chest walls hide it from the normal item pick and the
	;pedestal keeps the player just outside the 1.2 pick range, so it gets its own, longer click
	If I2295Item <> Null Then
		If I2295Item\Picked Then
			I2295Item = Null
		ElseIf KillTimer >= 0 And ClosestItem = Null Then
			If EntityDistance(Camera, I2295Item\collider) < 2.0 Then
				If IndevAimedAt(I2295Item\collider, I2295Item\collider, 2.0) Then
					DrawHandIcon = True
					If MouseHit1 Then
						MouseHit1 = False
						PickItem(I2295Item)
						I2295Item = Null
					EndIf
				EndIf
			EndIf
		EndIf
	EndIf
	If I963Cool > 0 Then I963Cool = I963Cool - FPSfactor
	If I2295Cool > 0 Then I2295Cool = I2295Cool - FPSfactor
	If I963Wake > 0 Then
		;getting back up
		I963Wake = I963Wake - FPSfactor
		CurrSpeed = 0
		BlinkTimer = Min(BlinkTimer, -2)
	EndIf
End Function

;SCP-914
Function IndevRefine963(item.Items, setting$, x#, y#, z#)
	Local de.Decals
	PositionEntity(item\collider, x, y, z)
	ResetEntity(item\collider)
	If item\itemtemplate\name = "scp963" Then
		Msg = "The amulet comes out exactly as it went in. Somewhere, somebody is laughing."
		MsgTimer = 70*4
		Return
	EndIf
	Select setting
		Case "rough", "coarse"
			de = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
			EntityColor(de\obj, 200, 180, 150)
			de\Size = 0.3 : ScaleSprite(de\obj, de\Size, de\Size)
			I2295Cool = 70*600
			Msg = "The bear comes out in tatters, stuffing everywhere. It's already trying to sew itself back together."
			MsgTimer = 70*5
		Case "fine", "very fine"
			I2295Cool = 0
			Msg = "The bear comes out freshly restuffed, every seam neat and tight."
			MsgTimer = 70*4
	End Select
End Function
