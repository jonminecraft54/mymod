;=====================================================================
; SCP: Containment Breach - Indev: SCP-2107 "Diet Ghost" (twenty-seventh batch)
;
;   The can (item scp2107): drink it from the inventory. 30 to 60 seconds later the haunting starts and lasts
;   2 to 4 minutes per can (the article's 3-7 minutes and 1-3 hours, scaled to a game). Every can drunk adds time
;   and makes it worse: events come more often, and from the third can they can hurt.
;   The haunting: footsteps behind you, whispering, knocking, the lights flickering, a nearby open door
;   slamming shut, a cold breath, something pale at the edge of sight, and (3+ cans) being shoved or scratched.
;   It ends when the drink has broken down, or when you die.
;
;   room2b27diet: the cans are on the shelves (items); the refrigerated CNSI unit gives one cold can, once; the
;   break room's vending machine drops one can, once, then only hums.
;
;   The dose and timers are kept in the save (IndevSide.bb). Summary of scp-wiki.wikidot.com/scp-2107 (CC BY-SA 3.0).
;=====================================================================

Global I2107Cans%      ;cans in the system right now (the haunting's strength)
Global I2107Delay#     ;frames until the haunting starts (0 = started or none)
Global I2107Time#      ;frames of haunting left
Global I2107Next#      ;frames to the next event
Global Indev27Events%  ;for the room test

Function Indev2107Reset()
	I2107Cans = 0 : I2107Delay = 0 : I2107Time = 0 : I2107Next = 0
End Function

;drinking a can (Main.bb, the item-use code)
Function IndevUse2107(it.Items)
	If WearingGasMask > 0 Or WearingHazmat > 0 Then
		Msg = "You can't drink with your mask on." : MsgTimer = 70 * 4
		Return
	EndIf
	I2107Cans = I2107Cans + 1
	If I2107Time <= 0 And I2107Delay <= 0 Then I2107Delay = 70 * Rand(30, 60)
	I2107Time = I2107Time + 70 * Rand(120, 240)
	Stamina = Min(100, Stamina + 15)
	PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))
	If I2107Cans = 1 Then
		Msg = "You crack the can and drink. Diet cola, flat and very cold - colder than it was a moment ago."
	ElseIf I2107Cans = 2 Then
		Msg = "A second can. It tastes the same. The room feels a little more crowded."
	Else
		Msg = "Another one. The fizz sounds almost like whispering. Somewhere behind you, something exhales."
	EndIf
	MsgTimer = 70 * 6
	RemoveItem(it)
	SelectedItem = Null
End Function

;every frame (IndevHazards.bb): the countdown, then the haunting
Function UpdateIndev2107()
	Local n%, d.Doors, best.Doors, bd#, dd#
	If I2107Cans <= 0 Then Return
	If KillTimer < 0 Then
		Indev2107Reset()
		Return
	EndIf
	If I2107Delay > 0 Then
		I2107Delay = I2107Delay - FPSfactor
		If I2107Delay <= 0 Then
			I2107Delay = 0
			I2107Next = 70 * 3
			IndevStress = Min(100, IndevStress + 10)
			Msg = "The air turns cold around you. You hear your name, very quietly, from no direction at all." : MsgTimer = 70 * 6
		EndIf
		Return
	EndIf
	I2107Time = I2107Time - FPSfactor
	If I2107Time <= 0 Then
		Indev2107Reset()
		Msg = "The cold drains out of the air. Whatever was following you has let go - for now." : MsgTimer = 70 * 6
		Return
	EndIf
	I2107Next = I2107Next - FPSfactor
	If I2107Next > 0 Then Return
	;the more cans, the more often: 20-40 s with one, 7-13 s with three or more
	I2107Next = 70 * Rnd(20, 40) / Min(3, I2107Cans)
	Indev27Events = Indev27Events + 1
	n = Rand(1, 7 + (I2107Cans >= 3) * 2)
	Select n
		Case 1
			I2107Behind("SFX\Step\Step" + Rand(1, 8) + ".ogg", 0.8)
			If MsgTimer <= 0 Then Msg = "Footsteps, right behind you. They stop when you stop." : MsgTimer = 70 * 4
		Case 2
			I2107Behind("SFX\Indev\muffle.wav", 0.7)
			If MsgTimer <= 0 Then Msg = "Whispering, just too quiet to make out. It sounds pleased." : MsgTimer = 70 * 4
		Case 3
			I2107Behind("SFX\Indev\thump.wav", 0.9)
			If MsgTimer <= 0 Then Msg = "Three knocks on the wall beside you." : MsgTimer = 70 * 4
		Case 4
			LightBlink = Rnd(1.0, 2.0)
			I2107Behind("SFX\Indev\zap.wav", 0.4)
		Case 5
			;the nearest open door within six metres slams
			bd = 6.0 : best = Null
			For d = Each Doors
				If d\open And (Not d\locked) And d\IsElevatorDoor = 0 Then
					dd = EntityDistance(d\obj, Collider)
					If dd < bd Then bd = dd : best = d
				EndIf
			Next
			If best <> Null Then
				best\open = False ;IndevDoorCloseSound gives it the sound
				If MsgTimer <= 0 Then Msg = "A door slams shut. Nobody touched it." : MsgTimer = 70 * 4
			Else
				I2107Behind("SFX\Indev\creak.wav", 0.8)
			EndIf
		Case 6
			BlurTimer = Max(BlurTimer, 70 * 2)
			IndevStress = Min(100, IndevStress + 5)
			If MsgTimer <= 0 Then Msg = "Cold breath on the back of your neck." : MsgTimer = 70 * 4
		Case 7
			LightBlink = 1.0
			IndevStress = Min(100, IndevStress + 8)
			If MsgTimer <= 0 Then Msg = "Something pale stands at the edge of your sight. You turn. Nothing." : MsgTimer = 70 * 4
		Default
			;three cans or more: it can touch you now
			Injuries = Injuries + 0.25 * (I2107Cans - 1)
			CameraShake = Max(CameraShake, 1.2)
			PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage" + Rand(1, 4) + ".ogg"))
			If MsgTimer <= 0 Then Msg = "Something invisible shoves you hard. There are scratches on your arm that weren't there." : MsgTimer = 70 * 5
	End Select
End Function

;a sound a couple of metres behind the player
Function I2107Behind(file$, vol#)
	Local p% = CreatePivot()
	PositionEntity(p, EntityX(Collider), EntityY(Collider), EntityZ(Collider))
	RotateEntity(p, 0, EntityYaw(Camera) + 180 + Rnd(-40, 40), 0)
	MoveEntity(p, 0, 0, Rnd(1.5, 3.0))
	PlaySound2(LoadTempSound(file), Camera, p, 8.0, vol)
	FreeEntity(p)
End Function

Function IndevU27Dress(r.Rooms)
	If r\RoomTemplate\Name = "room2b27diet" Then IndevScpMesh(r, r\Objects[U27_DGT_VEND], "v2107") ;the vending machine (IndevScpProps.bb)
End Function

;the fridge (flag f) and the vending machine (flag v) each give one can
Function UpdateIndevU27(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U27_DGT_FRIDGE], 2.0) Then
		If IAxFlag(e, "f") Then
			Msg = "The CNSI unit is empty now, and cold enough to fog your breath." : MsgTimer = 70 * 4
		Else
			IAxSetFlag(e, "f")
			IS16Give("scp2107", r\Objects[U27_DGT_FRIDGE])
			Msg = "Inside the refrigerated unit, one can of Diet Ghost, beaded with frost. Trial stock." : MsgTimer = 70 * 5
		EndIf
	EndIf
	If IS10Press(r\Objects[U27_DGT_VEND], 2.5) Then
		IS10Sound("SFX\Indev\clicks.wav", r\Objects[U27_DGT_VEND], 6.0, 0.8)
		If IAxFlag(e, "v") Then
			Msg = "The vending machine hums. Every button is lit. None of them does anything." : MsgTimer = 70 * 4
		Else
			IAxSetFlag(e, "v")
			IS16Give("scp2107", r\Objects[U27_DGT_VEND])
			Msg = "You didn't put any money in. A can drops anyway: light blue, a cartoon ghost. YOUR OLD FAVORITE IS BACK!" : MsgTimer = 70 * 6
		EndIf
	EndIf
End Function
