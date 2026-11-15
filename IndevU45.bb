;=====================================================================
; SCP: Containment Breach - Indev: the forty-fifth batch - the old SCP-939 chamber, the Morgue, the Off-Shoot Hall,
; the damaged wing. Each room rolls a variation once per game (e\EventState2), so it is not the same twice.
;
;   room2b47old939    1: the pack is still down there - voices of the dead calling up from the pit, red teeth
;                     catching the light; 2: silence, and the red hatch stands open; 3: one voice that knows your
;                     designation. Fall into the pit and you do not come out.
;   room2b47morgue    the drawers, table 2; on the first visit there is a chance SCP-106 comes up through the floor
;   room3b47offshoot  very dark (closer fog); one of two sets of floor holes is real - fall in and you die; the jammed
;                     door is hot enough to burn; a chance SCP-106 is waiting in the dark
;   room2b47damaged   aftershocks; under the hole, falling debris
;   Summary of scp-wiki.wikidot.com/scp-939 in our own words (CC BY-SA 3.0).
;=====================================================================

Global I45Glint% = 0, I45GlintT#, I45Dark%, I45Fall#

Function Indev45Reset(newGame%)
	I45GlintT = 0 : I45Dark = False : I45Fall = 0
End Function

Function IndevU45Dress(r.Rooms)
End Function

;SCP-106 comes up through the floor at pivot p (the pattern IndevAnnex.bb uses)
Function U45Summon106(p%)
	If Curr106 = Null Or Contained106 Then Return
	If Curr106\State <= 0 Then Return
	PositionEntity(Curr106\Collider, EntityX(p, True), EntityY(p, True), EntityZ(p, True))
	ResetEntity(Curr106\Collider)
	Curr106\State = -0.1
	ShowEntity(Curr106\obj)
End Function

;called from IndevOutdoorFrame (IndevU26.bb): the off-shoot hall's darkness
Function U45Frame()
	If I45Dark Then
		CameraFogMode(Camera, 1)
		CameraFogRange(Camera, 0.3, 3.0)
		CameraFogColor(Camera, 4, 4, 5)
		CameraClsColor(Camera, 4, 4, 5)
	EndIf
End Function

Function UpdateIndevU45(e.Events)
	Local r.Rooms = e\room, lx#, ly#, lz#, k%, d#, tex%
	If e\EventState2 = 0 Then e\EventState2 = Rand(1, 3)
	If PlayerRoom <> r Then
		If r\RoomTemplate\Name = "room3b47offshoot" Then I45Dark = False
		If I45Glint <> 0 And r\RoomTemplate\Name = "room2b47old939" Then HideEntity(I45Glint)
		Return
	EndIf
	lx = U37LX(r) : ly = U37LY(r) : lz = U37LZ(r)
	Select r\RoomTemplate\Name
		;---------------- the old SCP-939 chamber
		Case "room2b47old939"
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 Then
				e\EventState3 = 70 * Rnd(25, 50)
				Select e\EventState2
					Case 1
						Select Rand(4)
							Case 1 : IAxSay("From the pit", "(a woman's voice) Hello? Is someone up there? I'm hurt, I can't climb...", 6)
							Case 2 : IAxSay("From the pit", "(a guard's voice) Come down, it's safe, they've moved them. Come on down.", 6)
							Case 3 : IAxSay("From the pit", "(a child's voice) Help. Help. Help. Help.", 5)
							Default : IAxSay("From the pit", "(your own voice, a beat late) ...is someone up there?", 6)
						End Select
					Case 2 : IS16Tell("Silence from the pit. The red hatch in the far wall stands open. There are long scratches round it, at a height of about two metres.", 6)
					Default : IAxSay("From the pit", "D-9341. D-9341. We know you. Come and see.", 6)
				End Select
			EndIf
			;red teeth catching the light, down in the dark
			If e\EventState2 <> 2 And lx < 260 Then
				If I45GlintT > 0 Then
					I45GlintT = I45GlintT - FPSfactor
					If I45GlintT <= 0 And I45Glint <> 0 Then HideEntity(I45Glint)
				ElseIf Rand(200) = 1 Then
					If I45Glint = 0 Then
						I45Glint = IS10Quad(50, 20, True, False)
						tex = LoadTexture_Strict("GFX\map\indev_b36eyes.png", 2)
						If tex <> 0 Then
							EntityTexture(I45Glint, tex)
							FreeTexture(tex)
						EndIf
						EntityColor(I45Glint, 255, 60, 50)
						EntityFX(I45Glint, 1 + 8)
					EndIf
					IxPlace(I45Glint, r, Rnd(500, 900), -330, Rnd(-500, 500))
					RotateEntity(I45Glint, 0, EntityYaw(r\obj, True) + 90, 0, True)
					ShowEntity(I45Glint)
					I45GlintT = 40
				EndIf
			EndIf
			;fallen into the pit
			If ly < -200 And KillTimer >= 0 Then
				I45Fall = I45Fall + FPSfactor
				If I45Fall > 70 * 1.5 Then
					DeathMSG = "Subject D-9341 was seen climbing over the parapet into the old SCP-939 chamber, apparently in response to a voice. No remains were recovered."
					Kill()
				EndIf
			EndIf
			If IS10Press(r\Objects[U45_O39_REELS], 1.6) Then
				IS16Tell("The reel-to-reel is still threaded: AUDIO, PIT, NIGHT 14. Voices, dozens of them, all calling the same name - and the name changes, one by one, to the voice that says it.", 8)
			EndIf
		;---------------- the morgue
		Case "room2b47morgue"
			If lx > 256 And e\EventState = 0 Then
				e\EventState = 1
				If Rand(100) <= 35 Then e\EventState3 = 70 * 5 Else e\EventState3 = -1
				IS16Tell("The morgue is cold and smells of disinfectant over something worse. The operating lamp is still on over table 2.", 6)
			EndIf
			If e\EventState3 > 0 Then
				e\EventState3 = e\EventState3 - FPSfactor
				If e\EventState3 <= 0 Then
					e\EventState3 = -1
					U45Summon106(r\Objects[U45_MRG_SPAWN106])
				EndIf
			EndIf
			If IS10Press(r\Objects[U45_MRG_DRAWERS], 2.4) Then
				Select Rand(4)
					Case 1 : IS16Tell("You pull a drawer. Empty - but the tray is warm.", 4)
					Case 2 : IS16Tell("A drawer you haven't touched slides open by itself, slowly, all the way. Empty.", 5)
					Case 3
						IndevStress = Min(100, IndevStress + 8)
						IS16Tell("The name card on this drawer reads D-9341. Your number. It's empty. For now.", 6)
					Default : IS16Tell("A drawer of personal effects: a wedding ring, a watch still running, a keycard sleeve with no card.", 5)
				End Select
			EndIf
			If IS10Press(r\Objects[U45_MRG_TABLE2], 1.6) Then
				IndevStress = Min(100, IndevStress + 10)
				If e\EventState2 = 1 Then
					IS16Tell("Table 2. The straps are still buckled. The Y-incision was begun and not finished. The fingers of the left hand are curled - as if gripping the edge of the table.", 8)
				Else
					IS16Tell("Table 2. As you lean over it, the head turns, very slightly, toward you. It doesn't move again. You are almost sure it doesn't move again.", 8)
				EndIf
			EndIf
		;---------------- the off-shoot hall
		Case "room3b47offshoot"
			I45Dark = True
			If e\EventState = 0 Then
				e\EventState = 1
				If Rand(100) <= 45 Then e\EventState3 = 70 * 6 Else e\EventState3 = -1
			EndIf
			If e\EventState3 > 0 Then
				e\EventState3 = e\EventState3 - FPSfactor
				If e\EventState3 <= 0 Then
					e\EventState3 = -1
					U45Summon106(r\Objects[U45_OFS_SPAWN106])
				EndIf
			EndIf
			;the holes: set A (EventState2 1) or set B (2, 3) is real
			For k = 0 To 3
				d = EntityDistance(Collider, r\Objects[U45_OFS_HOLEA1 + k])
				If d < 0.28 And KillTimer >= 0 Then
					If (k < 2 And e\EventState2 = 1) Or (k >= 2 And e\EventState2 <> 1) Then
						DeathMSG = "The body of Subject D-9341 was recovered from a sinkhole beneath the Off-Shoot Halls. The floor there had been reported unsafe for over a year."
						Kill()
					ElseIf Rand(120) = 1 Then
						IS16Tell("The dark patch holds your weight. Just a stain. This one.", 4)
					EndIf
				ElseIf d < 0.6 And Rand(240) = 1 Then
					IS16Tell("The floor creaks underfoot. There's a darker patch just ahead.", 3)
				EndIf
			Next
			d = EntityDistance(Collider, r\Objects[U45_OFS_FIREDOOR])
			If d < 1.3 And Rand(400) = 1 Then IS16Tell("Heat on your face from the jammed door. Small flames lick out of the seam. Nothing behind it should be burning.", 5)
			If IS10Press(r\Objects[U45_OFS_FIREDOOR], 1.2) Then
				Injuries = Injuries + 0.15
				IS16Tell("You grab the handle - and let go with a yelp. It's scalding. The door doesn't move a millimetre.", 5)
			EndIf
		;---------------- the damaged wing
		Case "room2b47damaged"
			e\EventState3 = e\EventState3 - FPSfactor
			If e\EventState3 <= 0 Then
				e\EventState3 = 70 * Rnd(30, 50)
				CameraShake = 2.5
				If lx > 470 And lx < 830 And Abs(lz) < 230 And Rand(2) = 1 Then
					Injuries = Injuries + 0.25
					IS16Tell("An aftershock - and a chunk of concrete drops out of the hole above you and catches your shoulder.", 6)
				Else
					IS16Tell("An aftershock. Dust pours out of the hole in the ceiling. Somewhere above, something heavy shifts.", 5)
				EndIf
			EndIf
	End Select
End Function
