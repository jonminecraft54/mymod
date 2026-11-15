;=====================================================================
; SCP: Containment Breach - Indev existing-room improvements
;
;   Design.md rule 6. Three real hand-placed extras that follow the
;   connection chain and use vanilla interactions (visible wall button,
;   proximity prompt, MouseHit1 to trigger). Any of them can be turned
;   off by commenting out its single Case-line in FillRoom.
;
;   1. MEDIBAY - broken emergency locker on the wall. First use pops
;      a firstaid AND note500 (custody form) - a chain hook at SCP-500.
;
;   2. room2closets - stuck bottom drawer. Hold left-click 2s to force.
;      Drops one random storage-pool item, then permanently jams.
;
;   3. room2offices - wall intercom. Plays random SFX/Radio/Chatter*.ogg.
;      1 in 3 leaks the AccessCode's last digit.
;
;   All three use CopyEntity(ButtonOBJ) as the visible anchor, so the
;   player sees a wall button in the same style as every other one in
;   the facility. That's the SCP:CB convention.
;=====================================================================

Global IExMediBtn%, IExMediRoom.Rooms, IExMediUsed%
Global IExClosetBtn%, IExClosetRoom.Rooms, IExClosetUsed%
Global IExClosetHold#
Global IExOfficeBtn%, IExOfficeRoom.Rooms, IExOfficeUsedMs%

Function IndevRoomExtrasReset()
	IExMediBtn = 0 : IExMediRoom = Null : IExMediUsed = False
	IExClosetBtn = 0 : IExClosetRoom = Null : IExClosetUsed = False : IExClosetHold = 0
	IExOfficeBtn = 0 : IExOfficeRoom = Null : IExOfficeUsedMs = 0
End Function

;a visible wall button, styled exactly like every SCP:CB door button.
Function IndevMakeButton%(r.Rooms, x#, y#, z#, yaw%)
	Local b% = CopyEntity(ButtonOBJ, r\obj)
	ScaleEntity(b, 0.03, 0.03, 0.03)
	PositionEntity(b, x, y, z, True)
	RotateEntity(b, 0, yaw, 0, True)
	EntityType(b, HIT_MAP)
	EntityPickMode(b, 2)
	Return b
End Function

;true when the player is close enough to be prompted (about 2.5 m) and
;the button is at least somewhat in front of them.
Function IndevBtnNear%(b%)
	If b = 0 Then Return False
	If EntityDistance(Collider, b) > 2.5 Then Return False
	Local dx# = EntityX(b, True) - EntityX(Camera, True)
	Local dz# = EntityZ(b, True) - EntityZ(Camera, True)
	Local ln# = Sqr(dx*dx + dz*dz)
	If ln < 0.001 Then Return True
	TFormVector(0, 0, 1, Camera, 0)
	Local dot# = (dx * TFormedX() + dz * TFormedZ()) / ln
	Return (dot > 0.2) ;wide cone, roughly 130 degrees
End Function

;---------------------------------------------------------------------
; 1. medibay - a broken emergency locker
;---------------------------------------------------------------------

;coords measured on the medibay mesh: back wall on the -x side, floor at 0,
;the bed row runs along -z. We put the locker button waist-high, on the
;wall to the left as you enter (x -300, y +140, z -90). Tweak here if you
;move the medibay mesh.
Function IndevFillMedibayExtras(r.Rooms)
	IExMediRoom = r
	IExMediUsed = False
	IExMediBtn = IndevMakeButton(r, r\x - 300.0 * RoomScale, r\y + 140.0 * RoomScale, r\z - 90.0 * RoomScale, 90)
End Function

Function UpdateIndevMediLocker()
	If IExMediBtn = 0 Or IExMediRoom = Null Then Return
	If PlayerRoom <> IExMediRoom Then Return
	If Not IndevBtnNear(IExMediBtn) Then Return

	If IExMediUsed Then
		Msg = "EMERGENCY LOCKER 4-B: door hanging off its hinges, smells of iodine. Empty."
		MsgTimer = 70 * 3
		Return
	EndIf
	Msg = "EMERGENCY LOCKER 4-B - broken lock. Click to force it open."
	MsgTimer = 70 * 2
	If MouseHit1 Then
		IExMediUsed = True
		Local x# = EntityX(IExMediBtn, True), y# = EntityY(IExMediBtn, True), z# = EntityZ(IExMediBtn, True)
		Local it.Items = CreateItem("firstaid", x, y - 0.15, z + 0.10)
		EntityParent(it\collider, IExMediRoom\obj)
		it = CreateItem("note500", x, y - 0.20, z - 0.10)
		EntityParent(it\collider, IExMediRoom\obj)
		Msg = "The locker pops open. Inside: one field first-aid kit. Also a slip of paper with a custody-form heading. Take both."
		MsgTimer = 70 * 6
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
	EndIf
End Function

;---------------------------------------------------------------------
; 2. room2closets - a stuck drawer
;---------------------------------------------------------------------

;the closets are three side-by-side booths, corridor runs along x, doorways
;on the -x wall. We put the drawer button on the middle booth's back wall
;(z +720 side), at knee height so it reads as a bottom drawer.
Function IndevFillClosetExtras(r.Rooms)
	IExClosetRoom = r
	IExClosetUsed = False
	IExClosetBtn = IndevMakeButton(r, r\x + 0.0, r\y + 70.0 * RoomScale, r\z + 720.0 * RoomScale, 180)
End Function

Function UpdateIndevClosetDrawer()
	If IExClosetBtn = 0 Or IExClosetRoom = Null Then Return
	If PlayerRoom <> IExClosetRoom Then IExClosetHold = 0 : Return
	If Not IndevBtnNear(IExClosetBtn) Then IExClosetHold = 0 : Return

	If IExClosetUsed Then
		Msg = "The drawer's runners are still bent. It won't take anything else."
		MsgTimer = 70 * 3
		Return
	EndIf
	Msg = "Bottom drawer - jammed. Hold left-click to force it (" + Int(Min(IExClosetHold / (70 * 2.0) * 100, 100)) + "%)."
	MsgTimer = 70 * 2
	If MouseDown1 Then
		IExClosetHold = IExClosetHold + FPSfactor
		If IExClosetHold > 70 * 2.0 Then
			IExClosetUsed = True
			IExClosetHold = 0
			Local x# = EntityX(IExClosetBtn, True), y# = EntityY(IExClosetBtn, True), z# = EntityZ(IExClosetBtn, True)
			Local pool$[7]
			pool[0] = "bat" : pool[1] = "electronics" : pool[2] = "gasmask"
			pool[3] = "18vbat" : pool[4] = "indevration" : pool[5] = "syringe" : pool[6] = "cup"
			Local it.Items = CreateItem(pool[Rand(0, 6)], x, y - 0.20, z - 0.15)
			EntityParent(it\collider, IExClosetRoom\obj)
			Msg = "The drawer bangs open and something drops out. The runners are ruined."
			MsgTimer = 70 * 5
			PlaySound_Strict(LoadTempSound("SFX\Interact\PickItem2.ogg"))
		EndIf
	Else
		IExClosetHold = Max(0, IExClosetHold - FPSfactor * 2.0)
	EndIf
End Function

;---------------------------------------------------------------------
; 3. room2offices - wall intercom
;---------------------------------------------------------------------

;the offices template has a long back wall on the -z side of the room.
;We put the intercom button up on the wall at head height.
Function IndevFillOfficeExtras(r.Rooms)
	IExOfficeRoom = r
	IExOfficeUsedMs = 0
	IExOfficeBtn = IndevMakeButton(r, r\x + 0.0, r\y + 180.0 * RoomScale, r\z + 940.0 * RoomScale, 0)
End Function

Function UpdateIndevOfficeIntercom()
	If IExOfficeBtn = 0 Or IExOfficeRoom = Null Then Return
	If PlayerRoom <> IExOfficeRoom Then Return
	If Not IndevBtnNear(IExOfficeBtn) Then Return

	;60-second cooldown between uses
	If IExOfficeUsedMs > 0 Then
		If MilliSecs() - IExOfficeUsedMs < 60000 Then
			Msg = "The intercom is silent. Whoever was on the other end has moved on."
			MsgTimer = 70 * 3
			Return
		EndIf
	EndIf

	Msg = "WALL INTERCOM. Click to listen in."
	MsgTimer = 70 * 2
	If MouseHit1 Then
		IExOfficeUsedMs = MilliSecs()
		PlaySound_Strict(LoadTempSound("SFX\Radio\Chatter" + Rand(1, 4) + ".ogg"))
		If Rand(3) = 1 Then
			Local d% = AccessCode Mod 10
			Msg = "Through the static, one voice: " + Chr(34) + "...and the last digit was " + d + ". Repeat, ends in " + d + ". Copy that." + Chr(34)
			MsgTimer = 70 * 8
		Else
			Msg = "Static, then two voices arguing about lunch rotations. Nothing useful. It cuts out."
			MsgTimer = 70 * 5
		EndIf
	EndIf
End Function

;---------------------------------------------------------------------
; per-frame dispatch
;---------------------------------------------------------------------

Function UpdateIndevRoomExtras()
	If KillTimer < 0 Then Return
	UpdateIndevMediLocker()
	UpdateIndevClosetDrawer()
	UpdateIndevOfficeIntercom()
End Function
