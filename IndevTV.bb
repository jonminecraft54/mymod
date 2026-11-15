;=====================================================================
; SCP: Containment Breach - Indev SCP-993 "Bobble the Clown"
;
; A CRT television in an office. It shows static - until the player
; walks up and looks at it. Then Bobble's theme plays, the player (who
; is well over ten) gets a stabbing headache and blacks out for the
; whole episode, and wakes up on the floor with the TV back on static.
; SCP-173 plays fair while the player is out, same as the SCP-990 dream.
;=====================================================================

Global I993TV%, I993Screen%, I993Room.Rooms
Global I993TexOff%, I993TexS1%, I993TexS2%, I993TexB1%, I993TexB2%, I993TexB3%
Global I993State%, I993Timer#, I993Anim#, I993Cooldown#, I993Seen%
Global I993Theme%, I993Static%, I993Pick%, I993Off%, I993BlackMs%

Function Indev993Reset()
	;entities belonged to the old map and were freed with it
	I993TV = 0 : I993Screen = 0 : I993Room = Null
	If I993State = 2 Then UnableToMove = False
	I993State = 0 : I993Timer = 0 : I993Anim = 0 : I993Cooldown = 0 : I993Seen = 0
	I993Theme = 0 : I993Static = 0 : I993Pick = 0 : I993Off = False
End Function

;called from FillRoom: puts the TV at (x, y, z), facing yaw, settled onto whatever is below it.
;Returns False if this map already has one (there's only one SCP-993 set).
Function IndevCreate993%(r.Rooms, x#, y#, z#, yaw#)
	If I993TV <> 0 Then Return False
	I993Room = r
	I993TV = LoadMesh_Strict("GFX\map\Props\tv993.b3d", r\obj)
	Local tex% = LoadTexture_Strict("GFX\map\Props\tv993.png", 1)
	EntityTexture(I993TV, tex)
	ScaleEntity(I993TV, 0.001, 0.001, 0.001, True) ;global: the parent room is already scaled by RoomScale
	RotateEntity(I993TV, 0, yaw, 0, True)

	;sit it on the desk top. (No LinePick: during map generation the desk props aren't pickable yet, so the
	;ray used to drop the TV through the desk. room2offices2's desk top is at y -69, checked against the room mesh.)
	Local halfH# = 540.0 * 0.001 * 0.5
	If r\RoomTemplate\Name = "room2offices2" Then y = r\y - 69.0 * RoomScale + halfH
	PositionEntity(I993TV, x, y, z, True)
	EntityType(I993TV, HIT_MAP)
	EntityPickMode(I993TV, 2)

	;(the screen sprite is made on the first frame, unparented and in world units - a sprite parented to the
	;scaled TV ignored that scale and came out hundreds of units wide, covering the whole view)
	I993Screen = 0

	I993TexOff = LoadTexture_Strict("GFX\map\Props\tv993_off.png", 1)
	I993TexS1 = LoadTexture_Strict("GFX\map\Props\tv993_static1.png", 1)
	I993TexS2 = LoadTexture_Strict("GFX\map\Props\tv993_static2.png", 1)
	I993TexB1 = LoadTexture_Strict("GFX\map\Props\tv993_bobble1.png", 1)
	I993TexB2 = LoadTexture_Strict("GFX\map\Props\tv993_bobble2.png", 1)
	I993TexB3 = LoadTexture_Strict("GFX\map\Props\tv993_bobble3.png", 1)
	Return True
End Function

Function UpdateIndev993()
	If I993TV = 0 Then Return
	If I993Screen = 0 Then
		;the picture tube: model point (-70, 17, -243), 222 x 198 model units -> world (TV scale 0.001)
		TFormPoint(-70, 17, -243 - 2, I993TV, 0)
		I993Screen = CreateSprite()
		PositionEntity(I993Screen, TFormedX(), TFormedY(), TFormedZ(), True)
		RotateEntity(I993Screen, EntityPitch(I993TV, True), EntityYaw(I993TV, True), EntityRoll(I993TV, True), True)
		SpriteViewMode(I993Screen, 2)
		ScaleSprite(I993Screen, 0.222, 0.198)
		EntityFX(I993Screen, 1 + 16)
		EntityTexture(I993Screen, I993TexS1)
		If I993Room <> Null Then EntityParent(I993Screen, I993Room\obj, True) ;hidden together with the room
		;click target around the set
		TFormPoint(0, 0, 0, I993TV, 0)
		I993Pick = CreatePivot()
		PositionEntity(I993Pick, TFormedX(), TFormedY(), TFormedZ(), True)
		EntityRadius(I993Pick, 0.3)
		EntityPickMode(I993Pick, 1, False)
	EndIf

	Local dist# = EntityDistance(I993Screen, Camera)

	;the power knob (only between episodes)
	If I993State = 0 And KillTimer >= 0 Then
		If IndevAimedAt(I993TV, I993Pick, 1.8) Then
			DrawHandIcon = True
			If MouseHit1 Then
				MouseHit1 = False
				I993Off = (Not I993Off)
				PlaySound_Strict(ButtonSFX)
				If I993Off Then
					EntityTexture(I993Screen, I993TexOff)
					Msg = "You switch the TV off. The screen collapses to a bright dot and fades. Somehow the room feels safer."
				Else
					EntityTexture(I993Screen, I993TexS1)
					Msg = "You switch the TV back on. Static hisses up out of nothing."
				EndIf
				MsgTimer = 70*4
			EndIf
		EndIf
	EndIf
	If I993Off And I993State = 0 Then Return
	I993Anim = I993Anim + FPSfactor
	If I993Cooldown > 0 Then I993Cooldown = I993Cooldown - FPSfactor

	Select I993State
		Case 0 ;static, until someone watches
			If dist < 10.0 And I993Anim > 3 Then
				I993Anim = 0
				If Rand(2) = 1 Then
					EntityTexture(I993Screen, I993TexS1)
				Else
					EntityTexture(I993Screen, I993TexS2)
				EndIf
			EndIf
			If I993Cooldown <= 0 And dist < 3.5 And Indev990State = 0 And KillTimer >= 0 Then
				;(the click target sphere sits inside the set and would block the sight line, so it's
				;switched off while checking)
				Local seen% = False
				If EntityInView(I993Screen, Camera) Then
					If I993Pick <> 0 Then EntityPickMode(I993Pick, 0)
					seen = EntityVisible(Camera, I993TV)
					If I993Pick <> 0 Then EntityPickMode(I993Pick, 1, False)
				EndIf
				If seen Then
					I993State = 1
					I993Timer = 70*2.8
					If I993Theme = 0 Then I993Theme = LoadSound_Strict("SFX\SCP\993\Theme.ogg")
					PlaySound2(I993Theme, Camera, I993TV, 10.0, 1.0)
					LightBlink = 0.3
				EndIf
			EndIf

		Case 1 ;the program begins - the player gets to see about three seconds of it
			If I993Anim > 9 Then
				I993Anim = 0
				Select Rand(1,3)
					Case 1 EntityTexture(I993Screen, I993TexB1)
					Case 2 EntityTexture(I993Screen, I993TexB2)
					Default EntityTexture(I993Screen, I993TexB3)
				End Select
			EndIf
			I993Timer = I993Timer - FPSfactor
			If I993Timer <= 0 And IndevCogOn Then
				;Cognitive Filter Glasses: the broadcast never gets a proper grip
				I993State = 0
				I993Cooldown = 70*60*4
				EntityTexture(I993Screen, I993TexS1)
				Msg = "Bobble's face smears into grey noise behind the filter lenses. A stabbing headache - but you stay on your feet."
				MsgTimer = 70*6
				BlurTimer = 70*2
				Injuries = Injuries + 0.02
			ElseIf I993Timer <= 0 Then
				I993State = 2
				I993Timer = 70*15
				I993BlackMs = MilliSecs()
				Msg = "A stabbing pain behind your eyes -"
				MsgTimer = 70*2
				CameraShake = 3
			EndIf

		Case 2 ;unconscious for the episode (the black screen itself is drawn in DrawIndev993)
			BlinkTimer = -10
			UnableToMove = True
			CurrSpeed = 0
			If Curr173 <> Null Then
				If Curr173\Idle < 2 Then Curr173\IdleTimer = Max(Curr173\IdleTimer, 70*3)
			EndIf
			I993Timer = I993Timer - FPSfactor
			;(real-time failsafe too, so the blackout can never get stuck)
			If I993Timer <= 0 Or MilliSecs() - I993BlackMs > 15000 Or MilliSecs() < I993BlackMs Then
				I993State = 0
				I993Cooldown = 70*60*4
				UnableToMove = False
				EntityTexture(I993Screen, I993TexS1)
				If I993Static = 0 Then I993Static = LoadSound_Strict("SFX\SCP\993\Static.ogg")
				PlaySound2(I993Static, Camera, I993TV, 8.0, 0.8)
				BlurTimer = 70*8
				CameraShake = 1.5
				Injuries = Injuries + 0.05
				I993Seen = I993Seen + 1
				If I993Seen = 1 Then
					Msg = "You come to on the floor with a splitting headache. The TV is showing static. You have no idea what the episode was about - and a strong feeling you're better off that way."
				Else
					Msg = "You wake up on the floor again, head pounding. Bobble learned something new today. You didn't."
				EndIf
				MsgTimer = 70*8
			EndIf
	End Select
End Function

;black screen while knocked out by the episode, fading in and out at the edges
Function DrawIndev993()
	If I993State <> 2 Then Return
	;last-resort failsafe in case the update stopped running (menus, loading): wake up anyway
	If MilliSecs() - I993BlackMs > 17000 Or MilliSecs() < I993BlackMs Then
		I993State = 0 : I993Cooldown = 70*60*4 : UnableToMove = False
		If I993Screen <> 0 Then EntityTexture(I993Screen, I993TexS1)
		Return
	EndIf
	;solid black over the world and the HUD for the whole episode
	Color 0, 0, 0
	Rect 0, 0, GraphicWidth, GraphicHeight, True
	;a faint countdown of the episode's end credits, so it's clear the game hasn't frozen
	Local left% = Max(0, 15 - (MilliSecs() - I993BlackMs) / 1000)
	SetFont Font1
	Color 40, 40, 40
	Text GraphicWidth / 2, GraphicHeight / 2, "...", True, True
	If left <= 3 Then
		Color 70, 70, 70
		Text GraphicWidth / 2, GraphicHeight / 2 + 30 * MenuScale, "(somewhere far away, a theme tune is ending)", True, True
	EndIf
	Color 255, 255, 255
End Function
