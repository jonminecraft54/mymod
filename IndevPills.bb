;=====================================================================
; SCP: Containment Breach - Indev pill SCPs
;
;   SCP-214  string virus (vial)    - opened vial = fatal infection (~10 min), tissue turns to string
;   SCP-217  clockwork virus (vial) - opened vial = fatal infection (~11 min), stops bleeding, ticks
;   SCP-407  the song (cassette)   - heals for a minute, then growths, infection, overgrowth
;   SCP-006  spring water (vial)    - heals, cures, and keeps regenerating you for three minutes
;   SCP-006-B 914 concentrate       - all of the above, ten minutes, near-instant regen, tireless, immune
;   SCP-9282 regenerating bandage  - heals all injuries (needs a wound)
;   SCP-8228 chocolate cupcake      - heals and cures everything; costs you permanent fatigue
;   SCP-1642 Insta-teen tablets    - teenage mood swings; 2nd = anxiety, 3rd = coma
;   SCP-474  Alexylva placebo      - your next rest is a broadcast dream
;   SCP-483  anti-aging bottle      - turns a pill in your inventory into SCP-483-1
;   SCP-484  "V"                    - eye contact steals memories (guards know the code)
;   SCP-500  panacea                - (vanilla item) now also cures every pill effect here
;   SCP-876  element capsules       - two different colours in a row are fatal
;   SCP-2022 sunlight pills         - warm and energised; overdose burns and glows
;   SCP-2968 afterlife supplements  - lowers blood pressure; you die at peace
;   SCP-3494 superlax by dado       - you're not constipated. Lucky.
;   SCP-3521 banana equivalent dose - fatal
;   SCP-3866 youth in asia by dado  - permanent hibernation
;   SCP-3929 by dado                - you age ~70 years; stamina never recovers
;   SCP-4193 migraine medicine e    - first cures, the rest shrink your eyes
;   SCP-4257 space drive by dado    - you're a car: sprint forever, briefly
;   SCP-4292 freaky pills by dado   - random alteration, then withdrawal
;   SCP-5043 dado's brainexplosion  - three seconds, then your head explodes (and comes back)
;   SCP-7521 capsule collection     - a countdown to regressing into a fetus
;
; Nothing here is saved, same as Indev.bb: effects reset on load.
;=====================================================================

Global Pill474Pending%, Pill474Rest#
Global Pill483Years%
Global Pill484Timer#, Pill484Seen$
Global Pill876First$, Pill876Timer#
Global Pill2022Doses%, Pill2022Window#
Global Pill2968Taken%, Pill2968Shown%
Global Pill3866Timer#
Global Pill3521Timer#, Pill3521Stage%
Global Pill3929Stage%, Pill3929Timer#
Global Pill4193Count%, Pill4193Timer#
Global Pill4257Timer#
Global PillF02Timer#
Global Bowl348Cooldown#, Bowl348Note$, Bowl348NoteTimer#, Bowl348Meals%
Global Pill4292Effect%, Pill4292Timer#, Pill4292Next#, Pill4292Withdrawal#
Global Pill5043Timer#, Pill5043Blind#
Global Pill7521Timer#, Pill7521Stage%
Global Pill1642Doses%, Pill1642Window#, Pill1642Mood#, Pill1642Moods%, Pill1642Coma#
Global Pill8228Eaten%, Pill8228Timer#
Global Spring006Timer#, Spring006BTimer#
Global Virus214Time#, Virus214Stage%, Virus214Next#
Global Virus217Time#, Virus217Stage%, Virus217Next#, Virus217Snd%
Global Zone214X#, Zone214Y#, Zone214Z#, Zone214Timer#, Zone217X#, Zone217Y#, Zone217Z#, Zone217Timer#
Global Pill407Playing%, Pill407CHN%, Pill407Snd%, Pill407Item.Items, Pill407Exposure#, Pill407Stage%, Pill407Next#
Global IndevPillR%, IndevPillG%, IndevPillB%

Function IndevPillsReset()
	Pill474Pending = False : Pill474Rest = 0
	Pill483Years = 0
	Pill484Timer = 0 : Pill484Seen = ""
	Pill876First = "" : Pill876Timer = 0
	Pill2022Doses = 0 : Pill2022Window = 0
	Pill2968Taken = False : Pill2968Shown = False
	Pill3866Timer = 0
	Pill3521Timer = 0 : Pill3521Stage = 0
	Pill3929Stage = 0 : Pill3929Timer = 0
	Pill4193Count = 0 : Pill4193Timer = 0
	Pill4257Timer = 0
	PillF02Timer = 0
	Bowl348Cooldown = 0 : Bowl348Note = "" : Bowl348NoteTimer = 0 : Bowl348Meals = 0
	Pill4292Effect = 0 : Pill4292Timer = 0 : Pill4292Next = 0 : Pill4292Withdrawal = 0
	Pill5043Timer = 0 : Pill5043Blind = 0
	Pill7521Timer = 0 : Pill7521Stage = 0
	Pill1642Doses = 0 : Pill1642Window = 0 : Pill1642Mood = 0 : Pill1642Moods = 0 : Pill1642Coma = 0
	Pill8228Eaten = 0 : Pill8228Timer = 0
	Spring006Timer = 0 : Spring006BTimer = 0
	IndevStop407()
	Pill407Snd = 0 ;reloaded on first play, in case the old handle went with the last game
	Virus214Time = 0 : Virus214Stage = 0 : Virus214Next = 0
	Virus217Time = 0 : Virus217Stage = 0 : Virus217Next = 0 : Virus217Snd = 0
	Zone214Timer = 0 : Zone217Timer = 0
	Pill407Item = Null : Pill407Exposure = 0 : Pill407Stage = 0 : Pill407Next = 0
End Function

Function IndevPillMsg(txt$, secs# = 6)
	Msg = txt
	MsgTimer = 70*secs
End Function

;every pill-shaped item that SCP-483 will accept
Function IndevIsPill%(name$)
	Select name
		Case "pill", "scp500", "scp500death", "scp9097", "scp6833", "scp5604", "scp7985", "scp2077gel", "scp2077cap"
			Return True
		Case "scp474", "scp484", "scp876r", "scp876g", "scp876b", "scp2022", "scp2968", "scp3494", "scp3521"
			Return True
		Case "scp3866", "scp3929", "scp4193", "scp4257", "scp4292", "scp5043", "scp7521", "scp1642", "scpf02"
			Return True
	End Select
	Return False
End Function

Function IndevPillDeath(txt$)
	DeathMSG = txt
	Kill()
End Function

;---------------------------------------------------------------------
; using an item (called from the inventory Select in Main.bb)
;---------------------------------------------------------------------

Function IndevUsePill(it.Items)
	Local name$ = it\itemtemplate\name

	;a plain lemon (a nod to a certain rant about them): eating one patches you up a little
	If name = "lemon" Then
		If Not CanUseItem(False, False, True) Then Return
		Injuries = Max(0, Injuries - 0.15)
		Bloodloss = Max(0, Bloodloss - 5)
		Stamina = Min(100, Stamina + 20)
		IndevRelieveStress(3)
		Select Rand(1, 4)
			Case 1 IndevPillMsg("You bite straight into the lemon, peel and all. Incredibly sour. You feel a little better.", 5)
			Case 2 IndevPillMsg("The juice runs down your chin and your whole face puckers. Somehow it helps.", 5)
			Case 3 IndevPillMsg("When the facility gives you lemons, you eat the lemons. You feel slightly less terrible.", 5)
			Default IndevPillMsg("Sour enough to make your eyes water, but the vitamin C has to count for something.", 5)
		End Select
		PlaySound_Strict(LoadTempSound("SFX\SCP\294\slurp.ogg"))
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-458 (Indev458.bb)
	If name = "scp458" Then
		IndevUse458(it)
		Return
	EndIf

	;SCP-1471 (IndevOffices2.bb)
	If name = "scp1471" Then
		IndevUse1471(it)
		Return
	EndIf

	;SCP-963 / SCP-2295 (Indev963.bb)
	If name = "scp963" Then
		IndevUse963(it)
		Return
	EndIf
	If name = "scp2295" Then
		IndevUse2295(it)
		Return
	EndIf

	;SCP-109 (Indev109.bb)
	If name = "scp109" Then
		IndevUse109(it)
		Return
	EndIf

	;SCP-268 - the fez goes on and comes off like a hat (Indev268.bb)
	If name = "scp268" Then
		IndevUse268(it)
		Return
	EndIf

	;SCP-085 - the hand-drawn woman on graph paper (Indev085.bb)
	If name = "scp085" Then
		IndevUse085(it)
		Return
	EndIf

	;SCP-2935 evidence items - flavour text straight from the recovered-
	;artifacts log, read on use instead of a full document (Indev2935.bb)
	If name = "item2935paper" Then
		SelectedItem = Null
		IndevPillMsg("The newspaper is covered in dust. There are no signs of decomposition or microbial activity. Dated April 19th, 2016.", 6)
		Return
	EndIf
	If name = "item2935phone" Then
		SelectedItem = Null
		IndevPillMsg("The phone is completely inactive. Last message, sent 2041 hours, April 19th: " + Chr(34) + "are you guys still playing cards tonight? i have steven but he'll probably be asleep soon." + Chr(34), 8)
		Return
	EndIf
	If name = "item2935calendar" Then
		SelectedItem = Null
		IndevPillMsg("SITE-81. Every square through April 19th is crossed off. Nothing after that day is marked.", 6)
		Return
	EndIf

	;Commissary items (IndevRations.bb)
	If name = "indevration" Then
		IndevUseRation(it)
		Return
	EndIf
	If name = "indevwater" Then
		IndevUseWater(it)
		Return
	EndIf

	;SCP-113 (Indev113.bb)
	If name = "scp113" Then
		IndevUse113(it)
		Return
	EndIf

	;SCP-693 string dolls (Indev693.bb)
	If IsDoll693(name) Then
		IndevUse693(it)
		Return
	EndIf

	;MJOLNIR Type 1 - put on / take off like the vest (IndevMjolnir.bb)
	If name = "mjolnir" Then
		IndevUseMjolnir(it)
		Return
	EndIf

	;SCP-202 - the FOB watch compass stays open while selected (Indev202.bb)
	If name = "scp202" Then
		IndevUse202(it)
		Return
	EndIf

	;Cognitive Filter Glasses (IndevHazards.bb)
	If name = "cogglasses" Then
		IndevUseCogGlasses()
		SelectedItem = Null
		Return
	EndIf

	;SCP-770 - the iron flask (IndevHazards.bb)
	If name = "scp770" Then
		IndevUse770(it)
		Return
	EndIf

	;SCP-483 is a bottle, not a pill: it converts one pill in the inventory
	If name = "scp483" Then
		IndevUse483()
		SelectedItem = Null
		Return
	EndIf

	;SCP-214 / SCP-217 - virus sample vials: first use reads the label, second use opens it
	If name = "scp214" Or name = "scp217" Then
		;already opened by SCP-914: nothing to confirm, the virus is right there
		If it\state = 2 Then
			IndevPillMsg("The cap is already off. You tip the open vial to look inside and the contents run over your fingers.", 6)
			IndevInfect(name)
			RemoveItem(it)
			SelectedItem = Null
			Return
		EndIf
		If it\state < 1 Then
			it\state = 1
			IndevPillMsg("The label reads " + Chr(34) + "BIOHAZARD - DO NOT OPEN" + Chr(34) + ". Use it again if you really want to unscrew the cap.", 6)
			SelectedItem = Null
			Return
		EndIf
		If name = "scp214" Then
			IndevPillMsg("You unscrew the cap. A sour, dusty smell - and a few pale fibres drift up out of the vial and into your face.", 7)
		Else
			IndevPillMsg("You unscrew the cap. The fluid inside is full of tiny brass gears, and some of them are still turning. A few get on your hand.", 7)
		EndIf
		IndevInfect(name)
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-407 - the cassette player: use toggles PLAY / STOP, it isn't consumed
	If name = "scp407" Then
		If Pill407Playing Then
			IndevStop407()
			IndevPillMsg("You press STOP. The silence afterwards is almost painful.", 4)
		Else
			If Pill407Snd = 0 Then Pill407Snd = LoadSound_Strict("SFX\SCP\407\Song.ogg")
			Pill407CHN = PlaySound_Strict(Pill407Snd)
			Pill407Playing = True
			Pill407Item = it
			If Pill407Exposure < 1 Then
				IndevPillMsg("You press PLAY. Voices - dozens of them - rise out of the tiny speaker in a language you've never heard. It's the most beautiful thing you have ever heard.", 8)
			Else
				IndevPillMsg("You press PLAY again. The choir picks up exactly where it left off, somewhere deep inside you.", 6)
			EndIf
		EndIf
		SelectedItem = Null
		Return
	EndIf

	;SCP-006 - water from the spring near Astrakhan. It is simply "health".
	If name = "scp006" Then
		If Not CanUseItem(False, False, True) Then Return
		If Wearing714 = 1 Then
			IndevPillMsg("You break the four seals and drink. It tastes like cold mineral water, and nothing else happens. The ring on your finger feels heavier.", 7)
		Else
			If Injuries > 1.0 Or Bloodloss > 20 Then
				IndevPillMsg("You break the four seals and drink. Cold mineral water - then heat, spreading out from your stomach. You watch torn skin pull itself closed.", 8)
			Else
				IndevPillMsg("You break the four seals and drink. It tastes like ordinary mineral water, but every part of you suddenly feels impossibly, frighteningly healthy.", 8)
			EndIf
			Injuries = 0
			Bloodloss = 0
			Stamina = 100
			ResetDiseases()
			IndevCureViruses()
			Indev330RegrowHands()
			BlurTimer = 70*2
			Spring006Timer = 70*180 ;keeps knitting you back together for three minutes
		EndIf
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-006-B - SCP-914's concentrate of the spring. The same "health", turned all the way up.
	If name = "scp006b" Then
		If Not CanUseItem(False, False, True) Then Return
		If Wearing714 = 1 Then
			IndevPillMsg("You snap the ampoule and swallow the thick golden liquid. It's sweet, and warm, and the ring on your finger keeps every bit of it away from you.", 7)
		Else
			IndevPillMsg("You snap the ampoule and swallow. Liquid sunlight. Your heart hammers, your vision sharpens, and every cell in your body wakes up at once. You have never been this alive.", 9)
			Injuries = 0
			Bloodloss = 0
			Stamina = 100
			ResetDiseases()
			IndevCureViruses()
			IndevPillsCure()
			Indev330RegrowHands()
			BlurTimer = 70*4
			Spring006Timer = 0
			Spring006BTimer = 70*600 ;ten minutes of it
		EndIf
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-348 - the "thinking of you" bowl
	If name = "scp348" Then
		If Bowl348NoteTimer > 0 And Bowl348Note <> "" Then
			IndevPillMsg("Printed inside the empty bowl, in the same pale blue as the flowers: " + Chr(34) + Bowl348Note + Chr(34), 7)
		ElseIf Bowl348Ailing() Then
			IndevPillMsg("The bowl is empty, but it feels faintly warm, like it's getting something ready.", 5)
		ElseIf Injuries > 1.5 Or Bloodloss > 35 Then
			IndevPillMsg("An empty ceramic bowl with blue flowers. Whatever is wrong with you now is more than a bowl of soup can fix.", 6)
		Else
			IndevPillMsg("An empty ceramic bowl with blue flowers. Some characters are etched into the side - you can't read them, but they look kind.", 6)
		EndIf
		SelectedItem = Null
		Return
	EndIf
	If name = "scp348soup" Then
		If Not CanUseItem(False, False, True) Then Return
		Bowl348Meals = Bowl348Meals + 1
		Injuries = Max(0, Injuries - 1.0)
		Bloodloss = Max(0, Bloodloss - 30)
		Stamina = 100
		BlurTimer = 0
		Select Rand(1, 4)
			Case 1 IndevPillMsg("Noodles, a few slices of sausage, some soft greens. It tastes exactly like something you ate as a kid. Your scrapes stop stinging.", 7)
			Case 2 IndevPillMsg("Hot broth, carrots, a little too much salt, just the way it used to be. For a moment the facility is very far away.", 7)
			Case 3 IndevPillMsg("You finish every drop. You're eating alone in a containment facility, and somehow you don't feel lonely at all.", 7)
			Default IndevPillMsg("It's the kind of soup someone makes when you stay home sick. The ache in your cuts fades with every spoonful.", 7)
		End Select
		Bowl348Cooldown = 70*60*3
		IndevRelieveStress(40) ;it tastes like home
		;Addendum 348-2: sometimes a message is left behind
		If Rand(3) <> 1 Or Bowl348Meals = 1 Then
			Select Rand(1, 8)
				Case 1 Bowl348Note = "Eat well. You're doing fine."
				Case 2 Bowl348Note = "I'm proud of you."
				Case 3 Bowl348Note = "Be careful out there."
				Case 4 Bowl348Note = "Don't forget to rest."
				Case 5 Bowl348Note = "You're not alone."
				Case 6 Bowl348Note = "Come home safe."
				Case 7 Bowl348Note = "Wear something warm."
				Default Bowl348Note = "Thinking of you."
			End Select
			Bowl348NoteTimer = 70*60*8
		Else
			Bowl348Note = "" : Bowl348NoteTimer = 0
		EndIf
		IndevSwap348(it, "scp348")
		SelectedItem = Null
		Return
	EndIf

	;SCP-9282 - regenerating bandage: only goes on an actual wound
	If name = "scp9282" Then
		If Injuries <= 0 And Bloodloss <= 0 Then
			IndevPillMsg("You don't have a wound to put it on. Better save it.", 4)
			SelectedItem = Null
			Return
		EndIf
		If Not CanUseItem(False, True, True) Then Return
		If Injuries > 1.5 Then
			IndevPillMsg("You press the bandage over the worst of it. Underneath, you feel flesh knitting, bone setting, skin closing. When you peel it off there isn't even a scar.", 8)
		Else
			IndevPillMsg("You apply the bandage. A warm tingle, a faint itch, and the wound underneath is simply gone.", 6)
		EndIf
		Injuries = 0
		Bloodloss = Max(0, Bloodloss - 50)
		Indev330RegrowHands() ;it regrows amputated limbs, too
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-330 candy
	If Left(name, 8) = "candy330" Then
		If Not CanUseItem(False, False, True) Then Return
		IndevEatCandy330(name)
		IndevRelieveStress(10)
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	;SCP-8228 - the cupcake fixes everything. Then it takes something.
	If name = "scp8228" Then
		If Not CanUseItem(False, False, True) Then Return
		Injuries = 0
		Bloodloss = 0
		ResetDiseases()
		IndevPillsCure()
		Stamina = 100
		Pill8228Eaten = Pill8228Eaten + 1
		;the cost (Indev gameplay stand-in for the classified one): you are permanently, bone-deep tired
		BlinkEffect = 1.0 + 0.35 * Pill8228Eaten : BlinkEffectTimer = 99999
		StaminaEffect = Max(StaminaEffect, 1.0 + 0.2 * Pill8228Eaten) : StaminaEffectTimer = 99999
		Pill8228Timer = 70*Rnd(40,60)
		If Pill8228Eaten = 1 Then
			IndevPillMsg("The best cupcake you have ever eaten. Every ache, every cut, every bruise is gone. You feel perfect.", 7)
		Else
			IndevPillMsg("Another one. Perfect again. But you remember what the last one cost.", 6)
		EndIf
		Indev330RegrowHands()
		RemoveItem(it)
		SelectedItem = Null
		Return
	EndIf

	If Not CanUseItem(False, False, True) Then Return

	Select name
		Case "scpf02"
			If PillF02Timer > 0 Then
				IndevPillMsg("You swallow another Recovery Pill. The warmth in your chest starts over again, no faster than before.", 5)
			Else
				IndevPillMsg("You swallow the green and white capsule. A slow, pleasant warmth spreads out from your chest.", 5)
			EndIf
			PillF02Timer = 70*120
		Case "scp1642"
			IndevUse1642()
		Case "scp474"
			IndevPillMsg("You swallow the blue pill. It tastes of nothing at all. A placebo, surely.")
			Pill474Pending = True
		Case "scp483pill"
			Pill483Years = Pill483Years + 1
			If Pill483Years = 1 Then
				IndevPillMsg("You swallow the pink tablet. You are exactly one year younger. Your records agree. So, somehow, do you.", 7)
			Else
				IndevPillMsg("Another year gone. You are " + Pill483Years + " years younger than you were this morning. You always were.", 7)
			EndIf
			Injuries = Max(0, Injuries - 0.25)
			Stamina = 100
		Case "scp484"
			IndevPillMsg("You swallow the purple tablet. The world sharpens around other people's eyes.")
			Pill484Timer = 70*60*3
			Pill484Seen = ""
		Case "scp876r", "scp876g", "scp876b"
			IndevUse876(Right(name, 1))
		Case "scp2022"
			IndevUse2022()
		Case "scp2968"
			IndevPillMsg("Happy Hereafter. Your pulse slows to something calm and even. You feel oddly unafraid of dying.", 7)
			Bloodloss = Bloodloss * 0.5
			Pill2968Taken = True
		Case "scp3494"
			IndevPillMsg("superlax by dado. Luckily, you aren't constipated, so nothing happens. You try very hard not to think about the alternative.", 8)
		Case "scp3521"
			;(the test subject lasted thirty minutes; the player gets thirty seconds - SCP-500 can still save you)
			IndevPillMsg("The yellow gel capsule slides down easily. It tastes faintly of banana.", 5)
			If Pill3521Timer <= 0 Then Pill3521Timer = 70*30 : Pill3521Stage = 0
		Case "scp3866"
			IndevPillMsg("Your heartbeat slows. And slows. And...", 5)
			Pill3866Timer = 70*5
			BlurTimer = 70*5
		Case "scp3929"
			IndevPillMsg("You swallow the dark capsule. For a moment, nothing. Then your knuckles start to ache.")
			If Pill3929Stage = 0 Then Pill3929Stage = 1 : Pill3929Timer = 70*40
		Case "scp4193"
			IndevUse4193()
		Case "scp4257"
			IndevPillMsg("space drive by dado. Your spine locks perfectly straight and something like an engine starts idling in your chest. You can only go forward.", 8)
			Pill4257Timer = 70*30
			Stamina = 100
			StaminaEffect = 0.0 : StaminaEffectTimer = 30
		Case "scp4292"
			IndevUse4292()
		Case "scp5043"
			IndevPillMsg("dado's brainexplosion. You swallow the vitamin. Three...", 3)
			Pill5043Timer = 70*3
		Case "scp7521"
			If Pill7521Timer <= 0 Then
				IndevPillMsg("The capsule dissolves on your tongue almost instantly. You feel completely fine.")
				Pill7521Timer = 70*60
				Pill7521Stage = 0
			Else
				IndevPillMsg("It dissolves just as fast as the last one.")
			EndIf
	End Select

	If it <> Null Then RemoveItem(it)
	SelectedItem = Null
End Function

Function IndevUse483()
	Local n%, found.Items = Null, slot% = -1, nm$

	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If IndevIsPill(Inventory(n)\itemtemplate\name) Then found = Inventory(n) : slot = n : Exit
		EndIf
	Next

	If found = Null Then
		IndevPillMsg("The bottle is empty. It feels like it's waiting for a pill.", 4)
		Return
	EndIf

	nm = found\itemtemplate\displayname
	RemoveItem(found)

	Local it.Items = CreateItem("scp483pill", 1, 1, 1)
	it\Picked = True
	it\Dropped = -1
	it\itemtemplate\found = True
	Inventory(slot) = it
	HideEntity(it\collider)
	EntityParent(it\collider, 0)
	ItemAmount = ItemAmount + 1

	IndevPillMsg("You drop the " + nm + " into the bottle and give it a shake. A pale pink tablet rattles back out.", 6)
End Function

Function IndevUse876(col$)
	Local nm$
	Select col
		Case "r" nm = "red"
		Case "g" nm = "green"
		Default nm = "blue"
	End Select

	If Pill876First = "" Or Pill876Timer <= 0 Then
		Pill876First = col
		Pill876Timer = 70*60
		IndevPillMsg("You swallow the " + nm + " capsule. Nothing happens. Yet.")
	ElseIf Pill876First = col Then
		Pill876Timer = 70*60
		IndevPillMsg("Another " + nm + " one. Still nothing. Maybe the colours have to be different.")
	Else
		IndevPillDeath("Subject D-9341 was found deceased. Autopsy shows every atom of " + IndevElement876(Pill876First) + " in the subject's body had been converted into " + IndevElement876(col) + " at the same instant. Two empty SCP-876 capsules were recovered from the stomach.")
	EndIf
End Function

Function IndevElement876$(col$)
	Select col
		Case "r" Return "iron"
		Case "g" Return "chlorine"
		Default Return "neon"
	End Select
End Function

Function IndevUse2022()
	If Pill2022Window <= 0 Then Pill2022Doses = 0
	Pill2022Doses = Pill2022Doses + 1
	Pill2022Window = 70*60*5

	Select Pill2022Doses
		Case 1
			IndevPillMsg("Sunlight Pills. A tropical warmth spreads from your stomach to your fingertips. You feel like you've been on holiday for a week.", 7)
			Stamina = 100
			BlurTimer = 0
			LightFlash = 0.6
		Case 2
			IndevPillMsg("Too much sun. Your insides are burning, and your skin is glowing through your jumpsuit.", 7)
			Injuries = Injuries + 1.5
			LightFlash = 3
			CameraShake = 2
		Default
			IndevPillDeath("Subject D-9341 was found deceased, still glowing brightly enough to be located from the corridor. Internal organs were severely burned. Three SCP-2022 capsules were recovered from the stomach.")
	End Select
End Function

;---------------------------------------------------------------------
; SCP-214 / SCP-217 - virus infections, ~10 minutes to death.
; Cured by SCP-500, SCP-8228, or SCP-407's healing minute.
;---------------------------------------------------------------------

;start an infection (does nothing if the player already has that one)
Function IndevInfect(name$)
	If IndevMjolnirOn Then
		IndevPillMsg("The MJOLNIR's atmospheric filters seal instantly. Whatever was in there never reaches you.", 5)
		Return
	EndIf
	If name = "scp214" Then
		If Virus214Time <= 0 Then Virus214Time = 0.01 : Virus214Stage = 0 : Virus214Next = 0
	Else
		If Virus217Time <= 0 Then Virus217Time = 0.01 : Virus217Stage = 0 : Virus217Next = 0
	EndIf
End Function

;SCP-914 let a virus loose: anyone who comes within reach of the spill in the next few minutes catches it
Function IndevContaminate(name$, x#, y#, z#)
	If name = "scp214" Then
		Zone214X = x : Zone214Y = y : Zone214Z = z : Zone214Timer = 70*60*3
	Else
		Zone217X = x : Zone217Y = y : Zone217Z = z : Zone217Timer = 70*60*3
	EndIf
End Function

Function UpdateVirusZones()
	Local dx#, dy#, dz#
	If Zone214Timer > 0 Then
		Zone214Timer = Zone214Timer - FPSfactor
		dx = EntityX(Collider) - Zone214X : dy = EntityY(Collider) - Zone214Y : dz = EntityZ(Collider) - Zone214Z
		If dx*dx + dz*dz < 1.3*1.3 And Abs(dy) < 1.5 Then
			Zone214Timer = 0
			If Virus214Time <= 0 Then
				IndevPillMsg("Pale fibres are drifting in the air of the output booth. You breathe some of them in before you can stop yourself.", 7)
				IndevInfect("scp214")
			EndIf
		EndIf
	EndIf
	If Zone217Timer > 0 Then
		Zone217Timer = Zone217Timer - FPSfactor
		dx = EntityX(Collider) - Zone217X : dy = EntityY(Collider) - Zone217Y : dz = EntityZ(Collider) - Zone217Z
		If dx*dx + dz*dz < 1.3*1.3 And Abs(dy) < 1.5 Then
			Zone217Timer = 0
			If Virus217Time <= 0 Then
				IndevPillMsg("Tiny brass gears are scattered across the output booth floor. Some are still turning. One of them is on your hand.", 7)
				IndevInfect("scp217")
			EndIf
		EndIf
	EndIf
End Function

Function IndevCureViruses%()
	Local had% = (Virus214Time > 0 Or Virus217Time > 0)
	If Virus214Time > 0 Or Virus217Time > 0 Then
		StaminaEffect = 1.0 : StaminaEffectTimer = 0
	EndIf
	Virus214Time = 0 : Virus214Stage = 0
	Virus217Time = 0 : Virus217Stage = 0
	Return had
End Function

;SCP-214 - tissue turns to string, from the fingertips in
Function UpdateVirus214()
	If Virus214Time <= 0 Then Return
	Virus214Time = Virus214Time + FPSfactor / 70.0

	;milestones (seconds since infection)
	Local ms#[6]
	ms[0] = 60 : ms[1] = 180 : ms[2] = 300 : ms[3] = 420 : ms[4] = 540 : ms[5] = 600
	If Virus214Stage < 6 Then
		If Virus214Time >= ms[Virus214Stage] Then
			Select Virus214Stage
				Case 0 IndevPillMsg("Your fingertips have gone numb. There are fine white threads under your nails.", 6)
				Case 1
					IndevPillMsg("You scratch your forearm and a loose thread comes away. It doesn't hurt. It should hurt.", 7)
					StaminaEffect = 1.3 : StaminaEffectTimer = 99999
				Case 2
					IndevPillMsg("The muscle in your arms feels soft and fibrous. Every movement is weaker than the last.", 7)
					StaminaEffect = 1.7 : StaminaEffectTimer = 99999
					Injuries = Injuries + 0.3
				Case 3
					IndevPillMsg("You can barely close your hands. They're more string than flesh now.", 6)
					Injuries = Injuries + 0.5
					CameraShake = 1.0
				Case 4
					IndevPillMsg("You're coming apart at the seams. Literally.", 6)
					BlurTimer = 70*6
					StaminaEffect = 2.5 : StaminaEffectTimer = 99999
				Case 5
					IndevPillDeath("Subject D-9341 was recovered as a loose, roughly human-shaped heap of fine white string, still wearing an orange jumpsuit. SCP-214 infection had progressed to completion. The remains were incinerated.")
					Return
			End Select
			Virus214Stage = Virus214Stage + 1
			Virus214Next = 70*Rnd(25,40)
		EndIf
	EndIf

	;in between: small, creeping reminders
	If Virus214Stage >= 1 Then
		Virus214Next = Virus214Next - FPSfactor
		If Virus214Next <= 0 Then
			Select Rand(1,3)
				Case 1 IndevPillMsg("Something under your skin pulls taut, then goes slack.", 3)
				Case 2 IndevPillMsg("A thread is poking out of your wrist.", 3)
				Default IndevPillMsg("Your fingers twitch like someone is tugging on them.", 3)
			End Select
			Virus214Next = 70*Rnd(30,55)
		EndIf
	EndIf
End Function

;SCP-217 - the clockwork virus. Converted tissue doesn't bleed, but it doesn't last either
Function UpdateVirus217()
	If Virus217Time <= 0 Then Return
	Virus217Time = Virus217Time + FPSfactor / 70.0

	;brass doesn't bleed
	If Virus217Stage >= 2 Then Bloodloss = Max(0, Bloodloss - FPSfactor * 0.05)

	Local ms#[6]
	ms[0] = 60 : ms[1] = 180 : ms[2] = 300 : ms[3] = 420 : ms[4] = 540 : ms[5] = 660
	If Virus217Stage < 6 Then
		If Virus217Time >= ms[Virus217Stage] Then
			Select Virus217Stage
				Case 0 IndevPillMsg("Your little finger has gone stiff. Under the skin, something small and hard is turning. It ticks.", 7)
				Case 1
					IndevPillMsg("The cut on your hand isn't bleeding. There's a brass gear showing through it, spinning quietly.", 7)
					StaminaEffect = 1.3 : StaminaEffectTimer = 99999
				Case 2
					IndevPillMsg("Your whole arm moves with a faint whirr now. It's strong. It's not yours.", 7)
					StaminaEffect = 1.6 : StaminaEffectTimer = 99999
				Case 3
					IndevPillMsg("Your heartbeat has turned into a steady, precise tick-tock.", 6)
					StaminaEffect = 2.0 : StaminaEffectTimer = 99999
				Case 4
					IndevPillMsg("You can hear every gear inside you. Some of them are grinding.", 6)
					CameraShake = 1.0
					BlurTimer = 70*4
				Case 5
					IndevPillDeath("Subject D-9341 was found fully converted to a clockwork mechanism of brass-like alloy by SCP-217. The mechanism continued to walk in slow circles for three hours before it wound down.")
					Return
			End Select
			Virus217Stage = Virus217Stage + 1
			Virus217Next = 70*Rnd(20,30)
		EndIf
	EndIf

	;ticking, more and more often
	If Virus217Stage >= 1 Then
		Virus217Next = Virus217Next - FPSfactor
		If Virus217Next <= 0 Then
			If Virus217Snd = 0 Then Virus217Snd = LoadSound_Strict("SFX\SCP\217\Tick.ogg")
			PlaySound_Strict(Virus217Snd)
			Virus217Next = 70*Rnd(35,60) / Virus217Stage
		EndIf
	EndIf
End Function

;---------------------------------------------------------------------
; SCP-407 - the song. Exposure only builds while the tape is playing,
; and it never goes back down on its own (SCP-500 resets it to 60s):
;   0-60s   everything heals
;   60-180s benign growths - running wears you out faster, for good
;   180-240s bacteria and fungus - coughing, slowly getting hurt
;   240-300s it gets much worse
;   300s+   overgrowth
;---------------------------------------------------------------------

Function IndevStop407()
	If Pill407CHN <> 0 Then
		If ChannelPlaying(Pill407CHN) Then StopChannel(Pill407CHN)
	EndIf
	Pill407CHN = 0
	Pill407Playing = False
End Function

;SCP-348: only minor things - a scrape, a cut, a bit of blood - never anything serious
Function Bowl348Ailing%()
	If Injuries > 1.5 Or Bloodloss > 35 Then Return False
	Return (Injuries > 0.05 Or Bloodloss > 2)
End Function

;replace an SCP-348 in the inventory with its full/empty version, in the same slot
Function IndevSwap348(it.Items, newName$)
	Local n%, slot% = -1
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) = it Then slot = n : Exit
	Next
	If slot < 0 Then Return
	If SelectedItem = it Then SelectedItem = Null
	RemoveItem(it)
	Local it2.Items = CreateItem(newName, 1, 1, 1)
	it2\Picked = True
	it2\Dropped = -1
	it2\itemtemplate\found = True
	Inventory(slot) = it2
	HideEntity(it2\collider)
	EntityParent(it2\collider, 0)
	ItemAmount = ItemAmount + 1
End Function

;SCP-F02 - Recovery Pill: health comes back a little at a time over two minutes
Function UpdatePillF02()
	If PillF02Timer <= 0 Then Return
	PillF02Timer = PillF02Timer - FPSfactor
	If KillTimer < 0 Then PillF02Timer = 0 : Return
	Injuries = Max(0, Injuries - FPSfactor * 0.00045)
	Bloodloss = Max(0, Bloodloss - FPSfactor * 0.012)
	Stamina = Min(100, Stamina + FPSfactor * 0.08)
	If PillF02Timer <= 0 Then IndevPillMsg("The warmth from the Recovery Pill fades. You feel a lot better than you did.", 5)
End Function

Function UpdateBowl348()
	If Bowl348Cooldown > 0 Then Bowl348Cooldown = Bowl348Cooldown - FPSfactor
	If Bowl348NoteTimer > 0 Then
		Bowl348NoteTimer = Bowl348NoteTimer - FPSfactor
		If Bowl348NoteTimer <= 0 Then Bowl348Note = ""
	EndIf
	If Bowl348Cooldown > 0 Or KillTimer < 0 Then Return
	If Not Bowl348Ailing() Then Return

	Local n%
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "scp348" Then
				IndevSwap348(Inventory(n), "scp348soup")
				Bowl348Note = "" : Bowl348NoteTimer = 0 ;the words fade when a new meal comes
				Bowl348Cooldown = 70*60*3
				If MsgTimer <= 0 Then IndevPillMsg("The bowl in your bag has gone warm and heavy. You can smell broth.", 5)
				Return
			EndIf
		EndIf
	Next
End Function

Function UpdatePill407()
	If (Not Pill407Playing) Then Return

	;the player only plays while you're holding it
	Local n%, held% = False
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) = Pill407Item And Pill407Item <> Null Then held = True : Exit
	Next
	If (Not held) Then
		IndevStop407()
		IndevPillMsg("The tape clatters and stops.", 3)
		Return
	EndIf

	;the tape is ~2.5 minutes long; rewind and keep going
	If Pill407CHN = 0 Or (Not ChannelPlaying(Pill407CHN)) Then Pill407CHN = PlaySound_Strict(Pill407Snd)

	Local dt# = FPSfactor / 70.0
	Pill407Exposure = Pill407Exposure + dt

	If Pill407Exposure < 60 Then
		Injuries = Max(0, Injuries - dt * 0.06)
		Bloodloss = Max(0, Bloodloss - dt * 1.5)
		If Pill407Stage = 0 And Pill407Exposure > 20 Then
			Pill407Stage = 1
			IndevPillMsg("Every cut, every bruise, every ache is fading as you listen. Your skin feels new.", 6)
		EndIf
	ElseIf Pill407Exposure < 180 Then
		If Pill407Stage < 2 Then
			Pill407Stage = 2
			Injuries = 0 : Bloodloss = 0
			ResetDiseases()
			If IndevCureViruses() Then
				IndevPillMsg("The numbness, the threads, the ticking - all gone. You feel better than you ever have in your life. Maybe you should stop the tape now.", 8)
			Else
				IndevPillMsg("You feel better than you ever have in your life. Maybe you should stop the tape now.", 7)
			EndIf
			Pill407Next = 70*15
		EndIf
		Pill407Next = Pill407Next - FPSfactor
		If Pill407Next <= 0 Then
			Select Rand(1,3)
				Case 1 IndevPillMsg("There's a hard lump under the skin of your forearm. It wasn't there a minute ago.", 5)
				Case 2 IndevPillMsg("Your knuckles have grown thick, calcified knots. They ache when you make a fist.", 5)
				Default IndevPillMsg("Soft growths are swelling along your neck and shoulders. They don't hurt. Much.", 5)
			End Select
			Injuries = Injuries + 0.1
			StaminaEffect = Max(StaminaEffect, 1.0 + (Pill407Exposure - 60) / 240.0) : StaminaEffectTimer = 99999
			CameraShake = 0.5
			Pill407Next = 70*Rnd(25,40)
		EndIf
	ElseIf Pill407Exposure < 300 Then
		If Pill407Stage < 3 Then
			Pill407Stage = 3
			IndevPillMsg("Your throat is thick. Something is growing in your lungs, and the air tastes of mould. The choir is still beautiful.", 7)
			Pill407Next = 70*10
		EndIf
		Local rate# = 0.01
		If Pill407Exposure > 240 Then rate = 0.03
		Injuries = Injuries + dt * rate
		StaminaEffect = Max(StaminaEffect, 1.8) : StaminaEffectTimer = 99999
		Pill407Next = Pill407Next - FPSfactor
		If Pill407Next <= 0 Then
			Select Rand(1,4)
				Case 1 IndevPillMsg("You double over coughing. Something grey and fibrous comes up.", 4)
				Case 2 IndevPillMsg("Pale fungus is spreading across the back of your hand.", 4)
				Case 3 IndevPillMsg("Every breath rattles.", 3)
				Default IndevPillMsg("Your stomach cramps. Something inside you is growing faster than you are.", 4)
			End Select
			BlurTimer = 70*3
			CameraShake = 1.0 + (Pill407Exposure > 240)
			Pill407Next = 70*Rnd(10,18)
		EndIf
	Else
		IndevStop407()
		IndevPillDeath("Subject D-9341 was located by the sound of a choir coming from a small cassette player. The subject could not be separated from the moss, fungi and unidentified organisms that had grown through the corridor around them, and was declared deceased. The player was recovered intact. The tape had not finished.")
	EndIf
End Function

;SCP-1642 - you're already an adult, so you just get the worst of being a teenager again
Function IndevUse1642()
	If Pill1642Window <= 0 Then Pill1642Doses = 0
	Pill1642Doses = Pill1642Doses + 1
	Pill1642Window = 70*60*10

	Select Pill1642Doses
		Case 1
			IndevPillMsg("Dr. Wondertainment's Insta-teen! It tastes like bubblegum. Your voice cracks, your face breaks out, and suddenly everything is SO unfair.", 8)
			Stamina = 100
			StaminaEffect = 0.7 : StaminaEffectTimer = 120  ;boundless teenage energy
			Pill1642Mood = 70*Rnd(20,35)
			Pill1642Moods = 4
		Case 2
			IndevPillMsg("A second one. Your heart is hammering. Your palms are soaked. Everyone is looking at you. Everyone.", 7)
			StaminaEffect = 1.6 : StaminaEffectTimer = 90
			BlurTimer = 70*6
			CameraShake = 2
			Pill1642Mood = 70*Rnd(15,25)
			Pill1642Moods = 3
		Default
			IndevPillMsg("Your thoughts go bright, then thin, then very, very quiet.", 5)
			Pill1642Coma = 70*5
			BlurTimer = 70*5
	End Select
End Function

Function UpdatePill1642()
	If Pill1642Window > 0 Then Pill1642Window = Pill1642Window - FPSfactor

	If Pill1642Coma > 0 Then
		Pill1642Coma = Pill1642Coma - FPSfactor
		BlurTimer = Max(BlurTimer, 70)
		If Pill1642Coma <= 0 Then
			IndevPillDeath("Subject D-9341 was found unresponsive, with three SCP-1642 wrappers nearby. Scans show extreme and irreversible brain damage. The subject has been in a coma since, and is not expected to wake.")
		EndIf
		Return
	EndIf

	If Pill1642Moods <= 0 Then Return
	Pill1642Mood = Pill1642Mood - FPSfactor
	If Pill1642Mood > 0 Then Return

	If Pill1642Doses >= 2 Then
		Select Rand(1,3)
			Case 1 IndevPillMsg("Your chest is tight. You can't get enough air.", 4)
			Case 2 IndevPillMsg("Something terrible is about to happen. You're sure of it.", 4)
			Default IndevPillMsg("Your hands won't stop shaking.", 4)
		End Select
		BlurTimer = 70*2
		CameraShake = 1.0
	Else
		Select Rand(1,4)
			Case 1 IndevPillMsg("Nobody in this facility understands you. Nobody.", 4)
			Case 2 IndevPillMsg("You catch your reflection. Is that a new pimple?", 4)
			Case 3 IndevPillMsg("You feel like slamming the next door you go through.", 4)
			Default IndevPillMsg("Your voice cracks when you mutter to yourself.", 4)
		End Select
	EndIf
	Pill1642Moods = Pill1642Moods - 1
	Pill1642Mood = 70*Rnd(25,40)
End Function

Function IndevUse4193()
	If Pill4193Count = 0 Then
		IndevPillMsg("migraine medicine e. The headache you didn't know you had is simply gone. Your head has never been this clear.")
		BlurTimer = 0
		CameraShake = 0
	Else
		IndevPillMsg("Your eyes feel... smaller. Everything is sharper. Much, much sharper.")
		BlinkEffect = 0.6 : BlinkEffectTimer = 99999   ;tiny eyes dry out slower
		Pill4193Timer = 70*Rnd(20,40)
	EndIf
	Pill4193Count = Pill4193Count + 1
End Function

Function IndevUse4292()
	Pill4292Effect = Rand(1,4)
	Pill4292Timer = 70*60*3
	Pill4292Next = 70*Rnd(15,25)
	Pill4292Withdrawal = 0
	Select Pill4292Effect
		Case 1 IndevPillMsg("freaky pills by dado. Soft cartoon feathers are sprouting all over your arms. Your legs really, really want to dance.", 7)
		Case 2 IndevPillMsg("freaky pills by dado. Your skin has gone clown-white and your nose is round and red. It honks when you touch it.", 7)
		Case 3 IndevPillMsg("freaky pills by dado. Your shadow has started moving half a second after you do.", 7)
		Default IndevPillMsg("freaky pills by dado. Your fingers have too many joints now. They flex on their own.", 7)
	End Select
End Function

;SCP-500: cures every ongoing pill effect in this file (and the other Indev pill effects)
Function IndevPillsCure()
	Pill876First = "" : Pill876Timer = 0
	Pill2022Doses = 0 : Pill2022Window = 0
	If Pill3929Stage > 0 Then StaminaEffect = 1.0 : StaminaEffectTimer = 0
	Pill3929Stage = 0 : Pill3929Timer = 0
	If Pill4193Count > 1 Then BlinkEffect = 1.0 : BlinkEffectTimer = 0
	Pill4193Count = 0 : Pill4193Timer = 0
	Pill4292Effect = 0 : Pill4292Timer = 0 : Pill4292Withdrawal = 0
	Pill7521Timer = 0 : Pill7521Stage = 0
	Pill3521Timer = 0 : Pill3521Stage = 0
	Pill1642Doses = 0 : Pill1642Window = 0 : Pill1642Moods = 0 : Pill1642Coma = 0
	I867Seed = 0 : I867Pain = 0 ;SCP-867's seed dies too (IndevU29.bb)
	I4427Trait = 0 ;and an SCP-4427-A heat trait calms (IndevU30.bb)
	I207On = False : I207Boost = 0 : I1079Count = 0 : I1650Poison = 0 ;SCP-207, SCP-1079, SCP-1650 (IndevU31.bb)
	If I1563Grab > 0 Then I1563Grab = 1 ;SCP-1563 lets go (IndevU33.bb)
	I34Sprout = 0 : I34Sleep = 0 ;SCP-1255's sprout dies, SCP-3866's sleep ends (IndevU34.bb)
	I36Cotton = 0 ;SCP-1921-A2 is dissolved (IndevU36.bb)
	Indev38Cure() ;SCP-1117-3 is cured (IndevU38.bb)
	Indev42Cure() ;SCP-439 is coughed up (IndevU42.bb)
	IndevCureViruses()
	;SCP-407: the growths and infection go, the "healthy minute" doesn't come back
	If Pill407Exposure > 60 Then
		Pill407Exposure = 60 : Pill407Stage = 2 : Pill407Next = 70*15
		StaminaEffect = 1.0 : StaminaEffectTimer = 0
	EndIf
	Indev2077Doses = 0 : Indev2077Timer = 0
	Indev7985Doses = 0 : Indev7985Timer = 0
	Indev5604Timer = 0
End Function

;---------------------------------------------------------------------
; per-frame (called from UpdateIndev)
;---------------------------------------------------------------------

Function UpdateIndevPills()
	UpdatePill474()
	UpdatePill484()
	UpdatePill1642()
	UpdatePill407()
	UpdateBowl348()
	UpdatePillF02()
	UpdateVirusZones()
	UpdateVirus214()
	UpdateVirus217()

	;SCP-006-B: wounds close almost as they open, you don't tire, nothing can take hold
	If Spring006BTimer > 0 Then
		Spring006BTimer = Spring006BTimer - FPSfactor
		Injuries = Max(0, Injuries - FPSfactor * 0.004)
		Bloodloss = Max(0, Bloodloss - FPSfactor * 0.4)
		Stamina = Min(100, Stamina + FPSfactor * 0.6)
		If Virus214Time > 0 Or Virus217Time > 0 Then IndevCureViruses()
		If Spring006BTimer <= 0 Then
			Spring006BTimer = 0
			BlurTimer = 70*6
			StaminaEffect = Max(StaminaEffect, 1.3) : StaminaEffectTimer = 70*60
			IndevPillMsg("The golden heat drains out of you all at once. Your legs shake. Your cells slow back down to merely human, and they are exhausted.", 8)
		EndIf
	EndIf

	;SCP-006: vastly improved tissue repair, while it lasts
	If Spring006Timer > 0 Then
		Spring006Timer = Spring006Timer - FPSfactor
		Injuries = Max(0, Injuries - FPSfactor * 0.0006)
		Bloodloss = Max(0, Bloodloss - FPSfactor * 0.05)
		If Spring006Timer <= 0 Then
			Spring006Timer = 0
			IndevPillMsg("The warmth in your blood fades. Somewhere, you're sure, a form has already been filed to have you incinerated.", 7)
		EndIf
	EndIf

	;SCP-8228: the bill arrives a little after dessert
	If Pill8228Timer > 0 Then
		Pill8228Timer = Pill8228Timer - FPSfactor
		If Pill8228Timer <= 0 Then
			IndevPillMsg("A heaviness settles into you that no amount of rest will lift. Something was taken in exchange. You can feel exactly where it used to be.", 8)
			BlurTimer = 70*3
		EndIf
	EndIf

	If Pill876Timer > 0 Then Pill876Timer = Pill876Timer - FPSfactor
	If Pill2022Window > 0 Then Pill2022Window = Pill2022Window - FPSfactor

	If Pill3521Timer > 0 Then
		Pill3521Timer = Pill3521Timer - FPSfactor
		If Pill3521Stage = 0 And Pill3521Timer < 70*20 Then
			Pill3521Stage = 1
			IndevPillMsg("A cramp twists through your stomach. Then another. Something in there is getting heavier.", 5)
			CameraShake = Max(CameraShake, 1.0)
		ElseIf Pill3521Stage = 1 And Pill3521Timer < 70*10 Then
			Pill3521Stage = 2
			PlaySound_Strict(LoadTempSound("SFX\SCP\294\retch1.ogg"))
			IndevPillMsg("Your belly is swelling against your uniform. You can smell bananas. Lots of bananas. You need SCP-500, NOW.", 6)
		EndIf
		If Pill3521Stage = 2 Then
			CameraShake = Max(CameraShake, 1.5)
			BlurTimer = Max(BlurTimer, 70)
			CurrSpeed = CurrSpeed * 0.9
			Stamina = Min(Stamina, 20)
		EndIf
		If Pill3521Timer <= 0 Then
			IndevPillDeath("Subject D-9341 was found deceased. Cause of death: stomach rupture caused by approximately 9.15 million kilograms of unpeeled bananas. Recovery of the remains is expected to take several weeks.")
			Return
		EndIf
	EndIf

	If Pill3866Timer > 0 Then
		Pill3866Timer = Pill3866Timer - FPSfactor
		BlurTimer = Max(BlurTimer, 70)
		If Pill3866Timer <= 0 Then
			IndevPillDeath("Subject D-9341 was recovered alive but unresponsive. The subject's heart beats roughly once every 34 days. They have been moved to long-term storage in the Site-19 medical wing, where they are expected to remain indefinitely.")
			Return
		EndIf
	EndIf

	UpdatePill3929()
	UpdatePill4193()

	If Pill4257Timer > 0 Then
		Pill4257Timer = Pill4257Timer - FPSfactor
		If Pill4257Timer <= 0 Then IndevPillMsg("The engine in your chest sputters out. You're a person again. Mostly.", 5)
	EndIf

	UpdatePill4292()
	UpdatePill5043()
	UpdatePill7521()
End Function

Function UpdatePill474()
	If (Not Pill474Pending) Then Return
	If Indev990State > 0 Then Pill474Rest = 0 : Return

	;resting (holding the blink key) for a few seconds tunes you into the broadcast
	If KeyDown(KEY_BLINK) And BlinkTimer < 0 And (Not IsAnyMenuOpen()) Then
		Pill474Rest = Pill474Rest + FPSfactor
	Else
		Pill474Rest = 0
	EndIf

	If Pill474Rest > 70*3 Then
		Pill474Rest = 0
		Pill474Pending = False
		Indev990State = 1
		Indev990Variant = 8 ;SCP-474 broadcast dream, see Indev990Line
		Indev990CHN = PlaySound_Strict(LoadTempSound("SFX\SCP\079\Broadcast"+Rand(1,7)+".ogg"))
	EndIf
End Function

Function UpdatePill484()
	If Pill484Timer <= 0 Then Return
	Pill484Timer = Pill484Timer - FPSfactor
	If Pill484Timer <= 0 Then
		IndevPillMsg("The edges of other people's eyes stop glittering. The V has worn off.", 5)
		Return
	EndIf

	Local n.NPCs, key$
	For n = Each NPCs
		If n\Collider <> 0 And n\obj <> 0 And (Not n\IsDead) Then
			If EntityDistance(n\Collider, Collider) < 5.0 Then
				key = "[" + n\NPCtype + "]"
				If Instr(Pill484Seen, key) = 0 Then
					If EntityInView(n\obj, Camera) And EntityVisible(Camera, n\Collider) Then
						Pill484Seen = Pill484Seen + key
						IndevSteal484(n\NPCtype)
						Return
					EndIf
				EndIf
			EndIf
		EndIf
	Next
End Function

Function IndevSteal484(t%)
	BlurTimer = 70*3
	CameraShake = 1.0
	Select t
		Case NPCtype173
			IndevPillMsg("You meet its painted eyes. You see yourself from across a dark cell, frozen between blinks. It has been waiting a very, very long time.", 8)
		Case NPCtypeOldMan
			IndevPillMsg("His eyes find yours. Rust. Corridors that fold in on themselves. Decades of patient hunting. You taste corrosion for a minute afterwards.", 8)
			Injuries = Injuries + 0.2
		Case NPCtypeGuard, NPCtypeMTF
			IndevPillMsg("Eye contact. A morning briefing, bad coffee, a keypad under a flickering light. The maintenance code is " + AccessCode + ".", 9)
		Case NPCtypeD
			IndevPillMsg("Eye contact. An orange jumpsuit. A cell. A number where a name used to be. It feels a lot like your own.", 7)
		Case NPCtype5131
			IndevPillMsg("There is nothing behind its eyes. Nothing at all, except the sound of a bell.", 7)
		Case NPCtypeClerk
			IndevPillMsg("Eye contact. A reception desk. Endless forms. Somebody's birthday cake in the break room.", 7)
		Default
			IndevPillMsg("Eye contact. Someone else's memories wash over you: a childhood you never had, a name you'll never use.", 7)
	End Select
End Function

Function UpdatePill3929()
	If Pill3929Stage = 0 Or Pill3929Stage > 4 Then Return
	Pill3929Timer = Pill3929Timer - FPSfactor
	If Pill3929Timer > 0 Then Return

	Select Pill3929Stage
		Case 1 IndevPillMsg("There's grey in your stubble. Your joints crack when you move.")
		Case 2 IndevPillMsg("Your back protests every step. The skin on your hands has gone thin and papery.")
		Case 3 IndevPillMsg("Your reflection in the glass is somebody's grandfather.")
		Case 4 IndevPillMsg("Seventy years in an afternoon. At least you're still standing. For now.", 7)
	End Select
	;every stage, running wears you out faster - permanently
	StaminaEffect = 1.0 + Pill3929Stage * 0.25 : StaminaEffectTimer = 99999
	CameraShake = 0.5
	Pill3929Stage = Pill3929Stage + 1
	Pill3929Timer = 70*45
End Function

Function UpdatePill4193()
	If Pill4193Count < 2 Then Return
	Pill4193Timer = Pill4193Timer - FPSfactor
	If Pill4193Timer > 0 Then Return

	;microscopic vision: the image lurches in, then the hallucination
	CurrCameraZoom = Min(10 + Pill4193Count * 6, 40)
	Select Rand(1,4)
		Case 1 IndevPillMsg("Tiny things are crawling over the walls. Mites. They were always there.")
		Case 2 IndevPillMsg("You can see every pore in the concrete. Each one is a cavern, and something lives in each cavern.")
		Case 3 IndevPillMsg("Something microscopic just looked back at you.")
		Default IndevPillMsg("The dust in the air is full of faces.")
	End Select
	Pill4193Timer = 70*60*Rnd(1.5,3) / Min(Pill4193Count - 1, 3)
End Function

Function UpdatePill4292()
	If Pill4292Effect > 0 Then
		Pill4292Timer = Pill4292Timer - FPSfactor
		If Pill4292Timer <= 0 Then
			Pill4292Effect = 0
			Pill4292Withdrawal = 70*60*10
			Pill4292Next = 70*20
			IndevPillMsg("The alteration fades. Almost immediately, you want another pill. Badly.", 6)
			Return
		EndIf
		Pill4292Next = Pill4292Next - FPSfactor
		If Pill4292Next <= 0 Then
			Select Pill4292Effect
				Case 1 IndevPillMsg("Your feet do a little shuffle on their own.", 4) : CameraShake = 1.5
				Case 2 IndevPillMsg("Honk.", 3)
				Case 3 IndevPillMsg("Your shadow waves at you. You weren't waving.", 4)
				Default IndevPillMsg("Your fingers drum a rhythm you don't know.", 4)
			End Select
			Pill4292Next = 70*Rnd(20,35)
		EndIf
		Return
	EndIf

	If Pill4292Withdrawal > 0 Then
		Pill4292Withdrawal = Pill4292Withdrawal - FPSfactor
		;shaky and winded the whole time, and it gets dangerous as it drags on
		StaminaEffect = Max(StaminaEffect, 1.5) : StaminaEffectTimer = Max(StaminaEffectTimer, 2)
		If Pill4292Withdrawal < 70*60*6 Then Injuries = Injuries + FPSfactor * 0.00005
		Pill4292Next = Pill4292Next - FPSfactor
		If Pill4292Next <= 0 Then
			Select Rand(1,3)
				Case 1 IndevPillMsg("You need another one. Your hands won't stop shaking.", 4)
				Case 2 IndevPillMsg("Cold sweat. Your heart is racing. Where are the pills?", 4)
				Default IndevPillMsg("Every inch of you itches for a rainbow.", 4)
			End Select
			BlurTimer = 70*3
			Pill4292Next = 70*Rnd(40,70)
		EndIf
		If Pill4292Withdrawal <= 0 Then IndevPillMsg("The craving finally loosens its grip.", 5)
	EndIf
End Function

Function UpdatePill5043()
	If Pill5043Timer > 0 Then
		Pill5043Timer = Pill5043Timer - FPSfactor
		If Pill5043Timer <= 0 Then
			;BOOM
			PlaySound_Strict(DamageSFX(Rand(0,1)))
			LightFlash = 2
			CameraShake = 4
			BlurTimer = 70*8
			Pill5043Blind = 70*3
			Local e% = LinePick(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, -5, 0)
			If e <> 0 Then
				Local de.Decals = CreateDecal(3, EntityX(Collider), PickedY() + 0.005, EntityZ(Collider), 90, Rand(360), 0)
				de\Size = 0.8 : ScaleSprite(de\obj, de\Size, de\Size)
			EndIf
			IndevPillMsg("", 1)
		EndIf
		Return
	EndIf

	If Pill5043Blind > 0 Then
		;no head, no eyes, no walking
		Pill5043Blind = Pill5043Blind - FPSfactor
		BlinkTimer = -10
		UnableToMove = True
		If Pill5043Blind <= 0 Then
			UnableToMove = False
			IndevPillMsg("Wet sounds. Pressure. Your head pulls itself back together, piece by piece. Everything works. You have a new appreciation for the phrase " + Chr(34) + "mind-blowing" + Chr(34) + ".", 8)
		EndIf
	EndIf
End Function

Function UpdatePill7521()
	If Pill7521Timer <= 0 Then Return
	Pill7521Timer = Pill7521Timer - FPSfactor

	If Pill7521Stage = 0 And Pill7521Timer < 70*30 Then
		Pill7521Stage = 1
		IndevPillMsg("Your jumpsuit feels a little loose.")
	ElseIf Pill7521Stage = 1 And Pill7521Timer < 70*12 Then
		Pill7521Stage = 2
		IndevPillMsg("Your hands. Are they smaller? Why is the floor closer?")
		CameraShake = 1.0
	ElseIf Pill7521Timer <= 0 Then
		IndevPillDeath("An empty orange jumpsuit was recovered from the facility floor. Inside it was a human fetus, approximately twelve weeks developed, genetically identical to Subject D-9341. The regression took two seconds.")
	EndIf
End Function

;---------------------------------------------------------------------
; death hook: SCP-2968 changes what happens after
;---------------------------------------------------------------------

Function IndevPillsOnDeath()
	If Pill407Playing Then IndevStop407()
	If Pill2968Taken And (Not Pill2968Shown) Then
		Pill2968Shown = True
		DeathMSG = DeathMSG + " Recovery teams noted that the subject's face showed an expression of complete and total peace."
	EndIf
End Function

;---------------------------------------------------------------------
; SCP-914 (called from Use914 in Main.bb)
;---------------------------------------------------------------------

Function IndevRefinePill(item.Items, setting$, x#, y#, z#)
	Local name$ = item\itemtemplate\name
	Local it2.Items, d.Decals, r%, g%, b%

	;SCP-770: crushing the flask lets the mould out into the output booth; anything finer just polishes the iron
	If name = "scp770" Then
		If setting = "rough" Or setting = "coarse" Then
			IndevRelease770(x, y, z)
		Else
			it2 = CreateItem("scp770", x, y, z)
		EndIf
		RemoveItem(item)
		Return
	EndIf

	If name = "scp458" Then
		IndevRefine458(item, setting, x, y, z)
		Return
	EndIf

	If name = "scp1471" Then
		IndevRefine1471(item, setting, x, y, z)
		Return
	EndIf

	If name = "scp963" Or name = "scp2295" Then
		IndevRefine963(item, setting, x, y, z)
		Return
	EndIf

	If name = "scp109" Then
		IndevRefine109(item, setting, x, y, z)
		Return
	EndIf

	If name = "scp268" Then
		IndevRefine268(item, setting, x, y, z)
		Return
	EndIf

	If name = "indevration" Then
		IndevRefineRation(item, setting, x, y, z)
		Return
	EndIf
	If name = "scp085" Then
		IndevRefine085(item, setting, x, y, z)
		Return
	EndIf
	If name = "scp006b" Then
		If Indev914Refine37(item, setting, x, y, z) Then Return ;SCP-028's recipe (IndevU37.bb)
	EndIf
	If name = "scp770" Then
		Indev914Refine770(item, setting, x, y, z)
		Return
	EndIf
	If name = "indevwater" Then
		IndevRefineWater(item, setting, x, y, z)
		Return
	EndIf

	If name = "scp113" Then
		IndevRefine113(item, setting, x, y, z)
		Return
	EndIf

	If IsDoll693(name) Then
		IndevRefine693(item, setting, x, y, z)
		Return
	EndIf

	;SCP-214 / SCP-217 vials: SCP-914 opens them. Whatever comes out, the virus is loose in the output booth
	If name = "scp214" Or name = "scp217" Then
		;a spill either way - the cap comes off, or the whole vial is crushed
		d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
		If name = "scp214" Then
			EntityColor(d\obj, 206, 190, 168)
		Else
			EntityColor(d\obj, 176, 132, 52)
		EndIf
		If setting = "rough" Or setting = "coarse" Then
			d\Size = 0.3 : EntityAlpha(d\obj, 0.85) : ScaleSprite(d\obj, d\Size, d\Size)
		Else
			d\Size = 0.12 : EntityAlpha(d\obj, 0.7) : ScaleSprite(d\obj, d\Size, d\Size)
			;the cap has been unscrewed "very carefully" - an open vial comes out
			it2 = CreateItem(name, x, y, z)
			it2\state = 2
		EndIf
		IndevContaminate(name, x, y, z)
		RemoveItem(item)
		Return
	EndIf

	;SCP-407: the player can be refined, the song can't
	If name = "scp407" Then
		If Pill407Item = item Then IndevStop407()
		If setting = "rough" Or setting = "coarse" Then
			d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
			d\Size = 0.2 : EntityColor(d\obj, 60, 64, 74) : ScaleSprite(d\obj, d\Size, d\Size)
			;a scrap of tape survives in the debris - and it is still SCP-407
			it2 = CreateItem("scp407", x, y, z)
		Else
			it2 = CreateItem("scp407", x, y, z)
		EndIf
		RemoveItem(item)
		Return
	EndIf

	;the two non-pills
	;SCP-006 - the container breaks, the water doesn't care
	If name = "scp006" Then
		If setting = "rough" Or setting = "coarse" Then
			d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
			d\Size = 0.25 : EntityColor(d\obj, 110, 150, 165) : EntityAlpha(d\obj, 0.6) : ScaleSprite(d\obj, d\Size, d\Size)
		ElseIf setting = "fine" Or setting = "very fine" Then
			;914 distils the spring down into something far stronger
			it2 = CreateItem("scp006b", x, y, z)
		Else
			it2 = CreateItem("scp006", x, y, z)
		EndIf
		RemoveItem(item)
		Return
	EndIf

	;SCP-006-B - Rough/Coarse dilutes it back to spring water; it can't be refined any further
	If name = "scp006b" Then
		If setting = "rough" Or setting = "coarse" Then
			it2 = CreateItem("scp006", x, y, z)
		Else
			it2 = CreateItem("scp006b", x, y, z)
		EndIf
		RemoveItem(item)
		Return
	EndIf

	If name = "lemon" Then
		Select setting
			Case "rough", "coarse"
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				EntityColor(d\obj, 240, 210, 40)
				d\Size = 0.14 : ScaleSprite(d\obj, d\Size, d\Size) ;juiced
			Case "1:1"
				it2 = CreateItem("lemon", x, y, z)
			Default
				;when life gives you lemons...
				it2 = CreateItem("lemon", x, y, z)
				it2 = CreateItem("lemon", x + 0.05, y, z)
		End Select
		RemoveItem(item)
		Return
	EndIf

	If name = "mjolnir" Then
		Select setting
			Case "rough", "coarse"
				it2 = CreateItem("veryfinevest", x, y, z) ;stripped down to a set of Dragonium plates
			Default
				it2 = CreateItem("mjolnir", x, y, z) ;nothing in the machine can improve on it
		End Select
		RemoveItem(item)
		Return
	EndIf

	If name = "scp202" Then
		Select setting
			Case "rough", "coarse"
				;the case cracks, and whatever it was holding leaks out as a flash
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				EntityColor(d\obj, 150, 60, 180)
				d\Size = 0.15 : ScaleSprite(d\obj, d\Size, d\Size)
				it2 = CreateItem("scp202", x, y, z) ;it reassembles - the anomaly survives
			Default
				it2 = CreateItem("scp202", x, y, z)
		End Select
		RemoveItem(item)
		Return
	EndIf

	If name = "cogglasses" Then
		Select setting
			Case "rough", "coarse"
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				EntityColor(d\obj, 60, 150, 150)
				d\Size = 0.12 : ScaleSprite(d\obj, d\Size, d\Size) ;crushed filter film and wire
			Default
				it2 = CreateItem("cogglasses", x, y, z) ;the filter film survives, nothing to refine
		End Select
		RemoveItem(item)
		Return
	EndIf

	If name = "scp348" Or name = "scp348soup" Then
		Select setting
			Case "rough", "coarse"
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				EntityColor(d\obj, 225, 228, 235)
				d\Size = 0.2 : ScaleSprite(d\obj, d\Size, d\Size) ;ceramic dust and shards
			Case "1:1"
				it2 = CreateItem("emptycup", x, y, z) ;a plain ceramic cup, nothing kind about it
			Default
				it2 = CreateItem("scp348", x, y, z) ;it comes out empty, and exactly the same
		End Select
		RemoveItem(item)
		Return
	EndIf

	If name = "scp9282" Or name = "scp8228" Then
		Select setting
			Case "rough", "coarse"
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				If name = "scp8228" Then
					EntityColor(d\obj, 80, 45, 25)
				Else
					EntityColor(d\obj, 214, 170, 132)
				EndIf
				d\Size = 0.18 : ScaleSprite(d\obj, d\Size, d\Size)
			Case "1:1"
				If name = "scp9282" Then it2 = CreateItem("firstaid", x, y, z) Else it2 = CreateItem("scp8228", x, y, z)
			Default
				it2 = CreateItem(name, x, y, z) ;the anomaly survives any refinement
		End Select
		RemoveItem(item)
		Return
	EndIf

	Select setting
		Case "rough", "coarse"
			If name = "scp483" Then
				;a crushed bottle, nothing more
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				d\Size = 0.2 : EntityColor(d\obj, 200, 110, 30) : ScaleSprite(d\obj, d\Size, d\Size)
			Else
				IndevPillColor(name)
				d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
				d\Size = 0.15 : EntityColor(d\obj, IndevPillR, IndevPillG, IndevPillB) : EntityAlpha(d\obj, 0.85)
				ScaleSprite(d\obj, d\Size, d\Size)
			EndIf
		Case "1:1"
			Select name
				Case "scp474"    it2 = CreateItem("pill", x, y, z)       ;chemically identical to a placebo, after all
				Case "scp876r"   it2 = CreateItem("scp876g", x, y, z)    ;the colour code shifts along
				Case "scp876g"   it2 = CreateItem("scp876b", x, y, z)
				Case "scp876b"   it2 = CreateItem("scp876r", x, y, z)
				Default          it2 = CreateItem(name, x, y, z)
			End Select
		Case "fine", "very fine"
			Select name
				Case "scp483"     it2 = CreateItem("scp483", x, y, z)
				Case "scp483pill" If setting = "very fine" Then it2 = CreateItem("scp500", x, y, z) Else it2 = CreateItem("pill", x, y, z)
				Case "scp4193"    it2 = CreateItem("scp4193", x, y, z)   ;already "perfect" migraine medicine
				Default           it2 = CreateItem("pill", x, y, z)
			End Select
	End Select

	RemoveItem(item)
End Function

Function IndevPillColor(name$)
	Select name
		Case "scp1642"         IndevPillR = 176 : IndevPillG = 88  : IndevPillB = 205
		Case "scp474"          IndevPillR = 78  : IndevPillG = 120 : IndevPillB = 220
		Case "scp483pill"      IndevPillR = 236 : IndevPillG = 205 : IndevPillB = 218
		Case "scp484"          IndevPillR = 120 : IndevPillG = 62  : IndevPillB = 165
		Case "scp876r"         IndevPillR = 205 : IndevPillG = 40  : IndevPillB = 40
		Case "scp876g"         IndevPillR = 55  : IndevPillG = 165 : IndevPillB = 75
		Case "scp876b"         IndevPillR = 55  : IndevPillG = 95  : IndevPillB = 205
		Case "scp2022"         IndevPillR = 255 : IndevPillG = 205 : IndevPillB = 40
		Case "scp2968"         IndevPillR = 150 : IndevPillG = 192 : IndevPillB = 142
		Case "scp3494"         IndevPillR = 205 : IndevPillG = 128 : IndevPillB = 110
		Case "scp3521"         IndevPillR = 225 : IndevPillG = 215 : IndevPillB = 55
		Case "scp3929"         IndevPillR = 110 : IndevPillG = 70  : IndevPillB = 40
		Case "scpf02"          IndevPillR = 70  : IndevPillG = 180 : IndevPillB = 115
		Case "scp4193"         IndevPillR = 72  : IndevPillG = 122 : IndevPillB = 212
		Case "scp4257"         IndevPillR = 172 : IndevPillG = 176 : IndevPillB = 186
		Case "scp4292"         IndevPillR = Rand(100,255) : IndevPillG = Rand(100,255) : IndevPillB = Rand(100,255)
		Case "scp5043"         IndevPillR = 236 : IndevPillG = 142 : IndevPillB = 42
		Case "scp7521"         IndevPillR = 182 : IndevPillG = 222 : IndevPillB = 232
		Default                IndevPillR = 235 : IndevPillG = 235 : IndevPillB = 232
	End Select
End Function
