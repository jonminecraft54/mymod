;=====================================================================
; SCP: Containment Breach - Indev: the twenty-ninth batch - SCP-820-JP, SCP-867, SCP-120 and Lunar Area-32
;
;   room2b29blade   SCP-820-JP's inspection dock. An unmanned submarine circles the tank without stopping and
;                   surfaces at the dock for a few seconds about once a minute; while it is up, the hatch holds the
;                   knife (item scp820jp, once). Carry the knife and stay in one room for too long and its transmitter
;                   signals: a retrieval team takes it back to the submarine. Look at it (use it) too often and you
;                   start to want to use it, somewhere everybody would see. The stall across the corridor sells
;                   "famous local cookies" - the knife's contagious fascination at work.
;   room2b29spruce  SCP-867, Section E. Brush against a tree without the hazmat suit and a seed is injected. It
;                   sleeps for five minutes, then grows: about a minute of agony, then death. The herbicide injector
;                   (item herbicide867), the decontamination shower or SCP-500 kills it.
;   room2b29pool    SCP-120. The liquid's colour shows which of its eleven destinations it is set to; the dial in
;                   the operators' room moves it on (a Class-D is sent through - one per dial). Step into the pool,
;                   carrying six things or fewer (the 37.8 kg limit), and you go:
;                     9 grey   Lunar Area-32, built into this same room far above (y 3072): one-sixth gravity, the
;                              reception, observatory, cargo bay (the supply lander home), and by lift Sub-Level 1:
;                              the sealed SCP-001 vault, the SCP-L001 records terminal, SCP-2219, storage
;                     3 5 8 10 11 black   Lagrange points: lost
;                     1 2 4 6 7   the Earth outposts: Sigma-6 sends you back to the outbuilding hours later
;                   Every use moves SCP-120 on by one.
;   Summaries of scp-wiki.wikidot.com/scp-820-jp, /scp-867, /scp-120, /secure-facility-dossier-lunar-area-32,
;   /scp-2219 and /scp-l001 (CC BY-SA 3.0).
;=====================================================================

Global I120Dest%            ;SCP-120's configuration, 1..11 (kept in the save)
Global I120In%              ;the player is standing in the pool (it fires once per step in)
Global I867Seed#            ;frames until an SCP-867 seed wakes (0 = none)
Global I867Pain#            ;frames of agony left (0 = none)
Global I820Taken%           ;the knife is out of the submarine
Global I820Look#            ;how long you have looked at the knife
Global I820Here#, I820Warned%, I820Room.Rooms
Global I29Sub%, I29SubT#, I29Liquid%, Indev29Uses%

Const U29_LUNAR_Y# = 3072.0
Const U29_LUNAR_Y1# = 2432.0

Function Indev29Reset(newGame%)
	If newGame Then
		I120Dest = Rand(1, 11)
		I820Taken = 0
	EndIf
	I120In = 0 : I867Seed = 0 : I867Pain = 0 : I820Look = 0 : I820Here = 0 : I820Warned = 0 : I820Room = Null
	;I29Sub / I29Liquid are not cleared: the rooms set them when built, and a quick load keeps the rooms
End Function

Function IndevU29Dress(r.Rooms)
	Local body%, sail%, prop%, k%, m%, tree0%, p%, s#
	Select r\RoomTemplate\Name
		Case "room2b29spruce"
			;the four blood-red spruces: the HD model (Tools\roomkit\make_hd29.py), one loaded, three copies
			If FileType("GFX\map\props\scp867.b3d") = 1 Then
				For k = 0 To 3
					p = r\Objects[U29_SPR_T0 + k]
					If tree0 = 0 Then
						tree0 = LoadMesh_Strict("GFX\map\props\scp867.b3d")
						m = tree0
					Else
						m = CopyEntity(tree0)
					EndIf
					s = Rnd(0.8, 0.9)
					ScaleEntity(m, RoomScale * s, RoomScale * s, RoomScale * s)
					PositionEntity(m, EntityX(p, True), EntityY(r\obj, True) + 2 * RoomScale, EntityZ(p, True), True)
					RotateEntity(m, 0, Rnd(360), 0, True)
					EntityParent(m, r\obj, True)
				Next
			EndIf
		Case "room2b29blade"
			;the unmanned submarine: a yellow hull, a sail, a propeller - long along its own z
			I29Sub = CreatePivot()
			body = CreateSphere(12, I29Sub)
			ScaleEntity(body, 0.07, 0.065, 0.30)
			EntityColor(body, 214, 172, 40)
			EntityShininess(body, 0.6)
			sail = CreateCube(I29Sub)
			ScaleEntity(sail, 0.025, 0.045, 0.06)
			PositionEntity(sail, 0, 0.08, 0.06)
			EntityColor(sail, 60, 60, 66)
			prop = CreateCylinder(8, True, I29Sub)
			ScaleEntity(prop, 0.05, 0.008, 0.05)
			RotateEntity(prop, 90, 0, 0)
			PositionEntity(prop, 0, 0, -0.31)
			EntityColor(prop, 120, 110, 90)
			PositionEntity(I29Sub, EntityX(r\Objects[U29_BLD_SUBC], True), EntityY(r\Objects[U29_BLD_SUBC], True), EntityZ(r\Objects[U29_BLD_SUBC], True), True)
			EntityParent(I29Sub, r\obj, True)
		Case "room2b29pool"
			;the liquid: a flat glowing disc whose colour is the destination
			I29Liquid = CreateCylinder(28, True)
			ScaleEntity(I29Liquid, 198 * RoomScale, 0.004, 198 * RoomScale)
			PositionEntity(I29Liquid, EntityX(r\Objects[U29_POL_POOL], True), EntityY(r\obj, True) + 46 * RoomScale, EntityZ(r\Objects[U29_POL_POOL], True), True)
			EntityFX(I29Liquid, 1)
			EntityAlpha(I29Liquid, 0.88)
			EntityParent(I29Liquid, r\obj, True)
			U29Colour(1.0)
	End Select
End Function

;the colour of SCP-120's liquid for its current destination
Function U29Colour(k#)
	Local cr%, cg%, cb%
	If I29Liquid = 0 Then Return
	Select I120Dest
		Case 1 : cr = 40 : cg = 110 : cb = 240
		Case 2, 4 : cr = 240 : cg = 244 : cb = 255
		Case 6 : cr = 240 : cg = 210 : cb = 40
		Case 7 : cr = 140 : cg = 96 : cb = 52
		Case 9 : cr = 140 : cg = 140 : cb = 148
		Default : cr = 4 : cg = 4 : cb = 8
	End Select
	EntityColor(I29Liquid, cr * k, cg * k, cb * k)
End Function

Function U29DestName$(d%)
	Select d
		Case 1 : Return "1 - blue - the Pacific (SCPS Demeter)"
		Case 2 : Return "2 - white - Greenland"
		Case 3 : Return "3 - black - Lagrange point L3"
		Case 4 : Return "4 - white - the Himalayas"
		Case 5 : Return "5 - black - Lagrange point L5"
		Case 6 : Return "6 - yellow - the Sahara"
		Case 7 : Return "7 - brown - the Gobi"
		Case 8 : Return "8 - black - Lagrange point L2"
		Case 9 : Return "9 - grey - Mare Imbrium (Lunar Area-32)"
		Case 10 : Return "10 - black - Lagrange point L4"
	End Select
	Return "11 - black - Lagrange point L1"
End Function

Function UpdateIndevU29(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b29blade" : U29Blade(e)
		Case "room2b29spruce" : U29Spruce(e)
		Case "room2b29pool"
			IndevLiftTick(e) ;the lift between the surface and Sub-Level 1 of Lunar Area-32
			U29Pool(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- SCP-820-JP
Function U29Blade(e.Events)
	Local r.Rooms = e\room, c% = r\Objects[U29_BLD_SUBC], d% = r\Objects[U29_BLD_DOCK]
	Local cyc# = 70 * 60, t#, a#, k#, ox#, oz#, x#, y#, z#, px#, pz#, up%
	Local dx#, dy#, dz#, lx#, lz#
	;the submarine: 40 s circling under water, 5 s to the dock, 2 s up, 10 s surfaced, 3 s down again
	I29SubT = I29SubT + FPSfactor
	t = I29SubT - Floor(I29SubT / cyc) * cyc
	If I29Sub <> 0 Then
		a = Min(t, 70 * 40) * 0.25
		TFormVector(150 * Cos(a), 0, 260 * Sin(a), r\obj, 0)
		ox = TFormedX() : oz = TFormedZ()
		x = EntityX(c, True) + ox : z = EntityZ(c, True) + oz : y = EntityY(c, True)
		dx = EntityX(d, True) : dz = EntityZ(d, True) : dy = EntityY(d, True) - 6 * RoomScale
		If t < 70 * 40 Then
			px = x : pz = z
		ElseIf t < 70 * 45 Then
			k = (t - 70 * 40) / (70 * 5)
			px = x + (dx - x) * k : pz = z + (dz - z) * k
		ElseIf t < 70 * 47 Then
			k = (t - 70 * 45) / (70 * 2)
			px = dx : pz = dz : y = y + (dy - y) * k
		ElseIf t < 70 * 57 Then
			px = dx : pz = dz : y = dy : up = True
		Else
			k = (t - 70 * 57) / (70 * 3)
			px = dx + (x - dx) * k : pz = dz + (z - dz) * k : y = dy + (y - dy) * k
		EndIf
		lx = EntityX(I29Sub, True) : lz = EntityZ(I29Sub, True)
		If Abs(px - lx) + Abs(pz - lz) > 0.0005 Then RotateEntity(I29Sub, 0, VectorYaw(px - lx, 0, pz - lz), 0, True)
		PositionEntity(I29Sub, px, y, pz, True)
	EndIf
	If PlayerRoom <> r Then Return
	If IS10Press(d, 2.0) Then
		If t >= 70 * 47 And t < 70 * 57 Then
			If Not I820Taken Then
				I820Taken = True
				Indev29Uses = Indev29Uses + 1
				IS16Give("scp820jp", d)
				IS10Sound("SFX\Indev\ding.wav", d, 6.0, 0.6)
				IS16Tell("The hatch hisses open on a padded case. In it, a stone knife with a snake coiled round the blade. You could just take it.", 7)
			Else
				IS16Tell("The hatch opens on an empty padded case and a blinking transmitter cradle. The knife is out of containment.", 6)
			EndIf
		Else
			IS16Tell("The submarine is under way somewhere in the tank. It surfaces at the dock for inspection about once a minute.", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[U29_BLD_COOKIES], 1.6) Then
		Indev29Uses = Indev29Uses + 1
		Stamina = 100
		I820Look = I820Look + 70 * 8
		IS16Tell("A free sample of the famous local cookies: shattered biscuit set in chocolate, with raspberry. Delicious. You'd quite like to see where it all happened.", 7)
	EndIf
	If IS10Press(r\Objects[U29_BLD_PIG], 1.8) Then
		IS16Tell("A pig mascot in a costume dressed like... someone. Nobody is inside it. You find yourself waving back at it anyway.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- SCP-867
Function U29Spruce(e.Events)
	Local r.Rooms = e\room, k%, p%, dx#, dz#
	If PlayerRoom <> r Then
		IS13Drop(e, "h")
		Return
	EndIf
	For k = 0 To 3
		p = r\Objects[U29_SPR_T0 + k]
		dx = EntityX(Collider) - EntityX(p, True) : dz = EntityZ(Collider) - EntityZ(p, True)
		If dx * dx + dz * dz < 0.72 * 0.72 Then
			If WearingHazmat > 0 Then
				If Not IAxFlag(e, "h") Then
					IAxSetFlag(e, "h")
					IS16Tell("Red needles rattle across the suit like hail. The Kevlar underlayer holds.", 5)
				EndIf
			ElseIf I867Seed = 0 And I867Pain = 0 Then
				I867Seed = 70 * 60 * 5
				Indev29Uses = Indev29Uses + 1
				IS16Tell("A branch brushes your neck, soft as a feather. You don't feel anything at all.", 5)
			EndIf
		EndIf
	Next
	If IS10Press(r\Objects[U29_SPR_ROVER], 1.8) Then
		IS16Tell("REMOTE ROVER R-2: irrigation 100%. Needle shed 0.3%. New specimens: 0. Last host: [DATA EXPUNGED].", 6)
	EndIf
	If IS10Press(r\Objects[U29_SPR_SHOWER], 1.6) Then
		Indev29Uses = Indev29Uses + 1
		BlurTimer = Max(BlurTimer, 70 * 3)
		If I867Seed > 0 Or I867Pain > 0 Then
			I867Seed = 0 : I867Pain = 0
			IS16Tell("Herbicide mist, stinging, bitter. Afterwards you find it: a tiny puncture under your jaw, scabbed over. Whatever was in it is dead. Fifteen days' quarantine, says the sign.", 8)
		Else
			IS16Tell("Herbicide mist, stinging, bitter. You check yourself all over for puncture marks. None. Lucky.", 6)
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- SCP-120
Function U29Pool(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U29_POL_POOL], dx#, dz#, dd#
	If I29Liquid <> 0 Then U29Colour(0.88 + 0.12 * Sin(MilliSecs() * 0.05))
	If e\EventState2 > 0 Then e\EventState2 = e\EventState2 - FPSfactor
	If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
	If PlayerRoom <> r Then Return
	;the operators' room
	If IS10Press(r\Objects[U29_POL_DIAL], 1.8) Then
		If e\EventState2 > 0 Then
			IS16Tell("The dial is still resetting.", 2)
		Else
			e\EventState2 = 70 * 3
			I120Dest = (I120Dest Mod 11) + 1
			Indev29Uses = Indev29Uses + 1
			IS10Sound("SFX\Indev\buzzer.wav", r\Objects[U29_POL_DIAL], 5.0, 0.6)
			IS16Tell("On the monitor a Class-D steps into the pool and is gone. The glow changes. SCP-120 is now at destination " + U29DestName(I120Dest) + ".", 7)
		EndIf
	EndIf
	If IS10Press(r\Objects[U29_POL_CHART], 1.8) Then
		IS16Tell("The chart, read against the camera feed: SCP-120 is at destination " + U29DestName(I120Dest) + ".", 6)
	EndIf
	;stepping into the pool
	dx = EntityX(Collider) - EntityX(p, True) : dz = EntityZ(Collider) - EntityZ(p, True)
	dd = Sqr(dx * dx + dz * dz)
	If dd < 0.72 And Abs(EntityY(Collider) - EntityY(p, True)) < 1.0 Then
		If Not I120In Then
			I120In = True
			U29Jump(e)
		EndIf
	ElseIf dd > 0.95 Then
		I120In = False
	EndIf
	;Lunar Area-32
	If IS10Press(r\Objects[U29_POL_LANDER], 2.2) Then
		Indev29Uses = Indev29Uses + 1
		U29Move(r\Objects[U29_POL_RETURN])
		BlurTimer = 70 * 6
		IS16Tell("The supply lander is fuelled and leaving. Three days of noise and weightlessness later, Sigma-6 walk you from the landing site back to SCP-120's outbuilding.", 9)
	EndIf
	If IS10Press(r\Objects[U29_POL_OBS], 2.5) Then
		IS16Tell("Earth hangs over the grey plain of Mare Imbrium, half lit, impossibly blue. Every image of this view is altered before it leaves the Moon.", 7)
	EndIf
	If IS10Press(r\Objects[U29_POL_FREIGHT], 2.0) Then
		IS16Tell("MAIN FREIGHT ELEVATOR - CARGO QUARANTINE IN PROGRESS. Personnel use the lift by the reception.", 5)
	EndIf
	If IS10Press(r\Objects[U29_POL_VAULT], 2.0) Then
		IS16Tell("SCP-001. LEVEL 5. O5 AUTHORISATION. The vault door has no handle, no keypad and no seam you can find. A note is taped under the plate: 'Empty? Ask Investigations.'", 8)
	EndIf
	If IS10Press(r\Objects[U29_POL_REGISTRY], 1.8) Then
		IS16Tell("JURISDICTION: SCP-2493, 2651, 2686, 2821 (Keter), 3321 (Keter), EE-3570, 3609, 3655, 4379, 4731, 4905, 5775, 6981, 7470 (neutralized), 7548 (Keter), 8815, 9042 (Keter). Held here: SCP-001 (sealed), SCP-L001, SCP-2219.", 10)
	EndIf
	If IS10Press(r\Objects[U29_POL_TERM], 1.8) Then
		If Not IAxFlag(e, "t") Then
			IAxSetFlag(e, "t")
			IS16Give("docl001", r\Objects[U29_POL_TERM])
		EndIf
		IS16Tell("SCP-001 INDEX. {$AUTH_PERSON}. {$PROTOCOL_CONTENT}. [ERROR] [ERROR] [ERROR]. Multiple failures registered. The printer spits out a memo.", 7)
	EndIf
	If IS10Press(r\Objects[U29_POL_PROXY], 1.8) Then
		Indev29Uses = Indev29Uses + 1
		Select Rand(4)
			Case 1 : IS16Tell("REMOTE PROXY: GOLDOX collects 100 porridge. The proxy's sensors log nothing. Behind you the locker is very quiet.", 6)
			Case 2 : IS16Tell("REMOTE PROXY: GOLDOX loses a life to PAPAPA. Proxy status: nominal. It doesn't have teeth to lose.", 6)
			Case 3 : IS16Tell("REMOTE PROXY: 22 porridge at the end of level 3. The proxy twitches its servo once. Test logged.", 6)
			Default : IS16Tell("REMOTE PROXY: GAME OVER. 'PROVE YOU WROTH!' The camera feed shows the proxy reset itself. Nobody has beaten DAGRON.", 6)
		End Select
	EndIf
	If IS10Press(r\Objects[U29_POL_LOCKER], 1.6) Then
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * 6
			IS16Tell("SCP-2219, 'PORRIDGE'. DIRECT HUMAN TESTING IS PROHIBITED. ...The handheld is right there. (Again to play.)", 6)
		Else
			e\EventState3 = 0
			Indev29Uses = Indev29Uses + 1
			U29Porridge()
		EndIf
	EndIf
End Function

;SCP-2219, played by hand: what happens in the game happens to you
Function U29Porridge()
	Select Rand(4)
		Case 1
			IndevStress = Max(0, IndevStress - 25)
			IS16Tell("GOLDOX collects 100 porridge. A warm, heavy calm settles over you, like a sedative. You put the game down. Slowly.", 7)
		Case 2
			CameraShake = 3.0 : BlurTimer = Max(BlurTimer, 70 * 4)
			IS16Tell("Level over: 19 porridge. Your vision jerks, your hands spasm - a short seizure. The screen says WEAK UNDESERVING.", 7)
		Case 3
			Stamina = 0 : BlurTimer = Max(BlurTimer, 70 * 6)
			IS16Tell("GOLDOX loses a life. Your throat swells almost shut; every breath whistles. It eases, minutes later.", 7)
		Default
			Injuries = Injuries + 0.8
			IS16Tell("GAME OVER. Numb patches spread across your hands and face as you watch. The note said incompetence would be penalised.", 8)
	End Select
End Function

;SCP-120 takes you: where depends on its configuration, and every use moves it on
Function U29Jump(e.Events)
	Local r.Rooms = e\room, n%, i%, d% = I120Dest
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then n = n + 1
	Next
	If n > 6 Then
		IS16Tell("Your feet meet a smooth floor under the glowing liquid. Nothing happens: you're carrying too much (over 37.8 kg).", 6)
		Return
	EndIf
	Indev29Uses = Indev29Uses + 1
	I120Dest = (I120Dest Mod 11) + 1
	Select d
		Case 9
			U29Move(r\Objects[U29_POL_ARRIVE])
			LightFlash = 1.0
			IS16Tell("You fall through grey light and land on a painted circle in an airtight white room. Your next step lifts you clean off the floor. LUNAR AREA-32, SCP-120 RECEPTION.", 9)
		Case 3, 5, 8, 10, 11
			DeathMSG = "Subject D-9341 entered SCP-120 while it was connected to a Lagrange point. Nothing was recovered. SCP-120 was moved to its next configuration as normal."
			Kill()
			IS16Tell("Black. Cold. No floor, no air, and the Earth very small and very far away.", 8)
		Default
			U29Move(r\Objects[U29_POL_RETURN])
			BlurTimer = 70 * 6
			Stamina = 20
			Select d
				Case 1 : IS16Tell("You drop two metres into a ship's cargo hold, the SCPS Demeter, mid-Pacific. Hours later a helicopter and Sigma-6 bring you back.", 8)
				Case 2 : IS16Tell("Snow, wind, an airstrip under a white sky: Greenland. The outpost crew put you on the next flight back, shivering.", 8)
				Case 4 : IS16Tell("Thin air, a canopy, an eight-metre pit you don't look into: the Himalayas. Sigma-6 bring you back down and home, much later.", 8)
				Case 6 : IS16Tell("Heat like a wall, sand, a small outpost: the Sahara. They give you water and a long ride back.", 8)
				Default : IS16Tell("Wind and brown dust: the Gobi outpost. Hours later you are walked back through Command to the outbuilding.", 8)
			End Select
	End Select
End Function

Function U29Move(p%)
	PositionEntity(Collider, EntityX(p, True), EntityY(p, True) + 0.45, EntityZ(p, True))
	ResetEntity(Collider)
	DropSpeed = 0
	UpdateDoors()
	UpdateRooms()
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev29()
	Local it.Items, i%, has.Items
	;SCP-867: the seed sleeps, then grows
	If I867Seed > 0 Then
		I867Seed = I867Seed - FPSfactor
		If I867Seed <= 0 Then
			I867Seed = 0
			I867Pain = 70 * 75
			IS16Tell("Something moves under your skin, along your veins - and then the pain arrives all at once.", 7)
		EndIf
	EndIf
	If I867Pain > 0 And KillTimer >= 0 Then
		I867Pain = I867Pain - FPSfactor
		CameraShake = Max(CameraShake, 1.2)
		BlurTimer = Max(BlurTimer, 70)
		Injuries = Injuries + 0.0006 * FPSfactor
		If I867Pain < 70 * 40 And I867Pain + FPSfactor >= 70 * 40 Then IS16Tell("Thin red tendrils show under the skin of your wrists. The herbicide. The shower. Anything.", 6)
		If I867Pain <= 0 Then
			I867Pain = 0
			DeathMSG = "Subject D-9341 was found in a corridor of Heavy Containment, dead of an SCP-867 infection. A red spruce sapling had already broken through the subject's chest. Section E has one more specimen."
			Kill()
		EndIf
	EndIf
	;SCP-820-JP: the transmitter. Stay put with it and it gets taken back
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			If Inventory(i)\itemtemplate\name = "scp820jp" Then has = Inventory(i) : Exit
		EndIf
	Next
	If has <> Null And PlayerRoom <> Null Then
		If PlayerRoom <> I820Room Then
			I820Room = PlayerRoom : I820Here = 0 : I820Warned = False
		Else
			I820Here = I820Here + FPSfactor
			If I820Here > 70 * 100 And (Not I820Warned) Then
				I820Warned = True
				IS16Tell("The knife's transmitter starts to beep. It has been in one place too long.", 6)
			EndIf
			If I820Here > 70 * 160 Then
				RemoveItem(has)
				I820Taken = False : I820Here = 0 : I820Warned = False
				BlurTimer = Max(BlurTimer, 70 * 2)
				IS16Tell("Two agents in grey are suddenly beside you. One takes the knife out of your hands without a word; they are gone before you can speak.", 8)
			EndIf
		EndIf
	EndIf
	;Lunar Area-32: one-sixth gravity
	If PlayerRoom <> Null Then
		If PlayerRoom\RoomTemplate\Name = "room2b29pool" Then
			If EntityY(Collider) - EntityY(PlayerRoom\obj, True) > (U29_LUNAR_Y1 - 300) * RoomScale Then
				If DropSpeed < 0 Then DropSpeed = Max(DropSpeed + 0.005 * FPSfactor, -0.35)
			EndIf
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse29(it.Items)
	Select it\itemtemplate\name
		Case "scp820jp"
			I820Look = I820Look + 70 * 12
			If I820Look > 70 * 45 Then
				IndevStress = Min(100, IndevStress + 15)
				BlurTimer = Max(BlurTimer, 70 * 2)
				IS16Tell("You can't look away from it. Somewhere busy. Somewhere everyone would see. You put it away slowly, and your hands are shaking.", 8)
			Else
				IS16Tell("A stone knife, a snake coiled from the grip to the tip. The grip is engraved: a tourism company's mark. It is... fascinating.", 7)
			EndIf
			SelectedItem = Null
		Case "herbicide867"
			If I867Seed > 0 Or I867Pain > 0 Then
				If I867Pain > 0 Then Injuries = Injuries + 0.2
				I867Seed = 0 : I867Pain = 0
				IS16Tell("You inject the herbicide. It burns down every vein at once - and something under your skin goes still.", 7)
			Else
				IS16Tell("You inject the herbicide anyway. It burns, and nothing else happens.", 5)
			EndIf
			RemoveItem(it)
			SelectedItem = Null
	End Select
End Function
