;=====================================================================
; SCP: Containment Breach - Indev SCP-173-B "Practice Sculpture"
;
;   The Foundation trains new personnel by making them stand in a room
;   with a duplicate SCP-173 sculpture until they lose the "blink first"
;   flinch. SCP-173-B is that duplicate. It is not anomalous. It cannot
;   move. It has taken twenty years of the same terrified staring and
;   has never once moved a millimetre.
;
;   It doesn't have to move. Every person in that room already believes
;   it can, and every person in that room already stands there rigid.
;
;   Dedicated room:      room2173cages (Indev Zone), cage 3 on the lower
;                        level. See MapSystem.bb hookup below.
;   Containment:         open plinth in a locked cage; the cage door is
;                        released from the observation desk on entry.
;   Documents:           doc173b (procedure) + note173b (a wall of
;                        graffiti from previous trainees, drawn in as a
;                        readable document).
;   Gameplay mechanic:   an inverted SCP-173 fear test. As long as you
;                        watch the sculpture, stress drains and stamina
;                        drains too - concentration. Look away for more
;                        than half a second and stress spikes hard - the
;                        muscle memory of being in a room with SCP-173.
;   Event:               "PRACTICE SESSION - do not look away" HUD line
;                        for 45 seconds after you first enter the cage.
;                        Finish it (watch it for 45 s cumulative) and a
;                        Level 4 keycard drops from the plinth as your
;                        completion reward. Fail it (three look-away
;                        spikes) and the door reopens with no reward.
;                        Leaving the room cancels the session.
;
;   Vanilla-first: this reuses the existing GFX\map\173_2.b3d sculpture
;   prop (already loaded in the intro room), the existing IndevStress
;   meter, EntityVisible for the sight check, and CreateItem for the
;   reward drop. No new globals for the sculpture's anomalous state,
;   because it doesn't have any.
;=====================================================================

Global I173B_Sculpt%, I173B_Plinth%          ;the props
Global I173B_Room.Rooms                       ;the room instance
Global I173B_Time#                            ;cumulative time you've watched it (frames at 70Hz)
Global I173B_LookAway#                        ;time since you last had it on screen
Global I173B_Fails%                           ;strikes; 3 = failure
Global I173B_State%                           ;0 not started, 1 running, 2 won, 3 failed
Global I173B_Reward% = False                  ;dropped the keycard yet
Global I173B_MsgT#                            ;little "PRACTICE SESSION" HUD timer

Const I173B_GOAL# = 70.0 * 45.0               ;45 seconds of cumulative eye contact

Function Indev173BReset()
	I173B_Sculpt = 0 : I173B_Plinth = 0 : I173B_Room = Null
	I173B_Time = 0 : I173B_LookAway = 0 : I173B_Fails = 0
	I173B_State = 0 : I173B_Reward = False : I173B_MsgT = 0
End Function

;called from FillRoom
;the room's floor waypoints put the cages on the lower level, centred around
;(-500..700, y -544, -800..300). The middle cage sits at approximately x 60, z -300.
;
;PLACEMENT NOTES (fixed 2026-09-23 after in-game report):
;  - The plinth mesh is 169 room-units tall (see make268.py plinth()).
;    In world units it stands (169 * RoomScale) high, so the sculpture's
;    feet sit at (plinth base y + 169 * RoomScale), NOT +0.169 world units.
;  - Both documents live on the lower cage floor right beside the plinth.
;    Placing them on an upper "observation desk" that didn't exist meant
;    they fell out of the room.
Function IndevFill173B(r.Rooms)
	I173B_Room = r

	;the plinth. Base at r\y - 544 room-units, top at r\y - 544 + 169 room-units.
	I173B_Plinth = LoadMesh_Strict("GFX\map\Props\indevplinth.b3d", r\obj)
	PositionEntity(I173B_Plinth, r\x + 60.0 * RoomScale, r\y - 544.0 * RoomScale, r\z - 300.0 * RoomScale, True)
	ScaleEntity(I173B_Plinth, RoomScale, RoomScale, RoomScale, True)
	EntityType(I173B_Plinth, HIT_MAP)

	;the sculpture, standing on top of the plinth (not inside it).
	I173B_Sculpt = LoadMesh_Strict("GFX\map\173_2.b3d", r\obj)
	PositionEntity(I173B_Sculpt, r\x + 60.0 * RoomScale, r\y + (-544.0 + 169.0) * RoomScale, r\z - 300.0 * RoomScale, True)
	;the intro-room sculpture is used at natural scale in the intro; we do the same here
	EntityType(I173B_Sculpt, HIT_MAP)
	EntityPickMode(I173B_Sculpt, 2)

	;both documents on the cage floor beside the plinth, so they cannot fall out
	;of the room
	Local it.Items
	it = CreateItem("doc173b", r\x + 200.0 * RoomScale, r\y - 540.0 * RoomScale, r\z - 260.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it = CreateItem("note173b", r\x - 100.0 * RoomScale, r\y - 540.0 * RoomScale, r\z - 260.0 * RoomScale)
	EntityParent(it\collider, r\obj)
End Function

;is the player looking at it right now? cheap: EntityVisible + distance
Function Indev173BSees%()
	If I173B_Sculpt = 0 Then Return False
	If EntityDistance(Collider, I173B_Sculpt) > 6.0 Then Return False
	If Not EntityVisible(Collider, I173B_Sculpt) Then Return False
	;a rough "in the crosshair" check: the dot of (sculpture - camera) forward with camera forward
	Local dx# = EntityX(I173B_Sculpt, True) - EntityX(Camera, True)
	Local dy# = EntityY(I173B_Sculpt, True) - EntityY(Camera, True)
	Local dz# = EntityZ(I173B_Sculpt, True) - EntityZ(Camera, True)
	Local ln# = Sqr(dx*dx + dy*dy + dz*dz)
	If ln < 0.001 Then Return True
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dot# = (dx*fx + dy*fy + dz*fz) / ln
	Return (dot > 0.55) ;roughly "on screen" (a little tighter than the 90 degree FOV)
End Function

Function UpdateIndev173B()
	If I173B_Sculpt = 0 Or I173B_Room = Null Then Return
	If KillTimer < 0 Then Return

	Local inRoom% = (PlayerRoom = I173B_Room)
	If Not inRoom Then
		;leaving the room ends the session but keeps progress
		If I173B_State = 1 Then
			I173B_State = 0
			I173B_Time = 0 : I173B_LookAway = 0 : I173B_Fails = 0
		EndIf
		I173B_MsgT = 0
		Return
	EndIf

	;fresh start when the player first steps in (or comes back after failing)
	If I173B_State = 0 And (Not I173B_Reward) Then
		I173B_State = 1
		I173B_Time = 0 : I173B_LookAway = 0 : I173B_Fails = 0
		Msg = "PRACTICE SESSION: watch the sculpture. Do not look away. This is a duplicate. It is not anomalous. Your instinct disagrees. Ignore it."
		MsgTimer = 70 * 8
		I173B_MsgT = 70 * 45
	EndIf

	If I173B_State <> 1 Then Return

	Local sees% = Indev173BSees()
	If sees Then
		;watching: cumulative timer ticks up, stress drains, stamina drains
		I173B_Time = I173B_Time + FPSfactor
		I173B_LookAway = 0
		IndevStress = Max(0, IndevStress - FPSfactor * 0.15)
		Stamina = Max(20, Stamina - FPSfactor * 0.10)
	Else
		I173B_LookAway = I173B_LookAway + FPSfactor
		;half a second: warning. One second: strike + stress spike + stamina slam
		If I173B_LookAway > 35 Then
			If I173B_LookAway < 35 + FPSfactor Then
				Msg = "You looked away. STOP. This is a practice session. It is not moving."
				MsgTimer = 70 * 3
			EndIf
			IndevStress = Min(100, IndevStress + FPSfactor * 0.35)
		EndIf
		If I173B_LookAway > 70 Then
			I173B_Fails = I173B_Fails + 1
			IndevStress = Min(100, IndevStress + 18)
			Stamina = Max(0, Stamina - 25)
			I173B_LookAway = 0
			PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Damage" + Rand(1, 4) + ".ogg"))
			If I173B_Fails >= 3 Then
				I173B_State = 3
				Msg = "Session terminated. Report to the observation desk. Do not look at your reflection in the door on the way out."
				MsgTimer = 70 * 8
				I173B_MsgT = 0
				Return
			Else
				Msg = "Strike " + I173B_Fails + " of 3. Watch the sculpture."
				MsgTimer = 70 * 4
			EndIf
		EndIf
	EndIf

	If I173B_MsgT > 0 Then I173B_MsgT = Max(0, I173B_MsgT - FPSfactor)

	;win
	If I173B_Time >= I173B_GOAL And (Not I173B_Reward) Then
		I173B_State = 2
		I173B_Reward = True
		Msg = "Session complete. You held out. A cage-key drops from the plinth's release mechanism."
		MsgTimer = 70 * 8
		I173B_MsgT = 0
		;drop the training reward at the plinth's foot
		Local it.Items = CreateItem("key4", EntityX(I173B_Plinth, True), EntityY(I173B_Plinth, True) + 0.05, EntityZ(I173B_Plinth, True))
		EntityParent(it\collider, I173B_Room\obj)
	EndIf
End Function

;the "PRACTICE SESSION" HUD line: drawn on top by DrawIndev
Function DrawIndev173B()
	If I173B_State <> 1 Then Return
	If I173B_MsgT <= 0 Then Return
	Local s# = I173B_Time / I173B_GOAL
	If s > 1 Then s = 1
	SetFont Font1
	Color 220, 60, 60
	Text GraphicWidth / 2, 60, "PRACTICE SESSION  " + Int(s * 100) + "%", True, True
	;a thin progress bar under it
	Color 30, 30, 30
	Rect GraphicWidth / 2 - 140, 82, 280, 6, True
	Color 200, 70, 70
	Rect GraphicWidth / 2 - 140, 82, 280 * s, 6, True
	Color 255, 255, 255
End Function
