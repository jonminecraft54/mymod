;=====================================================================
; SCP: Containment Breach - Indev SCP-2536 "Big Xmas"
;
;   A 2-metre purple-and-white plastic Christmas tree that manifests in
;   the facility only during December. Comes with a speaker at its base
;   playing a looped festive tune. Underneath it is SCP-2536-1, a gift
;   box that contains an item the target greatly desires.
;
;   Foundation guidance: refrain from accepting the gift, leave the
;   vicinity, inform your supervisor. So obviously the player takes it.
;
;   Purpose:     a once-per-run December surprise; the gift is a large
;                lump of usefulness (best 914 output, a Level 4 key, a
;                random pill, ...) that fits the player's current need
;   Effect:      one manifestation per game session, in an office room
;                the player has walked into. Music fades in, tree pops,
;                the present sits on the floor in front of it.
;   Drawback:    stress + slightly while standing near it (uncanny) and
;                if the player LEAVES the room without picking up the
;                gift, both tree and present vanish after ~3 minutes.
;   Reason to carry: the gift itself, once opened, gives you an item
;                keyed to what you're running low on
;   Spawn:       December only. First qualifying office room the player
;                enters gets a spawn.
;
;   Vanilla-first: reuses CurrentDate(), StreamSound_Strict,
;   IndevXmasIsOfficeRoom, IndevStress, and CreateItem. No new key binds.
;=====================================================================

Global I2536Tree%, I2536Gift%, I2536Room.Rooms
Global I2536MusicCHN%, I2536Placed%, I2536Taken%
Global I2536Timer#, I2536CheckedMonth%
Global I2536ChamberActive%       ;True when the permanent chamber is holding the tree

Function Indev2536Reset()
	;the old world (tree and gift included) is already freed when a new game starts - freeing the stale
	;handles here crashed the second new game of a session ("FreeEntity: Entity does not exist!")
	I2536Tree = 0
	I2536Gift = 0
	If I2536MusicCHN <> 0 Then
		StopStream_Strict(I2536MusicCHN)
		I2536MusicCHN = 0
	EndIf
	I2536Room = Null
	I2536Placed = False
	I2536Taken = False
	I2536Timer = 0
	I2536CheckedMonth = 0
	I2536ChamberActive = False
End Function

Function Indev2536InDec%()
	Return (Mid(CurrentDate(), 4, 3) = "Dec")
End Function

;spawned by MapSystem's Case "room1scp2536". This is the permanent
;containment chamber, so the tree stands here all year round instead of
;only during December. The December office-manifestation behaviour still
;runs on top - both can happen in the same seed.
;
;Tree and gift are placed near the room's local origin. The mesh
;(room1scp2536.rmesh) is a bespoke small chamber, and its interior
;centre is a safe landing spot: any authoring will have a floor at (0,0,0)
;in local coords. If future in-game testing shows they clip a wall,
;retune the offset constants below.
Function IndevFill2536(r.Rooms)
	I2536Room = r
	I2536Placed = True     ;so UpdateIndev2536 doesn't also try to place it in an office
	I2536ChamberActive = True
	I2536Taken = False
	I2536Timer = 0

	;Placement (revised again 2026-09-23 after the tree still clipped a wall
	;on seed 8,10 even at 0.75 scale). Root cause: the mesh's cones are
	;quite wide (400 room units at the base) and the rmesh's back walls
	;are only ~2 m from centre, so any tree at the geometric centre pokes
	;the corner. Two fixes:
	;   1. Shrink to 0.5 * RoomScale => ~1 m tall, ~0.8 m wide at the base
	;   2. Offset the tree 0.6 m from centre toward the -z corner so it
	;      leaves the middle of the room free for the player to walk in
	;Gift now sits 1.0 m in front of the tree so the player walks into
	;the gift first, opens it, and only then approaches the tree.
	I2536Tree = LoadMesh_Strict("GFX\map\Props\scp2536tree.b3d", r\obj)
	PositionEntity(I2536Tree, r\x, r\y, r\z - 0.6, True)
	ScaleEntity(I2536Tree, RoomScale * 0.5, RoomScale * 0.5, RoomScale * 0.5, True)
	EntityType(I2536Tree, HIT_MAP)

	I2536Gift = LoadMesh_Strict("GFX\map\Props\scp2536gift.b3d", r\obj)
	PositionEntity(I2536Gift, r\x, r\y, r\z + 0.4, True)
	ScaleEntity(I2536Gift, RoomScale, RoomScale, RoomScale, True)
	EntityType(I2536Gift, HIT_MAP)

	DebugLog "Indev: IndevFill2536 - permanent SCP-2536 chamber at (" + r\x + ", " + r\y + ", " + r\z + "), mesh=room1scp2536.rmesh"
End Function

;called every frame from UpdateIndevHazards
Function UpdateIndev2536()
	;if the permanent chamber (room1scp2536) is holding the tree this
	;seed, we skip the month gate and the office-room placement - the
	;tree already exists, and we just run the interaction loop below
	If Not I2536ChamberActive Then
		;month gate - only in December
		If I2536CheckedMonth = 0 Then
			If Indev2536InDec() Then I2536CheckedMonth = 1 Else I2536CheckedMonth = 2
		EndIf
		If I2536CheckedMonth <> 1 Then Return

		;first office room the player walks into during December gets the tree
		If (Not I2536Placed) And KillTimer >= 0 Then
			If IndevXmasIsOfficeRoom(PlayerRoom) Then
				Indev2536Manifest(PlayerRoom)
			EndIf
			Return
		EndIf
	EndIf

	;while manifested: play music, apply mild stress near the tree, run
	;the vanish timer if the player leaves and never picks up the gift
	If I2536Room = Null Then Return

	If PlayerRoom = I2536Room And KillTimer >= 0 Then
		;stress from proximity (the song, the plastic, the uncanny cheer)
		If I2536Tree <> 0 Then
			Local d# = EntityDistance(Collider, I2536Tree)
			If d < 4.0 Then IndevStress = Min(100, IndevStress + FPSfactor * 0.04)
		EndIf
		;reset the vanish timer while the player is present
		I2536Timer = 0
	Else
		;player has left. The permanent chamber never vanishes; only the
		;transient office manifestation does.
		If Not I2536ChamberActive Then
			I2536Timer = I2536Timer + FPSfactor
			If I2536Timer > 70.0 * 60.0 * 3.0 Then Indev2536Vanish()
		EndIf
	EndIf

	;pull up music while the player is in the room
	Local want# = 0
	If PlayerRoom = I2536Room And KillTimer >= 0 Then want = 0.6

	If I2536MusicCHN <> 0 Then
		SetStreamVolume_Strict(I2536MusicCHN, want * SFXVolume)
	ElseIf want > 0.01 Then
		I2536MusicCHN = StreamSound_Strict("SFX\Radio\ChristmasOn-Site Radio.ogg", want * SFXVolume)
	EndIf

	;pick up the gift by walking onto it (permanent chamber's gift respawns
	;every visit; the office manifestation's gift is one-shot)
	If (Not I2536Taken) And I2536Gift <> 0 And KillTimer >= 0 Then
		If PlayerRoom = I2536Room Then
			Local dg# = EntityDistance(Collider, I2536Gift)
			If dg < 0.8 Then Indev2536Open()
		EndIf
	EndIf
End Function

Function Indev2536Manifest(r.Rooms)
	I2536Room = r
	I2536Placed = True
	I2536Timer = 0

	;place tree slightly off centre so the player doesn't spawn inside it.
	;Same 0.75 scale as the chamber version - stops it clipping the
	;ceiling of small office rooms.
	I2536Tree = LoadMesh_Strict("GFX\map\Props\scp2536tree.b3d", r\obj)
	PositionEntity(I2536Tree, r\x + 1.2, r\y, r\z - 1.6, True)
	ScaleEntity(I2536Tree, RoomScale * 0.75, RoomScale * 0.75, RoomScale * 0.75, True)
	EntityType(I2536Tree, HIT_MAP)

	I2536Gift = LoadMesh_Strict("GFX\map\Props\scp2536gift.b3d", r\obj)
	PositionEntity(I2536Gift, r\x + 1.2, r\y, r\z - 0.9, True)
	ScaleEntity(I2536Gift, RoomScale, RoomScale, RoomScale, True)
	EntityType(I2536Gift, HIT_MAP)

	Msg = "A plastic Christmas tree stands in the corner. It was not there a second ago. Something under it is wrapped in purple paper."
	MsgTimer = 70 * 6

	DebugLog "Indev: SCP-2536 manifested in room " + r\RoomTemplate\Name + " at (" + r\x + ", " + r\y + ", " + r\z + ")"
End Function

;the player walked onto the present - open it, get a gift, tree stays
Function Indev2536Open()
	I2536Taken = True

	;capture WHERE the gift box was standing before removing it - the
	;item drops right there instead of at the player's chest, which
	;kept letting it snap through the floor or into the tree mesh
	Local gx#, gy#, gz#
	If I2536Gift <> 0 Then
		gx = EntityX(I2536Gift, True)
		gy = EntityY(I2536Gift, True)
		gz = EntityZ(I2536Gift, True)
		FreeEntity(I2536Gift)
		I2536Gift = 0
	Else
		gx = EntityX(Collider, True)
		gy = EntityY(Collider, True)
		gz = EntityZ(Collider, True)
	EndIf

	;pick a gift keyed to what the player is short on right now. Vanilla-
	;first: the picker uses standard existing items rather than inventing new ones.
	Local gift$ = Indev2536PickGift()

	;drop the item from just above the box so it lands on the floor
	;instead of clipping through it. 0.4 m up is enough clearance to
	;not spawn inside another mesh but not enough to fall from ceiling.
	Local it.Items = CreateItem(gift, gx, gy + 0.4, gz)
	If it <> Null Then
		EntityParent(it\collider, I2536Room\obj)
		it\DropSpeed = 0.0  ;start the physics drop from rest so items land clean
	EndIf

	Msg = "The wrapping paper falls away by itself. Inside: exactly what you needed."
	MsgTimer = 70 * 6

	DebugLog "Indev: SCP-2536-1 opened, gift = " + gift + " at (" + gx + ", " + gy + ", " + gz + ")"
End Function

;pick the item that best matches what the player is missing
Function Indev2536PickGift$()
	;heavily injured -> firstaid
	If Injuries > 30 Or Bloodloss > 30 Then Return "firstaid"
	;infected -> SCP-500
	If Infect > 30 Then Return "scp500"
	;stressed -> pill
	If IndevStress > 50 Then Return "scp420j"
	;otherwise something showy: a Level 4 keycard fits the SCP-770 chain
	;and is genuinely useful
	Return "key4"
End Function

;dev command: force-spawn the tree+gift in a given room right now, no
;month gate, no room whitelist, no prior-state check. Called by the
;spawn2536 / 2536tree / testtree / xmastree console commands.
Function Indev2536TestSpawn(r.Rooms)
	If r = Null Then Return
	;wipe any existing instance first so it doesn't leak entities
	If I2536Tree <> 0 Then FreeEntity(I2536Tree) : I2536Tree = 0
	If I2536Gift <> 0 Then FreeEntity(I2536Gift) : I2536Gift = 0

	I2536Room = r
	I2536Placed = True
	I2536ChamberActive = True    ;so the vanish timer never fires - dev spawn is permanent
	I2536Taken = False
	I2536Timer = 0

	I2536Tree = LoadMesh_Strict("GFX\map\Props\scp2536tree.b3d", r\obj)
	PositionEntity(I2536Tree, EntityX(Collider, True), EntityY(Collider, True) - 0.4, EntityZ(Collider, True) - 1.5, True)
	ScaleEntity(I2536Tree, RoomScale * 0.5, RoomScale * 0.5, RoomScale * 0.5, True)
	EntityType(I2536Tree, HIT_MAP)
	EntityParent(I2536Tree, r\obj)

	I2536Gift = LoadMesh_Strict("GFX\map\Props\scp2536gift.b3d", r\obj)
	PositionEntity(I2536Gift, EntityX(Collider, True), EntityY(Collider, True) - 0.4, EntityZ(Collider, True) - 0.9, True)
	ScaleEntity(I2536Gift, RoomScale, RoomScale, RoomScale, True)
	EntityType(I2536Gift, HIT_MAP)
	EntityParent(I2536Gift, r\obj)

	DebugLog "Indev: Indev2536TestSpawn - dev-spawned tree+gift in " + r\RoomTemplate\Name
End Function

Function Indev2536Vanish()
	If I2536Tree <> 0 Then FreeEntity(I2536Tree) : I2536Tree = 0
	If I2536Gift <> 0 Then FreeEntity(I2536Gift) : I2536Gift = 0
	If I2536MusicCHN <> 0 Then
		StopStream_Strict(I2536MusicCHN)
		I2536MusicCHN = 0
	EndIf
	;NOTE: I2536Placed stays True so it doesn't respawn the same run
	I2536Room = Null

	Msg = "You come back. It's gone. The song is still stuck in your head."
	MsgTimer = 70 * 5

	DebugLog "Indev: SCP-2536 vanished after 3-minute abandonment"
End Function
