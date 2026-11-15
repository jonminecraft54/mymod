;=====================================================================
; SCP: Containment Breach - Indev SCP-738 "The Devil's Deal"
;
; A mahogany desk (738-1), a straight-backed chair (738-2) and a gilded
; throne (738-3) standing in a dead-end room. Click the chair to sit down:
; the throne drags itself around to the far side of the desk, someone is
; sitting in it, and a voice makes offers.
;
;   [1-5] make a request      [B] bargain for another price
;   [Y] accept                [N] refuse
;
; Deals are fulfilled to the letter - not past it - and the price is
; always paid. Three deals per run, then the throne stays empty.
;=====================================================================

Global I738Room.Rooms, I738Desk%, I738Chair%, I738Throne%
Global I738Tex%, I738Voice%[3], I738Drag%
Global I738State%, I738Timer#, I738Phi#, I738PhiTarget#, I738Cooldown#
Global I738Deals%, I738Req%, I738Price%, I738Desc$, I738DescTime#
Global I738Line$[6], I738Lines%, I738LineTime#
Global I738Checked%

;room-local layout (RoomScale units, +Z = toward the big gate): the set stands deep in the room,
;well clear of the entrance passage. The throne orbits the desk (phi 0 = behind the chair, 180 = across the desk)
Const I738_ORBIT# = 185.0
;desk/chair positions depend on the room (checked against the room meshes): the endroom floor runs deep
;toward the gate; the smaller endroom2 only has floor from z -400 to +300
Global I738DeskZ# = 720.0, I738ChairZ# = 615.0
Const I738_CM# = 1.25 ;model centimetres -> RoomScale units (1.9 made the throne almost as tall as the doorway)

Function Indev738Reset()
	If I738State > 0 Then UnableToMove = False
	I738Room = Null : I738Desk = 0 : I738Chair = 0 : I738Throne = 0 : I738Tex = 0
	I738Voice[0] = 0 : I738Voice[1] = 0 : I738Voice[2] = 0 : I738Drag = 0
	I738State = 0 : I738Timer = 0 : I738Phi = 0 : I738PhiTarget = 0 : I738Cooldown = 0
	I738Deals = 0 : I738Req = 0 : I738Price = 0 : I738Desc = "" : I738DescTime = -99999
	I738Lines = 0
	I738Checked = False
End Function

;called from FillRoom. Only one set per map - returns False if it already exists
Function IndevCreate738%(r.Rooms)
	If I738Desk <> 0 Then Return False
	I738Room = r
	If r\RoomTemplate\Name = "endroom2" Then
		I738DeskZ = -40.0 : I738ChairZ = -145.0
	Else
		I738DeskZ = 720.0 : I738ChairZ = 615.0
	EndIf
	I738Tex = LoadTexture_Strict("GFX\map\Props\scp738.png", 1)

	I738Desk = LoadMesh_Strict("GFX\map\Props\scp738_1.b3d", r\obj)
	I738Chair = LoadMesh_Strict("GFX\map\Props\scp738_2.b3d", r\obj)
	I738Throne = LoadMesh_Strict("GFX\map\Props\scp738_3.b3d", r\obj)

	Local e%, i%
	For i = 0 To 2
		Select i
			Case 0 e = I738Desk
			Case 1 e = I738Chair
			Default e = I738Throne
		End Select
		EntityTexture(e, I738Tex)
		ScaleEntity(e, I738_CM, I738_CM, I738_CM) ;local scale: the room itself is already scaled to RoomScale
		EntityType(e, HIT_MAP)
		EntityPickMode(e, 2)
	Next

	PositionEntity(I738Desk, 0, 0, I738DeskZ, False)
	RotateEntity(I738Desk, 0, 0, 0, False)          ;drawers face the chair
	PositionEntity(I738Chair, 0, 0, I738ChairZ, False)
	RotateEntity(I738Chair, 0, 180, 0, False)       ;seat faces the desk
	I738Phi = 0 : I738PhiTarget = 0
	I738PlaceThrone()
	Return True
End Function

;True if the player is within maxDist (ignoring height) of ent and turned toward it within maxAngle degrees.
;More forgiving than EntityInView for low furniture props in dark rooms.
Function IndevFacing%(ent%, maxDist#, maxAngle#)
	If ent = 0 Then Return False
	Local dx# = EntityX(ent, True) - EntityX(Collider, True)
	Local dz# = EntityZ(ent, True) - EntityZ(Collider, True)
	If dx * dx + dz * dz > maxDist * maxDist Then Return False
	If Abs(EntityY(ent, True) - EntityY(Collider, True)) > 1.5 Then Return False
	Return (Abs(DeltaYaw(Camera, ent)) < maxAngle)
End Function

;the throne always faces the desk as it moves around it
Function I738PlaceThrone()
	PositionEntity(I738Throne, I738_ORBIT * Sin(I738Phi), 0, I738DeskZ - I738_ORBIT * Cos(I738Phi), False)
	RotateEntity(I738Throne, 0, 180 + I738Phi, 0, False)
End Function

Function I738Say(t$, voice% = True)
	If I738Lines >= 6 Then
		Local i%
		For i = 0 To 4 : I738Line[i] = I738Line[i + 1] : Next
		I738Lines = 5
	EndIf
	I738Line[I738Lines] = t
	I738Lines = I738Lines + 1
	I738LineTime = 0
	If voice Then
		Local v% = Rand(0, 2)
		If I738Voice[v] = 0 Then I738Voice[v] = LoadSound_Strict("SFX\SCP\738\Voice" + (v + 1) + ".ogg")
		PlaySound2(I738Voice[v], Camera, I738Throne, 8.0, 0.9)
	EndIf
End Function

Function I738ClearLines()
	I738Lines = 0
End Function

Function I738Describe$()
	;the same visitor again soon sees the same thing; otherwise it's someone new
	If PlayTime - I738DescTime < 70*60*5 And I738Desc <> "" Then Return I738Desc
	Select Rand(1,6)
		Case 1 I738Desc = "a woman in a dress the colour of old wine, smiling as if she's known you for years"
		Case 2 I738Desc = "a young man with a kind, familiar face - it takes you a moment to realise it's almost yours"
		Case 3 I738Desc = "an elderly gentleman in a perfectly pressed suit, fingers steepled"
		Case 4 I738Desc = "someone you used to love. You never told anyone about them"
		Case 5 I738Desc = "a figure far too elegant to be real, legs crossed, head tilted, patient"
		Default I738Desc = "a child swinging its feet, who speaks with an old man's voice"
	End Select
	I738DescTime = PlayTime
	Return I738Desc
End Function

Function I738RequestText$(i%)
	Select i
		Case 1 Return "Get me out of here."
		Case 2 Return "Heal me."
		Case 3 Return "Tell me the door code."
		Case 4 Return "Make the statue leave me alone."
		Default Return "Nothing. I'm leaving."
	End Select
End Function

Function I738PriceText$(req%, alt%)
	Select req
		Case 1
			If alt = 0 Then Return "A day's worth of pain, all in one breath."
			Return "The warmth in your legs. You will tire so very easily."
		Case 2
			If alt = 0 Then Return "When you close your eyes, they will stay closed a little longer. Always."
			Return "Something you are carrying. The thing you would miss the most."
		Case 3
			If alt = 0 Then Return "Your blood. Not all of it. Enough that you'll notice."
			Return "Something you are carrying. The thing you would miss the most."
		Case 4
			Return "Such a small thing. Your dreams - you won't be needing them."
	End Select
	Return ""
End Function

;True if some event lives in this room (e.g. endroom106, where SCP-106 takes the janitor across the room)
Function I738RoomHasEvent%(r.Rooms)
	Local e.Events
	For e = Each Events
		If e\room = r Then Return True
	Next
	Return False
End Function

;placed on the first gameplay frame, once events exist: a standard dead end with no event in it
;(never the SCP-106 janitor room), otherwise an HCZ dead end that isn't the SCP-990 area
Function IndevEnsure738()
	I738Checked = True
	If I738Desk <> 0 Then Return
	Local r.Rooms, pick.Rooms = Null, it.Items
	For r = Each Rooms
		If r\RoomTemplate\Name = "endroom" And (Not I738RoomHasEvent(r)) Then pick = r : Exit
	Next
	If pick = Null Then
		For r = Each Rooms
			If r\RoomTemplate\Name = "endroom2" And r <> Indev990Room And (Not I738RoomHasEvent(r)) Then pick = r : Exit
		Next
	EndIf
	If pick = Null Then
		DebugLog "Indev: no free dead end for SCP-738 on this map"
		Return
	EndIf
	If IndevCreate738(pick) Then
		;the document by the wall, out of the walkway
		it = CreateItem("doc738", pick\x, pick\y + 0.5, pick\z)
		EntityParent(it\collider, pick\obj)
		PositionEntity(it\collider, -250.0, 120.0, I738ChairZ, False)
		ResetEntity(it\collider)
		DebugLog "Indev: SCP-738 placed in " + pick\RoomTemplate\Name
	EndIf
End Function

Function UpdateIndev738()
	If (Not I738Checked) Then IndevEnsure738()
	If I738Desk = 0 Then Return
	If I738Cooldown > 0 Then I738Cooldown = I738Cooldown - FPSfactor
	I738LineTime = I738LineTime + FPSfactor

	;the throne glides toward where it wants to be
	If Abs(I738Phi - I738PhiTarget) > 0.1 Then
		If I738Phi < I738PhiTarget Then
			I738Phi = Min(I738PhiTarget, I738Phi + FPSfactor * 0.55)
		Else
			I738Phi = Max(I738PhiTarget, I738Phi - FPSfactor * 0.55)
		EndIf
		I738PlaceThrone()
	EndIf

	If I738State = 0 Then
		If KillTimer < 0 Or Indev990State > 0 Then Return
		;any of the three pieces works - clicking the chair, the desk or the throne sits you down
		If IndevAimedAt(I738Chair, I738Chair, 1.8) Or IndevAimedAt(I738Desk, I738Desk, 2.0) Or IndevAimedAt(I738Throne, I738Throne, 1.8) Then
			If True Then
				DrawHandIcon = True
				If MouseHit1 Then
					MouseHit1 = False
					If I738Deals >= 3 Then
						Msg = "You sit in the chair. The throne stays where it is, and it stays empty. Your business here is done."
						MsgTimer = 70*5
					ElseIf I738Cooldown > 0 Then
						Msg = "You sit down. Nothing happens. You get the feeling you are being made to wait."
						MsgTimer = 70*4
					Else
						I738SitDown()
					EndIf
				EndIf
			EndIf
		EndIf
		Return
	EndIf

	;--- in a session: the player is seated and can't move; SCP-173 plays fair
	UnableToMove = True
	CurrSpeed = 0
	If Curr173 <> Null Then
		If Curr173\Idle < 2 Then Curr173\IdleTimer = Max(Curr173\IdleTimer, 70*3)
	EndIf
	I738Timer = I738Timer + FPSfactor

	Select I738State
		Case 1 ;sitting down, the throne comes around the desk
			If I738Timer > 70*1.5 And I738Lines = 1 Then
				I738Say("The throne is on the other side of the desk now. Someone is sitting in it: " + I738Describe() + ".", False)
			EndIf
			If I738Timer > 70*5.5 And I738Lines = 2 Then
				Select Rand(1,3)
					Case 1 I738Say(Chr(34) + "Anything, D-9341. Safety. Freedom. A way out. You only have to ask." + Chr(34))
					Case 2 I738Say(Chr(34) + "You look tired. Hurt. Lost. I can fix every one of those things." + Chr(34))
					Default I738Say(Chr(34) + "Sit. Stay a while. Tell me what you want more than anything." + Chr(34))
				End Select
			EndIf
			If I738Timer > 70*8 Then
				I738State = 2 : I738Timer = 0
				FlushKeys()
			EndIf

		Case 2 ;choosing a request
			Local k%
			For k = 1 To 5
				If KeyHit(k + 1) Then I738Request(k) : Exit
			Next

		Case 3 ;a price is on the table
			If KeyHit(21) Then ;Y
				I738Accept()
			ElseIf KeyHit(49) Then ;N
				I738Say(Chr(34) + "No? Then what else do you want?" + Chr(34))
				I738State = 2 : I738Timer = 0
			ElseIf KeyHit(48) Then ;B
				If I738Req = 4 Then
					I738Say(Chr(34) + "There's nothing of equal value to haggle over. It's a small thing." + Chr(34))
				Else
					I738Price = 1 - I738Price
					I738Say(Chr(34) + "Of equal value, then: " + I738PriceText(I738Req, I738Price) + Chr(34))
				EndIf
			EndIf

		Case 4 ;the deal is done or refused - read the outcome, then get up
			If I738Timer > 70*6 Then I738StandUp()
	End Select
End Function

Function I738SitDown()
	I738State = 1 : I738Timer = 0
	I738ClearLines()

	;into the chair, facing the desk
	EntityType(I738Chair, 0)
	PositionEntity(Collider, EntityX(I738Chair, True), EntityY(Collider), EntityZ(I738Chair, True), True)
	ResetEntity(Collider)
	RotateEntity(Collider, 0, EntityYaw(I738Chair, True) + 180, 0, True)
	Crouch = True

	I738PhiTarget = 180
	If I738Drag = 0 Then I738Drag = LoadSound_Strict("SFX\SCP\738\Drag.ogg")
	PlaySound2(I738Drag, Camera, I738Throne, 8.0, 1.0)
	I738Say("The chair creaks as you sit. Behind you, something heavy drags itself across the floor.", False)
End Function

Function I738StandUp()
	I738State = 0 : I738Timer = 0
	I738ClearLines()
	UnableToMove = False
	Crouch = False
	EntityType(I738Chair, HIT_MAP)
	I738PhiTarget = 0
	I738Cooldown = 70*60*3
End Function

Function I738Request(k%)
	I738Req = k
	I738Price = 0
	Select k
		Case 5
			I738Say(Chr(34) + "Come back when you know what you want." + Chr(34))
			I738State = 4 : I738Timer = 70*3
			Return
		Case 4
			;requests that would help others are refused more often than not
			If Rand(2) = 1 Then
				I738Say(Chr(34) + "You don't want that enough. You want it for everyone who comes through here after you." + Chr(34))
				I738Say("The request is not fulfilled.", False)
				I738State = 4 : I738Timer = 0
				Return
			EndIf
	End Select
	I738Say(Chr(34) + I738RequestText(k) + Chr(34) + " - a pause. The quill starts writing on its own.", False)
	I738Say(Chr(34) + "The price is: " + I738PriceText(k, 0) + Chr(34))
	I738State = 3 : I738Timer = 0
End Function

;removes the most valuable thing in the inventory (highest keycard first, otherwise anything)
Function I738TakeBestItem$()
	Local n%, best% = -1, score%, bestScore% = -1, s$, name$
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			name = Inventory(n)\itemtemplate\name
			score = 1
			Select name
				Case "key1" score = 11
				Case "key2" score = 12
				Case "key3" score = 13
				Case "key4" score = 14
				Case "key5" score = 15
				Case "key6" score = 16
				Case "nav", "nav300", "nav310", "navulti" score = 10
				Case "gasmask", "supergasmask", "vest", "finevest" score = 8
				Case "scp500" score = 9
			End Select
			If score > bestScore Then bestScore = score : best = n
		EndIf
	Next
	If best < 0 Then Return ""
	s = Inventory(best)\itemtemplate\displayname
	If SelectedItem = Inventory(best) Then SelectedItem = Null
	RemoveItem(Inventory(best))
	Return s
End Function

Function I738Accept()
	I738Deals = I738Deals + 1
	I738State = 4 : I738Timer = 0
	I738Say("You nod. Somewhere in the desk, a drawer slides shut.", False)

	;--- the request, to the letter
	Local r.Rooms, count%, pick%, taken$
	Select I738Req
		Case 1
			I738Say(Chr(34) + "Out of here. Out of this room. To the letter." + Chr(34))
		Case 2
			Injuries = 0 : Bloodloss = 0
			ResetDiseases()
			IndevPillsCure()
			I738Say("Every wound closes. You feel whole.", False)
		Case 3
			I738Say(Chr(34) + "The code is " + AccessCode + ". I never said which door it opens." + Chr(34))
		Case 4
			I738Say(Chr(34) + "The statue will not touch you. For as long as you are sitting in that chair." + Chr(34))
	End Select

	;--- the price
	Select I738Req
		Case 1
			If I738Price = 0 Then
				Injuries = Injuries + 1.2
				CameraShake = 3 : BlurTimer = 70*6
			Else
				StaminaEffect = Max(StaminaEffect, 1.5) : StaminaEffectTimer = 99999
			EndIf
		Case 2
			If I738Price = 0 Then
				BlinkEffect = Max(BlinkEffect, 1.35) : BlinkEffectTimer = 99999
			Else
				taken = I738TakeBestItem()
			EndIf
		Case 3
			If I738Price = 0 Then
				Bloodloss = Min(Bloodloss + 45, 95)
				Local de.Decals = CreateDecal(3, EntityX(Collider), EntityY(Collider) - 0.3, EntityZ(Collider), 90, Rand(360), 0)
				de\Size = 0.4 : ScaleSprite(de\obj, de\Size, de\Size)
			Else
				taken = I738TakeBestItem()
			EndIf
		Case 4
			Indev990Seen = 2 ;no more dreams of SCP-990, ever
	End Select
	If taken <> "" Then I738Say("Your pocket feels lighter. The " + taken + " is gone.", False)

	;"out of here" is fulfilled once the player is out of the chair: any corridor, anywhere in the facility
	If I738Req = 1 Then
		count = 0
		For r = Each Rooms
			If r <> I738Room And r\zone = I738Room\zone And Left(r\RoomTemplate\Name, 5) = "room2" And Instr(r\RoomTemplate\Name, "tesla") = 0 Then count = count + 1
		Next
		If count > 0 Then
			pick = Rand(1, count) : count = 0
			For r = Each Rooms
				If r <> I738Room And r\zone = I738Room\zone And Left(r\RoomTemplate\Name, 5) = "room2" And Instr(r\RoomTemplate\Name, "tesla") = 0 Then
					count = count + 1
					If count = pick Then
						I738StandUp()
						PositionEntity(Collider, EntityX(r\obj), EntityY(r\obj) + 0.7, EntityZ(r\obj))
						ResetEntity(Collider)
						UpdateDoors()
						UpdateRooms()
						PlayerRoom = r
						Msg = "You blink, and the chair is gone. You are standing in a corridor. You are out of there - exactly as you asked."
						MsgTimer = 70*7
						Exit
					EndIf
				EndIf
			Next
		EndIf
	EndIf
End Function

Function DrawIndev738()
	If I738State = 0 Or I738Lines = 0 Then Return
	Local i%, y%, x% = GraphicWidth / 2
	Local lh% = 26 * MenuScale
	Local top% = GraphicHeight - (I738Lines + 7) * lh

	SetFont Font1
	For i = 0 To I738Lines - 1
		If Left(I738Line[i], 1) = Chr(34) Then Color 220, 170, 255 Else Color 210, 210, 210
		Text x, top + i * lh, I738Line[i], True, False
	Next

	y = top + (I738Lines + 1) * lh
	If I738State = 2 Then
		Color 255, 230, 160
		For i = 1 To 5
			Text x, y + (i - 1) * lh, "[" + i + "] " + I738RequestText(i), True, False
		Next
	ElseIf I738State = 3 Then
		Color 255, 230, 160
		Text x, y, "[Y] Accept     [N] Refuse     [B] Bargain", True, False
	EndIf
	Color 255, 255, 255
End Function
