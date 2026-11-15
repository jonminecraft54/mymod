;=====================================================================
; SCP: Containment Breach - Indev: ten containment rooms, sixteen SCPs
;
;   room2siv       LCZ    Small Items Vault
;                         SCP-1045  the candle lantern: light it and it costs you your nerve
;                         SCP-1510  the helmet: binds your wounds, takes your wind and your calm
;                         SCP-1125  the answer die: Yes steadies, No winds, the third roll is one too many
;   room2bio       LCZ    Biological Holding
;                         SCP-1513  a potted pet to stroke, and the one nobody watered
;                         SCP-1515  five rodents in a wire enclosure (they are not interested in you)
;                         SCP-1517  a freezer left ajar: shut it before the shells thaw
;                         SCP-1519  the lamplighter: its cradle makes a battery every three minutes
;   room2origin    HCZ    SCP-1512  slime across the hall; hold the pencil to a worksheet to draw it back
;   room2purge     HCZ    SCP-1518  loose bubbles; FAN PURGE pins them in the foam for half a minute
;   room2review    EZ     SCP-1110  play the footage and whatever lies on the counter is robbed
;                         SCP-1250  a tape that says how near SCP-173 is (and lies one time in three)
;   room2lecture   EZ     SCP-1313  follow the board to the end and the answer is a bear
;   room2site41    Indev  SCP-1312  past the fence you are the anomaly: the black one contains you
;   room2cell49    Indev  SCP-1516  pass it one word card, take what it makes of the word
;   room2vault117  Indev  SCP-1511  a lift down to a fragment that is restful to listen to
;   room2bunker    Indev  SCP-1514  a lift down to an overdue inspection: touch the panel, do not hold on
;
;   IndevS16Data.bb is generated (Tools\roomkit\gen_s16.py): the S16_* slot constants, the
;   FillRoom table, the fan table and the event list. This file is everything else. No globals:
;   handles live in r\Objects[] / r\RoomDoors[] / r\NPC[], progress in the room's event
;   (EventState / EventState2 / EventState3 and one-letter flags in EventStr).
;=====================================================================

;---------------------------------------------------------------------
; helpers
;---------------------------------------------------------------------

Function IS16Door.Doors(r.Rooms, lx#, ly#, lz#, angle%, key%, locked%)
	Local d.Doors = CreateDoor(r\zone, r\x + lx * RoomScale, r\y + ly * RoomScale, r\z + lz * RoomScale, angle, r, False, False, key)
	d\AutoClose = False : d\open = False : d\locked = locked
	IndevButtonsToWall(d) ;out of the thick side-room walls (IndevAnnex.bb)
	Return d
End Function

;a model built in room units, standing where a pivot is
Function IS16Prop%(r.Rooms, file$, skin$, at%, yaw#)
	Local m% = LoadMesh_Strict(file)
	Local tex% = LoadTexture_Strict(skin)
	EntityTexture(m, tex)
	FreeTexture(tex)
	ScaleEntity(m, RoomScale, RoomScale, RoomScale)
	PositionEntity(m, EntityX(at, True), EntityY(at, True), EntityZ(at, True), True)
	EntityParent(m, r\obj)
	RotateEntity(m, 0, yaw, 0)
	Return m
End Function

;seconds, for things that drift or wag
Function IS16Time#()
	Return Float(MilliSecs() Mod 3600000) / 1000.0
End Function

;the player is within dist of a pivot and looking at it (tight = cosine of the allowed angle)
Function IS16Aim%(p%, dist#, tight#)
	If p = 0 Then Return False
	If EntityDistance(Camera, p) > dist Then Return False
	If InvOpen Or OtherOpen <> Null Or SelectedItem <> Null Or MenuOpen Then Return False
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dx# = EntityX(p, True) - EntityX(Camera, True)
	Local dy# = EntityY(p, True) - EntityY(Camera, True)
	Local dz# = EntityZ(p, True) - EntityZ(Camera, True)
	Local l# = Sqr(dx * dx + dy * dy + dz * dz)
	If l < 0.001 Then Return True
	Return ((fx * dx + fy * dy + fz * dz) / l > tight)
End Function

;aimed at a prop: shows the hand, True on the click
Function IS16Click%(ent%, pick%, dist#)
	If ent = 0 Or pick = 0 Then Return False
	If Not IndevAimedAt(ent, pick, dist) Then Return False
	DrawHandIcon = True
	If MouseHit1 Then
		MouseHit1 = False
		Return True
	EndIf
	Return False
End Function

Function IS16Tell(txt$, secs#)
	Msg = U39Typo(txt) ;SCP-586 swaps a word when you are near it (IndevU39.bb)
	MsgTimer = 70 * secs
End Function

Function IS16Person.NPCs(r.Rooms, slot%, yaw#)
	Local n.NPCs = CreateNPC(NPCtypeD, EntityX(r\Objects[slot], True), EntityY(r\Objects[slot], True) + 0.5, EntityZ(r\Objects[slot], True))
	n\State = 0
	RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + yaw, 0)
	Return n
End Function

Function IS16Body.NPCs(r.Rooms, slot%, yaw#, frame%)
	Local n.NPCs = IS16Person(r, slot, yaw)
	n\State = 3
	SetNPCFrame(n, frame)
	n\IsDead = True
	Return n
End Function

Function IS16Give(name$, at%)
	Local it.Items = CreateItem(name, EntityX(at, True), EntityY(at, True) + 0.05, EntityZ(at, True))
	EntityType(it\collider, HIT_ITEM)
	PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
End Function

Function IS16Flat(m%)
	RotateEntity(m, 0, EntityYaw(m, True), 0, True)
End Function

;---------------------------------------------------------------------
; the things only code can make (called at the end of IndevFillS16)
;---------------------------------------------------------------------

Function IndevS16Dress(r.Rooms)
	Local i%, m%, tex%, s%, at%
	Select r\RoomTemplate\Name
		Case "room2siv"
			;the flame SCP-1045 burns with
			at = r\Objects[S16_SIV_LANTERN]
			m = CreateSprite()
			EntityTexture(m, LightSpriteTex(0))
			EntityBlend(m, 3)
			EntityFX(m, 1 + 8)
			ScaleSprite(m, 0.1, 0.14)
			PositionEntity(m, EntityX(at, True), EntityY(at, True), EntityZ(at, True), True)
			EntityParent(m, r\obj)
			HideEntity(m)
			r\Objects[S16_SIV_GLOW] = m

		Case "room2bio"
			;SCP-1515: five in the enclosure
			at = r\Objects[S16_BIO_RODENTS]
			For i = 0 To 4
				m = IS16Prop(r, "GFX\npcs\scp1515.b3d", "GFX\npcs\indev_rodent.png", at, i * 77.0)
				PositionEntity(m, EntityX(at, True) + (i - 2) * 62.0 * RoomScale, EntityY(at, True), EntityZ(at, True) + ((i Mod 2) * 2 - 1) * 58.0 * RoomScale, True)
				r\Objects[S16_BIO_ROD + i] = m
			Next
			;SCP-1513: the one that was looked after, and the one that was not
			m = IS16Prop(r, "GFX\npcs\scp1513.b3d", "GFX\npcs\scp1513.png", r\Objects[S16_BIO_PET], -90)
			EntityPickMode(m, 2)
			r\Objects[S16_BIO_PETM] = m
			r\Objects[S16_BIO_FERALM] = IS16Prop(r, "GFX\npcs\scp1513b.b3d", "GFX\npcs\scp1513b.png", r\Objects[S16_BIO_FERAL0], 150)
			;the freezer door, hung on its hinge and left ajar
			m = CreateCube(r\Objects[S16_BIO_HINGE])
			ScaleEntity(m, 80.0 * RoomScale, 109.0 * RoomScale, 3.0 * RoomScale)
			PositionEntity(m, 80.0 * RoomScale, 0, 0)
			tex = LoadTexture_Strict("GFX\map\white.jpg")
			EntityTexture(m, tex)
			FreeTexture(tex)
			EntityPickMode(m, 2)
			RotateEntity(r\Objects[S16_BIO_HINGE], 0, 52, 0)
			r\Objects[S16_BIO_SLAB] = m

		Case "room2lecture"
			m = IS16Prop(r, "GFX\npcs\indev_bear.b3d", "GFX\npcs\indev_bear.png", r\Objects[S16_LEC_BEAR], 180)
			HideEntity(m)
			r\Objects[S16_LEC_BEARM] = m

		Case "room2origin"
			;the slime: one flat sheet across the hall, so it can draw back
			at = r\Objects[S16_ORI_SLIME]
			m = CreateMesh()
			s = CreateSurface(m)
			AddVertex(s, -352, 0, -300, 0, 0)
			AddVertex(s, 352, 0, -300, 2, 0)
			AddVertex(s, 352, 0, 300, 2, 2)
			AddVertex(s, -352, 0, 300, 0, 2)
			AddTriangle(s, 0, 2, 1)
			AddTriangle(s, 0, 3, 2)
			tex = LoadTexture_Strict("GFX\map\indev_slime.png", 1 + 2)
			EntityTexture(m, tex)
			FreeTexture(tex)
			EntityFX(m, 16)
			ScaleEntity(m, RoomScale, RoomScale, RoomScale)
			PositionEntity(m, EntityX(at, True), EntityY(at, True), EntityZ(at, True), True)
			EntityParent(m, r\obj)
			EntityAlpha(m, 0.85)
			r\Objects[S16_ORI_SLIMEM] = m

		Case "room2purge"
			tex = LoadTexture_Strict("GFX\map\indev_bubble.png", 1 + 2)
			For i = 0 To 6
				m = CreateSprite()
				EntityTexture(m, tex)
				EntityFX(m, 1)
				ScaleSprite(m, 0.13 + (i Mod 3) * 0.03, 0.13 + (i Mod 3) * 0.03)
				HideEntity(m)
				r\Objects[S16_PUR_BUB + i] = m
			Next
			FreeTexture(tex)
	End Select
End Function

;---------------------------------------------------------------------
; the shared event
;---------------------------------------------------------------------

Function UpdateIndevS16(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2siv"
			UpdateS16Siv(e)
		Case "room2bio"
			UpdateS16Bio(e)
		Case "room2origin"
			UpdateS16Origin(e)
		Case "room2purge"
			UpdateS16Purge(e)
		Case "room2review"
			UpdateS16Review(e)
		Case "room2lecture"
			UpdateS16Lecture(e)
		Case "room2site41"
			UpdateS16Site41(e)
		Case "room2cell49"
			UpdateS16Cell49(e)
		Case "room2vault117"
			UpdateS16Vault(e)
		Case "room2bunker"
			UpdateS16Bunker(e)
	End Select
End Function

;=====================================================================
; room2siv - Small Items Vault
;   EventState  SCP-1045 burning (time left)   EventState2  rolls of SCP-1125
;   EventState3 SCP-1510 cooldown
;=====================================================================

Function UpdateS16Siv(e.Events)
	Local r.Rooms = e\room
	Local glow% = r\Objects[S16_SIV_GLOW]
	Local fl#, res%, pre$

	If r\dist < 10.0 Then IndevS16Spin(r, 1.0)
	If e\EventState3 > 0 Then e\EventState3 = Max(0, e\EventState3 - FPSfactor)
	If PlayerRoom <> r Then
		If e\EventState > 0 Then
			e\EventState = 0
			HideEntity(glow)
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return

	;---- SCP-1045
	If e\EventState > 0 Then
		e\EventState = e\EventState - FPSfactor
		ShowEntity(glow)
		fl = 0.09 + Rnd(0.0, 0.03) + 0.02 * Sin(e\EventState * 9.0)
		ScaleSprite(glow, fl, fl * 1.4)
		If EntityDistance(Collider, r\Objects[S16_SIV_LANTERN]) < 3.0 Then IndevStress = Min(100, IndevStress + 0.012 * FPSfactor)
		If e\EventState <= 0 Then
			e\EventState = 0
			HideEntity(glow)
			IS16Tell("The stub gutters out. There is a smear of fat in the cup that was not there before.", 7)
		EndIf
	ElseIf IS16Click(r\Objects[S16_SIV_LANTERN], r\Objects[S16_SIV_LANTERN], 1.3) Then
		e\EventState = 70 * 25
		ShowEntity(glow)
		IndevStress = Min(100, IndevStress + 10)
		PlaySound_Strict(LoadTempSound("SFX\Horror\Horror3.ogg"))
		IS16Tell("You light the stub. On each paper side a small shadow starts to writhe. This one has a voice.", 8)
	EndIf

	;---- SCP-1510
	If IS16Click(r\Objects[S16_SIV_HELMET], r\Objects[S16_SIV_HELMET], 1.3) Then
		If e\EventState3 > 0 Then
			IS16Tell("Your head is still ringing from the last time. The helmet can wait.", 5)
		Else
			e\EventState3 = 70 * 180
			BlinkTimer = -10
			Injuries = Max(0, Injuries - 1.5)
			Bloodloss = 0
			Stamina = 0
			BlurTimer = 700
			IndevStress = Min(100, IndevStress + 25)
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
			IS16Tell("Somebody speaks Latin in your voice. Then it is later, and your cuts are bound with strips of your own sleeve.", 10)
		EndIf
	EndIf

	;---- SCP-1125
	If IS16Click(r\Objects[S16_SIV_DICE], r\Objects[S16_SIV_DICE], 1.2) Then
		e\EventState2 = e\EventState2 + 1
		PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem1.ogg"))
		res = Rand(3)
		pre = ""
		While res = 3
			pre = pre + "Maybe. "
			res = Rand(3)
		Wend
		If e\EventState2 >= 3 Then
			IndevStress = Min(100, IndevStress + 20)
			BlurTimer = Max(BlurTimer, 400)
			Stamina = 0
			IS16Tell("The die: " + pre + "You can't decide whether to put it down. You should ask it.", 8)
		ElseIf res = 1 Then
			Stamina = 100
			IndevRelieveStress(8)
			IS16Tell("The die: " + pre + "Yes. You don't remember asking, but you feel better for being told.", 7)
		Else
			Stamina = 0
			IndevStress = Min(100, IndevStress + 6)
			IS16Tell("The die: " + pre + "No. Whatever you were about to do, you find you haven't the wind for it.", 7)
		EndIf
	EndIf
End Function

;=====================================================================
; room2bio - Biological Holding
;   EventState  how long the freezer has stood open with you in the room
;   EventState2 SCP-1513 cooldown      EventState3 SCP-1519 cradle recharge
;   flags: s freezer shut, w warned, h shells hatched, k a sphere in your hand,
;          r the rodents noticed you, f you saw the feral one
;=====================================================================

Function UpdateS16Bio(e.Events)
	Local r.Rooms = e\room
	Local i%, m%, t#, d#, best%, bd#, lx#, inside%
	Local slab% = r\Objects[S16_BIO_SLAB], hinge% = r\Objects[S16_BIO_HINGE]

	If r\dist < 10.0 Then IndevS16Spin(r, 1.0)
	If e\EventState2 > 0 Then e\EventState2 = Max(0, e\EventState2 - FPSfactor)
	If e\EventState3 > 0 Then e\EventState3 = Max(0, e\EventState3 - FPSfactor)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	t = IS16Time()
	IAxLocal(r)
	lx = TFormedX()
	inside = (lx > 250.0)

	;---- SCP-1515: they hop, and they all turn to look
	For i = 0 To 4
		m = r\Objects[S16_BIO_ROD + i]
		If m <> 0 Then
			PositionEntity(m, EntityX(m), 6.0 + Abs(Sin(t * (150.0 + i * 17.0) + i * 70.0)) * (5.0 + i), EntityZ(m))
			If inside Then
				If EntityDistance(m, Collider) < 3.5 Then
					PointEntity(m, Collider)
					IS16Flat(m)
					If Not IAxFlag(e, "r") Then
						IAxSetFlag(e, "r")
						IndevStress = Min(100, IndevStress + 3)
						IS16Tell("All five turn to look at you. One chirps. It is not you they are counting.", 7)
					EndIf
				EndIf
			EndIf
		EndIf
	Next

	;---- SCP-1513: the pet
	m = r\Objects[S16_BIO_PETM]
	If m <> 0 Then
		RotateEntity(m, 0, -90.0 + 9.0 * Sin(t * 300.0), 0)
		If IS16Click(m, r\Objects[S16_BIO_PET], 1.5) Then
			If e\EventState2 <= 0 Then
				e\EventState2 = 70 * 90
				IndevRelieveStress(18)
				IS16Tell("It pushes its leaves into your hand like a cat. It is a sunflower. You feel steadier all the same.", 7)
			Else
				IS16Tell("It leans after your hand. It has had its fuss for now.", 5)
			EndIf
		EndIf
	EndIf

	;---- SCP-1513: the other one moves when nobody is looking
	m = r\Objects[S16_BIO_FERALM]
	If m <> 0 And inside Then
		If EntityInView(m, Camera) Then
			If EntityDistance(m, Collider) < 2.2 And (Not IAxFlag(e, "f")) Then
				IAxSetFlag(e, "f")
				IS16Tell("It is all stem and root, and it does not want to be looked at.", 6)
			EndIf
		ElseIf Rand(45) = 1 Then
			best = -1
			bd = 0
			For i = 0 To 3
				d = EntityDistance(r\Objects[S16_BIO_FERAL0 + i], Collider)
				If d > bd And (Not EntityInView(r\Objects[S16_BIO_FERAL0 + i], Camera)) Then
					bd = d
					best = i
				EndIf
			Next
			If best >= 0 Then
				PositionEntity(m, EntityX(r\Objects[S16_BIO_FERAL0 + best], True), EntityY(r\Objects[S16_BIO_FERAL0 + best], True), EntityZ(r\Objects[S16_BIO_FERAL0 + best], True), True)
				PointEntity(m, Collider)
				IS16Flat(m)
			EndIf
		EndIf
	EndIf

	;---- SCP-1519: the cradle
	If IS16Click(r\Objects[S16_BIO_CRADLE], r\Objects[S16_BIO_CRADLE], 1.3) Then
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * 180
			IS16Give("bat", r\Objects[S16_BIO_CRADLE])
			IS16Tell("The thing in the tank flexes. The cradle clicks and gives up a cell, warm as a hand.", 7)
		Else
			IS16Tell("The cradle is empty. The lamplighter is five hundred years old and will not be hurried.", 6)
		EndIf
	EndIf

	;---- SCP-1517: the freezer
	If IAxFlag(e, "s") Then
		RotateEntity(hinge, 0, CurveAngle(0.0, EntityYaw(hinge), 6.0), 0)
		Return
	EndIf
	If inside Then e\EventState = e\EventState + FPSfactor
	If e\EventState > 70 * 40 And (Not IAxFlag(e, "w")) Then
		IAxSetFlag(e, "w")
		IS16Tell("Something in the freezer ticks, like sugar cracking.", 6)
	EndIf
	If e\EventState > 70 * 75 Then
		If Not IAxFlag(e, "h") Then
			IAxSetFlag(e, "h")
			PlaySound_Strict(LoadTempSound("SFX\General\GlassBreak.ogg"))
			IS16Tell("A shell splits. The shelf is suddenly busy.", 6)
		EndIf
		If inside Then
			Injuries = Injuries + 0.0006 * FPSfactor
			DeathMSG = "Subject D-9341 was found in Biological Holding beside an open freezer. Most of the body mass had been converted to boiled sweets. Remains incinerated."
			If Rand(500) = 1 And MsgTimer <= 0 Then IS16Tell("The back of your hand has gone glassy and smells of pear drops. It doesn't hurt at all.", 7)
		EndIf
	EndIf
	If IS16Click(slab, slab, 1.6) Then
		IAxSetFlag(e, "s")
		PlaySound_Strict(LoadTempSound("SFX\Interact\LeverFlip.ogg"))
		If IAxFlag(e, "h") Then
			IS16Tell("You lean on the freezer door until the seal takes. The ones already out go still in the cold draught.", 7)
		Else
			IS16Tell("The freezer door shuts and the seal takes. The compressor settles.", 6)
		EndIf
	ElseIf IS16Aim(r\Objects[S16_BIO_CANDY], 1.2, 0.97) Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			If IAxFlag(e, "k") Then
				DeathMSG = "Subject D-9341 was found in Biological Holding beside an open freezer. Most of the body mass had been converted to boiled sweets. Remains incinerated."
				IS16Tell("It tastes of pear drops. Then you can't feel your tongue. Then you can't feel anything.", 8)
				Kill()
			Else
				IAxSetFlag(e, "k")
				IS16Tell("You pick one up. It is sweating in your fingers. Click again to put it in your mouth.", 7)
			EndIf
		EndIf
	ElseIf IAxFlag(e, "k") Then
		e\EventStr = Replace(e\EventStr, "k", "")
		IS16Tell("You put it back on the shelf and wipe your fingers.", 4)
	EndIf
End Function

;=====================================================================
; room2origin - Procedure 1512-Alpha
;   EventState  the slime is drawn back (time left, from 60 s)
;   EventState2 how long the pencil has been held to a worksheet
;   EventState3 pause between warnings        flag n: the body is placed
;=====================================================================

Function UpdateS16Origin(e.Events)
	Local r.Rooms = e\room
	Local slime% = r\Objects[S16_ORI_SLIMEM]
	Local a#, hold%, aimed%

	If r\dist < 10.0 Then IndevS16Spin(r, 1.0)
	If e\EventState > 0 Then e\EventState = Max(0, e\EventState - FPSfactor)
	a = 0.85
	If e\EventState > 70 * 57 Then
		a = 0.85 * (e\EventState - 70 * 57) / (70 * 3.0)
	ElseIf e\EventState > 70 * 4 Then
		a = 0.0
	ElseIf e\EventState > 0 Then
		a = 0.85 * (1.0 - e\EventState / (70 * 4.0))
	EndIf
	If slime <> 0 Then EntityAlpha(slime, a)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return
	If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Body(r, S16_ORI_BODY, -90, 40)
	EndIf
	If r\NPC[0] <> Null Then IAxSkin(r\NPC[0], "GFX\npcs\scientist.jpg")

	aimed = IS16Aim(r\Objects[S16_ORI_SHEET_S], 1.3, 0.95) Or IS16Aim(r\Objects[S16_ORI_SHEET_N], 1.3, 0.95)
	hold = False
	If aimed Then
		DrawHandIcon = True
		If MouseDown1 Then hold = True
	EndIf
	If hold And e\EventState <= 0 Then
		If e\EventState2 = 0 Then IS16Tell("You take up the working where the last hand left off. You do not believe a line of it.", 5)
		e\EventState2 = e\EventState2 + FPSfactor
		If e\EventState2 >= 70 * 5 Then
			e\EventState2 = 0
			e\EventState = 70 * 60
			IndevStress = Min(100, IndevStress + 5)
			PlaySound_Strict(LoadTempSound("SFX\General\Hiss.ogg"))
			IS16Tell("The figures come out. They cannot be right. Behind you the slime draws back into the floor.", 8)
		EndIf
	ElseIf hold Then
		If MsgTimer <= 0 Then IS16Tell("The working holds for now. Cross while it does.", 4)
	Else
		e\EventState2 = Max(0, e\EventState2 - FPSfactor * 2)
	EndIf

	;the slime burns and turns the room over
	If a > 0.4 Then
		IAxLocal(r)
		If Abs(TFormedZ()) < 300.0 And Abs(TFormedX()) < 352.0 Then
			Injuries = Injuries + 0.004 * FPSfactor
			BlurTimer = Max(BlurTimer, 500)
			CameraShake = Max(CameraShake, 1.2)
			Stamina = Max(0, Stamina - 0.4 * FPSfactor)
			DeathMSG = "Subject D-9341 was recovered from the Procedure 1512-Alpha hall with chemical burns to the lower body, having crossed the growth without performing the procedure."
			If e\EventState3 <= 0 Then
				e\EventState3 = 70 * 8
				IS16Tell("The slime eats through your soles and the hall tips sideways. You no longer know which end you came in by.", 7)
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room2purge - SCP-1518
;   EventState  purge running (time left, from 30 s)   EventState2 how far the bubbles are blown (0..1)
;   EventState3 pause after a bubble touched you
;=====================================================================

Function UpdateS16Purge(e.Events)
	Local r.Rooms = e\room
	Local i%, b%, t#, x#, y#, z#, target#

	If e\EventState > 0 Then
		e\EventState = Max(0, e\EventState - FPSfactor)
		target = 1.0
	EndIf
	e\EventState2 = CurveValue(target, e\EventState2, 40.0)
	If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
	If r\dist < 10.0 Then IndevS16Spin(r, 0.4 + 6.0 * e\EventState2)

	If PlayerRoom <> r Then
		For i = 0 To 6
			If r\Objects[S16_PUR_BUB + i] <> 0 Then HideEntity(r\Objects[S16_PUR_BUB + i])
		Next
		Return
	EndIf
	If e\EventState2 > 0.2 Then r\SoundCHN = LoopSound2(RoomAmbience[9], r\SoundCHN, Camera, r\Objects[S16_PUR_FAN0], 12.0, e\EventState2)

	t = IS16Time()
	For i = 0 To 6
		b = r\Objects[S16_PUR_BUB + i]
		If b <> 0 Then
			x = EntityX(r\Objects[S16_PUR_BUBC]) + 300.0 * Sin(t * (7.0 + i * 1.3) + i * 51.0)
			z = EntityZ(r\Objects[S16_PUR_BUBC]) + 400.0 * Sin(t * (5.0 + i * 0.9) + i * 97.0)
			y = EntityY(r\Objects[S16_PUR_BUBC]) + 90.0 * Sin(t * (9.0 + i) + i * 33.0)
			x = x + (440.0 - x) * e\EventState2
			TFormPoint(x, y, z, r\obj, 0)
			PositionEntity(b, TFormedX(), TFormedY(), TFormedZ(), True)
			ShowEntity(b)
			If e\EventState2 < 0.85 And e\EventState3 <= 0 And KillTimer >= 0 Then
				If EntityDistance(b, Camera) < 0.34 Or EntityDistance(b, Collider) < 0.36 Then
					e\EventState3 = 70 * 2.5
					Injuries = Injuries + 1.2
					CameraShake = 3.0
					IndevStress = Min(100, IndevStress + 10)
					DeathMSG = "Subject D-9341 entered the SCP-1518 vault without running the fan purge. Recovered remains account for roughly a third of the subject."
					IS16Tell("A bubble touches you, shrinks, and takes that much of you with it. It does not burst.", 7)
					If Injuries > 4.5 Then Kill()
				EndIf
			EndIf
		EndIf
	Next
	If KillTimer < 0 Then Return

	If IS16Click(r\Objects[S16_PUR_PURGE_S], r\Objects[S16_PUR_PURGE_S], 1.2) Or IS16Click(r\Objects[S16_PUR_PURGE_N], r\Objects[S16_PUR_PURGE_N], 1.2) Then
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button.ogg"))
		If e\EventState <= 0 Then
			e\EventState = 70 * 30
			IS16Tell("FAN PURGE. The fans wind up and everything loose in the hall leans east, into the foam.", 7)
		Else
			IS16Tell("The purge is already running.", 4)
		EndIf
	EndIf
End Function

;=====================================================================
; room2review - Surveillance Review
;   EventState  footage running (time left)   EventState2 the tape deck is rewinding
;   flag n: the researcher is placed. NPC[0] the researcher
;=====================================================================

Function UpdateS16Review(e.Events)
	Local r.Rooms = e\room
	Local it.Items, found.Items, n%, d#, far%, q$ = Chr(34)

	If e\EventState2 > 0 Then e\EventState2 = Max(0, e\EventState2 - FPSfactor)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S16_REV_STAFF, 90)
	EndIf
	If r\NPC[0] <> Null Then
		IAxSkin(r\NPC[0], "GFX\npcs\indev_archivist.jpg")
		d = EntityDistance(r\NPC[0]\Collider, Collider)
		If d < 6.0 Then IAxFace(r\NPC[0], Collider)
		If d < 2.4 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Researcher", "Take what you want off the counter. Then, if you must, press play. In that order.", 7)
				Case 2
					IAxSay("Researcher", "I filed a tape of myself leaving an hour ago. I'd like to know which of us it was.", 7)
				Case 3
					IAxSay("Researcher", "Nobody in the room ever sees them. Only the camera. That is the whole trouble.", 7)
			End Select
		EndIf
	EndIf

	;---- SCP-1110
	If e\EventState > 0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 0
			n = 0
			Repeat
				found = Null
				For it = Each Items
					If it\Picked = False Then
						If EntityDistance(it\collider, r\Objects[S16_REV_COUNTER]) < 0.85 Then
							found = it
							Exit
						EndIf
					EndIf
				Next
				If found = Null Then Exit
				RemoveItem(found)
				n = n + 1
			Until n > 20
			If n > 0 Then
				IndevStress = Min(100, IndevStress + 8)
				IS16Tell("On the screen two figures sweep the counter into a case. You look round. The counter is bare.", 8)
			Else
				IS16Tell("On the screen two figures find the counter empty. The one in the skull mask looks up at the camera.", 8)
			EndIf
		EndIf
	ElseIf IS16Click(r\Objects[S16_REV_PLAY], r\Objects[S16_REV_PLAY], 1.4) Then
		e\EventState = 70 * 6
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button.ogg"))
		IS16Tell("You press PLAY. The counter behind you, seen from above. Nobody at it. Then somebody.", 6)
	EndIf

	;---- SCP-1250
	If IS16Click(r\Objects[S16_REV_DECK], r\Objects[S16_REV_DECK], 1.3) Then
		If e\EventState2 > 0 Then
			IS16Tell("The tape is rewinding.", 3)
		Else
			e\EventState2 = 70 * 20
			PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
			far = 2
			If Curr173 <> Null Then
				d = EntityDistance(Curr173\Collider, Collider)
				If d < 16.0 Then
					far = 0
				ElseIf d < 45.0 Then
					far = 1
				EndIf
			EndIf
			If Rand(3) = 1 Then far = (far + Rand(2)) Mod 3
			Select far
				Case 0
					IS16Tell("Tape: " + q + "...stone on concrete, and close. The next room, or the one after." + q, 8)
				Case 1
					IS16Tell("Tape: " + q + "...it's in the wing. Not near. I can hear it when the fans drop." + q, 8)
				Default
					IS16Tell("Tape: " + q + "...nothing on the floor mics. Wherever the sculpture is, it isn't here." + q, 8)
			End Select
		EndIf
	EndIf
End Function

;=====================================================================
; room2lecture - SCP-1313
;   EventState  0 the board is waiting, 1 the bear is in the room, 2 over
;   EventState2 how far you have followed the board / pause between the bear's swipes
;   EventState3 how long the bear stays
;=====================================================================

Function UpdateS16Lecture(e.Events)
	Local r.Rooms = e\room
	Local bear% = r\Objects[S16_LEC_BEARM]
	Local lx#, lz#, bx#, bz#, dx#, dz#, l#, inside%

	If PlayerRoom <> r Then
		If e\EventState = 1 Then
			e\EventState = 2
			SecondaryLightOn = 1.0
			HideEntity(bear)
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return
	IAxLocal(r)
	lx = TFormedX()
	lz = TFormedZ()
	inside = (lx < -250.0)

	Select e\EventState
		Case 0
			If inside And IS16Aim(r\Objects[S16_LEC_BOARD], 3.2, 0.93) Then
				e\EventState2 = e\EventState2 + FPSfactor
				If e\EventState2 > 70 * 2 And (Not IAxFlag(e, "a")) Then
					IAxSetFlag(e, "a")
					IS16Tell("It is ordinary algebra. You find you are following the second line.", 5)
				EndIf
				If e\EventState2 > 70 * 4.5 And (Not IAxFlag(e, "b")) Then
					IAxSetFlag(e, "b")
					IS16Tell("The fourth line follows from the third. Somebody has written DO NOT FINISH. Look away.", 5)
				EndIf
				If e\EventState2 > 70 * 7 And (Not IAxFlag(e, "c")) Then
					IAxSetFlag(e, "c")
					IS16Tell("The last line has been wiped, but you can see what it must have been. LOOK AWAY.", 5)
				EndIf
				If e\EventState2 > 70 * 9.5 Then
					e\EventState = 1
					e\EventState2 = 70 * 2.5
					e\EventState3 = 70 * 40
					PositionEntity(bear, EntityX(r\Objects[S16_LEC_BEAR], True), EntityY(r\Objects[S16_LEC_BEAR], True), EntityZ(r\Objects[S16_LEC_BEAR], True), True)
					ShowEntity(bear)
					LightBlink = 3.0
					IndevStress = Min(100, IndevStress + 20)
					PlaySound_Strict(LoadTempSound("SFX\SCP\860\Cancer1.ogg"))
					IS16Tell("a = one adult female grizzly bear. The lights go.", 6)
				EndIf
			Else
				e\EventState2 = Max(0, e\EventState2 - FPSfactor * 0.5)
			EndIf

		Case 1
			SecondaryLightOn = CurveValue(0.0, SecondaryLightOn, 10.0)
			ShowEntity(bear) ;(a loaded game starts with it hidden)
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState2 > 0 Then e\EventState2 = e\EventState2 - FPSfactor
			TFormPoint(EntityX(bear, True), EntityY(bear, True), EntityZ(bear, True), 0, r\obj)
			bx = TFormedX()
			bz = TFormedZ()
			If inside Then
				dx = lx - bx
				dz = lz - bz
				l = Sqr(dx * dx + dz * dz)
				If l > 70.0 And e\EventState3 < 70 * 38 Then
					bx = Min(Max(bx + dx / l * 5.2 * FPSfactor, -880.0), -272.0)
					bz = Min(Max(bz + dz / l * 5.2 * FPSfactor, -580.0), 528.0)
					TFormPoint(bx, Abs(Sin(e\EventState3 * 6.0)) * 8.0, bz, r\obj, 0)
					PositionEntity(bear, TFormedX(), TFormedY(), TFormedZ(), True)
				EndIf
				RotateEntity(bear, 0, VectorYaw(EntityX(Collider, True) - EntityX(bear, True), 0, EntityZ(Collider, True) - EntityZ(bear, True)), 0, True)
				If l < 150.0 And e\EventState2 <= 0 Then
					e\EventState2 = 70 * 1.6
					Injuries = Injuries + 1.3
					CameraShake = 4.0
					BlurTimer = Max(BlurTimer, 300)
					PlaySound_Strict(LoadTempSound("SFX\General\Slash" + Rand(1, 2) + ".ogg"))
					DeathMSG = "Subject D-9341 was found in Lecture Room 2 with injuries consistent with a large carnivore. The whiteboard had been wiped. No animal was recovered."
					IS16Tell("Something very large hits you in the dark.", 4)
					If Injuries > 4.5 Then Kill()
				EndIf
			EndIf
			If Rand(260) = 1 Then PlaySound2(LoadTempSound("SFX\SCP\860\Cancer" + Rand(0, 5) + ".ogg"), Camera, bear, 8.0)
			If e\EventState3 <= 0 Then
				e\EventState = 2
				HideEntity(bear)
				IS16Tell("The lights come back. The chairs are not where they were, and the board is clean.", 7)
			EndIf

		Default
			If SecondaryLightOn < 0.995 Then SecondaryLightOn = CurveValue(1.0, SecondaryLightOn, 20.0)
	End Select
End Function

;=====================================================================
; room2site41 - SCP-1312
;   EventState  0 free, 1 held in their cell   EventState2 how long the black one leaves you alone
;   EventState3 time left in the cell
;   NPC[0] the guard, [1] white, [2] orange, [3] black
;   flags: n placed, c the black one has spoken, p the white one has shown you the page
;=====================================================================

Function UpdateS16Site41(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, d#, lx#, lz#, inzone%, dx#, dz#
	Local door.Doors = r\RoomDoors[S16_S41_D_CELL]
	Local q$ = Chr(34)

	If e\EventState2 > 0 Then e\EventState2 = Max(0, e\EventState2 - FPSfactor)
	If PlayerRoom <> r Then
		If e\EventState = 1 Then
			e\EventState = 0
			door\locked = False
		EndIf
		Return
	EndIf
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[S16_S41_GUARD], True), EntityY(r\Objects[S16_S41_GUARD], True) + 0.35, EntityZ(r\Objects[S16_S41_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 90, 0)
		r\NPC[0] = n
		r\NPC[1] = IS16Person(r, S16_S41_WHITE, 90)
		r\NPC[2] = IS16Person(r, S16_S41_ORANGE, 0)
		r\NPC[3] = IS16Person(r, S16_S41_BLACK, 180)
	EndIf
	IAxSkin(r\NPC[1], "GFX\npcs\indev_flat_white.jpg")
	IAxSkin(r\NPC[2], "GFX\npcs\indev_flat_orange.jpg")
	IAxSkin(r\NPC[3], "GFX\npcs\indev_flat_black.jpg")

	n = r\NPC[0]
	If n <> Null Then
		n\State = 9
		If EntityDistance(n\Collider, Collider) < 2.4 And MsgTimer <= 0 And Rand(600) = 1 Then
			Select Rand(3)
				Case 1
					IAxSay("Guard", "This side of the wire you're my problem. That side you're theirs.", 6)
				Case 2
					IAxSay("Guard", "The black one only knows two words. You'll hear them if you go through the gate.", 7)
				Case 3
					IAxSay("Guard", "They let the last one out after half a minute. They'd written him up by then.", 7)
			End Select
		EndIf
	EndIf

	IAxLocal(r)
	lx = TFormedX()
	lz = TFormedZ()
	inzone = (lx > 492.0 And lx < 960.0 And Abs(lz) < 576.0)
	n = r\NPC[3]
	If n = Null Then Return

	If e\EventState = 0 Then
		If inzone And e\EventState2 <= 0 Then
			;the black one walks straight at whatever does not belong
			n\State = 1
			dx = EntityX(Collider) - EntityX(n\Collider)
			dz = EntityZ(Collider) - EntityZ(n\Collider)
			RotateEntity(n\Collider, 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(n\Collider), 10.0), 0)
			If Not IAxFlag(e, "c") Then
				IAxSetFlag(e, "c")
				IndevStress = Min(100, IndevStress + 8)
				IS16Tell("The black figure: " + q + "containment breach" + q, 5)
			EndIf
			If r\NPC[1] <> Null Then IAxFace(r\NPC[1], Collider)
			If r\NPC[2] <> Null Then IAxFace(r\NPC[2], Collider)
			If EntityDistance(n\Collider, Collider) < 0.8 Then
				e\EventState = 1
				e\EventState3 = 70 * 35
				BlinkTimer = -10
				PositionEntity(Collider, EntityX(r\Objects[S16_S41_CELLSPOT], True), EntityY(r\Objects[S16_S41_CELLSPOT], True) + 0.5, EntityZ(r\Objects[S16_S41_CELLSPOT], True))
				ResetEntity(Collider)
				DropSpeed = 0
				door\open = False
				door\locked = True
				n\State = 0
				PositionEntity(n\Collider, EntityX(r\Objects[S16_S41_POST], True), EntityY(r\Objects[S16_S41_POST], True) + 0.5, EntityZ(r\Objects[S16_S41_POST], True))
				ResetEntity(n\Collider)
				IndevStress = Min(100, IndevStress + 15)
				IS16Tell("A flat black hand closes on your arm. When you can see again there is a door, and it is shut.", 8)
			EndIf
		Else
			n\State = 0
		EndIf
	Else
		;held: they write you up, then lose interest
		n\State = 0
		door\locked = True
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 < 70 * 18 And (Not IAxFlag(e, "p")) Then
			IAxSetFlag(e, "p")
			IS16Tell("The white one holds a page up to the door. It is a containment procedure. It is for you.", 8)
		EndIf
		If e\EventState3 <= 0 Then
			e\EventState = 0
			e\EventState2 = 70 * 30
			door\locked = False
			door\open = True
			e\EventStr = Replace(Replace(e\EventStr, "c", ""), "p", "")
			IS16Tell("The lock lets go. They have filed you and lost interest. That will not last.", 7)
		EndIf
	EndIf
End Function

;=====================================================================
; room2cell49 - SCP-1516
;   EventState  the word is being lifted off the card (time left)   EventState2 which card
;   NPC[0] the Written Man.  flags: n placed, g it has made its one thing for you
;=====================================================================

Function UpdateS16Cell49(e.Events)
	Local r.Rooms = e\room
	Local n.NPCs, i%, best%

	If r\dist < 10.0 Then IndevS16Spin(r, 1.0)
	If PlayerRoom <> r Then Return
	If KillTimer < 0 Then Return

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, S16_C49_MAN, 90)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		IAxSkin(n, "GFX\npcs\indev_text.jpg")
		IAxLocal(r)
		If TFormedX() > 250.0 Then IAxFace(n, Collider)
	EndIf

	If e\EventState > 0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then
			e\EventState = 0
			Select Int(e\EventState2)
				Case 1
					IS16Give("indevration", r\Objects[S16_C49_TRAY])
					IS16Tell("PAN hangs in the air in grey type. Then it is in the tray, and it is bread. More or less.", 8)
				Case 2
					IS16Give("firstaid", r\Objects[S16_C49_TRAY])
					IS16Tell("VENDA unrolls off the card like a ribbon. What lands in the tray is a dressing. More or less.", 8)
				Default
					IS16Give("bat", r\Objects[S16_C49_TRAY])
					IS16Tell("PILA drops into the tray with a click. It has a charge. It also has serifs.", 8)
			End Select
		EndIf
		Return
	EndIf

	best = -1
	For i = 0 To 2
		If IS16Aim(r\Objects[S16_C49_CARD0 + i], 1.2, 0.985) Then best = i
	Next
	If best >= 0 Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			If IAxFlag(e, "g") Then
				IS16Tell("It reads the card and shakes its head. A word comes off its shoulder and hangs there: UNA.", 7)
			Else
				IAxSetFlag(e, "g")
				e\EventState = 70 * 4
				e\EventState2 = best + 1
				PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
				IS16Tell("You post the card through the tray. The figure lifts the word off the paper like a hair off a sleeve.", 6)
			EndIf
		EndIf
	EndIf
End Function

;=====================================================================
; room2vault117 - SCP-1511
;   EventState  how much calm the fragment has given (it recovers while you are away)
;   EventState2 the lift
;=====================================================================

Function UpdateS16Vault(e.Events)
	Local r.Rooms = e\room
	Local q$ = Chr(34)

	If PlayerRoom <> r Then
		If e\EventState > 0 Then e\EventState = Max(0, e\EventState - 0.002 * FPSfactor)
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then Return

	If EntityDistance(Collider, r\Objects[S16_V117_CRYSTAL]) < 1.7 Then
		If e\EventState < 30.0 Then
			IndevRelieveStress(0.03 * FPSfactor)
			e\EventState = e\EventState + 0.03 * FPSfactor
		EndIf
		If MsgTimer <= 0 And Rand(350) = 1 Then
			Select Rand(6)
				Case 1
					IS16Tell("The fragment: " + q + "There is a shore. You will know the boat when it comes." + q, 7)
				Case 2
					IS16Tell("The fragment: " + q + "Where I am going the fields are already cut." + q, 7)
				Case 3
					IS16Tell("The fragment: " + q + "It begins soon. I was told it begins soon." + q, 7)
				Case 4
					IS16Tell("The fragment: " + q + "Sit. Nothing is asked of you there." + q, 7)
				Case 5
					IS16Tell("The fragment hums one note for a long time. Your shoulders come down.", 7)
				Case 6
					IndevStress = Min(100, IndevStress + 4)
					IS16Tell("The fragment: " + q + "TRANSFER 4 OF 9. HULL OPEN. OCCUPANTS UNSECURED." + q, 7)
			End Select
		EndIf
	EndIf
End Function

;=====================================================================
; room2bunker - SCP-1514
;   EventState  0 inspection overdue (alarm), 1 logged   EventState2 the lift
;   EventState3 how long your hand has been on the panel
;   NPC[0] the technician who should have done it.  flags: n placed, w warned
;=====================================================================

Function UpdateS16Bunker(e.Events)
	Local r.Rooms = e\room
	Local door.Doors = r\RoomDoors[S16_BUN_D_LOCKER]
	Local touching%
	Local q$ = Chr(34)

	If r\dist < 10.0 Then IndevS16Spin(r, 1.0)
	If PlayerRoom <> r Then
		IS16Hush(e)
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If KillTimer < 0 Then
		IS16Hush(e)
		Return
	EndIf

	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Body(r, S16_BUN_BODY, 200, 19)
	EndIf
	If r\NPC[0] <> Null Then IAxSkin(r\NPC[0], "GFX\npcs\janitor.jpg")

	If e\EventState = 0 Then
		door\locked = True
		If e\Sound = 0 Then e\Sound = LoadSound_Strict("SFX\Alarm\Alarm3.ogg")
		e\SoundCHN = LoopSound2(e\Sound, e\SoundCHN, Camera, r\Objects[S16_BUN_PANEL], 6.0, 0.7)
	EndIf

	touching = False
	If IS16Aim(r\Objects[S16_BUN_PANEL], 1.3, 0.95) Then
		DrawHandIcon = True
		If MouseDown1 Then touching = True
	EndIf
	If touching Then
		e\EventState3 = e\EventState3 + FPSfactor
		If e\EventState3 > 70 * 1.2 And (Not IAxFlag(e, "w")) Then
			IAxSetFlag(e, "w")
			IS16Tell("Intercom: " + q + "Inspection logged. Remove your hand from the unit." + q, 4)
		EndIf
		If e\EventState3 > 70 * 3.2 Then
			PlaySound_Strict(LoadTempSound("SFX\General\Gunshot.ogg"))
			DeathMSG = "Subject D-9341 was terminated by the automatic defences of the Secure Bunker after exceeding the permitted contact with SCP-1514-1A. The signal was not interrupted."
			Kill()
		EndIf
	ElseIf e\EventState3 > 0 Then
		;the hand came off in time: that was an inspection
		e\EventState3 = 0
		e\EventStr = Replace(e\EventStr, "w", "")
		If e\EventState = 0 Then
			e\EventState = 1
			IS16Hush(e)
			door\locked = False
			door\open = True
			IndevRelieveStress(10)
			PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
			IS16Tell("A needle swings back into the green and the alarm stops. Behind you a lock lets go.", 8)
		Else
			IS16Tell("The log already shows your inspection. The next is due in twenty minutes. You will not be here.", 7)
		EndIf
	EndIf
End Function

Function IS16Hush(e.Events)
	If e\SoundCHN <> 0 Then
		If ChannelPlaying(e\SoundCHN) Then StopChannel(e\SoundCHN)
	EndIf
End Function
