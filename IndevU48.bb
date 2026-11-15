;=====================================================================
; SCP: Containment Breach - Indev batch 48: SCP-806, the resurrection projector (room2scp806, the screening room;
; room by Tools\roomkit\rooms_b48.py, slot table in the generated IndevU48Data.bb).
;
; SCP-806 (summary of scp-wiki.wikidot.com/scp-806 in our own words, CC BY-SA 3.0): an old film projector, rebuilt
; with a lens of shaved gemstone layers, an LED array and alloy gearing. Run 13-27 hours of footage of a dead person
; onto a silver screen and needle-thin rays from the lens build a colourless copy of them (SCP-806-1) before the
; screen. Someone must watch the whole time or the forming slowly undoes itself; shut it down and the copy fails -
; blood and graphite, or an unfinished body. Only real, dead people: not the living, not cartoons, and with several
; people on film the one with the most screen time. Copies remember their lives and die of cardiac arrest 70-75
; hours later - all but SCP-806-1-a, who formed from a 5.8 second loop and remembers nothing, not even her name.
;
; Here (the screening room projector is geared to run a full set of reels in minutes):
;   - take a reel from Containment Locker 8, click the projector to load it, click again to run it
;   - while it runs, keep the screen in view: forming advances while you watch and slides back while you don't
;   - click the projector while it runs to shut it down: what was forming fails
;   - a finished copy is grey all over, talks as the person it was, and dies of cardiac arrest about seven minutes
;     later (one game minute for each ten hours); 806-1-a does not
;
; Event "u48room": EventState = phase (0 empty, 1 loaded, 2 running, 3 a copy is alive), EventState2 = forming
; 0..100, EventState3 = the reel (1 D, 2 SEC, 3 TOON, 4 LIVE, 5 the 5.8 s loop), EventStr = the copy's frames left.
;=====================================================================

Global I806Tex%[8]         ;0..5 film frames, 6 the silver screen, 7 the grey skin
Global I806Beam%            ;beam texture
Global I806Lines%[6]        ;the needle rays (world entities, positioned every frame)
Global I806Talk%, I806Gift%, I806Frame#, I806Warn#, I806Hint%

Const U48_SCRQUAD% = 3, U48_PROJ% = 4, U48_REEL1% = 5 ;U48_S06_SLOTS = 3 (IndevU48Data.bb)
Const U48_REEL2% = 6, U48_CONE% = 7, U48_LENS% = 8
Const U48_SCREENLIGHT% = 9

Function Indev48Reset(newGame%)
	I806Talk = 0 : I806Gift = 0 : I806Frame = 0 : I806Warn = 0 : I806Hint = 0
	Local i%
	For i = 0 To 5
		I806Lines[i] = 0 ;freed with the world
	Next
End Function

Function I806LoadTex()
	If I806Tex[6] <> 0 Then Return
	Local i%
	For i = 0 To 5
		I806Tex[i] = LoadTexture_Strict("GFX\map\indev_806f" + i + ".png", 1)
	Next
	I806Tex[6] = LoadTexture_Strict("GFX\map\indev_806screen.png", 1)
	I806Tex[7] = LoadTexture_Strict("GFX\map\indev_806grey.png", 1)
	I806Beam = LoadTexture_Strict("GFX\map\indev_806beam.png", 1)
End Function

;one part of the projector: a box (kind 0) or a cylinder along x (kind 1) / along z (kind 2), in room units
Function I806Part%(parent%, kind%, sx#, sy#, sz#, x#, y#, z#, tex$, r%=255, g%=255, b%=255)
	Local m%
	Select kind
		Case 0
			m = CreateCube()
		Case 1
			m = CreateCylinder(20)
			RotateMesh(m, 0, 0, 90)
		Default
			m = CreateCylinder(28)
			RotateMesh(m, 90, 0, 0)
	End Select
	ScaleMesh(m, sx, sy, sz)
	If tex <> "" Then
		Local t% = LoadTexture_Strict(tex, 1)
		EntityTexture(m, t)
		FreeTexture(t)
	EndIf
	EntityColor(m, r * 0.8, g * 0.8, b * 0.8)
	EntityFX(m, 1) ;the room's baked light doesn't reach code-made props
	EntityParent(m, parent, False)
	PositionEntity(m, x, y, z)
	Return m
End Function

;the projector after the reference photo: a gunmetal body with chrome plates, the lens barrel with its gemstone
;face, the lamp house behind, two reel arms with big reels, knobs down the side, a crank. Built in room units,
;facing +x (the screen). Returns the root; r\Objects[] gets the two reels and the lens point.
Function I806BuildProjector%(r.Rooms, p%)
	Local root% = CreatePivot()
	EntityParent(root, p, False)
	ScaleEntity(root, RoomScale * 1.6, RoomScale * 1.6, RoomScale * 1.6)
	Local met$ = "GFX\map\indev_806metal.png", chr$ = "GFX\map\indev_806chrome.png"
	I806Part(root, 0, 34, 26, 20, 0, 26, 0, met)                                   ;the body
	I806Part(root, 0, 30, 20, 1, 0, 28, 20.5, chr)                                ;side plate
	I806Part(root, 0, 30, 20, 1, 0, 28, -20.5, chr)
	I806Part(root, 0, 16, 18, 16, -40, 30, 0, met)                                ;the lamp house
	I806Part(root, 0, 6, 4, 14, -40, 50, 0, chr)                                  ;its vent cap
	I806Part(root, 1, 9, 14, 9, 44, 30, 0, met)                                   ;the lens barrel
	I806Part(root, 1, 11, 2.5, 11, 58, 30, 0, chr)                                ;the bezel
	Local face% = I806Part(root, 1, 9.5, 0.6, 9.5, 61, 30, 0, "GFX\map\indev_806lens.png")
	EntityFX(face, 1)
	EntityShininess(face, 1.0)
	Local k%
	For k = 0 To 3                                                                ;knobs down the side
		I806Part(root, 2, 3, 3, 2, -18 + k * 12, 14 + (k Mod 2) * 22, 22, chr)
	Next
	I806Part(root, 0, 2, 12, 2, -10, 6, 24, chr)                                  ;the crank
	I806Part(root, 0, 6, 2, 2, -10, -4, 26, chr)
	;the reel arms and the reels (feed at the front, take-up at the back), discs along z
	I806Part(root, 0, 2, 26, 3, 14, 70, 0, chr)
	I806Part(root, 0, 2, 26, 3, -22, 70, 0, chr)
	Local rt% = LoadTexture_Strict("GFX\items\filmreel.png", 1 + 4)
	Local reel1% = CreateCylinder(32)
	RotateMesh(reel1, 90, 0, 0)
	ScaleMesh(reel1, 30, 30, 3)
	EntityTexture(reel1, rt)
	EntityFX(reel1, 1)
	EntityColor(reel1, 210, 210, 210)
	EntityParent(reel1, root, False)
	PositionEntity(reel1, 18, 100, 0)
	Local reel2% = CopyEntity(reel1, root)
	PositionEntity(reel2, -26, 100, 0)
	FreeTexture(rt)
	r\Objects[U48_REEL1] = reel1
	r\Objects[U48_REEL2] = reel2
	;the lens point - the rays start here
	Local lp% = CreatePivot(root)
	PositionEntity(lp, 62, 30, 0)
	r\Objects[U48_LENS] = lp
	Return root
End Function

Function IndevU48Dress(r.Rooms)
	If r\RoomTemplate\Name <> "room2scp806" Then Return
	I806LoadTex()
	;the silver screen
	Local q% = IS10Quad(1240, 470, True, True)
	IS10OnPivot(q, r\Objects[U48_S06_SCREEN])
	EntityTexture(q, I806Tex[6])
	EntityFX(q, 1 + 16)
	r\Objects[U48_SCRQUAD] = q
	;the projector on its stand
	r\Objects[U48_PROJ] = I806BuildProjector(r, r\Objects[U48_S06_PROJ])
	;the beam: a cone of light from the lens to the screen, hidden until it runs
	Local c% = CreateCone(16, False)
	RotateMesh(c, 0, 0, 90)
	PositionMesh(c, 1, 0, 0)
	ScaleMesh(c, (978 - (-640 + 99)) / 2.0, 235, 620)
	EntityTexture(c, I806Beam)
	EntityBlend(c, 3)
	EntityFX(c, 1 + 16)
	EntityAlpha(c, 0.12)
	Local cp% = CreatePivot(r\Objects[U48_S06_PROJ])
	ScaleEntity(cp, RoomScale, RoomScale, RoomScale)
	EntityParent(c, cp, False)
	PositionEntity(c, 99, 48, 0) ;the lens (62, 30) on the 1.6x projector
	HideEntity(c)
	r\Objects[U48_CONE] = c
	;the light off the screen
	r\Objects[U48_SCREENLIGHT] = CreateLight(2, r\Objects[U48_S06_SCREEN])
	LightRange(r\Objects[U48_SCREENLIGHT], 6)
	LightColor(r\Objects[U48_SCREENLIGHT], 0, 0, 0)
	TranslateEntity(r\Objects[U48_SCREENLIGHT], -0.6, 0, 0, True)
End Function

;the needle rays: made the first time they are needed, positioned in world space every frame
Function I806Needles(show%, r.Rooms, n.NPCs, amount#)
	Local i%, l%, lx#, ly#, lz#, tx#, ty#, tz#, d#
	For i = 0 To 5
		If I806Lines[i] = 0 Then
			l = CreateCube()
			PositionMesh(l, 0, 0, 1)
			EntityTexture(l, I806Beam)
			EntityBlend(l, 3)
			EntityFX(l, 1 + 16)
			EntityColor(l, 235, 235, 255)
			HideEntity(l)
			I806Lines[i] = l
		EndIf
		l = I806Lines[i]
		If show And n <> Null And i < 2 + Int(amount * 4) Then
			ShowEntity(l)
			lx = EntityX(r\Objects[U48_LENS], True) : ly = EntityY(r\Objects[U48_LENS], True) : lz = EntityZ(r\Objects[U48_LENS], True)
			tx = EntityX(n\Collider, True) + Rnd(-0.15, 0.15)
			ty = EntityY(n\Collider, True) + Rnd(-0.25, 0.45)
			tz = EntityZ(n\Collider, True) + Rnd(-0.15, 0.15)
			PositionEntity(l, lx, ly, lz, True)
			PointEntity(l, n\Collider)
			RotateEntity(l, VectorPitch(tx - lx, ty - ly, tz - lz), VectorYaw(tx - lx, ty - ly, tz - lz), 0, True)
			d = Sqr((tx - lx) * (tx - lx) + (ty - ly) * (ty - ly) + (tz - lz) * (tz - lz))
			ScaleEntity(l, 0.004, 0.004, d / 2.0, True)
			EntityAlpha(l, Rnd(0.25, 0.8))
		Else
			HideEntity(l)
		EndIf
	Next
End Function

Function I806Alpha(ent%, a#)
	Local i%
	If EntityClass(ent) = "Mesh" Then EntityAlpha(ent, a)
	For i = 1 To CountChildren(ent)
		I806Alpha(GetChild(ent, i), a)
	Next
End Function

;the copy is grey all over (whatever colour the footage was)
Function I806Grey(n.NPCs)
	I806LoadTex()
	IndevOldTexAll(n\obj, I806Tex[7])
	EntityColor(n\obj, 205, 205, 205)
End Function

Function I806Type%(reel%)
	Select reel
		Case 1 Return NPCtypeD
		Case 2 Return NPCtypeGuard
		Case 5 Return NPCtypeClerk
	End Select
	Return 0
End Function

Function I806MakeCopy.NPCs(r.Rooms, reel%)
	Local p% = r\Objects[U48_S06_FORM]
	Local n.NPCs = CreateNPC(I806Type(reel), EntityX(p, True), EntityY(p, True) + 0.35, EntityZ(p, True))
	Select reel
		Case 1 : n\State = 0
		Case 2 : n\State = 9
		Default : n\State = 0 : n\State2 = 0
	End Select
	RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90 + 180, 0) ;facing the room, back to the screen
	I806Grey(n)
	I806Alpha(n\obj, 0.05)
	Return n
End Function

;keep the copy standing where it formed
Function I806Pin(r.Rooms, n.NPCs)
	If n = Null Then Return
	If n\IsDead Then Return
	Local p% = r\Objects[U48_S06_FORM]
	If Abs(EntityX(n\Collider, True) - EntityX(p, True)) + Abs(EntityZ(n\Collider, True) - EntityZ(p, True)) > 0.3 Or EntityY(n\Collider, True) < EntityY(p, True) - 0.15 Then
		PositionEntity(n\Collider, EntityX(p, True), EntityY(p, True) + 0.35, EntityZ(p, True), True)
		ResetEntity(n\Collider)
	EndIf
End Function

;what is left when a copy fails or dies: an unfinished or dead body (a grey Class-D body lying down), or blood
;and graphite if almost nothing had formed
Function I806Fail(r.Rooms, e.Events, how%)
	Local n.NPCs = r\NPC[0], x#, y#, z#
	Local p% = r\Objects[U48_S06_FORM]
	x = EntityX(p, True) : y = EntityY(p, True) : z = EntityZ(p, True)
	If n <> Null Then
		x = EntityX(n\Collider, True) : z = EntityZ(n\Collider, True)
		RemoveNPC(n)
		r\NPC[0] = Null
	EndIf
	If how = 0 Then
		;blood and graphite dust
		Local de.Decals = CreateDecal(3, x, y + 0.006, z, 90, Rand(360), 0)
		de\Size = 0.6 : ScaleSprite(de\obj, de\Size, de\Size)
		de = CreateDecal(0, x + 0.2, y + 0.008, z - 0.1, 90, Rand(360), 0)
		de\Size = 0.5 : ScaleSprite(de\obj, de\Size, de\Size)
		EntityColor(de\obj, 40, 40, 44)
		PlaySound_Strict(LoadTempSound("SFX\Character\D9341\BloodDrip" + Rand(0, 3) + ".ogg"))
	Else
		Local b.NPCs = CreateNPC(NPCtypeD, x, y + 0.3, z)
		b\State = 0
		SetNPCFrame(b, 19)
		b\IsDead = True
		I806Grey(b)
		PlaySound_Strict(LoadTempSound("SFX\Indev\thump.wav"))
	EndIf
End Function

Function I806FindReel.Items()
	Local i%
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			If Left(Inventory(i)\itemtemplate\name, 7) = "reel806" Then Return Inventory(i)
		EndIf
	Next
	Return Null
End Function

Function I806ReelId%(name$)
	Select name
		Case "reel806a" Return 1
		Case "reel806b" Return 2
		Case "reel806c" Return 3
		Case "reel806d" Return 4
		Case "reel806e" Return 5
	End Select
	Return 0
End Function

Function I806ReelName$(id%)
	Return "reel806" + Mid("abcde", id, 1)
End Function

;give the reel back on the stand
Function I806Eject(r.Rooms, e.Events)
	If e\EventState3 > 0 Then
		Local p% = r\Objects[U48_S06_PROJ]
		TFormPoint(-20, 20, 60, p, 0)
		CreateItem(I806ReelName(e\EventState3), TFormedX(), TFormedY() + 0.1, TFormedZ())
	EndIf
	e\EventState3 = 0
End Function

Function I806Watching%(r.Rooms)
	If PlayerRoom <> r Or KillTimer < 0 Then Return False
	If Not (BlinkTimer < -16 Or BlinkTimer > -6) Then Return False
	Return EntityInView(r\Objects[U48_SCRQUAD], Camera)
End Function

;what the copy says when you talk to it
Function I806Line$(reel%, k%)
	Select reel
		Case 1
			Select k Mod 4
				Case 0 Return "Why is it so cold in here? Where is everybody - did they move my work detail again?"
				Case 1 Return "Last thing I remember is the alarm. Then the lights. Then... a cinema? You've got to be kidding me."
				Case 2 Return "My hands. Why are my hands grey? Why is EVERYTHING about me grey?"
				Default Return "Listen - my locker's on the Heavy side. Card's still in it. You take it. I don't think I'll need it."
			End Select
		Case 2
			Select k Mod 4
				Case 0 Return "Officer on post. Report. Why is this room dark, and why am I standing in front of the screen?"
				Case 1 Return "My partner was right beside me. Where is he? ...He's not coming, is he."
				Case 2 Return "My chest has been tight since I woke up. Probably nothing."
				Default Return "Here. My card. Get to the surface. That's an order, whoever you are."
			End Select
		Default
			Select k Mod 4
				Case 0 Return "Hello? Do I - do I know you? I'm sorry. I don't know anyone. I don't know my own name."
				Case 1 Return "There was music, I think. Somebody laughing. Was it me?"
				Case 2 Return "They tell me the others only last three days. I've been here much longer than that."
				Default Return "Will you come back? Nobody ever comes back down here."
			End Select
	End Select
End Function

Function UpdateIndevU48(e.Events)
	Local r.Rooms = e\room, n.NPCs, it.Items, watching%, i%, rate#
	If r\Objects[U48_PROJ] = 0 Then Return
	I806LoadTex()

	;after loading a save: find the copy again (NPCs are saved, the link to them is not)
	If e\EventState >= 2 And r\NPC[0] = Null And e\EventState2 > 5 Then
		Local fp% = r\Objects[U48_S06_FORM], best.NPCs, bd# = 3.0
		For n = Each NPCs
			If n\NPCtype = I806Type(e\EventState3) And (Not n\IsDead) Then
				If EntityDistance(n\Collider, fp) < bd Then bd = EntityDistance(n\Collider, fp) : best = n
			EndIf
		Next
		If best <> Null Then
			r\NPC[0] = best
			I806Grey(best)
		ElseIf e\EventState = 3 Then
			e\EventState = 0 : e\EventState2 = 0 : e\EventStr = ""
		EndIf
	EndIf

	If r\dist > 14 And e\EventState <> 2 And e\EventState <> 3 Then Return

	Local proj% = r\Objects[U48_S06_PROJ]
	Select e\EventState
		Case 0 ;--------------------------------------------------- empty
			If IndevTestOn And GetCLIInt("testproj", 0) > 0 And PlayerRoom = r And I806Hint = 0 Then ;room test: load and run straight away, 20x fast
				I806Hint = 1 : e\EventState3 = GetCLIInt("testproj", 0) : e\EventState = 2 : e\EventState2 = 0
				ShowEntity(r\Objects[U48_CONE])
			EndIf
			If PlayerRoom = r And I806Hint = 0 Then
				I806Hint = 1
				IS16Tell("A screening room. A big old projector stands on the stand at the back, aimed at a silver screen. The reels are in the cage - Containment Locker 8.", 7)
			EndIf
			If IS10Press(proj, 1.4) Then
				it = I806FindReel()
				If it = Null Then
					IS16Tell("The projector's spools are empty. The reels are kept in Containment Locker 8, in the corner.", 5)
				Else
					e\EventState3 = I806ReelId(it\itemtemplate\name)
					RemoveItem(it)
					e\EventState = 1
					PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
					IS16Tell("You thread the reel through the gate and onto the take-up spool. The lens glitters like a jeweller's tray. Click the projector again to run it.", 6)
				EndIf
			EndIf
		Case 1 ;--------------------------------------------------- loaded
			If IS10Press(proj, 1.4) Then
				e\EventState = 2 : e\EventState2 = 0 : I806Warn = 0
				ShowEntity(r\Objects[U48_CONE])
				IS16Tell("The LED array snaps on. Light floods the screen and the reels start to turn. Keep your eyes on the screen.", 5)
			EndIf
		Case 2 ;--------------------------------------------------- running
			;the reels, the sound, the footage, the light
			TurnEntity(r\Objects[U48_REEL1], 0, 0, -6 * FPSfactor)
			TurnEntity(r\Objects[U48_REEL2], 0, 0, -6 * FPSfactor)
			If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Indev\projector806.wav")
			e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, r\Objects[U48_LENS], 8, 0.8)
			I806Frame = I806Frame + FPSfactor
			If I806Frame > 6 Then
				I806Frame = 0
				Select e\EventState3
					Case 3 : EntityTexture(r\Objects[U48_SCRQUAD], I806Tex[5 * (Rand(2) - 1)])
					Case 5 : EntityTexture(r\Objects[U48_SCRQUAD], I806Tex[4])
					Default : EntityTexture(r\Objects[U48_SCRQUAD], I806Tex[Rand(1, 5) - (Rand(3) = 1)])
				End Select
				i = Rand(150, 230)
				LightColor(r\Objects[U48_SCREENLIGHT], i, i, i)
				EntityAlpha(r\Objects[U48_CONE], Rnd(0.08, 0.15))
			EndIf
			watching = I806Watching(r)
			e\EventState2 = e\EventState2 + 0 ;(kept as progress)
			Select e\EventState3
				Case 3, 4
					;nothing forms: cartoons and the living are beyond it - just let the reel run out
					e\EventState2 = e\EventState2 + FPSfactor * 100.0 / (70 * 20)
					If e\EventState2 >= 100 Then
						If e\EventState3 = 3 Then
							IS16Tell("The animated short runs out. Nothing has formed in front of the screen - drawings have nobody to bring back.", 6)
						Else
							IS16Tell("The interview runs out. Nothing forms. The interviewee is alive somewhere, and the projector can't touch the living.", 6)
						EndIf
						I806Stop(r, e)
						I806Eject(r, e)
						e\EventState = 0
					EndIf
				Default
					If e\EventState3 = 5 Then rate = 100.0 / (70 * 35) Else rate = 100.0 / (70 * 100)
					If IndevTestOn And GetCLIInt("testproj", 0) > 0 Then rate = rate * 20 : watching = True
					If watching Then
						e\EventState2 = Min(100, e\EventState2 + FPSfactor * rate)
						I806Warn = 0
					Else
						e\EventState2 = Max(0, e\EventState2 - FPSfactor * rate * 0.5)
						I806Warn = I806Warn + FPSfactor
						If I806Warn > 70 * 4 And r\NPC[0] <> Null And PlayerRoom = r Then
							I806Warn = -70 * 20
							IS16Tell("Nobody is watching. The shape in front of the screen is thinning out again.", 4)
						EndIf
					EndIf
					;the copy appears once the rays have something to build on
					If r\NPC[0] = Null And e\EventState2 > 5 Then
						r\NPC[0] = I806MakeCopy(r, e\EventState3)
						If e\EventState3 = 2 Then
							IS16Tell("Two officers walk the corridor on screen. Only one of them is starting to take shape in the light - the one the camera followed.", 6)
						ElseIf e\EventState3 = 5 Then
							IS16Tell("The same five seconds, over and over: a young woman laughing. It should be far too little film. Something is forming anyway.", 7)
						Else
							IS16Tell("Needle-thin rays reach out of the lens. Where they touch the air in front of the screen, something grey is building itself.", 6)
						EndIf
					EndIf
					If r\NPC[0] <> Null Then
						I806Pin(r, r\NPC[0])
						I806Alpha(r\NPC[0]\obj, Max(0.05, e\EventState2 / 100.0))
						If e\EventState2 <= 0 Then ;fully undone
							RemoveNPC(r\NPC[0]) : r\NPC[0] = Null
							IS16Tell("The shape in front of the screen comes apart into light and is gone.", 5)
						EndIf
					EndIf
					I806Needles(r\NPC[0] <> Null, r, r\NPC[0], e\EventState2 / 100.0)
					If e\EventState2 >= 100 Then
						;finished
						I806Stop(r, e)
						I806Alpha(r\NPC[0]\obj, 1.0)
						e\EventState = 3
						If e\EventState3 = 5 Then e\EventStr = "-1" Else e\EventStr = Str(Int(70 * 60 * Rnd(7.0, 7.5)))
						I806Talk = 0 : I806Gift = 0
						IS16Tell("The last reel runs out of the gate. Standing before the screen is a person - colourless from head to foot, blinking at the light.", 7)
						I806Eject(r, e)
					EndIf
			End Select
			;shut it down mid-run
			If e\EventState = 2 And IS10Press(proj, 1.4) Then
				If r\NPC[0] <> Null Then
					If e\EventState2 >= 60 Then
						I806Fail(r, e, 1)
						IS16Tell("You kill the lamp. The nearly finished body drops to the floor and doesn't get up. Its eyes are open. Nobody is behind them.", 7)
					ElseIf e\EventState2 >= 20 Then
						I806Fail(r, e, 1)
						IS16Tell("You kill the lamp. The half-made body folds onto the floor and lies still.", 6)
					Else
						I806Fail(r, e, 0)
						IS16Tell("You kill the lamp. What was forming sloughs onto the floor - blood, and a fine grey dust like pencil lead.", 7)
					EndIf
				Else
					IS16Tell("You shut the projector down. The reels clatter to a stop.", 4)
				EndIf
				I806Stop(r, e)
				I806Eject(r, e)
				e\EventState = 0 : e\EventState2 = 0
			EndIf
		Case 3 ;--------------------------------------------------- a copy is alive
			n = r\NPC[0]
			If n = Null Then
				e\EventState = 0 : e\EventStr = ""
				Return
			EndIf
			I806Pin(r, n)
			If PlayerRoom = r Then
				If IS10Press(n\Collider, 1.3) Then
					IS16Tell(Chr(34) + I806Line(e\EventState3, I806Talk) + Chr(34), 6)
					I806Talk = I806Talk + 1
					If I806Talk >= 4 And I806Gift = 0 Then
						I806Gift = 1
						Select e\EventState3
							Case 1 : CreateItem("key3", EntityX(n\Collider, True), EntityY(n\Collider, True) + 0.2, EntityZ(n\Collider, True))
							Case 2 : CreateItem("key4", EntityX(n\Collider, True), EntityY(n\Collider, True) + 0.2, EntityZ(n\Collider, True))
							Default : IndevRelieveStress(15)
						End Select
					EndIf
				EndIf
			EndIf
			;the lifespan (806-1-a has none)
			If e\EventStr <> "-1" Then
				Local lifeLeft# = Float(e\EventStr) - FPSfactor
				e\EventStr = Str(Int(lifeLeft))
				If lifeLeft < 70 * 20 And lifeLeft + FPSfactor >= 70 * 20 And PlayerRoom = r Then
					IS16Tell(Chr(34) + "My heart's going funny. Must be the cold." + Chr(34), 4)
				EndIf
				If lifeLeft <= 0 Then
					If PlayerRoom = r Then
						PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Heartbeat.ogg"))
						IS16Tell("The grey figure clutches at its chest and goes down. Cardiac arrest - right on schedule, if the file is to be believed.", 7)
					EndIf
					I806Fail(r, e, 1)
					e\EventState = 0 : e\EventState2 = 0 : e\EventStr = ""
				EndIf
			EndIf
	End Select
End Function

Function I806Stop(r.Rooms, e.Events)
	If e\SoundCHN <> 0 Then
		If ChannelPlaying(e\SoundCHN) Then StopChannel(e\SoundCHN)
		e\SoundCHN = 0
	EndIf
	HideEntity(r\Objects[U48_CONE])
	EntityTexture(r\Objects[U48_SCRQUAD], I806Tex[6])
	LightColor(r\Objects[U48_SCREENLIGHT], 0, 0, 0)
	I806Needles(False, r, Null, 0)
End Function
