;=====================================================================
; SCP: Containment Breach - Indev: the thirty-fifth batch - Storage Areas 10 (the cell block) and 11 (the bunker)
;
;   Twenty-three SCPs as units of the batch-34 storage system (IndevU34.bb: the arrays, U34Use, the side effects;
;   this batch's rows are numbers 100-122 of its table, IndevU35Data.bb). What is special here:
;     SCP-799    the blankets want your warmth: lovely, then they start to feed
;     SCP-478    the moths beat at the glass - worse the younger you look
;     SCP-1429   lean too close and the glow gets on your skin
;     SCP-1779   it eats coins: have SCP-762-EX on you and it takes it, and grows
;     SCP-3369   the anecdote - read the first word and someone else laughs inside your head
;     SCP-569    the marble heads drift up and down, changing faces
;     SCP-517    Grandmother Predictions gives you a card - and some of them come true
;     SCP-1579   the moss is always damp; SCP-806 shows more than the film; SCP-1479's photograph leaks cold
;   Items: SCP-2890 (the top hat - put it on a figure: SCP-629, the mannequins, the cedar giant), SCP-2816 (copy a
;   painting), SCP-1388 (a small super power), SCP-1912 (the watch that ticks backwards).
;   Summaries of the scp-wiki.wikidot.com articles in our own words.
;=====================================================================

Global I35Fortune#, I35Power#, I35PowerK%, I35Watch#, I35Paint#, I35Hat%, I1779Fed%, I35Blanket#

Function Indev35Reset(newGame%)
	If newGame Then
		I1779Fed = 0 : I35Hat = 0
	EndIf
	I35Fortune = 0 : I35Power = 0 : I35Watch = 0 : I35Paint = 0 : I35Blanket = 0
	U35Tables()
End Function

;the batch-34 table, then this batch's rows (100+)
Function U35Tables()
	If U34Count = 0 Then IndevU34Table()
	If U34Count < 101 Then IndevU35Table()
End Function

Function IndevU35Dress(r.Rooms)
	U35Tables()
	IndevU35Units(r)
End Function

Function UpdateIndevU35(e.Events)
	Local r.Rooms = e\room
	UpdateIndevU34(e)                                     ;the units: the same code as batch 34
	If PlayerRoom <> r Then Return
	If r\RoomTemplate\Name = "room2b35cellblock" Then
		If IS10Press(r\Objects[U35_BLK_CAMS], 2.0) Then IS16Tell("Six feeds of the cell block. On camera 4 the upper tier is full: every cell occupied. You look up. Every upper cell is empty.", 8)
		If IS10Press(r\Objects[U35_BLK_DOORS], 2.0) Then IS16Tell("CELL DOORS - REMOTE RELEASE. Every switch has been taped down at LOCKED. Someone wrote on the tape: 'NOT THE BLANKETS'.", 7)
	Else
		If IS10Press(r\Objects[U35_BNK_LOCKDOWN], 2.0) Then IS16Tell("BUNKER LOCKDOWN: the big lever is at OFF, the generators idle. A note: 'If the lights go, the moss on 1579 glows. You can find the door by it.'", 8)
		If IS10Press(r\Objects[U35_BNK_SEALED], 2.0) Then
			IS10Sound("SFX\Indev\creak.wav", r\Objects[U35_BNK_SEALED], 5.0, 0.6)
			IS16Tell("An old door, older than the bunker, at the end of the stone passage. Behind it, stairs go down and down under arched lamps. It is welded shut.", 8)
		EndIf
	EndIf
End Function

;called from U34Special for numbers it does not know: True if handled
Function U35Special%(e.Events, i%, head$)
	Local it.Items
	Select U34Num(i)
		Case "799"
			I35Blanket = I35Blanket + 1
			If I35Blanket < 3 Then
				Stamina = 100 : IndevStress = Max(0, IndevStress - 10)
				IS16Tell(head + "You put your hand to the bars and a blanket flows up to it, warm, so warm. You could lie down here.", 7)
			Else
				Injuries = Injuries + 0.25 : Stamina = 0
				IS16Tell(head + "This time it wraps your wrist and pulls, and the warmth goes the other way - out of you. You tear free. You are freezing.", 8)
				I35Blanket = 0
			EndIf
		Case "478"
			IndevStress = Min(100, IndevStress + 12) : LightBlink = 1.0
			IS16Tell(head + "They hurl themselves at the glass the moment you lean in, a soft dark storm. They are hungry for someone young. You'll do.", 7)
		Case "1429"
			Injuries = Injuries + 0.12 : BlurTimer = Max(BlurTimer, 70 * 3)
			IS16Tell(head + "You lean close. Your knuckle brushes the tank seal - and a faint blue glow is on your skin now, itching. It doesn't wash off.", 7)
		Case "1779"
			it = U30Has("coin762")
			If it <> Null Then
				RemoveItem(it)
				I1779Fed = I1779Fed + 1
				IS16Tell(head + "It sees the 1968 quarter in your pocket before you do. A flick through the feeding hatch and it's gone - two-headed or not. It purrs, and its mane fluffs up.", 8)
			ElseIf I1779Fed > 0 Then
				IS16Tell(head + "It's bigger than it was. It sniffs at your pockets for more coins. You don't have any.", 6)
			Else
				IS16Tell(head + U34Text(i), 7)
			EndIf
		Case "3369"
			If IAxFlag(e, "a") Then
				IS16Tell(head + "You don't look at the screen again. Somewhere behind your eyes, someone is still chuckling.", 6)
			Else
				IAxSetFlag(e, "a")
				IndevStress = Min(100, IndevStress + 10) : BlurTimer = Max(BlurTimer, 70 * 2)
				IAxSay("???", "(inside your head) Ha! Oh, that's a good one. You don't even know the rest yet.", 7)
				IS16Tell(head + "You read the first word. That was enough. Something laughed - not you.", 6)
			EndIf
		Case "569"
			IS16Tell(head + "The nearest head turns to you with a look of pure joy - then, between one blink and the next, of terrible distress.", 7)
			IndevStress = Min(100, IndevStress + 5)
		Case "517"
			If I35Fortune > 0 Then
				IS16Tell(head + "Grandmother's hand stays still. One fortune at a time.", 4)
			Else
				I35Fortune = 70 * 90
				IS10Sound("SFX\Indev\clicks.wav", U34Piv(i), 4.0, 0.8)
				Select Rand(5)
					Case 1
						IS16Tell(head + "The puppet's hand sweeps over the crystal ball. A card drops: 'A WOUND WILL CLOSE.' Your cuts stop stinging.", 7)
						Injuries = Max(0, Injuries - 0.3)
					Case 2
						IS16Tell(head + "A card: 'SOMEONE IS FOLLOWING YOU.' You look back. No one. You keep looking back.", 7)
						IndevStress = Min(100, IndevStress + 15)
					Case 3
						IS16Tell(head + "A card: 'YOU WILL FIND WHAT YOU NEED UNDER THE STAIRS.' (Under the mezzanine stairs, something has been left for you.)", 8)
						IS16Give("firstaid", U34Piv(i))
					Case 4
						IS16Tell(head + "A card: 'THE LIGHTS WILL GO.' And they do - for a second.", 6)
						LightBlink = 3.0
					Default
						IS16Tell(head + "A card, blank on both sides. Grandmother's head turns, slowly, to look at you. The cord is cut. The candle burns.", 8)
				End Select
			EndIf
		Case "1579"
			IS16Tell(head + "You touch the moss on its shin: cool and wet, as if just rained on. The wood beneath is warm. The head is a little lower than it was.", 7)
		Case "806"
			IS10Sound("SFX\Indev\clicks.wav", U34Piv(i), 5.0, 0.6)
			BlurTimer = Max(BlurTimer, 70 * 3)
			IS16Tell(head + "It clatters into life and throws a film on the concrete: this bunker, empty, from where you stand. In the film, behind you, someone is standing very still.", 9)
			IndevStress = Min(100, IndevStress + 8)
		Case "1479"
			Injuries = Injuries + 0.03 : BlurTimer = Max(BlurTimer, 70 * 2)
			IS16Tell(head + "A breath of pine and frost comes off the photograph of the door. Your fingers ache with cold. 144 square kilometres of it.", 7)
		Default
			Return False
	End Select
	Return True
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev35()
	Local i%, k%, m%
	If I35Fortune > 0 Then I35Fortune = I35Fortune - FPSfactor
	;SCP-569: the heads drift up and down
	i = U34Find("569")
	If i >= 0 Then
		For k = 0 To 2
			m = U34Mdl(i, k)
			If m <> 0 Then TranslateEntity(m, 0, Sin(MilliSecs() / (11.0 + k * 3) + k * 120) * 0.0012 * FPSfactor, 0)
		Next
	EndIf
	;SCP-1388: the small super power
	If I35Power > 0 Then
		I35Power = I35Power - FPSfactor
		Select I35PowerK
			Case 1 : Stamina = 100
			Case 2 : If Injuries > 0 Then Injuries = Max(0, Injuries - 0.00015 * FPSfactor)
			Default : BlinkTimer = Max(BlinkTimer, 300)
		End Select
		If I35Power <= 0 Then IS16Tell("The power fades. The briefs are just briefs. You are, frankly, relieved.", 5)
	EndIf
	;SCP-1912: the watch, ticking backwards
	If I35Watch > 0 Then
		I35Watch = I35Watch - FPSfactor
		If I35Watch <= 0 Then IS16Tell("The pocket watch stops ticking backwards. The second hand trembles, and goes forward again.", 5)
	EndIf
	;SCP-2816: the copy, when you aren't looking
	If I35Paint > 0 Then
		I35Paint = I35Paint - FPSfactor
		If I35Paint <= 0 Then
			IndevStress = Min(100, IndevStress + 10)
			IS16Tell("The copy you painted has changed while you weren't looking: in it, the figure has turned its head towards you.", 7)
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse35(it.Items)
	Local i%, k%, best%, bd# = 2.5, nm$
	Select it\itemtemplate\name
		Case "hat2890"
			best = -1
			For i = 0 To U34Count - 1                                ;a figure near you to put it on
				nm = U34Num(i)
				If nm = "629" Or nm = "5147" Or nm = "1579" Or nm = "3228" Then
					If U34PRoom(i) = PlayerRoom And U34Piv(i) <> 0 Then
						If EntityDistance(Collider, U34Piv(i)) < bd Then bd = EntityDistance(Collider, U34Piv(i)) : best = i
					EndIf
				EndIf
			Next
			If best >= 0 Then
				I35Hat = I35Hat + 1 : I34Uses = I34Uses + 1
				Select U34Num(best)
					Case "629" : IAxSay("SCP-629", "Ah! Thank you. Mr. Brass, at your service. Do you know - is the Doctor still looking for us?", 8)
					Case "5147" : IAxSay("The Cook (SCP-5147)", "A hat! At last, a hat. Shall I make you something? I can make anything. Go on, ask.", 8)
					Case "1579" : IS16Tell("You can't reach its head. You put the hat on its outstretched hand instead. The fingers close, very slowly, round the brim.", 7)
					Default : IS16Tell("You set the hat on the ceramic head through the hatch. It turns to you and says its first word in years: 'Thank you.'", 7)
				End Select
				IS16Tell("SCP-2890: the hat animates any figure meant to look like a person. Take it back before the figure walks off with it.", 6)
			Else
				IS16Tell("A black silk top hat, Wilson and Sons, a crown sewn in the lining. Put it on something shaped like a person and it lives. (Mr. Brass, a mannequin...)", 7)
			EndIf
		Case "brush2816"
			If I35Paint > 0 Then
				IS16Tell("You're still waiting for the last copy to dry. You don't want to look at it.", 4)
			Else
				I35Paint = 70 * 25 : I34Uses = I34Uses + 1
				IS16Tell("You copy the painting from the wall of the office as well as you can on the back of a document. Not bad. The brushes are faintly warm.", 7)
			EndIf
		Case "briefs1388"
			If I35Power > 0 Then
				IS16Tell("You've already got a power. One at a time.", 4)
			Else
				I35Power = 70 * 60 : I35PowerK = Rand(1, 3) : I34Uses = I34Uses + 1
				Select I35PowerK
					Case 1 : IS16Tell("SUPER POWERS! They stretch to fit over your jumpsuit. Your power: you never get out of breath. For a minute.", 7)
					Case 2 : IS16Tell("SUPER POWERS! Your power: your scrapes heal, slowly, while you watch. For a minute.", 7)
					Default : IS16Tell("SUPER POWERS! Your power: you don't need to blink. For a minute. Dignity not included.", 7)
				End Select
			EndIf
		Case "watch1912"
			I35Watch = 70 * 20
			BlurTimer = Max(BlurTimer, 70 * 2)
			Injuries = Max(0, Injuries - 0.1)
			IS16Tell("You open the case: the second hand is going backwards. For a moment so are you - a scrape on your arm un-scrapes.", 7)
	End Select
	SelectedItem = Null
End Function
