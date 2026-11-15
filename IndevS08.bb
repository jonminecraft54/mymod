;=====================================================================
; SCP: Containment Breach - Indev: eighth batch, five rooms, eight SCPs
;
;   room2yule       LCZ    Containment 4-Y (the reference corridor a third time), four cells:
;                          SCP-2983  pour the milk and the marshmallows sing; the box has a prize code; the
;                                    vendor terminal is still logged in, and prizes land in your lap
;                          SCP-1933  a drunk Santa and his wrapped bottle: one sip is fine, more is a gamble
;                          SCP-1225  the ornament is on the tree again: everything closed near it rots. Box it
;                                    before the supply locker is ruined
;                          SCP-6895  MTF Kappa-31's staging room - and Sir Nicholas himself, who turns up
;                                    anywhere in the facility when you are badly hurt, with a present
;   room2pinata     Indev  SCP-956   it walks the edge of its cell and stares at one wall. The candy (SCP-956-1)
;                                    is in the cold store: eat it and one in three survive. The incinerator
;   room2demoncore  HCZ    SCP-095-FR down a lift: flux peaks every few minutes (get in the control room and
;                                    shut the door), electronics die, and do not touch the bench
;   room2argos      Indev  SCP-3355  St. Nick's Workshop, and the Argos bunker below: talk to Nick, patiently,
;                                    and a package comes down the chute for you
;   room2chrono     HCZ    SCP-4255  the replica sleigh and its reindeer on the launch deck (lift up); versions
;                                    of him turn up, give you what you need, and are gone
;
;   IndevS08Data.bb is generated (Tools\roomkit\gen_b8.py). Helpers come from IndevS10.bb / IndevS16.bb /
;   IndevS13.bb / IndevAnnex.bb. No globals: handles in r\Objects[] / r\RoomDoors[] / r\NPC[], progress in
;   the room's event (EventState / 2 / 3, lower-case flags in EventStr, numbers as <K123>).
;=====================================================================

;what a version of Santa (or a sergeant in a box) decides you need
Function IS08HasKey%(level%)
	Local i%, k%
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			For k = level To 6
				If Inventory(i)\itemtemplate\name = "key" + k Then Return True
			Next
		EndIf
	Next
	Return False
End Function

Function IS08Need$()
	Local i%
	If Injuries > 1.0 Or Bloodloss > 20 Then Return "finefirstaid"
	If Not IS08HasKey(3) Then Return "key3"
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			Select Inventory(i)\itemtemplate\name
				Case "radio", "18vradio", "snav", "snav300", "snav310", "nvgoggles", "finenvgoggles"
					If Inventory(i)\state < 30 Then Return "18vbat"
			End Select
		EndIf
	Next
	Return "supereyedrops"
End Function

;every battery-powered thing you carry goes flat (returns True if anything did)
Function IS08Drain%()
	Local i%, any% = False
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			Select Inventory(i)\itemtemplate\name
				Case "radio", "18vradio", "fineradio", "veryfineradio", "snav", "snav300", "snav310", "snavulti", "nvgoggles", "finenvgoggles", "supernv"
					If Inventory(i)\state > 0 Then
						Inventory(i)\state = 0
						any = True
					EndIf
			End Select
		EndIf
	Next
	Return any
End Function

;the bunker's siren has its own channel: e\SoundCHN belongs to the lift (UpdateElevators plays the lift's
;moving sound on it), and sharing it kept the lift silent until it stopped
Global IS08SirenCHN%

Function IS08Hush(e.Events)
	IS16Hush(e)
	If IS08SirenCHN <> 0 Then
		If ChannelPlaying(IS08SirenCHN) Then StopChannel(IS08SirenCHN)
	EndIf
	If e\SoundCHN2 <> 0 Then
		If ChannelPlaying(e\SoundCHN2) Then StopChannel(e\SoundCHN2)
	EndIf
End Function

Function IndevS08Dress(r.Rooms)
	Local i%, m%
	Select r\RoomTemplate\Name
		Case "room2yule"
			m = IS16Prop(r, "GFX\npcs\scp1225.b3d", "GFX\npcs\indev_ornament.png", r\Objects[S08_YUL_ORN], 0)
			EntityPickMode(m, 2)
			r\Objects[S08_YUL_ORNM] = m
			For i = 0 To 2
				r\Objects[S08_YUL_UNIM + i] = IS16Prop(r, "GFX\npcs\indev_unicycle.b3d", "GFX\npcs\indev_unicycle.png", r\Objects[S08_YUL_UNI0 + i], 90 + i * 8)
			Next
			m = IS16Prop(r, "GFX\npcs\indev_unicycle.b3d", "GFX\npcs\indev_unicycle.png", r\Objects[S08_YUL_UNI0], 0)
			HideEntity(m)
			r\Objects[S08_YUL_UNIV] = m

		Case "room2pinata"
			m = IS16Prop(r, "GFX\npcs\scp956.b3d", "GFX\npcs\indev_pinata.png", r\Objects[S08_PIN_PINATA], 90)
			EntityPickMode(m, 2)
			r\Objects[S08_PIN_PINM] = m
			m = IS16Prop(r, "GFX\npcs\scp956.b3d", "GFX\npcs\indev_pinata.png", r\Objects[S08_PIN_EXTRA], 180)
			ScaleEntity(m, 0.6, 0.6, 0.6)
			r\Objects[S08_PIN_EXTRAM] = m

		Case "room2argos"
			m = IS16Prop(r, "GFX\npcs\indev_parcel.b3d", "GFX\map\indev_props6.png", r\Objects[S08_ARG_CHUTE], 20)
			EntityPickMode(m, 2)
			HideEntity(m)
			r\Objects[S08_ARG_PARCELM] = m

		Case "room2chrono"
			m = IS16Prop(r, "GFX\npcs\scp4255s.b3d", "GFX\npcs\indev_sleigh.png", r\Objects[S08_CHR_SLEIGH], 0)
			EntityPickMode(m, 2)
			r\Objects[S08_CHR_SLEIGHM] = m
			For i = 0 To 7
				m = IS16Prop(r, "GFX\npcs\indev_reindeer.b3d", "GFX\npcs\indev_reindeer.png", r\Objects[S08_CHR_RD0 + i], 0)
				EntityPickMode(m, 2)
				r\Objects[S08_CHR_RDM + i] = m
			Next
	End Select
End Function

Function UpdateIndevS08(e.Events)
	Local r.Rooms = e\room
	If r\dist < 10.0 Then IndevS08Spin(r, 1.0)
	Select r\RoomTemplate\Name
		Case "room2yule"
			UpdateS08Yule(e)
		Case "room2pinata"
			UpdateS08Pinata(e)
		Case "room2demoncore"
			UpdateS08DemonCore(e)
		Case "room2argos"
			UpdateS08Argos(e)
		Case "room2chrono"
			UpdateS08Chrono(e)
	End Select
End Function

;=====================================================================
; room2yule - Containment 4-Y
;   EventState  how long SCP-1225 has been on the tree (once you have been in)   EventState2 Sir Nicholas's
;   cooldown      EventState3 how long Sir Nicholas has been with you
;   numbers: <P> prizes won, <N> times Sir Nicholas has come, <R> ornament tick
;   flags: n placed, c a code card in hand, m milk poured, o ornament in your hand, x ornament boxed, l locker
;          opened, v you have been in, g gift tag taken, q Sir Nicholas is here;
;   counts: b bowls eaten, d drinks from the bottle.  NPC[0] Waters, [1] SCP-1933, [2] Kappa-31 agent, [3] SCP-6895
;=====================================================================

Function IS08Nicholas(e.Events)
	Local r.Rooms = e\room, n.NPCs, fx#, fz#, l#, k%, side#, gift$, uni% = r\Objects[S08_YUL_UNIV]
	Local px#, py#, pz#

	If e\EventState2 > 0 Then e\EventState2 = Max(0, e\EventState2 - FPSfactor)
	If KillTimer < 0 Then Return

	If IAxFlag(e, "q") Then
		e\EventState3 = e\EventState3 + FPSfactor
		n = r\NPC[3]
		If n <> Null Then
			IAxFace(n, Collider)
			If EntityDistance(n\Collider, Collider) > 12.0 Then e\EventState3 = 70 * 99
		EndIf
		If e\EventState3 > 70 * 7 Then
			IS13Drop(e, "q")
			EntityParent(uni, r\obj)
			HideEntity(uni)
			IS13Gone(r, 3)
			e\EventState2 = 70 * 240
			LightFlash = 0.4
			IS16Tell("You blink and he's gone - him and the unicycle both.", 5)
		EndIf
		Return
	EndIf

	If e\EventState2 > 0 Or IS10Num(e, "N") >= 3 Or PlayerRoom = Null Then Return
	If Not (Injuries > 1.6 Or Bloodloss > 25 Or IndevStress > 80) Then Return
	Select PlayerRoom\RoomTemplate\Name
		Case "pocketdimension", "dimension1499", "173", "gatea", "exit1"
			Return
	End Select

	;somewhere to stand: in front of you, or else behind you
	TFormVector(0, 0, 1, Camera, 0)
	fx = TFormedX() : fz = TFormedZ()
	l = Sqr(fx * fx + fz * fz)
	If l < 0.01 Then Return
	fx = fx / l : fz = fz / l
	side = 0
	For k = 0 To 1
		side = 1 - 2 * k
		LinePick(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), fx * side * 1.9, 0, fz * side * 1.9)
		If PickedEntity() = 0 Then Exit
		side = 0
	Next
	If side = 0 Then
		e\EventState2 = 70 * 10
		Return
	EndIf
	px = EntityX(Collider, True) + fx * side * 1.4
	py = EntityY(Collider, True)
	pz = EntityZ(Collider, True) + fz * side * 1.4
	n = CreateNPC(NPCtypeD, px, py + 0.2, pz)
	n\State = 0
	RotateEntity(n\Collider, 0, VectorYaw(-fx * side, 0, -fz * side), 0)
	IAxSkin(n, "GFX\npcs\indev_santa6895.jpg")
	r\NPC[3] = n
	ShowEntity(uni)
	EntityParent(uni, n\Collider, True)
	PositionEntity(uni, 0.35, -0.3, 0.1)
	RotateEntity(uni, 0, 90, 0)
	IAxSetFlag(e, "q")
	e\EventState3 = 0
	IS10SetNum(e, "N", IS10Num(e, "N") + 1)
	IS10Sound("SFX\Indev\bells.wav", n\Collider, 10.0, 0.8)
	gift = ""
	If Injuries > 1.6 Or Bloodloss > 25 Then gift = "finefirstaid"
	If gift <> "" Then
		IS16Give(gift, Collider)
		IS16Tell("An old man on a unicycle reaches behind his back, where there is nothing, and hands you a first aid kit. " + Chr(34) + "Oh dear, look at you." + Chr(34), 8)
	Else
		IndevRelieveStress(40)
		Stamina = 100
		IAxSay("Sir Nicholas", "You look like you've had a night of it. Eggnog - my mother's recipe. Drink up.", 7)
	EndIf
End Function

Function UpdateS08Yule(e.Events)
	Local r.Rooms = e\room
	Local i%, n.NPCs, d#, orn% = r\Objects[S08_YUL_ORNM], q$ = Chr(34), roll%, k%, gift$

	IS08Nicholas(e)

	;the ornament ages the locker whether you watch or not
	If IAxFlag(e, "v") And (Not IAxFlag(e, "o")) And (Not IAxFlag(e, "x")) Then e\EventState = e\EventState + FPSfactor
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return
	IAxSetFlag(e, "v")

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S08_YUL_WATERS, 180)
		r\NPC[1] = IS16Person(r, S08_YUL_SANTA, 90)
		r\NPC[2] = IS16Person(r, S08_YUL_KAPPA, 0)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\scientist.jpg")
	IAxSkin(r\NPC[1], "GFX\npcs\indev_santa1933.jpg")
	IAxSkin(r\NPC[2], "GFX\npcs\indev_kappa31.jpg")
	For i = 0 To 2
		n = r\NPC[i]
		If n <> Null Then
			d = EntityDistance(n\Collider, Collider)
			If d < 4.0 Then IAxFace(n, Collider)
			If i = 1 Then RotateEntity(n\Collider, Sin(MilliSecs() * 0.12) * 4, EntityYaw(n\Collider), Sin(MilliSecs() * 0.09) * 6)
			If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
				Select i * 3 + Rand(0, 2)
					Case 0
						IAxSay("Researcher Waters", "Put the code in and the prize lands in your lap. Literally. Mind your coffee.", 6)
					Case 1
						IAxSay("Researcher Waters", "To a child it's the best cereal ever. To us it's oatmeal. Unsweetened.", 6)
					Case 2
						IAxSay("Researcher Waters", "The O5s gave this project a hundred and twenty million dollars. For prizes.", 6)
					Case 3
						IAxSay("SCP-1933", "Ho ho - hic - ho. Merry Christmas! Have you had your present? Have it now.", 6)
					Case 4
						IAxSay("SCP-1933", "I'm not dangerous. I'm FESTIVE. Pass the whiskey.", 5)
					Case 5
						IAxSay("SCP-1933", "They hose me down every Sunday. A man should be allowed to smell like Christmas.", 6)
					Case 6
						IAxSay("Kappa-31", "We wear the suit and ride the bikes so nobody looks twice at him. It works.", 6)
					Case 7
						IAxSay("Kappa-31", "He finds whoever's having the worst night. In here, that's usually one of you.", 6)
					Case 8
						IAxSay("Kappa-31", "Christmas night, half past seven to half past ten. Every city at once, sometimes.", 6)
				End Select
			EndIf
		EndIf
	Next

	;---- SCP-2983
	If IS10Press(r\Objects[S08_YUL_BOX], 1.4) Then
		If IAxFlag(e, "c") Then
			IS16Tell("You already have a code card in your hand.", 4)
		ElseIf IS10Num(e, "P") >= 3 Then
			IS16Tell("Every box on these shelves has been opened. No more codes.", 4)
		Else
			IAxSetFlag(e, "c")
			If IS10Num(e, "P") = 0 Then IS16Give("doc2983c", r\Objects[S08_YUL_BOX])
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IS16Tell("At the bottom of the box: a code card. Six characters, none of them letters.", 6)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_YUL_TERM], 1.4) Then
		PlaySound_Strict(LoadTempSound("SFX\Indev\beep.wav"))
		If Not IAxFlag(e, "c") Then
			IS16Tell("PRIZE INPUT. Enter your code (that you can find on the inside of every cereal box!). Good luck!!", 7)
		Else
			IS13Drop(e, "c")
			IS10SetNum(e, "P", IS10Num(e, "P") + 1)
			Select Rand(5)
				Case 1
					gift = "18vbat"
				Case 2
					gift = "fineeyedrops"
				Case 3
					gift = "finefirstaid"
				Case 4
					gift = "snav300"
				Default
					gift = "key3"
			End Select
			IS16Give(gift, Collider)
			IS16Tell("You type the symbols - your fingers know how. An email you never signed up for: WOWWEE! A WINNER! Something lands in your lap.", 8)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_YUL_BOWL], 1.4) Then
		If IS13Count(e, "b") >= 2 Then
			IS16Tell("The bowl is empty and the milk is gone.", 4)
		ElseIf Not IAxFlag(e, "m") Then
			IAxSetFlag(e, "m")
			IS10Sound("SFX\Indev\choir.wav", r\Objects[S08_YUL_BOWL], 8.0, 1.0)
			IS16Tell("You pour the milk. Six marshmallows stand up - a fish, a moon, a trumpet, a skull, a sweet, and one you can't see - and sing about brushing your teeth.", 9)
		Else
			IS13Drop(e, "m")
			e\EventStr = e\EventStr + "b"
			Stamina = 100
			Injuries = Max(0, Injuries - 0.25)
			IS16Tell("It tastes like unsweetened oatmeal. Your body seems to get more out of it than your tongue does.", 7)
		EndIf
	EndIf

	;---- SCP-1933's present
	If IS10Press(r\Objects[S08_YUL_BOTTLE], 1.3) Then
		If Not IAxFlag(e, "g") Then
			IAxSetFlag(e, "g")
			IS16Give("doc1933b", r\Objects[S08_YUL_BOTTLE])
			IS16Tell("A bottle in torn wrapping paper, a tag tied on with string. Click again to drink.", 6)
		Else
			e\EventStr = e\EventStr + "d"
			k = IS13Count(e, "d")
			roll = Rand(100)
			If k > 1 And roll <= 25 * (k - 1) Then
				DeathMSG = "Subject D-9341 was found in SCP-1933's cell. Every fluid in the body had become Irish cream. SCP-1933 has asked whether the subject liked the present."
				Kill()
			Else
				IndevRelieveStress(15)
				BlurTimer = BlurTimer + 400
				If k = 1 Then
					IS16Tell("Irish cream. Warm. A good deal of whiskey in it. About 25 ml - the safe amount.", 6)
				Else
					IS16Tell("More. You got away with it. Your blood feels thick and sweet.", 6)
				EndIf
				IAxSay("SCP-1933", "Good, isn't it? I made it myself. Have some more!", 5)
			EndIf
		EndIf
	EndIf

	;---- SCP-1225
	If (Not IAxFlag(e, "o")) And (Not IAxFlag(e, "x")) Then
		If EntityDistance(Collider, r\Objects[S08_YUL_ORN]) < 2.2 Then
			IndevStress = Min(100, IndevStress + 0.015 * FPSfactor)
			IS10SetNum(e, "R", IS10Num(e, "R") + 1)
			If IS10Num(e, "R") > 210 Then
				IS10SetNum(e, "R", 0)
				If IS08Drain() Then IS16Tell("Your batteries are corroded through. The casings are pitted like they've been in a cellar for years.", 6)
			EndIf
			If MsgTimer <= 0 And Rand(900) = 1 Then IS16Tell("You are suddenly furious with the lights, the tree, everyone. You don't know why.", 5)
		EndIf
		If IS16Click(orn, orn, 1.6) Then
			IAxSetFlag(e, "o")
			HideEntity(orn)
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
			IS16Tell("You lift the ornament off the branch. Nothing else in the room changes, but you feel calmer at once.", 6)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_YUL_SBOX], 1.3) Then
		If IAxFlag(e, "x") Then
			IS16Tell("SCP-1225 is in its box, in its packing, locked.", 4)
		ElseIf IAxFlag(e, "o") Then
			IAxSetFlag(e, "x")
			PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
			IS16Tell("Packing, box, lock. The supply locker clicks: whatever is left inside has stopped getting older.", 7)
		Else
			IS16Tell("The steel box is empty and unlocked. The thing that belongs in it is on the tree.", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_YUL_LOCKER], 1.3) Then
		If Not IAxFlag(e, "x") Then
			IS16Tell("The locker door is warm and pitted. Something inside smells like it has been rotting for years.", 6)
		ElseIf IAxFlag(e, "l") Then
			IS16Tell("The locker is empty.", 3)
		Else
			IAxSetFlag(e, "l")
			If e\EventState < 70 * 60 Then
				IS16Give("finefirstaid", r\Objects[S08_YUL_LOCKER])
				IS16Give("18vbat", r\Objects[S08_YUL_LOCKER])
				IS16Tell("You were quick. The first aid kit is barely yellowed and the battery still holds a charge.", 6)
			ElseIf e\EventState < 70 * 150 Then
				IS16Give("firstaid", r\Objects[S08_YUL_LOCKER])
				IS16Tell("The supplies have aged badly. One kit is still usable. Just.", 5)
			Else
				IS16Tell("Everything in the locker has aged ten years: rags, rust, a battery leaking white crust. Nothing worth taking.", 7)
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room2pinata - SCP-956
;   EventState  0 walking the edge of the cell, 1 standing facing the wall   EventState2 the candy working in you
;   EventState3 how long it has stood there.  numbers: <W> which corner it is walking to
;   flags: n placed, w warned about the candy, e ate it, f the incinerator ran, k the key given, c cold,
;          t it is facing the furnace
;   NPC[0] Dr. N.
;=====================================================================

Function UpdateS08Pinata(e.Events)
	Local r.Rooms = e\room
	Local pin% = r\Objects[S08_PIN_PINM], w%, left#, lx#, lz#, n.NPCs, d#, t# = IS16Time()

	;---- SCP-956-1, wherever you are
	If IAxFlag(e, "e") And KillTimer >= 0 Then
		e\EventState2 = e\EventState2 - FPSfactor
		If e\EventState2 < 70 * 120 And e\EventState2 + FPSfactor >= 70 * 120 Then IS16Tell("Your mouth tastes of sugar, and of something under the sugar.", 5)
		If e\EventState2 < 70 * 30 And e\EventState2 + FPSfactor >= 70 * 30 Then IS16Tell("Your hands won't stop shaking.", 4)
		If e\EventState2 <= 0 Then
			IS13Drop(e, "e")
			CameraShake = 5.0
			BlinkTimer = -10
			BlurTimer = 1800
			Stamina = 0
			Injuries = Injuries + 1.0
			If Rand(100) <= 65 Then
				DeathMSG = "Subject D-9341 suffered a seizure followed by cardiac arrest approximately three minutes after eating SCP-956-1 from the cold store. The jar was found open."
				Kill()
			Else
				IS16Tell("A seizure takes you to the floor and shakes you like a rag. Then it lets go. You're one of the third who get up.", 8)
			EndIf
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S08_PIN_DOCN, 90)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\scientist.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Dr. N.", "Adults are safe in there. That's the only reason any of us can work here.", 6)
				Case 2
					IAxSay("Dr. N.", "It walks the walls, then it stands facing north-east. There's a school that way.", 6)
				Case 3
					IAxSay("Dr. N.", "The one on the cart was made from one of its victims. It goes in the furnace. Somebody has to press the button.", 7)
			End Select
		EndIf
	EndIf

	;---- SCP-956 walks the edge of its cell, then stares at the wall
	Select e\EventState
		Case 0
			w = IS10Num(e, "W")
			left = IS10Walk(pin, EntityX(r\Objects[S08_PIN_PC0 + w]), EntityZ(r\Objects[S08_PIN_PC0 + w]), 0.9)
			PositionEntity(pin, EntityX(pin), Abs(Sin(t * 260)) * 3, EntityZ(pin))
			If Rand(260) = 1 Then IS10Sound("SFX\Indev\crinkle.wav", pin, 6.0, 0.7)
			If left < 6.0 Then
				If w >= 3 Then
					IS10SetNum(e, "W", 0)
					e\EventState = 1
					e\EventState3 = 0
				Else
					IS10SetNum(e, "W", w + 1)
				EndIf
			EndIf
		Case 1
			e\EventState3 = e\EventState3 + FPSfactor
			IS10Walk(pin, EntityX(r\Objects[S08_PIN_PINATA]), EntityZ(r\Objects[S08_PIN_PINATA]), 0.9)
			If IAxFlag(e, "t") Then
				RotateEntity(pin, 0, CurveAngle(VectorYaw(EntityX(r\Objects[S08_PIN_FURNACE]) - EntityX(pin), 0, EntityZ(r\Objects[S08_PIN_FURNACE]) - EntityZ(pin)), EntityYaw(pin), 30.0), 0)
			ElseIf e\EventState3 > 70 * 4 Then
				RotateEntity(pin, 0, CurveAngle(-45, EntityYaw(pin), 30.0), 0)
			EndIf
			If e\EventState3 > 70 * 40 Then
				e\EventState = 0
				IS13Drop(e, "t")
			EndIf
	End Select
	If IS16Click(pin, pin, 1.5) Then
		IS10Sound("SFX\Indev\crinkle.wav", pin, 6.0, 1.0)
		IS16Tell("You hit it as hard as you can. Your knuckles sting. It doesn't even dent, and it doesn't look at you.", 6)
	EndIf

	;---- the cold store, SCP-956-1
	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()
	If lz > 544.0 And lx > 296.0 And lx < 564.0 Then
		Stamina = Max(0, Stamina - 0.04 * FPSfactor)
		BlurTimer = Max(BlurTimer, 120)
		If Not IAxFlag(e, "c") Then
			IAxSetFlag(e, "c")
			IS16Tell("Minus four. Your breath fogs. The jars on the shelves are full of bright, unmarked sweets.", 6)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_PIN_CANDY], 1.4) Then
		If IAxFlag(e, "e") Then
			IS16Tell("You've had one. That was already one too many.", 4)
		ElseIf Not IAxFlag(e, "w") Then
			IAxSetFlag(e, "w")
			IS16Tell("SCP-956-1. Over twelve: a seizure within three minutes, one in three survive. Click again to eat one anyway.", 8)
		Else
			IAxSetFlag(e, "e")
			e\EventState2 = 70 * 180
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IS16Tell("It's very sweet. For a moment it's the best thing you have ever tasted.", 6)
		EndIf
	EndIf

	;---- the incinerator
	If IS10Press(r\Objects[S08_PIN_BURN], 1.3) Then
		If IAxFlag(e, "f") Then
			IS16Tell("The furnace is still cooling.", 3)
		Else
			IAxSetFlag(e, "f")
			HideEntity(r\Objects[S08_PIN_EXTRAM])
			IS10Sound("SFX\Indev\fire.wav", r\Objects[S08_PIN_FURNACE], 10.0, 1.0)
			IS10Sound("SFX\Indev\crinkle.wav", r\Objects[S08_PIN_FURNACE], 10.0, 1.0)
			CameraShake = 1.5
			e\EventState = 1
			e\EventState3 = 0
			IAxSetFlag(e, "t")
			IndevStress = Min(100, IndevStress + 10)
			IS16Tell("The cart tips the small one into the flames. It burns like paper and screams like something that isn't. In the cell, SCP-956 turns its head towards the sound.", 9)
			If r\NPC[0] <> Null And (Not IAxFlag(e, "k")) Then
				IAxSetFlag(e, "k")
				IS16Give("key3", r\NPC[0]\Collider)
				IAxSay("Dr. N.", "Thank you. I couldn't do it again. Take my card - I won't be needing it today.", 6)
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room2demoncore - SCP-095-FR
;   EventState  0 between peaks, 1 the siren (a peak is coming), 2 -   EventState2 the lift
;   EventState3 time to the next peak / to the flash
;   numbers: <Z> how long since you lifted the shell (the dose you took then is fatal)
;   flags: n placed, w first time down, d batteries killed this visit, s warned about the bench, c you lifted it
;   NPC[0] the Class-D handler
;=====================================================================

Function UpdateS08DemonCore(e.Events)
	Local r.Rooms = e\room
	Local core% = r\Objects[S08_DEM_CORE], door.Doors = r\RoomDoors[S08_DEM_D_CTRL]
	Local lx#, ly#, lz#, down%, inctrl%, d#, z%, n.NPCs

	;---- what lifting the shell did to you
	If IAxFlag(e, "c") And KillTimer >= 0 Then
		z = IS10Num(e, "Z") + 1
		IS10SetNum(e, "Z", z)
		BlurTimer = Max(BlurTimer, 300)
		If z = 70 * 20 Then IS16Tell("You throw up. Then again.", 4)
		If z = 70 * 45 Then IS16Tell("Your hands are red and swelling. The one that touched the shell is worse.", 6)
		If z = 70 * 70 Then IS16Tell("You can't stay standing for long. Your mouth is full of the taste of metal.", 6)
		If z > 70 * 90 Then
			DeathMSG = "Subject D-9341 died of acute radiation syndrome after a criticality incident with SCP-095-FR. Like Louis Slotin in 1946, the subject knocked the upper shell away by hand; the Class-D present survived."
			Kill()
		EndIf
	EndIf
	If PlayerRoom <> r Then
		IS13Drop(e, "d")
		IS08Hush(e)
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	;for the room test: frames the lift was moving, and frames its moving sound was playing
	If e\EventState2 <> 0 Then
		IndevLiftMove = IndevLiftMove + 1
		If e\SoundCHN <> 0 Then
			If ChannelPlaying(e\SoundCHN) Then IndevLiftSnd = IndevLiftSnd + 1
		EndIf
	EndIf
	If KillTimer < 0 Then
		IS08Hush(e)
		Return
	EndIf

	IAxLocal(r)
	lx = TFormedX() : ly = TFormedY() : lz = TFormedZ()
	down = (ly < -400.0)
	inctrl = (down And lx < 528.0 And lz < -500.0)

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S08_DEM_HANDLER, 180)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_hazmat.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Class-D", "They said I get executed after this. Standard procedure. Is that true?", 6)
				Case 2
					IAxSay("Class-D", "Siren means get in the control room and shut the door. Don't stand there looking at it.", 6)
				Case 3
					IAxSay("Class-D", "Don't touch the screwdriver. I mean it. Don't even breathe near the screwdriver.", 6)
			End Select
		EndIf
	EndIf

	If Not down Then
		IS08Hush(e)
		Return
	EndIf

	;---- twenty metres of dead electronics, and the counter
	If Not IAxFlag(e, "d") Then
		IAxSetFlag(e, "d")
		If IS08Drain() Then IS16Tell("Everything electronic you carry dies the moment the lift doors open.", 5)
	EndIf
	d = EntityDistance(Collider, core)
	If e\Sound2 = 0 Then e\Sound2 = LoadSound_Strict("SFX\Indev\geiger2.wav")
	e\SoundCHN2 = LoopSound2(e\Sound2, e\SoundCHN2, Camera, core, 14.0, Max(0.15, 1.0 - d / 7.0))
	If d < 2.0 Then
		Injuries = Injuries + 0.0004 * FPSfactor
		DeathMSG = "Subject D-9341 died of radiation exposure in Bunker 095-FR after spending too long within two metres of SCP-095-FR."
	EndIf

	;---- flux peaks
	If Not IAxFlag(e, "w") Then
		IAxSetFlag(e, "w")
		e\EventState3 = 70 * 45
	EndIf
	e\EventState3 = e\EventState3 - FPSfactor
	Select e\EventState
		Case 0
			If e\EventState3 <= 0 Then
				e\EventState = 1
				e\EventState3 = 70 * 12
				If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Alarm\Alarm3.ogg")
				LightBlink = 1.5
				IS16Tell("SIREN. FLUX PEAK. TAKE COVER. Twelve seconds - the control room, and shut the door behind you.", 7)
			EndIf
		Case 1
			If e\Sound <> 0 Then IS08SirenCHN = LoopSound2(e\Sound, IS08SirenCHN, Camera, core, 20.0, 1.0)
			If e\EventState3 <= 0 Then
				If IS08SirenCHN <> 0 Then
					If ChannelPlaying(IS08SirenCHN) Then StopChannel(IS08SirenCHN)
				EndIf
				e\EventState = 0
				e\EventState3 = 70 * 150
				LightFlash = 2.5
				CameraShake = 2.0
				IS10Sound("SFX\Indev\zap.wav", core, 20.0, 1.0)
				If inctrl And (Not door\open) Then
					IS16Tell("Through the lead glass the bunker goes blue for a heartbeat. The needle pins and drops back. You're fine.", 7)
				ElseIf d < 3.0 Then
					DeathMSG = "Subject D-9341 was within three metres of SCP-095-FR during a neutron flux peak. Death was effectively instantaneous."
					Kill()
				Else
					If inctrl Then
						Injuries = Injuries + 0.6
						BlurTimer = 600
						IS16Tell("You were behind the lead, but the door was open. You feel it anyway, a warmth from the inside.", 7)
					Else
						Injuries = Injuries + 1.4
						Bloodloss = Min(100, Bloodloss + 15)
						BlurTimer = 1200
						IndevStress = Min(100, IndevStress + 20)
						DeathMSG = "Subject D-9341 died of radiation exposure after a neutron flux peak in Bunker 095-FR, outside the shielded control room."
						IS16Tell("A blue flash, everywhere at once, and heat on your skin. You took a dose. You can taste it.", 7)
					EndIf
				EndIf
			EndIf
	End Select

	;---- the bench, the safe
	If IS10Press(r\Objects[S08_DEM_SCREW], 1.2) And (Not IAxFlag(e, "c")) Then
		If Not IAxFlag(e, "s") Then
			IAxSetFlag(e, "s")
			IS16Tell("The upper shell sits on a screwdriver, a hair above the core. Louis Slotin did exactly this. Click again to lift it.", 8)
		Else
			IAxSetFlag(e, "c")
			IS10SetNum(e, "Z", 0)
			LightFlash = 4.0
			CameraShake = 3.0
			BlurTimer = 2000
			IS10Sound("SFX\Indev\zap.wav", core, 20.0, 1.0)
			IS16Tell("The screwdriver slips. Blue light, everywhere at once, and heat. You knock the shell off with your hand. Too late, and you know it.", 9)
			IAxSay("Class-D", "...Thank you. Oh god. Thank you.", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[S08_DEM_SAFE], 1.4) Then IS16Tell("The lead safe stands open. The core is supposed to be inside. It is on the bench.", 5)
End Function

;=====================================================================
; room2argos - SCP-3355
;   EventState  terminal lockout (time left)   EventState2 the lift   EventState3 the pause after each line
;   numbers: <L> lines Nick has said.  flags: n placed, p a package in the chute, o opened it, m manifest printed
;   count a: how many times you interrupted.  NPC[0] the volunteer upstairs
;=====================================================================

Function UpdateS08Argos(e.Events)
	Local r.Rooms = e\room
	Local par% = r\Objects[S08_ARG_PARCELM], n.NPCs, d#, l%, q$ = Chr(34), gift$

	If e\EventState3 > 0 Then e\EventState3 = Max(0, e\EventState3 - FPSfactor)
	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S08_ARG_VOL, 180)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_sweater.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Volunteer", "St. Nick's Workshop! Every package delivered by St. Nick himself. Well. Sort of.", 6)
				Case 2
					IAxSay("Volunteer", "If you go down there, be polite. He locks people out. He locked the board out twice.", 6)
				Case 3
					IAxSay("Volunteer", "We just answer the phones. The packages do themselves.", 5)
			End Select
		EndIf
	EndIf

	;---- TERMINAL LOCKOUT
	If e\EventState > 0 Then
		e\EventState = Max(0, e\EventState - FPSfactor)
		r\RoomDoors[0]\locked = True
		r\RoomDoors[1]\locked = True
		If e\EventState = 0 Then
			r\RoomDoors[0]\locked = False
			r\RoomDoors[1]\locked = False
			IS16Tell("The lift panel lights up again. Nick has let you go.", 5)
		EndIf
	EndIf

	If IS10Press(r\Objects[S08_ARG_TERM], 1.4) Then
		PlaySound_Strict(LoadTempSound("SFX\Indev\beep.wav"))
		If e\EventState > 0 Then
			IS16Tell("TERMINAL LOCKOUT.", 3)
		ElseIf e\EventState3 > 0 Then
			e\EventStr = e\EventStr + "a"
			If IS13Count(e, "a") >= 3 Then
				IS13Drop(e, "a")
				e\EventState = 70 * 20
				LightBlink = 2.0
				IS16Tell("ARGOS: " + q + "Enough. TERMINAL LOCKOUT." + q + " Behind you the lift doors lock.", 7)
			Else
				IS16Tell("ARGOS: " + q + "I'm busy. Wait your turn." + q, 4)
			EndIf
		Else
			l = IS10Num(e, "L") + 1
			IS10SetNum(e, "L", l)
			e\EventState3 = 70 * 4
			Select l
				Case 1
					IS16Tell("ARGOS: " + q + "Come again? Who are you? How'd you get down here?" + q, 6)
				Case 2
					IS16Tell("ARGOS: " + q + "Nick. Sergeant, US Army, population management, Fort Sheridan. That's the name. Need anything else?" + q, 8)
				Case 3
					IS16Tell("ARGOS: " + q + "I'm not angry. I just don't get visitors. And I'm behind on deliveries before the holiday." + q, 8)
				Case 4
					IS16Tell("ARGOS: " + q + "An engineer woke me up and said: look after Chicago. I can't stop a fire. I can do this." + q, 8)
				Case 5
					IS16Tell("ARGOS: " + q + "...You look like you could use something yourself, kid. Check the chute." + q, 7)
					IAxSetFlag(e, "p")
					ShowEntity(par)
					IS10Sound("SFX\Indev\thump.wav", r\Objects[S08_ARG_CHUTE], 8.0, 1.0)
					If Not IAxFlag(e, "m") Then
						IAxSetFlag(e, "m")
						IS10Sound("SFX\Indev\teletype.wav", r\Objects[S08_ARG_PRINTER], 8.0, 1.0)
						IS16Give("doc3355b", r\Objects[S08_ARG_PRINTER])
					EndIf
				Default
					IS16Tell("ARGOS: " + q + "I'm busy. It's nearly Christmas. It's always nearly Christmas down here." + q, 6)
			End Select
		EndIf
	EndIf

	If IAxFlag(e, "p") And (Not IAxFlag(e, "o")) Then
		If IS16Click(par, par, 1.5) Then
			IAxSetFlag(e, "o")
			HideEntity(par)
			gift = IS08Need()
			IS16Give(gift, r\Objects[S08_ARG_CHUTE])
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IS16Tell("FROM: ST. NICK, 100 CHRISTMAS STREET, NORTH POLE. Inside is exactly what you needed.", 7)
		EndIf
	EndIf
End Function

;=====================================================================
; room2chrono - SCP-4255
;   EventState  how long you have been on the launch deck   EventState2 the lift   EventState3 a version of
;   him is here (time)    flags: n placed, e a version came this visit, h one is here now, b BTKAI told you
;   count v: versions who have come.  NPC[0] Stan Clane, NPC[1] the version
;=====================================================================

Function UpdateS08Chrono(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, d#, i%, ly#, gift$, q$ = Chr(34), m%

	If PlayerRoom <> r Then
		IS13Drop(e, "e")
		If IAxFlag(e, "h") Then
			IS13Drop(e, "h")
			IS13Gone(r, 1)
		EndIf
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S08_CHR_CLANE, 0)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_clane.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Clane", "They tell me I've already done all this. Two hundred and ninety-four of me, all at once. No pressure.", 7)
				Case 2
					IAxSay("Clane", "Third test flight we landed eleven minutes before we took off. The reindeer didn't mind. They don't mind anything.", 7)
				Case 3
					IAxSay("Clane", "If an older me turns up, take whatever he gives you. He knows. He always knows.", 6)
			End Select
		EndIf
	EndIf

	;---- the BTKAI unit
	If IS10Press(r\Objects[S08_CHR_BTKAI], 1.4) Then
		PlaySound_Strict(LoadTempSound("SFX\Indev\beep.wav"))
		If Not IAxFlag(e, "b") Then
			IAxSetFlag(e, "b")
			IS16Tell("BTKAI: KNOWLEDGE COMPLETE TO 20##. It prints, unasked, a keypad code you have not needed yet: " + Indev055Code() + ".", 9)
		Else
			Select Rand(3)
				Case 1
					IS16Tell("BTKAI: GIFT QUEUE 2,118,604,551. ACCURACY TARGET 82.56%. CURRENT: 82.56%.", 6)
				Case 2
					IS16Tell("BTKAI: SUBJECT D-9341 - PREFERRED GIFT: AN EXIT.", 5)
				Default
					IS16Tell("BTKAI: PILOT CLANE, S. - ROLE COMPLETE 21##. DO NOT INFORM PILOT.", 6)
			End Select
		EndIf
	EndIf

	;---- the sleigh and the reindeer
	m = r\Objects[S08_CHR_SLEIGHM]
	If IS16Click(m, m, 2.0) Then
		If Left(CurrentDate(), 6) = "24 Dec" Or Left(CurrentDate(), 6) = "25 Dec" Then
			IS16Tell("SCP-4255-1 (replica). Tonight the temporal coils are humming on their own. Somewhere up there, all of him are flying.", 8)
		Else
			IS16Tell("SCP-4255-1 (replica): red lacquer, gold scrollwork, two humming coils at the back. The flight log is pinned to the console.", 7)
		EndIf
	EndIf
	For i = 0 To 7
		m = r\Objects[S08_CHR_RDM + i]
		If IS16Click(m, m, 1.6) Then IS16Tell("It's cold. Not dead cold - no-temperature cold, like it isn't quite here. Its eyes follow you anyway.", 6)
	Next

	;---- a version of him, from somewhere else in his life
	IAxLocal(r)
	ly = TFormedY()
	If ly > 600.0 Then e\EventState = e\EventState + FPSfactor
	If IAxFlag(e, "h") Then
		e\EventState3 = e\EventState3 + FPSfactor
		n = r\NPC[1]
		If n <> Null Then
			IAxSkin(n, "GFX\npcs\indev_santa4255.jpg")
			IAxFace(n, Collider)
		EndIf
		If e\EventState3 > 70 * 8 Then
			IS13Drop(e, "h")
			IS13Gone(r, 1)
			IS10Sound("SFX\Indev\bells.wav", r\Objects[S08_CHR_ECHO], 12.0, 0.8)
			LightFlash = 0.5
			IS16Tell("Sleigh bells, from nowhere in particular, and he's gone.", 5)
		EndIf
	ElseIf ly > 600.0 And e\EventState > 70 * 20 And (Not IAxFlag(e, "e")) And IS13Count(e, "v") < 3 Then
		IAxSetFlag(e, "e")
		IAxSetFlag(e, "h")
		e\EventStr = e\EventStr + "v"
		e\EventState3 = 0
		r\NPC[1] = IS16Person(r, S08_CHR_ECHO, 90)
		IS10Sound("SFX\Indev\timewarp.wav", r\Objects[S08_CHR_ECHO], 12.0, 1.0)
		LightFlash = 0.8
		BlurTimer = 500
		gift = IS08Need()
		IS16Give(gift, Collider)
		Select IS13Count(e, "v")
			Case 1
				IAxSay("SCP-4255", "Ho, there you are. Right on time. This is for you - you'll want it in about ten minutes.", 8)
			Case 2
				IAxSay("SCP-4255", "Don't tell young Clane what I look like now. It spoils the surprise. Here.", 7)
			Default
				IAxSay("SCP-4255", "Last one I'm allowed to give you. You'll get out. Not the way you think.", 7)
		End Select
	EndIf
End Function
