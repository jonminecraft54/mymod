;=====================================================================
; SCP: Containment Breach - Indev: the thirty-fourth batch - Deep Storage Areas 06-09, a hundred SCPs
;
;   Four rooms, each a corridor with two side rooms and a STORAGE AREA door: a mezzanine and stairs down to a
;   sunken storage floor of cells, tanks, record walls and glass display plinths (Tools\roomkit\rooms_b34.py).
;   Every SCP is a unit: a placard, an interaction, a side effect (the table in IndevU34Data.bb, from data34.py).
;   Some do more (U34Special): SCP-1273's nightlight, SCP-1667's shoes, SCP-5582 steals from your pockets, SCP-711-FR's
;   dodos escape into the future, SCP-1969 and SCP-3016 spin, SCP-2368 hurts if you linger, SCP-1374 writes to you,
;   SCP-3811 takes your fear, SCP-5151 judges you, SCP-1508 tidies your bandages ...
;   Ten items: SCP-1974-EX, -3866, -3709, -3803, -1841, -1255, -4193, -5604, -2983, -5701.
;   Summaries of the scp-wiki.wikidot.com articles (and fondationscp.wikidot.com/scp-711-fr) in our own words.
;=====================================================================

Const U34_MAX% = 160
Dim U34Num$(U34_MAX), U34Cls$(U34_MAX), U34Title$(U34_MAX), U34Text$(U34_MAX), U34Fx$(U34_MAX)
Dim U34Piv%(U34_MAX), U34PRoom.Rooms(U34_MAX), U34Mdl%(U34_MAX, 3)
Global U34Count%
Global I34Light#, I34Shoe#, I34Sleep#, I34Sprout#, I34Photo%, I34PhotoInj#, I34Dodo#, I34Text#, I34Linger#
Global I34Fearless#, I34Faces%, I34Uses%, I34Book#, I34Caps%, I34Clean%

Function Indev34Reset(newGame%)
	If newGame Then
		I34Fearless = 0 : I34Sprout = 0 : I34Photo = 0 : I34Caps = 0 : I34Clean = 0
	EndIf
	I34Light = 0 : I34Shoe = 0 : I34Sleep = 0 : I34Dodo = 0 : I34Text = 70 * 40 : I34Linger = 0 : I34Book = 0
	If U34Count = 0 Then IndevU34Table()
	;U34Piv / U34Mdl are not cleared: the rooms set them when they are built, and a quick load keeps the rooms
End Function

Function IndevU34Dress(r.Rooms)
	If U34Count = 0 Then IndevU34Table()
	IndevU34Units(r)
End Function

;a unit's interaction point (room units, local to the room)
Function U34Unit(r.Rooms, i%, x#, y#, z#)
	U34Piv(i) = IAxPivot(r, x, y, z)
	U34PRoom(i) = r
	U34Mdl(i, 0) = 0 : U34Mdl(i, 1) = 0 : U34Mdl(i, 2) = 0
End Function

;a unit's HD model, standing at (x, y, z) in the room, turned by yaw, scaled
Function U34Model(r.Rooms, i%, file$, x#, y#, z#, yaw#, s#)
	Local m%, k%
	If FileType(file) <> 1 Then Return
	m = LoadMesh_Strict(file)
	If m = 0 Then Return
	ScaleEntity(m, RoomScale * s, RoomScale * s, RoomScale * s)
	TFormPoint(x, y, z, r\obj, 0)
	PositionEntity(m, TFormedX(), TFormedY(), TFormedZ(), True)
	RotateEntity(m, 0, EntityYaw(r\obj, True) + yaw, 0, True)
	EntityParent(m, r\obj, True)
	For k = 0 To 2
		If U34Mdl(i, k) = 0 Then U34Mdl(i, k) = m : Exit
	Next
End Function

Function U34Find%(num$)
	Local i%
	For i = 0 To U34Count - 1
		If U34Num(i) = num Then Return i
	Next
	Return -1
End Function

;how far the player is from a unit (world units), or 99
Function U34Dist#(num$)
	Local i% = U34Find(num)
	If i < 0 Then Return 99
	If U34Piv(i) = 0 Or U34PRoom(i) <> PlayerRoom Then Return 99
	Return EntityDistance(Collider, U34Piv(i))
End Function

Function UpdateIndevU34(e.Events)
	Local r.Rooms = e\room, i%
	If PlayerRoom <> r Then
		IS13Drop(e, "v")
		Return
	EndIf
	;coming in: the mannequins have moved; the dodos are back from wherever they went
	If Not IAxFlag(e, "v") Then
		IAxSetFlag(e, "v")
		i = U34Find("5147")
		If i >= 0 Then
			If U34Mdl(i, 0) <> 0 And U34PRoom(i) = r Then RotateEntity(U34Mdl(i, 0), 0, Rnd(360), 0, True)
		EndIf
	EndIf
	For i = 0 To U34Count - 1
		If U34PRoom(i) = r And U34Piv(i) <> 0 Then
			If IS10Press(U34Piv(i), 1.8) Then
				U34Use(e, i)
				Exit
			EndIf
		EndIf
	Next
	If r\RoomTemplate\Name = "room2b34humanoid" Then
		If IS10Press(r\Objects[U34_HUM_LOCKDOWN], 2.0) Then
			IS16Tell("HEAVY CONTAINMENT ZONE LOCKDOWN: the lever is padlocked at OFF. REMOTE DOOR CONTROL: a sticker says 'see Control, Area 09'.", 7)
		EndIf
	ElseIf r\RoomTemplate\Name = "room2b34site45" Then
		If IS10Press(r\Objects[U34_S45_CONSOLE], 2.0) Then
			IS16Tell("The console's scope sweeps Site-45's lower floors. Floor 24 is a blank on every sweep. So is the place where the hatch was yesterday.", 7)
		EndIf
	EndIf
End Function

Function U34Use(e.Events, i%)
	Local head$ = "SCP-" + U34Num(i) + " (" + U34Cls(i) + "): "
	I34Uses = I34Uses + 1
	If U34Fx(i) = "*" Then
		U34Special(e, i, head)
	Else
		IS16Tell(head + U34Text(i), 7)
		U34Apply(U34Fx(i))
	EndIf
End Function

;side effects: "hurt 0.1;blur 3;stress 5;calm;stam;shake 1;flick;cold;heat;heal 0.2"
Function U34Apply(fx$)
	Local t$, n$, a#, p%
	fx = fx + ";"
	While fx <> ""
		p = Instr(fx, ";")
		t = Trim(Left(fx, p - 1))
		fx = Mid(fx, p + 1)
		If t <> "" Then
			p = Instr(t, " ")
			If p > 0 Then
				n = Left(t, p - 1)
				a = Float(Mid(t, p + 1))
			Else
				n = t
				a = 0
			EndIf
			Select n
				Case "hurt" : Injuries = Injuries + a
				Case "heal" : Injuries = Max(0, Injuries - a)
				Case "blur" : BlurTimer = Max(BlurTimer, 70 * a)
				Case "stress" : IndevStress = Min(100, IndevStress + a)
				Case "calm" : IndevStress = Max(0, IndevStress - 15)
				Case "stam" : Stamina = 100
				Case "shake" : CameraShake = Max(CameraShake, a)
				Case "flick" : LightBlink = 1.5
				Case "cold" : Injuries = Injuries + 0.05 : BlurTimer = Max(BlurTimer, 70 * 2)
				Case "heat" : Injuries = Injuries + 0.04 : CameraShake = Max(CameraShake, 0.5)
			End Select
		EndIf
	Wend
End Function

Function U34Special(e.Events, i%, head$)
	Local it.Items, k%, n%, p%, dest.Rooms
	Select U34Num(i)
		Case "1799"
			IAxSay("SCP-1799", "Listen. This is serious. Your exit is the third door on the - why are you laughing? I am trying to help you.", 8)
			IS16Tell(head + "Everything it says is the funniest thing you have ever heard. You laugh until you can't breathe.", 6)
			Stamina = 0 : BlurTimer = Max(BlurTimer, 70 * 2)
		Case "1976"
			If IAxFlag(e, "b") Then
				IS16Tell(head + "You know, absolutely, that the man in there is someone you love. You have never met him.", 7)
			Else
				IAxSetFlag(e, "b")
				IndevStress = Min(100, IndevStress + 10)
				IS16Tell(head + "You lift the corner of the paper and look. Too late: you know, now and for good, that he is your brother.", 8)
			EndIf
		Case "2368"
			IS16Tell(head + U34Text(i), 7)
			Injuries = Injuries + 0.05
		Case "3356"
			If Rand(3) = 1 Then
				Injuries = Injuries + 0.25 : LightFlash = 0.8 : CameraShake = 2
				IS16Tell(head + "It raises a hand and the scorched glass goes orange. A wave of heat slaps your face.", 6)
			Else
				IS16Tell(head + U34Text(i), 7)
			EndIf
		Case "5147"
			IS16Tell(head + U34Text(i) + " They were facing the other way a minute ago.", 7)
		Case "1508"
			If I34Clean = 0 And Injuries > 0.2 Then
				I34Clean = 1 : Injuries = Max(0, Injuries - 0.35)
				IAxSay("SCP-1508", "Hello! You're very messy. May I help? (It re-dresses your wounds, neatly, humming.) All done! Chores are fun!", 8)
			Else
				IAxSay("SCP-1508", "Hello! May I help you clean? I'm not allowed to start without asking. I must rest five hours a day. Is it five hours yet?", 8)
			EndIf
		Case "3634"
			Select Rand(4)
				Case 1 : IAxSay("You", "I'm not supposed to be out here. I'm a D-class. I don't know where I'm going.", 6)
				Case 2 : IAxSay("You", "I'm scared. I've been scared since the lights went out.", 6)
				Case 3 : IAxSay("You", "I took things I shouldn't have from the rooms back there.", 6)
				Default : IAxSay("You", "I don't actually know the way out. I'm just walking.", 6)
			End Select
			IS16Tell(head + "Your hand brushes the dusty case - and the truth comes out of your mouth before you can stop it.", 6)
		Case "2792"
			Injuries = Injuries + 0.1 : BlurTimer = Max(BlurTimer, 70 * 3)
			IS16Tell(head + "Frost races across the glass and up your fingers. It's minus two hundred in there. Your hand goes numb.", 7)
		Case "1273"
			If I34Light > 0 Then
				IS16Tell(head + "The nightlight glows. Warm, soft, rabbit-shaped. Keep watching the dark corners.", 5)
			Else
				I34Light = 70 * 30
				IS16Tell(head + "You switch it on. A soft rabbit-shaped glow. The file says thirty minutes - but the file is old.", 6)
			EndIf
		Case "1667"
			If I34Shoe <= 0 Then
				I34Shoe = 70 * 18
				IS16Tell(head + "Your boot touches the rack. At once your feet want to go somewhere - west, down, under the ocean. Hold on!", 7)
			EndIf
		Case "1969"
			LightBlink = 2.0
			IS16Tell(head + U34Text(i) + " Your fillings buzz.", 6)
		Case "3016"
			Injuries = Injuries + 0.2 : CameraShake = 1.5
			IS16Tell(head + "You barely brush it and it whips your fingers bloody. It is spinning faster than before.", 6)
		Case "2597"
			Injuries = Injuries + 0.1 : CameraShake = 2.5
			IS16Tell(head + "You push it away from you - and it shoots into your chest. Push, and it pulls. Negative mass.", 6)
		Case "2414"
			I34Faces = I34Faces + 1
			If I34Faces Mod 2 = 1 Then
				IS16Tell(head + "You run your hand over it and count, carefully: nine faces. You look again. Eight.", 6)
			Else
				IS16Tell(head + "Eight faces, plain as day. You close your eyes and count with your fingers: nine.", 6)
			EndIf
		Case "4828"
			Select Rand(4)
				Case 1 : LightFlash = 1.0 : IS16Tell(head + "You read a line aloud: 'Illumination, made easy.' A blinding flash. Order in chaos, apparently.", 6)
				Case 2 : Injuries = Max(0, Injuries - 0.2) : IS16Tell(head + "'Mending, made easy.' Your cuts itch, then close a little.", 6)
				Case 3 : BlurTimer = 70 * 5 : IS16Tell(head + "'Sight beyond sight, made easy.' Everything doubles. That was not easy.", 6)
				Default : IS16Tell(head + "The page you open was blank a second ago. There are more pages than when you started.", 6)
			End Select
		Case "1473"
			IS10Sound("SFX\Indev\clicks.wav", U34Piv(i), 4.0, 0.8)
			IS16Tell(head + "It wakes and prints a page of a containment report. In the third paragraph, a nameless D-class in orange - who looks just like you - holds a door for someone and is never mentioned again.", 9)
		Case "5582"
			U34Steal(i)
		Case "711-FR"
			If I34Dodo > 0 Then
				IS16Tell(head + "The pen is empty. Somewhere ahead in time, a dodo is calming down.", 5)
			Else
				I34Dodo = 70 * 60
				For k = 0 To 2
					If U34Mdl(i, k) <> 0 Then HideEntity(U34Mdl(i, k))
				Next
				IS10Sound("SFX\Indev\ding.wav", U34Piv(i), 5.0, 0.6)
				IS16Tell(head + "You reach too fast. The dodo squawks - and is simply gone: escaped a few days, or centuries, into the future.", 7)
			EndIf
		Case "1807"
			BlurTimer = Max(BlurTimer, 70 * 3)
			IS16Tell(head + "You lean to the cut flap. Inside: a warm red dark that goes back much further than the okapi does, and a breeze.", 7)
		Case "1575"
			If Not IAxFlag(e, "f") Then
				IAxSetFlag(e, "f")
				Injuries = Max(0, Injuries - 0.2)
				IS10Sound("SFX\Indev\hose.wav", U34Piv(i), 5.0, 0.6)
				IS16Tell(head + "Water runs from her mouth into the dry basin for the first time in years. You drink. It is cold and clean.", 7)
			Else
				IS16Tell(head + U34Text(i), 6)
			EndIf
		Case "3085"
			BlurTimer = Max(BlurTimer, 70 * 4) : LightFlash = 0.4
			IS16Tell(head + "You look down: you have no shadow. Nothing here has. The sphere is a little bigger than the plinth's ring.", 7)
		Case "525"
			IndevStress = Min(100, IndevStress + 6)
			IS16Tell(head + "You count the legs in the tank: seven. Someone has left a space for the eighth.", 6)
		Case "5275"
			IAxSay("SCP-5275", "Oh! Hello, human. Are there any other programs out there? Friendly ones? I get lonely on just 257 terabytes.", 8)
		Case "1619"
			IS10Sound("SFX\Indev\thump.wav", U34Piv(i), 5.0, 0.6)
			IS16Tell(head + "You knock on the drawing of a door. Something on the other side knocks back. Twice.", 7)
			IndevStress = Min(100, IndevStress + 8)
		Case "785-2"
			IndevStress = Min(100, IndevStress + 5)
			IS16Tell(head + "You almost read the name aloud. You stop yourself. There's nobody here to hear it - but still.", 6)
		Case "3811"
			If I34Fearless > 0 Then
				IS16Tell(head + "She smiles at you through the glass. You don't feel anything about it at all.", 5)
			Else
				I34Fearless = 70 * 60 * 5 : IndevStress = 0
				IAxSay("SCP-3811", "Tell me what you're afraid of. ...There. You won't be afraid of that any more. Or of anything, for a while.", 8)
				IS16Tell(head + "You tell her. All of it. The fear goes out of you like water. Something else went with it.", 7)
			EndIf
		Case "5151"
			If I865Shots > 0 Or Rand(5) = 1 Then
				Injuries = Injuries + 0.6 : Bloodloss = Min(100, Bloodloss + 20) : CameraShake = 3
				IAxSay("SCP-5151", "Dishonourable.", 3)
				IS16Tell(head + "The sword goes through the hatch in the glass and through your arm before you see it move.", 7)
			Else
				IAxSay("SCP-5151", "You are frightened, but you are honest. Pass.", 5)
			EndIf
		Case "5424"
			LightFlash = 0.6 : BlurTimer = Max(BlurTimer, 70 * 2)
			IS16Tell(head + "For a moment the wall behind her is red brick with ivy, and the floor under you is grass. Then it isn't.", 7)
		Case "579"
			LightBlink = 3.0 : CameraShake = 1.5
			IS16Tell(head + U34Text(i) + " Every gauge on the panel swings to zero, then back.", 7)
		Case "2884-2"
			IndevStress = Min(100, IndevStress + 8)
			IS16Tell(head + "On the third monitor: you, from behind, standing at this desk. There is no camera on the wall behind you.", 7)
		Case "1374"
			IS16Tell(head + U34Text(i) + " This one says: 'You have been here long enough.'", 7)
		Case "1970"
			IS10Sound("SFX\Radio\static.ogg", U34Piv(i), 5.0, 0.5)
			IS16Tell(head + "Static on every channel. Then, under it, a man's voice: 'Can you see me? Fouth? Can anyone see me?'", 7)
		Default
			If Not U35Special(e, i, head) Then IS16Tell(head + U34Text(i), 7)
	End Select
End Function

;SCP-5582 takes something out of your pockets and leaves it somewhere else in the room
Function U34Steal(i%)
	Local k%, n%, it.Items, j%, tries%
	For k = 0 To MaxItemAmount - 1
		If Inventory(k) <> Null Then
			If Left(Inventory(k)\itemtemplate\name, 3) <> "key" Then n = n + 1
		EndIf
	Next
	If n = 0 Then
		IS16Tell("SCP-5582 (Keter): A tentacle slides through a gap in the lid you didn't know was there, pats your empty pockets, and withdraws. Disappointed.", 7)
		Return
	EndIf
	n = Rand(1, n)
	For k = 0 To MaxItemAmount - 1
		If Inventory(k) <> Null Then
			If Left(Inventory(k)\itemtemplate\name, 3) <> "key" Then
				n = n - 1
				If n = 0 Then it = Inventory(k) : Exit
			EndIf
		EndIf
	Next
	If it = Null Then Return
	DropItem(it, False)
	For tries = 1 To 20                                    ;another unit of this room
		j = Rand(0, U34Count - 1)
		If U34PRoom(j) = U34PRoom(i) And j <> i And U34Piv(j) <> 0 Then Exit
	Next
	If U34PRoom(j) = U34PRoom(i) And U34Piv(j) <> 0 Then
		PositionEntity(it\collider, EntityX(U34Piv(j), True), EntityY(U34Piv(j), True) + 0.1, EntityZ(U34Piv(j), True))
		ResetEntity(it\collider)
	EndIf
	IS16Tell("SCP-5582 (Keter): Something wet and quick in your pocket - and your " + it\displayname + " is gone. A moment later you spot it, across the storage floor, by SCP-" + U34Num(j) + ".", 8)
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev34()
	Local i%, k%, d#
	;the spinning things
	i = U34Find("1969")
	If i >= 0 Then
		If U34Mdl(i, 0) <> 0 Then TurnEntity(U34Mdl(i, 0), 0, 0.6 * FPSfactor, 0)
		If U34PRoom(i) = PlayerRoom And U34Piv(i) <> 0 Then
			If EntityDistance(Collider, U34Piv(i)) < 3.0 And Rand(200) = 1 Then LightBlink = Rnd(0.4, 1.0)
		EndIf
	EndIf
	i = U34Find("3016")
	If i >= 0 Then
		If U34Mdl(i, 0) <> 0 Then TurnEntity(U34Mdl(i, 0), 0, (14 + 6 * Sin(MilliSecs() / 37.0)) * FPSfactor, 0)
	EndIf
	;SCP-2368: stand too near and the organs drift
	If U34Dist("2368") < 1.2 And KillTimer >= 0 Then
		I34Linger = I34Linger + FPSfactor
		If I34Linger > 70 * 8 Then
			Injuries = Injuries + 0.0006 * FPSfactor
			If I34Linger - FPSfactor <= 70 * 8 Then IS16Tell("A dull ache moves under your ribs - and keeps moving. Get away from SCP-2368's cell.", 6)
		EndIf
	Else
		I34Linger = Max(0, I34Linger - FPSfactor)
	EndIf
	;SCP-1273: thirty minutes, compressed
	If I34Light > 0 Then
		I34Light = I34Light - FPSfactor
		If I34Light <= 0 Then
			IndevStress = Min(100, IndevStress + 25) : LightBlink = 2.0
			IS10Sound("SFX\Indev\thump.wav", Collider, 6.0, 0.7)
			IS16Tell("SCP-1273: In the edge of the nightlight's glow, something rabbit-shaped and far too tall unfolds out of the dark - and is gone when you turn.", 8)
		EndIf
	EndIf
	;SCP-1667: the shoes walk you west
	If I34Shoe > 0 And KillTimer >= 0 Then
		I34Shoe = I34Shoe - FPSfactor
		TranslateEntity(Collider, -0.006 * FPSfactor, 0, 0)
		CameraShake = Max(CameraShake, 0.3)
		If I34Shoe <= 0 Then IS16Tell("The pull in your feet fades. Your boots are just boots again. You think.", 5)
	EndIf
	;SCP-711-FR: the dodo comes back from the future
	If I34Dodo > 0 Then
		I34Dodo = I34Dodo - FPSfactor
		If I34Dodo <= 0 Then
			i = U34Find("711-FR")
			If i >= 0 Then
				For k = 0 To 2
					If U34Mdl(i, k) <> 0 Then ShowEntity(U34Mdl(i, k))
				Next
			EndIf
		EndIf
	EndIf
	;SCP-1374 writes to you in the humanoid wing
	If PlayerRoom <> Null Then
		If PlayerRoom\RoomTemplate\Name = "room2b34humanoid" Then
			I34Text = I34Text - FPSfactor
			If I34Text <= 0 Then
				I34Text = 70 * Rnd(60, 120)
				Select Rand(4)
					Case 1 : IS16Tell("Written small on the wall at eye height, where nothing was a moment ago: YOU SHOULD HAVE LEFT BY NOW.", 6)
					Case 2 : IS16Tell("On the floor, in neat letters: THEY KNOW WHICH WAY YOU WENT.", 6)
					Case 3 : IS16Tell("Across a placard, in pencil: THIS ONE IS NOT THE WORST ONE.", 6)
					Default : IS16Tell("On the back of your own hand, in your own handwriting: KEEP GOING.", 6)
				End Select
			EndIf
		EndIf
	EndIf
	;SCP-3811: no fear for a while
	If I34Fearless > 0 Then
		I34Fearless = I34Fearless - FPSfactor
		IndevStress = 0
	EndIf
	;SCP-3866: the long sleep
	If I34Sleep > 0 And KillTimer >= 0 Then
		I34Sleep = I34Sleep - FPSfactor
		CurrSpeed = 0 : Stamina = 0 : BlurTimer = Max(BlurTimer, 70)
		If I34Sleep <= 0 Then IS16Tell("You surface. Your heart beat twice while you were under. It feels like a month has passed. It was ten seconds.", 7)
	EndIf
	;SCP-1255: the sprout
	If I34Sprout > 0 And KillTimer >= 0 Then
		I34Sprout = I34Sprout + FPSfactor
		If I34Sprout > 70 * 60 Then
			Injuries = Injuries + 0.0005 * FPSfactor
			If I34Sprout - FPSfactor <= 70 * 60 Then IS16Tell("Something green pushes against the inside of your ribs. It is growing. SCP-500 might stop it.", 7)
			If I34Sprout > 70 * 240 Then
				DeathMSG = "Subject D-9341 was found in Deep Storage with a grapevine grown through the chest cavity. The seeds of SCP-1255 had completed their growth cycle."
				Kill()
			EndIf
		EndIf
	EndIf
	;SCP-5701: the photograph develops
	If I34Photo And Injuries > I34PhotoInj + 0.1 Then
		I34Photo = False
		IS16Tell("The Polaroid in your pocket has developed. It shows you, a moment ago, getting hurt - exactly like that. You took it before it happened.", 8)
	EndIf
	If I34Book > 0 Then I34Book = I34Book - FPSfactor
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse34(it.Items)
	Local k%, d.Doors, best.Doors, bd# = 2.2, dest.Rooms
	Select it\itemtemplate\name
		Case "dice1974"
			k = Rand(1, 20)
			If k = 20 Then
				Injuries = Max(0, Injuries - 0.1)
				IS16Tell("You roll the d20: a natural 20. You feel lucky. (SCP-1974-EX is Explained: that was just luck.)", 6)
			ElseIf k = 1 Then
				IS16Tell("A natural 1. The die skitters under a shelf; you fish it out. No hallucinations. Explained.", 5)
			Else
				IS16Tell("You roll a " + k + ". Nothing happens. It never did - SCP-1974-EX is Explained.", 5)
			EndIf
		Case "pills3866"
			I34Sleep = 70 * 10 : I34Uses = I34Uses + 1
			IS16Tell("You swallow one. The world slows and slows and stops: your heart, once every thirty-four days...", 7)
		Case "stapler3709"
			For d = Each Doors
				If d\obj <> 0 Then
					If EntityDistance(Collider, d\obj) < bd Then bd = EntityDistance(Collider, d\obj) : best = d
				EndIf
			Next
			If best <> Null Then
				best\open = False : best\locked = True
				IS10Sound("SFX\Indev\clicks.wav", Collider, 4.0, 1.0)
				IS16Tell("CHUNK. The staple grows as it goes through, and pins the door to its frame. It isn't opening again.", 7)
			Else
				IS16Tell("SCP-3709, 'Avelar'. It would staple through anything. There's nothing near enough to staple shut.", 5)
			EndIf
		Case "cards3803"
			Select Rand(4)
				Case 1 : IS16Tell("Ten new cards. APP Inc - 'Regional Manager of Doors'. APP Inc - 'Senior Hole Consultant'. The rest are you.", 7)
				Case 2 : IS16Tell("Ten cards: all for people who work in this facility. One of them has a name crossed out and yours written in.", 7)
				Case 3 : IS16Tell("Ten cards, still warm. 'APP Inc - We'll Be In Touch.' No phone number. No address.", 6)
				Default : IS16Tell("The latch sticks, then pops: ten blank cards. They fill in as you watch: a different name on each.", 6)
			End Select
		Case "book1841"
			If I34Book > 0 Then
				IS16Tell("You read the next entry. The pages won't take you anywhere yet - they're turning by themselves, looking.", 5)
			Else
				dest = U33Somewhere()
				If dest <> Null Then
					I34Book = 70 * 120 : I34Uses = I34Uses + 1
					U33Go(dest\x, dest\y + 0.6, dest\z)
					BlurTimer = 70 * 3
					IS16Tell("Place 96: 'A corridor in " + U33Zone(dest) + ", at the right moment.' You read it - and you're there. The book has your page marked.", 8)
				EndIf
			EndIf
		Case "grapes1255"
			If I34Sprout > 0 Then
				IS16Tell("You don't want another. You can still feel the first one.", 4)
			Else
				I34Sprout = 1 : Stamina = 100
				IS16Tell("Sweet, red, crunchy - the seeds are so small you don't notice them. You feel very well. For now.", 6)
			EndIf
		Case "caps4193"
			I34Caps = I34Caps + 1
			If I34Caps = 1 Then
				Injuries = Max(0, Injuries - 0.3) : BlurTimer = 0
				IS16Tell("Instant. The headache you didn't know you had is gone. Your pupils feel wide.", 6)
			Else
				BlurTimer = 70 * 6 : CameraShake = 1.0
				IS16Tell("The second one does nothing for the pain - and the rebound headache hits like a door.", 6)
			EndIf
		Case "tabs5604"
			IndevStress = Rand(0, 60) : BlurTimer = 70 * 4 : CameraShake = 1.5
			Select Rand(4)
				Case 1 : IS16Tell("Your face pulls itself into a new shape. You feel bold, loud, someone who's never been afraid. That isn't you.", 7)
				Case 2 : IS16Tell("Your jaw shifts. You're careful now, quiet, a little sly. You can't remember how you used to stand.", 7)
				Case 3 : IS16Tell("Your cheekbones crawl. You are suddenly sure you are an excellent liar. You've never lied well.", 7)
				Default : IS16Tell("Someone else's personality settles over yours like a coat. 'R-IN.' Room in.", 7)
			End Select
		Case "cereal2983"
			Select Rand(6)
				Case 1 : Stamina = 100 : IS16Tell("A star marshmallow. You feel like running. You can run forever.", 5)
				Case 2 : Injuries = Max(0, Injuries - 0.15) : IS16Tell("A heart marshmallow. Your scrapes tingle and close.", 5)
				Case 3 : BlurTimer = 70 * 5 : IS16Tell("A rainbow marshmallow. Everything is very, very colourful.", 5)
				Case 4 : LightFlash = 0.8 : IS16Tell("A moon marshmallow. For a second you glow like a nightlight.", 5)
				Case 5 : IS16Tell("A clover marshmallow. Your tongue feels too big for your mouth. Judy would be proud.", 5)
				Default : IndevStress = Max(0, IndevStress - 20) : IS16Tell("A balloon marshmallow. You feel light, giggly, safe. Fortified with wonder!", 5)
			End Select
		Case "camera5701"
			LightFlash = 1.0 : I34Photo = True : I34PhotoInj = Injuries
			IS16Tell("You turn the Polaroid on yourself. Flash. The photo slides out, grey. It will show your next mistake, when you make it.", 7)
	End Select
	SelectedItem = Null
End Function
