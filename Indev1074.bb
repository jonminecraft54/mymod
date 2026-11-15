;=====================================================================
; SCP: Containment Breach - Indev SCP-1074 "Stendhal's Nightmare"
;
;   room2scp1074room (LCZ). The painting stands on an easel in the north
;   room, facing the doorway (level 3 door, always open) from the south room.
;   A painting texture (a Class-D kneeling with his head bowed, on black)
;   is laid over the easel's canvas.
;
;   Looking straight at it with your eyes open:
;     1  heart pounding, vertigo - and you start walking toward it. Look away
;        (or blink) for a couple of seconds and you break free
;     2  once you're standing in front of it you can't move and your gaze is
;        dragged back to it. D-9341 starts talking about the painting
;     3  after the monologue: keep looking and you slip into catatonia (death).
;        Keep breaking your gaze and you stay alive - but stuck, with
;        SCP-173 somewhere in the facility
;   Night vision goggles or the CF-1 Cognitive Filter Glasses stop it at any
;   point. Afterwards the painting shows up behind your eyelids for a while.
;=====================================================================

Global I1074Room.Rooms, I1074Pivot%, I1074Stage%, I1074T#, I1074Away#, I1074Line%, I1074Cata#
Global I1074After#, I1074Cool#, I1074Img%, I1074Music%, I1074Gaze#, I1074Walk#
Global I1074Fake%, I1074FakeT#, I1074FakeCool#, I1074FakeSeen#, I1074Exposed%

;the painting's music (SFX\Music\Intro.ogg): starts when it pulls you in, stops when it lets go
Function I1074StartMusic()
	If I1074Music <> 0 Then Return
	I1074Music = StreamSound_Strict("SFX\Music\Intro.ogg", SFXVolume, 0)
	If I1074Music = -1 Then I1074Music = 0
End Function

Function I1074StopMusic()
	If I1074Music = 0 Then Return
	StopStream_Strict(I1074Music)
	I1074Music = 0
End Function

Function Indev1074Reset(keepWorld% = False)
	If I1074Stage >= 1 And I1074Stage <= 3 Then UnableToMove = False
	I1074StopMusic()
	If Not keepWorld Then I1074Room = Null : I1074Pivot = 0
	I1074Stage = 0 : I1074T = 0 : I1074Away = 0 : I1074Line = 0 : I1074Cata = 0
	I1074After = 0 : I1074Cool = 0 : I1074Img = 0 : I1074Gaze = 0
	If Not keepWorld Then I1074Fake = 0
	I1074HideFake()
	I1074FakeCool = 0 : I1074Exposed = False
End Function

;called from FillRoom
Function IndevFill1074(r.Rooms)
	I1074Room = r

	;the door between the two rooms: level 3 keycard, but it's always standing open
	Local d.Doors = CreateDoor(r\zone, r\x + 672.0 * RoomScale, r\y, r\z, 0, r, True, False, 3)
	d\AutoClose = False : d\open = True

	;the painting over the easel canvas (canvas corners from the room mesh; it leans back and faces -Z)
	Local tex% = LoadTexture_Strict("GFX\map\Props\scp1074.png", 1)
	Local m% = CreateMesh(r\obj)
	Local s% = CreateSurface(m)
	Local nx# = 0.0, ny# = 0.421, nz# = -0.906, off# = 1.5
	AddVertex(s, 899.5 + nx * off, 88.1 + ny * off, 522.9 + nz * off, 1, 1)
	AddVertex(s, 769.3 + nx * off, 88.1 + ny * off, 522.9 + nz * off, 0, 1)
	AddVertex(s, 769.3 + nx * off, 227.5 + ny * off, 587.7 + nz * off, 0, 0)
	AddVertex(s, 899.5 + nx * off, 227.5 + ny * off, 587.7 + nz * off, 1, 0)
	AddTriangle(s, 0, 1, 2) : AddTriangle(s, 0, 2, 3)
	AddTriangle(s, 2, 1, 0) : AddTriangle(s, 3, 2, 0)
	UpdateNormals(m)
	EntityTexture(m, tex)
	EntityFX(m, 1)
	FreeTexture(tex)

	I1074Pivot = CreatePivot(r\obj)
	PositionEntity(I1074Pivot, 834.0, 162.0, 546.0, False) ;just in front of the canvas, so the canvas itself does not block the sight line
End Function

;looking straight at the painting with open eyes, and nothing filtering it
Function I1074Seen%()
	If BlinkTimer < 0 Then Return False
	If WearingNightVision > 0 Or IndevCogOn Then Return False
	If EntityDistance(Camera, I1074Pivot) > 8.0 Then Return False
	If Not EntityInView(I1074Pivot, Camera) Then Return False
	If Not EntityVisible(Camera, I1074Pivot) Then Return False
	TFormVector(0, 0, 1, Camera, 0)
	Local fx# = TFormedX(), fy# = TFormedY(), fz# = TFormedZ()
	Local dx# = EntityX(I1074Pivot, True) - EntityX(Camera, True)
	Local dy# = EntityY(I1074Pivot, True) - EntityY(Camera, True)
	Local dz# = EntityZ(I1074Pivot, True) - EntityZ(Camera, True)
	Local l# = Sqr(dx * dx + dy * dy + dz * dz)
	If l < 0.01 Then Return True
	Return ((fx * dx + fy * dy + fz * dz) / l > 0.93)
End Function

;turn the player toward the painting; strength = CurveAngle divisor (smaller = stronger)
Function I1074Pull(strength#)
	Local dx# = EntityX(I1074Pivot, True) - EntityX(Collider, True)
	Local dz# = EntityZ(I1074Pivot, True) - EntityZ(Collider, True)
	RotateEntity(Collider, EntityPitch(Collider), CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(Collider), strength), EntityRoll(Collider))
	Local h# = Sqr(dx * dx + dz * dz)
	Local pitch# = ATan2(EntityY(Camera, True) - EntityY(I1074Pivot, True), Max(h, 0.1))
	user_camera_pitch = CurveValue(pitch, user_camera_pitch, strength)
End Function

Function I1074Release(txt$)
	I1074Stage = 0 : I1074Away = 0 : I1074Cata = 0 : I1074Line = 0
	UnableToMove = False
	I1074After = 70*180 : I1074Cool = 70*8 : I1074Gaze = 0
	I1074Exposed = True : I1074FakeCool = 70*3 ;the first time, he shows up soon after
	I1074StopMusic()
	Msg = txt : MsgTimer = 70*6
End Function

Function UpdateIndev1074()
	UpdateIndev1074Fake()
	If I1074After > 0 Then
		I1074After = I1074After - FPSfactor
		;it's still there when you close your eyes
		If BlinkTimer < -3 And Rand(40) = 1 Then IndevStress = Min(100, IndevStress + 1)
	EndIf
	If I1074Room = Null Or I1074Pivot = 0 Then Return
	If KillTimer < 0 Then
		If I1074Stage > 0 Then I1074Stage = 0 : UnableToMove = False
		I1074StopMusic()
		Return
	EndIf
	If I1074Cool > 0 Then I1074Cool = I1074Cool - FPSfactor
	;out of the room: whatever it was doing stops (no pulling, no lock, no music)
	If PlayerRoom <> I1074Room Then
		I1074Gaze = 0
		If I1074Stage > 0 Then I1074Release("Out of its sight, the pull fades. Your hands are shaking.")
		Return
	EndIf

	Local seen% = I1074Seen()
	Local protect% = (WearingNightVision > 0 Or IndevCogOn)

	Select I1074Stage
		Case 0
			;a glance isn't enough - it takes about a second of actually looking at it
			If seen Then I1074Gaze = I1074Gaze + FPSfactor Else I1074Gaze = Max(0, I1074Gaze - FPSfactor * 2)
			If I1074Gaze > 70 And I1074Cool <= 0 Then
				I1074Gaze = 0
				I1074Stage = 1 : I1074Away = 0 : I1074T = 0 : I1074Walk = 0
				I1074StartMusic()
				If IndevCogOn Then Return
				Msg = "Your heart lurches. The painting - it's the most beautiful thing you have ever seen." : MsgTimer = 70*5
			EndIf

		Case 1 ;drawn toward it
			If protect Then I1074Release("The picture flattens into dull grey paint. Your legs are your own again.") : Return
			If seen Then
				I1074Away = 0
				;the legs walk toward it on their own, but the head is still yours: turn away to break it
				Local tyaw# = VectorYaw(EntityX(I1074Pivot, True) - EntityX(Collider, True), 0, EntityZ(I1074Pivot, True) - EntityZ(Collider, True))
				ForceMove = 0.45 : ForceAngle = WrapAngle(tyaw - EntityYaw(Collider)) ;MovePlayer walks along (Cos, Sin) of yaw+ForceAngle+90
				HeartBeatVolume = Max(HeartBeatVolume, 0.5) : HeartBeatRate = Max(HeartBeatRate, 120)
				CameraShake = Max(CameraShake, 0.25)
				IndevStress = Min(100, IndevStress + FPSfactor / 70.0 * 2.0)
			Else
				I1074Away = I1074Away + FPSfactor
				If I1074Away > 35 Then I1074Release("You tear your eyes away. Your heart is hammering, and part of you wants nothing more than to look again.") : Return
			EndIf
			;walking into a wall on the way (grabbed through a doorway at an angle): the spell doesn't hold forever
			I1074Walk = I1074Walk + FPSfactor
			If I1074Walk > 70*20 Then I1074Release("Your body can't find a way to it. Slowly, the need to look fades.") : Return
			Local hd# = Sqr((EntityX(I1074Pivot, True) - EntityX(Collider, True)) ^ 2 + (EntityZ(I1074Pivot, True) - EntityZ(Collider, True)) ^ 2)
			If hd < 2.0 Then ;(the easel legs stop you before you get much closer)
				I1074Stage = 2 : I1074T = 70*2 : I1074Line = 0 : I1074Cata = 0
				Msg = "You're standing right in front of it. You don't remember walking here." : MsgTimer = 70*3
			EndIf

		Case 2, 3 ;in front of it: can't move, the gaze keeps being dragged back
			If protect Then I1074Release("The goggles' flat green picture shows a canvas of plain grey paint. Whatever held you lets go.") : Return
			UnableToMove = True
			CurrSpeed = 0
			I1074Pull(16.0) ;strong, but you can still fight it with the mouse for a moment
			HeartBeatVolume = Max(HeartBeatVolume, 0.7) : HeartBeatRate = Max(HeartBeatRate, 135)
			If Rand(300) = 1 Then CameraShake = Max(CameraShake, 0.6)
			IndevStress = Min(100, IndevStress + FPSfactor / 70.0 * 1.5)

			If I1074Stage = 2 Then
				I1074T = I1074T - FPSfactor
				If I1074T <= 0 Then
					I1074T = 70*6
					Select I1074Line
						Case 0 Msg = Chr(34) + "It's... it's the greatest work of art I've ever seen." + Chr(34)
						Case 1 Msg = Chr(34) + "That's me. On my knees. Look at the floor - it's so dark you could fall into it." + Chr(34)
						Case 2 Msg = Chr(34) + "Why would anyone paint me? Who even knew I was here?" + Chr(34)
						Case 3 Msg = Chr(34) + "The black isn't the background. It's everything that's waiting for me." + Chr(34)
						Case 4 Msg = Chr(34) + "I know what it means. It means I don't get to walk away from what I did." + Chr(34)
						Case 5 Msg = Chr(34) + "Those people. I remember their faces. The painting remembers them too." + Chr(34)
						Case 6 Msg = Chr(34) + "This is my sentence. Not theirs. Mine." + Chr(34)
						Case 7 Msg = Chr(34) + "I'm sorry. I'm so sorry." + Chr(34)
						Case 8 Msg = "You can't move your feet. Keep looking away, keep blinking - and pray you have something that changes the way you see."
						Default
							I1074Stage = 3
					End Select
					MsgTimer = 70*6
					I1074Line = I1074Line + 1
				EndIf
			Else
				;keep staring and the mind goes quiet for good; breaking the gaze buys time
				If seen Then
					I1074Cata = I1074Cata + FPSfactor
				Else
					I1074Cata = Max(0, I1074Cata - FPSfactor * 0.5)
				EndIf
				If I1074Cata > 70*4 And I1074Cata - FPSfactor <= 70*4 Then Msg = "Your thoughts are getting very slow and very far away." : MsgTimer = 70*4
				If I1074Cata > 70*12 Then
					UnableToMove = False
					I1074Stage = 0
					I1074StopMusic()
					DeathMSG = "Subject D-9341 was found standing in front of SCP-1074, catatonic and unresponsive. EEG readings indicate the subject is fully awake and aware. No means of reversing the condition is known. Subject is scheduled for termination."
					Kill()
				EndIf
			EndIf
	End Select
End Function

;the painting behind your eyelids after an exposure
Function DrawIndev1074()
	If I1074After <= 0 Then Return
	If BlinkTimer >= -3 Then Return
	If I1074Img = 0 Then I1074Img = LoadImage_Strict("GFX\map\Props\scp1074_small.png")
	If I1074Img = 0 Then Return
	DrawImage(I1074Img, GraphicWidth / 2 - ImageWidth(I1074Img) / 2, GraphicHeight / 2 - ImageHeight(I1074Img) / 2)
End Function

;---------------------------------------------------------------------
; the watcher: after looking at the painting, D-9341 keeps seeing the man
; from it - a Class-D standing half behind a door frame, peeking out.
; It is only a picture in your head: it's never there when you get close,
; and it's gone after a blink.
;---------------------------------------------------------------------

Function I1074HideFake()
	If I1074Fake <> 0 Then HideEntity(I1074Fake)
	I1074FakeT = 0 : I1074FakeSeen = 0
End Function

;doorway = 0 north (z 576..768), 1 south (z -896..-704); both in the corridor wall at x ~304..360.
;He stands on the far side, pressed against one jamb, so only part of him shows.
Function I1074ShowFake(doorway%)
	If I1074Fake = 0 Then
		I1074Fake = CopyEntity(ClassDObj)
		Local sc# = 0.5 / MeshWidth(I1074Fake)
		ScaleEntity(I1074Fake, sc, sc, sc)
		EntityFX(I1074Fake, 0)
		;same cull box the Class-D NPCs use, or the animated mesh can get culled while it is on screen
		MeshCullBox(I1074Fake, -MeshWidth(ClassDObj), -MeshHeight(ClassDObj), -MeshDepth(ClassDObj)*4, MeshWidth(ClassDObj)*2, MeshHeight(ClassDObj)*2, MeshDepth(ClassDObj)*8)
	EndIf
	;standing right in the opening (wall x 304..360), a little to one side of centre so the frame hides an edge of him
	Local lz# = 700.0
	If doorway = 1 Then lz = -830.0
	TFormPoint(345.0, 0.0, lz, I1074Room\obj, 0)
	PositionEntity(I1074Fake, TFormedX(), TFormedY(), TFormedZ(), True)
	;sanity checks at runtime: never next to the painting or the player, and only where the player can
	;actually see the spot (head height) from where they are standing
	If EntityDistance(I1074Fake, I1074Pivot) < 3.0 Or EntityDistance(I1074Fake, Collider) < 5.0 Then
		HideEntity(I1074Fake) : I1074FakeCool = 70*5
		Return
	EndIf
	Local head% = CreatePivot()
	PositionEntity(head, EntityX(I1074Fake, True), EntityY(I1074Fake, True) + 1.4, EntityZ(I1074Fake, True), True)
	Local vis% = EntityVisible(Camera, head)
	FreeEntity(head)
	If Not vis Then
		HideEntity(I1074Fake) : I1074FakeCool = 70*3
		Return
	EndIf
	;facing out into the corridor, toward the player
	PointEntity(I1074Fake, Collider)
	RotateEntity(I1074Fake, 0, EntityYaw(I1074Fake) - 180.0, 0)
	SetAnimTime(I1074Fake, 212)
	ShowEntity(I1074Fake)
	I1074FakeT = 70*25 : I1074FakeSeen = 0
End Function

Function UpdateIndev1074Fake()
	If I1074Room = Null Then Return
	If I1074FakeCool > 0 Then I1074FakeCool = I1074FakeCool - FPSfactor

	If I1074FakeT > 0 Then
		I1074FakeT = I1074FakeT - FPSfactor
		Local d# = EntityDistance(I1074Fake, Collider)
		If EntityInView(I1074Fake, Camera) And BlinkTimer > 0 Then
			I1074FakeSeen = I1074FakeSeen + FPSfactor
			If I1074FakeSeen > 0 And I1074FakeSeen - FPSfactor <= 0 Then
				HeartBeatVolume = Max(HeartBeatVolume, 0.6) : HeartBeatRate = Max(HeartBeatRate, 130)
				IndevStress = Min(100, IndevStress + 6)
			EndIf
		EndIf
		;gone when you get close, after a blink once you've seen him, or when he's waited long enough
		If d < 3.5 Or (I1074FakeSeen > 35 And BlinkTimer < -3) Or I1074FakeT <= 0 Or PlayerRoom <> I1074Room Or I1074Stage > 0 Then
			If I1074FakeSeen > 35 And MsgTimer <= 0 Then
				Msg = "The doorway is empty. Of course it is. You can still see him when you close your eyes." : MsgTimer = 70*4
			EndIf
			I1074HideFake()
			I1074FakeCool = 70 * Rnd(25, 45)
		EndIf
		Return
	EndIf

	;only after you've looked at the painting, only in this room, and never right in front of you
	If (Not I1074Exposed) Or I1074Stage > 0 Or I1074FakeCool > 0 Then Return
	If PlayerRoom <> I1074Room Or KillTimer < 0 Then Return
	TFormPoint(EntityX(Collider, True), 0, EntityZ(Collider, True), 0, I1074Room\obj)
	Local pz# = TFormedZ(), px# = TFormedX()
	If px > 300 Then Return ;he watches the corridor, not the halls
	;the doorway you're further from, as long as it's at a good distance
	Local door% = 0
	If Abs(pz - 672.0) < Abs(pz + 800.0) Then door = 1
	Local dz# = Abs(pz - 672.0) : If door = 1 Then dz = Abs(pz + 800.0)
	If dz < 700 Or dz > 1700 Then Return
	I1074ShowFake(door)
End Function
