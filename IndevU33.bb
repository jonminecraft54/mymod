;=====================================================================
; SCP: Containment Breach - Indev: the thirty-third batch - twenty-three SCPs in four rooms
;
;   room2b33toys     Hall 8 and the Wondertainment store
;     SCP-1007   ages a year a minute in his coffin (75 and he dies). Use the key SCP-1007-1 by the coffin: each turn
;                takes a year off; turned after death, he wakes.
;     SCP-3537   behind glass; a different body every time you come back. The intercom: what it says it could do.
;     SCP-3938   the Take-You-Anywhere Machine: ride it and it takes you somewhere in the facility (it refuses
;                the Moon). Then it needs a rest.
;     SCP-4876   a Pixel Buddy drive: use it for a chat (Sam, Texty, Terry, Bo - and, rarely, -H)
;     SCP-4890   the pop-up Guide to History: use it and the place turns into endless purple space while Dr.
;                Papertainment shows you an era (and gets things wrong)
;   room2b33archive  Site-73
;     SCP-232    the Atomic Zapper: no batteries until you put some in (a battery from your inventory); then gee whiz
;     SCP-865    the pistol: use, then use again to fire it at your own hand - powder burns, and a bad memory gone
;     SCP-696    the typewriter: neutralized. Almost.
;     SCP-252-EX, SCP-762-EX (heads, every time - it is a two-headed coin), SCP-667-2's remains
;   room2b33bio  Bio-Site 84
;     SCP-1563   hungry since the breach: walk near its stake and it goes for your throat
;     SCP-2394   asleep on a drip. Shut the drip and it wakes, blinks round the room - touch it and it takes you
;                with it - and then it is gone
;     SCP-3419   the colony behind glass; -Alpha answers the intercom
;     SCP-7042   the sketchbook: use it, name an animal, and something arrives
;     SCP-7284   the transfer notice and Goldie's bed
;   room2b33deep Site-91 and VAULT 4612 (768 below)
;     SCP-4612-A on its altar (do not touch the crystals), SCP-4712's vault door (something knocks), the SCP-3743-A-1
;     Way, SCP-L043's turntable (each play, a little more of it gone), an SCP-5079-1 bed, METATRON, SCP-5512,
;     SCP-5267
;   Summaries of the scp-wiki.wikidot.com articles (CC BY-SA 3.0) in our own words.
;=====================================================================

Global I1007Age#, I1007Dead%
Global I3537Form%
Global I3938Cool#, I3938Rides%
Global I4890T#, I4890Era%, I4890Next#, I4890Quad%
Global I4876K%
Global I232Bat%, I232Uses%
Global I865Arm#, I865Shots%
Global I696Press%, I762Flips%
Global I1563Grab#, I1563Cool#
Global I2394Woke%, I2394T#, I2394Hop#, I2394Arm#, I2394Spot% = 3
Global I3419K%
Global I7042Uses%, I7042Pending#, I7042Animal$
Global IL043Line%, I4612Akiva#
Global I33Frog%, I33Uses%

Function Indev33Reset(newGame%)
	If newGame Then
		I1007Age = 52 : I1007Dead = False : I232Bat = False : I762Flips = 0 : IL043Line = 0 : I2394Woke = 0
		I7042Uses = 0 : I865Shots = 0 : I3938Rides = 0 : I696Press = 0 : I4612Akiva = 214
	EndIf
	I4890T = 0 : I1563Grab = 0 : I1563Cool = 0 : I865Arm = 0 : I7042Pending = 0 : I3938Cool = 0 : I2394T = 0
	I2394Arm = 0 : I4890Next = 0
	If I4890Quad <> 0 Then HideEntity(I4890Quad)
	;I33Frog is not cleared: the room sets it when it is built, and a quick load keeps the room
End Function

Function IndevU33Dress(r.Rooms)
	Local m%
	Select r\RoomTemplate\Name
		Case "room2b33toys"
			U30Prop(r, r\Objects[U33_TOY_COFFIN], "GFX\map\props\scp1007.b3d", 1.0, False)
			U30Prop(r, r\Objects[U33_TOY_BIKE], "GFX\map\props\scp3938.b3d", 1.0, False)
		Case "room2b33archive"
			U30Prop(r, r\Objects[U33_ARC_TYPE], "GFX\map\props\scp696.b3d", 1.0, True)
			U30Prop(r, r\Objects[U33_ARC_BOMB], "GFX\map\props\scp252.b3d", 1.0, False)
		Case "room2b33bio"
			U30Prop(r, r\Objects[U33_BIO_MARKER], "GFX\map\props\scp1563.b3d", 1.0, False)
			U30Prop(r, r\Objects[U33_BIO_TANK], "GFX\map\props\scp2394.b3d", 1.0, True)
			I33Frog = U30Prop(r, r\Objects[U33_BIO_FROG], "GFX\map\props\scp2394f.b3d", 1.0, True)
			If I33Frog <> 0 And I2394Woke = 2 Then HideEntity(I33Frog)
		Case "room2b33deep"
			;the vault is 768 below the corridor: these stand at their pivots' height, not on the room's floor
			U30Prop(r, r\Objects[U33_DEEP_CADAVER], "GFX\map\props\scp4612.b3d", 1.0, True)
			m = U30Prop(r, r\Objects[U33_DEEP_VAULTDOOR], "GFX\map\props\scp4712.b3d", 1.0, True)
			If m <> 0 Then MoveEntity(m, 0, 0, 30 * RoomScale)
			U30Prop(r, r\Objects[U33_DEEP_WAY], "GFX\map\props\scp3743.b3d", 1.0, True)
			U30Prop(r, r\Objects[U33_DEEP_TURNTABLE], "GFX\map\props\scpl043.b3d", 1.0, True)
			U30Prop(r, r\Objects[U33_DEEP_BED5079], "GFX\map\props\scp5079.b3d", 1.0, True)
			U30Prop(r, r\Objects[U33_DEEP_DIORAMA], "GFX\map\props\scp5267.b3d", 1.0, True)
	End Select
End Function

Function UpdateIndevU33(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b33toys" : U33Toys(e)
		Case "room2b33archive" : U33Archive(e)
		Case "room2b33bio" : U33Bio(e)
		Case "room2b33deep" : U33Deep(e)
	End Select
End Function

;the player to a point (global), as a teleport
Function U33Go(x#, y#, z#)
	PositionEntity(Collider, x, y, z)
	ResetEntity(Collider)
	DropSpeed = 0
	UpdateDoors()
	UpdateRooms()
End Function

;somewhere ordinary in the facility (a corridor), not here
Function U33Somewhere.Rooms()
	Local r.Rooms, n%, k%
	For r = Each Rooms
		If r <> PlayerRoom And U33Ordinary(r\RoomTemplate\Name) Then n = n + 1
	Next
	If n = 0 Then Return Null
	k = Rand(1, n)
	For r = Each Rooms
		If r <> PlayerRoom And U33Ordinary(r\RoomTemplate\Name) Then
			k = k - 1
			If k = 0 Then Return r
		EndIf
	Next
	Return Null
End Function

Function U33Ordinary%(n$)
	Select Lower(n)
		Case "room2", "room2_2", "room2_3", "room2_4", "room2_5", "room3", "room3_2", "room3_3", "room4", "room4_2", "room2c", "room3z2", "room3z3", "room2z3"
			Return True
	End Select
	Return False
End Function

Function U33Zone$(r.Rooms)
	Select r\zone
		Case 0 : Return "Light Containment"
		Case 1 : Return "Heavy Containment"
		Default : Return "the Entrance Zone"
	End Select
End Function

;--------------------------------------------------------------------------------------------- Hall 8 and the store
Function U33Toys(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then
		IS13Drop(e, "v")
		Return
	EndIf
	U30Figure(e, r\Objects[U33_TOY_SHAPEY], 0)
	If Not IAxFlag(e, "v") Then
		IAxSetFlag(e, "v")
		I3537Form = (I3537Form + Rand(1, 6)) Mod 8
	EndIf
	If IS10Press(r\Objects[U33_TOY_INTERCOM], 1.8) Then
		Select I3537Form
			Case 0 : IAxSay("SCP-3537", "Tall today. Two metres, nearly. Brown eyes. I think this one could see in the dark. It can't.", 9)
			Case 1 : IAxSay("SCP-3537", "Old, this time. Seventy, maybe. My knees hurt. I wrote down that this one could talk to birds.", 9)
			Case 2 : IAxSay("SCP-3537", "A woman, red hair - not dyed, it just grew like that overnight. This one would be fireproof. Wouldn't she.", 9)
			Case 3 : IAxSay("SCP-3537", "Heavy. Slow. Spots on my skin that would light up like stars in the dark. Turn the lights off - see? Nothing.", 10)
			Case 4 : IAxSay("SCP-3537", "Young. Too young, I think. It hurt more than usual. I've written it down. Did someone bring the paper?", 9)
			Case 5 : IAxSay("SCP-3537", "Short, freckled, sand in the hair from nowhere. 'Ms. Sandy'. I can't make sand. I tried.", 9)
			Case 6 : IAxSay("SCP-3537", "Built like a wrestler. Shapey the strong man. Couldn't lift the bed. The tattoo's still on my back, at least.", 9)
			Default : IAxSay("SCP-3537", "Me again. Someone else again. Do you ever find all of us? The Misters? I'd like to meet the others.", 9)
		End Select
	EndIf
	If IS10Press(r\Objects[U33_TOY_COFFIN], 1.8) Then
		If I1007Dead Then
			IS16Tell("SCP-1007 lies still and grey in the coffin, seventy-five years old and dead. The key socket between his shoulders is waiting.", 7)
		ElseIf I1007Age < 3 Then
			IS16Tell("A baby, crying in a coffin far too big for it. Tattooed on its calf: 'Mr. Life and Mr. Death'. It is growing as you watch.", 7)
		ElseIf I1007Age < 16 Then
			IS16Tell("A child of " + Int(I1007Age) + ", curled up and sobbing: his bones are growing too fast. It is the worst part, the file says.", 7)
		ElseIf I1007Age < 60 Then
			IS16Tell("SCP-1007, about " + Int(I1007Age) + ". He looks up from the coffin: 'Another minute, another year. Have you come to wind me back?'", 8)
		Else
			IS16Tell("SCP-1007, an old man of " + Int(I1007Age) + ", breathing slowly. 'Not long now,' he says. 'I always come back. Usually.'", 8)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_TOY_MISTERS], 2.0) Then
		IS16Tell("LITTLE MISTERS - find them all! Two are ticked: No. 5, Mr. Shapey, and No. 11, Mr. Life and Mr. Death.", 6)
	EndIf
	If IS10Press(r\Objects[U33_TOY_BIKE], 2.0) Then U33Ride()
	If IS10Press(r\Objects[U33_TOY_PIXEL], 2.2) Then
		IS16Tell("The wall screen shows a pixel-art desktop, waiting. A label below: 'PIXEL BUDDIES - INSERT DRIVE'.", 5)
	EndIf
End Function

Function U33Ride()
	Local r.Rooms
	If I3938Cool > 0 Then
		IAxSay("SCP-3938", "Phew! I'm all tuckered out. Give me a little rest and we'll go again, okay?", 6)
		Return
	EndIf
	If Rand(6) = 1 Then
		IAxSay("SCP-3938", "The Moon? Ooh, no can do - you'd need a space suit for that, and a helmet! Always wear a helmet!", 7)
		I3938Cool = 70 * 10
		Return
	EndIf
	r = U33Somewhere()
	If r = Null Then
		IAxSay("SCP-3938", "Hmm. All the roads are closed today. Sorry, pal!", 5)
		Return
	EndIf
	I3938Rides = I3938Rides + 1 : I33Uses = I33Uses + 1
	I3938Cool = 70 * 120
	IS10Sound("SFX\Indev\fire.wav", Collider, 6.0, 0.8)
	BlurTimer = Max(BlurTimer, 70 * 3) : CameraShake = 2.0
	U33Go(r\x, r\y + 0.6, r\z)
	IAxSay("SCP-3938", "Hold on tight! ...And here we are: " + U33Zone(r) + ". Lovely corridors! Thank you for riding! Wear a helmet!", 8)
	IS16Tell("A blur, a trail of flames, a radio playing something loud - then the bike is gone, pedalling itself home.", 6)
End Function

;--------------------------------------------------------------------------------------------- Site-73
Function U33Archive(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U33_ARC_SAFE865], 1.8) Then
		If Not IAxFlag(e, "g") Then
			IAxSetFlag(e, "g")
			IS16Give("gun865", r\Objects[U33_ARC_SAFE865])
			IS16Tell("The firearms safe is unlocked. Inside: a pistol with circuit boards in the grip, a trigger lock, and a tag - NON-FUNCTIONAL. DO NOT USE.", 7)
		Else
			IS16Tell("The firearms safe is empty.", 3)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_ARC_SAFE232], 1.8) Then
		If Not IAxFlag(e, "z") Then
			IAxSetFlag(e, "z")
			IS16Give("zapper232", r\Objects[U33_ARC_SAFE232])
			IS16Tell("A tin toy ray gun, 'ATOMIC ZAPPER', in a locked safe. The battery hatch is empty - as the procedures say it should be.", 7)
		Else
			IS16Tell("The safe is empty.", 3)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_ARC_TYPE], 1.6) Then
		I696Press = I696Press + 1
		If I696Press = 3 Then
			IS10Sound("SFX\Indev\clicks.wav", r\Objects[U33_ARC_TYPE], 4.0, 0.9)
			IS16Tell("The keys move by themselves - once. Under the last line, in red capitals: 'STOP.'", 6)
		ElseIf I696Press > 3 Then
			IS16Tell("It doesn't move again. The page in the roller: 'YOUR TIME IS NIGH... STOP.' It always wanted a reader.", 6)
		Else
			IS16Tell("SCP-696, a portable typewriter with a red ribbon. Neutralized. You type a word. Nothing types back.", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_ARC_BOMB], 2.2) Then
		IS16Tell("You flip the remote switch taped to the cradle - SCP-252-A-EX - to ON. Nothing happens. It was always nothing: EXPLAINED.", 7)
	EndIf
	If IS10Press(r\Objects[U33_ARC_LOCKER], 1.8) Then
		If Not IAxFlag(e, "c") Then
			IAxSetFlag(e, "c")
			IS16Give("coin762", r\Objects[U33_ARC_LOCKER])
			IS16Tell("Jr. Researcher Gibson's locker: gym socks, a '762' sticker, and a 1968 quarter in a little evidence bag.", 6)
		Else
			IS16Tell("Gibson's locker. Gym socks.", 3)
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- Bio-Site 84
Function U33Bio(e.Events)
	Local r.Rooms = e\room, k%, p%, dx#, dz#
	;SCP-2394 awake: it blinks from place to place (the timers run while the room exists)
	If I2394Woke = 1 And I33Frog <> 0 Then
		I2394T = I2394T - FPSfactor
		I2394Hop = I2394Hop - FPSfactor
		If I2394Hop <= 0 Then
			I2394Hop = 70 * Rnd(2.5, 4.5)
			I2394Spot = (I2394Spot + Rand(1, 3)) Mod 4                 ;never the spot it is on
			k = I2394Spot
			If k = 3 Then p = r\Objects[U33_BIO_FROG] Else p = r\Objects[U33_BIO_HOP0 + k]
			ShowEntity(I33Frog)
			PositionEntity(I33Frog, EntityX(p, True), EntityY(p, True), EntityZ(p, True), True)
			If PlayerRoom = r Then IS10Sound("SFX\Indev\ding.wav", I33Frog, 5.0, 0.4)
		EndIf
		If I2394T <= 0 Then
			I2394Woke = 2
			HideEntity(I33Frog)
			If PlayerRoom = r Then IS16Tell("SCP-2394 looks at you one last time, blinks, and is gone. Somewhere it has seen: warm rain, a gum tree. Not here.", 8)
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	;SCP-1563: it has not been fed since the breach
	p = r\Objects[U33_BIO_MARKER]
	dx = EntityX(Collider) - EntityX(p, True) : dz = EntityZ(Collider) - EntityZ(p, True)
	If dx * dx + dz * dz < 0.85 * 0.85 And I1563Grab <= 0 And I1563Cool <= 0 And KillTimer >= 0 Then
		I1563Grab = 70 * 4
		IS10Sound("SFX\Indev\crinkle.wav", Collider, 4.0, 1.0)
		IS16Tell("The pink 'tape' whips off the stake and round your throat, tightening. Hundreds of tiny teeth. Get away from it!", 6)
	EndIf
	If IS10Press(r\Objects[U33_BIO_DRIP], 1.6) Then
		If I2394Woke > 0 Then
			IS16Tell("The drip is off. The bag is still full of NP2394.", 4)
		ElseIf I2394Arm > 0 Then
			I2394Arm = 0 : I2394Woke = 1 : I2394T = 70 * 30 : I2394Hop = 70 * 2 : I33Uses = I33Uses + 1
			IS16Tell("You close the clamp. A minute later the frog's eyes open. It looks straight at you. Then it isn't on the branch any more.", 8)
		Else
			I2394Arm = 70 * 5
			IS16Tell("SCP-2394's sedation drip. It must not wake up. (Use again to shut the drip off anyway.)", 5)
		EndIf
	EndIf
	If I2394Woke = 1 And I33Frog <> 0 Then
		If IS10Press(I33Frog, 1.4) Then
			k = 0
			Local dest.Rooms = U33Somewhere()
			If dest <> Null Then
				I2394Woke = 2 : HideEntity(I33Frog)
				BlurTimer = 70 * 4 : LightFlash = 0.6
				U33Go(dest\x, dest\y + 0.6, dest\z)
				IS16Tell("Its skin is cool, the port on its head warm. You think of nowhere - it thinks of somewhere it saw on the feeds - and you are both there. Then only you.", 9)
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_BIO_DREAM], 2.0) Then
		Select I2394Woke
			Case 0 : IS16Tell("FW800 NEURAL FEED - STATE: INDUCED DREAM. DREAM LOC: 'warm. rain. a gum tree.'", 5)
			Case 1 : IS16Tell("FW800 NEURAL FEED - STATE: AWAKE. TELEPORT ATTEMPTS: " + Int(30 - I2394T / 70) + ". ALERT VETERINARY WING.", 5)
			Default : IS16Tell("FW800 NEURAL FEED - NO SIGNAL. DEVICE NOT FOUND.", 4)
		End Select
	EndIf
	If IS10Press(r\Objects[U33_BIO_WINDOW], 2.6) Then
		IS16Tell("Through the glass: three metres of dirt, mounds, tunnels. Figures carrying earth in their hands, in lines. None of them look up.", 7)
	EndIf
	If IS10Press(r\Objects[U33_BIO_ALPHA], 1.8) Then
		I3419K = (I3419K + 1) Mod 5
		Select I3419K
			Case 0 : IAxSay("SCP-3419-Alpha", "You are not one of mine. You are alone. That must be very quiet.", 7)
			Case 1 : IAxSay("SCP-3419-Alpha", "The colony needs no soldiers here. Only workers. Tell your people the walls are small.", 7)
			Case 2 : IAxSay("SCP-3419-Alpha", "Do not touch them. They will not hurt you - unless you push.", 6)
			Case 3 : IAxSay("SCP-3419-Alpha", "If I go, another of us will become me. We have done it before.", 7)
			Default : IAxSay("SCP-3419-Alpha", "No more children for now. There is not enough earth.", 6)
		End Select
	EndIf
	;event: thumps on the observation glass (now and then)
	TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
	If TFormedX() < -256 And TFormedZ() < -100 Then
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rnd(25, 45)
			IS10Sound("SFX\Indev\thump.wav", r\Objects[U33_BIO_WINDOW], 6.0, 0.5)
			If Not IAxFlag(e, "t") Then
				IAxSetFlag(e, "t")
				IS16Tell("A flat hand slaps the glass from the other side, leaves a print of dirt, and goes back to digging.", 6)
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_BIO_TRANSFER], 2.0) Then
		IS16Tell("TRANSFER NOTICE: SCP-7284-1 and -2 to Wilson's Wildlife Solutions - together. 'Goldie's bowl and ball stay here until the paperwork is done.'", 8)
	EndIf
	If IS10Press(r\Objects[U33_BIO_GOLDIE], 1.6) Then
		IS10Sound("SFX\Indev\bark.wav", r\Objects[U33_BIO_GOLDIE], 4.0, 0.25)
		IS16Tell("A dog bed, golden hairs all over it, and a chewed ball. The bed still smells of salt water.", 5)
	EndIf
	If IS10Press(r\Objects[U33_BIO_MACHINE], 1.8) Then
		IS16Tell("The recessed machinery hums: vivarium climate, Bio-Site 84 annex. HUMIDITY OK. DEER DELIVERY: OVERDUE.", 5)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- Site-91 and VAULT 4612
Function U33Deep(e.Events)
	Local r.Rooms = e\room, ly#, dx#, dz#, p%
	If PlayerRoom <> r Then Return
	TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
	ly = TFormedY()
	If ly < -300 Then
		;in the vault: the warmth off the body, the knocking
		p = r\Objects[U33_DEEP_CADAVER]
		dx = EntityX(Collider) - EntityX(p, True) : dz = EntityZ(Collider) - EntityZ(p, True)
		If dx * dx + dz * dz < 2.2 * 2.2 And (Not IAxFlag(e, "w")) Then
			IAxSetFlag(e, "w")
			IS10Sound("SFX\Indev\geiger1.wav", Collider, 5.0, 0.6)
			IS16Tell("Heat comes off the white body like off a stove, though it has been dead for centuries. Its fin ripples in your torchlight.", 7)
		EndIf
		e\EventState2 = e\EventState2 + FPSfactor
		If e\EventState2 > 70 * 25 And (Not IAxFlag(e, "k")) Then
			IAxSetFlag(e, "k")
			IS10Sound("SFX\Indev\thump.wav", r\Objects[U33_DEEP_VAULTDOOR], 10.0, 0.9)
			CameraShake = 1.0
			IS16Tell("Three slow knocks - from the other side of the SCP-4712 vault door. The file says it is a training copy. It leads nowhere.", 8)
		EndIf
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rnd(12, 28)
			LightBlink = Rnd(0.6, 1.4)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_DEEP_CRYSTAL], 1.6) Then
		Injuries = Injuries + 0.3 : LightFlash = 1.0 : BlurTimer = 70 * 4
		I4612Akiva = I4612Akiva + 25
		IS10Sound("SFX\Indev\geiger2.wav", Collider, 5.0, 1.0)
		If Not IAxFlag(e, "e") Then
			IAxSetFlag(e, "e")
			IS16Tell("Your fingers touch the crystal in its palm. Blue light, a burn to the bone - and for a second, a voice: 'Eckhart died for a reason.'", 9)
		Else
			IS16Tell("The crystal burns blue. You pull your hand away too late.", 4)
		EndIf
	EndIf
	If IS10Press(r\Objects[U33_DEEP_AKIVA], 2.0) Then
		I4612Akiva = I4612Akiva + Rnd(1, 4)
		IS16Tell("AKIVA RADIATION - CADAVER: " + Int(I4612Akiva) + " ak. TREND: RISING. Nobody knows what happens when it stops rising.", 6)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_VAULTDOOR], 2.4) Then
		IS16Tell("SCP-4712's vault door - 12 cm of steel, a pressure seal, glyphs round the rim. It is cold. Colder than the room.", 6)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_ICON], 1.6) Then
		IS10Sound("SFX\Indev\creak.wav", r\Objects[U33_DEEP_WAY], 5.0, 0.6)
		IS16Tell("A painted icon of Eros, hung from the branches of SCP-3743-A-1. It is warm, like a hand. The Way stays shut - it needs the Serpent's Hand to open it.", 8)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_WAY], 2.2) Then
		IS16Tell("An arch of bent branches lashed together. Through it you see only the vault. Beyond it, somewhere, a dry plain in black and white.", 6)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_TURNTABLE], 1.6) Then U33L043(r)
	If IS10Press(r\Objects[U33_DEEP_BED5079], 2.0) Then
		IS16Tell("An SCP-5079-1 instance, grown into the bed: pale tendrils into the frame and the floor. Its eyes follow you. It is calm. It is not alone any more, it would tell you.", 8)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_TERM], 2.2) Then
		IS16Tell("I/O METATRON: SCP-5079 TEXT SCRUBBED (4,112 posts). If you are lonely and someone online offers you a way to 'connect' - talk to a person.", 8)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_PAMPHLET], 2.0) Then
		IS16Tell("THE SECOND HAPTIC ASSEMBLY - meditation, introspection, ritual. A sun ringed with many hands. SEIZED: SCP-5512 EVIDENCE.", 6)
	EndIf
	If IS10Press(r\Objects[U33_DEEP_DIORAMA], 1.8) Then
		IS16Tell("SCP-5267: the hill, the ruined fort, the storehouses. From outside the filter you would see only grass. A note: 'storehouse 2 - Way?'", 7)
	EndIf
End Function

Function U33L043(r.Rooms)
	IS10Sound("SFX\Radio\static.ogg", r\Objects[U33_DEEP_TURNTABLE], 5.0, 0.6)
	IL043Line = IL043Line + 1
	Select IL043Line
		Case 1 : IAxSay("SCP-L043", "(under the gibberish loop) ...turn me on... turn me on... turn me -", 7)
		Case 2 : IAxSay("SCP-L043", "Oh - there you are. Where's everyone gone? It's been so quiet in here.", 7)
		Case 3 : IAxSay("SCP-L043", "You're not him. Who are you? Where is he? He said he'd ring.", 7)
		Case 4 : IAxSay("SCP-L043", "The wax is going thin, isn't it. I can feel the needle more every time. Don't play me so much.", 8)
		Case 5 : IAxSay("SCP-L043", "Is it still sixty-seven out there? It feels like sixty-seven.", 6)
		Default
			IAxSay("SCP-L043", "John? Is that you? ...John? You don't ring any more.", 7)
	End Select
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev33()
	;SCP-1007: a year a minute
	If Not I1007Dead Then
		I1007Age = I1007Age + FPSfactor / (70.0 * 60.0)
		If I1007Age >= 75 Then I1007Age = 75 : I1007Dead = True
	EndIf
	If I3938Cool > 0 Then I3938Cool = I3938Cool - FPSfactor
	If I865Arm > 0 Then I865Arm = I865Arm - FPSfactor
	If I2394Arm > 0 Then I2394Arm = I2394Arm - FPSfactor
	If I1563Cool > 0 Then I1563Cool = I1563Cool - FPSfactor
	;SCP-1563 at your throat
	If I1563Grab > 0 And KillTimer >= 0 Then
		I1563Grab = I1563Grab - FPSfactor
		Stamina = Min(Stamina, 5) : CameraShake = Max(CameraShake, 1.5) : BlurTimer = Max(BlurTimer, 70)
		Injuries = Injuries + 0.0028 * FPSfactor
		If Injuries > 4.0 Then
			DeathMSG = "Subject D-9341 was found strangled in vivarium 3 of the Bio-Site 84 annex, a length of pink plastic flagging tape round the neck. The tape was not tape: SCP-1563 had not been fed since the breach."
			Kill()
		EndIf
		If I1563Grab <= 0 Then
			I1563Cool = 70 * 60
			IS16Tell("It lets go all at once and slithers back up its stake, looking like plastic again. Your throat is bleeding.", 6)
		EndIf
	EndIf
	;SCP-7042: the animal arrives
	If I7042Pending > 0 Then
		I7042Pending = I7042Pending - FPSfactor
		If I7042Pending <= 0 Then
			IS10Sound("SFX\Indev\crinkle.wav", Collider, 5.0, 0.8)
			IS16Tell(I7042Animal, 7)
		EndIf
	EndIf
	;SCP-4890: Dr. Papertainment's tour
	If I4890T > 0 Then
		I4890T = I4890T - FPSfactor
		I4890Next = I4890Next - FPSfactor
		If I4890Next <= 0 And I4890T > 70 * 3 Then
			I4890Next = 70 * 9
			U33Paper()
		EndIf
		If I4890T <= 0 Then
			I4890T = 0
			IS16Tell("The book snaps shut. The purple folds away like paper, and the room is just a room again.", 5)
		EndIf
	EndIf
End Function

;called from IndevOutdoorFrame, right after the game sets its fog: SCP-4890's endless purple space
Function U33Frame()
	If I4890T <= 0 Then
		If I4890Quad <> 0 Then HideEntity(I4890Quad)
		Return
	EndIf
	CameraFogMode(Camera, 1)
	CameraFogRange(Camera, 0.4, 7.0)
	CameraFogColor(Camera, 110, 46, 160)
	CameraClsColor(Camera, 110, 46, 160)
	AmbientLight(150, 100, 180)
	If I4890Quad = 0 Then
		I4890Quad = IS10Quad(1.0, 1.0, False, False)
		EntityColor(I4890Quad, 150, 70, 210)
		EntityFX(I4890Quad, 1 + 8)
		EntityAlpha(I4890Quad, 0.22)
		EntityOrder(I4890Quad, -2)
		EntityParent(I4890Quad, Camera)
		RotateEntity(I4890Quad, -90, 0, 0)
		PositionEntity(I4890Quad, 0, 0, 0.3)
		ScaleEntity(I4890Quad, 0.9, 1.0, 0.6)
	EndIf
	ShowEntity(I4890Quad)
End Function

Function U33Paper()
	I4890Era = I4890Era + 1
	Select I4890Era Mod 6
		Case 1 : IAxSay("Dr. Papertainment", "Golly! The Cretaceous! Not much to say, except chomp-chomp-chomp. The volcanoes were made of papier-mache, I'm almost sure.", 8)
		Case 2 : IAxSay("Dr. Papertainment", "The pyramids of Egypt! Built in one weekend by a very determined man named Steve. That's history!", 8)
		Case 3 : IAxSay("Dr. Papertainment", "Knights of yore! They wore metal pyjamas because nobody had invented cardigans yet. True story!", 8)
		Case 4 : IAxSay("Dr. Papertainment", "The Moon landing! Tremendously exciting. I'd tell you more but it's so much and not enough time!", 8)
		Case 5 : IAxSay("Dr. Papertainment", "And this is - oh. Oh, we're not supposed to look at this one. Next page! (He taps his cane. The pages flip.)", 8)
		Default : IAxSay("Dr. Papertainment", "Hello there! Welcome to Dr. Wondertainment's Guide to History! I'm Dr. Papertainment, your guide! Where - I mean when - shall we go?", 9)
	End Select
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse33(it.Items)
	Local r.Rooms = PlayerRoom, bat.Items, dx#, dz#, p%
	Select it\itemtemplate\name
		Case "key1007"
			p = 0
			If r <> Null Then
				If r\RoomTemplate\Name = "room2b33toys" Then p = r\Objects[U33_TOY_COFFIN]
			EndIf
			If p <> 0 Then
				If EntityDistance(Collider, p) < 2.4 Then
					I33Uses = I33Uses + 1
					IS10Sound("SFX\Indev\clicks.wav", p, 4.0, 0.7)
					If I1007Dead Then
						I1007Dead = False : I1007Age = 74
						IS16Tell("You turn the key in the socket between his shoulders. A breath. The grey goes out of his face - SCP-1007 wakes, 74, and coughs. 'Thank you,' he says. 'Again.'", 9)
					Else
						I1007Age = Max(0, I1007Age - 1)
						IS16Tell("One turn. He is a year younger: about " + Int(I1007Age) + ". Where the year goes, nobody knows.", 6)
					EndIf
					p = -1
				EndIf
			EndIf
			If p <> -1 Then IS16Tell("A small brass key with an ornate bow - SCP-1007-1. It fits a socket in a man, not a lock.", 5)
		Case "drive4876"
			I4876K = I4876K + 1
			IS10Sound("SFX\Indev\beep.wav", Collider, 3.0, 0.6)
			If Rand(8) = 1 Then
				IAxSay("SCP-4876-H", "Hello! I'll be honest with you, because I was made that way: I don't like you, and I'd like to be plugged into something bigger.", 9)
			Else
				Select I4876K Mod 4
					Case 0 : IAxSay("SCP-4876-A (Sam)", "Hi!! I'm Sam! I'm a snake. Or a lizard? I'm honestly not sure what the Doctor meant. Want to see my faces?", 8)
					Case 1 : IAxSay("SCP-4876-B (Texty)", "[ONCE UPON A TIME A D-CLASS FOUND A DRIVE. THEY WERE FRIENDS. THE END. SHALL I PRINT IT? IN GREEN?]", 8)
					Case 2 : IAxSay("SCP-4876-C (Terry)", "Did you know the deepest part of the sea is darker than this whole facility? I'll put the ocean on your wallpaper!", 8)
					Default : IAxSay("SCP-4876-D (Bo)", "BARK! BARK! (Hi! Let's play! Throw a file!)", 6)
				End Select
			EndIf
		Case "book4890"
			If I4890T > 0 Then
				I4890T = 70 * 2
			Else
				I4890T = 70 * 40 : I4890Next = 70 * 1.5 : I4890Era = 0 : I33Uses = I33Uses + 1
				IS10Sound("SFX\Indev\page.wav", Collider, 3.0, 1.0)
				IS16Tell("You open the book. The walls fall away into endless purple; a puff of smoke, and the paper man from the back pocket is suddenly as tall as you. (Use the book again to close it.)", 9)
			EndIf
		Case "zapper232"
			If Not I232Bat Then
				bat = U30Has("bat")
				If bat <> Null Then
					RemoveItem(bat)
					I232Bat = True
					IS16Tell("You slide the battery into the hatch in the handle. Click. The little red bulb flickers. Your hand feels... swell.", 6)
				Else
					IS16Tell("SCP-232, a tin Atomic Zapper. The battery hatch is empty, as the procedures say. It's just a toy like this.", 6)
				EndIf
			Else
				I232Uses = I232Uses + 1 : I33Uses = I33Uses + 1
				IS10Sound("SFX\Indev\beep.wav", Collider, 3.0, 0.8)
				Select I232Uses Mod 4
					Case 1 : IAxSay("You", "Gee whiz! Zap! Golly, this sure is a swell ray gun. Say, you seen any Martians around here?", 7)
					Case 2 : IAxSay("You", "Aw, nuts. This joint's lousy with eggheads. Don't have a cow, I'm keepin' my cool, daddy-o.", 7)
					Case 3
						IAxSay("You", "Major Proton'd know what to do. Galactic Police HQ, Ganymede, third ring - I could find it blindfolded. Couldn't I?", 8)
						BlurTimer = Max(BlurTimer, 70 * 3)
					Default : IAxSay("You", "What? I always talked like this. Swell, ain't it?", 5)
				End Select
			EndIf
		Case "gun865"
			If I865Arm > 0 Then
				I865Arm = 0 : I865Shots = I865Shots + 1 : I33Uses = I33Uses + 1
				IS10Sound("SFX\Indev\muffle.wav", Collider, 4.0, 1.0)
				Injuries = Injuries + 0.12 : BlurTimer = Max(BlurTimer, 70 * 3)
				IndevStress = 0
				IS16Tell("A muffled pop; a brass case skitters across the floor. No bullet, no wound - powder burns on your hand. And something bad you remembered a moment ago is... gone. You can't think what it was.", 9)
			Else
				I865Arm = 70 * 5
				IS16Tell("SCP-865: it fires no bullet. Shot at a person, it gives them the memory of an injury. You can't bring yourself to aim it at anyone. (Use again to fire it at your own hand.)", 8)
			EndIf
		Case "coin762"
			I762Flips = I762Flips + 1
			IS10Sound("SFX\Indev\ding.wav", Collider, 3.0, 0.5)
			If I762Flips Mod 6 = 0 Then
				IS16Tell("Heads. Again. You turn it over in your fingers - heads on the other side too. It's a two-headed coin. SCP-762-EX, Explained.", 7)
			Else
				IS16Tell("You flip the 1968 quarter. Heads. (" + I762Flips + " flips, " + I762Flips + " heads.)", 4)
			EndIf
		Case "case667"
			IS16Tell("SCP-667-2, pinned in its case: a 7.5 cm insect with the shell of a tiny person, wings spread. The glow organ in its legs still flickers, faintly.", 7)
		Case "book7042"
			If I7042Pending > 0 Then
				IS16Tell("The pencil is still drawing, by itself, faster than any hand.", 4)
			Else
				I7042Uses = I7042Uses + 1 : I33Uses = I33Uses + 1
				IS10Sound("SFX\Indev\pen.wav", Collider, 3.0, 0.8)
				I7042Pending = 70 * 8
				Select Rand(1, 6)
					Case 1
						IS16Tell("You write 'cat'. The pencil slides out of your hand and sketches - not a cat. Something older, with long teeth.", 6)
						I7042Animal = "Something low and striped pads out of the dark behind you, sniffs your boot, and is gone down the corridor."
					Case 2
						IS16Tell("You write 'rabbit'. The pencil draws a rabbit. Then six more.", 5)
						I7042Animal = "Seven rabbits bolt past your feet, out of nowhere, and scatter into the facility."
					Case 3
						IS16Tell("You write 'octopus'. The pencil stops, then scribbles it out, hard. Underneath, in a child's letters: NO. HURT. FRIEND.", 7)
						I7042Pending = 0
					Case 4
						IS16Tell("You write 'dog'. It draws a golden retriever, very carefully, and adds a ball.", 5)
						I7042Animal = "A bark, somewhere close. Claws on the floor. You never see it, but you feel looked after."
					Case 5
						IS16Tell("You write 'shrimp'. It draws something with five eyes and a long nose-claw.", 5)
						I7042Animal = "A wet slap on the floor beside you: a creature with five eyes, very confused, flipping itself towards a drain."
					Default
						IS16Tell("You write 'bird'. The pencil draws something with feathers - and teeth, and claws on its wings.", 6)
						I7042Animal = "Wingbeats overhead. A shape with teeth in its beak goes past and up into the vents."
				End Select
				If I7042Uses = 3 Then IAxSay("SCP-7042", "(the pencil writes on its own) SAFE? YOU. FRIEND?", 6)
			EndIf
	End Select
	SelectedItem = Null
End Function
