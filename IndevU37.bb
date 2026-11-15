;=====================================================================
; SCP: Containment Breach - Indev: the thirty-seventh batch - SCP-028, the reactor, the deep archive,
; the balcony hall and the cell block (rooms from the user's reference images 132-138)
;
;   room1scp028      SCP-028 "Knowledge": stand in the invisible 2 m cube at the centre of the sealed room in the
;                    abandoned yard and, after a few seconds, you simply know something - a keypad code, the
;                    layout of the facility for five rooms round you, or an SCP-914 recipe nobody wrote down.
;                    Every exposure dumps memory to make room: IndevMemory jumps a whole stage (IndevMemory.bb).
;                    From the third exposure on, migraines and dizziness.
;   room2b39reactor  the heavy water pool: radiation over the whole hall (IHzIrradiate, IndevHazards.bb); without a
;                    hazmat suit or the MJOLNIR armour it is fatal in 45 seconds. A service lift goes down to the
;                    pool-floor walkway, where the sealed tray holds SCP-006-B.
;   room2b39archive  twelve motorised shelves that shift every 20-35 s: caught between them, you are crushed
;                    (Injuries + Bloodloss); they also block the line of sight of anything hunting you.
;   room2b39hall     the balcony hall: a staff lift, two D-class on the floor, a guard on the balcony
;   room2b39cells    D-block: a D-class in Cell 1; in the shutter next to Cell 6, someone knocks back
;   Summary of scp-wiki.wikidot.com/scp-028 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I37Uses%, I37Inside%, I37Wait#, I37Recipe%, I37Codes%, I37Migraine#
Global I37Dose#, I37InReactor%, I37InArchive%, I37InYard%
Global I37Aisle%, I37CrushCD#, I37Knocks%, I37Vent%
Global I37Water% = 0, I37WaterTex% = 0
Dim I37Shelf%(11), I37ShelfZ#(11)

Function Indev37Reset(newGame%)
	If newGame Then
		I37Uses = 0 : I37Recipe = False : I37Codes = 0 : I37Knocks = 0 : I37Vent = False
	EndIf
	I37Inside = False : I37Wait = 0 : I37Migraine = 0 : I37Dose = 0 : I37CrushCD = 0
	I37InReactor = False : I37InArchive = False : I37InYard = False
	;the shelves and the pool water are made with the room (IndevU37Dress) and survive a quick load
End Function

;room units of the player inside room r. The map generator turns a room AFTER FillRoom, so this goes through
;the room mesh's own transform (scaled by RoomScale, rotated by r\angle) - right at any rotation.
Function U37LX#(r.Rooms)
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, r\obj)
	Return TFormedX()
End Function
Function U37LY#(r.Rooms)
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, r\obj)
	Return TFormedY()
End Function
Function U37LZ#(r.Rooms)
	TFormPoint(EntityX(Collider, True), EntityY(Collider, True), EntityZ(Collider, True), 0, r\obj)
	Return TFormedZ()
End Function

;put an entity at room units (lx, ly, lz) of room r, whatever way the room is turned
Function IxPlace(ent%, r.Rooms, lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, r\obj, 0)
	PositionEntity(ent, TFormedX(), TFormedY(), TFormedZ(), True)
End Function

Function U37ShelfTarget#(i%)
	If i < I37Aisle Then Return -955.0 + 90.0 * i
	Return 955.0 - 90.0 * (11 - i)
End Function

Function IndevU37Dress(r.Rooms)
	Local i%, tex%
	Select r\RoomTemplate\Name
		Case "room2b39archive"
			tex = LoadTexture_Strict("GFX\map\indev_b37files.png", 1)
			If tex <> 0 Then ScaleTexture(tex, 0.5, 0.5)
			I37Aisle = 6
			For i = 0 To 11
				I37Shelf(i) = CreateCube()
				ScaleEntity(I37Shelf(i), 280 * RoomScale, 300 * RoomScale, 44 * RoomScale)
				If tex <> 0 Then EntityTexture(I37Shelf(i), tex)
				EntityColor(I37Shelf(i), 200, 200, 196)
				EntityType(I37Shelf(i), HIT_MAP)
				EntityPickMode(I37Shelf(i), 2, True)          ;blocks line of sight, like a wall
				I37ShelfZ(i) = U37ShelfTarget(i)
				PositionEntity(I37Shelf(i), r\x + 620 * RoomScale, r\y + 300 * RoomScale, r\z + I37ShelfZ(i) * RoomScale, True)
				EntityParent(I37Shelf(i), r\obj, True)
			Next
			If tex <> 0 Then FreeTexture(tex)
		Case "room2b39reactor"
			I37Water = CreateCube()
			ScaleEntity(I37Water, 220 * RoomScale, 0.002, 700 * RoomScale)
			I37WaterTex = LoadTexture_Strict("GFX\map\indev_b37water.png", 1)
			If I37WaterTex <> 0 Then
				ScaleTexture(I37WaterTex, 0.25, 0.25)
				EntityTexture(I37Water, I37WaterTex)
			EndIf
			EntityFX(I37Water, 1)
			EntityBlend(I37Water, 3)
			EntityAlpha(I37Water, 0.8)
			PositionEntity(I37Water, r\x + 780 * RoomScale, r\y - 470 * RoomScale, r\z - 300 * RoomScale, True)
			EntityParent(I37Water, r\obj, True)
	End Select
End Function

Function UpdateIndevU37(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room1scp028" : U37Knowledge(e)
		Case "room2b39reactor" : U37Reactor(e)
		Case "room2b39archive" : U37Archive(e)
		Case "room2b39hall" : U37Hall(e)
		Case "room2b39cells" : U37Cells(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- SCP-028
Function U37Knowledge(e.Events)
	Local r.Rooms = e\room, lx#, lz#, inCube%
	If PlayerRoom <> r Then
		I37InYard = False : I37Inside = False : I37Wait = 0
		Return
	EndIf
	lx = U37LX(r) : lz = U37LZ(r)
	I37InYard = (lx > 260)
	inCube = (Abs(lx - 660) < 120 And Abs(lz) < 120 And U37LY(r) < 300)
	If inCube Then
		If Not I37Inside Then
			I37Wait = I37Wait + FPSfactor
			If I37Wait > 70 * 4 Then
				I37Inside = True
				U37Epiphany()
			EndIf
		EndIf
	Else
		If I37Wait > 0 And (Not I37Inside) Then IS16Tell("Nothing. Just a dusty floor. Then you're out of the middle of the room, and the hum in your ears stops.", 5)
		I37Wait = 0 : I37Inside = False
	EndIf
	If IS10Press(r\Objects[U37_K28_SEAL], 1.6) Then
		IS16Tell("SCP-028. NO ENTRY WITHOUT AUTHORISATION. Personnel found inside the containment room will be detained indefinitely.", 7)
	EndIf
	If IS10Press(r\Objects[U37_K28_CAMS], 2.0) Then
		IS16Tell("A camera over the door, its red light steady. Somewhere, someone is watching the supply room.", 5)
	EndIf
End Function

;one exposure: a white flash, one piece of knowledge, and a whole stage of memory dumped to make room for it
Function U37Epiphany()
	Local s%, k%, code$, rr.Rooms, px%, pz%, gx%, gz%, n%
	I37Uses = I37Uses + 1
	LightFlash = 2.0 : BlurTimer = 70 * 3
	IS10Sound("SFX\Indev\clicks.wav", Collider, 4.0, 0.6)
	k = Rand(3)
	If I37Uses = 1 Then k = 1
	Select k
		Case 1
			I37Codes = I37Codes + 1
			Select I37Codes
				Case 1 : code = Str(AccessCode) + " - the code to the nearest keypad lock on the containment doors"
				Case 2 : code = Str(Indev914Code()) + " - the keypad by SCP-914"
				Case 3 : code = Str(Indev268Code()) + " - the keypad on SCP-268's locker"
				Default : code = Str(IndevOffices2Code()) + " - the offices' keypad"
			End Select
			IS16Tell("WHITE. Then a number, as plain as your own name: " + code + ". It's in your notes before you know you wrote it.", 10)
			IAxSay("Your notes", "CODE: " + code, 8)
		Case 2
			px = Floor(EntityX(Collider, True) / 8.0) : pz = Floor(EntityZ(Collider, True) / 8.0)
			For rr = Each Rooms
				gx = Floor(EntityX(rr\obj) / 8.0) : gz = Floor(EntityZ(rr\obj) / 8.0)
				If Abs(gx - px) <= 5 And Abs(gz - pz) <= 5 Then
					MapFound(gx, gz) = Max(MapFound(gx, gz), 1)
					n = n + 1
				EndIf
			Next
			IS16Tell("WHITE. Then the facility, laid out in your head like a drawing: " + n + " rooms round you, every corridor, every turn. Your map has caught up with you.", 10)
		Default
			I37Recipe = True
			IS16Tell("WHITE. Then a recipe nobody wrote down: SCP-006 concentrate, Very Fine, comes back from SCP-914 as SCP-500. You don't know how you know. You just do.", 10)
	End Select
	;memory: the brain dumps a whole stage to fit it in
	s = IndevMemoryStageOf(IndevMemory)
	If s < 7 Then
		IndevMemory = Min(100, s * 15 + 1)
		IndevMemoryShown = IndevMemory
		IndevMemoryTell("Something you knew this morning is gone. A name? A face? There's a clean, empty space where it was.")
	EndIf
	;after two exposures, it starts to hurt
	If I37Uses > 2 Then
		I37Migraine = 70 * (12 + 6 * (I37Uses - 2))
		Injuries = Injuries + 0.15 * (I37Uses - 2)
		IS16Tell("A migraine like a nail behind your eye. The floor tilts. Maybe that's enough knowing for one day.", 6)
	EndIf
End Function

;SCP-914 (IndevPills.bb): the recipe SCP-028 teaches - SCP-006-B on Very Fine makes SCP-500
Function Indev914Refine37%(item.Items, setting$, x#, y#, z#)
	Local it2.Items
	If Not I37Recipe Then Return False
	If setting <> "very fine" Then Return False
	it2 = CreateItem("scp500", x, y, z)
	RemoveItem(item)
	IndevPillMsg("SCP-914 hums for a long time. In the output booth: a single red pill. You knew it would be.", 7)
	Return True
End Function

;--------------------------------------------------------------------------------------------- reactor
Function U37Reactor(e.Events)
	Local r.Rooms = e\room, lx#, ly#, rate#, prot%
	If I37Water <> 0 And I37WaterTex <> 0 And r\dist < 10 Then
		PositionTexture(I37WaterTex, (MilliSecs() Mod 9000) / 9000.0, (MilliSecs() Mod 13000) / 13000.0)
	EndIf
	If PlayerRoom <> r Then
		I37InReactor = False
		Return
	EndIf
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	lx = U37LX(r) : ly = U37LY(r)
	I37InReactor = (lx > 256)
	If I37InReactor And KillTimer >= 0 Then
		rate = 0.06
		If ly < -300 Then rate = 0.1
		IHzIrradiate(rate)
		prot = (WearingHazmat > 0 Or IndevMjolnirOn)
		If Not prot Then
			I37Dose = I37Dose + FPSfactor
			If I37Dose - FPSfactor <= 0 Then IS16Tell("The blue light off the pool. Your dosimeter screams. Without a suit, this hall kills you in under a minute.", 7)
			If I37Dose > 70 * 20 And I37Dose - FPSfactor <= 70 * 20 Then IS16Tell("Your skin prickles everywhere at once. You taste metal.", 5)
			If I37Dose > 70 * 35 And I37Dose - FPSfactor <= 70 * 35 Then
				IS16Tell("You are vomiting. Your hands are red. Get out. Get out now.", 5)
				BlurTimer = 70 * 6
			EndIf
			If I37Dose > 70 * 45 Then
				DeathMSG = "Subject D-9341 was found on the gantry of the Heavy Containment reactor hall without protective equipment. The body was too contaminated to recover; the hall has been sealed."
				Kill()
			EndIf
		EndIf
	Else
		If I37Dose > 0 Then I37Dose = Max(0, I37Dose - FPSfactor * 0.25)
	EndIf
	If IS10Press(r\Objects[U37_RCT_TRAY], 1.6) Then
		IS16Tell("THE SEALED SAMPLE TRAY. Items lifted off the pool floor by the crane. One vial, labelled SCP-006-B - CONCENTRATE. HANDLE WITH TONGS.", 7)
	EndIf
	If IS10Press(r\Objects[U37_RCT_CRANE], 1.8) Then
		IS16Tell("The crane console: RETRIEVAL ARM PARKED. The service lift is slow on purpose - lead-lined cab. Wait for it.", 6)
	EndIf
	If IS10Press(r\Objects[U37_RCT_POOL], 2.4) Then
		IS16Tell("Heavy water, very clear, very still. The core glows at the bottom like something breathing.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- archive
Function U37Archive(e.Events)
	Local r.Rooms = e\room, i%, lx#, lz#, t#, d#, moving% = False, a%
	If r\dist > 14 Or I37Shelf(0) = 0 Then Return
	;the shelves glide towards their places on the tracks
	For i = 0 To 11
		t = U37ShelfTarget(i)
		d = t - I37ShelfZ(i)
		If Abs(d) > 0.5 Then
			moving = True
			I37ShelfZ(i) = I37ShelfZ(i) + Sgn(d) * Min(Abs(d), 1.6 * FPSfactor)
			IxPlace(I37Shelf(i), r, 620, 300, I37ShelfZ(i))
		EndIf
	Next
	If PlayerRoom <> r Then
		I37InArchive = False
		Return
	EndIf
	lx = U37LX(r) : lz = U37LZ(r)
	I37InArchive = (lx > 256)
	;a new file requested: the open aisle moves
	e\EventState3 = e\EventState3 - FPSfactor
	If e\EventState3 <= 0 Then
		e\EventState3 = 70 * Rnd(20, 35)
		a = Rand(0, 12)
		If a = I37Aisle Then a = (a + 5) Mod 13
		I37Aisle = a
		If I37InArchive Then
			IS10Sound("SFX\Indev\creak.wav", I37Shelf(Min(a, 11)), 10.0, 0.9)
			IS16Tell("A klaxon chirps twice and the motors start. The shelves are moving.", 4)
		EndIf
	EndIf
	;crushed between shelves
	If I37CrushCD > 0 Then I37CrushCD = I37CrushCD - FPSfactor
	If moving And I37InArchive And lx > 320 And lx < 920 And I37CrushCD <= 0 And KillTimer >= 0 Then
		For i = 0 To 11
			If Abs(lz - I37ShelfZ(i)) < 44 + 26 Then
				I37CrushCD = 70 * 3
				Injuries = Injuries + 1.4
				Bloodloss = Min(100, Bloodloss + 35)
				CameraShake = 3.0 : BlurTimer = 70 * 4
				IS10Sound("SFX\Indev\creak.wav", Collider, 6.0, 1.0)
				IS16Tell("The shelves close on you. Steel and paper and your own ribs. They grind back an inch, and you drag yourself out into the cross aisle.", 7)
				DeathMSG = "Subject D-9341 was found between two motorised shelves in the Entrance Zone deep archive. Cause of death: crush asphyxia. The shelves' safety beam had been disabled."
				IxPlace(Collider, r, 300, U37LY(r), lz)
				ResetEntity(Collider)
				Exit
			EndIf
		Next
	EndIf
	;the old tubes
	e\EventState2 = e\EventState2 - FPSfactor
	If e\EventState2 <= 0 Then
		e\EventState2 = 70 * Rnd(4, 12)
		If I37InArchive Then LightBlink = Rnd(0.6, 1.2)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- balcony hall
Function U37Hall(e.Events)
	Local r.Rooms = e\room, n.NPCs, k%
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		For k = 0 To 1
			n = CreateNPC(NPCtypeD, EntityX(r\Objects[U37_HAL_DCLASS], True), EntityY(r\Objects[U37_HAL_DCLASS], True) + 0.3, EntityZ(r\Objects[U37_HAL_DCLASS], True) + k * 0.8)
			n\State = 0
			RotateEntity(n\Collider, 0, 90, 0)
			r\NPC[k] = n
		Next
		n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U37_HAL_GUARD], True), EntityY(r\Objects[U37_HAL_GUARD], True) + 0.35, EntityZ(r\Objects[U37_HAL_GUARD], True))
		n\State = 9
		RotateEntity(n\Collider, 0, 0, 0)
		r\NPC[2] = n
	EndIf
	;keep them at their posts, out of the walkways (no wandering into the player's path)
	U37Pin(r\NPC[0], r\Objects[U37_HAL_DCLASS], 0.0, 0.3)
	U37Pin(r\NPC[1], r\Objects[U37_HAL_DCLASS], 0.8, 0.3)
	U37Pin(r\NPC[2], r\Objects[U37_HAL_GUARD], 0.0, 0.35)
	If PlayerRoom <> r Then Return
	e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
	If IS10Press(r\Objects[U37_HAL_CAMH], 2.0) Then
		IS16Tell("A camera over the supply room. Under it, someone has written in marker: SMILE.", 5)
	EndIf
End Function

;an NPC that has drifted off its post (pivot p, dz world units along z) is put back; dead ones are left alone
Function U37Pin(n.NPCs, p%, dz#, dy#)
	Local x#, z#
	If n = Null Or p = 0 Then Return
	If n\IsDead Then Return
	x = EntityX(p, True) : z = EntityZ(p, True) + dz
	If Abs(EntityX(n\Collider, True) - x) + Abs(EntityZ(n\Collider, True) - z) > 0.25 Then
		PositionEntity(n\Collider, x, EntityY(p, True) + dy, z, True)
		ResetEntity(n\Collider)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- cells
Function U37Cells(e.Events)
	Local r.Rooms = e\room, n.NPCs
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		n = CreateNPC(NPCtypeD, EntityX(r\Objects[U37_CEL_DCELL], True), EntityY(r\Objects[U37_CEL_DCELL], True) + 0.3, EntityZ(r\Objects[U37_CEL_DCELL], True))
		n\State = 0
		RotateEntity(n\Collider, 0, 270, 0)
		r\NPC[0] = n
	EndIf
	U37Pin(r\NPC[0], r\Objects[U37_CEL_DCELL], 0.0, 0.3)
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U37_CEL_KNOCK], 1.8) Then
		I37Knocks = I37Knocks + 1
		IS10Sound("SFX\Indev\clicks.wav", r\Objects[U37_CEL_KNOCK], 5.0, 0.8)
		Select I37Knocks
			Case 1 : IS16Tell("You knock on the shutter. Three knocks come back - from the other side, at exactly your height.", 6)
			Case 2
				IndevStress = Min(100, IndevStress + 10)
				IS16Tell("You knock again. A voice, very close to the metal, says your name. The cell behind this shutter is empty. The rules say so.", 7)
			Default : IS16Tell("Silence. Then, slowly, the shutter flexes outwards, as if someone were leaning on it. You step back.", 6)
		End Select
	EndIf
	If IS10Press(r\Objects[U37_CEL_VENT6], 1.6) Then
		If Not I37Vent Then
			I37Vent = True
			IS16Give("docb37_cells", r\Objects[U37_CEL_VENT6])
			IS16Tell("The vent grille in Cell 6 is loose. Behind it, folded small, someone's copy of the cell rules - with a note scrawled on the back: IT ONLY KNOCKS WHEN YOU DO.", 8)
		Else
			IS16Tell("The vent is empty now. Cold air, and far off, knocking.", 4)
		EndIf
	EndIf
End Function

;called from IndevOutdoorFrame (IndevU26.bb): the dead stillness of SCP-028's yard, the archive's dust
Function U37Frame()
	If I37InYard Then
		CameraFogMode(Camera, 1)
		CameraFogRange(Camera, 0.6, 9.0)
		CameraFogColor(Camera, 128, 128, 124)
		CameraClsColor(Camera, 128, 128, 124)
		AmbientLight(Max(Brightness, 110), Max(Brightness, 110), Max(Brightness, 106))
	ElseIf I37InArchive Then
		CameraFogMode(Camera, 1)
		CameraFogRange(Camera, 1.0, 10.0)
		CameraFogColor(Camera, 62, 58, 50)
	ElseIf I37InReactor Then
		CameraFogColor(Camera, 10, 30, 60)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev37()
	If I37Migraine > 0 And KillTimer >= 0 Then
		I37Migraine = I37Migraine - FPSfactor
		CameraShake = Max(CameraShake, 0.4)
		If Rand(300) = 1 Then BlurTimer = Max(BlurTimer, 70 * 2)
	EndIf
End Function
