;=====================================================================
; SCP: Containment Breach - Indev: ninth batch, four rooms, four SCPs
;
;   room2burn457   HCZ    SCP-457  down a lift: the burning man under the misting sprinklers. Every press of
;                                  FUEL past the allotment makes it bigger and cleverer; it writes on the
;                                  wall; shut the water off and it grows, splits and breaks the window seal.
;                                  The blast shield, the hose, a dead man's Level 4 card in the chamber
;   room2cold016   HCZ    SCP-016  the reference corridor a fourth time, as a BC-L5 wing: a UV lock, the cold
;                                  room with the dish, a dropped culture tray. Catch it and stay calm and you
;                                  bleed out; be frightened enough and it rebuilds you instead
;   room2read152   HCZ    SCP-152  up a lift: the reading room. The last page describes the present; every
;                                  minute or two the book is gone for one second and comes back an edition
;                                  later, with a new way you died somewhere else
;   room2dark280   Indev  SCP-280  the second reference shot: a dark hall round a block, the cell inside the
;                                  block. The lamp backs it into its corner; the floodlights put it out in
;                                  the hall with you
;
;   IndevS04Data.bb is generated (Tools\roomkit\gen_b9.py). Helpers come from IndevS08.bb / IndevS10.bb /
;   IndevS16.bb / IndevS13.bb / IndevAnnex.bb. No globals: handles in r\Objects[] / r\RoomDoors[] / r\NPC[],
;   progress in the room's event (EventState / 2 / 3, lower-case flags in EventStr, numbers as <K123>).
;=====================================================================

Function IS04Suited%()
	Return (WearingHazmat > 0)
End Function

Function IS04Masked%()
	Return (WearingHazmat > 0 Or WearingGasMask > 0)
End Function

;which part of the facility something is in, the way SCP-152 would put it
Function IS04ZoneName$(ent%)
	Local band% = GetZone(Int(Floor(EntityZ(ent, True) / 8.0 + 0.5)))
	Select band
		Case 0
			Return "Light Containment"
		Case 1
			Return "Heavy Containment"
		Case 2
			Return "the unfinished halls"
	End Select
	Return "the offices"
End Function

;a plain box in room units, centred on a pivot (made while the room is still unrotated)
Function IS04Box%(r.Rooms, at%, hx#, hy#, hz#, skin$)
	Local m% = CreateCube()
	Local tex% = LoadTexture_Strict(skin)
	EntityTexture(m, tex)
	FreeTexture(tex)
	ScaleEntity(m, hx * RoomScale, hy * RoomScale, hz * RoomScale)
	PositionEntity(m, EntityX(at, True), EntityY(at, True), EntityZ(at, True), True)
	EntityParent(m, r\obj)
	Return m
End Function

;a flat panel of light hung on a pivot: dx / dy / dz in room units from it
Function IS04Glow%(p%, w#, h#, dx#, dy#, dz#, alpha#)
	Local m% = IS10Quad(w, h, False, False)
	IS10OnPivot(m, p)
	PositionEntity(m, dx * RoomScale, dy * RoomScale, dz * RoomScale)
	EntityColor(m, 255, 246, 226)
	If alpha < 1.0 Then
		EntityBlend(m, 3)
		EntityAlpha(m, alpha)
	EndIf
	HideEntity(m)
	Return m
End Function

;the cell's lightmap is baked dark, so a light that is switched on is a volume of added light: a drum
;standing on the cell floor, drawn from both sides, that brightens whatever is seen through it
Function IS04Shell%(p%, radius#, half#, dx#, dy#, lum%)
	Local m% = CreateCylinder(16, True)
	EntityParent(m, p, False)
	ScaleEntity(m, radius * RoomScale, half * RoomScale, radius * RoomScale)
	PositionEntity(m, dx * RoomScale, dy * RoomScale, 0)
	RotateEntity(m, 0, 0, 0)
	EntityFX(m, 1 + 16)
	EntityBlend(m, 3)
	EntityColor(m, lum, lum * 0.96, lum * 0.88)
	HideEntity(m)
	Return m
End Function

Function IndevS04Dress(r.Rooms)
	Local m%, t%
	Select r\RoomTemplate\Name
		Case "room2burn457"
			m = IS16Prop(r, "GFX\npcs\scp457.b3d", "GFX\npcs\indev_flame.png", r\Objects[S04_BRN_FLAME], 250)
			EntityFX(m, 1 + 16)
			EntityBlend(m, 3)
			ScaleEntity(m, 0.35, 0.35, 0.35)
			r\Objects[S04_BRN_FLAMEM] = m
			m = IS16Prop(r, "GFX\npcs\scp457.b3d", "GFX\npcs\indev_flame.png", r\Objects[S04_BRN_CENTER], 0)
			EntityFX(m, 1 + 16)
			EntityBlend(m, 3)
			HideEntity(m)
			r\Objects[S04_BRN_FLAME2M] = m
			m = IS10Quad(320, 100, True, True)
			IS10OnPivot(m, r\Objects[S04_BRN_CHAR])
			EntityColor(m, 130, 122, 112)
			HideEntity(m)
			r\Objects[S04_BRN_CHARM] = m
			r\Objects[S04_BRN_SHUTM] = IS04Box(r, r\Objects[S04_BRN_SHUTTER], 6, 90, 178, "GFX\map\dirtymetal.jpg")

		Case "room2cold016"
			r\Objects[S04_COL_FISHM] = IS16Prop(r, "GFX\npcs\scp0161.b3d", "GFX\npcs\indev_d0161.png", r\Objects[S04_COL_FISHA], 0)

		Case "room2read152"
			m = IS16Prop(r, "GFX\npcs\scp152.b3d", "GFX\npcs\indev_book152.png", r\Objects[S04_RDR_BOOK], 0)
			EntityPickMode(m, 2)
			r\Objects[S04_RDR_BOOKM] = m

		Case "room2dark280"
			m = IS16Prop(r, "GFX\npcs\scp280.b3d", "GFX\npcs\indev_280.png", r\Objects[S04_DRK_HOME], 135)
			EntityFX(m, 1)
			r\Objects[S04_DRK_S280M] = m
			t = IS16Prop(r, "GFX\npcs\scp280e.b3d", "GFX\npcs\indev_280.png", r\Objects[S04_DRK_HOME], 135)
			EntityFX(t, 1)
			EntityParent(t, m)
			HideEntity(t)
			ScaleEntity(m, 1.0, 0.5, 1.0) ;balled up; the eyes are its child, so they follow
			r\Objects[S04_DRK_EYEM] = t
			r\Objects[S04_DRK_LAMPM] = IS04Glow(r\Objects[S04_DRK_LAMPFX], 90, 90, 0, 0, 0, 1.0)
			r\Objects[S04_DRK_POOLM] = IS04Shell(r\Objects[S04_DRK_LAMPFX], 118, 196, -40, -199, 56)
			r\Objects[S04_DRK_FLOODM] = IS04Glow(r\Objects[S04_DRK_FLOODFX], 220, 220, 0, 0, 0, 1.0)
			r\Objects[S04_DRK_FPOOLM] = IS04Shell(r\Objects[S04_DRK_FLOODFX], 262, 196, 0, -199, 120)
			;both levers are kept by the save
			r\Levers[0] = r\Objects[S04_DRK_LAMP + 1]
			r\Levers[1] = r\Objects[S04_DRK_FLOOD + 1]
	End Select
End Function

Function UpdateIndevS04(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2burn457"
			If r\dist < 10.0 Then IndevS04Spin(r, 1.0)
			UpdateS04Burn(e)
		Case "room2cold016"
			If r\dist < 10.0 Then IndevS04Spin(r, 1.0)
			UpdateS04Cold(e)
		Case "room2read152"
			If r\dist < 10.0 Then IndevS04Spin(r, 0.35) ;quiet, near the reading room
			UpdateS04Read(e)
		Case "room2dark280"
			If r\dist < 10.0 Then IndevS04Spin(r, 1.0)
			UpdateS04Dark(e)
	End Select
End Function

;=====================================================================
; room2burn457 - SCP-457
;   EventState   its size (0.35 a small flame, 1.0 a man, 1.25 it splits)     EventState2  the lift
;   EventState3  how long the sprinklers have been off; after a breach, how long the emergency mist holds
;   numbers: <F> times fed, <M> the message on the wall + 1, <B> how long it has been touching you,
;            <H> the hose (frames left), <T> the two of them fighting (frames left)
;   flags: n placed, v here this visit, d shield down, s it has split, x emergency mist, k card taken,
;          w seen at the window, c told about the heat, b it has broken the seal before
;   NPC[0] the fire technician, NPC[1] Novak
;=====================================================================

Function IS04Flicker(m%, size#, seed#)
	Local t# = IS16Time()
	ScaleEntity(m, size * (1.0 + 0.05 * Sin(t * 700 + seed)), size * (1.0 + 0.08 * Sin(t * 900 + seed * 2) + 0.05 * Sin(t * 1570 + seed)), size)
End Function

;put the charred writing back the way the event remembers it
Function IS04CharShow(e.Events)
	Local r.Rooms = e\room, m% = r\Objects[S04_BRN_CHARM], k% = IS10Num(e, "M") - 1, tex%
	If k < 0 Then
		HideEntity(m)
		Return
	EndIf
	tex = LoadTexture_Strict("GFX\map\indev_char" + k + ".png")
	EntityTexture(m, tex)
	FreeTexture(tex)
	ShowEntity(m)
End Function

Function IS04Char(e.Events, k%)
	If IS10Num(e, "M") = k + 1 Then Return
	IS10SetNum(e, "M", k + 1)
	IS04CharShow(e)
End Function

Function UpdateS04Burn(e.Events)
	Local r.Rooms = e\room
	Local fl% = r\Objects[S04_BRN_FLAMEM], fl2% = r\Objects[S04_BRN_FLAME2M], sh% = r\Objects[S04_BRN_SHUTM]
	Local lvr% = r\Objects[S04_BRN_SPRINK + 1], home% = r\Objects[S04_BRN_FLAME]
	Local lx#, ly#, lz#, down%, inch%, ingal%, wet%, fed%, size#, target#, dx#, dz#, dist#, tx#, tz#, spd#, k#
	Local hose%, fight%, touch%, n.NPCs, d#, hit%, left#, base#, sy#, atwin%, t# = IS16Time()
	Local p.Particles

	If PlayerRoom <> r Then
		IS13Drop(e, "v")
		IS08Hush(e)
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then
		IS08Hush(e)
		Return
	EndIf

	If e\EventState <= 0 Then e\EventState = 0.35
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S04_BRN_TECH, 180)
		r\NPC[1] = IS16Body(r, S04_BRN_BODY, 40, 40)
	EndIf
	If Not IAxFlag(e, "v") Then
		IAxSetFlag(e, "v")
		IS04CharShow(e)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_firesuit.jpg")
	IAxSkin(r\NPC[1], "GFX\npcs\indev_firesuit.jpg")

	IAxLocal(r)
	lx = TFormedX() : ly = TFormedY() : lz = TFormedZ()
	down = (ly < -400.0)
	inch = (down And lx > 344.0 And lz > -316.0 And lz < 316.0)
	ingal = (down And lx < 316.0)

	n = r\NPC[0]
	If n <> Null Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3) + IAxFlag(e, "b")
				Case 4
					IAxSay("Fire tech", "It asked you to shut the water off. Didn't it. It asked Novak too.", 6)
				Case 1
					IAxSay("Fire tech", "One press of FUEL a day. It gets taller with every extra one, and it gets ideas.", 6)
				Case 2
					IAxSay("Fire tech", "The mist stays on. Whatever it writes on that wall, the mist stays on.", 6)
				Case 3
					IAxSay("Fire tech", "Novak's card is still in there with him. Level 4. You'd want a suit, and you'd want it small.", 7)
			End Select
		EndIf
	EndIf

	;---- the sprinklers, the allotment, how big it is
	wet = UpdateLever(lvr)
	fed = IS10Num(e, "F")
	size = e\EventState
	If IAxFlag(e, "x") Then
		;the emergency system holds the mist on for a minute after a breach
		RotateEntity(lvr, 80, EntityYaw(lvr), 0)
		wet = True
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			IS13Drop(e, "x")
			e\EventState3 = 0
		EndIf
	ElseIf wet Then
		e\EventState3 = 0
	Else
		If e\EventState3 = 0 Then
			PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
			IS16Tell("The mist thins and stops. On the other side of the glass, the fire straightens up.", 6)
		EndIf
		e\EventState3 = e\EventState3 + FPSfactor
	EndIf
	base = 0.35 + 0.2 * fed
	target = base
	If (Not wet) Then target = Min(1.3, base + e\EventState3 / (70.0 * 22.0) * (0.6 + 0.3 * fed))
	size = CurveValue(target, size, 50.0)
	e\EventState = size

	;---- past a certain size it splits, and the two fight
	fight = IS10Num(e, "T")
	If (Not wet) And size >= 1.22 And (Not IAxFlag(e, "s")) Then
		IAxSetFlag(e, "s")
		fight = 70 * 6
		IS10SetNum(e, "T", fight)
		PositionEntity(fl2, EntityX(r\Objects[S04_BRN_CENTER]), EntityY(r\Objects[S04_BRN_CENTER]), EntityZ(r\Objects[S04_BRN_CENTER]))
		IS10Sound("SFX\Indev\scream457.wav", fl, 20.0, 1.0)
		If down Then IS16Tell("It comes apart down the middle. Two of them now, and each one wants what the other is burning.", 7)
	EndIf
	If IAxFlag(e, "s") And wet Then
		IS13Drop(e, "s")
		IS10SetNum(e, "T", 0)
		IS10Sound("SFX\Indev\scream457.wav", fl, 20.0, 1.0)
		If down Then IS16Tell("The mist comes back. The smaller one goes out like a match, and the other backs under its shelter.", 7)
	EndIf
	If IAxFlag(e, "s") Then
		ShowEntity(fl2)
		IS04Flicker(fl2, size * 0.9, 77)
		IS10Walk(fl2, EntityX(fl) + Sin(t * 300) * 90, EntityZ(fl) + Cos(t * 300) * 90, 3.0)
		fight = fight - 1
		IS10SetNum(e, "T", fight)
		If Rand(70) = 1 Then IS10Sound("SFX\Indev\scream457.wav", fl2, 20.0, 0.8)
		If fight <= 0 Then
			;one eats the other, and the flare finds the window seal
			IS13Drop(e, "s")
			HideEntity(fl2)
			IAxSetFlag(e, "x")
			e\EventState3 = 70 * 60
			IS10SetNum(e, "F", 0)
			fed = 0
			size = 0.35
			e\EventState = size
			IS04Char(e, 4)
			LightFlash = 3.0
			CameraShake = 3.0
			IS10Sound("SFX\Indev\fire.wav", r\Objects[S04_BRN_WIN], 24.0, 1.0)
			PlaySound_Strict(LoadTempSound("SFX\General\LightSwitch.ogg"))
			If IAxFlag(e, "d") Then
				If down Then
					IS16Tell("One of them eats the other and the chamber goes white. The blast shield takes all of it. Then the emergency mist cuts in.", 9)
				EndIf
			ElseIf inch Then
				DeathMSG = "Subject D-9341 was inside Containment Chamber 457 with the misting system shut off when SCP-457 reached its splitting threshold. The remains were recovered with the fuel."
				Kill()
			ElseIf ingal Then
				BlurTimer = 1500
				IndevStress = Min(100, IndevStress + 25)
				DeathMSG = "Subject D-9341 was at the observation window of Chamber 457, with the blast shield open and the misting system off, when SCP-457 breached the window seal."
				If IS04Suited() Then
					Injuries = Injuries + 0.5
					IS16Tell("A sheet of flame comes through the window seal and over you. The suit holds. Behind it the emergency mist cuts in.", 8)
				Else
					Injuries = Injuries + 1.8
					Bloodloss = Min(100, Bloodloss + 10)
					IS16Tell("A sheet of flame comes through the window seal and over you. Then the emergency mist cuts in. The shield was there for this.", 9)
				EndIf
			ElseIf down Then
				IS16Tell("Behind you the window seal lets go with a roar. The emergency mist cuts in.", 6)
			EndIf
			IAxSetFlag(e, "b")
		EndIf
	Else
		HideEntity(fl2)
	EndIf

	;---- the console: the fuel injector and the blast shield
	If IS10Press(r\Objects[S04_BRN_FUEL], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If fed >= 3 Then
			IS16Tell("The injector coughs. The fuel tank is empty.", 4)
		Else
			fed = fed + 1
			IS10SetNum(e, "F", fed)
			IS10Sound("SFX\Indev\fire.wav", r\Objects[S04_BRN_FUELP], 16.0, 0.8)
			Select fed
				Case 1
					IS04Char(e, 0)
					IS16Tell("The daily allotment. The fire swells to the size of a child, turns to the back wall and chars one word into it.", 7)
				Case 2
					IS04Char(e, 1)
					IS16Tell("A second allotment. It stands as tall as you now, and the way it looks at the glass has changed. That was tomorrow's fuel.", 8)
				Default
					IS04Char(e, 3)
					IS16Tell("A third. It is a man made of fire. It writes slowly, and neatly, and waits by the words.", 7)
			End Select
		EndIf
	EndIf
	If IS10Press(r\Objects[S04_BRN_SHIELD], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		IS10Sound("SFX\Indev\shutter.wav", r\Objects[S04_BRN_SHUTTER], 12.0, 1.0)
		If IAxFlag(e, "d") Then
			IS13Drop(e, "d")
		Else
			IAxSetFlag(e, "d")
		EndIf
	EndIf
	sy = EntityY(r\Objects[S04_BRN_SHUTTER])
	If IAxFlag(e, "d") Then sy = sy - 180.0
	PositionEntity(sh, EntityX(sh), CurveValue(sy, EntityY(sh), 10.0), EntityZ(sh))

	;---- the hose, in the chamber
	hose = IS10Num(e, "H")
	If hose > 0 Then IS10SetNum(e, "H", hose - 1)
	If IS10Press(r\Objects[S04_BRN_HOSE], 1.4) Then
		If hose > 0 Then
			IS16Tell("The hose is still running.", 3)
		Else
			hose = 70 * 5
			IS10SetNum(e, "H", hose)
			IS10Sound("SFX\Indev\hose.wav", r\Objects[S04_BRN_HOSE], 12.0, 1.0)
			IS10Sound("SFX\Indev\scream457.wav", fl, 20.0, 1.0)
			If fed > 0 Then
				fed = fed - 1
				IS10SetNum(e, "F", fed)
			EndIf
			IS04Char(e, 2)
			IS16Tell("Two megapascals of water. It screams, a kettle with a voice, and goes back to its shelter smaller than it left.", 7)
		EndIf
	EndIf

	;---- where it goes
	tx = EntityX(home) : tz = EntityZ(home)
	dx = lx - EntityX(fl) : dz = lz - EntityZ(fl)
	dist = Sqr(dx * dx + dz * dz)
	If IAxFlag(e, "s") Then
		tx = EntityX(r\Objects[S04_BRN_CENTER]) : tz = EntityZ(r\Objects[S04_BRN_CENTER])
	ElseIf hose > 0 Then
		;driven back
	ElseIf inch Then
		If fed > 0 Or (Not wet) Or dist < 330.0 Then
			tx = lx : tz = lz
		EndIf
	ElseIf ingal And (Not IAxFlag(e, "d")) And Abs(lz) < 260.0 Then
		tx = EntityX(r\Objects[S04_BRN_WIN]) : tz = EntityZ(r\Objects[S04_BRN_WIN])
		atwin = True
	ElseIf fed > 0 Then
		If Sin(t * 20) > 0 Then
			tx = EntityX(r\Objects[S04_BRN_CENTER]) : tz = EntityZ(r\Objects[S04_BRN_CENTER])
		EndIf
	EndIf
	spd = 0.9 + 1.3 * size
	If wet Then spd = spd * 0.6
	If hose > 0 Then spd = 3.2
	left = IS10Walk(fl, tx, tz, spd)
	If left < 8.0 And down Then IS10Look(r, fl)
	IS04Flicker(fl, size, 0)
	If atwin And left < 8.0 And (Not IAxFlag(e, "w")) Then
		IAxSetFlag(e, "w")
		IS16Tell("It comes up to the glass and lays a hand of flame flat against it. The glass ticks. It is looking at you the way you would look at firewood.", 9)
	EndIf

	;---- what it does to you
	touch = IS10Num(e, "B")
	If inch Then
		k = 1.0
		If IS04Suited() Then k = 0.25
		If (Not IAxFlag(e, "c")) Then
			IAxSetFlag(e, "c")
			If IS04Suited() Then
				IS16Tell("Sixty degrees and raining. Inside the suit you can still feel which side of you is facing it.", 6)
			Else
				IS16Tell("Sixty degrees and raining. Without a suit your skin tightens at once. Don't stay.", 6)
			EndIf
			If fed > 0 Then IS04Char(e, 5)
		EndIf
		Injuries = Injuries + 0.0005 * size * k * FPSfactor
		Stamina = Max(0, Stamina - 0.03 * k * FPSfactor)
		If dist < 60.0 + 150.0 * size And (Not IAxFlag(e, "s")) Then
			touch = touch + 1
			IS10SetNum(e, "B", touch)
			Injuries = Injuries + 0.012 * k * FPSfactor
			BlurTimer = Max(BlurTimer, 500)
			CameraShake = Max(CameraShake, 1.2)
			If Rand(90) = 1 Then IS10Sound("SFX\Indev\scream457.wav", fl, 20.0, 0.7)
			DeathMSG = "Subject D-9341 entered Containment Chamber 457 and was caught by SCP-457. Asked afterwards how it felt about humans, SCP-457 charred two words into the wall."
			If touch > 70 * 3 / k Then Kill()
		ElseIf touch > 0 Then
			IS10SetNum(e, "B", 0)
		EndIf
	ElseIf touch > 0 Then
		IS10SetNum(e, "B", 0)
	EndIf

	;---- Novak
	hit = False
	n = r\NPC[1]
	If n <> Null Then hit = IS16Click(n\obj, n\Collider, 1.7)
	If (Not hit) Then hit = IS10Press(r\Objects[S04_BRN_BODY], 1.7)
	If hit Then
		If IAxFlag(e, "k") Then
			IS16Tell("There is nothing else on him you could carry.", 4)
		Else
			IAxSetFlag(e, "k")
			IS16Give("key4", r\Objects[S04_BRN_BODY])
			IS16Tell("Novak, in what is left of a flame suit. The card on his lanyard has curled at one corner. Level 4. It still reads.", 7)
		EndIf
	EndIf

	;---- sound, sparks, mist
	If down Then
		If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Indev\fire.wav")
		e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, fl, 9.0, Min(1.0, 0.25 + 0.6 * size))
		If wet Then
			If e\Sound2 = 0 Then e\Sound2 = LoadSound_Strict("SFX\Indev\mist.wav")
			e\SoundCHN2 = LoopSound2(e\Sound2, e\SoundCHN2, Camera, r\Objects[S04_BRN_CENTER], 9.0, 0.7)
		ElseIf e\SoundCHN2 <> 0 Then
			If ChannelPlaying(e\SoundCHN2) Then StopChannel(e\SoundCHN2)
		EndIf
		If Rand(3) = 1 Then
			p = CreateParticle(EntityX(fl, True) + Rnd(-0.12, 0.12) * size, EntityY(fl, True) + Rnd(0.2, 0.95) * size, EntityZ(fl, True) + Rnd(-0.12, 0.12) * size, 7, 0.02 + 0.03 * size, -0.25, 45)
			p\speed = 0
			p\Achange = -0.03
		EndIf
		If wet And Rand(2) = 1 Then
			TFormPoint(Rnd(360.0, 980.0), -310.0, Rnd(-300.0, 300.0), r\obj, 0)
			p = CreateParticle(TFormedX(), TFormedY(), TFormedZ(), 6, 0.22, 0.5, 90)
			p\speed = 0
			p\A = 0.3
			EntityAlpha(p\obj, 0.3)
			p\Achange = -0.004
		EndIf
	Else
		IS08Hush(e)
	EndIf
End Function

;=====================================================================
; room2cold016 - SCP-016
;   EventState   the infection clock (frames since you caught it)     EventState2  the UV cycle (frames left)
;   flags: n placed, i infected, s it has seen you frightened, t it rebuilt you, d dormant (you bled and lived),
;          u the UV cycle has been run, k D-016-2 searched, c cold told, a tank told, w the tray seen through
;          a mask, f the swimmer is heading north, l supplies taken, p phase 2 told, q phase 3 told, o cold told
;   NPC[0] the duty researcher, NPC[1] D-016-2
;=====================================================================

Function IS04Infect(e.Events)
	If IAxFlag(e, "i") Or IAxFlag(e, "t") Or IAxFlag(e, "d") Then Return
	IAxSetFlag(e, "i")
	IS13Drop(e, "s")
	IS13Drop(e, "p")
	IS13Drop(e, "q")
	IS13Drop(e, "o")
	e\EventState = 0
End Function

;severe stress: it stops multiplying and rebuilds the host instead
Function IS04Rebuild(e.Events)
	IS13Drop(e, "i")
	IAxSetFlag(e, "t")
	Injuries = 0
	Bloodloss = 0
	StaminaEffect = 0.4
	StaminaEffectTimer = 300
	CameraShake = 3.0
	BlurTimer = 1500
	IndevStress = Max(IndevStress, 50)
	PlaySound_Strict(LoadTempSound("SFX\General\Slash1.ogg"))
	IS16Tell("Something in you decides you are in danger and starts rebuilding. Your knuckles split and knit thicker; your chest feels twice the size. The bleeding has stopped. You are very angry.", 11)
End Function

;the course of the disease, wherever you are
Function IS04Sickness(e.Events)
	Local c#
	If (Not IAxFlag(e, "i")) Or KillTimer < 0 Then Return
	e\EventState = e\EventState + FPSfactor
	c = e\EventState
	If IndevStress >= 60 Then IAxSetFlag(e, "s")

	If c < 70 * 60 Then
		;phase one: a cold
		BlinkTimer = BlinkTimer - 0.25 * FPSfactor
		If Rand(600) = 1 Then PlaySound_Strict(CoughSFX(Rand(0, 2)))
		If (Not IAxFlag(e, "o")) And c > 70 * 5 Then
			IAxSetFlag(e, "o")
			IS16Tell("Your eyes itch. Your nose is running. Your shoulders ache as if you had slept on a floor. A cold, you tell yourself.", 7)
		EndIf
	ElseIf c < 70 * 150 Then
		;phase two: bleeding into the lungs
		If Not IAxFlag(e, "p") Then
			IAxSetFlag(e, "p")
			PlaySound_Strict(CoughSFX(Rand(0, 2)))
			IS16Tell("You cough, and there is blood in it: a fine red mist every time you breathe out. It is not a cold.", 7)
		EndIf
		If Bloodloss < 70 Then Bloodloss = Max(Bloodloss, 5) + 0.006 * FPSfactor
		BlurTimer = Max(BlurTimer, 200)
		If Rand(350) = 1 Then PlaySound_Strict(CoughSFX(Rand(0, 2)))
		If IAxFlag(e, "s") And c > 70 * 75 Then IS04Rebuild(e)
	Else
		;phase three: the crash
		If IAxFlag(e, "s") Then
			IS04Rebuild(e)
			Return
		EndIf
		If Not IAxFlag(e, "q") Then
			IAxSetFlag(e, "q")
			CameraShake = 2.0
			IS16Tell("It lets go all at once. Blood from your nose, your eyes, from under your nails. You were calm. That was the mistake.", 8)
		EndIf
		DeathMSG = "Subject D-9341 died of exsanguination in the third phase of SCP-016 infection. No transformation was observed: at no point did the subject show signs of severe stress. Remains incinerated under BC-L5 conditions."
		Bloodloss = Bloodloss + 0.05 * FPSfactor
		BlurTimer = Max(BlurTimer, 600)
		If c > 70 * 162 Then
			IS13Drop(e, "i")
			IAxSetFlag(e, "d")
			IS16Tell("It stops. You are still here, grey and shaking, in more of your own blood than you thought you had. Whatever it was has gone quiet inside you.", 9)
		EndIf
	EndIf
End Function

Function UpdateS04Cold(e.Events)
	Local r.Rooms = e\room
	Local fish% = r\Objects[S04_COL_FISHM], lx#, lz#, incold%, inlock%, intank%, n.NPCs, d#, hit%, left#, tgt%, t# = IS16Time()

	IS04Sickness(e)
	If PlayerRoom <> r Then
		IS16Hush(e)
		Return
	EndIf
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S04_COL_DOC, 200)
		r\NPC[1] = IS16Body(r, S04_COL_BODY2, 60, 40)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_mopp.jpg")
	n = r\NPC[0]
	If n <> Null Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			If IAxFlag(e, "i") Then
				IAxSay("Duty officer", "You've got it. I can hear it in your chest. Don't sit down, don't calm down. It needs a reason to change you. Go and find one.", 9)
			Else
				Select Rand(3)
					Case 1
						IAxSay("Duty officer", "Run the UV before you go in. Six hours it lives on a hard surface, and somebody dropped a tray.", 7)
					Case 2
						IAxSay("Duty officer", "Same room, same water, three men. One grew gills. One grew fists. One grew a gas torch. It listens to what you're afraid of.", 9)
					Case 3
						IAxSay("Duty officer", "The calm ones die. Write that on your hand.", 5)
				End Select
			EndIf
		EndIf
	EndIf

	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()
	incold = (lx > 288.0 And lx < 736.0 And lz > -200.0 And lz < 200.0)
	inlock = (lx > 288.0 And lx < 736.0 And lz < -260.0)
	intank = (lx < -288.0 And lz > 260.0)

	;---- the UV cycle
	If IS10Press(r\Objects[S04_COL_UVBTN], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If e\EventState2 > 0 Then
			IS16Tell("The cycle is running.", 3)
		Else
			e\EventState2 = 70 * 8
			IS16Tell("UV CYCLE: 8 SECONDS. The tubes in the lock and the cold room come up to full.", 6)
		EndIf
	EndIf
	If e\EventState2 > 0 Then
		e\EventState2 = e\EventState2 - FPSfactor
		If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Indev\uvhum.wav")
		e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, r\Objects[S04_COL_UVBTN], 9.0, 1.0)
		If (inlock Or incold) And (Not IS04Suited()) Then
			BlinkTimer = BlinkTimer - 0.6 * FPSfactor
			BlurTimer = Max(BlurTimer, 250)
		EndIf
		If e\EventState2 <= 0 Then
			e\EventState2 = 0
			IS16Hush(e)
			IAxSetFlag(e, "u")
			IS16Tell("The cycle ends. Whatever was alive on the floors and walls of the lock and the cold room is not any more.", 7)
		EndIf
	EndIf

	;---- the cold room: the cold, the dropped tray, the dish, the supplies
	If incold Then
		Stamina = Max(0, Stamina - 0.03 * FPSfactor)
		If Not IAxFlag(e, "c") Then
			IAxSetFlag(e, "c")
			IS16Tell("Below freezing. In the cube on the plinth, a petri dish, and something rust-coloured that is not rust.", 6)
		EndIf
		If (Not IAxFlag(e, "u")) And EntityDistance(Collider, r\Objects[S04_COL_TRAY]) < 1.5 Then
			If IS04Masked() Then
				If Not IAxFlag(e, "w") Then
					IAxSetFlag(e, "w")
					IS16Tell("A culture tray lies smashed on the floor, its contents frozen where they ran. You are breathing filtered air. It cannot reach you.", 7)
				EndIf
			ElseIf Not (IAxFlag(e, "i") Or IAxFlag(e, "t") Or IAxFlag(e, "d")) Then
				IS04Infect(e)
				IS16Tell("Something crunches under your shoe: a dropped culture tray. You have breathed in before you think not to.", 7)
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[S04_COL_DISH], 1.4) Then IS16Tell("SCP-016, in its dish, in its cube. The sample port is sealed with a wire and a lead tag. You leave the wire alone.", 6)
	If IS10Press(r\Objects[S04_COL_SUPPLY], 1.4) Then
		If IAxFlag(e, "l") Then
			IS16Tell("The cabinet is empty.", 3)
		Else
			IAxSetFlag(e, "l")
			IS16Give("finefirstaid", r\Objects[S04_COL_SUPPLY])
			IS16Give("18vbat", r\Objects[S04_COL_SUPPLY])
			IS16Tell("BC-L5 field supplies, kept cold: a trauma kit, and a battery that has lost nothing in here.", 6)
		EndIf
	EndIf

	;---- D-016-2
	hit = False
	n = r\NPC[1]
	If n <> Null Then hit = IS16Click(n\obj, n\Collider, 1.7)
	If (Not hit) Then hit = IS10Press(r\Objects[S04_COL_BODY2], 1.7)
	If hit Then
		If IAxFlag(e, "k") Then
			IS16Tell("Knuckles like walnuts under split skin. He got the door to bend. Not far enough.", 5)
		Else
			IAxSetFlag(e, "k")
			IS16Give("key3", r\Objects[S04_COL_BODY2])
			If IS04Suited() Or IAxFlag(e, "t") Or IAxFlag(e, "d") Or IAxFlag(e, "i") Then
				IS16Tell("D-016-2. His hands are twice the size of yours and still raw. Somebody's Level 3 card is in his pocket.", 6)
			Else
				IS04Infect(e)
				IS16Tell("D-016-2. Somebody's Level 3 card is in his pocket. His hands are still raw, and now what was on them is on yours.", 7)
			EndIf
		EndIf
	EndIf

	;---- D-016-1
	tgt = r\Objects[S04_COL_FISHA]
	If IAxFlag(e, "f") Then tgt = r\Objects[S04_COL_FISHB]
	If intank Then
		IS10Look(r, fish)
		If Rand(220) = 1 Then IS10Sound("SFX\Indev\clicks.wav", fish, 8.0, 1.0)
		If Not IAxFlag(e, "a") Then
			IAxSetFlag(e, "a")
			IS10Sound("SFX\Indev\clicks.wav", fish, 8.0, 1.0)
			IS16Tell("It was a man. It has fins where the arms were and skin where the eyes were. It turns to face you exactly, and clicks.", 8)
		EndIf
	Else
		left = IS10Walk(fish, EntityX(tgt), EntityZ(tgt), 0.7)
		If left < 60.0 Then ;it turns before its head reaches the tank wall
			If IAxFlag(e, "f") Then
				IS13Drop(e, "f")
			Else
				IAxSetFlag(e, "f")
			EndIf
		EndIf
	EndIf
	PositionEntity(fish, EntityX(fish), EntityY(r\Objects[S04_COL_FISHA]) + Sin(t * 40) * 14, EntityZ(fish))
	If IS10Press(r\Objects[S04_COL_DRAIN], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If IS08HasKey(4) Then
			IS16Tell("The panel takes your card and asks you to confirm DRAIN. Behind the glass it has stopped swimming. You take the card back out.", 7)
		Else
			IS16Tell("TANK DRAIN: LEVEL 4 AUTHORISATION. That is how the last experiment was ended.", 5)
		EndIf
	EndIf
End Function

;=====================================================================
; room2read152 - SCP-152
;   EventState   the book is away (frames left of its one second)     EventState2  the lift
;   EventState3  time until the next edition
;   numbers: <U> editions since you came, <P> the page it is open at (0 = the last page)
;   flags: n placed, c copy taken, h the new edition has an entry you have not read
;   count q: times the guard has had to tell you.  NPC[0] the archivist, NPC[1] the guard
;=====================================================================

;the last page describes the present, accurately
Function IS04Present(e.Events)
	Local s$ = "The last page. Today, this Site, in words you might have used yourself. "
	If Curr173 <> Null Then s = s + "The sculpture is in " + IS04ZoneName(Curr173\Collider) + ". "
	If Curr106 <> Null Then
		If Curr106\State <= 0 Then
			s = s + "The old man is walking. "
		Else
			s = s + "The old man is waiting in the walls. "
		EndIf
	EndIf
	If Indev079Timer > 0 Then s = s + "The Old Machine acts again within " + Int(Indev079Timer / 4200.0 + 1) + " min. "
	s = s + "A man in orange is reading this."
	IS16Tell(s, 11)
End Function

;each new edition ends differently: in it, you died somewhere else
Function IS04Edition(e.Events)
	Local s$ = "The new entry. In this edition the man in orange "
	Select (IS10Num(e, "U") - 1) Mod 6
		Case 0
			s = s + "turned the floodlights on over the dark cell, and what was in the cell came out to stand beside him."
		Case 1
			s = s + "shut off the water because the fire wrote that it would sleep. It did not sleep."
		Case 2
			s = s + "ate the bright sweets from the cold store. It gives the time to the second: three minutes."
		Case 3
			s = s + "caught the miner's sickness, kept calm, and bled out in a corridor. The frightened ones lived, it notes."
		Case 4
			s = s + "was still looking at the core when the siren stopped."
		Default
			s = s + "took a second drink from the bottle Santa gave him."
	End Select
	IS16Tell(s, 10)
End Function

Function UpdateS04Read(e.Events)
	Local r.Rooms = e\room
	Local book% = r\Objects[S04_RDR_BOOKM], n.NPCs, d#, ly#, upst%, pg%

	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S04_RDR_ARCH, 90)
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[S04_RDR_GUARD], True), EntityY(r\Objects[S04_RDR_GUARD], True) + 0.35, EntityZ(r\Objects[S04_RDR_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
		r\NPC[1] = n
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_archivist.jpg")
	IAxLocal(r)
	ly = TFormedY()
	upst = (ly > 600.0)

	n = r\NPC[0]
	If n <> Null Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Archivist", "Every time it changes we scan the lot. Jansen says it doesn't change. He says somebody sends us a new one.", 8)
				Case 2
					IAxSay("Archivist", "Half the last fifty pages are us getting it wrong. It gives you a little perspective.", 6)
				Case 3
					IAxSay("Archivist", "It reads to me in my grandmother's dialect. I've stopped mentioning it.", 6)
			End Select
		EndIf
	EndIf
	n = r\NPC[1]
	If n <> Null And upst Then
		d = EntityDistance(n\Collider, Collider)
		If PlayerSoundVolume > 3.4 And MsgTimer <= 0 Then
			e\EventStr = e\EventStr + "q"
			Select IS13Count(e, "q")
				Case 1
					IAxSay("Guard", "Quiet. Walk.", 4)
				Case 2
					IAxSay("Guard", "I said walk. It's a reading room.", 4)
				Default
					IAxSay("Guard", "Next time I put you back in the lift myself.", 5)
			End Select
		ElseIf d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Guard", "Level 2 and up. Leave it open at the last page when you're done.", 6)
				Case 2
					IAxSay("Guard", "It goes for one second. Exactly one. I've stopped looking.", 5)
				Case 3
					IAxSay("Guard", "Don't run up here.", 3)
			End Select
		EndIf
	EndIf

	;---- the book is replaced, now and then, while you are up here
	If e\EventState > 0 Then
		HideEntity(book)
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 0
			ShowEntity(book)
			IS10SetNum(e, "U", IS10Num(e, "U") + 1)
			IS10SetNum(e, "P", 0)
			IAxSetFlag(e, "h")
			IS10Sound("SFX\Indev\page.wav", r\Objects[S04_RDR_BOOK], 9.0, 1.0)
			If upst Then IS16Tell("Exactly one second. The book is back on the scale, a leaf thicker, open at a last page that was not there before.", 8)
		EndIf
	ElseIf upst Then
		If e\EventState3 <= 0 Then e\EventState3 = 70 * Rnd(50, 90)
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 And IS10Num(e, "U") < 6 Then
			e\EventState = 70
			e\EventState3 = 70 * Rnd(70, 120)
			HideEntity(book)
			LightBlink = 0.5
			IS10Sound("SFX\Indev\poof.wav", r\Objects[S04_RDR_BOOK], 9.0, 0.9)
			IS10Sound("SFX\Indev\beep.wav", r\Objects[S04_RDR_BOOK], 12.0, 1.0)
			IS16Tell("The scale alarm goes. The desk is empty.", 3)
		EndIf
	EndIf

	;---- reading it
	pg = IS10Num(e, "P")
	If e\EventState <= 0 Then
		If IS16Click(book, book, 1.6) Then
			IS10Sound("SFX\Indev\page.wav", r\Objects[S04_RDR_BOOK], 9.0, 1.0)
			Select pg
				Case 0
					If IAxFlag(e, "h") Then
						IS13Drop(e, "h")
						IS04Edition(e)
					Else
						IS04Present(e)
						pg = 1
					EndIf
				Case 1
					IS16Tell("You turn back to the first entry. 6000 BC: the sun fails, no cause given. It follows the last family round a fire for eleven days.", 8)
					pg = 2
				Case 2
					IS16Tell("1983. A duty officer believes a satellite warning. In your world he did not. The entry ends with a submarine crew, eight months on.", 8)
					pg = 3
				Case 3
					IS16Tell("A mining camp, a man with a cut hand. Nobody collapsed the shaft. The entry runs two days past the hour the device should have gone off.", 8)
					pg = 4
				Default
					IS16Tell("2007. A wildfire that wanted things, and people who fed it because it asked. The last line is one word, and for once it is not in your language.", 8)
					pg = 0
			End Select
			IS10SetNum(e, "P", pg)
		EndIf
		;he turns it back for you
		If pg <> 0 And EntityDistance(Collider, r\Objects[S04_RDR_BOOK]) > 3.2 Then
			IS10SetNum(e, "P", 0)
			If upst Then IAxSay("Guard", "Last page. Every time.", 4)
		EndIf
	EndIf

	;---- the copier
	If IS10Press(r\Objects[S04_RDR_PRINTER], 1.4) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If IAxFlag(e, "c") Then
			IS16Tell("It copies the last page again. Ink will not hold on the original; it holds on the copy. You already have one.", 6)
		Else
			IAxSetFlag(e, "c")
			IS10Sound("SFX\Indev\teletype.wav", r\Objects[S04_RDR_PRINTER], 9.0, 1.0)
			IS16Give("doc152b", r\Objects[S04_RDR_PRINTER])
			IS16Tell("The copier pulls the last page under its lamp and hands you what it saw. One phrase has come out as marks, not words.", 7)
		EndIf
	EndIf
End Function

;=====================================================================
; room2dark280 - SCP-280
;   EventState   0 balled up in its corner, 1 hunting in the cell, 2 backed off by the lamp, 3 out in the hall
;   EventState2  how long it has had its hands on you
;   EventState3  the floods striking (in the cell) / how long the floods have been off (in the hall)
;   flags: n placed, v here this visit, k Reyes searched, w told at the door, u walked close to it,
;          h told it is hunting, o it has been out in the hall
;   NPC[0] the night technician, NPC[1] Reyes
;=====================================================================

Function IS04Home280(e.Events)
	Local r.Rooms = e\room, m% = r\Objects[S04_DRK_S280M]
	PositionEntity(m, EntityX(r\Objects[S04_DRK_HOME]), 0, EntityZ(r\Objects[S04_DRK_HOME]))
	RotateEntity(m, 0, 135, 0)
	e\EventState = 0
	e\EventState2 = 0
	e\EventState3 = 0
End Function

Function IS04InCell%(x#, z#)
	Return (Abs(x) < 270.0 And Abs(z) < 270.0 And Abs(x) + Abs(z) < 430.0)
End Function

Function UpdateS04Dark(e.Events)
	Local r.Rooms = e\room
	Local m% = r\Objects[S04_DRK_S280M], eyes% = r\Objects[S04_DRK_EYEM]
	Local lamp%, flood%, lx#, lz#, incell%, mx#, mz#, mincell%, dx#, dz#, dist#, target#, tx#, tz#, l#
	Local n.NPCs, d#, i%, best%, bd#, hit%, st%, grab%, showeyes%, moving%

	If PlayerRoom <> r Then
		If IAxFlag(e, "v") Then
			IS13Drop(e, "v")
			IS13Drop(e, "h")
			IS04Home280(e)
			IS16Hush(e)
			SecondaryLightOn = 1.0
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf
	IAxSetFlag(e, "v")

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S04_DRK_TECH, 270)
		r\NPC[1] = IS16Body(r, S04_DRK_BODY, 30, 40)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_tech.jpg")
	IAxSkin(r\NPC[1], "GFX\npcs\indev_tech.jpg")
	n = r\NPC[0]
	If n <> Null Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Night tech", "Lamp, not floods. The lamp backs it into the corner. The floods put it out here with us.", 7)
				Case 2
					IAxSay("Night tech", "It's black on black. If you think you see a coat on the floor in there, it isn't a coat.", 6)
				Case 3
					IAxSay("Night tech", "Reyes went in for his goggles. Don't go in for Reyes.", 5)
			End Select
		EndIf
	EndIf

	;---- the two levers, and what you can see
	lamp = UpdateLever(r\Objects[S04_DRK_LAMP + 1])
	flood = UpdateLever(r\Objects[S04_DRK_FLOOD + 1])
	If lamp Then
		ShowEntity(r\Objects[S04_DRK_LAMPM])
		ShowEntity(r\Objects[S04_DRK_POOLM])
	Else
		HideEntity(r\Objects[S04_DRK_LAMPM])
		HideEntity(r\Objects[S04_DRK_POOLM])
	EndIf
	If flood Then
		ShowEntity(r\Objects[S04_DRK_FLOODM])
		ShowEntity(r\Objects[S04_DRK_FPOOLM])
	Else
		HideEntity(r\Objects[S04_DRK_FLOODM])
		HideEntity(r\Objects[S04_DRK_FPOOLM])
	EndIf

	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()
	incell = IS04InCell(lx, lz)
	If incell Then
		target = 0.05
		If lamp Then target = 0.5
		If flood Then target = 1.0
		SecondaryLightOn = CurveValue(target, SecondaryLightOn, 10.0)
	ElseIf SecondaryLightOn < 0.995 Then
		SecondaryLightOn = CurveValue(1.0, SecondaryLightOn, 15.0)
	EndIf
	If (Not IAxFlag(e, "w")) And (Not incell) And EntityDistance(Collider, r\Objects[S04_DRK_CELLC]) < 2.4 Then
		IAxSetFlag(e, "w")
		IS16Tell("DARK CELL 280. The block is cold to stand next to. Nothing inside it makes a sound.", 6)
	EndIf

	mx = EntityX(m) : mz = EntityZ(m)
	mincell = IS04InCell(mx, mz)
	dx = lx - mx : dz = lz - mz
	dist = Sqr(dx * dx + dz * dz)
	st = Int(e\EventState)
	tx = mx : tz = mz

	;---- fully lit, it is gone, and it is somewhere else
	If flood And st <> 3 Then
		e\EventState3 = e\EventState3 + FPSfactor
		showeyes = True
		If e\EventState3 > 70 * 1.5 Then
			best = 0 : bd = -1.0
			For i = 0 To 3
				d = EntityDistance(Collider, r\Objects[S04_DRK_TP0 + i])
				If d > bd Then
					bd = d
					best = i
				EndIf
			Next
			IS10Sound("SFX\Indev\poof.wav", m, 10.0, 1.0)
			PositionEntity(m, EntityX(r\Objects[S04_DRK_TP0 + best]), 0, EntityZ(r\Objects[S04_DRK_TP0 + best]))
			IS10Sound("SFX\Indev\poof.wav", m, 10.0, 1.0)
			st = 3
			e\EventState3 = 0
			e\EventState2 = 0
			IAxSetFlag(e, "o")
			IndevStress = Min(100, IndevStress + 15)
			If incell Then LightFlash = 0.8
			IS16Tell("The floods strike white. The shape in the cell is gone before the tubes have finished coming on. Out in the hall, where it is dim, something has two white eyes.", 10)
		EndIf
	ElseIf st <> 3 Then
		e\EventState3 = 0
	EndIf

	Select st
		Case 0
			;balled up against the wall until somebody comes in
			ScaleEntity(m, 1.0, 0.5, 1.0)
			If lamp Then
				st = 2
			ElseIf incell And (Not flood) Then
				st = 1
			EndIf
		Case 1
			;hands out, gliding at you; it stays in the dark of the cell
			ScaleEntity(m, 1.0, 1.0, 1.0)
			If Not IAxFlag(e, "h") Then
				IAxSetFlag(e, "h")
				IndevStress = Min(100, IndevStress + 10)
				If WearingNightVision > 0 Then
					IS16Tell("In the goggles: something in the corner unfolds, tall, no legs, both arms held out towards you. It makes no sound at all.", 8)
				Else
					IS16Tell("You can see nothing. Something in here with you has started to move. It makes no sound at all.", 7)
				EndIf
			EndIf
			If lamp Then
				st = 2
			Else
				tx = Max(-235.0, Min(235.0, lx)) : tz = Max(-235.0, Min(235.0, lz))
				l = Abs(tx) + Abs(tz)
				If l > 380.0 Then
					tx = tx * 380.0 / l : tz = tz * 380.0 / l
				EndIf
				moving = True
			EndIf
		Case 2
			;the lamp: it backs into its corner and shows its eyes
			ScaleEntity(m, 1.0, 1.0, 1.0)
			showeyes = True
			tx = EntityX(r\Objects[S04_DRK_HOME]) : tz = EntityZ(r\Objects[S04_DRK_HOME])
			If Not lamp Then
				st = 0
				If incell Then st = 1
			EndIf
			If dist < 256.0 * 1.3 Then
				IndevStress = Min(100, IndevStress + 0.05 * FPSfactor)
				If Not IAxFlag(e, "u") Then
					IAxSetFlag(e, "u")
					IS16Tell("Two white eyes that do not see, turned on you. One metre, the procedures say. You are inside it.", 7)
				EndIf
			EndIf
		Case 3
			;out in the hall
			ScaleEntity(m, 1.0, 1.0, 1.0)
			If flood And incell Then
				;you are standing in the one fully lit place in the room: it backs off, eyes on you
				showeyes = True
				best = 0 : bd = -1.0
				For i = 0 To 3
					d = EntityDistance(Collider, r\Objects[S04_DRK_TP0 + i])
					If d > bd Then
						bd = d
						best = i
					EndIf
				Next
				IS10Walk(m, EntityX(r\Objects[S04_DRK_TP0 + best]), EntityZ(r\Objects[S04_DRK_TP0 + best]), 0.8)
			Else
				tx = lx : tz = lz
				moving = True
			EndIf
			If Not flood Then
				e\EventState3 = e\EventState3 + FPSfactor
				If e\EventState3 > 70 * 8 And dist > 256.0 * 1.2 Then
					IS10Sound("SFX\Indev\poof.wav", m, 10.0, 1.0)
					IS04Home280(e)
					st = 0
					IS16Tell("With the floods off the cell is dark again. Between one blink and the next, the hall is empty.", 7)
				EndIf
			Else
				e\EventState3 = 0
			EndIf
	End Select
	e\EventState = st

	If st = 2 Then
		IS10Walk(m, tx, tz, 0.8)
		IS10Look(r, m)
	ElseIf moving Then
		If dist > 256.0 * 0.45 Then
			If st = 3 Then
				IS10Walk(m, tx, tz, 1.7)
			Else
				IS10Walk(m, tx, tz, 1.4)
			EndIf
		EndIf
		IS10Look(r, m)
	ElseIf st = 3 Then
		IS10Look(r, m)
	EndIf
	If showeyes Then
		ShowEntity(eyes)
	Else
		HideEntity(eyes)
	EndIf

	;---- its hands
	grab = False
	If dist < 256.0 * 0.6 Then
		If st = 1 Or st = 2 Then grab = True
		If st = 3 And (Not (flood And incell)) Then grab = True
	EndIf
	If grab Then
		EntityAlpha(m, 1.0)
		e\EventState2 = e\EventState2 + FPSfactor
		Injuries = Injuries + 0.008 * FPSfactor
		CameraShake = Max(CameraShake, 1.5)
		BlurTimer = Max(BlurTimer, 300)
		If Rand(40) = 1 Then PlaySound_Strict(LoadTempSound("SFX\General\Slash" + Rand(1, 2) + ".ogg"))
		DeathMSG = "Subject D-9341 was recovered from Dark Cell 280. The cell lighting log shows the inspection lamp was off. SCP-280 was found balled against the north-west wall and did not respond to the recovery team's lights."
		If st = 3 Then DeathMSG = "Subject D-9341 was recovered from the hall outside Dark Cell 280. The cell lighting log shows the floodlights had been switched on four minutes earlier. SCP-280 was later found in its cell."
		If e\EventState2 > 70 * 4 Then Kill()
	Else
		If st = 0 Then
			EntityAlpha(m, 0.85)
		Else
			EntityAlpha(m, 0.6)
		EndIf
		e\EventState2 = Max(0, e\EventState2 - FPSfactor * 0.5)
	EndIf

	If st = 1 Or st = 3 Then
		If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Indev\drone280.wav")
		e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, m, 7.0, 1.0)
	Else
		IS16Hush(e)
	EndIf

	;---- Reyes
	hit = False
	n = r\NPC[1]
	If n <> Null Then hit = IS16Click(n\obj, n\Collider, 1.7)
	If (Not hit) Then hit = IS10Press(r\Objects[S04_DRK_BODY], 1.7)
	If hit Then
		If IAxFlag(e, "k") Then
			IS16Tell("You have what he came in for. Leave him.", 4)
		Else
			IAxSetFlag(e, "k")
			IS16Give("nvgoggles", r\Objects[S04_DRK_BODY])
			IS16Give("bat", r\Objects[S04_DRK_BODY])
			IS16Tell("Reyes, what is left of him, pulled apart a piece at a time. His goggles are still strapped round his head. You take them.", 7)
		EndIf
	EndIf
End Function
