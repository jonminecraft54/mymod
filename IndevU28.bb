;=====================================================================
; SCP: Containment Breach - Indev: SCP-983, the birthday monkey (twenty-eighth batch)
;
;   Each new game rolls whether today is D-9341's birthday (one in three). The board by the door says so.
;   Not your birthday: clicking the monkey is safe - an old wind-up toy.
;   Your birthday: clicking it wakes it. A backflip, then every 3.5 s a verse - "A RING DING DING DING IT'S YOUR
;   BIRTHDAY!" and a bell - and every verse ages you a year (I983Age): stamina is capped lower, from 30 years the
;   view blurs, at 60 years you die of old age (and a black candy drops from the bell).
;   Sing along: click while "IT'S YOUR BIRTHDAY!" comes (0.9 to 1.9 s into the verse; 1.2 to 1.6 is perfect).
;   Six verses in a row in time stop it: "BIRTHDAY!", a backflip, and a gumdrop drops from the bell -
;     all six perfect: luminescent;  four or more perfect: clear;  otherwise red, green, yellow or purple.
;   Candies (items candy983_*): luminescent and clear give the years back (luminescent also heals you fully, and a
;   minute later the light comes out of you - a blinding flash); red heals a little, green restores stamina, yellow
;   calms you, purple clears your head a little. The black one can't be eaten: you can only stare into it.
;   Summary of scp-wiki.wikidot.com/scp-983 (CC BY-SA 3.0).
;=====================================================================

Global I983Birthday%   ;today is D-9341's birthday (rolled for a new game, kept in the save)
Global I983Age#        ;years SCP-983 has taken
Global I983Glow#       ;frames until the luminescent candy's flash (0 = none)
Global I983Mesh%, I983Spin#, Indev28Verses%

Function Indev983Reset(newGame%)
	If newGame Then I983Birthday = (Rand(3) = 1)
	I983Age = 0 : I983Glow = 0
End Function

Function IndevU28Dress(r.Rooms)
	If r\RoomTemplate\Name = "room2b28monkey" Then I983Mesh = IndevScpMesh(r, r\Objects[U28_MKY_MONKEY], "m983") ;the monkey (IndevScpProps.bb)
	If I983Mesh <> 0 Then TurnEntity(I983Mesh, 0, 180, 0) ;the model faces -z: turn it towards the door
End Function

;the state of the song lives in the room's event: EventState 0 asleep, 1 singing, 2 finished.
;EventState2: frames into the current verse.  EventState3: 10 for every verse in a row sung in time, +1 if it was
;perfect - so after six in a row it is 60 plus the number of perfect ones.
;flags: c clicked this verse, d done (it sang its last for this playthrough)
Function UpdateIndevU28(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U28_MKY_MONKEY], t#, good%, perf%, kind$
	If I983Spin > 0 Then
		I983Spin = I983Spin - FPSfactor
		If I983Mesh <> 0 Then TurnEntity(I983Mesh, 360.0 / 35.0 * FPSfactor, 0, 0)
		If I983Spin <= 0 And I983Mesh <> 0 Then RotateEntity(I983Mesh, 0, EntityYaw(I983Mesh), 0)
	EndIf
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U28_MKY_BOARD], 1.5) Then
		If I983Birthday Then
			Msg = "BIRTHDAYS TODAY: Dr. A. Lowe (Archives), J. Marsh (Security), D-9341. ...D-9341. That's you." : MsgTimer = 70 * 7
		Else
			Msg = "BIRTHDAYS TODAY: Dr. A. Lowe (Archives), J. Marsh (Security). Not you. Not today." : MsgTimer = 70 * 6
		EndIf
	EndIf
	If IS10Press(r\Objects[U28_MKY_KIT], 1.5) Then
		Msg = "Emergency Kit 135r: a kazoo, a party hat, and Document 135r. Sing on the last line. Six in a row." : MsgTimer = 70 * 6
	EndIf
	If IS10Press(r\Objects[U28_MKY_CASE], 1.5) Then
		Msg = "Collected candies, each tagged: clear, clear, red, green, yellow, purple - and one black, in its own sealed box." : MsgTimer = 70 * 6
	EndIf

	Select e\EventState
		Case 0
			If IS10Press(p, 1.2) Then ;arm's length: you have to pick it up
				If IAxFlag(e, "d") Then
					Msg = "The monkey sits still, bell raised, grinning. It has done its singing for today." : MsgTimer = 70 * 5
				ElseIf Not I983Birthday Then
					Msg = "An old wind-up monkey. On the sole of its left foot, a faded date: 194-. It stays perfectly still." : MsgTimer = 70 * 6
				Else
					e\EventState = 1 : e\EventState2 = 0 : e\EventState3 = 0
					IS13Drop(e, "c")
					I983Spin = 35
					IS10Sound("SFX\Indev\jingle.wav", p, 8.0, 1.0)
					Msg = "The monkey jerks to life in your hands, flips over backwards and lands grinning. It raises its bell." : MsgTimer = 70 * 5
				EndIf
			EndIf
		Case 1
			If KillTimer < 0 Then
				e\EventState = 2
				IAxSetFlag(e, "d")
				Return
			EndIf
			t = e\EventState2
			e\EventState2 = e\EventState2 + FPSfactor
			;the verse starts: the song, the bell, a year
			If t = 0 Then
				Indev28Verses = Indev28Verses + 1
				I983Age = I983Age + 1
				IS10Sound("SFX\Indev\bells.wav", p, 10.0, 1.0)
				Msg = Chr(34) + "A RING DING DING DING - IT'S YOUR BIRTHDAY!" + Chr(34) + "   (sing on the last line - click)   You feel " + Int(I983Age) + " years older." : MsgTimer = 70 * 3
				If I983Mesh <> 0 Then TranslateEntity(I983Mesh, 0, 0.03, 0) ;a little hop with the bell
			EndIf
			If I983Mesh <> 0 And t < 6 And e\EventState2 >= 6 Then TranslateEntity(I983Mesh, 0, -0.03, 0)
			;singing along: a click (not in the inventory), within 3 m of the monkey - from further off it can't hear
			;you, and it keeps singing at you
			If MouseHit1 And EntityDistance(Camera, p) < 3.0 And (Not InvOpen) And SelectedItem = Null And (Not IAxFlag(e, "c")) Then
				MouseHit1 = False
				IAxSetFlag(e, "c")
				good = (e\EventState2 >= 70 * 0.9 And e\EventState2 <= 70 * 1.9)
				perf = (e\EventState2 >= 70 * 1.2 And e\EventState2 <= 70 * 1.6)
				If good Then
					e\EventState3 = e\EventState3 + 10 + perf
				Else
					e\EventState3 = 0
					Msg = "You come in at the wrong moment. The monkey sings right over you." : MsgTimer = 70 * 2
				EndIf
			EndIf
			;the verse ends
			If e\EventState2 >= 70 * 3.5 Then
				If Not IAxFlag(e, "c") Then e\EventState3 = 0 ;silence breaks the run too
				IS13Drop(e, "c")
				e\EventState2 = 0
				If e\EventState3 >= 60 Then
					;six in a row: BIRTHDAY!
					If Int(e\EventState3) - 60 >= 6 Then
						kind = "candy983_lum"
					ElseIf Int(e\EventState3) - 60 >= 4 Then
						kind = "candy983_clear"
					Else
						Select Rand(4)
							Case 1 : kind = "candy983_red"
							Case 2 : kind = "candy983_green"
							Case 3 : kind = "candy983_yellow"
							Default : kind = "candy983_purple"
						End Select
					EndIf
					I983Finish(e, kind, "BIRTHDAY!" + Chr(34) + " The monkey flips over backwards, rings its bell once - and a gumdrop drops out of it.")
					Return
				EndIf
			EndIf
			;the years
			Stamina = Min(Stamina, Max(10, 100 - I983Age * 1.5))
			If I983Age >= 30 Then BlurTimer = Max(BlurTimer, 70 * 0.5 * (I983Age - 29) / 10)
			If I983Age >= 60 Then
				DeathMSG = "Subject D-9341 was found in SCP-983's chamber, reduced to a skeleton with the skin clinging to it. SCP-983 was sitting beside the remains with a black candy in its bell. It was the subject's birthday."
				Kill()
				I983Finish(e, "candy983_black", "BIRTHDAY!" + Chr(34) + " The last thing you hear.")
			EndIf
	End Select
End Function

Function I983Finish(e.Events, kind$, txt$)
	Local p% = e\room\Objects[U28_MKY_MONKEY]
	e\EventState = 2
	IAxSetFlag(e, "d")
	I983Spin = 35
	IS10Sound("SFX\Indev\ding.wav", p, 10.0, 1.0)
	IS16Give(kind, p)
	Msg = Chr(34) + txt : MsgTimer = 70 * 7
End Function

;eating a candy (Main.bb, the item-use code)
Function IndevUse983Candy(it.Items)
	Local n$ = it\itemtemplate\name
	If n = "candy983_black" Then
		IndevStress = Min(100, IndevStress + 20)
		BlurTimer = Max(BlurTimer, 70 * 6)
		Msg = "You raise the black gumdrop to your mouth - and stop. You've been staring into it. You don't know for how long." : MsgTimer = 70 * 7
		SelectedItem = Null
		Return
	EndIf
	Select n
		Case "candy983_lum"
			I983Age = 0 : Injuries = 0 : Bloodloss = 0 : Stamina = 100
			I983Glow = 70 * 60
			Msg = "It tastes of birthday cake and starlight. The years fall away. Your skin is faintly glowing." : MsgTimer = 70 * 7
		Case "candy983_clear"
			I983Age = 0
			Msg = "Clear as glass, sweet as sugar. The aches of the lost years melt away. You are yourself again." : MsgTimer = 70 * 6
		Case "candy983_red"
			Injuries = Max(0, Injuries - 0.5)
			Msg = "Cherry, a little too sweet. Your wounds sting less." : MsgTimer = 70 * 5
		Case "candy983_green"
			Stamina = 100
			Msg = "Lime. You feel like you could run for a mile." : MsgTimer = 70 * 5
		Case "candy983_yellow"
			IndevStress = Max(0, IndevStress - 30)
			Msg = "Lemon, and for a moment it's your birthday party, years ago. You feel calm." : MsgTimer = 70 * 5
		Default
			IndevMemory = Max(0, IndevMemory - 10)
			Msg = "Grape. Things you'd forgotten come back: a name, a face, a song." : MsgTimer = 70 * 5
	End Select
	RemoveItem(it)
	SelectedItem = Null
End Function

;every frame (IndevHazards.bb): the luminescent candy's light, a minute later
Function UpdateIndev983()
	If I983Glow <= 0 Then Return
	I983Glow = I983Glow - FPSfactor
	If I983Glow <= 0 Then
		I983Glow = 0
		LightFlash = 4.0
		BlurTimer = Max(BlurTimer, 70 * 8)
		CameraShake = 2.0
		Msg = "The light comes out of you all at once - blinding, silent. When you can see again, every lamp nearby is brighter." : MsgTimer = 70 * 7
	EndIf
End Function
