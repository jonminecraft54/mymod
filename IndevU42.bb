;=====================================================================
; SCP: Containment Breach - Indev: the forty-second batch - the Panopticon, the Toy Box, the Vault, the Cellar
;
;   room2b44panopticon  a D-class in an open cell, the dead in another; now and then, the feeling of the tower
;   room3b44toybox      SCP-127 groans and bites; SCP-439 - sit still by the terrarium too long and you doze, and
;                       it moves in (pinches, blurred spells; SCP-500 cures); SCP-1577-1, the flare gun (an item):
;                       a blinding flare, and a minute later (the hour, compressed) the aircraft comes over
;   room4b44vault       SCP-4139 - rearrange the magnets and the fridge does something else each time;
;                       SCP-154, the bracelets (an item): the bow of light
;   room2b44cellar      the detonator's locked cover; SCP-466 behind the glass - come close and the vessels hit it
;   Summaries of scp-wiki.wikidot.com/scp-127, -439, -1577, -154, -4139, -466 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I42Ear%, I42EarT#, I42Still#, I42PX#, I42PZ#, I42Plane#, I42Flares%, I42FridgeN%, I42Glass#, I42GlassCD#
Global I42Watch#

Function Indev42Reset(newGame%)
	If newGame Then
		I42Ear = False : I42Flares = 3 : I42FridgeN = 0
	EndIf
	I42EarT = 70 * 30 : I42Still = 0 : I42Plane = 0 : I42Glass = 0 : I42GlassCD = 0 : I42Watch = 70 * 40
End Function

Function IndevU42Dress(r.Rooms)
End Function

Function UpdateIndevU42(e.Events)
	Local r.Rooms = e\room, n.NPCs, d#
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		Select r\RoomTemplate\Name
			Case "room2b44panopticon"
				n = CreateNPC(NPCtypeD, EntityX(r\Objects[U42_PAN_OPEN1], True), EntityY(r\Objects[U42_PAN_OPEN1], True) + 0.3, EntityZ(r\Objects[U42_PAN_OPEN1], True))
				n\State = 0 : r\NPC[0] = n
				r\NPC[1] = U41Body(r, r\Objects[U42_PAN_OPEN2], 30)
			Case "room2b44cellar"
				n = CreateNPC(NPCtypeD, EntityX(r\Objects[U42_CEL_S466], True), EntityY(r\Objects[U42_CEL_S466], True) + 0.3, EntityZ(r\Objects[U42_CEL_S466], True))
				n\State = 0 : r\NPC[0] = n
				IAxSkin(n, "GFX\npcs\indev_b42veins.jpg")
		End Select
	EndIf
	Select r\RoomTemplate\Name
		Case "room2b44panopticon" : U37Pin(r\NPC[0], r\Objects[U42_PAN_OPEN1], 0.0, 0.3)
		Case "room2b44cellar" : U37Pin(r\NPC[0], r\Objects[U42_CEL_S466], 0.0, 0.3)
	End Select
	If PlayerRoom <> r Then Return
	Select r\RoomTemplate\Name
		;---------------- the Panopticon
		Case "room2b44panopticon"
			I42Watch = I42Watch - FPSfactor
			If I42Watch <= 0 Then
				I42Watch = 70 * Rnd(35, 60)
				IndevStress = Min(100, IndevStress + 3)
				IS16Tell("The tower's glass is dark. You can't see if anyone is in the cab. That's the point: you have to assume someone is.", 6)
			EndIf
			If IS10Press(r\Objects[U42_PAN_TOWER], 3.0) Then
				IS16Tell("The observation cab: every cell in the ring visible from up there, and nothing in the cab visible from down here. A light moves behind the glass. Then it doesn't.", 7)
			EndIf
		;---------------- the Toy Box
		Case "room3b44toybox"
			If IS10Press(r\Objects[U42_TOY_GUN], 1.6) Then
				Injuries = Injuries + 0.1 : CameraShake = 1.0
				IS16Tell("SCP-127 in its case: a compact submachine gun that breathes. You tap the glass. It groans, wet and low, and something like a tooth clicks against the inside of the case.", 7)
			EndIf
			If IS10Press(r\Objects[U42_TOY_TERRA], 1.6) Then
				IS16Tell("SCP-439's terrarium: grit, a twig, and a grey, almost see-through earwig that stops moving the moment you look. The test cot beside it has been stripped.", 7)
			EndIf
			;dozing off by the terrarium: crouched and still for twelve seconds
			d = EntityDistance(Collider, r\Objects[U42_TOY_TERRA])
			If d < 2.5 And Crouch And (Not I42Ear) And Abs(EntityX(Collider, True) - I42PX) + Abs(EntityZ(Collider, True) - I42PZ) < 0.02 Then
				I42Still = I42Still + FPSfactor
				If I42Still > 70 * 6 And I42Still - FPSfactor <= 70 * 6 Then IS16Tell("Your eyes are heavy. It's quiet in here. Very quiet.", 4)
				If I42Still > 70 * 12 Then
					I42Ear = True : I42Still = 0
					BlurTimer = 70 * 4
					IS16Tell("You jerk awake. Something dry and light is on your tongue - then it isn't. The terrarium lid is ajar. Your throat itches.", 8)
				EndIf
			Else
				I42Still = 0
			EndIf
			I42PX = EntityX(Collider, True) : I42PZ = EntityZ(Collider, True)
			If IS10Press(r\Objects[U42_TOY_TESTROOM], 3.0) Then
				IS16Tell("The test room is empty and very large. The ceiling is scorched in a long streak, as if something big flew low through it.", 6)
			EndIf
		;---------------- the Vault
		Case "room4b44vault"
			If IS10Press(r\Objects[U42_VLT_FRIDGE], 1.6) Then
				I42FridgeN = I42FridgeN + 1
				Select Rand(5)
					Case 1
						Stamina = 0 : BlurTimer = 70 * 2
						IS16Tell("You swap the rocket and the picnic. The door breathes out a blast of air so cold your eyelashes freeze.", 6)
					Case 2
						IndevStress = Min(100, IndevStress + 8)
						IS16Tell("You move the family drawing to the bottom. From inside the fridge, three slow knocks. You put it back.", 6)
					Case 3
						IS16Give("cup", r\Objects[U42_VLT_FRIDGE])
						IS16Tell("New arrangement. The door clicks open on its own: a single cup of tea, still steaming, on an empty shelf.", 6)
					Case 4 : IS16Tell("You move a magnet. The whole vault smells of the sea for a moment - salt, weed, gulls. Gone.", 6)
					Default
						IS16Give("indevration", r\Objects[U42_VLT_FRIDGE])
						IS16Tell("The drawings back as they were. It's just a fridge again - 1.6 degrees, and a ration nobody put there.", 6)
				End Select
			EndIf
			If IS10Press(r\Objects[U42_VLT_SERVERS], 2.4) Then
				IS16Tell("The backup servers hum in the cold. One screen on a rack shows a login prompt, and under it, typed by nobody: HELLO.", 6)
			EndIf
		;---------------- the Cellar
		Case "room2b44cellar"
			If IS10Press(r\Objects[U42_CEL_DETONATOR], 1.6) Then
				IS16Tell("TUNNEL DEMOLITION - E-BLOCK. The firing switch is under a steel cover with two key slots. A label: O5 AUTHORISATION ONLY. NO TESTS.", 7)
			EndIf
			If I42GlassCD > 0 Then I42GlassCD = I42GlassCD - FPSfactor
			If EntityDistance(Collider, r\Objects[U42_CEL_GLASS]) < 1.8 And I42GlassCD <= 0 Then
				I42Glass = I42Glass + FPSfactor
				If I42Glass > 70 * 2 Then
					I42Glass = 0 : I42GlassCD = 70 * 20
					CameraShake = 3.0
					IndevStress = Min(100, IndevStress + 15)
					IS16Tell("The thing in the cell turns. Dark ropes of vessel tear out of its arms and slam the glass where your face is. The glass holds. A smear of blood slides down it.", 8)
				EndIf
			Else
				I42Glass = 0
			EndIf
	End Select
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev42()
	If I42Plane > 0 Then
		I42Plane = I42Plane - FPSfactor
		If I42Plane <= 0 Then
			CameraShake = 5.0
			IndevStress = Min(100, IndevStress + 10)
			IS16Tell("A roar overhead, four big piston engines, so low the ceiling shakes - an old transport aircraft coming in to land where the flare went up. It passes. There is no sky down here.", 9)
		EndIf
	EndIf
	If I42Ear And KillTimer >= 0 Then
		I42EarT = I42EarT - FPSfactor
		If I42EarT <= 0 Then
			I42EarT = 70 * Rnd(40, 90)
			BlurTimer = Max(BlurTimer, 70 * 2)
			Injuries = Injuries + 0.05
			IS16Tell("A sharp pinch at the back of your throat. Something is making itself at home.", 5)
		EndIf
	EndIf
End Function

;SCP-500 (IndevPills.bb)
Function Indev42Cure()
	If I42Ear Then IS16Tell("You cough up something small, grey and wriggling. It scuttles off under a door.", 6)
	I42Ear = False
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse42(it.Items)
	Select it\itemtemplate\name
		Case "flare1577"
			If I42Flares <= 0 Then
				IS16Tell("The flare gun clicks on an empty chamber. There are no flares left.", 4)
			Else
				I42Flares = I42Flares - 1
				LightFlash = 3.0 : BlurTimer = 70 * 3
				If I42Plane <= 0 Then I42Plane = 70 * 60
				IS16Tell("SCP-1577-1 fires with a crack. The flare burns white-hot, far brighter and longer than it should, and hangs under the ceiling. Somewhere very far off, engines.", 8)
			EndIf
		Case "bracelets154"
			LightFlash = 1.2
			IndevRelieveStress(5)
			IS16Tell("Both bracelets on one arm, the archer's pose - and a huge, faint bow of light is in your hand, the bracelets glowing. You draw and loose. The arrow lights the whole corridor as it goes.", 8)
	End Select
	SelectedItem = Null
End Function
