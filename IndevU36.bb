;=====================================================================
; SCP: Containment Breach - Indev: the thirty-sixth batch - the confectionery wing and SCP-1479's taiga
;
;   room2b36confect  five candy SCPs:
;     SCP-1200  a pack of "Tastes Like" gum (five sticks): Lemons, Sunshine (you glow), Body (you rearrange - and
;               heal), Running, or just Chewing Gum
;     SCP-1916  a jar of six jawbreakers, eaten in order: Mars, Venus, the Moon, Jupiter, the black one, the "?"
;               - your weight changes and you move as if the gravity had (IndevSpeedMul)
;     SCP-3147  a Tongue Twister lollipop: it takes two - with someone near, your words come out of them
;     SCP-1921  the kiosk in its sealed cell; the sample hatch gives a cone of black floss - eat it and it goes
;               quietly to work on your memory (SCP-500 clears it)
;     SCP-3409  the chocolate fungus behind the glass
;   room2b36taiga    SCP-1479: the utility room that holds a night taiga - dark fog, cold, eyes in the trees that
;               are gone when you get close, a cabin with a lantern where something scratches at the door; a radio
;               shows the walls your eyes cannot
;   Summaries of scp-wiki.wikidot.com/scp-1200, -1916, -1921, -3147, -3409, -1479 in our own words.
;=====================================================================

Global I36GumLeft%, I36Glow#, I36Run#
Global I1916Next%, I1916K%, I1916T#
Global I36Cotton#, I36Hatch#, I36Pop#
Global I36InTaiga%, I36Taiga#, I36Scratch%, I36Radio%
Dim I36Eye%(5)

Function Indev36Reset(newGame%)
	If newGame Then
		I36GumLeft = 5 : I1916Next = 1 : I36Cotton = 0 : I36Scratch = 0
	EndIf
	I36Glow = 0 : I36Run = 0 : I1916T = 0 : I1916K = 0 : I36Hatch = 0 : I36Pop = 0
	I36InTaiga = False : I36Taiga = 0 : I36Radio = False
	;I36Eye() is not cleared: the room makes the eyes when it is built, and a quick load keeps the room
End Function

;the movement multiplier of SCP-1916 (and SCP-1200's Running): IndevSpeedMul, IndevU31.bb
Function U36SpeedMul#()
	Local m# = 1.0
	If I1916T > 0 Then
		Select I1916K
			Case 1 : m = 1.25          ;Mars
			Case 2 : m = 1.05          ;Venus
			Case 3 : m = 1.45          ;the Moon
			Case 4 : m = 0.55          ;Jupiter
			Case 5 : m = 0.3           ;the black one
		End Select
	EndIf
	If I36Run > 0 Then m = m * 1.2
	m = m * U44SpeedMul() ;the gravity chamber's light floor (IndevU44.bb)
	Return m
End Function

Function IndevU36Dress(r.Rooms)
	Local m%, k%, tex%, p%
	Select r\RoomTemplate\Name
		Case "room2b36confect"
			m = U30Prop(r, r\Objects[U36_CON_KIOSK], "GFX\map\props\scp1921.b3d", 1.0, False)
			If m <> 0 Then TurnEntity(m, 0, 90, 0)
			U30Prop(r, r\Objects[U36_CON_TRUCK], "GFX\map\props\truck36.b3d", 1.0, True)
		Case "room2b36taiga"
			m = U30Prop(r, r\Objects[U36_TGA_CABIN], "GFX\map\props\cabin1479.b3d", 1.0, False)
			If m <> 0 Then TurnEntity(m, 0, -90, 0)
			tex = LoadTexture_Strict("GFX\map\indev_b36eyes.png", 2)
			For k = 0 To 5
				p = r\Objects[U36_TGA_EYE0 + k]
				I36Eye(k) = IS10Quad(60, 30, True, False)
				If tex <> 0 Then EntityTexture(I36Eye(k), tex)
				EntityFX(I36Eye(k), 1 + 8)
				PositionEntity(I36Eye(k), EntityX(p, True), EntityY(p, True), EntityZ(p, True), True)
				RotateEntity(I36Eye(k), 0, EntityYaw(r\obj, True), 0, True)
				EntityParent(I36Eye(k), r\obj, True)
			Next
			If tex <> 0 Then FreeTexture(tex)
	End Select
End Function

Function UpdateIndevU36(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b36confect" : U36Confect(e)
		Case "room2b36taiga" : U36Taiga(e)
	End Select
End Function

Function U36Confect(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U36_CON_HATCH], 1.6) Then
		If I36Hatch > 0 Then
			IS16Tell("The sample hatch is cycling. The kiosk behind the glass spins on its own; the floss comes out black.", 5)
		Else
			I36Hatch = 70 * 90
			IS10Sound("SFX\Indev\clicks.wav", r\Objects[U36_CON_HATCH], 4.0, 0.8)
			IS16Give("cotton1921", r\Objects[U36_CON_HATCH])
			IS16Tell("SAMPLE HATCH - SCP-1921-A2. A clunk, and a cone of black cotton candy slides into the tray. FOR D-CLASS TESTING ONLY.", 7)
		EndIf
	EndIf
	If IS10Press(r\Objects[U36_CON_FUNGUS], 2.2) Then
		IndevStress = Min(100, IndevStress + 6)
		IS16Tell("SCP-3409-A: brown tendrils over the floor and up the walls of the cell, a smell of cocoa through the seals. In the corner the air is wrong - a dark red glow. The tendrils are longer than an hour ago.", 9)
	EndIf
	If IS10Press(r\Objects[U36_CON_KIOSK], 3.0) Then
		IS16Tell("SCP-1921, in its cage: COTTON CANDY - FREE WITH ADMISSION. The paint is scorched. The spinner turns by itself.", 6)
	EndIf
	If IS10Press(r\Objects[U36_CON_FEEDS], 2.4) Then
		IS16Tell("Twelve feeds. CAM 04 and CAM 09: someone standing quite still at the end of a corridor. CAM 07 is dead. You check again: CAM 04 is empty.", 8)
		IndevStress = Min(100, IndevStress + 5)
	EndIf
	If IS10Press(r\Objects[U36_CON_TRUCK], 3.0) Then
		IS16Tell("A Foundation transport, cab locked. Under the canvas: crates stamped CONFECTIONERY ANOMALIES - DO NOT EAT. One crate has been opened, and is empty.", 8)
	EndIf
	If IS10Press(r\Objects[U36_CON_BAYDOOR], 3.0) Then
		IS16Tell("VEHICLE BAY 3. The big door is locked down for the breach. Behind it, the ramp up to the surface roads.", 6)
	EndIf
End Function

Function U36Taiga(e.Events)
	Local r.Rooms = e\room, k%, d#, lx#
	If PlayerRoom <> r Then
		I36InTaiga = False
		Return
	EndIf
	TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
	lx = TFormedX()
	I36InTaiga = (lx > 260)
	;the eyes: there in the dark - gone when you come near
	For k = 0 To 5
		If I36Eye(k) <> 0 Then
			d = EntityDistance(Collider, I36Eye(k))
			If d < 1.4 Then
				If Not EntityHidden(I36Eye(k)) Then
					HideEntity(I36Eye(k))
					If Not IAxFlag(e, "e") Then
						IAxSetFlag(e, "e")
						IS16Tell("A pair of eyes between the trunks, low, watching. You take a step and they are simply not there.", 6)
					EndIf
				EndIf
			ElseIf d > 3.5 And EntityHidden(I36Eye(k)) And Rand(600) = 1 Then
				ShowEntity(I36Eye(k))
			EndIf
		EndIf
	Next
	If I36InTaiga Then
		I36Taiga = I36Taiga + FPSfactor
		e\EventState3 = e\EventState3 - FPSfactor
		If e\EventState3 <= 0 Then
			e\EventState3 = 70 * Rnd(14, 26)
			IS10Sound("SFX\Indev\wind.wav", Collider, 8.0, 0.5)
		EndIf
		If I36Taiga > 70 * 60 Then
			Injuries = Injuries + 0.00012 * FPSfactor
			If I36Taiga - FPSfactor <= 70 * 60 Then IS16Tell("The cold has got into your hands. Your breath smokes. The door is somewhere behind you - is it?", 6)
		EndIf
		If (Not I36Radio) And U31HasDevice() Then
			I36Radio = True
			IS16Tell("Your radio's little display has drawn a box round you: walls, four metres away in every direction. You can't see them. The trees go on.", 8)
		EndIf
	Else
		I36Taiga = Max(0, I36Taiga - FPSfactor * 2)
	EndIf
	If IS10Press(r\Objects[U36_TGA_CABINDOOR], 2.0) Then
		I36Scratch = I36Scratch + 1
		IS10Sound("SFX\Indev\creak.wav", r\Objects[U36_TGA_CABINDOOR], 6.0, 0.7)
		If I36Scratch = 1 Then
			IS16Tell("You knock. The lantern swings. From inside, slowly, something scratches at the door - at about the height of your knees.", 7)
		ElseIf I36Scratch = 2 Then
			IndevStress = Min(100, IndevStress + 15)
			IS16Tell("It opens a crack on its own. Warm air, woodsmoke - and on the stairs to the attic, a pair of eyes, and then another. The door shuts.", 8)
		Else
			IS16Tell("The door won't open again. Above you, in the attic window, two lights. Watching.", 6)
		EndIf
	EndIf
	If IS10Press(r\Objects[U36_TGA_CAMERA], 1.8) Then
		IS16Tell("The investigators' camera, pointed at the utility room door: on its screen, a small empty room, four metres square. Through the door with your own eyes: forest.", 8)
	EndIf
End Function

;called from IndevOutdoorFrame (IndevU26.bb) after the game sets its fog: the taiga's night, SCP-1200's glow
Function U36Frame()
	If I36InTaiga And I36Glow <= 0 Then
		CameraFogMode(Camera, 1)
		CameraFogRange(Camera, 0.8, 14.0)
		CameraFogColor(Camera, 30, 34, 38)
		CameraClsColor(Camera, 30, 34, 38)
		AmbientLight(70, 74, 82)
	EndIf
	If I36Glow > 0 Then
		AmbientLight(210, 210, 190)
		If I36InTaiga Then CameraFogRange(Camera, 1.0, 18.0)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev36()
	Local n.NPCs
	If I36Hatch > 0 Then I36Hatch = I36Hatch - FPSfactor
	If I36Glow > 0 Then
		I36Glow = I36Glow - FPSfactor
		If I36Glow <= 0 Then IS16Tell("Your glow fades to nothing. It doesn't hurt. It never did.", 5)
	EndIf
	If I36Run > 0 Then
		I36Run = I36Run - FPSfactor
		Stamina = Min(100, Stamina + 0.3 * FPSfactor)
	EndIf
	If I1916T > 0 And KillTimer >= 0 Then
		I1916T = I1916T - FPSfactor
		If I1916K = 4 Then Stamina = Min(Stamina, 40)
		If I1916K = 5 Then
			Stamina = Min(Stamina, 10) : CameraShake = Max(CameraShake, 0.6)
			Injuries = Injuries + 0.0008 * FPSfactor
		EndIf
		If I1916T <= 0 Then IS16Tell("Your weight comes back to normal all at once. The floor feels like the floor again.", 5)
	EndIf
	If I36Pop > 0 Then I36Pop = I36Pop - FPSfactor
	;SCP-1921-A2 at work
	If I36Cotton > 0 And KillTimer >= 0 Then
		I36Cotton = I36Cotton + FPSfactor
		If I36Cotton > 70 * 45 Then
			If (I36Cotton - FPSfactor) <= 70 * 45 Then IS16Tell("Behind your eyes, very quietly, a carnival organ is playing. Free with admission. You can't remember what you ate.", 7)
			If Rand(1400) = 1 Then
				IndevMemory = Min(100, IndevMemory + 6)
				IAxSay("???", "(a whisper, in a showman's voice) Step right up. Step right up. It's free.", 5)
			EndIf
		EndIf
	EndIf
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse36(it.Items)
	Local n.NPCs, near.NPCs, k%
	Select it\itemtemplate\name
		Case "gum1200"
			If I36GumLeft <= 0 Then
				IS16Tell("The pack is empty. A tiny print on the inside: 'collect all 83!'", 4)
			Else
				I36GumLeft = I36GumLeft - 1
				Select Rand(5)
					Case 1 : IS16Tell("'Tastes Like Lemons.' It does - and so does your own spit, and the air. Everything will taste of lemons for a day.", 7)
					Case 2
						I36Glow = 70 * 40 : LightFlash = 1.0
						IS16Tell("'Tastes Like Sunshine.' You start to shine - a hard white light from your skin that throws shadows down the corridor.", 7)
					Case 3
						Injuries = Max(0, Injuries - 0.4) : BlurTimer = 70 * 3
						IS16Tell("'Tastes Like Putty.' You can move your fingers to the other hand. You don't. You smooth your cuts closed instead.", 7)
					Case 4
						I36Run = 70 * 60
						IS16Tell("'Tastes Like Running.' Your legs want to go. Your lungs agree.", 6)
					Default : IS16Tell("'Tastes Like Chewing Gum.' It tastes like chewing gum. That's somehow the worst one.", 6)
				End Select
				If I36GumLeft = 0 Then
					RemoveItem(it)
					SelectedItem = Null
					Return
				EndIf
			EndIf
		Case "jar1916"
			If I1916Next > 6 Then
				IS16Tell("The jar is empty. A faint smell of sugar and something metallic.", 4)
			Else
				k = I1916Next
				I1916Next = I1916Next + 1
				If k = 6 Then k = Rand(1, 5)
				I1916K = k : I1916T = 70 * 60
				Select k
					Case 1 : IS16Tell("The red one. A minute later you feel light - a third of yourself. Mars. You bound down the corridor.", 7)
					Case 2 : IS16Tell("The beige one with white streaks. Venus: a little lighter. Barely worth it.", 6)
					Case 3 : IS16Tell("The moon-grey one. Your feet hardly touch the floor. One sixth of you.", 6)
					Case 4 : IS16Tell("The banded one with the red spot. Two and a half times your weight lands on your knees. Jupiter.", 7)
					Default : IS16Tell("The black one. You weigh as much as a car. Each step is a fight. Your heart is labouring.", 7)
				End Select
				If I1916Next = 7 Then IS16Tell("(The last one had a question mark on it.)", 4)
			EndIf
		Case "pop3147"
			For n = Each NPCs
				If n\Collider <> 0 Then
					If EntityDistance(n\Collider, Collider) < 4.0 Then near = n : Exit
				EndIf
			Next
			If near <> Null Then
				I36Pop = 70 * 60
				IS16Tell("You hold it out. A lick each. Then you speak - and the words come out of the other mouth, in your voice.", 7)
				IAxSay("Not you", "Tantalizing Tongue Twisters! From Doctor Wondertainment!", 5)
			Else
				IS16Tell("Strawberry, artificially. 'Gather two or three of your bestest friends!' There's nobody here to share it with.", 6)
			EndIf
		Case "cotton1921"
			If I36Cotton > 0 Then
				IS16Tell("You don't want any more. You're not sure why.", 4)
			Else
				I36Cotton = 1
				RemoveItem(it)
				IS16Tell("Black floss, sweet and burnt. It shrinks on your tongue until you can't feel it at all. That's all. That's all it does.", 7)
				SelectedItem = Null
				Return
			EndIf
	End Select
	SelectedItem = Null
End Function
