;=====================================================================
; SCP: Containment Breach - Indev: sixth batch, seven rooms, thirteen SCPs
;
;   room2scps4      LCZ    Containment 4-L (rebuilt from the reference corridor shot)
;                          SCP-1079  bonbons: one is a nosebleed through the skin, four kill
;                          SCP-1916  moon rocks: each one changes what you weigh (stamina) for a while
;                          SCP-1200  gum: Lemons, Sunshine, Rubik's Cube or Moon's Shadow - you find out by chewing
;                                    SCP-1200-A stands in a glass case and watches
;                          SCP-971   hold the menu, use the phone: a meal turns up at your feet later
;   room2storage13  Indev  SCP-1080  the chamber, and its worker: call him over, lead him to the broken
;                                    tug, he fixes it and the pallet comes off the store door
;                          SCP-1081  the speaker's switch: SHUTDOWN takes your voice, REACTIVATE in time
;                          SCP-1082  a safe nobody may open
;                          SCP-1083  the quartz skull: months of argument, and you come back knowing a code
;   room2beefbelly  EZ     SCP-2789  staff serve you a meal; the free burger turns you into the next restaurant
;   room2grocery    Indev  SCP-3182  walk down Aisle 3 (or be there 19:52-20:52 by your clock): the Deimos Event
;   room2testhouse  EZ     SCP-1879  up a lift: a closet door knocks, a salesman steps out
;   room2nagasaki   HCZ    SCP-1145  down a lift: the lamps fail, the bear comes to you; hold it, reach the breaker
;   room2ltstorage  HCZ    SCP-1921  black floss, the calliope and its rolls; do not drink the Clown Milk
;
;   IndevS13Data.bb is generated (Tools\roomkit\gen_b6.py): the S13_* slot constants, FillRoom table,
;   fans, events. Shared helpers (IS16Aim, IS16Click, IS16Tell, IS16Person, IS16Give, IS16Prop ...)
;   are in IndevS16.bb. No globals: handles in r\Objects[] / r\RoomDoors[] / r\NPC[], progress in the
;   room's event (EventState / 2 / 3, flags and small counts as letters in EventStr).
;=====================================================================

;how many times a letter occurs in EventStr (small counters)
Function IS13Count%(e.Events, c$)
	Local n% = 0, i%
	For i = 1 To Len(e\EventStr)
		If Mid(e\EventStr, i, 1) = c Then n = n + 1
	Next
	Return n
End Function

Function IS13Drop(e.Events, c$)
	e\EventStr = Replace(e\EventStr, c, "")
End Function

Function IS13Gone(r.Rooms, k%)
	If r\NPC[k] <> Null Then
		RemoveNPC(r\NPC[k])
		r\NPC[k] = Null
	EndIf
End Function

Function IndevS13Dress(r.Rooms)
	Local m%
	Select r\RoomTemplate\Name
		Case "room2storage13"
			m = IS16Prop(r, "GFX\npcs\scp1080t.b3d", "GFX\map\indev_props4.png", r\Objects[S13_U13_CRATE], 90)
			r\Objects[S13_U13_CRATEM] = m
		Case "room2nagasaki"
			m = IS16Prop(r, "GFX\npcs\scp1145.b3d", "GFX\npcs\indev_teddy.png", r\Objects[S13_N45_TEDDY], 180)
			EntityPickMode(m, 2)
			r\Objects[S13_N45_TEDDYM] = m
	End Select
End Function

Function UpdateIndevS13(e.Events)
	Local r.Rooms = e\room
	If r\dist < 10.0 Then IndevS13Spin(r, 1.0)
	Select r\RoomTemplate\Name
		Case "room2scps4"
			UpdateS13Corridor(e)
		Case "room2storage13"
			UpdateS13Storage(e)
		Case "room2beefbelly"
			UpdateS13Beefbelly(e)
		Case "room2grocery"
			UpdateS13Grocery(e)
		Case "room2testhouse"
			UpdateS13House(e)
		Case "room2nagasaki"
			UpdateS13Nagasaki(e)
		Case "room2ltstorage"
			UpdateS13Kiosk(e)
	End Select
End Function

;=====================================================================
; room2scps4 - Containment 4-L
;   EventState  SCP-1200 Moon's Shadow bleed (time left)   EventState2 the SCP-1079 "sitting" (time left)
;   EventState3 the SCP-971 order on its way (time left)
;   flags: n SCP-1200-A placed, m menu in hand, o ordered, d delivered;
;   counts: b bonbons this sitting, r moon rocks eaten, g gum packs chewed.  NPC[0] SCP-1200-A
;=====================================================================

Function UpdateS13Corridor(e.Events)
	Local r.Rooms = e\room
	Local n%, it.Items, q$ = Chr(34)

	;---- what follows you out of the room
	If e\EventState > 0 And KillTimer >= 0 Then
		e\EventState = Max(0, e\EventState - FPSfactor)
		Injuries = Injuries + 0.00012 * FPSfactor
		DeathMSG = "Subject D-9341 died of blood loss with no wound to be found. A wrapper from SCP-1200-62 was in a pocket."
		If Rand(1400) = 1 And MsgTimer <= 0 Then IS16Tell("Your sleeve is wet with blood. There is no cut anywhere.", 6)
	EndIf
	If e\EventState2 > 0 Then
		e\EventState2 = Max(0, e\EventState2 - FPSfactor)
		If e\EventState2 = 0 Then IS13Drop(e, "b")
	EndIf
	If e\EventState3 > 0 And KillTimer >= 0 Then
		e\EventState3 = Max(0, e\EventState3 - FPSfactor)
		If e\EventState3 = 0 Then
			IAxSetFlag(e, "d")
			it = CreateItem("indevration", EntityX(Collider, True), EntityY(Collider, True) + 0.2, EntityZ(Collider, True))
			EntityType(it\collider, HIT_ITEM)
			IS16Tell("Something bumps your foot: a warm paper bag. QUIK 'N READY MEALZ. Nobody brought it.", 8)
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	;---- SCP-1200-A in its case
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S13_C4L_IRON, -90)
	EndIf
	If r\NPC[0] <> Null Then
		IAxSkin(r\NPC[0], "GFX\npcs\indev_paintiron.jpg")
		If EntityDistance(r\NPC[0]\Collider, Collider) < 5.0 Then IAxFace(r\NPC[0], Collider)
	EndIf

	;---- SCP-1079
	If IS16Click(r\Objects[S13_C4L_BONBON], r\Objects[S13_C4L_BONBON], 1.3) Then
		n = IS13Count(e, "b") + 1
		e\EventStr = e\EventStr + "b"
		e\EventState2 = 70 * 120
		PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
		Select n
			Case 1
				Injuries = Injuries + 0.05
				IS16Tell("It tingles. Then pink foam that smells of bubblegum comes out of the skin of your arms. It is your blood.", 8)
			Case 2
				Injuries = Injuries + 0.45
				Bloodloss = Min(100, Bloodloss + 10)
				IS16Tell("More foam, much more. It is coming from your back and your stomach. You feel light-headed.", 8)
			Case 3
				Injuries = Injuries + 1.2
				Bloodloss = Min(100, Bloodloss + 30)
				BlurTimer = 800
				IS16Tell("Your blood fizzes. You are standing in a pink puddle and it is all you.", 8)
			Default
				DeathMSG = "Subject D-9341 was found in Containment 4-L in a large quantity of pink foam. Cause of death: exsanguination. Four SCP-1079 wrappers were recovered."
				Kill()
		End Select
	EndIf

	;---- SCP-1916
	If IS16Click(r\Objects[S13_C4L_MOONROCKS], r\Objects[S13_C4L_MOONROCKS], 1.3) Then
		If IS13Count(e, "r") >= 6 Then
			IS16Tell("The tray is empty.", 4)
		ElseIf StaminaEffectTimer > 0 Then
			e\EventStr = e\EventStr + "r"
			Injuries = Injuries + 0.8
			CameraShake = 4.0
			BlurTimer = 900
			IS16Tell("One every four hours, the box said. Your inner ear gives up and you hit the floor.", 7)
		Else
			e\EventStr = e\EventStr + "r"
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			Select Rand(6)
				Case 1
					StaminaEffect = 0.5 : StaminaEffectTimer = 90
					IS16Tell("Martian Cherry. You feel light on your feet, about a third lighter.", 6)
				Case 2
					StaminaEffect = 1.6 : StaminaEffectTimer = 60
					BlurTimer = 300
					IS16Tell("Venusian Berry. The air feels as thick as water.", 6)
				Case 3
					StaminaEffect = 0.15 : StaminaEffectTimer = 90
					IS16Tell("Lunar Lime. One-sixth of your weight. You could run forever.", 6)
				Case 4
					StaminaEffect = 3.0 : StaminaEffectTimer = 60
					Stamina = 0
					CameraShake = 2.0
					IS16Tell("Jovian Jelly. Your knees nearly fold. Standing is work.", 6)
				Case 5
					StaminaEffect = 0.1 : StaminaEffectTimer = 60
					Injuries = Injuries + 0.6
					CameraShake = 4.0
					IS16Tell("Outer Space Strawberry. You drift up and hit the ceiling, hard, then come down slowly.", 7)
				Default
					StaminaEffect = 1.2 : StaminaEffectTimer = 30
					BlinkTimer = -10
					BlurTimer = 1000
					Injuries = Injuries + 0.4
					IndevStress = Min(100, IndevStress + 30)
					IS16Tell("Planet X. For a moment you weigh nothing and everything at once.", 7)
			End Select
		EndIf
	EndIf

	;---- SCP-1200
	If IS16Click(r\Objects[S13_C4L_GUM], r\Objects[S13_C4L_GUM], 1.3) Then
		If IS13Count(e, "g") >= 3 Then
			IS16Tell("No packs left.", 4)
		Else
			e\EventStr = e\EventStr + "g"
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IndevStress = Min(100, IndevStress + 3)
			Select Rand(4)
				Case 1
					IS16Tell("Tastes Like Lemons. It does. Everything will, for a day.", 6)
				Case 2
					LightFlash = 1.5
					IndevRelieveStress(15)
					IS16Tell("Tastes Like Sunshine. You glow, white and warm, and for a while nothing is dark.", 7)
				Case 3
					BlurTimer = 700
					CameraShake = 3.0
					Stamina = 0
					Injuries = Injuries + 0.3
					IS16Tell("Tastes Like Rubik's Cube. Your left hand is where your right was. You put it back. Mostly.", 8)
				Default
					e\EventState = 70 * 120
					IS16Tell("Tastes Like Moon's Shadow. Nothing happens. Then something pale with long ears goes into your chest.", 8)
			End Select
		EndIf
	EndIf

	;---- SCP-971
	If IS16Click(r\Objects[S13_C4L_MENU], r\Objects[S13_C4L_MENU], 1.2) Then
		If Not IAxFlag(e, "m") Then
			IAxSetFlag(e, "m")
			IS16Tell("You pick up the menu. QUIK 'N READY MEALZ, and a phone number.", 5)
		Else
			IS16Tell("You already have the menu in your hand.", 4)
		EndIf
	EndIf
	If IS16Click(r\Objects[S13_C4L_PHONE], r\Objects[S13_C4L_PHONE], 1.2) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If IAxFlag(e, "o") Then
			IS16Tell("The number is a software help desk again. Your order is already on its way.", 6)
		ElseIf Not IAxFlag(e, "m") Then
			IS16Tell("A software help desk. " + q + "Have you tried turning it off and on?" + q + " You need the menu in your hand.", 7)
		Else
			IAxSetFlag(e, "o")
			e\EventState3 = 70 * 75
			IS16Tell("A recorded voice takes A1 and C1, reads back a card number you don't have, and thanks you.", 8)
		EndIf
	EndIf
End Function

;=====================================================================
; room2storage13 - Storage Unit 13
;   EventState  the worker: 0 at his post, 1 following you, 2 fixing the tug, 3 done
;   EventState2 how long you have been without a voice (SCP-1081)
;   EventState3 fixing time, then how far the pallet has moved (0..1)
;   flags: n worker placed, a no voice, x no voice for good, k held the skull;
;   count: p clicks of the SCP-1081 switch (position = count Mod 4).  NPC[0] the worker
;=====================================================================

Function UpdateS13Storage(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, d#, dx#, dz#, pos%, t#
	Local door.Doors = r\RoomDoors[S13_U13_D_CLOSET]
	Local crate% = r\Objects[S13_U13_CRATEM]
	Local q$ = Chr(34)

	;---- SCP-1081: the silence goes where you go
	If IAxFlag(e, "a") And KillTimer >= 0 Then
		e\EventState2 = e\EventState2 + FPSfactor
		IndevStress = Min(100, IndevStress + 0.004 * FPSfactor)
		If Rand(1600) = 1 And MsgTimer <= 0 Then IS16Tell("You try to swear. Nothing comes. Not even a gesture.", 5)
		If e\EventState2 > 70 * 180 Then
			IS13Drop(e, "a")
			IAxSetFlag(e, "x")
			IndevStress = Min(100, IndevStress + 25)
			IS16Tell("Somewhere in the last minute the silence set. It is not coming back.", 7)
		EndIf
	EndIf

	;the pallet stays where it was put
	If e\EventState = 3 And crate <> 0 Then
		If e\EventState3 < 1.0 Then e\EventState3 = Min(1.0, e\EventState3 + FPSfactor / (70 * 3.0))
		t = e\EventState3
		PositionEntity(crate, EntityX(r\Objects[S13_U13_CRATE], True) * (1 - t) + EntityX(r\Objects[S13_U13_CRATE2], True) * t, EntityY(r\Objects[S13_U13_CRATE], True), EntityZ(r\Objects[S13_U13_CRATE], True) * (1 - t) + EntityZ(r\Objects[S13_U13_CRATE2], True) * t, True)
		If t >= 1.0 And door\locked Then
			door\locked = False
			door\open = True
		EndIf
	Else
		door\locked = True
	EndIf

	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	;---- SCP-1080-1, the worker
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S13_U13_WORKER, 90)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_tech.jpg")
		Select e\EventState
			Case 0
				n\State = 0
				If IndevAimedAt(n\obj, n\Collider, 1.6) Then
					DrawHandIcon = True
					If MouseHit1 Then
						MouseHit1 = False
						e\EventState = 1
						IS16Tell("You read the number off the back of his hand and say: come here. He comes.", 6)
					EndIf
				EndIf
			Case 1
				d = EntityDistance(n\Collider, Collider)
				dx = EntityX(Collider) - EntityX(n\Collider)
				dz = EntityZ(Collider) - EntityZ(n\Collider)
				RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 10.0), 0)
				If d > 1.3 Then
					n\State = 1
				Else
					n\State = 0
				EndIf
				If IS16Click(r\Objects[S13_U13_TUG], r\Objects[S13_U13_TUG], 1.5) Then
					If EntityDistance(n\Collider, r\Objects[S13_U13_TUG]) < 2.2 Then
						e\EventState = 2
						e\EventState3 = 0
						n\State = 0
						IS16Tell("You point at the tug: fix this. He kneels by it and starts taking it apart.", 6)
					Else
						IS16Tell("He is too far away to see what you mean.", 4)
					EndIf
				ElseIf IndevAimedAt(n\obj, n\Collider, 1.6) Then
					DrawHandIcon = True
					If MouseHit1 Then
						MouseHit1 = False
						e\EventState = 0
						PositionEntity(n\Collider, EntityX(r\Objects[S13_U13_WORKER], True), EntityY(r\Objects[S13_U13_WORKER], True) + 0.5, EntityZ(r\Objects[S13_U13_WORKER], True))
						ResetEntity(n\Collider)
						IS16Tell("You say: leave. He goes back to his place by the chamber and stands there.", 5)
					EndIf
				EndIf
			Case 2
				n\State = 0
				IAxFace(n, r\Objects[S13_U13_TUG])
				e\EventState3 = e\EventState3 + FPSfactor
				If e\EventState3 > 70 * 6 Then
					e\EventState = 3
					e\EventState3 = 0
					PlaySound_Strict(LoadTempSound("SFX\General\GeneratorOn.ogg"))
					IS16Tell("The tug starts, sweeter than new. He drives it to the store door and lifts the pallet clear.", 7)
				EndIf
			Default
				n\State = 0
		End Select
	EndIf

	;---- SCP-1080, the chamber
	If IS16Click(r\Objects[S13_U13_TANK], r\Objects[S13_U13_TANK], 1.3) Then
		IS16Tell("The lid will not move. It only locks itself for children.", 5)
	EndIf

	;---- SCP-1081
	If IS16Click(r\Objects[S13_U13_SPEAKER], r\Objects[S13_U13_SPEAKER], 1.3) Then
		e\EventStr = e\EventStr + "p"
		pos = IS13Count(e, "p") Mod 4
		PlaySound_Strict(LoadTempSound("SFX\Interact\LeverFlip.ogg"))
		Select pos
			Case 1
				IS16Tell("The switch clicks to ACTIVE. A faint hiss from the little black figure.", 5)
			Case 2
				PlaySound_Strict(LoadTempSound("SFX\Radio\squelch.ogg"))
				If IAxFlag(e, "x") Then
					IS16Tell("SHUTDOWN. A whistle, and a welcome in no language you know. You have nothing left for it to take.", 7)
				Else
					IAxSetFlag(e, "a")
					e\EventState2 = 0
					IndevStress = Min(100, IndevStress + 10)
					IS16Tell("SHUTDOWN. A bosun's whistle, then: " + q + "Please refrain from talking during the performance." + q + " You can't.", 8)
				EndIf
			Case 3
				PlaySound_Strict(LoadTempSound("SFX\Radio\squelch.ogg"))
				If IAxFlag(e, "a") Then
					IS13Drop(e, "a")
					IndevRelieveStress(10)
					IS16Tell("REACTIVATE. " + q + "Thank you for your consideration. The show is now at a conclusion." + q + " You can speak.", 8)
				Else
					IS16Tell("REACTIVATE. The little figure thanks you for your attention.", 5)
				EndIf
			Default
				IS16Tell("The switch clicks back to INACTIVE.", 4)
		End Select
	EndIf

	;---- SCP-1082
	If IS16Click(r\Objects[S13_U13_SAFE], r\Objects[S13_U13_SAFE], 1.4) Then
		IS16Tell("Three dials, three locks. You have none of the combinations, and you are glad.", 5)
	EndIf

	;---- SCP-1083
	If IS16Click(r\Objects[S13_U13_SKULL], r\Objects[S13_U13_SKULL], 1.3) Then
		BlinkTimer = -10
		If Not IAxFlag(e, "k") Then
			IAxSetFlag(e, "k")
			BlurTimer = 900
			IndevStress = Min(100, IndevStress + 35)
			IS16Tell("A voice argues with you for what feels like months. You come back knowing the office keypad code: " + AccessCode + ".", 12)
		Else
			Injuries = Injuries + 1.0
			IndevStress = Min(100, IndevStress + 20)
			IS16Tell(q + "You came back." + q + " He shows you everything you have done. When it ends your hands are bleeding.", 9)
		EndIf
	EndIf
End Function

;=====================================================================
; room2beefbelly - SCP-2789
;   EventState3 the special working on you (time left)
;   flags: n staff placed, o served, w warned about the special, e ate it, c given the card
;   NPC[0..2] staff, NPC[3] SCP-2789-1
;=====================================================================

Function UpdateS13Beefbelly(e.Events)
	Local r.Rooms = e\room
	Local i%, n.NPCs, d#, q$ = Chr(34)

	;---- the special, wherever you are
	If IAxFlag(e, "e") And KillTimer >= 0 Then
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 < 70 * 100 And e\EventState3 + FPSfactor >= 70 * 100 Then
			IS16Tell("Your chest is tight. You want to be somewhere else. A big city, with no Beefbelly Bill's.", 7)
		EndIf
		If e\EventState3 < 70 * 60 Then
			Stamina = Min(Stamina, 40)
			If Rand(300) = 1 Then CameraShake = 2.0
		EndIf
		If e\EventState3 < 70 * 25 Then
			BlurTimer = Max(BlurTimer, 400)
			Injuries = Injuries + 0.0008 * FPSfactor
		EndIf
		If e\EventState3 <= 0 Then
			DeathMSG = "Subject D-9341's remains were not recovered. Three weeks later a Beefbelly Bill's opened two levels below the Indev zone. MTF Xi-17 has been informed."
			Kill()
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		For i = 0 To 2
			r\NPC[i] = IS16Person(r, S13_BB_STAFF0 + i, -90)
		Next
		r\NPC[3] = IS16Person(r, S13_BB_CEO, 90)
	EndIf
	For i = 0 To 2
		If r\NPC[i] <> Null Then
			IAxSkin(r\NPC[i], "GFX\npcs\indev_bbstaff.jpg")
			If EntityDistance(r\NPC[i]\Collider, Collider) < 4.0 Then IAxFace(r\NPC[i], Collider)
		EndIf
	Next
	n = r\NPC[3]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_ceo.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 5.0 Then IAxFace(n, Collider)
		If d < 2.2 And (Not IAxFlag(e, "c")) And MsgTimer <= 0 Then
			IAxSetFlag(e, "c")
			IS16Give("doc2789b", r\Objects[S13_BB_CEO])
			IAxSay("Bill", "Welcome, welcome! How would you make the menu better? Here, take my card.", 7)
		ElseIf d < 2.4 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Bill", "Did you try the special? Everybody should try the special.", 6)
				Case 2
					IAxSay("Bill", "Thirty lucky customers a year. You have a lucky face.", 6)
				Case 3
					IAxSay("Bill", "This building has lovely plumbing. It was very easy to move in.", 6)
			End Select
		EndIf
	EndIf

	If IS16Click(r\Objects[S13_BB_BELL], r\Objects[S13_BB_BELL], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If Not IAxFlag(e, "o") Then
			IAxSetFlag(e, "o")
			IS16Give("indevration", r\Objects[S13_BB_BELL])
			IAxSay("Staff", "One Bill Burger. And today we have a special offer for you.", 6)
		Else
			IAxSay("Staff", "Have you seen our special offer? It is free.", 5)
		EndIf
	EndIf

	If IS16Click(r\Objects[S13_BB_BURGER], r\Objects[S13_BB_BURGER], 1.3) Then
		If IAxFlag(e, "e") Then
			IS16Tell("You have already had the special.", 4)
		ElseIf Not IAxFlag(e, "w") Then
			IAxSetFlag(e, "w")
			IS16Tell("TODAY ONLY - FREE BURGER. It smells better than anything you have ever eaten. Click again to eat it.", 7)
		Else
			IAxSetFlag(e, "e")
			e\EventState3 = 70 * 150
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IAxSay("Staff", "Thank you for choosing Beefbelly Bill's.", 5)
		EndIf
	EndIf
End Function

;=====================================================================
; room2grocery - SCP-3182
;   EventState  0 quiet, 1 a Deimos Event is running   EventState2 how long it has run
;   EventState3 quiet time before the clock can start another
;   flags: f the first one has happened.  NPC[0..2] the shapes in the aisles
;=====================================================================

Function UpdateS13Grocery(e.Events)
	Local r.Rooms = e\room
	Local i%, lx#, lz#, inaisle%, instore%, hm$, door.Doors = r\RoomDoors[S13_GRO_D_STORE]
	Local prev#

	If e\EventState3 > 0 Then e\EventState3 = Max(0, e\EventState3 - FPSfactor)
	If PlayerRoom <> r Then
		If e\EventState = 1 Then IS13EndDeimos(e)
		Return
	EndIf
	If KillTimer < 0 Then Return

	IAxLocal(r)
	lx = TFormedX()
	lz = TFormedZ()
	instore = (lx < -256.0)
	inaisle = (lx > -900.0 And lx < -440.0 And lz > -80.0 And lz < 140.0)

	If e\EventState = 0 Then
		hm = Left(CurrentTime(), 5)
		If instore And ((inaisle And (Not IAxFlag(e, "f"))) Or (e\EventState3 <= 0 And hm >= "19:52" And hm < "20:52")) Then
			e\EventState = 1
			e\EventState2 = 0
			door\open = False
			door\locked = True
			LightBlink = 2.0
			PlaySound_Strict(LoadTempSound("SFX\Room\Blackout.ogg"))
			For i = 0 To 2
				r\NPC[i] = IS16Person(r, S13_GRO_FIG0 + i, 0)
			Next
			IS16Tell("The lights go. The door you came in by is not there any more.", 6)
		EndIf
		Return
	EndIf

	;---- a Deimos Event
	prev = e\EventState2
	e\EventState2 = e\EventState2 + FPSfactor
	SecondaryLightOn = CurveValue(0.15, SecondaryLightOn, 15.0)
	door\locked = True
	IndevStress = Min(100, IndevStress + 0.02 * FPSfactor)
	For i = 0 To 2
		If r\NPC[i] <> Null Then
			IAxSkin(r\NPC[i], "GFX\npcs\indev_flat_black.jpg")
			IAxFace(r\NPC[i], Collider)
		EndIf
	Next
	If prev < 70 * 8 And e\EventState2 >= 70 * 8 Then IS16Tell("You remember buying bread here every Friday for thirty years. You have never been to Missouri.", 8)
	If prev < 70 * 16 And e\EventState2 >= 70 * 16 Then IS16Tell("Grief, all at once, for a town you don't know. Something is coming to it.", 7)
	If Rand(400) = 1 Then PlaySound2(LoadTempSound("SFX\SCP\173\StoneDrag.ogg"), Camera, r\Objects[S13_GRO_AISLE3], 10.0)
	If Rand(500) = 1 Then PlaySound2(LoadTempSound("SFX\Horror\Horror" + Rand(0, 16) + ".ogg"), Camera, r\Objects[S13_GRO_AISLE3], 10.0, 0.6)
	If prev < 70 * 30 And e\EventState2 >= 70 * 30 Then
		PlaySound2(LoadTempSound("SFX\SCP\106\Corrosion1.ogg"), Camera, r\Objects[S13_GRO_AISLE3], 12.0)
		IS16Tell("A soft gurgling, from Aisle 3.", 5)
	EndIf
	If e\EventState2 > 70 * 33 And e\EventState2 < 70 * 41 And inaisle Then
		Injuries = Injuries + 0.006 * FPSfactor
		CameraShake = Max(CameraShake, 2.0)
		DeathMSG = "Subject D-9341 was found in the Aisle 3 fixtures of SCP-3182 after a Deimos Event. The injuries match no known cause. The shelves were undisturbed."
	EndIf
	If e\EventState2 > 70 * 45 Then
		IS13EndDeimos(e)
		IS16Tell("The lights come back. The door is where it always was.", 6)
	EndIf
End Function

Function IS13EndDeimos(e.Events)
	Local r.Rooms = e\room, i%
	e\EventState = 0
	e\EventState3 = 70 * 600
	IAxSetFlag(e, "f")
	SecondaryLightOn = 1.0
	r\RoomDoors[S13_GRO_D_STORE]\locked = False
	For i = 0 To 2
		IS13Gone(r, i)
	Next
End Function

;=====================================================================
; room2testhouse - SCP-1879
;   EventState  0 quiet, 1 knocking, 2 he is out and selling, 3 you bought, 4 he gave up
;   EventState2 the lift      EventState3 time (between knocks / how long he has been pitching)
;   count: v visits refused (the knocking door is visit Mod 3).  NPC[0] SCP-1879-2
;=====================================================================

Function UpdateS13House(e.Events)
	Local r.Rooms = e\room
	Local v%, k%, d#, n.NPCs, door.Doors, q$ = Chr(34), m#, item$, price$, line$

	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return
	If e\EventState >= 3 Then Return

	v = IS13Count(e, "v")
	k = v Mod 3
	door = r\RoomDoors[S13_TH_D_DOOR0 + k]
	m = 1.0 + v * 0.6
	Select (v * 7) Mod 4
		Case 0
			item = "firstaid" : price = "All I'm asking for is a little blood."
		Case 1
			item = "bat" : price = "Gimme some sugar, that's all."
		Case 2
			item = "key3" : price = "I want your soul. Just a bit of it."
		Default
			item = "nvgoggles" : price = "Just your eyes. For a second."
	End Select
	IAxLocal(r)
	If TFormedY() < 500.0 Then Return

	Select e\EventState
		Case 0, 1
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
			If door\open Then
				;he was waiting behind it
				e\EventState = 2
				e\EventState3 = 0
				n = IS16Person(r, S13_TH_SPOT0 + k, 0)
				r\NPC[0] = n
				IS16Tell("A man in a brown suit steps out of the closet, smiling, already talking.", 6)
			ElseIf EntityDistance(Collider, r\Objects[S13_TH_SPOT0 + k]) < 2.5 And e\EventState3 <= 0 Then
				e\EventState3 = 70 * 1.6
				PlaySound2(LoadTempSound("SFX\Door\WoodenDoorBudge.ogg"), Camera, r\Objects[S13_TH_SPOT0 + k], 8.0)
				If e\EventState = 0 Then
					e\EventState = 1
					IS16Tell("Somebody is knocking on the closet door. From the inside.", 5)
				EndIf
			EndIf

		Case 2
			n = r\NPC[0]
			If n = Null Then
				e\EventState = 0
				Return
			EndIf
			IAxSkin(n, "GFX\npcs\indev_salesman.jpg")
			IAxFace(n, Collider)
			e\EventState3 = e\EventState3 + FPSfactor
			d = EntityDistance(n\Collider, Collider)
			If MsgTimer <= 0 Then
				Select Rand(3)
					Case 1
						line = "Let me tell you about this, friend - the best one you'll ever own."
					Case 2
						line = "Sit down, sit down. Price? " + price
					Default
						line = "Don't walk away from a deal like this. " + price
				End Select
				If v = 2 Then line = "Last time I'm asking nice. " + price
				IAxSay("Salesman", line, 6)
			EndIf
			If IndevAimedAt(n\obj, n\Collider, 1.5) Then
				DrawHandIcon = True
				If MouseHit1 Then
					MouseHit1 = False
					IS16Give(item, n\Collider)
					Select item
						Case "firstaid"
							Injuries = Injuries + 0.5 * m
						Case "bat"
							Stamina = 0
							StaminaEffect = 1.5 * m : StaminaEffectTimer = 120
						Case "key3"
							IndevStress = Min(100, IndevStress + 30 * m)
							BlurTimer = 600
						Default
							BlinkTimer = -10
							BlurTimer = 1200 * m
					End Select
					IAxSay("Salesman", "Pleasure doing business! You won't regret it. Probably.", 6)
					IS13Gone(r, 0)
					door\open = False
					e\EventState = 3
					Return
				EndIf
			EndIf
			If d > 4.0 Or e\EventState3 > 70 * 30 Then
				IS13Gone(r, 0)
				door\open = False
				e\EventStr = e\EventStr + "v"
				If v >= 2 Then
					Injuries = Injuries + 0.8
					CameraShake = 4.0
					e\EventState = 4
					IS16Tell("He hits you, hard, out of nowhere, and is gone. The knocking stops for good.", 7)
				Else
					e\EventState = 0
					e\EventState3 = 70 * 20
					IAxSay("Salesman", "Your loss. I'll be back - and the price goes up.", 6)
				EndIf
			EndIf
	End Select
End Function

;=====================================================================
; room2nagasaki - SCP-1145
;   EventState  0 lamps on, 1 lamps out, 2 lamps back on (over)   EventState2 the lift
;   EventState3 how long it has been dark (the bear moves after 3 s; the dose climbs every 30 s)
;   flags: n Class-D placed, h holding the bear, b the bear went to a Class-D.  NPC[0..1] the Class-D
;=====================================================================

Function UpdateS13Nagasaki(e.Events)
	Local r.Rooms = e\room
	Local teddy% = r\Objects[S13_N45_TEDDYM], lvr% = r\Objects[S13_N45_LEVER + 1]
	Local i%, n.NPCs, up%, lx#, dp#, dd#, fx#, fz#, l#, q$ = Chr(34)

	If PlayerRoom <> r Then
		If e\EventState = 1 Then
			;the dark stays down there; the bear is back in the dark water
			SecondaryLightOn = 1.0
			IS13Drop(e, "h")
			IS13Drop(e, "b")
			e\EventState3 = 0
			If teddy <> 0 Then
				EntityParent(teddy, r\obj)
				PositionEntity(teddy, EntityX(r\Objects[S13_N45_TEDDY], True), EntityY(r\Objects[S13_N45_TEDDY], True), EntityZ(r\Objects[S13_N45_TEDDY], True), True)
			EndIf
			IS16Hush(e)
		EndIf
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S13_N45_DCLASS0, 180)
		r\NPC[1] = IS16Person(r, S13_N45_DCLASS1, 0)
	EndIf
	For i = 0 To 1
		n = r\NPC[i]
		If n <> Null Then
			If EntityDistance(n\Collider, Collider) < 5.0 Then IAxFace(n, Collider)
			If EntityDistance(n\Collider, Collider) < 3.0 And MsgTimer <= 0 And Rand(700) = 1 Then
				Select Rand(3)
					Case 1
						IAxSay("Class-D", "They keep us down here in case it wakes up. So it has somebody to go to.", 7)
					Case 2
						IAxSay("Class-D", "If the lights go, it goes to whoever's nearest. Stay away from the tank.", 7)
					Case 3
						IAxSay("Class-D", "Breaker's on the far wall. Push it up. Don't stand there thinking.", 6)
				End Select
			EndIf
		EndIf
	Next

	IAxLocal(r)
	lx = TFormedX()
	up = UpdateLever(lvr)

	Select e\EventState
		Case 0
			;the breaker trips the first time somebody walks out into the chamber (or pulls it)
			If (TFormedY() < -400.0 And lx > 150.0) Or (Not up) Then
				e\EventState = 1
				e\EventState3 = 0
				RotateEntity(lvr, -80, EntityYaw(lvr), 0)
				LightBlink = 3.0
				PlaySound_Strict(LoadTempSound("SFX\Room\Blackout.ogg"))
				IS16Tell("The breaker trips. Eight lamps go out at once. Only the water still glows, faintly.", 7)
			EndIf

		Case 1
			SecondaryLightOn = CurveValue(0.12, SecondaryLightOn, 12.0)
			e\EventState3 = e\EventState3 + FPSfactor
			If e\EventState3 > 70 * 3 And teddy <> 0 And (Not IAxFlag(e, "h")) And (Not IAxFlag(e, "b")) Then
				;it goes to whoever is nearest the tank
				dp = EntityDistance(Collider, r\Objects[S13_N45_TEDDY])
				dd = 999.0
				If r\NPC[0] <> Null Then dd = EntityDistance(r\NPC[0]\Collider, r\Objects[S13_N45_TEDDY])
				If dd < dp And e\EventState3 < 70 * 3 + FPSfactor * 2 Then
					IAxSetFlag(e, "b")
					PositionEntity(teddy, EntityX(r\NPC[0]\Collider, True), EntityY(r\NPC[0]\Collider, True) - 0.2, EntityZ(r\NPC[0]\Collider, True), True)
					IS16Tell("In the cell by the north wall a man starts screaming, then goes quiet, holding something.", 7)
				Else
					;within a metre of you, wherever you go
					TFormVector(0, 0, 1, Camera, 0)
					fx = TFormedX()
					fz = TFormedZ()
					l = Sqr(fx * fx + fz * fz)
					If l > 0.01 Then
						fx = fx / l
						fz = fz / l
					EndIf
					If EntityDistance(teddy, Collider) > 1.3 Then
						If e\EventState3 < 70 * 3 + FPSfactor * 2 Then IS16Tell("The bear is gone from the tank. It is sitting at your feet.", 6)
						PositionEntity(teddy, EntityX(Collider, True) + fx * 0.9, EntityY(Collider, True) - 0.25, EntityZ(Collider, True) + fz * 0.9, True)
						RotateEntity(teddy, 0, VectorYaw(-fx, 0, -fz), 0, True)
					EndIf
					;the dose climbs every half minute until you pick it up
					Injuries = Injuries + 0.0006 * (1 + Floor((e\EventState3 - 70 * 3) / (70 * 30))) * FPSfactor
					BlurTimer = Max(BlurTimer, 300)
					DeathMSG = "Subject D-9341 died of acute radiation syndrome in Chamber 1145. SCP-1145 was found within one metre of the body."
					If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Radio\static.ogg")
					e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, teddy, 4.0, 0.8)
					If IS16Click(teddy, teddy, 1.6) Then
						IAxSetFlag(e, "h")
						EntityParent(teddy, Camera)
						PositionEntity(teddy, 0.16, -0.24, 0.42)
						RotateEntity(teddy, 0, 180, 0)
						IS16Tell("You pick it up. It is heavy, and warm, and the crackle drops to a murmur. Now the breaker.", 7)
					EndIf
				EndIf
			EndIf
			If IAxFlag(e, "h") Then
				If e\Sound <> 0 Then e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, Collider, 2.0, 0.2)
			EndIf
			If up Then
				;light again: it is only a bear
				e\EventState = 2
				SecondaryLightOn = 1.0
				IS16Hush(e)
				If IAxFlag(e, "h") Then
					EntityParent(teddy, r\obj)
					PositionEntity(teddy, EntityX(Collider, True), EntityY(Collider, True) - 0.25, EntityZ(Collider, True), True)
					RotateEntity(teddy, 0, EntityYaw(Collider, True), 0, True)
					IS13Drop(e, "h")
				EndIf
				IS16Tell("The lamps come back. You set the bear down in the light. It is only a bear.", 7)
			EndIf

		Default
			If SecondaryLightOn < 0.995 Then SecondaryLightOn = CurveValue(1.0, SecondaryLightOn, 20.0)
	End Select
End Function

;=====================================================================
; room2ltstorage - SCP-1921
;   EventState  the calliope playing (time left)   EventState2 The Skater's Waltz in your head (time left)
;   flags: a ate the floss, k a cup of Clown Milk in your hand; count: r rolls played
;=====================================================================

Function UpdateS13Kiosk(e.Events)
	Local r.Rooms = e\room
	Local roll%

	If e\EventState2 > 0 And KillTimer >= 0 Then
		e\EventState2 = Max(0, e\EventState2 - FPSfactor)
		IndevRelieveStress(0.05 * FPSfactor)
	EndIf
	If e\EventState > 0 Then e\EventState = Max(0, e\EventState - FPSfactor)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If IS16Click(r\Objects[S13_LT6_SPINNER], r\Objects[S13_LT6_SPINNER], 1.4) Then
		If IAxFlag(e, "a") Then
			IS16Tell("You've had yours. The floss in the bowl is black and very still.", 5)
		Else
			IAxSetFlag(e, "a")
			IS16Tell("The black floss shrinks to nothing on your tongue. A tickle, somewhere behind the eyes.", 7)
		EndIf
	EndIf

	If IS16Click(r\Objects[S13_LT6_CALLIOPE], r\Objects[S13_LT6_CALLIOPE], 1.4) Then
		If e\EventState > 0 Then
			IS16Tell("The calliope is still wheezing to a stop.", 4)
		Else
			e\EventState = 70 * 40
			roll = IS13Count(e, "r") Mod 3
			e\EventStr = e\EventStr + "r"
			PlaySound_Strict(LoadTempSound("SFX\Interact\LeverFlip.ogg"))
			If Not IAxFlag(e, "a") Then
				Select roll
					Case 0
						IS16Tell("The calliope wheezes into The Skater's Waltz. It sounds far away and in the room at once.", 7)
					Case 1
						IS16Tell("The calliope plays When You're Smiling, a little too slowly.", 6)
					Default
						IS16Tell("The calliope plays Officer of the Year. Nothing else happens. Should it?", 6)
				End Select
			Else
				Select roll
					Case 0
						e\EventState2 = 70 * 120
						IS16Tell("The Skater's Waltz. Suddenly none of this seems strange. Of course there is a bear in Nagasaki.", 8)
					Case 1
						IndevStress = 0
						BlurTimer = 500
						IS16Tell("When You're Smiling. You can't think of anything bad. You can't think of much at all.", 8)
					Default
						IS16Tell("Officer of the Year. Nothing anyone here does could be wrong. That is all it does to you.", 7)
				End Select
			EndIf
		EndIf
	EndIf

	If IS16Aim(r\Objects[S13_LT6_MILK], 1.2, 0.96) Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			If IAxFlag(e, "k") Then
				DeathMSG = "Subject D-9341 was found beside SCP-1921 with black fluid around the mouth. Cause of death: cardiac arrest. Serotonin levels were off the scale."
				IS16Tell("It tastes of nothing. Then you are happier than you have ever been, all at once, and your heart stops.", 8)
				Kill()
			Else
				IAxSetFlag(e, "k")
				IS16Tell("CLOWN MILK. Black, thick, warm. You hold a cupful. Click again to drink.", 6)
			EndIf
		EndIf
	ElseIf IAxFlag(e, "k") Then
		IS13Drop(e, "k")
		IS16Tell("You pour it back.", 3)
	EndIf
End Function
