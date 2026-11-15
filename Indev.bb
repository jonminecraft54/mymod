;=====================================================================
; SCP: Containment Breach - Indev core systems
;
; Small, self-contained mechanics for the reduced Indev roster:
;   - SCP-079 : the facility AI (lights, doors, cameras, alarms, half-truths)
;   - SCP-513 : a phantom bell the player may or may not have heard
;   - SCP-990 : an extremely rare dream while resting (holding the blink key)
;   - SCP-106 : corrodes doors open or seals rooms after an encounter
;
; Nothing here is saved: timers are re-rolled on new game / load, and any
; doors sealed by SCP-106 are unsealed before saving.
;=====================================================================

Type IndevLockedDoor
	Field d.Doors
End Type

Global Indev079Timer#, Indev079Elapsed#
Global Indev513Active%, Indev513Timer#, Indev513Rings%, Indev513Room.Rooms, Indev513Pivot%
Global Indev990Rest#, Indev990Cooldown#, Indev990State#, Indev990Variant%, Indev990Seen%, Indev990CHN%, Indev990Elapsed#
Global Indev106Init%, Indev106Prev#, Indev106Room.Rooms, Indev106Pending%, Indev106LockTimer#
Global Indev173Started%, Indev173SightTimer#
Global Indev990Room.Rooms, Indev990RoomPicked%, Indev990RoomFelt%
Global Indev6833State%, Indev6833Timer#
Global Indev8319Taken%
Global Indev096Photo%, Indev096PhotoTimer#, Indev096PhotoBlurred%, Indev096PhotoWarned% ;the SCP-096 photograph document
Global IndevCogOn%, IndevCogSanity# ;Cognitive Filter Glasses (IndevHazards.bb)
Global Indev2077Doses%, Indev2077Timer#, Indev2077Last%
Global Indev5604Timer#, Indev5604Stage%, Indev5604Next#
Global Indev7985Doses%, Indev7985FogTimer#, Indev7985Timer#, Indev7985Last%

;newGame = False when loading a save: SCP-173 keeps the position stored in the save
Function IndevReset(newGame% = True, keepWorld% = False)
	IndevUnlockDoors()

	;LoadGameQuick reloads the save into the map that's already built, so the props, screens and pick targets
	;made in FillRoom / on the first frame still exist. Remember them and hand them back after the reset.
	Local k993TV%, k993Screen%, k993Pick%, k993Room.Rooms
	Local k719TV%, k719Screen%, k719Pick%, k719Room.Rooms
	Local k718Stalk%, k718Eye%, k718Room.Rooms, k718Alive%
	Local k738Room.Rooms, k738Desk%, k738Chair%, k738Throne%, k738Tex%
	Local k330Bowl%, k330Room.Rooms, k330Tex%, k330Pick%
	Local k122Obj%, k122Glow%, k122Room.Rooms, k122Pick%
	Local k513Pivot%, kNR1Room.Rooms, kNR1State%, kNR2Room.Rooms, kNR8Room.Rooms, kNR65Room.Rooms, kNR65Hollow%, kNR65Head%
	If keepWorld Then
		k993TV = I993TV : k993Screen = I993Screen : k993Pick = I993Pick : k993Room = I993Room
		k719TV = I719TV : k719Screen = I719Screen : k719Pick = I719Pick : k719Room = I719Room
		k718Stalk = I718Stalk : k718Eye = I718Eye : k718Room = I718Room : k718Alive = I718Alive
		k738Room = I738Room : k738Desk = I738Desk : k738Chair = I738Chair : k738Throne = I738Throne : k738Tex = I738Tex
		k330Bowl = I330Bowl : k330Room = I330Room : k330Tex = I330Tex : k330Pick = I330Pick
		k122Obj = I122Obj : k122Glow = I122Glow : k122Room = I122Room : k122Pick = I122Pick
		k513Pivot = Indev513Pivot
		kNR1Room = INR1Room : kNR1State = INR1State : kNR2Room = INR2Room : kNR8Room = INR8Room
		kNR65Room = INR65Room : kNR65Hollow = INR65Hollow : kNR65Head = INR65Head
		Local p.I770Patch
		For p = Each I770Patch
			If p\spr <> 0 Then FreeEntity(p\spr)
		Next
	EndIf

	Indev173Started = (Not newGame)
	Indev096Photo = False : Indev096PhotoTimer = 0 : Indev096PhotoBlurred = False : Indev096PhotoWarned = False
	Indev173SightTimer = 70*60*Rnd(3,5)

	;the rooms don't exist yet, the SCP-990 area is picked on the first update
	Indev990Room = Null
	Indev990RoomPicked = False
	Indev990RoomFelt = False

	Indev079Timer = 70*60*Rnd(3,5)
	Indev079Elapsed = 0

	;only about a third of the runs ever hear the bell, and those hear it once. The roll is made for a new game
	;only: loading or quick-loading keeps it, so reloading can't bring the bell back again and again
	If newGame Then
		Indev513Active = (Rand(100) <= 35)
		Indev513Timer = 70*60*Rnd(8,25)
		Indev513Rings = 0
	EndIf
	Indev513Room = Null
	Indev513Pivot = 0 ;entities are freed with the world, just forget the old handle

	Indev990Rest = 0
	Indev990Cooldown = 0
	Indev990State = 0
	Indev990Variant = 0
	Indev990Seen = 0
	Indev990Elapsed = 0
	Indev990CHN = 0

	Indev106Init = False
	Indev106Room = Null
	Indev106Pending = False
	Indev106LockTimer = 0

	Indev6833State = 0
	Indev6833Timer = 0
	Indev8319Taken = 0
	Indev2077Doses = 0
	Indev2077Timer = 0
	Indev2077Last = 0
	Indev5604Timer = 0
	Indev5604Stage = 0
	Indev5604Next = 0
	Indev7985Doses = 0
	Indev7985FogTimer = 0
	Indev7985Timer = 0
	Indev7985Last = 0
	IndevPillsReset()
	Indev993Reset()
	Indev738Reset()
	Indev330Reset()
	IndevHazardsReset()
	IndevStressReset()
	IndevMemoryReset()
	Indev2107Reset()
	Indev983Reset(newGame)
	Indev29Reset(newGame) ;SCP-120's configuration, SCP-867's seed, SCP-820-JP (IndevU29.bb)
	Indev30Reset(newGame) ;Site-42: SCP-4427's count and trait, SCP-4433's calls (IndevU30.bb)
	Indev31Reset(newGame) ;SCP-467 and the five items of batch 31 (IndevU31.bb)
	Indev32Reset(newGame) ;Gate V (IndevU32.bb)
	Indev33Reset(newGame) ;batch 33: SCP storage and VAULT 4612 (IndevU33.bb)
	Indev34Reset(newGame) ;batch 34: deep storage areas 06-09 (IndevU34.bb)
	Indev35Reset(newGame) ;batch 35: storage areas 10-11 (IndevU35.bb)
	Indev36Reset(newGame) ;batch 36: confectionery and SCP-1479 (IndevU36.bb)
	Indev37Reset(newGame) ;batch 37: SCP-028, reactor, archive, hall, cells (IndevU37.bb)
	Indev45Reset(newGame) ;batch 45: old 939, morgue, off-shoot hall, damaged wing (IndevU45.bb)
	Indev50Reset(newGame) ;batch 50 research complex (IndevU50.bb)
	Indev49Reset(newGame) ;batch 49 SCP-087-B (IndevU49.bb)
	Indev48Reset(newGame) ;batch 48 SCP-806 (IndevU48.bb)
	Indev47Reset(newGame) ;batch 47 legacy rooms (IndevU47.bb)
	Indev689Reset(newGame) ;the old SCP-689 room (Indev689.bb)
	Indev46Reset(newGame) ;batch 46: alternate timeline (IndevU46.bb)
	Indev44Reset(newGame) ;batch 44: old SCP-1074 wing and five sites (IndevU44.bb)
	Indev43Reset(newGame) ;batch 43: lift lobby, checkpoint, offices (IndevU43.bb)
	Indev42Reset(newGame) ;batch 42: Panopticon, Toy Box, Vault, Cellar (IndevU42.bb)
	Indev41Reset(newGame) ;batch 41: staff, medical, security, recreation, D-block (IndevU41.bb)
	Indev40Reset(newGame) ;batch 40: the Residential Sector (IndevU40.bb)
	Indev39Reset(newGame) ;batch 39: research, Warehouse B, Test Containment 4 (IndevU39.bb)
	Indev38Reset(newGame) ;batch 38: long hallway, SCP-1039/1148 display hall, SCP-1117 party (IndevU38.bb)
	IndevMetersReset()
	Indev122Reset()
	Indev202Reset()
	Indev693Reset()
	Indev113Reset()
	Indev109Reset()
	Indev963Reset()
	Indev458Reset()
	Indev268Reset()
	Indev173BReset()
	Indev085Reset()
	Indev1155Reset()
	Indev770Reset()
	Indev2536Reset()
	Indev2935Reset()
	Indev140Reset()
	IndevAnnex2Reset()
	IndevRoomExtrasReset()
	IndevXmasReset()
	IndevOffices2Reset()
	IndevNewRoom1Reset()
	IndevNewRoom2Reset()
	Indev1074Reset(keepWorld)
	IndevOldBillReset(keepWorld)
	IndevNewRoom8Reset()
	IndevNewRoom65Reset()
	IndevMjolnirReset()
	IndevArmorReset()
	IndevBlinkReset()

	If keepWorld Then
		I993TV = k993TV : I993Screen = k993Screen : I993Pick = k993Pick : I993Room = k993Room
		If I993Screen <> 0 And I993TexS1 <> 0 Then EntityTexture(I993Screen, I993TexS1)
		I719TV = k719TV : I719Screen = k719Screen : I719Pick = k719Pick : I719Room = k719Room
		If I719Screen <> 0 Then EntityTexture(I719Screen, I719Tex[8]) : EntityColor(I719Screen, 255, 255, 255)
		I718Stalk = k718Stalk : I718Eye = k718Eye : I718Room = k718Room : I718Alive = k718Alive
		I738Room = k738Room : I738Desk = k738Desk : I738Chair = k738Chair : I738Throne = k738Throne : I738Tex = k738Tex
		If I738Throne <> 0 Then I738PlaceThrone()
		I330Bowl = k330Bowl : I330Room = k330Room : I330Tex = k330Tex : I330Pick = k330Pick
		I122Obj = k122Obj : I122Glow = k122Glow : I122Room = k122Room : I122Pick = k122Pick
		If I122Glow <> 0 Then I122SetLit(I122Powered())
		Indev513Pivot = k513Pivot
		INR1Room = kNR1Room
		INR2Room = kNR2Room
		INR8Room = kNR8Room
		INR65Room = kNR65Room : INR65Hollow = kNR65Hollow : INR65Head = kNR65Head
		If INR65Hollow <> 0 Then HideEntity(INR65Hollow)
		If kNR1State > 0 Then INR1State = 6 ;already happened on this map
	EndIf
End Function

;true when the player is within maxDist and aiming at a prop: the camera pick hits it (or its pick
;pivot), or the view direction passes within ~18 degrees of the pivot. Blocked while a menu/item is open.
Function IndevAimedAt%(ent%, pick%, maxDist#)
	If ent = 0 Or pick = 0 Then Return False
	If EntityDistance(Camera, pick) > maxDist Then Return False
	If InvOpen Or OtherOpen <> Null Or SelectedItem <> Null Or MenuOpen Then Return False
	Local p% = EntityPick(Camera, maxDist)
	If p <> 0 And (p = ent Or p = pick) Then Return True
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dx# = EntityX(pick, True) - EntityX(Camera, True)
	Local dy# = EntityY(pick, True) - EntityY(Camera, True)
	Local dz# = EntityZ(pick, True) - EntityZ(Camera, True)
	Local l# = Sqr(dx * dx + dy * dy + dz * dz)
	If l < 0.001 Then Return True
	Return ((fx * dx + fy * dy + fz * dz) / l > 0.95)
End Function

;SCP-914 chamber keypad code: derived from the run's access code so it changes every game
Function Indev914Code%()
	Local c% = (AccessCode * 7 + 914) Mod 10000
	If c < 1000 Then c = c + 1000
	If c = AccessCode Or c = HARPCODE Then c = c + 1
	Return c
End Function

Function UpdateIndev()
	If KillTimer < 0 Then IndevPillsOnDeath() : Return
	If FPSfactor <= 0 Then Return
	If PlayerRoom = Null Then Return

	Local RN$ = PlayerRoom\RoomTemplate\Name

	If (Not Indev990RoomPicked) Then IndevPick990Room()

	IndevUpdate990(RN)
	IndevUpdate106(RN)
	IndevUpdate6833()
	IndevUpdate2077()
	IndevUpdate096Photo()
	IndevUpdate5604()
	IndevUpdate7985()
	UpdateIndevPills()
	UpdateIndev993()
	UpdateIndev738()
	UpdateIndev330()
	UpdateIndevHazards()

	If Indev990State > 0 Then Return
	If RN = "173" Or RN = "pocketdimension" Or RN = "gatea" Or RN = "dimension1499" Then Return
	If RN = "exit1" And EntityY(Collider) > 1040.0*RoomScale Then Return

	IndevUpdate173(RN)
	IndevUpdate079()
	IndevUpdate513(RN)
End Function

;---------------------------------------------------------------------
; SCP-173 - random starting location & distant sightings
;---------------------------------------------------------------------

Function IndevUpdate173(RN$)
	If Curr173 = Null Then Return
	If Curr173\Idle <> 0 Then Return ;an event is scripting it right now

	;the first time the player leaves the containment chamber, 173 is somewhere else entirely
	If (Not Indev173Started) Then
		If RN <> "start" Then
			Indev173Started = True
			If (Not IndevPlace173(20.0, 45.0, False, True)) Then IndevPlace173(15.0, 60.0, False, False)
		EndIf
		Return
	EndIf

	;occasional distant sightings: 173 standing at the far end of a corridor, watching
	Indev173SightTimer = Indev173SightTimer - FPSfactor
	If Indev173SightTimer > 0 Then Return

	If EntityDistance(Curr173\Collider, Collider) > 20.0 And BlinkTimer > 0 Then
		If IndevPlace173(11.0, 16.0, True, False) Then
			Indev173SightTimer = 70*60*Rnd(4,8)
		Else
			Indev173SightTimer = 70*20 ;no good spot right now, try again soon
		EndIf
	Else
		Indev173SightTimer = 70*60 ;it's already close, no need for a reminder
	EndIf
End Function

;moves SCP-173 to a random waypoint between minDist and maxDist from the player
;inView  : the spot has to be in plain sight of the player (a "sighting")
;lczOnly : only Light Containment rooms
Function IndevPlace173%(minDist#, maxDist#, inView%, lczOnly%)
	Local w.WayPoints, dist#, count% = 0, pick% = 0, wy#, pass%, ok%
	Local pvt% = CreatePivot()

	;two passes: count the valid spots, then pick one of them at random
	For pass = 0 To 1
		If pass = 1 Then
			If count = 0 Then Exit
			pick = Rand(1, count)
			count = 0
		EndIf

		For w = Each WayPoints
			If w\door = Null And w\room <> Null Then
				If w\room <> PlayerRoom And ((Not lczOnly) Or w\room\zone = 1) Then
					wy = EntityY(w\obj, True)
					;stay on ground level, 173 is clamped below y=0.35 anyway
					If wy > -0.5 And wy < 0.5 Then
						dist = EntityDistance(w\obj, Collider)
						If dist > minDist And dist < maxDist Then
							ok = True
							If inView Then
								PositionEntity pvt, EntityX(w\obj, True), wy + 0.5, EntityZ(w\obj, True)
								ok = EntityInView(pvt, Camera)
								If ok Then ok = EntityVisible(Camera, pvt)
							EndIf
							If ok Then
								count = count + 1
								If pass = 1 And count = pick Then
									PositionEntity Curr173\Collider, EntityX(w\obj, True), wy + 0.25, EntityZ(w\obj, True)
									ResetEntity Curr173\Collider
									;facing the player
									PointEntity Curr173\Collider, Collider
									RotateEntity Curr173\Collider, 0, EntityYaw(Curr173\Collider), 0
									Curr173\EnemyX = 0 : Curr173\EnemyY = 0 : Curr173\EnemyZ = 0
									FreeEntity pvt
									DebugLog "Indev: SCP-173 moved to "+w\room\RoomTemplate\Name
									Return True
								EndIf
							EndIf
						EndIf
					EndIf
				EndIf
			EndIf
		Next
	Next

	FreeEntity pvt
	Return False
End Function

;---------------------------------------------------------------------
; SCP-079
;---------------------------------------------------------------------

Function IndevUpdate079()
	Indev079Elapsed = Indev079Elapsed + FPSfactor
	;079 only starts meddling once the player has had a couple of minutes to get going
	If Indev079Elapsed < 70*60*2 Then Return

	Indev079Timer = Indev079Timer - FPSfactor
	If Indev079Timer > 0 Then Return

	;SCP-5604's memetic effect: the facility's records no longer match the player,
	;so 079 can't single them out - no doors shut on them, no cameras tracking them
	If Indev5604Timer > 0 Then
		Indev079Timer = 70*Rnd(60,120)
		If Rand(2) = 1 Then
			Msg = I_Loc\Message079_5604
			MsgTimer = 70*5
			PlaySound_Strict(LoadTempSound("SFX\SCP\079\Broadcast"+Rand(1,7)+".ogg"))
		Else
			LightBlink = Rnd(0.5,1.5)
		EndIf
		Return
	EndIf

	;the security systems get more active the deeper the player goes
	Select PlayerZone
		Case 0
			Indev079Timer = 70*Rnd(150,240)
		Case 1
			Indev079Timer = 70*Rnd(90,160)
		Default
			Indev079Timer = 70*Rnd(60,110)
	End Select

	Select Rand(1,7)
		Case 1 ;lights
			LightBlink = Rnd(2.0,4.0)
			If Rand(2) = 1 Then PlaySound_Strict(LoadTempSound("SFX\SCP\079\Broadcast"+Rand(1,7)+".ogg"))
		Case 2 ;shut a door somewhere behind the player
			If (Not IndevCloseDoor()) Then LightBlink = Rnd(1.0,2.0)
		Case 3 ;occasionally, a useful door
			If Rand(3) = 1 Then
				If (Not IndevOpenDoor()) Then IndevMessage079()
			Else
				IndevMessage079()
			EndIf
		Case 4 ;alarm
			PlaySound_Strict(LoadTempSound("SFX\Alarm\Alarm"+Rand(3,5)+".ogg"))
			LightBlink = Rnd(0.5,1.5)
		Case 5 ;cameras
			IndevCameras079()
		Default ;half-truths
			IndevMessage079()
	End Select
End Function

Function IndevCloseDoor%()
	Local d.Doors, best.Doors = Null, bestDist# = 99.0, dist#

	For d = Each Doors
		If d\obj <> 0 And d\open And (Not d\locked) And (Not d\IsElevatorDoor) And d\Code = "" Then
			If d\openstate >= 180.0 Then
				dist = EntityDistance(d\obj, Collider)
				If dist > 3.0 And dist < 9.0 And dist < bestDist Then best = d : bestDist = dist
			EndIf
		EndIf
	Next

	If best = Null Then Return False

	best\open = False
	best\SoundCHN = PlaySound2(CloseDoorSFX(best\dir, Rand(0,2)), Camera, best\obj)
	Return True
End Function

Function IndevOpenDoor%()
	Local d.Doors, best.Doors = Null, bestDist# = 99.0, dist#

	For d = Each Doors
		If d\obj <> 0 And d\KeyCard > 0 And (Not d\open) And (Not d\locked) And (Not d\IsElevatorDoor) And d\Code = "" Then
			dist = EntityDistance(d\obj, Collider)
			If dist < 6.0 And dist < bestDist Then best = d : bestDist = dist
		EndIf
	Next

	If best = Null Then Return False

	best\open = True
	best\SoundCHN = PlaySound2(LoadTempSound("SFX\Door\DoorOpen079.ogg"), Camera, best\obj)
	Msg = "[SCP-079] ACCESS GRANTED."
	MsgTimer = 70*4
	Return True
End Function

Function IndevCameras079()
	Local sc.SecurityCams, found% = False

	For sc = Each SecurityCams
		If sc\room <> Null And sc <> CoffinCam Then
			If sc\room = PlayerRoom Or sc\room\dist < 8.0 Then
				sc\FollowPlayer = True
				found = True
				;079 can push SCP-895's feed onto any screen that is not shielded
				If sc\CoffinEffect = 2 Then sc\CoffinEffect = 3 : sc\PlayerState = 0
			EndIf
		EndIf
	Next

	If found Then
		Msg = "[SCP-079] I SEE YOU."
		MsgTimer = 70*4
	Else
		LightBlink = Rnd(1.0,2.5)
	EndIf
End Function

Function IndevMessage079()
	Local code$ = Str(AccessCode)

	Select Rand(1,9)
		Case 1
			Msg = "[SCP-079] SECTOR CLEAR. NO HOSTILE ENTITIES DETECTED."
		Case 2
			Msg = "[SCP-079] SCP-173 CONTAINMENT STATUS: RESTORED."
		Case 3
			Msg = "[SCP-079] GATE B LOCKDOWN LIFTED. PROCEED TO EXIT."
		Case 4
			Msg = "[SCP-079] YOU ARE NOT THE ONLY ONE HERE."
		Case 5
			Msg = "[SCP-079] CAMERA 6 IS SAFE. CAMERA 7 IS"
		Case 6
			Msg = "[SCP-079] SCP-106 LOCATION: UNKNOWN."
		Case 7 ;incomplete, but true
			Msg = "[SCP-079] MAINTENANCE CODE: " + Left(code, 2) + "??"
		Case 8 ;incomplete and possibly wrong
			Msg = "[SCP-079] MAINTENANCE CODE: ??" + Rand(0,9) + Right(code, 1)
		Default
			Msg = "[SCP-079] ERROR. ERROR. ERR"
	End Select
	MsgTimer = 70*6

	PlaySound_Strict(LoadTempSound("SFX\SCP\079\Broadcast"+Rand(1,7)+".ogg"))
End Function

;---------------------------------------------------------------------
; SCP-513 - "Did I actually hear that?"
;---------------------------------------------------------------------

Function IndevUpdate513(RN$)
	;the room where the bell was heard stays a little wrong
	If Indev513Room <> Null Then
		If PlayerRoom = Indev513Room Then
			;now and then a flicker - no more bells, it only rings once a playthrough
			If Rand(4200/FPSfactor) = 1 Then LightBlink = Rnd(0.4,1.0)
		EndIf
	EndIf

	If (Not Indev513Active) Or Indev513Rings >= 1 Then Return

	Indev513Timer = Indev513Timer - FPSfactor
	If Indev513Timer > 0 Then Return

	;never right next to the actual bell, that would give it away
	If RN = "room513" Then
		Indev513Timer = 70*30
		Return
	EndIf

	IndevRing513(1.0)
	Indev513Rings = Indev513Rings + 1
	Indev513Room = PlayerRoom

End Function

Function IndevRing513(volume#)
	If Indev513Pivot = 0 Then Indev513Pivot = CreatePivot()

	;somewhere behind the player, out of sight
	PositionEntity Indev513Pivot, EntityX(Collider), EntityY(Collider), EntityZ(Collider)
	RotateEntity Indev513Pivot, 0, EntityYaw(Camera) + 180 + Rnd(-50,50), 0
	MoveEntity Indev513Pivot, 0, 0, Rnd(4.0,7.0)

	PlaySound2(LoadTempSound("SFX\SCP\513\Bell"+Rand(1,3)+".ogg"), Camera, Indev513Pivot, 12.0, volume)
End Function

;---------------------------------------------------------------------
; SCP-990 - dream while resting (holding the blink key)
;---------------------------------------------------------------------

Function IndevUpdate990(RN$)
	If Indev990State > 0 Then
		Indev990State = Indev990State + FPSfactor

		;eyes stay shut, the player can't move, and SCP-173 plays fair
		BlinkTimer = -10
		UnableToMove = True
		If Curr173 <> Null Then
			If Curr173\Idle < 2 Then Curr173\IdleTimer = Max(Curr173\IdleTimer, 70*3)
		EndIf

		If Indev990State > 70*16 Then
			Indev990State = 0
			UnableToMove = False
			BlurTimer = 1200
			Msg = "You wake up with a start. How long were you out?"
			MsgTimer = 70*5
			If Indev990CHN <> 0 Then
				If ChannelPlaying(Indev990CHN) Then StopChannel(Indev990CHN)
				Indev990CHN = 0
			EndIf
		EndIf
		Return
	EndIf

	Indev990Elapsed = Indev990Elapsed + FPSfactor

	If Indev990Cooldown > 0 Then
		Indev990Cooldown = Indev990Cooldown - FPSfactor
		Indev990Rest = 0
		Return
	EndIf

	If Indev990Seen >= 2 Then Return
	If RN = "173" Or RN = "pocketdimension" Or RN = "gatea" Or RN = "exit1" Or RN = "dimension1499" Then
		Indev990Rest = 0
		Return
	EndIf

	;resting only counts when nothing is about to kill the player
	Local safe% = (Not IsAnyMenuOpen())
	If Curr173 <> Null Then
		If EntityDistance(Curr173\Collider, Collider) < 12.0 Then safe = False
	EndIf
	If Curr106 <> Null Then
		If Curr106\State <= 0 Then safe = False
	EndIf

	;the rare SCP-990 area: the air feels heavy, and resting here always leads to the dream
	Local inArea% = (Indev990Room <> Null And PlayerRoom = Indev990Room)
	If inArea And (Not Indev990RoomFelt) Then
		Indev990RoomFelt = True
		LightBlink = Rnd(0.5,1.0)
		Msg = "You suddenly feel very, very tired."
		MsgTimer = 70*5
	EndIf

	If KeyDown(KEY_BLINK) And BlinkTimer < 0 And safe Then
		Indev990Rest = Indev990Rest + FPSfactor
	Else
		Indev990Rest = 0
	EndIf

	If (inArea And Indev990Rest > 70*3) Then
		Indev990Rest = 0
		Indev990Cooldown = 70*90
		IndevStart990()
		Indev990Variant = 7 ;the area has its own dream
	ElseIf Indev990Rest > 70*6 Then
		Indev990Rest = 0
		Indev990Cooldown = 70*90
		If Indev990Elapsed > 70*60*8 And Rand(6) = 1 Then
			IndevStart990()
		Else
			Msg = "You rest your eyes for a moment."
			MsgTimer = 70*3
		EndIf
	EndIf
End Function

;picks the rare SCP-990 area for this run (or none): preferably a prototype room, otherwise a HCZ dead end
Function IndevPick990Room()
	Local r.Rooms, count% = 0, pick%, wanted$

	Indev990RoomPicked = True
	Indev990Room = Null

	wanted = "roompj"
	For r = Each Rooms
		If r\RoomTemplate\Name = wanted Then count = count + 1
	Next
	If count > 0 Then
		If Rand(10) > 3 Then Return ;30% of runs: the prototype room (now in every map) doubles as the dream area
	Else
		wanted = "endroom2"
		For r = Each Rooms
			If r\RoomTemplate\Name = wanted Then count = count + 1
		Next
		If count = 0 Or Rand(10) > 3 Then Return ;otherwise only ~30% of runs have one
	EndIf

	pick = Rand(1, count)
	count = 0
	For r = Each Rooms
		If r\RoomTemplate\Name = wanted Then
			count = count + 1
			If count = pick Then
				Indev990Room = r
				DebugLog "Indev: SCP-990 area is in "+wanted
				Return
			EndIf
		EndIf
	Next
End Function

Function IndevStart990()
	Indev990State = 1
	Indev990Seen = Indev990Seen + 1
	Indev990Variant = Rand(1,6)
	Indev990CHN = PlaySound_Strict(LoadTempSound("SFX\SCP\990\cwm"+Rand(1,2)+".cwm"))
End Function

Function Indev990Line$(variant%, i%)
	Local q$ = Chr(34)
	Local code$ = Str(AccessCode)

	Select variant
		Case 1
			Select i
				Case 0 Return "A man in a black suit is waiting at the end of the corridor."
				Case 1 Return q+"The machine is kinder on Fine than on Very Fine."+q
				Case 2 Return "He hands you a scrap of paper: " + Left(code, 2) + "__"
			End Select
		Case 2
			Select i
				Case 0 Return "Every screen in the room shows the same coffin."
				Case 1 Return q+"Don't watch the feeds that watch back."+q
				Case 2 Return q+"The screens in the security office are clean."+q
			End Select
		Case 3
			Select i
				Case 0 Return "The lights go out, one corridor at a time."
				Case 1 Return q+"The voice that runs this place doesn't lie."+q
				Case 2 Return q+"It just never finishes its sentences."+q
			End Select
		Case 4
			Select i
				Case 0 Return "You are back in your cell. The statue is facing the wall."
				Case 1 Return q+"It is patient. Keep your eyes open."+q
				Case 2 Return q+"Doors that close by themselves are not an accident."+q
			End Select
		Case 5
			Select i
				Case 0 Return "Somewhere, a bell rings in an empty room."
				Case 1 Return q+"There is nothing there."+q
				Case 2 Return q+"There was never anything there."+q
			End Select
		Case 8 ;SCP-474 - the dream is broadcast to every other sleeper on site
			Select i
				Case 0 Return "You are on a game show. The studio audience is everyone asleep on Site-19."
				Case 1 Return q+"Welcome back to Alexylva Late Night, live from your REM cycle!"+q
				Case 2 Return "Somewhere in the facility, a researcher wakes up humming the theme tune."
			End Select
		Case 7 ;only in the rare SCP-990 area
			Select i
				Case 0 Return "You are asleep in this exact room. Someone is sitting next to you."
				Case 1 Return q+"The code is "+code+". Don't tell the machine."+q
				Case 2 Return "He stands up and leaves through a door that isn't there."
			End Select
		Default
			Select i
				Case 0 Return "THIS AREA IS NOT FINISHED"
				Case 1 Return q+"...placeholder."+q
				Case 2 Return "The man in the suit apologises and turns off the lights."
			End Select
	End Select
	Return ""
End Function

Function DrawIndev()
	DrawIndev738()
	DrawIndev1074()
	DrawIndevNewRoom8()
	DrawIndev993()
	DrawIndev173B()
	DrawIndev085()
	If Indev990State <= 0 Then Return

	Local i%, t$, shown#, c#

	SetFont Font1
	For i = 0 To 2
		t = Indev990Line(Indev990Variant, i)
		shown = Indev990State - (70*1.5 + i*70*3.5)
		If t <> "" And shown > 0 Then
			c = Min(shown*3.0, 200.0)
			;fade out right before waking up
			If Indev990State > 70*14 Then c = c * Max(0.0, (70*16 - Indev990State) / (70*2.0))
			Color c, c, c
			Text GraphicWidth/2, GraphicHeight/2 - 50*MenuScale + i*35*MenuScale, t, True, True
		EndIf
	Next
	Color 255, 255, 255
End Function

;---------------------------------------------------------------------
; SCP-106 - corroded paths
;---------------------------------------------------------------------

Function IndevUpdate106(RN$)
	If Curr106 = Null Then Return

	If Indev106LockTimer > 0 Then
		Indev106LockTimer = Indev106LockTimer - FPSfactor
		If Indev106LockTimer <= 0 Then IndevUnlockDoors()
	EndIf

	If Contained106 Then Return

	If (Not Indev106Init) Then
		Indev106Prev = Curr106\State
		Indev106Init = True
	EndIf

	If Curr106\State <= 0 Then
		;SCP-106 is out - remember where the player met it
		If RN <> "pocketdimension" Then Indev106Room = PlayerRoom
	ElseIf Indev106Prev <= 0 Then
		;SCP-106 just sank back into the floor
		If Indev106Room <> Null Then Indev106Pending = True
	EndIf
	Indev106Prev = Curr106\State

	;wait until the player has left the room before touching its doors
	If Indev106Pending And Indev106Room <> Null Then
		If PlayerRoom <> Indev106Room And RN <> "pocketdimension" Then
			IndevCorrodeRoom(Indev106Room)
			Indev106Pending = False
			Indev106Room = Null
		EndIf
	EndIf
End Function

Function IndevCorrodeRoom(r.Rooms)
	Select r\RoomTemplate\Name
		Case "173", "start", "pocketdimension", "gatea", "gateaentrance", "exit1", "room106", "room079", "room2ccont", "room2nuke", "room2sl", "checkpoint1", "checkpoint2", "room2checkpointindev", "914", "dimension1499"
			Return
	End Select

	Local d.Doors, ld.IndevLockedDoor, count% = 0

	If Rand(2) = 1 Then
		;the residue eats through a card reader - a new path opens
		For d = Each Doors
			If d\room = r And d\obj <> 0 And d\KeyCard > 0 And (Not d\open) And (Not d\locked) And (Not d\IsElevatorDoor) And d\Code = "" Then
				d\KeyCard = 0
				d\open = True
				Msg = "A card reader nearby fizzles, eaten through by black residue."
				MsgTimer = 70*5
				Return
			EndIf
		Next
	EndIf

	;otherwise the room is sealed off for a while
	For d = Each Doors
		If d\room = r And d\obj <> 0 And (Not d\locked) And (Not d\IsElevatorDoor) And d\Code = "" Then
			If EntityDistance(d\obj, Collider) > 2.5 Then
				d\open = False
				d\locked = True
				ld = New IndevLockedDoor
				ld\d = d
				count = count + 1
			EndIf
		EndIf
	Next

	If count > 0 Then
		Indev106LockTimer = 70*90
		Msg = "Somewhere behind you, metal hisses and corrodes shut."
		MsgTimer = 70*5
	EndIf
End Function

Function IndevUnlockDoors()
	Local ld.IndevLockedDoor
	For ld = Each IndevLockedDoor
		If ld\d <> Null Then ld\d\locked = False
		Delete ld
	Next
	Indev106LockTimer = 0
End Function

;---------------------------------------------------------------------
; SCP-6833 - black tablet: a wormhole forms at the bladder, all future
; urine drains into SCP-6833-A. For the player it's a short sequence of
; sensations, then the occasional murmur from 73 planes below.
;---------------------------------------------------------------------

;---------------------------------------------------------------------
; SCP-2077 - "The Stuff Industry" pills. Each one works as advertised.
; Keep taking them (3+) and the body starts shedding and replacing
; itself: injuries heal, but for a moment your limbs aren't yours.
;---------------------------------------------------------------------

;---------------------------------------------------------------------
; SCP-5604 - "R-IN" methaqualone. Sedative (drowsy, winded, blurry),
; the face and personality rearrange themselves, and a memetic effect
; stops the facility's records from matching you (see IndevUpdate079).
; Extra doses extend the effect (capped at 10 minutes).
;---------------------------------------------------------------------

Function IndevTake5604()
	If Indev5604Timer <= 0 Then
		Indev5604Stage = 0
		Indev5604Next = 70*Rnd(20,35)
	EndIf
	Indev5604Timer = Min(Indev5604Timer + 70*60*Rnd(3,4), 70*60*10)

	;the drug itself: sedative-hypnotic
	BlinkEffect = 1.6 : BlinkEffectTimer = 60
	StaminaEffect = 1.8 : StaminaEffectTimer = 90
	BlurTimer = 70*4
End Function

Function IndevUpdate5604()
	If Indev5604Timer <= 0 Then Return

	Indev5604Timer = Indev5604Timer - FPSfactor
	If Indev5604Timer <= 0 Then
		Msg = I_Loc\MessageItem_Pill5604Wear
		MsgTimer = 70*6
		Return
	EndIf

	;the transformation, one step at a time
	If Indev5604Stage < 3 Then
		Indev5604Next = Indev5604Next - FPSfactor
		If Indev5604Next <= 0 Then
			Indev5604Stage = Indev5604Stage + 1
			Msg = I_Loc\MessageItem_Pill5604Effect[Indev5604Stage]
			MsgTimer = 70*6
			If Indev5604Stage = 1 Then CameraShake = 1.5 : BlurTimer = 70*2
			Indev5604Next = 70*Rnd(35,60)
		EndIf
	EndIf
End Function

;---------------------------------------------------------------------
; SCP-7985 - Mylex pills. Each dose is a mild stimulant that fogs your
; thinking. Keep taking them (3+) and branded slogans start replacing
; your thoughts; at 6+ the hive-mind occasionally takes the wheel.
;---------------------------------------------------------------------

Const INDEV7985_SLOGANS% = 3
Const INDEV7985_HIVE% = 6

Function IndevTake7985()
	Indev7985Doses = Indev7985Doses + 1

	;stimulant: second wind, slower stamina drain, eyes stay open longer
	Stamina = 100
	StaminaEffect = 0.5 : StaminaEffectTimer = 120
	BlinkEffect = 0.8 : BlinkEffectTimer = 60

	;...but thinking gets harder
	Indev7985FogTimer = 70*Rnd(15,25)

	If Indev7985Doses = INDEV7985_SLOGANS Then
		Msg = Msg + " " + I_Loc\MessageItem_Pill7985Warn
		MsgTimer = 70*8
		Indev7985Timer = 70*Rnd(40,70)
	ElseIf Indev7985Doses > INDEV7985_SLOGANS Then
		Indev7985Timer = Min(Indev7985Timer, 70*Rnd(30,50))
	EndIf
End Function

Function IndevUpdate7985()
	If Indev7985Doses = 0 Then Return

	If Indev7985FogTimer > 0 Then
		Indev7985FogTimer = Indev7985FogTimer - FPSfactor
		If Indev7985FogTimer <= 0 Then
			Msg = I_Loc\MessageItem_Pill7985Fog
			MsgTimer = 70*5
			BlurTimer = 70*3
		EndIf
	EndIf

	If Indev7985Doses < INDEV7985_SLOGANS Then Return

	Indev7985Timer = Indev7985Timer - FPSfactor
	If Indev7985Timer > 0 Then Return

	If Indev7985Doses >= INDEV7985_HIVE And Rand(3) = 1 Then
		;loss of agency: the body just... stops, and smiles
		Msg = I_Loc\MessageItem_Pill7985Hive
		MsgTimer = 70*7
		CurrSpeed = 0
		Stamina = 0
		BlurTimer = 70*5
		CameraShake = 1.0
	Else
		;more doses = the slogans get more possessive
		Local maxSlogan% = Min(Indev7985Doses - INDEV7985_SLOGANS + 2, 5)
		Local s% = Rand(1, maxSlogan)
		If s = Indev7985Last Then s = (s Mod maxSlogan) + 1
		Indev7985Last = s
		Msg = I_Loc\MessageItem_Pill7985Slogan[s]
		MsgTimer = 70*5
	EndIf

	Indev7985Timer = 70*60*Rnd(2,4) / Max(1.0, (Indev7985Doses - INDEV7985_SLOGANS) * 0.5 + 1.0)
End Function

Const INDEV2077_THRESHOLD% = 3

Function IndevTake2077()
	Indev2077Doses = Indev2077Doses + 1
	If Indev2077Doses = INDEV2077_THRESHOLD Then
		Msg = Msg + " " + I_Loc\MessageItem_PillUse2077Warn
		Indev2077Timer = 70*Rnd(45,90)
	ElseIf Indev2077Doses > INDEV2077_THRESHOLD Then
		;every extra dose brings the next episode closer
		Indev2077Timer = Min(Indev2077Timer, 70*Rnd(30,60))
	EndIf
End Function

;Attachment 096-A: an unredacted photo of SCP-096's face. Looking at it (opening the document) is
;the same as seeing the face - SCP-096 is cut from the facility, so it wakes up somewhere else and comes for you.
Function IndevUpdate096Photo()
	If Indev096PhotoTimer > 0 Then
		Indev096PhotoTimer = Indev096PhotoTimer - FPSfactor
		If Indev096PhotoTimer <= 0 Then
			Msg = "Somewhere far away, something is screaming. It's getting closer."
			MsgTimer = 70*6
		EndIf
	EndIf
	If SelectedItem = Null Then Indev096PhotoWarned = False : Return
	If SelectedItem\itemtemplate\name <> "doc096photo" Then Return

	;the Cognitive Filter Glasses turn the photograph into an unreadable grey smear:
	;swap the document image (reloaded by the paper drawing code) whenever the glasses go on or off
	Local it.ItemTemplates = SelectedItem\itemtemplate
	If IndevCogOn <> Indev096PhotoBlurred Or it\img = 0 Then
		Local want$ = "GFX\items\doc096photo.jpg"
		If IndevCogOn Then want = "GFX\items\doc096photo_cf.jpg"
		If it\imgpath <> want Then
			If it\img <> 0 Then FreeImage(it\img)
			it\img = 0
			it\imgpath = want
		EndIf
		Indev096PhotoBlurred = IndevCogOn
	EndIf

	If IndevCogOn Then
		If Not Indev096PhotoWarned Then
			Indev096PhotoWarned = True
			Msg = "Through the filter lenses the photograph is just a grey, shapeless smear. Probably for the best."
			MsgTimer = 70*5
		EndIf
		Return
	EndIf

	If Indev096Photo Then Return
	Indev096Photo = True
	IndevTrigger096()
End Function

Function IndevTrigger096()
	Local n.NPCs = Curr096
	If n = Null Then
		;wake it in a room a good distance away, so the scream arrives before it does
		Local r.Rooms, pick.Rooms = Null, best# = 0, d#
		For r = Each Rooms
			If r <> PlayerRoom Then
				d = Distance(EntityX(Collider), EntityZ(Collider), r\x, r\z)
				If d > 16 And d < 40 And r\RoomTemplate\Name <> "pocketdimension" And r\RoomTemplate\Name <> "gatea" And r\RoomTemplate\Name <> "dimension1499" Then
					If pick = Null Or Rand(3) = 1 Then pick = r
				EndIf
				If d > best Then best = d
			EndIf
		Next
		If pick = Null Then
			For r = Each Rooms
				If r <> PlayerRoom Then pick = r : Exit
			Next
		EndIf
		If pick = Null Then Return
		n = CreateNPC(NPCtype096, pick\x, pick\y + 0.5, pick\z)
		Curr096 = n
	EndIf
	If n\State = 0 Or n\State = 5 Then
		n\Frame = 194
		n\State = 1
		n\State3 = 0
		If n\SoundChn <> 0 Then
			StopStream_Strict(n\SoundChn) : n\SoundChn = 0 : n\SoundChn_IsStream = False
		EndIf
		n\Sound = 0
	EndIf
	n\Target = Null
	PlaySound_Strict LoadTempSound("SFX\SCP\096\Triggered.ogg")
	CurrCameraZoom = 10
	BlurTimer = 70*2
	Msg = "You look at the photograph. A pale, gaunt face, hands clawing at its own head. You saw its face."
	MsgTimer = 70*6
	Indev096PhotoTimer = 70*8
End Function

Function IndevUpdate2077()
	If Indev2077Doses < INDEV2077_THRESHOLD Then Return

	Indev2077Timer = Indev2077Timer - FPSfactor
	If Indev2077Timer > 0 Then Return

	;pick a symptom, never the same one twice in a row
	Local e% = Rand(1,4)
	If e = Indev2077Last Then e = (e Mod 4) + 1
	Indev2077Last = e

	Msg = I_Loc\MessageItem_Pill2077Effect[e]
	MsgTimer = 70*7

	;the replaced tissue comes back healthy
	Injuries = Max(0, Injuries - 0.5)

	;autotopagnosia: you can't place your own limbs for a while
	Local severity# = Min(Indev2077Doses - INDEV2077_THRESHOLD + 1, 4)
	CameraShake = 1.0 + severity * 0.5
	BlurTimer = 70*(2 + severity)
	Stamina = Min(Stamina, 50 - severity * 8)
	CurrSpeed = 0

	;the more you've taken, the more often it happens
	Indev2077Timer = 70*60*Rnd(4,7) / severity
End Function

Function IndevTake6833()
	Indev6833State = 1
	Indev6833Timer = 70*Rnd(25,40)
End Function

Function IndevUpdate6833()
	If Indev6833State = 0 Then Return

	Indev6833Timer = Indev6833Timer - FPSfactor
	If Indev6833Timer > 0 Then Return

	Select Indev6833State
		Case 1 ;the powder reaches the bladder and folds into a wormhole
			Msg = I_Loc\MessageItem_Pill6833Effect[1]
			MsgTimer = 70*6
			CameraShake = 1.5
			BlurTimer = 70*3
			Stamina = Stamina - 15
			Indev6833State = 2
			Indev6833Timer = 70*Rnd(60,90)
		Case 2
			Msg = I_Loc\MessageItem_Pill6833Effect[2]
			MsgTimer = 70*7
			Indev6833State = 3
			Indev6833Timer = 70*60*Rnd(4,8)
		Case 3 ;SCP-6833-B, heard through the Way every few minutes
			Msg = I_Loc\MessageItem_Pill6833Effect[3]
			MsgTimer = 70*6
			CameraShake = 0.5
			Indev6833Timer = 70*60*Rnd(6,12)
	End Select
End Function

;on-screen messages are drawn as one centred line; anything wider than the screen is wrapped at spaces here.
;grow -1: the lines stack upwards from y (the last one sits on y), 1: downwards from y
Function IndevDrawMsg(x#, y#, txt$, bright%, grow%)
	Local L$[12], n% = 0, rest$ = txt, cut%, k%, i%, maxw% = GraphicWidth - 80, lh%, ly#
	If StringWidth(txt) <= maxw Then
		Color 0, 0, 0
		Text(x + 1, y + 1, txt, True, False)
		Color bright, bright, bright
		Text(x, y, txt, True, False)
		Return
	EndIf
	While rest <> "" And n < 12
		If StringWidth(rest) <= maxw Then
			L[n] = rest
			rest = ""
		Else
			;the last space that still fits
			cut = 0
			k = Instr(rest, " ")
			While k > 0
				If StringWidth(Left(rest, k - 1)) > maxw Then Exit
				cut = k
				k = Instr(rest, " ", k + 1)
			Wend
			If cut = 0 Then
				cut = Instr(rest, " ")
				If cut = 0 Then cut = Len(rest) + 1
			EndIf
			L[n] = Left(rest, cut - 1)
			rest = Mid(rest, cut + 1)
		EndIf
		n = n + 1
	Wend
	lh = FontHeight() + 4
	For i = 0 To n - 1
		If grow < 0 Then
			ly = y - (n - 1 - i) * lh
		Else
			ly = y + i * lh
		EndIf
		Color 0, 0, 0
		Text(x + 1, ly + 1, L[i], True, False)
		Color bright, bright, bright
		Text(x, ly, L[i], True, False)
	Next
End Function
