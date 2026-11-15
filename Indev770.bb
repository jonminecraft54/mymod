;=====================================================================
; SCP: Containment Breach - Indev SCP-770 "Radiosynthetic Mould"
;
;   Blue-glowing slime mould stored in a small iron-56 flask. Respires
;   without oxygen by chewing on heavy isotopes and spitting out ionising
;   radiation. Reads "sealed" while the flask stopper is on and the lead
;   caddy is closed; reads "unsealed" while you are handling it or after
;   its stopper has been knocked loose in SCP-914.
;
;   Purpose:     a slow, expensive time-pressure item. It is the fastest
;                +infect / +bloodloss source in the mod when carried
;                unsealed, and the fastest thing you can feed to SCP-914
;                to force an interesting outcome.
;   Effect:      carried sealed - nothing (heavy, that's it)
;                carried unsealed - infect +, bloodloss +, stress +
;                in the room, whether or not carried - ambient dose while
;                you stand nearby
;   Drawback:    ionising radiation. It will kill you if you carry it
;                unsealed for more than a couple of rooms
;   Reason to carry: fastest 914 "very fine" fuel; a Level 5 keycard
;                drops from the recipe (radiation-hardened key). Also
;                the only cognitohazard-free light source in a blackout.
;   Spawn:       the room1scp770 chamber only (one per map)
;
;   Vanilla-first: reuses Injuries, Bloodloss, Infect, IndevStress,
;   IndevPillMsg, item state, the existing beaker mesh, PointLight for
;   the glow. No new key binds. Wired into Indev914Refine via
;   Indev914Refine770.
;=====================================================================

Global I770Room.Rooms
Global I770Flask.Items          ;the flask sitting in the chamber (before pickup)
Global I770Light%                ;point light on the flask
Global I770LightRoom%            ;point light while carried unsealed
Global I770DoseTimer#            ;house-keeping tick

Function Indev770Reset()
	I770Room = Null : I770Flask = Null
	I770Light = 0 : I770LightRoom = 0
	I770DoseTimer = 0
End Function

;keypad code retained (used to be for the interior vault door). The door
;itself was removed after in-game testing showed it clipping into the
;rmesh geometry - the authored corridor of room1scp770 is offset from
;the room centre in a way that made a centred CreateDoor collide with
;walls no matter how it was rotated. Keeping the code function around
;so the note770 texture still gets a per-seed number drawn on it in
;case we want to bring the door back later.
Function Indev770Code%()
	Local c% = (AccessCode * 11 + 7700) Mod 10000
	If c < 1000 Then c = c + 1000
	If c = AccessCode Or c = Indev914Code() Or c = Indev268Code() Or c = IndevOffices2Code() Then c = c + 17
	Return c
End Function

;spawned by MapSystem's Case "room1scp770"
Function IndevFill770(r.Rooms)
	I770Room = r
	DebugLog "Indev: IndevFill770 running for room1scp770 at (" + r\x + ", " + r\y + ", " + r\z + ")"

	;The flask sits on the observation desk.
	;Interior door additions were removed - CreateDoor's coordinates in
	;the rmesh authoring space kept clipping into walls, and without
	;knowing the exact corridor offset from the mesh centre it was safer
	;to leave the room's authored geometry alone. The corridor door
	;(placed by CreateDoors from the rmesh's own connection) is
	;upgraded to L4 keycard by IndevSetup770Doors below.
	Local it.Items
	it = CreateItem("scp770", r\x - 220.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 40.0 * RoomScale)
	EntityParent(it\collider, r\obj)
	it\state = 0 ;sealed
	I770Flask = it

	;a soft blue point light on the flask so the player can find it in the dark
	I770Light = CreateLight(2, r\obj)
	LightColor(I770Light, 40, 120, 255)
	LightRange(I770Light, 4.0)
	PositionEntity(I770Light, r\x - 220.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 40.0 * RoomScale, True)

	;doc770 next to the flask
	Local d.Items = CreateItem("doc770", r\x - 100.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 40.0 * RoomScale)
	EntityParent(d\collider, r\obj)
End Function

;the chamber's approach door is the vanilla old-Indev door for zone 4.
;CreateDoor made it with a plain ButtonOBJ though (because keycard=0 at
;create time), so the physical button model is a small round button, not
;a keycard reader panel. This function:
;  1. Sets the door's KeyCard field to Level 4.
;  2. Swaps its two buttons in-place with ButtonKeyOBJ (the wall-mounted
;     card reader panel), preserving position and rotation.
;  3. Marks it locked so it will actually enforce the keycard check.
;Level 4 (not 5) is intentional: Level 4 drops from SCP-173-B's practice
;session, forming the chain
;   173-B  ->  Level 4  ->  770 chamber door  ->  flask  ->  914 very fine
;   ->  Level 5 (radiation-hardened key)
;Level 5 would deadlock - the only Level 5 in the mod is the flask reward
;itself, and it lives behind this same door.
Function IndevSetup770Doors()
	Local d.Doors, count% = 0, i%, px#, py#, pz#, ry#
	For d = Each Doors
		If d\room <> Null Then
			If d\room\RoomTemplate <> Null Then
				If d\room\RoomTemplate\Name = "room1scp770" Then
					If d\KeyCard = 4 Then
						;already upgraded on a previous invocation (quick reload)
						count = count + 1
					Else
						d\KeyCard = 4
						d\Code = ""
						d\Locked = True
						;swap the plain button for a proper keycard reader panel
						For i = 0 To 1
							If d\buttons[i] <> 0 Then
								px = EntityX(d\buttons[i], True)
								py = EntityY(d\buttons[i], True)
								pz = EntityZ(d\buttons[i], True)
								ry = EntityYaw(d\buttons[i], True)
								FreeEntity(d\buttons[i])
								d\buttons[i] = CopyEntity(ButtonKeyOBJ)
								ScaleEntity(d\buttons[i], 0.03, 0.03, 0.03)
								PositionEntity(d\buttons[i], px, py, pz, True)
								RotateEntity(d\buttons[i], 0, ry, 0, True)
								EntityParent(d\buttons[i], d\frameobj)
								EntityPickMode(d\buttons[i], 2)
							EndIf
						Next
						count = count + 1
					EndIf
				EndIf
			EndIf
		EndIf
	Next
	DebugLog "Indev: IndevSetup770Doors upgraded " + count + " corridor door(s) on room1scp770 to L4 keycard"
End Function

;UpdateIndev770 and IndevUse770 already exist in IndevHazards.bb:
;the flask, when opened from inventory, releases a growing patch of
;radiosynthetic mould via IndevRelease770 - this is exactly the
;"unstable containment" mechanic we wanted.

;--- SCP-914 recipes for the flask
Function Indev914Refine770(item.Items, setting$, x#, y#, z#)
	Local it2.Items
	Select setting
		Case "rough"
			;shatters. Spawns the note500 sample style: a wet blue decal + a big infect+bloodloss spike right now.
			IndevPillMsg("SCP-914 grinds the flask to slag. Blue light leaks from the intake bay. Get out of the room.", 7)
			Injuries = Injuries + 45
			Bloodloss = Min(100, Bloodloss + 45)
			Infect = Min(100, Infect + 60)
			IndevStress = Min(100, IndevStress + 30)
			RemoveItem(item)
		Case "coarse"
			;stopper falls out
			item\state = 1
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			IndevPillMsg("SCP-914 pops the stopper off cleanly and slides the flask back onto the tray. It is unsealed.", 5)
		Case "fine"
			;stopper reseated, but no reward
			item\state = 0
			PositionEntity(item\collider, x, y, z) : ResetEntity(item\collider)
			IndevPillMsg("SCP-914 reseats the stopper. The flask is cold again.", 5)
		Case "very fine"
			;THE recipe: sealed flask + very fine = radiation-hardened Level 5 key
			it2 = CreateItem("key5", x, y, z)
			RemoveItem(item)
			IndevPillMsg("SCP-914 spits out a small metal key still glowing at the teeth. It works every door in this facility.", 8)
		Default
			it2 = CreateItem("cup", x, y, z)
			RemoveItem(item)
			IndevPillMsg("SCP-914 hands you back an ordinary empty beaker. The blue is gone.", 5)
	End Select
End Function
