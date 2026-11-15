;=====================================================================
; SCP: Containment Breach - Indev: seventh batch, ten rooms, ten SCPs
;
;   room2subway052  HCZ    SCP-052   down a lift to the 59th St. platform: the R4 car pulls in at its hour,
;                                    opens for three quarters of a minute and goes - with you or without you
;   room2hall99     LCZ    SCP-953   Hallway 99: a "researcher" calls you away from the kennels. The dogs
;                                    (KENNEL ALERT) are the only thing she will not walk past
;   room2gameshow   Indev  SCP-024   STAY or LEAVE; three rounds; TAKE IT or RISK IT; losers never leave.
;                                    A lift goes up to the observation lab. The tape turns up in the mailbox
;   room2diner      EZ     SCP-4258  Freddy's: your batteries die at the door, the coffee is free, the windows
;                                    show wherever the last customer came from
;   room2sheet      HCZ    SCP-6096  it gets up and walks to somebody; you will hold the door for it. If it
;                                    is you it wants, only you can act against it (the fan hoist)
;   room2block15    HCZ    SCP-2701  Cell 667: step inside while the INTAKE page is on the clip and you are
;                                    gone for fifteen seconds that last for weeks
;   room2mailbox    Indev  SCP-1269  a mailbox at the curb that is somewhere else every time you look back
;   room2psych      LCZ    SCP-482   the straitjacket: no fear while it is on; get the attendant to take it off in time
;   room2realchar   Indev  SCP-3325  the studio, and LG-1 below it: one of the "characters" is loose
;   room2wait1440   HCZ    SCP-1440  the old man: everything near him breaks, slowly, then all at once
;
;   IndevS10Data.bb is generated (Tools\roomkit\gen_b7.py): the S10_* slot constants, the FillRoom table,
;   the fans, the events. Shared helpers come from IndevS16.bb / IndevS13.bb / IndevAnnex.bb. No globals:
;   handles in r\Objects[] / r\RoomDoors[] / r\NPC[], progress in the room's event (EventState / 2 / 3,
;   lower-case one-letter flags in EventStr, whole numbers in EventStr as <K123> with an upper-case K).
;=====================================================================

;---------------------------------------------------------------------
; helpers
;---------------------------------------------------------------------

Function IS10Door.Doors(r.Rooms, lx#, ly#, lz#, angle%, key%, locked%, dopen%, old%)
	Local lvl% = r\zone
	If old Then lvl = 4
	Local d.Doors = CreateDoor(lvl, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, angle, r, dopen, False, key)
	d\AutoClose = False : d\open = dopen : d\locked = locked
	IndevButtonsToWall(d) ;out of the thick side-room walls (IndevAnnex.bb)
	Return d
End Function

;a whole number kept in EventStr as <K123>
Function IS10Num%(e.Events, k$)
	Local i% = Instr(e\EventStr, "<" + k)
	If i = 0 Then Return 0
	Local j% = Instr(e\EventStr, ">", i)
	Return Int(Mid(e\EventStr, i + 2, j - i - 2))
End Function

Function IS10SetNum(e.Events, k$, v%)
	Local i% = Instr(e\EventStr, "<" + k), j%
	If i > 0 Then
		j = Instr(e\EventStr, ">", i)
		e\EventStr = Left(e\EventStr, i - 1) + Mid(e\EventStr, j + 1)
	EndIf
	e\EventStr = e\EventStr + "<" + k + v + ">"
End Function

;aimed at a pivot within dist: shows the hand, True on the click
Function IS10Press%(p%, dist#)
	If Not IS16Aim(p, dist, 0.97) Then Return False
	DrawHandIcon = True
	If MouseHit1 Then
		MouseHit1 = False
		Return True
	EndIf
	Return False
End Function

;a flat square in room units, w across and h high, double-sided and unlit. vertical: in the local y-z plane
Function IS10Quad%(w#, h#, vertical%, flip%)
	Local m% = CreateMesh(), s% = CreateSurface(m), u0# = 0, u1# = 1
	If flip Then u0 = 1 : u1 = 0
	If vertical Then
		AddVertex(s, 0, -h / 2, -w / 2, u0, 1)
		AddVertex(s, 0, -h / 2, w / 2, u1, 1)
		AddVertex(s, 0, h / 2, w / 2, u1, 0)
		AddVertex(s, 0, h / 2, -w / 2, u0, 0)
	Else
		AddVertex(s, -w / 2, 0, -h / 2, u0, 1)
		AddVertex(s, w / 2, 0, -h / 2, u1, 1)
		AddVertex(s, w / 2, 0, h / 2, u1, 0)
		AddVertex(s, -w / 2, 0, h / 2, u0, 0)
	EndIf
	AddTriangle(s, 0, 2, 1)
	AddTriangle(s, 0, 3, 2)
	EntityFX(m, 1 + 16)
	Return m
End Function

;something made in room units that hangs off a pivot (the pivot's global scale is 1)
Function IS10OnPivot%(m%, p%)
	EntityParent(m, p, False)
	ScaleEntity(m, RoomScale, RoomScale, RoomScale)
	PositionEntity(m, 0, 0, 0)
	RotateEntity(m, 0, 0, 0)
	Return m
End Function

;move a room child (room units, local) towards (tx, tz); returns how far it still had to go
Function IS10Walk#(ent%, tx#, tz#, speed#)
	Local x# = EntityX(ent), z# = EntityZ(ent)
	Local dx# = tx - x, dz# = tz - z, l# = Sqr(dx * dx + dz * dz), st#
	If l < 0.5 Then Return l
	st = Min(l, speed * FPSfactor)
	PositionEntity(ent, x + dx / l * st, EntityY(ent), z + dz / l * st)
	RotateEntity(ent, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(ent), 8.0), 0)
	Return l
End Function

;turn a room child to face the player
Function IS10Look(r.Rooms, ent%)
	IAxLocal(r)
	RotateEntity(ent, 0, VectorYaw(TFormedX() - EntityX(ent), 0, TFormedZ() - EntityZ(ent)), 0)
End Function

;tug the player towards a world point (the camera turns a little, the feet follow)
Function IS10Pull(ent%, push#, turn#)
	Local dx# = EntityX(ent, True) - EntityX(Collider, True), dz# = EntityZ(ent, True) - EntityZ(Collider, True)
	Local l# = Sqr(dx * dx + dz * dz)
	If l < 0.05 Then Return
	RotateEntity(Collider, EntityPitch(Collider), CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(Collider), turn), EntityRoll(Collider))
	TranslateEntity(Collider, dx / l * push * FPSfactor, 0, dz / l * push * FPSfactor)
End Function

Function IS10Load(e.Events, file$)
	IS16Hush(e)
	If e\Sound <> 0 Then FreeSound_Strict(e\Sound)
	e\Sound = LoadSound_Strict(file)
End Function

Function IS10Sound(file$, ent%, range#, vol#)
	PlaySound2(LoadTempSound(file), Camera, ent, range, vol)
End Function

;---------------------------------------------------------------------
; the things only code can make (called at the end of IndevFillS10)
;---------------------------------------------------------------------

Function IndevS10Dress(r.Rooms)
	Local i%, m%, tex%, at%, lf%, gx#, gz#, sz#
	Select r\RoomTemplate\Name
		Case "room2subway052"
			;the R4 car: full-bright (its texture carries its own light), solid, hidden until it comes
			m = IS16Prop(r, "GFX\npcs\scp052.b3d", "GFX\npcs\indev_subway.png", r\Objects[S10_SUB_TRAIN], 0)
			EntityFX(m, 1)
			EntityType(m, HIT_MAP)
			r\Objects[S10_SUB_TRAINM] = m
			tex = LoadTexture_Strict("GFX\npcs\indev_subway.png")
			For i = 0 To 5
				lf = LoadMesh_Strict("GFX\npcs\scp052d.b3d")
				EntityTexture(lf, tex)
				EntityParent(lf, m, False)
				EntityFX(lf, 1)
				EntityType(lf, HIT_MAP)
				r\Objects[S10_SUB_LEAF + i] = lf
			Next
			FreeTexture(tex)
			For i = 0 To 1
				lf = LoadMesh_Strict("GFX\map\indev_ceilfan.b3d")
				EntityParent(lf, m, False)
				ScaleEntity(lf, 44, 44, 44)
				PositionEntity(lf, 0, 284, -375 + 750 * i)
				EntityFX(lf, 1 + 16)
				r\Objects[S10_SUB_TFAN + i] = lf
			Next
			IS10Leaves(r, 0)
			HideEntity(m)

		Case "room2hall99"
			For i = 0 To 5
				If i Mod 2 = 0 Then
					m = IS16Prop(r, "GFX\npcs\indev_dog.b3d", "GFX\npcs\indev_jindo.png", r\Objects[S10_H99_DOG0 + i], 270 - 180 * (i >= 3))
				Else
					m = IS16Prop(r, "GFX\npcs\indev_dog.b3d", "GFX\npcs\indev_hound.png", r\Objects[S10_H99_DOG0 + i], 270 - 180 * (i >= 3))
				EndIf
				r\Objects[S10_H99_DOGM + i] = m
			Next
			m = IS16Prop(r, "GFX\npcs\scp953f.b3d", "GFX\npcs\indev_fox.png", r\Objects[S10_H99_SPOTN], 180)
			HideEntity(m)
			r\Objects[S10_H99_FOXM] = m
			m = IS16Prop(r, "GFX\npcs\indev_cart.b3d", "GFX\npcs\indev_cart.png", r\Objects[S10_H99_CARTA], 0)
			EntityPickMode(m, 2)
			r\Objects[S10_H99_CARTM] = m

		Case "room2gameshow"
			gx = EntityX(r\Objects[S10_GS_GRID]) : gz = EntityZ(r\Objects[S10_GS_GRID])
			sz = (EntityX(r\Objects[S10_GS_GRID2]) - gx) / 3.0
			For i = 0 To 11
				m = IS10Quad(sz - 12, sz - 12, False, False)
				EntityParent(m, r\obj, False)
				PositionEntity(m, gx + ((i Mod 3) + 0.5) * sz, 2.0, gz + ((i / 3) + 0.5) * sz)
				EntityBlend(m, 3)
				EntityAlpha(m, 0.6)
				HideEntity(m)
				r\Objects[S10_GS_TILE + i] = m
			Next
			For i = 0 To 1
				m = IS16Prop(r, "GFX\npcs\indev_shade.b3d", "GFX\npcs\indev_shade.png", r\Objects[S10_GS_STAGEIN], 0)
				EntityFX(m, 1)
				EntityAlpha(m, 0.92)
				HideEntity(m)
				r\Objects[S10_GS_SHADE + i] = m
			Next

		Case "room2diner"
			tex = LoadTexture_Strict("GFX\map\indev_view0.png")
			For i = 0 To 3
				m = IS10OnPivot(IS10Quad(200, 150, True, True), r\Objects[S10_DIN_WIN0 + i])
				EntityTexture(m, tex)
			Next
			FreeTexture(tex)

		Case "room2sheet"
			m = IS16Prop(r, "GFX\npcs\scp6096.b3d", "GFX\npcs\indev_sheet.png", r\Objects[S10_SH6_SIT], 0)
			ScaleEntity(m, 1, 0.62, 1)
			EntityPickMode(m, 2)
			r\Objects[S10_SH6_SHEETM] = m
			m = CreatePivot()
			EntityParent(m, r\obj)
			r\Objects[S10_SH6_PIN] = m

		Case "room2mailbox"
			m = IS16Prop(r, "GFX\npcs\scp1269.b3d", "GFX\npcs\indev_mailbox.png", r\Objects[S10_MB_MS0], 90)
			EntityPickMode(m, 2)
			r\Objects[S10_MB_MBOX] = m
			lf = LoadMesh_Strict("GFX\npcs\scp1269f.b3d")
			tex = LoadTexture_Strict("GFX\npcs\indev_mailbox.png")
			EntityTexture(lf, tex)
			FreeTexture(tex)
			EntityParent(lf, m, False)
			PositionEntity(lf, 13, 156, 18)
			RotateEntity(lf, -90, 0, 0)
			r\Objects[S10_MB_MFLAG] = lf

		Case "room2psych"
			m = IS16Prop(r, "GFX\npcs\scp482.b3d", "GFX\npcs\indev_leather.png", r\Objects[S10_PSY_JACKET], 180)
			EntityPickMode(m, 2)
			r\Objects[S10_PSY_JACKETM] = m

		Case "room2realchar"
			For i = 0 To 4
				m = IS16Prop(r, "GFX\npcs\scp3325.b3d", "GFX\npcs\indev_puppet2.png", r\Objects[S10_RCI_TUBE0 + i], i * 71)
				ScaleEntity(m, 0.55, 0.55, 0.55)
				RotateEntity(m, 22, i * 71, 8)
				r\Objects[S10_RCI_SPEC + i] = m
			Next
			;the loose one: a collider like an NPC's, the model and its jaw hung off it
			at = r\Objects[S10_RCI_CRE]
			lf = CreatePivot()
			PositionEntity(lf, EntityX(at, True), EntityY(at, True) + 0.25, EntityZ(at, True))
			EntityRadius(lf, 0.2)
			EntityType(lf, HIT_PLAYER)
			r\Objects[S10_RCI_CREC] = lf
			m = IS16Prop(r, "GFX\npcs\scp3325.b3d", "GFX\npcs\indev_puppet.png", at, 0)
			EntityParent(m, lf, True)
			PositionEntity(m, 0, -0.2, 0)
			RotateEntity(m, 0, 0, 0)
			r\Objects[S10_RCI_CREM] = m
			at = LoadMesh_Strict("GFX\npcs\scp3325j.b3d")
			tex = LoadTexture_Strict("GFX\npcs\indev_puppet.png")
			EntityTexture(at, tex)
			FreeTexture(tex)
			EntityParent(at, m, False)
			PositionEntity(at, 0, 132, 8)
			r\Objects[S10_RCI_CREJ] = at
			m = CreateCube()
			ScaleEntity(m, 0.07, 0.03, 0.05)
			EntityColor(m, 150, 32, 40)
			EntityParent(m, r\obj)
			HideEntity(m)
			r\Objects[S10_RCI_MEATM] = m

		Case "room2wait1440"
			m = IS10OnPivot(IS10Quad(200, 220, True, False), r\Objects[S10_OLD_CRACKAT])
			tex = LoadTexture_Strict("GFX\map\indev_crack.png", 1 + 2)
			EntityTexture(m, tex)
			FreeTexture(tex)
			HideEntity(m)
			r\Objects[S10_OLD_CRACK] = m
	End Select
End Function

;---------------------------------------------------------------------
; the shared event
;---------------------------------------------------------------------

Function UpdateIndevS10(e.Events)
	Local r.Rooms = e\room
	Local k# = 1.0
	If r\dist < 10.0 Then
		Select r\RoomTemplate\Name
			Case "room2sheet"
				If IAxFlag(e, "f") Then k = 0
			Case "room2wait1440"
				If e\EventState2 >= 2 And (Not IAxFlag(e, "g")) Then k = 4.0 + Sin(MilliSecs() * 0.4) * 2.5
		End Select
		If k > 0 Then IndevS10Spin(r, k)
	EndIf
	Select r\RoomTemplate\Name
		Case "room2subway052"
			UpdateS10Subway(e)
		Case "room2hall99"
			UpdateS10Hall99(e)
		Case "room2gameshow"
			UpdateS10GameShow(e)
		Case "room2diner"
			UpdateS10Diner(e)
		Case "room2sheet"
			UpdateS10Sheet(e)
		Case "room2block15"
			UpdateS10Block15(e)
		Case "room2mailbox"
			UpdateS10Mailbox(e)
		Case "room2psych"
			UpdateS10Psych(e)
		Case "room2realchar"
			UpdateS10RealChar(e)
		Case "room2wait1440"
			UpdateS10OldMan(e)
	End Select
End Function

;=====================================================================
; room2subway052 - SCP-052
;   EventState  0 waiting, 1 coming in, 2 doors open, 3 doors closing, 4 riding
;   EventState2 the lift      EventState3 time left in the current state
;   flags: w first wait set, n guard placed, f first arrival (the passenger), i you've looked round the car,
;          g the guard has shouted; count q: lines the passenger has said.  NPC[0] the guard, NPC[1] passenger
;=====================================================================

;the three door openings of the car (its model: scp052.b3d, doors on its -x side at z -560 / 0 / 560)
Function IS10Leaves(r.Rooms, op#)
	Local i%, dz#, side#
	For i = 0 To 5
		dz = -560.0 + 560.0 * (i / 2)
		side = (i Mod 2) * 2 - 1
		PositionEntity(r\Objects[S10_SUB_LEAF + i], -192, 0, dz + side * (42.5 + 80.0 * op))
	Next
End Function

Function IS10TrainGone(e.Events)
	Local r.Rooms = e\room
	HideEntity(r\Objects[S10_SUB_TRAINM])
	IS13Drop(e, "v")
	IS10Leaves(r, 0)
	IS16Hush(e)
	e\EventState = 0
	e\EventState3 = 70 * Rand(70, 110)
End Function

Function UpdateS10Subway(e.Events)
	Local r.Rooms = e\room
	Local train% = r\Objects[S10_SUB_TRAINM]
	Local lx#, ly#, lz#, inpit%, incar%, i%, n.NPCs, q$ = Chr(34), roll%, cnt%, pick%, r2.Rooms, it.Items, d#

	If PlayerRoom <> r Then
		If e\EventState > 0 And e\EventState < 4 Then IS10TrainGone(e)
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[S10_SUB_GUARD], True), EntityY(r\Objects[S10_SUB_GUARD], True) + 0.35, EntityZ(r\Objects[S10_SUB_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 270, 0)
		r\NPC[0] = n
	EndIf

	IAxLocal(r)
	lx = TFormedX() : ly = TFormedY() : lz = TFormedZ()
	inpit = (lx > 445.0 And ly < -720.0 And lz < 828.0)
	incar = (lx > 492.0 And lx < 868.0 And Abs(lz) < 800.0 And ly > -720.0 And IAxFlag(e, "v"))

	;---- the guard of MTF Gamma-6
	n = r\NPC[0]
	If n <> Null Then
		n\State = 9
		d = EntityDistance(n\Collider, Collider)
		If incar And e\EventState = 2 And (Not IAxFlag(e, "g")) Then
			IAxSetFlag(e, "g")
			IAxSay("Gamma-6", "Off the train! Off it, now! Nobody boards - that's the whole job!", 6)
		ElseIf d < 2.6 And MsgTimer <= 0 And Rand(700) = 1 Then
			Select Rand(4)
				Case 1
					IAxSay("Gamma-6", "Station's closed. Track maintenance. That's what the sign says, so that's what it is.", 7)
				Case 2
					IAxSay("Gamma-6", "When the doors open you stay on the platform. Anyone who gets off goes to Site-21.", 7)
				Case 3
					IAxSay("Gamma-6", "If you're on the tracks when it comes, it comes anyway. Steps are at the north end.", 7)
				Case 4
					IAxSay("Gamma-6", "Last agent who rode it came back without his hands. And a note.", 6)
			End Select
		EndIf
	EndIf

	;---- passenger 052-27
	n = r\NPC[1]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_passenger.jpg")
		If EntityDistance(n\Collider, r\Objects[S10_SUB_PSTAND]) > 0.5 And (Not IAxFlag(e, "p")) Then
			n\State = 1
			RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(EntityX(r\Objects[S10_SUB_PSTAND], True) - EntityX(n\Collider), 0, EntityZ(r\Objects[S10_SUB_PSTAND], True) - EntityZ(n\Collider)), EntityYaw(n\Collider), 10.0), 0)
		Else
			IAxSetFlag(e, "p")
			If EntityDistance(n\Collider, Collider) < 4.0 Then IAxFace(n, Collider)
		EndIf
		If IndevAimedAt(n\obj, n\Collider, 1.6) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				e\EventStr = e\EventStr + "q"
				Select IS13Count(e, "q")
					Case 1
						IAxSay("Passenger", "What year is it? No - don't tell me. They told me not to ask anyone that.", 7)
					Case 2
						IAxSay("Passenger", "I got on two stops back. After the late show. It's still Saturday, isn't it? It has to be.", 7)
					Case 3
						IS16Give("doc052b", n\Collider)
						IAxSay("Passenger", "Here. I wrote it down, everything. Give it to whoever's in charge. Please.", 7)
					Default
						IAxSay("Passenger", "They're going to take me to Site-21, aren't they. My mother will be worried sick.", 6)
				End Select
			EndIf
		EndIf
	EndIf

	;---- the car
	Select e\EventState
		Case 0
			If ly < -400.0 Then
				If Not IAxFlag(e, "w") Then
					IAxSetFlag(e, "w")
					e\EventState3 = 70 * 14
				EndIf
				e\EventState3 = e\EventState3 - FPSfactor
				If Mid(CurrentTime(), 4, 2) = "57" Then e\EventState3 = Min(e\EventState3, 70 * 3)
				If e\EventState3 <= 0 Then
					e\EventState = 1
					e\EventState3 = 70 * 4.5
					IS10Sound("SFX\Indev\train_arrive.wav", r\Objects[S10_SUB_TRAIN], 14.0, 1.0)
					LightBlink = 1.0
					IS16Tell("A wind comes up the tunnel, then a roar, then a long iron squeal.", 5)
				EndIf
			EndIf

		Case 1
			e\EventState3 = e\EventState3 - FPSfactor
			CameraShake = Max(CameraShake, (1.0 - e\EventState3 / (70 * 4.5)) * 1.8)
			If e\EventState3 <= 0 Then
				If inpit Then
					DeathMSG = "Subject D-9341 was found on the track bed of the 59th St. platform reconstruction, struck by a subway car. The only car ever seen there is a type R4, scrapped in 1975."
					Kill()
					Return
				EndIf
				ShowEntity(train)
				IAxSetFlag(e, "v")
				IS10Leaves(r, 0)
				e\EventState = 2
				e\EventState3 = 70 * 45
				LightBlink = 2.0
				IS10Sound("SFX\Indev\train_chime.wav", r\Objects[S10_SUB_TRAIN], 12.0, 0.9)
				If Not IAxFlag(e, "f") Then
					IAxSetFlag(e, "f")
					n = IS16Person(r, S10_SUB_PASS, 90)
					r\NPC[1] = n
					IS16Tell("It is simply there: a green car, lit and spotless, A - 8 AV EXP. A man in a brown suit steps off, blinking.", 8)
				Else
					IS16Tell("The car is there again, as if it had never gone. Its doors open on an empty, lit interior.", 6)
				EndIf
			EndIf

		Case 2
			ShowEntity(train)
			IS10Leaves(r, Min(1.0, (70 * 45 - e\EventState3) / (70 * 1.5)))
			e\EventState3 = e\EventState3 - FPSfactor
			If incar And (Not IAxFlag(e, "i")) Then
				IAxSetFlag(e, "i")
				IS16Tell("Rattan seats, white straps, a FRESHA COLA card. Everything is new, and everything is from 1932.", 7)
			EndIf
			If e\EventState3 < 70 * 10 And e\EventState3 + FPSfactor >= 70 * 10 Then
				IS10Sound("SFX\Indev\train_chime.wav", r\Objects[S10_SUB_TRAIN], 12.0, 0.9)
				IS16Tell("Ding-dong. Stand clear of the closing doors.", 4)
			EndIf
			If e\EventState3 <= 0 Then
				e\EventState = 3
				e\EventState3 = 70 * 2.5
			EndIf

		Case 3
			IS10Leaves(r, Max(0, e\EventState3 / (70 * 2.5)))
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 Then
				IS10Leaves(r, 0)
				If incar Then
					e\EventState = 4
					e\EventState3 = 70 * 10
					IS10Load(e, "SFX\Indev\train_ride.wav")
					IS16Tell("The doors close. The platform slides away, and there are no more stations, only the dark.", 7)
				Else
					IS10Sound("SFX\Indev\train_depart.wav", r\Objects[S10_SUB_TRAIN], 14.0, 1.0)
					LightBlink = 1.5
					IS10TrainGone(e)
				EndIf
			EndIf

		Case 4
			;riding: where the car goes is nobody's business
			e\EventState3 = e\EventState3 - FPSfactor
			If e\Sound <> 0 Then e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, Collider, 6.0, 1.0)
			CameraShake = Max(CameraShake, 1.2)
			BlurTimer = Max(BlurTimer, 200)
			If Rand(120) = 1 Then LightBlink = 1.0
			If e\EventState3 < 70 * 6 And e\EventState3 + FPSfactor >= 70 * 6 Then IS16Tell("Lit platforms flick past in the dark. 1976. 2014. A sign that says 2204, and people waving.", 7)
			If e\EventState3 <= 0 Then
				IS16Hush(e)
				roll = Rand(100)
				If roll > 90 Then
					DeathMSG = "On the night of the incident a body was thrown from SCP-052 as it left the 59th St. platform, landing ten metres away. It was identified as Subject D-9341, who had boarded seconds earlier. Estimated time of death: [DATA EXPUNGED]."
					Kill()
					Return
				EndIf
				cnt = 0
				If roll > 40 And roll <= 75 Then
					For r2 = Each Rooms
						If r2 <> r And (Left(r2\RoomTemplate\Name, 7) = "room2v_" Or Left(r2\RoomTemplate\Name, 7) = "room2w_") Then cnt = cnt + 1
					Next
				EndIf
				If cnt > 0 Then
					;the doors open somewhere else
					pick = Rand(1, cnt)
					cnt = 0
					For r2 = Each Rooms
						If r2 <> r And (Left(r2\RoomTemplate\Name, 7) = "room2v_" Or Left(r2\RoomTemplate\Name, 7) = "room2w_") Then
							cnt = cnt + 1
							If cnt = pick Then Exit
						EndIf
					Next
					TFormPoint(0, 180, -720, r2\obj, 0)
					PositionEntity(Collider, TFormedX(), TFormedY(), TFormedZ())
					ResetEntity(Collider)
					UpdateDoors()
					UpdateRooms()
					For it = Each Items
						it\disttimer = 0
					Next
					PlayerRoom = r2
					HideEntity(train)
					IS13Drop(e, "v")
					e\EventState = 0
					e\EventState3 = 70 * Rand(70, 110)
					IndevStress = Min(100, IndevStress + 20)
					BlinkTimer = -10
					IS16Tell("The doors open on a corridor you know, nowhere near any station. When you turn round there is only wall.", 8)
				Else
					;back at 59th St.
					PositionEntity(Collider, EntityX(r\Objects[S10_SUB_EXIT], True), EntityY(r\Objects[S10_SUB_EXIT], True) + 0.4, EntityZ(r\Objects[S10_SUB_EXIT], True))
					ResetEntity(Collider)
					BlinkTimer = -10
					IS10TrainGone(e)
					If roll > 75 Then
						Injuries = Injuries + 2.2
						Bloodloss = Min(100, Bloodloss + 35)
						IndevStress = Min(100, IndevStress + 40)
						IS16Give("doc052c", Collider)
						IS16Tell("You are on the platform at 59th St. You don't remember the ride. Your hands are bandaged, badly. There is a note in your pocket.", 9)
					Else
						IndevStress = Min(100, IndevStress + 15)
						Select Rand(5)
							Case 1
								IS16Give("finefirstaid", Collider)
							Case 2
								IS16Give("18vbat", Collider)
							Case 3
								IS16Give("fineeyedrops", Collider)
							Case 4
								IS16Give("key4", Collider)
							Default
								IS16Give("snav300", Collider)
						End Select
						IS16Tell("The doors open on 59th St. The clock still says 11:57. Your legs say you rode for hours. Something from the seat came with you.", 9)
					EndIf
				EndIf
			EndIf
	End Select

	If IAxFlag(e, "v") Then
		For i = 0 To 1
			TurnEntity(r\Objects[S10_SUB_TFAN + i], 0, 6.0 * FPSfactor, 0)
		Next
	EndIf
End Function

;=====================================================================
; room2hall99 - SCP-953
;   EventState  0 nobody, 1 she is in the hallway (as a researcher), 2 the fox, running, 3 she is away (cooldown)
;   EventState2 the dogs barking (time left)      EventState3 time in the current state
;   flags: s she came in at the south end, r the cart is coming back, l she has been seen for what she is,
;          c a line said this second;  NPC[0] the "researcher"
;=====================================================================

Function UpdateS10Hall99(e.Events)
	Local r.Rooms = e\room
	Local fox% = r\Objects[S10_H99_FOXM], cart% = r\Objects[S10_H99_CARTM]
	Local i%, m%, n.NPCs, lx#, lz#, nz#, safe%, d#, t# = IS16Time(), spot%, cz#, fz#

	;the cart keeps its rounds whoever is watching
	If cart <> 0 Then
		If IAxFlag(e, "r") Then
			If IS10Walk(cart, EntityX(r\Objects[S10_H99_CARTA]), EntityZ(r\Objects[S10_H99_CARTA]), 1.1) < 1.0 Then IS13Drop(e, "r")
		Else
			If IS10Walk(cart, EntityX(r\Objects[S10_H99_CARTB]), EntityZ(r\Objects[S10_H99_CARTB]), 1.1) < 1.0 Then IAxSetFlag(e, "r")
		EndIf
	EndIf
	If e\EventState2 > 0 Then e\EventState2 = Max(0, e\EventState2 - FPSfactor)

	If PlayerRoom <> r Then
		If e\EventState = 1 Or e\EventState = 2 Then
			IS13Gone(r, 0)
			HideEntity(fox)
			e\EventState = 3
			e\EventState3 = 70 * 40
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return

	;---- the dogs: breathing, or on their feet and barking
	For i = 0 To 5
		m = r\Objects[S10_H99_DOGM + i]
		If e\EventState2 > 0 Then
			PositionEntity(m, EntityX(m), Abs(Sin(t * 520 + i * 70)) * 9, EntityZ(m))
			If r\NPC[0] <> Null Then
				TFormPoint(EntityX(r\NPC[0]\Collider, True), 0, EntityZ(r\NPC[0]\Collider, True), 0, r\obj)
				RotateEntity(m, 0, CurveAngle(VectorYaw(TFormedX() - EntityX(m), 0, TFormedZ() - EntityZ(m)), EntityYaw(m), 10), 0)
			EndIf
			If Rand(90) = 1 Then IS10Sound("SFX\Indev\bark.wav", m, 12.0, 0.9)
		Else
			PositionEntity(m, EntityX(m), 0, EntityZ(m))
			ScaleEntity(m, 1, 1.0 + 0.02 * Sin(t * 160 + i * 50), 1)
			If Rand(2200) = 1 Then IS10Sound("SFX\Indev\bark.wav", m, 10.0, 0.6)
		EndIf
	Next

	;---- KENNEL ALERT
	If IS10Press(r\Objects[S10_H99_ALERT], 1.3) Or IS10Press(r\Objects[S10_H99_ALERT2], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		e\EventState2 = 70 * 20
		IS16Tell("A klaxon whoops once and every dog in the hallway is up and barking.", 5)
	EndIf
	If IS16Click(cart, cart, 1.3) Then
		IS16Tell("A tray: 1.5 kg of fresh liver under film. HALLWAY 99 - CELL 953. A speaker on the cart croaks: STAND CLEAR.", 7)
	EndIf

	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()
	safe = (lz > -700.0 And lz < 330.0)

	Select e\EventState
		Case 0, 3
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 And Rand(300) = 1 Then
				;she comes in at the far end from you
				If lz > 0 Then
					spot = S10_H99_SPOTS
					IAxSetFlag(e, "s")
				Else
					spot = S10_H99_SPOTN
					IS13Drop(e, "s")
				EndIf
				If EntityDistance(r\Objects[spot], Collider) > 3.0 Then
					n = IS16Person(r, spot, 0)
					r\NPC[0] = n
					e\EventState = 1
					e\EventState3 = 0
					IS13Drop(e, "l")
				EndIf
			EndIf

		Case 1
			n = r\NPC[0]
			If n = Null Then
				e\EventState = 3
				Return
			EndIf
			IAxSkin(n, "GFX\npcs\indev_kumiho.jpg")
			IAxFace(n, Collider)
			e\EventState3 = e\EventState3 + FPSfactor
			d = EntityDistance(n\Collider, Collider)
			TFormPoint(EntityX(n\Collider, True), 0, EntityZ(n\Collider, True), 0, r\obj)
			nz = TFormedZ()
			;the dogs: barking, she cannot stay
			If e\EventState2 > 0 Then
				e\EventState = 2
				e\EventState3 = 70 * 3
				PositionEntity(fox, TFormedX(), 0, nz)
				RotateEntity(fox, 0, 180 * IAxFlag(e, "s"), 0)
				ShowEntity(fox)
				IS13Gone(r, 0)
				IS10Sound("SFX\Indev\foxhiss.wav", fox, 12.0, 1.0)
				IndevStress = Min(100, IndevStress + 12)
				IS16Tell("The barking hits her like a slap. For a second there is no woman: a red fox, nine tails up like a fan, and then it is running.", 8)
				Return
			EndIf
			;she will not come down among the kennels
			n\State = 0
			If d > 1.0 Then
				If IAxFlag(e, "s") And nz < -760 Then n\State = 1
				If (Not IAxFlag(e, "s")) And nz > 440 Then n\State = 1
			EndIf
			If Not safe And d < 9.0 Then
				;the suggestion: you start walking towards her
				IS10Pull(n\Collider, 0.008, 40.0)
				IndevStress = Min(100, IndevStress + 0.01 * FPSfactor)
				If MsgTimer <= 0 And Rand(160) = 1 Then
					Select Rand(5)
						Case 1
							IAxSay("Researcher", "Oh, thank god, somebody. Could you help me? The dogs won't let me past.", 6)
						Case 2
							IAxSay("Researcher", "Come here. Just for a second. I need you to hold something.", 5)
						Case 3
							IAxSay("Researcher", "It's all right, I'm one of you. Look, I've got my badge. Come and look.", 6)
						Case 4
							IAxSay("Researcher", "Don't look at the dogs. Look at me.", 4)
						Case 5
							IAxSay("Researcher", "Closer. You can't hear me properly from there.", 5)
					End Select
				EndIf
				If d < 2.4 And IS16Aim(n\Collider, 2.4, 0.95) And (Not IAxFlag(e, "l")) Then
					IAxSetFlag(e, "l")
					IndevStress = Min(100, IndevStress + 8)
					IS16Tell("This close you see it: the ears under her hair are a fox's. Her eyes catch the light the wrong way.", 7)
				EndIf
				If d < 0.8 Then
					DeathMSG = "Subject D-9341 was found in Hallway 99 with a single penetrating wound to the abdomen. The liver was missing. Kennel staff report that the dogs barked for an hour afterwards."
					PlaySound_Strict(LoadTempSound("SFX\General\Slash" + Rand(1, 2) + ".ogg"))
					Kill()
				EndIf
			ElseIf safe And MsgTimer <= 0 And Rand(400) = 1 Then
				IAxSay("Researcher", "Why are you standing there? With them? Come out. Please.", 5)
			EndIf
			If safe And e\EventState3 > 70 * 60 Then
				e\EventState = 3
				e\EventState3 = 70 * 60
				IS13Gone(r, 0)
				IS16Tell("At the end of the hall she stops smiling, and when you look again there is nobody there.", 6)
			EndIf

		Case 2
			;the fox runs for the end of the hallway it came from, and is not there any more
			e\EventState3 = e\EventState3 - FPSfactor
			fz = 1200
			If IAxFlag(e, "s") Then fz = -1200
			IS10Walk(fox, 0, fz, 9.0)
			PositionEntity(fox, EntityX(fox), Abs(Sin(t * 900)) * 12, EntityZ(fox))
			If e\EventState3 <= 0 Then
				HideEntity(fox)
				e\EventState = 3
				e\EventState3 = 70 * 90
			EndIf
	End Select
End Function

;=====================================================================
; room2gameshow - SCP-024
;   EventState  0 not entered, 1 STAY or LEAVE, 2 round one (the floor), 3 round two (the clock),
;               4 round three (TAKE IT / RISK IT), 5 won, 6 declined, 7 lost
;   EventState2 the lift      EventState3 the round's clock
;   numbers: <P> the tile pattern (12 bits, 1 = safe), <B> buzzers so far, <X> strikes
;   flags: k a tape in the mailbox, t tape taken, h the barrier has spoken, o you have been out on the course
;=====================================================================

Function IS10Tiles(e.Events, showing%)
	Local r.Rooms = e\room, i%, m%, pat% = IS10Num(e, "P")
	For i = 0 To 11
		m = r\Objects[S10_GS_TILE + i]
		If showing Then
			ShowEntity(m)
			If pat And (1 Shl i) Then
				EntityColor(m, 230, 236, 255)
			Else
				EntityColor(m, 255, 30, 30)
			EndIf
		Else
			HideEntity(m)
		EndIf
	Next
End Function

Function IS10Strike(e.Events, why$)
	IS10SetNum(e, "X", IS10Num(e, "X") + 1)
	PlaySound_Strict(LoadTempSound("SFX\Indev\buzzer.wav"))
	Injuries = Injuries + 0.35
	CameraShake = 3.0
	IAxSay("Announcer", why + " That's strike " + IS10Num(e, "X") + "!", 5)
End Function

Function IS10Guardian(e.Events, k%)
	Local r.Rooms = e\room, m% = r\Objects[S10_GS_SHADE + k]
	TFormVector(0, 0, -0.9, Collider, 0)
	PositionEntity(m, EntityX(Collider, True) + TFormedX(), EntityY(Collider, True) - 0.3, EntityZ(Collider, True) + TFormedZ(), True)
	RotateEntity(m, 0, EntityYaw(Collider, True), 0, True)
	ShowEntity(m)
End Function

Function IS10Outside(e.Events)
	Local r.Rooms = e\room, i%
	BlinkTimer = -10
	PositionEntity(Collider, EntityX(r\Objects[S10_GS_OUTSIDE], True), EntityY(r\Objects[S10_GS_OUTSIDE], True) + 0.4, EntityZ(r\Objects[S10_GS_OUTSIDE], True))
	ResetEntity(Collider)
	r\RoomDoors[S10_GS_D_STAGE]\open = False
	r\RoomDoors[S10_GS_D_STAGE]\locked = True
	IS10Tiles(e, False)
	For i = 0 To 1
		HideEntity(r\Objects[S10_GS_SHADE + i])
	Next
End Function

Function UpdateS10GameShow(e.Events)
	Local r.Rooms = e\room
	Local door.Doors = r\RoomDoors[S10_GS_D_STAGE]
	Local lx#, ly#, lz#, onstage%, i%, pat%, gx#, gz#, sz#, col%, row%, q$ = Chr(34), prev#, cnt%

	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	IAxLocal(r)
	lx = TFormedX() : ly = TFormedY() : lz = TFormedZ()
	onstage = (lx > 290.0 And ly < 500.0)

	;---- the mailbox by the entrance
	If IS10Press(r\Objects[S10_GS_MAILBOX], 1.2) Then
		If IAxFlag(e, "k") And (Not IAxFlag(e, "t")) Then
			IAxSetFlag(e, "t")
			IS16Give("doc024b", r\Objects[S10_GS_MAILBOX])
			IS16Tell("A VHS tape in a plain case. GAME 4,117 - ONE PLAYER. Nobody put it there.", 7)
		Else
			IS16Tell("The mailbox is empty. It smells faintly of popcorn.", 4)
		EndIf
	EndIf

	Select e\EventState
		Case 0
			If onstage Then
				e\EventState = 1
				door\open = False
				door\locked = True
				PlaySound_Strict(LoadTempSound("SFX\Indev\jingle.wav"))
				IAxSay("Announcer", "WELCOME, contestant! Fabulous prizes await! But be warned - losers never leave. Will you STAY, or LEAVE?", 10)
			EndIf

		Case 1
			door\locked = True
			If IS10Press(r\Objects[S10_GS_BLEAVE], 1.4) Then
				e\EventState = 6
				IAxSay("Announcer", "Oh, what a shame! Maybe next time! There won't be a next time.", 6)
				IS10Outside(e)
			ElseIf IS10Press(r\Objects[S10_GS_BSTAY], 1.4) Then
				e\EventState = 2
				e\EventState3 = 70 * 4
				IS10SetNum(e, "B", 0)
				IS10SetNum(e, "X", 0)
				PlaySound_Strict(LoadTempSound("SFX\Indev\applause.wav"))
				IAxSay("Announcer", "ROUND ONE! When the buzzer sounds, be standing on a WHITE square! Off you go!", 7)
			EndIf

		Case 2
			;round one: the floor
			door\locked = True
			prev = e\EventState3
			e\EventState3 = e\EventState3 - FPSfactor
			If prev >= 70 * 4 - FPSfactor * 1.5 Then
				pat = 0
				While True
					pat = Rand(0, 4095)
					cnt = 0
					For i = 0 To 11
						If pat And (1 Shl i) Then cnt = cnt + 1
					Next
					If cnt >= 4 And cnt <= 7 Then Exit
				Wend
				IS10SetNum(e, "P", pat)
				IS10Tiles(e, True)
			EndIf
			If e\EventState3 <= 0 Then
				gx = EntityX(r\Objects[S10_GS_GRID]) : gz = EntityZ(r\Objects[S10_GS_GRID])
				sz = (EntityX(r\Objects[S10_GS_GRID2]) - gx) / 3.0
				col = Floor((lx - gx) / sz) : row = Floor((lz - gz) / sz)
				If col < 0 Or col > 2 Or row < 0 Or row > 3 Then
					IS10Strike(e, "Off the board!")
				ElseIf (IS10Num(e, "P") And (1 Shl (row * 3 + col))) = 0 Then
					IS10Strike(e, "RED! Ooh, that's got to sting.")
				Else
					PlaySound_Strict(LoadTempSound("SFX\Indev\ding.wav"))
				EndIf
				IS10SetNum(e, "B", IS10Num(e, "B") + 1)
				e\EventState3 = 70 * 4
				If IS10Num(e, "B") >= 4 And IS10Num(e, "X") < 3 Then
					IS10Tiles(e, False)
					e\EventState = 3
					e\EventState3 = 70 * 16
					PlaySound_Strict(LoadTempSound("SFX\Indev\applause.wav"))
					IAxSay("Announcer", "ROUND TWO! Beat the clock! Get to the prize podium in fifteen seconds! GO GO GO!", 7)
				EndIf
			EndIf

		Case 3
			;round two: the clock
			door\locked = True
			e\EventState3 = e\EventState3 - FPSfactor
			If Rand(90) = 1 Then LightBlink = 0.6
			If lz > 540.0 And lx > 540.0 Then
				e\EventState = 4
				PlaySound_Strict(LoadTempSound("SFX\Indev\ding.wav"))
				PlaySound_Strict(LoadTempSound("SFX\Indev\applause.wav"))
				IAxSay("Announcer", "You made it! Now: TAKE IT - your prize, right now - or RISK IT for the GRAND PRIZE?", 9)
			ElseIf e\EventState3 <= 0 Then
				IS10Strike(e, "TIME! But we're feeling generous.")
				e\EventState = 4
			EndIf

		Case 4
			door\locked = True
			If IS10Press(r\Objects[S10_GS_BTAKE], 1.4) Then
				e\EventState = 5
				IAxSetFlag(e, "k")
				PlaySound_Strict(LoadTempSound("SFX\Indev\applause.wav"))
				IAxSay("Announcer", "A WINNER! Enjoy your prize! And don't come back - you can't.", 7)
				IS10Outside(e)
				IS16Give("finefirstaid", r\Objects[S10_GS_OUTSIDE])
				IS16Give("18vbat", r\Objects[S10_GS_OUTSIDE])
			ElseIf IS10Press(r\Objects[S10_GS_BRISK], 1.4) Then
				If Rand(2) = 1 Then
					e\EventState = 5
					IAxSetFlag(e, "k")
					PlaySound_Strict(LoadTempSound("SFX\Indev\jingle.wav"))
					IAxSay("Announcer", "THE GRAND PRIZE! The crowd goes WILD!", 7)
					IS10Outside(e)
					IS16Give("key5", r\Objects[S10_GS_OUTSIDE])
					IS16Give("veryfinefirstaid", r\Objects[S10_GS_OUTSIDE])
				Else
					e\EventState = 7
					e\EventState3 = 70 * 2
					IAxSetFlag(e, "k")
					PlaySound_Strict(LoadTempSound("SFX\Indev\buzzer.wav"))
					IAxSay("Announcer", "Ohhh, so close! I'm sorry, contestant. Guardians?", 6)
					IS10Guardian(e, 0)
				EndIf
			EndIf

		Case 5, 6
			;played (or refused): the barrier
			door\open = False
			door\locked = True
			If EntityDistance(Collider, door\obj) < 1.4 And (Not IAxFlag(e, "h")) Then
				IAxSetFlag(e, "h")
				IS16Tell("Something you can't see stops your hand an inch from the door. You have had your turn.", 6)
			EndIf

		Case 7
			e\EventState3 = e\EventState3 - FPSfactor
			IS10Guardian(e, 1)
			If e\EventState3 <= 0 Then
				DeathMSG = "Subject D-9341 entered SCP-024 and did not come out. The tape found in the mailbox afterwards shows a full studio audience cheering as two large shapes close in."
				Kill()
			EndIf
	End Select

	;---- the rules (rounds one and two): once you are out on the course, no going back to the start
	If (e\EventState = 2 Or e\EventState = 3) And lx > 540.0 Then IAxSetFlag(e, "o")
	If (e\EventState = 2 Or e\EventState = 3) And lx < 420.0 And onstage And IAxFlag(e, "o") Then
		IS10Guardian(e, 0)
		If IS10Num(e, "X") >= 2 Then
			e\EventState = 7
			e\EventState3 = 70 * 1.5
			IAxSay("Announcer", "Breaking the rules AGAIN? Guardians!", 5)
		Else
			IS10Strike(e, "No going back, contestant!")
			TFormPoint(560, EntityY(r\Objects[S10_GS_STAGEIN]), lz, r\obj, 0)
			PositionEntity(Collider, TFormedX(), EntityY(Collider), TFormedZ())
			ResetEntity(Collider)
			IS16Tell("Something huge and dark is behind you, and then you are back on the course. It stays where it was, watching.", 6)
		EndIf
	EndIf
	If (e\EventState >= 2 And e\EventState <= 4) And IS10Num(e, "X") >= 3 Then
		e\EventState = 7
		e\EventState3 = 70 * 2
		IS10Tiles(e, False)
		IAxSay("Announcer", "Three strikes! Oh, I'm so sorry. Guardians?", 5)
		IS10Guardian(e, 0)
	EndIf
End Function

;=====================================================================
; room2diner - SCP-4258
;   EventState  which view the windows show (0 here, 1-4 elsewhere)   EventState2 the jukebox (time left)
;   EventState3 time until somebody leaves (and the view changes)
;   flags: n placed, v batteries drained this visit, i first time in, c coffee this visit, p pie;
;          count k: visits.  NPC[0] Freddy, NPC[1..3] customers
;=====================================================================

Function IS10View(e.Events, v%)
	Local r.Rooms = e\room, i%
	Local tex% = LoadTexture_Strict("GFX\map\indev_view" + v + ".png")
	For i = 0 To 3
		EntityTexture(GetChild(r\Objects[S10_DIN_WIN0 + i], 1), tex)
	Next
	FreeTexture(tex)
	e\EventState = v
End Function

Function UpdateS10Diner(e.Events)
	Local r.Rooms = e\room
	Local i%, n.NPCs, d#, drained%, it.Items, inside%, v%

	If e\EventState2 > 0 Then
		e\EventState2 = Max(0, e\EventState2 - FPSfactor)
		If e\EventState2 = 0 Then IS16Hush(e)
	EndIf
	If PlayerRoom <> r Then
		IS13Drop(e, "v")
		IS13Drop(e, "c")
		IS16Hush(e)
		Return
	EndIf
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S10_DIN_FRED, 180)
		For i = 0 To 2
			r\NPC[i + 1] = IS16Person(r, S10_DIN_PAT0 + i, 90 * i)
		Next
		e\EventState3 = 70 * 70
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_freddy.jpg")
	IAxSkin(r\NPC[1], "GFX\npcs\indev_patron1.jpg")
	IAxSkin(r\NPC[2], "GFX\npcs\indev_patron2.jpg")
	IAxSkin(r\NPC[3], "GFX\npcs\indev_resident.jpg")

	IAxLocal(r)
	inside = (TFormedX() > 262.0)
	If Not inside Then Return

	;---- at the door: every battery goes flat
	If Not IAxFlag(e, "v") Then
		IAxSetFlag(e, "v")
		e\EventStr = e\EventStr + "k"
		drained = False
		For i = 0 To MaxItemAmount - 1
			If Inventory(i) <> Null Then
				Select Inventory(i)\itemtemplate\name
					Case "radio", "18vradio", "fineradio", "veryfineradio", "snav", "snav300", "snav310", "snavulti", "nvgoggles", "finenvgoggles", "supernv"
						If Inventory(i)\state > 0 Then
							Inventory(i)\state = 0
							drained = True
						EndIf
				End Select
			EndIf
		Next
		If Not IAxFlag(e, "i") Then
			IAxSetFlag(e, "i")
			IS10View(e, 0)
			IS16Tell("A bell over the door. Every window shows a grey corridor with strip lights - the one you just came in from.", 8)
		ElseIf drained Then
			IS16Tell("Everything you carry with a battery goes dead at once. " + Chr(34) + "Privacy of our patrons," + Chr(34) + " says the man behind the counter.", 8)
		EndIf
	EndIf

	IndevRelieveStress(0.012 * FPSfactor)

	;---- Freddy
	n = r\NPC[0]
	If n <> Null Then
		If EntityDistance(n\Collider, Collider) < 5.0 Then IAxFace(n, Collider)
		If IndevAimedAt(n\obj, n\Collider, 2.2) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				If Not IAxFlag(e, "c") Then
					IAxSetFlag(e, "c")
					Stamina = 100
					StaminaEffect = 0.7 : StaminaEffectTimer = 90
					IndevRelieveStress(20)
					IAxSay("Freddy", "Coffee, on the house. Everybody's first cup is. Sit anywhere you like.", 6)
				ElseIf IS13Count(e, "k") >= 2 And (Not IAxFlag(e, "p")) Then
					IAxSetFlag(e, "p")
					Injuries = Max(0, Injuries - 0.8)
					IAxSay("Freddy", "You came back. Cherry pie, then. Best in eleven realities, they tell me.", 6)
				Else
					Select Rand(4)
						Case 1
							IAxSay("Freddy", "Windows show where the last fella came from. Don't read too much into it.", 6)
						Case 2
							IAxSay("Freddy", "Nobody takes pictures in here. Batteries just don't like the place.", 5)
						Case 3
							IAxSay("Freddy", "You look like you've had a night. Everybody who comes in from that door does.", 6)
						Case 4
							IAxSay("Freddy", "Come back any time. If you can find the door again, you're welcome.", 5)
					End Select
				EndIf
			EndIf
		EndIf
	EndIf

	;---- the customers
	For i = 1 To 3
		n = r\NPC[i]
		If n <> Null Then
			d = EntityDistance(n\Collider, Collider)
			If d < 4.0 Then IAxFace(n, Collider)
			If d < 2.0 And MsgTimer <= 0 And Rand(500) = 1 Then
				Select i
					Case 1
						IAxSay("Customer", "Every reality has a Freddy's. Only this one has the cherry pie.", 6)
					Case 2
						IAxSay("Customer", "Back home the sky is under us. You stop noticing after a while.", 6)
					Case 3
						IAxSay("Customer", "Don't bother with a camera. It's already dead, isn't it?", 5)
				End Select
			EndIf
		EndIf
	Next

	;---- somebody leaves; the windows follow them home
	e\EventState3 = e\EventState3 - FPSfactor
	If e\EventState3 <= 0 Then
		e\EventState3 = 70 * Rand(60, 90)
		v = Rand(1, 4)
		If v = e\EventState Then v = (v Mod 4) + 1
		IS10View(e, v)
		IS10Sound("SFX\Indev\doorbell.wav", r\Objects[S10_DIN_JUKE], 10.0, 0.8)
		Select v
			Case 1
				IS16Tell("The bell over the door. Outside the windows now: a desert highway at sundown.", 6)
			Case 2
				IS16Tell("The bell. The windows show a city in the rain, every light a colour you don't have a name for.", 6)
			Case 3
				IS16Tell("The bell. Two suns over a violet plain. The customer at the counter waves at it.", 6)
			Case 4
				IS16Tell("The bell. The windows go black, then fill with stars. Freddy keeps drying the same cup.", 6)
		End Select
	EndIf

	;---- the jukebox, the shower
	If IS10Press(r\Objects[S10_DIN_JUKE], 1.4) Then
		If e\EventState2 > 0 Then
			IS16Tell("It's still playing.", 3)
		Else
			e\EventState2 = 70 * 45
			IS10Load(e, "SFX\Indev\jukebox.wav")
			IndevRelieveStress(10)
			IS16Tell("You press B-7. Something with a walking bass and a lot of saxophone.", 5)
		EndIf
	EndIf
	If e\EventState2 > 0 And e\Sound <> 0 Then e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, r\Objects[S10_DIN_JUKE], 12.0, 0.8)
	If IS10Press(r\Objects[S10_DIN_SHOWER], 1.4) Then
		IndevRelieveStress(5)
		IS16Tell("Lukewarm water. The sign says it is for anything that followed you in from somewhere else.", 6)
	EndIf
End Function

;=====================================================================
; room2sheet - SCP-6096
;   EventState  0 sitting, 1 walking to the Class-D in Holding B, 2 walking to you, 3 gone under the fan,
;               4 the Class-D is under the sheet, 5 sitting again (cooldown)
;   EventState2 how long you have been near it (it gets up after a while)   EventState3 time in the state
;   numbers: <W> which leg of its walk it is on.  flags: n placed, g the Class-D is gone, h you held the
;            door, f the fan is down, p Symanski has hold of you, s he gave you the notice, k he gave you the key;
;            count b: drinks.  NPC[0] Symanski, NPC[1] the Class-D
;=====================================================================

Function IS10SheetHome(e.Events)
	Local r.Rooms = e\room, m% = r\Objects[S10_SH6_SHEETM]
	PositionEntity(m, EntityX(r\Objects[S10_SH6_SIT]), 0, EntityZ(r\Objects[S10_SH6_SIT]))
	RotateEntity(m, 0, 0, 0)
	ScaleEntity(m, 1, 0.62, 1)
	IS16Hush(e)
	IS13Drop(e, "p")
	e\EventState = 5
	e\EventState3 = 70 * 150
	e\EventState2 = 0
	If e\Sound <> 0 Then
		FreeSound_Strict(e\Sound)
		e\Sound = 0
	EndIf
End Function

Function UpdateS10Sheet(e.Events)
	Local r.Rooms = e\room
	Local sheet% = r\Objects[S10_SH6_SHEETM], lvr% = r\Objects[S10_SH6_HOIST + 1], fan% = r\Objects[S10_SH6_FAN0]
	Local hold.Doors = r\RoomDoors[S10_SH6_D_HOLD], cham.Doors = r\RoomDoors[S10_SH6_D_CHAMBER]
	Local n.NPCs, d#, lx#, lz#, w%, tx#, tz#, left#, up%, dx#, dz#, q$ = Chr(34)

	hold\locked = True
	If e\EventState = 5 Then
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then e\EventState = 0
	EndIf
	If PlayerRoom <> r Then
		If e\EventState = 1 Or e\EventState = 2 Then
			e\EventState3 = e\EventState3 + FPSfactor
			If e\EventState3 > 70 * 50 Then
				;somebody else held the door, or it chose somebody else
				If e\EventState = 1 Then
					IAxSetFlag(e, "g")
					IS13Gone(r, 1)
				EndIf
				IS10SheetHome(e)
			EndIf
		EndIf
		If e\EventState = 4 Then
			IAxSetFlag(e, "g")
			IS13Gone(r, 1)
			IS10SheetHome(e)
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S10_SH6_ZETA, 90)
		r\NPC[1] = IS16Person(r, S10_SH6_DCLASS, 90)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_zeta.jpg")
	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()

	;---- the Class-D in Holding B
	n = r\NPC[1]
	If n <> Null And e\EventState <> 4 Then
		If EntityDistance(n\Collider, Collider) < 6.0 Then IAxFace(n, Collider)
		If e\EventState = 1 And MsgTimer <= 0 And Rand(300) = 1 Then IAxSay("Class-D", "Is it moving? Tell me it's not moving. TELL ME!", 5)
	EndIf

	;---- Symanski
	n = r\NPC[0]
	If n <> Null And e\EventState <> 2 Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If IndevAimedAt(n\obj, n\Collider, 1.8) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				If Not IAxFlag(e, "s") Then
					IAxSetFlag(e, "s")
					IS16Give("doc6096b", n\Collider)
					IAxSay("Symanski", "New face. Here - read that. Then have a drink. The booze is under the sink.", 6)
				ElseIf e\EventState = 3 Then
					IAxSay("Symanski", "Sheer coincidence. That's all it ever needed. Sheer bloody coincidence.", 6)
				Else
					Select Rand(3)
						Case 1
							IAxSay("Symanski", "Can't hurt it. Can't try. Can't even want to for long. You'll see.", 6)
						Case 2
							IAxSay("Symanski", "If it ever picks you, kid, I'll be the one holding you down. Sorry in advance.", 6)
						Case 3
							IAxSay("Symanski", "Hotel room. We call it a containment chamber. Nobody laughs any more.", 6)
					End Select
				EndIf
			EndIf
		EndIf
	EndIf

	;---- the booze, the sheet, the lever
	If IS10Press(r\Objects[S10_SH6_SINK], 1.3) Then
		If IS13Count(e, "b") >= 3 Then
			IS16Tell("The bottle is empty. Somebody will have put a new one there by tomorrow.", 5)
		Else
			e\EventStr = e\EventStr + "b"
			IndevRelieveStress(12)
			BlurTimer = BlurTimer + 300
			IS16Tell("Under the sink: a bottle with no label. It burns all the way down.", 5)
		EndIf
	EndIf
	If e\EventState <> 3 And e\EventState <> 2 And IS16Click(sheet, sheet, 1.6) Then
		IS16Tell("You reach for the sheet. Your hand will not close on it. You do not even want it to.", 6)
	EndIf
	up = UpdateLever(lvr)
	If (Not up) And (Not IAxFlag(e, "f")) Then
		If e\EventState = 2 Then
			;the target can act. Only the target.
			IAxSetFlag(e, "f")
			PositionEntity(fan, EntityX(fan), 30, EntityZ(fan))
			PlaySound_Strict(LoadTempSound("SFX\General\GlassBreak.ogg"))
			CameraShake = 3.0
			dx = EntityX(sheet) - EntityX(r\Objects[S10_SH6_FANSPOT])
			dz = EntityZ(sheet) - EntityZ(r\Objects[S10_SH6_FANSPOT])
			If Sqr(dx * dx + dz * dz) < 130.0 Then
				e\EventState = 3
				ScaleEntity(sheet, 1.2, 0.12, 1.2)
				PositionEntity(sheet, EntityX(fan), 0, EntityZ(fan))
				IS16Hush(e)
				IS13Drop(e, "p")
				IndevRelieveStress(40)
				IS16Tell("The fan comes down on it like a hammer. The sheet goes flat, and stays flat, and nothing under it moves.", 8)
				IAxSay("Symanski", "...You did it. Sheer coincidence. That's all it ever needed.", 7)
				If r\NPC[0] <> Null Then
					r\NPC[0]\State = 0
					If Not IAxFlag(e, "k") Then
						IAxSetFlag(e, "k")
						IS16Give("key4", r\NPC[0]\Collider)
					EndIf
				EndIf
			Else
				IS16Tell("The fan crashes down a metre from it. It doesn't even turn its head. It just keeps coming.", 6)
			EndIf
		Else
			RotateEntity(lvr, 80, EntityYaw(lvr), 0)
			IS16Tell("Your hand stops on the lever. You can't make yourself pull it. You can't even want to.", 6)
		EndIf
	EndIf

	Select e\EventState
		Case 0
			;it sits facing the TV; after a while near it, it gets up
			e\EventState2 = e\EventState2 + FPSfactor
			If e\EventState2 > 70 * 40 Then
				e\EventState2 = 0
				ScaleEntity(sheet, 1, 1, 1)
				IS10SetNum(e, "W", 0)
				e\EventState3 = 0
				If (Not IAxFlag(e, "g")) And Rand(10) <= 7 Then
					e\EventState = 1
					IndevStress = Min(100, IndevStress + 15)
					IS16Tell("It stands up. And you know: D-5531, in Holding B across the corridor. You know it like your own name. You have to help it get to him.", 9)
				Else
					e\EventState = 2
					IndevStress = Min(100, IndevStress + 30)
					IS16Tell("It stands up, and you know who it wants the way you know your own name. It's you. Only you can act against it now.", 9)
				EndIf
			EndIf

		Case 1
			;to Holding B, and you will hold the door
			w = IS10Num(e, "W")
			Select w
				Case 0
					tx = EntityX(r\Objects[S10_SH6_P1]) : tz = EntityZ(r\Objects[S10_SH6_P1])
				Case 1
					tx = EntityX(r\Objects[S10_SH6_P2]) : tz = EntityZ(r\Objects[S10_SH6_P2])
				Case 2
					tx = EntityX(r\Objects[S10_SH6_P3]) : tz = EntityZ(r\Objects[S10_SH6_P3])
				Default
					tx = EntityX(r\Objects[S10_SH6_DCLASS]) : tz = EntityZ(r\Objects[S10_SH6_DCLASS])
			End Select
			cham\open = True
			If w = 2 And (Not hold\open) Then
				left = 999.0
			Else
				left = IS10Walk(sheet, tx, tz, 2.0)
			EndIf
			If left < 8.0 Then IS10SetNum(e, "W", w + 1)
			;the compulsion: towards the button of Holding B
			If (Not hold\open) And EntityDistance(Collider, sheet) < 9.0 Then
				IS10Pull(hold\obj, 0.007, 30.0)
				If EntityDistance(Collider, hold\obj) < 1.2 Then
					hold\locked = False
					hold\open = True
					IAxSetFlag(e, "h")
					IndevStress = Min(100, IndevStress + 15)
					PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
					IS16Tell("Your hand is on the button. You do not remember deciding to put it there.", 7)
				EndIf
			EndIf
			If hold\open Then hold\locked = False
			If w >= 3 And left < 70.0 Then
				e\EventState = 4
				e\EventState3 = 70 * 30
				IS13Gone(r, 1)
				IS10Load(e, "SFX\Indev\muffle.wav")
				IS16Tell("It reaches him and he goes under the sheet, feet first. Under it, something fights.", 7)
			EndIf

		Case 2
			;to you. Symanski staggers after you to hold you still
			cham\open = True
			IAxLocal(r)
			If EntityX(sheet) < -190.0 And lx > -190.0 Then
				tx = EntityX(r\Objects[S10_SH6_P1]) : tz = EntityZ(r\Objects[S10_SH6_P1])
			Else
				tx = lx : tz = lz
			EndIf
			IS10Walk(sheet, tx, tz, 1.9)
			n = r\NPC[0]
			If n <> Null Then
				If IAxFlag(e, "p") Then
					n\State = 0
				Else
					IAxFace(n, Collider)
					n\State = 1 - (MilliSecs() / 900) Mod 2
					If EntityDistance(n\Collider, Collider) < 0.75 Then
						IAxSetFlag(e, "p")
						PositionEntity(r\Objects[S10_SH6_PIN], EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), True)
						IAxSay("Symanski", "Sorry, kid. I'm sorry. Stay still. It won't hurt for long.", 6)
					EndIf
				EndIf
			EndIf
			If IAxFlag(e, "p") Then
				PositionEntity(Collider, EntityX(r\Objects[S10_SH6_PIN], True), EntityY(Collider, True), EntityZ(r\Objects[S10_SH6_PIN], True), True)
			EndIf
			dx = EntityX(sheet) - lx : dz = EntityZ(sheet) - lz
			If Sqr(dx * dx + dz * dz) < 70.0 Then
				DeathMSG = "Subject D-9341 was drawn under SCP-6096 in Humanoid Chamber 6096. The struggle lasted thirty-four minutes. Commander Symanski has asked to be relieved of duty again."
				Kill()
			EndIf

		Case 4
			;under the sheet
			e\EventState3 = e\EventState3 - FPSfactor
			ScaleEntity(sheet, 1.2 + 0.08 * Sin(MilliSecs() * 1.3), 1.1 + 0.06 * Sin(MilliSecs() * 1.7), 1.2)
			If e\Sound <> 0 Then e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, sheet, 8.0, 0.9)
			If EntityInView(sheet, Camera) Then IndevStress = Min(100, IndevStress + 0.03 * FPSfactor)
			If e\EventState3 <= 0 Then
				IAxSetFlag(e, "g")
				IS10SheetHome(e)
				hold\open = False
				IS16Tell("It is over. The sheet folds itself flat around nothing, gets up, and walks back to watch the TV.", 7)
			EndIf
	End Select
End Function

;=====================================================================
; room2block15 - SCP-2701
;   EventState  0 quiet, 1 locked in (thirteen seconds), 2 gone, 3 back (what it left behind)
;   EventState3 time in the state.  flags: n placed, c read the form, t tore the page off;
;   count k: times in there.  NPC[0] the guard, NPC[1] the man in the open cell
;=====================================================================

Function UpdateS10Block15(e.Events)
	Local r.Rooms = e\room
	Local door.Doors = r\RoomDoors[S10_B15_D_C667], n.NPCs, lx#, prev#, trips%, q$ = Chr(34)

	;---- what it left behind goes wherever you go
	If e\EventState = 3 And KillTimer >= 0 Then
		e\EventState3 = e\EventState3 - FPSfactor
		IndevStress = Min(100, IndevStress + 0.01 * FPSfactor)
		If Rand(500) = 1 Then CameraShake = 1.5
		If MsgTimer <= 0 And Rand(1400) = 1 Then
			Select Rand(3)
				Case 1
					IS16Tell("For a moment the world goes quiet and you are back in there. You are not. You are not.", 6)
				Case 2
					IS16Tell("You catch yourself counting. You have no idea what you are counting.", 5)
				Case 3
					IS16Tell("The dark at the edge of the light feels very large.", 5)
			End Select
		EndIf
		If e\EventState3 <= 0 Then e\EventState = 0
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[S10_B15_GUARD], True), EntityY(r\Objects[S10_B15_GUARD], True) + 0.35, EntityZ(r\Objects[S10_B15_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True), 0)
		r\NPC[0] = n
		r\NPC[1] = IS16Body(r, S10_B15_PRIS, 90, 40)
	EndIf
	If r\NPC[1] <> Null Then IAxSkin(r\NPC[1], "GFX\npcs\indev_prisoner.jpg")
	n = r\NPC[0]
	If n <> Null Then
		n\State = 9
		If EntityDistance(n\Collider, Collider) < 2.6 And MsgTimer <= 0 And Rand(700) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Guard", "Cell 667. Don't go in. And if you go in, don't let anybody write your name down.", 7)
				Case 2
					IAxSay("Guard", "Him in the end cell came back last Tuesday. Release date said 1971. He's not said a word.", 7)
				Case 3
					IAxSay("Guard", "Tear the page off the clipboard if you like. Somebody always puts a new one on.", 6)
			End Select
		EndIf
	EndIf

	;---- the INTAKE form
	If IS10Press(r\Objects[S10_B15_CLIP], 1.2) Then
		If IAxFlag(e, "t") Then
			IS16Tell("The clip holds a blank page now. It stays blank.", 4)
		ElseIf Not IAxFlag(e, "c") Then
			IAxSetFlag(e, "c")
			IS16Tell("INTAKE. NAME / RELEASE DATE. 137 names; release dates out to the year 3399. The last line is empty, and the pen is warm.", 9)
		Else
			IAxSetFlag(e, "t")
			IndevRelieveStress(5)
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
			IS16Tell("You tear the page off and screw it up. The sheet under it is blank.", 6)
		EndIf
	EndIf

	IAxLocal(r)
	lx = TFormedX()
	Select e\EventState
		Case 0
			If lx > 340.0 And (Not IAxFlag(e, "t")) Then
				e\EventState = 1
				e\EventState3 = 70 * 13
				door\open = False
				door\locked = True
				IS10Sound("SFX\Indev\pen.wav", r\Objects[S10_B15_CLIP], 8.0, 1.0)
				IS10Load(e, "SFX\Indev\wind.wav")
				IS16Tell("The door slams. Outside, a pen scratches on paper. N-A-M-E. Then numbers.", 7)
			EndIf
			If e\EventState <> 1 Then door\locked = False

		Case 1
			prev = e\EventState3
			e\EventState3 = e\EventState3 - FPSfactor
			If e\Sound <> 0 Then e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, r\Objects[S10_B15_CELLIN], 6.0, Min(1.0, 1.0 - e\EventState3 / (70 * 13) + 0.2))
			If prev >= 70 * 6 And e\EventState3 < 70 * 6 Then IS16Tell("A wind with nowhere to go goes round and round the cell. Something under it, like breathing.", 6)
			If e\EventState3 <= 0 Then
				e\EventState = 2
				e\EventState3 = 70 * 24
				e\EventStr = e\EventStr + "k"
				IS16Hush(e)
				IS16Tell("Then nothing.", 3)
			EndIf

		Case 2
			;nothing: no light, no sound, no floor, no sleep
			prev = e\EventState3
			e\EventState3 = e\EventState3 - FPSfactor
			BlinkTimer = -10
			PositionEntity(Collider, EntityX(r\Objects[S10_B15_CELLIN], True), EntityY(Collider, True), EntityZ(r\Objects[S10_B15_CELLIN], True), True)
			trips = IS13Count(e, "k")
			IndevStress = Min(100, IndevStress + 0.035 * trips * FPSfactor)
			If prev >= 70 * 20 And e\EventState3 < 70 * 20 Then IS16Tell("Day 1. You can think. Thinking is all there is.", 4)
			If prev >= 70 * 15 And e\EventState3 < 70 * 15 Then IS16Tell("Day 9. You have counted to a million twice, to be sure.", 4)
			If prev >= 70 * 10 And e\EventState3 < 70 * 10 Then IS16Tell("Day 23. You are writing a letter, in your head, to whoever filled in the form.", 5)
			If prev >= 70 * 5 And e\EventState3 < 70 * 5 Then IS16Tell("Day 40. Somebody is talking. It is you. It has been you for a week.", 5)
			If e\EventState3 <= 0 Then
				If trips >= 3 Then
					DeathMSG = "Subject D-9341 was released from SCP-2701 after an activation event of under thirty seconds and found catatonic on the cell floor. Subject was terminated after 28 hours; there was nothing left to debrief."
					Kill()
					Return
				EndIf
				e\EventState = 3
				e\EventState3 = 70 * 120
				door\locked = False
				door\open = True
				BlurTimer = 1400
				CameraShake = 3.0
				IS16Tell("The door is open. It was fifteen seconds. Your number is on the INTAKE list, in handwriting that isn't yours.", 9)
			EndIf

		Case 3
			door\locked = False
	End Select

	If r\NPC[1] <> Null Then
		If IndevAimedAt(r\NPC[1]\obj, r\NPC[1]\Collider, 1.4) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				IS16Tell("He doesn't blink. His lips are moving: " + q + "how long was I in there. how long. how long." + q, 7)
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room2mailbox - SCP-1269
;   EventState  0 at the curb, 1 following you round the house, 2 the lights are out and it has stopped hiding
;   EventState3 time until it can move again / time left in the dark
;   numbers: <C> times it has moved, <M> where it is now (MS0..MS6)
;   flags: n placed, e the letter taken, u the second letter, s you have seen it where it is now;
;   NPC[0] the resident
;=====================================================================

Function IS10MailAt(e.Events, k%)
	Local r.Rooms = e\room, mb% = r\Objects[S10_MB_MBOX], at% = r\Objects[S10_MB_MS0 + k]
	PositionEntity(mb, EntityX(at), 0, EntityZ(at))
	IS10Look(r, mb)
	IS10SetNum(e, "M", k)
	IS13Drop(e, "s")
End Function

Function IS10MailHome(e.Events)
	Local r.Rooms = e\room
	IS10MailAt(e, 0)
	RotateEntity(r\Objects[S10_MB_MBOX], 0, 90, 0)
	SecondaryLightOn = 1.0
	e\EventState = 0
	e\EventState3 = 70 * 4
End Function

Function UpdateS10Mailbox(e.Events)
	Local r.Rooms = e\room
	Local mb% = r\Objects[S10_MB_MBOX], flag% = r\Objects[S10_MB_MFLAG]
	Local lx#, lz#, inhouse%, out%, i%, k%, cur%, best%, n.NPCs, d#, fx#, fz#, l#, q$ = Chr(34)

	If PlayerRoom <> r Then
		If e\EventState <> 0 Then IS10MailHome(e)
		Return
	EndIf
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S10_MB_RES, 180)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_resident.jpg")
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Resident", "It doesn't bother me. I'm not the occupant. I just live here.", 5)
				Case 2
					IAxSay("Resident", "If it starts turning up where you're looking, leave. That's what D-69124 didn't do.", 7)
				Case 3
					IAxSay("Resident", "She's asleep. She sleeps a lot. You would too.", 5)
			End Select
		EndIf
	EndIf

	;the flag: up while there is a letter in it
	If IAxFlag(e, "e") And e\EventState < 2 Then
		RotateEntity(flag, 0, 0, 0)
	Else
		RotateEntity(flag, -90, 0, 0)
	EndIf

	If IS16Click(mb, mb, 1.6) Then
		If Not IAxFlag(e, "e") Then
			IAxSetFlag(e, "e")
			IS16Give("doc1269b", mb)
			IS16Tell("An envelope with no address on it. The flag drops by itself as you take it out.", 6)
		Else
			IS16Tell("Empty. It is facing you.", 4)
		EndIf
	EndIf
	If IS10Press(r\Objects[S10_MB_KNOCK], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Door\WoodenDoorBudge.ogg"))
		Select Rand(3)
			Case 1
				IS16Tell("A woman's voice through the door: " + q + "Is it in the house again? Don't look at it. It doesn't like other people looking." + q, 8)
			Case 2
				IS16Tell("Through the door: " + q + "Please go. Every time someone comes in, it gets worse." + q, 6)
			Case 3
				IS16Tell("Through the door: " + q + "It writes to me. Every day now. I'm not opening this door." + q, 6)
		End Select
	EndIf

	IAxLocal(r)
	lx = TFormedX() : lz = TFormedZ()
	inhouse = (lx > 482.0 And Abs(lz) < 690.0)
	out = (lx < 256.0)

	Select e\EventState
		Case 0
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
			If inhouse Then
				e\EventState = 1
				e\EventState3 = 70 * 6
			EndIf

		Case 1
			If out Then
				IS10MailHome(e)
				IS16Tell("Out at the curb, the mailbox is where it always was.", 5)
				Return
			EndIf
			e\EventState3 = e\EventState3 - FPSfactor
			cur = IS10Num(e, "M")
			;seen where it is now
			d = EntityDistance(mb, Collider)
			If (Not IAxFlag(e, "s")) And EntityInView(mb, Camera) And d < 7.0 And (EntityVisible(Camera, mb) Or d < 3.2) Then
				IAxSetFlag(e, "s")
				IndevStress = Min(100, IndevStress + 6)
				IS10Sound("SFX\SCP\173\StoneDrag.ogg", mb, 6.0, 0.35)
				Select cur
					Case 1
						IS16Tell("Through the living-room window, on the lawn: the mailbox. Facing in.", 5)
					Case 2
						IS16Tell("Under the shower curtain, where feet would be: a white post.", 5)
					Case 3
						IS16Tell("In the kitchen doorway, half behind the frame: the mailbox.", 5)
					Case 4
						IS16Tell("In the corner of the room, in the shadow. Facing you.", 5)
					Case 5
						IS16Tell("By the fridge. Its red flag is up.", 4)
					Case 6
						IS16Tell("Outside the kitchen window, on the grass. Facing in.", 5)
				End Select
			EndIf
			;it moves when nobody is looking
			If e\EventState3 <= 0 And (Not (EntityInView(mb, Camera) And EntityVisible(Camera, mb))) And EntityDistance(mb, Collider) > 1.6 Then
				best = -1
				k = Rand(1, 6)
				For i = 0 To 5
					k = (k Mod 6) + 1
					If k <> cur Then
						d = EntityDistance(r\Objects[S10_MB_MS0 + k], Collider)
						If d > 1.6 And d < 7.5 And (Not (EntityInView(r\Objects[S10_MB_MS0 + k], Camera) And EntityVisible(Camera, r\Objects[S10_MB_MS0 + k]))) Then
							best = k
							Exit
						EndIf
					EndIf
				Next
				If best > 0 Then
					IS10MailAt(e, best)
					IS10SetNum(e, "C", IS10Num(e, "C") + 1)
					e\EventState3 = 70 * Rand(5, 9)
					If IS10Num(e, "C") = 3 And (Not IAxFlag(e, "u")) Then
						IAxSetFlag(e, "u")
						IS16Give("doc1269c", Collider)
						IS16Tell("A letter is on the floor at your feet. It was not there a second ago.", 6)
					EndIf
					If IS10Num(e, "C") >= 6 Then
						;the dark: it stops hiding
						e\EventState = 2
						e\EventState3 = 70 * 10
						TFormVector(0, 0, 1, Camera, r\obj)
						fx = TFormedX() : fz = TFormedZ()
						l = Sqr(fx * fx + fz * fz)
						If l > 0.01 Then
							fx = fx / l : fz = fz / l
						EndIf
						PositionEntity(mb, lx + fx * 300, 0, lz + fz * 300)
						IS10Look(r, mb)
						PlaySound_Strict(LoadTempSound("SFX\Room\Blackout.ogg"))
						IndevStress = Min(100, IndevStress + 20)
						IS16Tell("The lights go. It is right in front of you, flag up, and it is not hiding any more. Get off the property. Now.", 8)
					EndIf
				EndIf
			EndIf

		Case 2
			SecondaryLightOn = CurveValue(0.1, SecondaryLightOn, 10.0)
			e\EventState3 = e\EventState3 - FPSfactor
			IS10Look(r, mb)
			If out Then
				IS10MailHome(e)
				IS10SetNum(e, "C", 2)
				IS16Tell("The lights come back. Out at the curb, the mailbox is where it always was. Its flag is down.", 7)
			ElseIf e\EventState3 <= 0 Then
				DeathMSG = "Subject D-9341 was found three weeks later in a garbage bag behind a closed restaurant 25 km from Site-[REDACTED], beside four mailboxes painted with words. The hands and lips were missing."
				Kill()
			EndIf
	End Select
End Function

;=====================================================================
; room2psych - SCP-482
;   EventState  how long you have worn it   EventState2 how long you have stood by the attendant (to undo it)
;   EventState3 how long Time Point Beta has run
;   numbers: <A> how long Alpha lasts, <S> your stress when you put it on.
;   flags: q warned, w wearing it, b Beta.  NPC[0] the attendant, NPC[1] the patient
;=====================================================================

Function UpdateS10Psych(e.Events)
	Local r.Rooms = e\room
	Local jk% = r\Objects[S10_PSY_JACKETM], n.NPCs, s#, q$ = Chr(34)

	;---- the jacket goes where you go
	If IAxFlag(e, "w") And KillTimer >= 0 Then
		e\EventState = e\EventState + FPSfactor
		IndevStress = 0
		Stamina = Min(Stamina, 60)
		If SelectedItem <> Null Then
			SelectedItem = Null
			If MsgTimer <= 0 Then IS16Tell("Your arms are strapped across your chest. You can't use anything.", 4)
		EndIf
		If e\EventState > IS10Num(e, "A") Then
			If Not IAxFlag(e, "b") Then
				IAxSetFlag(e, "b")
				e\EventState3 = 0
				CameraShake = 3.0
				IS16Tell("Something under the leather moves that is not your arm. You still feel fine. That is the worst part.", 8)
			EndIf
			e\EventState3 = e\EventState3 + FPSfactor
			s = IS10Num(e, "S") / 100.0
			Injuries = Injuries + (0.0005 + 0.0012 * s) * FPSfactor
			BlurTimer = Max(BlurTimer, 250)
			If Rand(400) = 1 Then CameraShake = 2.0
			DeathMSG = "Subject D-9341 was terminated in accordance with the containment procedures for SCP-482, having worn it past Time Point Beta. The changes were consistent with the subject's psychological profile. The jacket was recovered intact."
			If e\EventState3 > 70 * 60 Then Kill()
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If r\NPC[0] = Null Then
		r\NPC[0] = IS16Person(r, S10_PSY_ATT, 180)
		r\NPC[1] = IS16Person(r, S10_PSY_PAT, 0)
	EndIf
	IAxSkin(r\NPC[0], "GFX\npcs\indev_attendant.jpg")
	IAxSkin(r\NPC[1], "GFX\npcs\indev_patient.jpg")
	If r\NPC[1] <> Null Then
		RotateEntity(r\NPC[1]\Collider, 0, EntityYaw(r\NPC[1]\Collider) + Sin(MilliSecs() * 0.15) * 0.4, 0)
	EndIf

	n = r\NPC[0]
	If n <> Null Then
		If EntityDistance(n\Collider, Collider) < 4.0 Then IAxFace(n, Collider)
		If IAxFlag(e, "w") And EntityDistance(n\Collider, Collider) < 1.5 Then
			e\EventState2 = e\EventState2 + FPSfactor
			If e\EventState2 > 70 * 2 Then
				e\EventState2 = 0
				IS13Drop(e, "w")
				IS13Drop(e, "q")
				ShowEntity(jk)
				PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
				If IAxFlag(e, "b") Then
					IS13Drop(e, "b")
					IndevStress = Min(100, IS10Num(e, "S") + 20)
					IAxSay("Attendant", "Off. It's off. What it did stays. I'm sorry. I should have kept you here.", 7)
				Else
					IndevStress = Min(100, IS10Num(e, "S") + 15)
					BlurTimer = 600
					IAxSay("Attendant", "There. And here it all comes back - all at once. Breathe. That's normal.", 7)
				EndIf
			EndIf
		Else
			e\EventState2 = 0
			If EntityDistance(n\Collider, Collider) < 2.4 And MsgTimer <= 0 And Rand(600) = 1 Then
				If IAxFlag(e, "w") Then
					IAxSay("Attendant", "Come here and stand still so I can get the buckles. Before it's too late.", 6)
				Else
					Select Rand(3)
						Case 1
							IAxSay("Attendant", "It works. That's the trouble with it. Everybody feels wonderful.", 5)
						Case 2
							IAxSay("Attendant", "Two minutes, give or take. Then the changes start, and then it's protocol.", 6)
						Case 3
							IAxSay("Attendant", "You can't take it off yourself. Nobody in a straitjacket can. That's the point.", 6)
					End Select
				EndIf
			EndIf
		EndIf
	EndIf

	If (Not IAxFlag(e, "w")) And IS16Click(jk, jk, 1.6) Then
		If Not IAxFlag(e, "q") Then
			IAxSetFlag(e, "q")
			IS16Tell("SCP-482: black leather, buckles, a tag that says No Aserejena Powder. Click again to put it on.", 7)
		Else
			IAxSetFlag(e, "w")
			e\EventState = 0
			e\EventState3 = 0
			IS10SetNum(e, "A", 70 * Rand(90, 150))
			IS10SetNum(e, "S", Int(IndevStress))
			HideEntity(jk)
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
			IndevStress = 0
			IS16Tell("The attendant sighs and buckles you in. Within a minute the fear, the noise, all of it, is simply gone. Come back to him before it changes.", 9)
		EndIf
	EndIf

	If r\NPC[1] <> Null And IAxFlag(e, "w") Then
		If EntityDistance(r\NPC[1]\Collider, Collider) < 3.0 And MsgTimer <= 0 And Rand(500) = 1 Then
			IS16Tell("The patient stops rocking and watches the jacket. She is smiling.", 5)
		EndIf
	EndIf
End Function

;=====================================================================
; room2realchar - SCP-3325
;   EventState  0 loose, 1 eating, 2 locked in the glass chamber
;   EventState2 the lift      EventState3 time until it can bite again / eating time left
;   flags: m you are carrying meat, t meat on the floor, d it has spoken to you.  (the creature is in Objects)
;=====================================================================

Function UpdateS10RealChar(e.Events)
	Local r.Rooms = e\room
	Local c% = r\Objects[S10_RCI_CREC], model% = r\Objects[S10_RCI_CREM], jaw% = r\Objects[S10_RCI_CREJ], meat% = r\Objects[S10_RCI_MEATM]
	Local cham.Doors = r\RoomDoors[S10_RCI_D_CHAMBER]
	Local ly#, down%, tgt%, dx#, dz#, l#, sp#, q$ = Chr(34), fx#, fz#, t# = IS16Time(), ln$

	If e\EventState3 > 0 Then e\EventState3 = Max(0, e\EventState3 - FPSfactor)
	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	IAxLocal(r)
	ly = TFormedY()
	down = (ly < -300.0)

	;---- the meat
	If IS10Press(r\Objects[S10_RCI_MEAT], 1.4) Then
		If IAxFlag(e, "m") Or IAxFlag(e, "t") Then
			IS16Tell("One slab at a time.", 3)
		Else
			IAxSetFlag(e, "m")
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
			IS16Tell("You pull a slab of raw meat off the carcass. Click anywhere to throw it down.", 6)
		EndIf
	ElseIf IAxFlag(e, "m") And MouseHit1 And (Not InvOpen) Then
		MouseHit1 = False
		IS13Drop(e, "m")
		IAxSetFlag(e, "t")
		TFormVector(0, 0, 1, Camera, 0)
		fx = TFormedX() : fz = TFormedZ()
		l = Sqr(fx * fx + fz * fz)
		If l > 0.01 Then
			fx = fx / l : fz = fz / l
		EndIf
		PositionEntity(meat, EntityX(Collider, True) + fx * 0.9, EntityY(r\Objects[S10_RCI_CRE], True) + 0.03, EntityZ(Collider, True) + fz * 0.9, True)
		ShowEntity(meat)
		IS16Tell("You throw the meat down. It hits the tiles with a wet slap.", 4)
	EndIf

	;---- the panel by the chamber
	If IS10Press(r\Objects[S10_RCI_PANEL], 1.3) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		If e\EventState = 2 Then
			IS16Tell("LOCKED. It presses its face to the glass and smiles at you.", 5)
		ElseIf e\EventState = 1 And EntityDistance(meat, r\Objects[S10_RCI_CHSPOT]) < 1.3 Then
			e\EventState = 2
			cham\open = False
			cham\locked = True
			IS16Tell("The glass door slides shut on it. It finishes eating, then looks up at you, and goes on smiling.", 8)
		Else
			cham\open = Not cham\open
			If cham\open Then
				IS16Tell("The chamber door slides open.", 3)
			Else
				IS16Tell("The chamber door slides shut on nothing.", 3)
			EndIf
		EndIf
	EndIf
	If e\EventState = 2 Then cham\locked = True

	;---- the loose one
	Select e\EventState
		Case 0
			If IAxFlag(e, "t") Then
				tgt = meat
			ElseIf down Then
				tgt = Collider
			Else
				tgt = r\Objects[S10_RCI_CRE]
			EndIf
			dx = EntityX(tgt, True) - EntityX(c, True) : dz = EntityZ(tgt, True) - EntityZ(c, True)
			l = Sqr(dx * dx + dz * dz)
			sp = 0.011
			If tgt = r\Objects[S10_RCI_CRE] Then sp = 0.005
			If l > 0.4 Then
				RotateEntity(c, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(c), 8.0), 0)
				MoveEntity(c, 0, 0, sp * FPSfactor)
			EndIf
			TranslateEntity(c, 0, -0.02 * FPSfactor, 0)
			PositionEntity(model, 0, -0.2 + Abs(Sin(t * 400)) * 0.03, 0)
			RotateEntity(jaw, 12 + 12 * Sin(t * 500), 0, 0)
			If tgt = meat And l < 0.45 Then
				e\EventState = 1
				e\EventState3 = 70 * 25
			EndIf
			If tgt = Collider And EntityDistance(c, Collider) < 0.55 And e\EventState3 <= 0 Then
				e\EventState3 = 70 * 1.5
				Injuries = Injuries + 0.9
				CameraShake = 3.0
				BlurTimer = Max(BlurTimer, 300)
				PlaySound_Strict(LoadTempSound("SFX\General\Slash" + Rand(1, 2) + ".ogg"))
				DeathMSG = "Subject D-9341 was found on LG-1 of the Real Characters Industries facility, partly eaten. An SCP-3325-1b instance in the room was heard repeating " + q + "sharing is caring" + q + " until it was tranquillised."
				IS16Tell(q + "Who wants a HUG?" + q, 3)
				If Injuries > 4.0 Then Kill()
			EndIf

		Case 1
			;eating: it won't look up for anything
			RotateEntity(jaw, 20 + 20 * Sin(t * 1400), 0, 0)
			PositionEntity(model, 0, -0.2, 0)
			TranslateEntity(c, 0, -0.02 * FPSfactor, 0)
			If e\EventState3 <= 0 Then
				e\EventState = 0
				IS13Drop(e, "t")
				HideEntity(meat)
			EndIf

		Case 2
			;in the chamber: it walks the glass
			dx = EntityX(r\Objects[S10_RCI_CHSPOT], True) + Sin(t * 20) * 0.5 - EntityX(c, True)
			dz = EntityZ(r\Objects[S10_RCI_CHSPOT], True) + Cos(t * 20) * 0.3 - EntityZ(c, True)
			l = Sqr(dx * dx + dz * dz)
			If l > 0.1 Then
				RotateEntity(c, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(c), 8.0), 0)
				MoveEntity(c, 0, 0, 0.004 * FPSfactor)
			EndIf
			TranslateEntity(c, 0, -0.02 * FPSfactor, 0)
			HideEntity(meat)
			IS13Drop(e, "t")
			RotateEntity(jaw, 10 + 10 * Sin(t * 300), 0, 0)
	End Select

	;---- what it says (and what the vents say)
	If down And Rand(420) = 1 Then
		IS10Sound("SFX\Indev\puppet" + Rand(0, 2) + ".wav", c, 12.0, 0.9)
		If EntityDistance(c, Collider) < 8.0 And MsgTimer <= 0 Then
			Select Rand(5)
				Case 1
					ln = "Let's be REAL today!"
				Case 2
					ln = "Who wants a HUG?"
				Case 3
					ln = "Say it with ME!"
				Case 4
					ln = "Sharing is CARING!"
				Default
					ln = "Can you be BRAVE?"
			End Select
			IS16Tell("The orange thing: " + q + ln + q, 4)
		EndIf
	EndIf
	If down And Rand(1100) = 1 Then
		IS10Sound("SFX\Indev\puppet" + Rand(0, 2) + ".wav", r\Objects[S10_RCI_FAN0], 9.0, 0.35)
		If MsgTimer <= 0 Then IS16Tell("Something small giggles inside the vent, and scrabbles away.", 5)
	EndIf
End Function

;=====================================================================
; room2wait1440 - SCP-1440
;   EventState  how long you have been near him (falls off slowly when you keep away)
;   EventState2 how far things have gone (1 lights, 2 a crack, 3 a pipe, 4 the ceiling)
;   EventState3 the hand of cards (time left)
;   flags: n placed, g he has moved on, c cards played, w warned; count q: lines said.  NPC[0] SCP-1440
;=====================================================================

Function UpdateS10OldMan(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, near%, rate#, sec#, inroom%, q$ = Chr(34), dx#, dz#

	If PlayerRoom <> r Then
		If e\EventState2 >= 2 And (Not IAxFlag(e, "g")) Then
			;he does not wait to be thrown out
			IAxSetFlag(e, "g")
			IS13Gone(r, 0)
			IS16Give("doc1440b", r\Objects[S10_OLD_TABLE])
		EndIf
		e\EventState = Max(0, e\EventState - 0.5 * FPSfactor)
		Return
	EndIf
	If KillTimer < 0 Then Return

	IAxLocal(r)
	inroom = (TFormedX() < -256.0 And TFormedZ() < 60.0)

	If IAxFlag(e, "g") Then
		If IS10Press(r\Objects[S10_OLD_CARDS], 1.3) Then IS16Tell("He has gone. He left the cards. They are still warm.", 5)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S10_OLD_OLD, -90)
	EndIf
	n = r\NPC[0]
	If n = Null Then Return
	IAxSkin(n, "GFX\npcs\indev_oldman.jpg")
	If EntityDistance(n\Collider, Collider) < 6.0 Then IAxFace(n, Collider)

	;---- talk
	If IndevAimedAt(n\obj, n\Collider, 1.8) Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			e\EventStr = e\EventStr + "q"
			Select IS13Count(e, "q") Mod 5
				Case 1
					IAxSay("Old man", "You should not stay. Things break around me, and then the people near the things.", 7)
				Case 2
					IAxSay("Old man", "Sit, if you like. One hand of cards, and then you go. I always win, but I'm sorry about it.", 7)
				Case 3
					IAxSay("Old man", "They tried to hold me at Area-142. Ask them how that went. You can't, of course.", 6)
				Case 4
					IAxSay("Old man", "I asked one of yours to destroy me, once. She couldn't. Nobody can.", 6)
				Default
					IAxSay("Old man", "I don't choose where I go. Something does. I'm sorry it was here.", 6)
			End Select
		EndIf
	EndIf

	;---- one hand of cards
	If IS10Press(r\Objects[S10_OLD_CARDS], 1.3) Then
		If IAxFlag(e, "c") Then
			IS16Tell("He has put the cards away. " + q + "One hand. That was the bargain." + q, 5)
		ElseIf e\EventState3 > 0 Then
			IS16Tell("You are playing. The lights flicker each time he turns a card.", 4)
		Else
			e\EventState3 = 70 * 14
			IS16Tell("He deals two hands, face down, with hands that do not shake at all.", 6)
		EndIf
	EndIf
	If e\EventState3 > 0 Then
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			IAxSetFlag(e, "c")
			If Rand(2) = 1 Then
				Select Rand(4)
					Case 1
						IS16Give("finefirstaid", r\Objects[S10_OLD_TABLE])
					Case 2
						IS16Give("supereyedrops", r\Objects[S10_OLD_TABLE])
					Case 3
						IS16Give("18vbat", r\Objects[S10_OLD_TABLE])
					Default
						IS16Give("key4", r\Objects[S10_OLD_TABLE])
				End Select
				IAxSay("Old man", "You win. That has not happened in a while. Take it - nothing of mine is hurt by me.", 7)
			Else
				IAxSay("Old man", "I win. I always win. I'm sorry about it.", 5)
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[S10_OLD_CUP], 1.2) Then
		If e\EventState2 >= 2 Then
			IS16Tell("His small glass cup: the only glass in the room without a crack in it.", 5)
		Else
			IS16Tell("A small glass cup, clean and empty.", 4)
		EndIf
	EndIf

	;---- what happens to everything near him
	near = (inroom And EntityDistance(n\Collider, Collider) < 5.0)
	rate = 1.0
	If e\EventState3 > 0 Then rate = 2.0
	If near Then
		e\EventState = e\EventState + FPSfactor * rate
	Else
		e\EventState = Max(0, e\EventState - 0.5 * FPSfactor)
	EndIf
	sec = e\EventState / 70.0
	If sec > 12 And e\EventState2 < 1 Then
		e\EventState2 = 1
		LightBlink = 1.5
		IS16Tell("The lights stutter. He looks up at them, and then at you, apologetically.", 6)
	EndIf
	If sec > 24 And e\EventState2 < 2 Then
		e\EventState2 = 2
		LightBlink = 3.0
		ShowEntity(r\Objects[S10_OLD_CRACK])
		PlaySound_Strict(LoadTempSound("SFX\General\GlassBreak.ogg"))
		IS16Tell("The bulb bursts. A crack runs up the wall behind him, and the fan starts to wobble.", 6)
	EndIf
	If sec > 36 And e\EventState2 < 3 Then
		e\EventState2 = 3
		IS10Sound("SFX\General\Hiss.ogg", r\Objects[S10_OLD_PIPE], 10.0, 1.0)
		IS10Sound("SFX\Indev\creak.wav", r\Objects[S10_OLD_PIPE], 12.0, 1.0)
		CameraShake = 3.0
		dx = EntityX(Collider, True) - EntityX(r\Objects[S10_OLD_PIPE], True) : dz = EntityZ(Collider, True) - EntityZ(r\Objects[S10_OLD_PIPE], True)
		If Sqr(dx * dx + dz * dz) < 1.6 Then Injuries = Injuries + 0.4
		IS16Tell("A pipe splits overhead and scalding steam pours down. He doesn't move. It doesn't touch him.", 6)
	EndIf
	If sec > 42 And (Not IAxFlag(e, "w")) Then
		IAxSetFlag(e, "w")
		IS10Sound("SFX\Indev\creak.wav", n\Collider, 14.0, 1.0)
		IAxSay("Old man", "The ceiling. Go. Now. Please.", 4)
	EndIf
	If sec > 48 Then
		e\EventState2 = 4
		IAxSetFlag(e, "g")
		IS13Gone(r, 0)
		IS16Give("doc1440b", r\Objects[S10_OLD_TABLE])
		If inroom Then
			DeathMSG = "Subject D-9341 was recovered from Interview Room 142 after the ceiling collapsed. The only intact objects in the room were a pack of playing cards and a small glass cup. SCP-1440 has not been located."
			PlaySound_Strict(LoadTempSound("SFX\Room\TunnelBurst.ogg"))
			Kill()
		EndIf
	EndIf
End Function
