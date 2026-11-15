;=====================================================================
; SCP: Containment Breach - Indev: the fortieth batch - the Residential Sector (twelve house rooms, five SCPs)
;
;   room2b42house1  the living floor: the television still on, the table set for six, the hallway of doors, and
;                   SCP-1220's tape in the kitchen - safe to play; repeat a word from it and a small zone of
;                   anomalous space opens round you (wheat, an ox, a flood, silence)
;   room2b42house2  SCP-1197, the sealed bedroom: shut the entrance door and open SCP-1197-1 - your double is in
;                   the doorway, the entrance locks, and it comes for you until the session ends.
;                   The bathroom's tube flickers. SCP-1192 in the playroom writes to you like a lost child.
;   room2b42house3  SCP-1355: some of the basement boxes move when you are not looking, and sing; stay and you
;                   wake up in the corridor without a voice. SCP-1196: the garage chairs shuffle after you,
;                   barking about your posture, louder the longer you stay.
;   Summaries of scp-wiki.wikidot.com/scp-1197, -1220, -1192, -1355, -1196 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I40Tape%, I40TapeCD#, I40Mute%, I40BirdN%, I40DoorN%
Global I40Session#, I40Dup.NPCs, I40SessDoor.Doors
Global I40Base#, I40Gar#, I40GarT#
Dim I40Box%(4), I40Chair%(3)

Function Indev40Reset(newGame%)
	If newGame Then
		I40Tape = 0 : I40Mute = False : I40BirdN = 0 : I40DoorN = 0
	EndIf
	I40TapeCD = 0 : I40Session = 0 : I40Base = 0 : I40Gar = 0 : I40GarT = 0
End Function

;the living boxes of SCP-1355 and the chairs of SCP-1196 (runtime, so they can move)
Function IndevU40Dress(r.Rooms)
	Local k%, tex%, p%, m%
	If r\RoomTemplate\Name <> "room2b42house3" Then Return
	p = r\Objects[U40_HS3_BOXES]
	tex = LoadTexture_Strict("GFX\map\indev_b40labels.png", 1)
	For k = 0 To 4
		I40Box(k) = CreateCube()
		ScaleEntity(I40Box(k), 35 * RoomScale, 30 * RoomScale, 30 * RoomScale)
		If tex <> 0 Then EntityTexture(I40Box(k), tex)
		PositionEntity(I40Box(k), EntityX(p, True) + Rnd(-1.0, 1.0), EntityY(p, True) + 30 * RoomScale, EntityZ(p, True) + Rnd(-0.6, 0.8), True)
		EntityParent(I40Box(k), r\obj, True)
	Next
	If tex <> 0 Then FreeTexture(tex)
	p = r\Objects[U40_HS3_CHAIRS]
	For k = 0 To 3
		If FileType("GFX\map\Props\scpcb_chair.x") = 1 Then
			m = LoadMesh_Strict("GFX\map\Props\scpcb_chair.x")
			If m <> 0 Then
				FitMesh(m, -0.22, 0, -0.22, 0.44, 0.85, 0.44, True)
				PositionEntity(m, EntityX(p, True) + k * 0.5 - 0.75, EntityY(p, True), EntityZ(p, True) + Rnd(-0.3, 0.3), True)
				RotateEntity(m, 0, Rnd(360), 0, True)
				EntityParent(m, r\obj, True)
				I40Chair(k) = m
			EndIf
		EndIf
	Next
End Function

Function UpdateIndevU40(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b42house1" : U40House1(e)
		Case "room2b42house2" : U40House2(e)
		Case "room2b42house3" : U40House3(e)
	End Select
End Function

;room units of the player
Function U40LX#(r.Rooms)
	Return U37LX(r)
End Function
Function U40LZ#(r.Rooms)
	Return U37LZ(r)
End Function

;--------------------------------------------------------------------------------------------- the living floor
Function U40House1(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If I40TapeCD > 0 Then I40TapeCD = I40TapeCD - FPSfactor
	If IS10Press(r\Objects[U40_HS1_TV], 1.8) Then
		IS16Tell("PLEASE STAND BY. Under the test card, very faint, a picture: this living room, seen from behind the sofa. Someone is standing where you are standing.", 8)
		IndevStress = Min(100, IndevStress + 4)
	EndIf
	If IS10Press(r\Objects[U40_HS1_TABLE6], 1.8) Then
		IS16Tell("Six places, six plates, six folded napkins. One plate is still warm. There is a name card at it, and it is yours.", 7)
	EndIf
	If IS10Press(r\Objects[U40_HS1_TAPE], 1.4) Then
		I40Tape = I40Tape + 1
		If I40Tape = 1 Then
			IS16Tell("SCP-1220, tape 1. An old woman's voice, sounds you didn't know a throat could make - chirps, clicks, a song under the words. The tape is harmless. Don't repeat any of it.", 9)
		ElseIf I40TapeCD > 0 Then
			IS16Tell("The tape hisses. Your mouth is still shaped around the last word.", 4)
		Else
			I40TapeCD = 70 * 20
			Select Rand(4)
				Case 1
					Injuries = Max(0, Injuries - 0.3)
					IS16Tell("You say it back, just one word. Wheat springs up through the lino round your feet, ripe and gold. You feel better, somehow.", 7)
				Case 2
					IndevStress = Min(100, IndevStress + 12) : CameraShake = 2.0
					IS16Tell("You say it back. Something enormous breathes right behind you - the warm, rough breath of an ox. You turn. Nothing. The kitchen smells of a barn.", 7)
				Case 3
					Stamina = 0 : BlurTimer = 70 * 3
					IS16Tell("You say it back. For two seconds the kitchen is under a metre of cold water, and then it is not. You're soaked, gasping, exhausted.", 7)
				Default : IS16Tell("You say it back. Everything goes silent - the tape, the hum, your own heartbeat - for a long, long moment.", 7)
			End Select
		EndIf
	EndIf
	If IS10Press(r\Objects[U40_HS1_DOORS], 2.4) Then
		I40DoorN = I40DoorN + 1
		Select (I40DoorN Mod 5)
			Case 1 : IS16Tell("You open one of the doors. A coat cupboard, full of coats. The same coat, fourteen times.", 6)
			Case 2 : IS16Tell("The next door opens onto a brick wall. Someone has written on it in pencil: NOT THIS ONE.", 6)
			Case 3 : IS16Tell("This door opens onto this hallway, seen from the other end. A figure at the far end is opening a door. You shut it quickly.", 7)
			Case 4 : IS16Tell("A linen cupboard. Towels, sheets, and a Foundation clipboard: 'DOOR 4 - INVENTORY COMPLETE. DOOR 5 - DO NOT'.", 7)
			Default : IS16Tell("It's painted on. All of them are painted on. You're sure that one opened a moment ago.", 6)
		End Select
	EndIf
End Function

;--------------------------------------------------------------------------------------------- the bedrooms
Function U40House2(e.Events)
	Local r.Rooms = e\room, d.Doors, best#, dd#, lx#, lz#
	;SCP-1197: a session in progress
	If I40Session > 0 Then
		I40Session = I40Session - FPSfactor
		If I40Dup <> Null And PlayerRoom = r Then
			If EntityDistance(I40Dup\Collider, Collider) < 1.0 And KillTimer >= 0 Then
				Injuries = Injuries + 0.004 * FPSfactor
				If Rand(120) = 1 Then IS16Tell("It fights exactly like you do. It knows every move before you make it.", 4)
			EndIf
		EndIf
		If I40Session <= 0 Then
			If I40Dup <> Null Then
				RemoveNPC(I40Dup)
				I40Dup = Null
			EndIf
			If I40SessDoor <> Null Then I40SessDoor\locked = False
			IS16Tell("SCP-1197-1 swings shut on its own. The entrance door clicks. You are alone in the suite - you think. You hope it was the other one who stayed.", 8)
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	lx = U40LX(r) : lz = U40LZ(r)
	If IS10Press(r\Objects[U40_HS2_D1197], 1.8) And I40Session <= 0 Then
		best = 99999
		For d = Each Doors
			If d\room = r Then
				dd = EntityDistance(d\obj, r\Objects[U40_HS2_D1197])
				If dd < best Then best = dd : I40SessDoor = d
			EndIf
		Next
		If I40SessDoor <> Null And I40SessDoor\open Then
			IS16Tell("SCP-1197-1 won't move. The handle is cold. (It only opens while the entrance door is shut.)", 6)
		Else
			I40Session = 70 * 25
			If I40SessDoor <> Null Then I40SessDoor\locked = True
			I40Dup = CreateNPC(NPCtypeD, EntityX(r\Objects[U40_HS2_DUP], True), EntityY(r\Objects[U40_HS2_DUP], True) + 0.3, EntityZ(r\Objects[U40_HS2_DUP], True))
			I40Dup\State = 0
			RotateEntity(I40Dup\Collider, 0, 90, 0)
			IndevStress = Min(100, IndevStress + 20)
			IS16Tell("The door opens onto the same suite - the same bed, the same television - and you, opening the same door, looking just as frightened. Behind you, the entrance door locks.", 9)
		EndIf
	EndIf
	If IS10Press(r\Objects[U40_HS2_PHONE], 1.4) Then
		IS16Tell("You lift the receiver. Breathing. Then your own voice, very calm: 'Don't open the door.' Click.", 6)
	EndIf
	;the bathroom tube
	If lx < -256 And lz > 20 And Rand(40) = 1 Then LightBlink = Rnd(0.4, 1.4)
	If IS10Press(r\Objects[U40_HS2_BIRD], 1.6) Then
		I40BirdN = I40BirdN + 1
		If WearingVest > 0 Then
			IS16Tell("SCP-1192 sees your vest and hops straight to the bars, bobbing, delighted - a policeman! It writes: 'u help me'.", 7)
		Else
			Select I40BirdN
				Case 1 : IS16Tell("A scruffy grey cockatoo with a red crest, feathers every which way. It picks up a pencil in its beak and writes: 'who ar u'.", 7)
				Case 2 : IS16Tell("It writes: 'timmi'. Then, more slowly: 'wher am I'.", 6)
				Case 3 : IS16Tell("It writes 'i wana go hom' and pushes the paper through the bars to you.", 6)
				Default : IS16Tell("It's drawn a house. A family. A boy. It taps the boy with its beak, over and over.", 6)
			End Select
		EndIf
	EndIf
	If IS10Press(r\Objects[U40_HS2_SHEETS], 2.4) Then
		IS16Tell("You lift a dust sheet. Under it, a chair - your height, your build, still warm, as if someone just stood up from it.", 7)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- below stairs
Function U40House3(e.Events)
	Local r.Rooms = e\room, k%, lx#, lz#, dx#, dz#, d#
	If PlayerRoom <> r Then
		I40Base = 0 : I40Gar = Max(0, I40Gar - FPSfactor)
		Return
	EndIf
	lx = U40LX(r) : lz = U40LZ(r)
	;---------------- SCP-1355: the basement
	If lx < -256 And lz < -20 And KillTimer >= 0 Then
		If I40Base = 0 Then IS16Tell("Somewhere among the boxes, many voices, singing - beautifully - a song you know. You feel calm. Count the boxes.", 7)
		I40Base = I40Base + FPSfactor
		If Rand(400) = 1 Then IndevRelieveStress(2)
		For k = 0 To 4
			If I40Box(k) <> 0 Then
				If (Not EntityInView(I40Box(k), Camera)) And Rand(160) = 1 Then
					dx = EntityX(Collider, True) - EntityX(I40Box(k), True) : dz = EntityZ(Collider, True) - EntityZ(I40Box(k), True)
					d = Sqr(dx * dx + dz * dz)
					If d > 1.0 Then TranslateEntity(I40Box(k), dx / d * 0.3, 0, dz / d * 0.3, True)
				EndIf
			EndIf
		Next
		If I40Base > 70 * 45 Then
			I40Base = 0 : I40Mute = True
			LightBlink = 3.0 : BlurTimer = 70 * 6
			IxPlace(Collider, r, 0, U37LY(r), -430)
			ResetEntity(Collider)
			IS16Tell("You wake up on the corridor floor outside. You don't remember lying down. You try to say 'hello' - you hear it, clear as anything. (Your throat makes no sound at all.)", 9)
		EndIf
	Else
		I40Base = 0
	EndIf
	;---------------- SCP-1196: the garage
	If lx < -256 And lz > 20 And KillTimer >= 0 Then
		I40Gar = I40Gar + FPSfactor
		For k = 0 To 3
			If I40Chair(k) <> 0 Then
				If (Not EntityInView(I40Chair(k), Camera)) And Rand(110) = 1 Then
					dx = EntityX(Collider, True) - EntityX(I40Chair(k), True) : dz = EntityZ(Collider, True) - EntityZ(I40Chair(k), True)
					d = Sqr(dx * dx + dz * dz)
					If d > 0.9 Then
						TranslateEntity(I40Chair(k), dx / d * 0.25, 0, dz / d * 0.25, True)
						RotateEntity(I40Chair(k), 0, VectorYaw(dx, 0, dz), 0, True)
						IS10Sound("SFX\Indev\clicks.wav", I40Chair(k), 4.0, 0.5)
					EndIf
				EndIf
			EndIf
		Next
		I40GarT = I40GarT - FPSfactor
		If I40GarT <= 0 Then
			I40GarT = 70 * Rnd(4, 8)
			If I40Gar < 70 * 40 Then
				Select Rand(4)
					Case 1 : IAxSay("A chair", "(squeaky) Stand up straight!", 3)
					Case 2 : IAxSay("A chair", "(squeaky) Don't slouch!", 3)
					Case 3 : IAxSay("A chair", "(squeaky) Fix your posture!", 3)
					Default : IAxSay("A chair", "(squeaky) Slouching causes scoliosis!", 3)
				End Select
			Else
				IAxSay("The chairs", "(deep, loud, together) STAND. UP. STRAIGHT.", 4)
				CameraShake = Max(CameraShake, 0.8)
				If Crouch Then Stamina = Min(Stamina, 20)
			EndIf
		EndIf
	EndIf
	If IS10Press(r\Objects[U40_HS3_MODEL], 1.8) Then
		IS16Tell("A perfect model of this house, every room, every lamp. In the tiny living room the tiny television is on. In the tiny garage, a tiny figure is standing very straight.", 8)
	EndIf
	If IS10Press(r\Objects[U40_HS3_SAFE], 2.0) Then
		IS16Tell("SAFEHOUSE FEEDS: every room of the house, room by room. The camera in the sealed bedroom shows two of the same person, both looking up at the camera.", 8)
	EndIf
End Function
