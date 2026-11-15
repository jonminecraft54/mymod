;=====================================================================
; SCP: Containment Breach - Indev "Old Bill" (SCP-513-1)
;
;   every few minutes a cowbell clangs over the facility intercom. A few
;   seconds later Old Bill is standing somewhere behind the player, on the
;   route they just walked, and starts following that trail.
;     - he moves slowly while you look at him and quickly when you don't
;     - staring at him for a few seconds (eyes open) makes him fade away
;     - if he catches up he hurts you and vanishes
;     - otherwise he gives up after a couple of minutes
;   He follows the player's own footsteps, so he never walks through walls.
;   Texture: GFX\npcs\900px-SCPCB_SCP-513.png (figure on black, drawn additive)
;   Console: "oldbill" rings the bell right away.
;=====================================================================

Const OB_CRUMBS% = 200 ;trail points, one every OB_STEP units
Const OB_STEP# = 0.5

Global OBSprite%, OBState%, OBTimer#, OBT#, OBStare#, OBLife#
Global OBHead%, OBCount%, OBPos# ;OBPos = how far along the trail he is (in crumbs, from the oldest)
Dim OBX#(OB_CRUMBS), OBY#(OB_CRUMBS), OBZ#(OB_CRUMBS)

Function IndevOldBillReset(keepWorld% = False)
	If Not keepWorld Then OBSprite = 0 ;entities are freed with the world
	If OBSprite <> 0 Then HideEntity(OBSprite)
	OBState = 0 : OBT = 0 : OBStare = 0 : OBLife = 0
	OBTimer = 70*60*Rnd(1,3)
	OBHead = 0 : OBCount = 0 : OBPos = 0
End Function

;trail point i, counted from the oldest one still stored
Function OBIndex%(i%)
	Return (OBHead - OBCount + i + OB_CRUMBS * 2) Mod OB_CRUMBS
End Function

Function OBRecordTrail()
	Local x# = EntityX(Collider, True), y# = EntityY(Collider, True), z# = EntityZ(Collider, True)
	If OBCount > 0 Then
		Local prev% = OBIndex(OBCount - 1)
		Local d# = Sqr((x - OBX(prev)) ^ 2 + (y - OBY(prev)) ^ 2 + (z - OBZ(prev)) ^ 2)
		If d > 4.0 Then
			;teleported (elevator, pocket dimension...) - the old trail leads nowhere
			OBCount = 0 : OBPos = 0
			If OBState = 2 Then OBVanish("")
		ElseIf d < OB_STEP
			Return
		EndIf
	EndIf
	OBX(OBHead) = x : OBY(OBHead) = y : OBZ(OBHead) = z
	OBHead = (OBHead + 1) Mod OB_CRUMBS
	If OBCount < OB_CRUMBS Then
		OBCount = OBCount + 1
	Else
		OBPos = Max(0, OBPos - 1) ;the oldest point was dropped
	EndIf
End Function

Function OBRingBell()
	PlaySound_Strict(LoadTempSound("SFX\SCP\513\Bell" + Rand(1,3) + ".ogg"))
	Msg = "The intercom crackles. Somewhere on the other end, a cowbell clangs." : MsgTimer = 70*5
	OBState = 1 : OBT = 70*Rnd(4,8)
End Function

Function OBSpawn%()
	;needs some trail behind the player, far enough back that he isn't right on top of them
	If OBCount < 16 Then Return False
	If OBSprite = 0 Then
		If FileType("GFX\npcs\900px-SCPCB_SCP-513.png") <> 1 Then Return False
		OBSprite = CreateSprite()
		Local tex% = LoadTexture_Strict("GFX\npcs\900px-SCPCB_SCP-513.png", 1)
		EntityTexture(OBSprite, tex)
		FreeTexture(tex)
		SpriteViewMode(OBSprite, 2) ;stays upright, turns to face the camera
		ScaleSprite(OBSprite, 0.95, 0.95)
		EntityBlend(OBSprite, 3) ;black background drops out
		EntityFX(OBSprite, 1 + 8)
	EndIf
	OBPos = Max(0, OBCount - 1 - Rand(14, 24)) ;7-12 units back along the path
	OBStare = 0 : OBLife = 70*Rnd(100,150)
	OBState = 2
	OBPlace()
	ShowEntity(OBSprite)
	Return True
End Function

Function OBPlace()
	Local i% = Floor(OBPos), f# = OBPos - i
	Local a% = OBIndex(i), b% = OBIndex(Min(i + 1, OBCount - 1))
	Local x# = OBX(a) + (OBX(b) - OBX(a)) * f
	Local y# = OBY(a) + (OBY(b) - OBY(a)) * f
	Local z# = OBZ(a) + (OBZ(b) - OBZ(a)) * f
	PositionEntity(OBSprite, x, y + 0.65, z, True) ;collider centre is 0.3 above the feet, sprite is 1.9 tall
End Function

Function OBVanish(txt$)
	If OBSprite <> 0 Then HideEntity(OBSprite)
	OBState = 0 : OBStare = 0
	OBTimer = 70*60*Rnd(2,4)
	If txt <> "" Then Msg = txt : MsgTimer = 70*5
End Function

Function UpdateIndevOldBill()
	If KillTimer < 0 Or PlayerRoom = Null Then
		If OBState = 2 Then OBVanish("")
		Return
	EndIf
	Select PlayerRoom\RoomTemplate\Name
		Case "173", "pocketdimension", "gatea", "dimension1499", "exit1"
			If OBState = 2 Then OBVanish("")
			OBCount = 0 : OBPos = 0
			Return
	End Select

	OBRecordTrail()

	Select OBState
		Case 0
			OBTimer = OBTimer - FPSfactor
			If OBTimer <= 0 Then OBRingBell()
		Case 1
			OBT = OBT - FPSfactor
			If OBT <= 0 Then
				If Not OBSpawn() Then OBT = 70*2 ;not enough trail yet, try again shortly
			EndIf
		Case 2
			Local seen% = False
			If BlinkTimer > 0 And EntityDistance(OBSprite, Camera) < 14.0 Then
				If EntityInView(OBSprite, Camera) Then seen = EntityVisible(Camera, OBSprite)
			EndIf

			;follow the trail: creeping while watched, fast when not
			Local speed# = 2.6
			If seen Then speed = 0.5
			OBPos = Min(OBPos + speed * FPSfactor / 70.0 / OB_STEP, OBCount - 1)
			OBPlace()

			Local d# = EntityDistance(OBSprite, Collider)
			If seen Then
				OBStare = OBStare + FPSfactor
				HeartBeatVolume = Max(HeartBeatVolume, 0.6) : HeartBeatRate = Max(HeartBeatRate, 125)
				IndevStress = Min(100, IndevStress + FPSfactor / 70.0 * 2.0)
				If OBStare > 70*4 Then OBVanish("You blink, and the corridor is empty. The smell of rot stays a little longer.") : Return
			Else
				OBStare = Max(0, OBStare - FPSfactor * 0.5)
			EndIf

			If d < 0.9 Then
				Injuries = Injuries + Rnd(0.8, 1.4)
				BlurTimer = Max(BlurTimer, 70*4)
				CameraShake = Max(CameraShake, 1.5)
				IndevStress = Min(100, IndevStress + 25)
				OBVanish("Cold, bony hands rake across your back. When you turn around, nobody is there.")
				Return
			EndIf

			OBLife = OBLife - FPSfactor
			If OBLife <= 0 Then OBVanish("")
	End Select
End Function
