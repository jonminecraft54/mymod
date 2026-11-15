;=====================================================================
; SCP: Containment Breach - Indev hazards
;
;   SCP-718  an eye on a stalk that stares. Stay in its sight and the
;            paranoia builds until you smash it. Its fluid blisters, and
;            a copy grows - on the floor, or on you. A first aid kit can
;            cut it out (it hurts). Leave it, and it shows you things.
;   SCP-719  a 1975 GE Porta-Color TV. Click to switch it on/off. Watch
;            the same broadcast too long and it drifts toward a burning,
;            sun-worshipping broadcast while the radiation doubles.
;            Turning it off resets it. Leave it on and it overloads.
;   SCP-770  radioactive slime mould in an iron flask (an item). Open it
;            and white-hot mould spreads across the floor, burning and
;            irradiating anything near it.
;
; Hazmat suits cut radiation and keep SCP-718's fluid off your skin.
;=====================================================================

;---------------- SCP-718
Global I718Stalk%, I718Eye%, I718Room.Rooms, I718Checked%
Global I718Alive%, I718Regrow#, I718Stare#, I718StareStage%
Global I718Blister#, I718Host%, I718Sanity#, I718Next#, I718Pending$

;---------------- SCP-719
Global I719TV%, I719Screen%, I719Room.Rooms
Global I719On%, I719T#, I719Anim#, I719Dead%, I719Frame%, I719MsgStage%
Global I719Tex%[9], I719HumCHN%, I719Hum%, I719Pick%

;---------------- SCP-770
Type I770Patch
	Field spr%, x#, y#, z#, size#, target#
End Type
Global I770Active%, I770Tex%, I770SporeT#, I770Patches%, I770MsgT#

;---------------- shared
Global IHzGeigerLo%, IHzGeigerHi%, IHzGeigerCHN%, IHzGeigerT#, IHzRadMsg#

Function IndevHazardsReset()
	If I718Host Or I719On Then UnableToMove = False
	I718Stalk = 0 : I718Eye = 0 : I718Room = Null : I718Checked = False
	I718Alive = True : I718Regrow = 0 : I718Stare = 0 : I718StareStage = 0
	I718Blister = 0 : I718Host = False : I718Sanity = 100 : I718Next = 0 : I718Pending = ""
	I719TV = 0 : I719Screen = 0 : I719Room = Null
	I719On = False : I719T = 0 : I719Anim = 0 : I719Dead = False : I719Frame = 0 : I719MsgStage = 0
	I719HumCHN = 0 : I719Hum = 0 : I719Pick = 0
	Local p.I770Patch
	For p = Each I770Patch : Delete p : Next ;sprites were freed with the old world
	I770Active = False : I770Tex = 0 : I770SporeT = 0 : I770Patches = 0 : I770MsgT = 0
	IHzGeigerLo = 0 : IHzGeigerHi = 0 : IHzGeigerCHN = 0 : IHzGeigerT = 0 : IHzRadMsg = 0
	IndevCogOn = False : IndevCogSanity = 0
End Function

Function UpdateIndevHazards()
	UpdateIndev718()
	UpdateIndev719()
	UpdateIndev770()
	UpdateIndevCogGlasses()
	UpdateIndev122()
	UpdateIndev202()
	UpdateIndev693()
	UpdateIndev113()
	UpdateIndev109()
	UpdateIndev963()
	UpdateIndev458()
	UpdateIndev268()
	UpdateIndev173B()
	UpdateIndev1155()
	UpdateIndev2536()
	UpdateIndev2935()
	UpdateIndev140()
	UpdateIndev131()
	UpdateIndevRoomExtras()
	UpdateIndevXmas()
	UpdateIndev005()
	UpdateIndevNoteOff2()
	UpdateIndev1471()
	UpdateIndevNewRoom1()
	UpdateIndevNewRoom2()
	UpdateIndev1074()
	UpdateIndevOldBill()
	UpdateIndevNewRoom8()
	UpdateIndevNewRoom65()
	UpdateIndevMjolnir()
	UpdateIndevArmor()
	UpdateIndevStress()
	UpdateIndevMemory()
	UpdateIndev2107() ;SCP-2107's haunting (IndevU27.bb)
	UpdateIndev983() ;SCP-983's luminescent candy (IndevU28.bb)
	UpdateIndev29() ;SCP-867's seed, SCP-820-JP's transmitter, the Moon's gravity (IndevU29.bb)
	UpdateIndev30() ;SCP-4427's trait, SCP-4433's calls, the thermal figures (IndevU30.bb)
	UpdateIndev31() ;SCP-467's day, SCP-178's entities, SCP-198, SCP-207, SCP-1079, SCP-1650 (IndevU31.bb)
	UpdateIndev33() ;SCP-1007's years, SCP-1563's grip, SCP-4890's tour, SCP-7042's animals (IndevU33.bb)
	UpdateIndev34() ;the deep storage areas: spinning things, timed effects, the ten items (IndevU34.bb)
	UpdateIndev35() ;storage areas 10-11: the drifting heads, the fortune, the four items (IndevU35.bb)
	UpdateIndev36() ;the candy SCPs' effects, SCP-1921-A2 at work (IndevU36.bb)
	UpdateIndev37() ;SCP-028's migraines (IndevU37.bb)
	UpdateIndev38() ;SCP-1117-3: fatigue and the food that finds you (IndevU38.bb)
	UpdateIndev42() ;SCP-1577-2's arrival, SCP-439 (IndevU42.bb)
	UpdateIndevMeters()
	UpdateIndevBlink()
End Function

;---------------- Cognitive Filter Glasses (CF-1)
;worn from the inventory like the gas mask; they soften visual/cognitive effects instead of blocking them
Function IndevUseCogGlasses()
	If IndevCogOn Then
		IndevCogOn = False
		Msg = "You take off the Cognitive Filter Glasses. Colours are a little too sharp for a moment."
		MsgTimer = 70*4
		Return
	EndIf
	If WearingNightVision > 0 Then
		Msg = "You can't fit the glasses on under the night vision goggles."
		MsgTimer = 70*4
		Return
	EndIf
	If WearingHazmat > 0 Then
		Msg = "You can't put glasses on through the hazmat hood."
		MsgTimer = 70*4
		Return
	EndIf
	IndevCogOn = True
	IndevCogSanity = Sanity
	Msg = "You put on the Cognitive Filter Glasses. Everything takes on a faint teal tint, and your head feels quieter."
	MsgTimer = 70*5
End Function

Function UpdateIndevCogGlasses()
	If (Not IndevCogOn) Then Return

	;dropped, or swapped for goggles / the hazmat suit
	Local n%, have% = False
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "cogglasses" Then have = True : Exit
		EndIf
	Next
	If (Not have) Or WearingNightVision > 0 Or WearingHazmat > 0 Then
		IndevCogOn = False
		If have Then
			Msg = "You take the glasses off to make room."
			MsgTimer = 70*3
		EndIf
		Return
	EndIf

	;blur, shaking and flashes wear off much faster
	If BlurTimer > 0 Then BlurTimer = Max(0, BlurTimer - FPSfactor * 2.0)
	If CameraShake > 0 Then CameraShake = Min(CameraShake, 1.5) * 0.9
	If LightFlash > 0 Then LightFlash = LightFlash * 0.8
	If Pill5043Blind > 0 Then Pill5043Blind = Max(0, Pill5043Blind - FPSfactor)

	;psychological strain (SCP-895 and friends): only half of any sanity loss gets through
	If Sanity < IndevCogSanity Then Sanity = IndevCogSanity + (Sanity - IndevCogSanity) * 0.5
	IndevCogSanity = Sanity
End Function

;radiation: dose in "injuries per second" scaled by the suit
Function IHzIrradiate(rate#)
	If rate <= 0 Then Return
	Local rawRate# = rate
	If WearingHazmat > 0 Then rate = rate * 0.15
	If IndevMjolnirOn Then rate = rate * 0.05 ;hardened against radiation
	IndevMeterRadiation(rawRate, rate)
	Injuries = Injuries + rate * FPSfactor / 70.0
	;geiger counter clicks faster the worse it is
	IHzGeigerT = IHzGeigerT - FPSfactor
	If IHzGeigerT <= 0 Then
		If IHzGeigerLo = 0 Then IHzGeigerLo = LoadSound_Strict("SFX\SCP\770\GeigerLow.ogg")
		If IHzGeigerHi = 0 Then IHzGeigerHi = LoadSound_Strict("SFX\SCP\770\GeigerHigh.ogg")
		If rate > 0.01 Then
			IHzGeigerCHN = PlaySound_Strict(IHzGeigerHi)
		Else
			IHzGeigerCHN = PlaySound_Strict(IHzGeigerLo)
		EndIf
		IHzGeigerT = 70*2.9
	EndIf
	IHzRadMsg = IHzRadMsg - FPSfactor
	If IHzRadMsg <= 0 And rate > 0.002 Then
		Select Rand(1,4)
			Case 1 Msg = "Your skin prickles, like the start of a sunburn."
			Case 2 Msg = "There's a metallic taste in your mouth."
			Case 3 Msg = "A wave of nausea rolls through you."
			Default Msg = "Your skin feels hot and tight."
		End Select
		If WearingHazmat > 0 Then Msg = Msg + " The suit is only doing so much."
		MsgTimer = 70*4
		IHzRadMsg = 70*Rnd(12,20)
	EndIf
End Function

;settle an entity onto the surface below (world coordinates)
;snap e onto the floor right under it, but only if that floor is within half a metre (no long drops, no climbing)
Function IHzSettleNear(e%)
	Local x# = EntityX(e, True), y# = EntityY(e, True), z# = EntityZ(e, True)
	If LinePick(x, y + 0.5, z, 0, -1.0, 0) <> 0 Then
		If Abs(PickedY() - y) < 0.5 Then PositionEntity(e, x, PickedY(), z, True)
	EndIf
End Function

Function IHzSettle(e%, lift#)
	Local x# = EntityX(e, True), y# = EntityY(e, True), z# = EntityZ(e, True)
	If LinePick(x, y + 0.3, z, 0, -4.0, 0) <> 0 Then PositionEntity(e, x, PickedY() + lift, z, True)
End Function

;=====================================================================
; SCP-718
;=====================================================================

;placed on the first gameplay frame: the prototype room if the map has one, otherwise an HCZ dead end
Function IndevEnsure718()
	I718Checked = True
	If I718Stalk <> 0 Then Return
	Local r.Rooms, pick.Rooms = Null, lx#, lz#, dx#, dz#
	For r = Each Rooms
		If r\RoomTemplate\Name = "roompj" Then pick = r : Exit
	Next
	If pick = Null Then
		For r = Each Rooms
			If r\RoomTemplate\Name = "endroom2" And r <> Indev990Room And r <> I738Room Then pick = r : Exit
		Next
	EndIf
	If pick = Null Then Return
	;(both spots checked against the room meshes: open floor, clear of the walls)
	If pick\RoomTemplate\Name = "roompj" Then
		lx = 400 : lz = 600
		dx = 280 : dz = 600
	Else
		lx = 0 : lz = -150
		dx = -120 : dz = -240
	EndIf

	I718Room = pick
	I718Stalk = LoadMesh_Strict("GFX\map\Props\scp718_stalk.b3d", pick\obj)
	EntityTexture(I718Stalk, LoadTexture_Strict("GFX\map\Props\scp718_stalk.png", 1))
	ScaleEntity(I718Stalk, 1.9, 1.9, 1.9)
	;stood on the room's floor (y 0), then snapped to the real floor only if one is found close by - the old
	;drop from 200 units up left it floating whenever the ray missed
	PositionEntity(I718Stalk, lx, 0, lz, False)
	IHzSettleNear(I718Stalk)
	I718Eye = LoadMesh_Strict("GFX\map\Props\scp718_eye.b3d", pick\obj)
	EntityTexture(I718Eye, LoadTexture_Strict("GFX\map\Props\scp718_eye.png", 1))
	ScaleEntity(I718Eye, 1.9, 1.9, 1.9)
	I718PlaceEye()
	EntityPickMode(I718Eye, 2)

	;the document goes on the floor a little away from the stalk, in room-local space (the room is
	;already rotated by now, so a world-space offset would swing it into a wall on some seeds)
	Local it.Items = CreateItem("doc718", EntityX(I718Stalk, True), EntityY(I718Stalk, True) + 0.5, EntityZ(I718Stalk, True))
	EntityParent(it\collider, pick\obj)
	PositionEntity(it\collider, dx, 120.0, dz, False)
	ResetEntity(it\collider)
	DebugLog "Indev: SCP-718 placed in " + pick\RoomTemplate\Name
End Function

;how far a regrowing copy has come: 1 = full size (it regrows over the last minute of I718Regrow)
Function I718Growth#()
	If I718Alive Then Return 1.0
	Return Max(0.15, 1.0 - I718Regrow / (70.0*60))
End Function

Function I718PlaceEye()
	;the eye sits on top of the stalk: 119cm * 1.9 RoomScale units per cm, times the growth
	Local h# = 119.0 * 1.9 * RoomScale * I718Growth()
	PositionEntity(I718Eye, EntityX(I718Stalk, True), EntityY(I718Stalk, True) + h, EntityZ(I718Stalk, True), True)
	ScaleEntity(I718Eye, 1.9 * I718Growth(), 1.9 * I718Growth(), 1.9 * I718Growth())
End Function

;hooked into the first aid kit (Main.bb)
Function IndevNeedsSurgery%()
	Return (I718Host Or I718Blister > 0)
End Function

Function IndevFirstAidUsed()
	If I718Host Then
		I718Host = False
		Injuries = Injuries + 1.2
		Bloodloss = Min(Bloodloss + 20, 90)
		CameraShake = 3
		I718Pending = "You dig the thing out of your arm with the scissors from the kit. The pain is indescribable. When it's done, you can still feel a faint urge to go back and destroy the other one."
	ElseIf I718Blister > 0 Then
		I718Blister = 0
		Injuries = Injuries + 0.2
		I718Pending = "You lance the black blister on your arm and scrub it clean. Something small and wet comes out with the fluid. You stamp on it."
	EndIf
End Function

Function UpdateIndev718()
	If (Not I718Checked) Then IndevEnsure718()
	Local dt# = FPSfactor / 70.0

	If I718Pending <> "" And MsgTimer < 70*2 Then
		Msg = I718Pending : MsgTimer = 70*8 : I718Pending = ""
	EndIf

	;--- a copy growing on the player
	If I718Blister > 0 Then
		I718Blister = I718Blister - FPSfactor
		If I718Blister < 70*60 And I718Next <= 0 Then
			Msg = "The blister on your arm has turned black. Something inside it is moving."
			MsgTimer = 70*5
			I718Next = 99999
		EndIf
		If I718Blister <= 0 Then
			I718Blister = 0
			I718Host = True
			I718Sanity = 100
			I718Next = 70*20
			Msg = "The blister bursts. Something small and wet unfolds from your forearm - and opens its eye."
			MsgTimer = 70*7
			CameraShake = 2
		EndIf
	EndIf
	If I718Host Then
		I718Sanity = I718Sanity - dt * 100.0 / (60*6) ;about six minutes
		I718Next = I718Next - FPSfactor
		If I718Next <= 0 Then
			;seeing through it: [DATA EXPUNGED], at the expense of normal sight
			BlurTimer = 70*4
			CurrCameraZoom = Max(CurrCameraZoom, 15)
			BlinkTimer = Min(BlinkTimer, -8)
			If I718Sanity > 60 Then
				Msg = "For a moment you see through the eye on your arm. You wish you hadn't."
			ElseIf I718Sanity > 30 Then
				Msg = "The eye shows you what is standing right behind everyone in the facility. It's standing behind you, too."
			Else
				Msg = "You can't stop seeing it. You can't stop seeing it. You can't stop"
			EndIf
			MsgTimer = 70*5
			I718Next = 70*Rnd(15,30) * Max(0.3, I718Sanity / 100.0)
		EndIf
		If I718Sanity <= 0 Then
			I718Host = False
			DeathMSG = "Subject D-9341 was found dead by suicide. A copy of SCP-718 was growing from the subject's left forearm; it burst shortly after death. The subject had written on the surrounding walls in their own blood. The writing has been [DATA EXPUNGED]."
			Kill()
		EndIf
	EndIf

	If I718Stalk = 0 Then Return

	;--- a destroyed eye grows back from the fluid on the floor
	If (Not I718Alive) Then
		I718Regrow = I718Regrow - FPSfactor
		If I718Regrow <= 70*60 Then
			If I718Regrow <= 0 Then I718Regrow = 0
			ShowEntity(I718Stalk) : ShowEntity(I718Eye)
			If I718Regrow = 0 Then I718Alive = True : I718Stare = 0 : I718StareStage = 0
			ScaleEntity(I718Stalk, 1.9, 1.9 * I718Growth(), 1.9)
			I718PlaceEye()
		EndIf
		Return
	EndIf

	;--- the eye turns to follow the player; the stalk leans a little after them
	PointEntity(I718Eye, Camera)
	Local dist# = EntityDistance(I718Eye, Camera)
	Local seen% = (dist < 7.0 And EntityVisible(I718Eye, Camera))
	If seen Then
		TurnEntity(I718Stalk, 0, DeltaYaw(I718Stalk, Camera) * 0.02, 0)
		Local stareRate# = 1.0
		If WearingHazmat > 0 Then stareRate = 0.5
		If IndevCogOn Then stareRate = stareRate * 0.35 ;the filter film breaks up its gaze
		I718Stare = I718Stare + dt * stareRate
	Else
		I718Stare = Max(0, I718Stare - dt * 0.5)
	EndIf

	If seen And I718StareStage = 0 And I718Stare > 3 Then
		I718StareStage = 1 : Msg = "The eye on the stalk turns. It's looking at you." : MsgTimer = 70*4
	ElseIf I718StareStage = 1 And I718Stare > 12 Then
		I718StareStage = 2 : Msg = "It hasn't blinked. It doesn't blink. Why is it looking at you like that?" : MsgTimer = 70*5
	ElseIf I718StareStage = 2 And I718Stare > 25 Then
		I718StareStage = 3 : Msg = "You can feel it inside your head. You need to make it stop looking. You need to destroy it." : MsgTimer = 70*6
	ElseIf I718StareStage = 3 And I718Stare > 40 Then
		Msg = "Before you know what you're doing, you've lunged at the eye."
		MsgTimer = 70*5
		I718Burst()
		Return
	EndIf
	If I718StareStage >= 2 And seen And (Not IndevCogOn) Then
		CameraShake = Max(CameraShake, 0.4 * (I718StareStage - 1))
		If Rand(200) = 1 Then BlurTimer = 70*2
	EndIf

	;--- smash it
	If (IndevAimedAt(I718Eye, I718Eye, 1.6) Or IndevAimedAt(I718Stalk, I718Stalk, 1.6)) And KillTimer >= 0 Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			Msg = "You grab the stalk and smash the eye against the floor."
			MsgTimer = 70*4
			I718Burst()
		EndIf
	EndIf
End Function

Function I718Burst()
	I718Alive = False
	I718Regrow = 70*60*3 ;three minutes until a copy has regrown to full size where the fluid landed
	PlaySound2(LoadTempSound("SFX\SCP\718\Burst.ogg"), Camera, I718Eye, 8.0, 1.0)
	Local de.Decals = CreateDecal(0, EntityX(I718Stalk, True), EntityY(I718Stalk, True) + 0.01, EntityZ(I718Stalk, True), 90, Rand(360), 0)
	EntityColor(de\obj, 200, 210, 215) : EntityAlpha(de\obj, 0.6) : de\Size = 0.6 : ScaleSprite(de\obj, de\Size, de\Size)
	HideEntity(I718Eye) : HideEntity(I718Stalk)
	;the fluid gets on the player if they're close enough - unless they're in a hazmat suit
	If EntityDistance(Collider, I718Stalk) < 2.2 And I718Blister <= 0 And (Not I718Host) Then
		If WearingHazmat > 0 Or IndevMjolnirOn Then
			Msg = Msg + " Clear fluid spatters across your hazmat suit. You wipe it off, very, very carefully."
		Else
			I718Blister = 70*60*2
			I718Next = 0
			Msg = Msg + " It bursts, spraying clear fluid over your arm. A clear, blister-like bubble rises where it landed."
		EndIf
		MsgTimer = 70*7
	EndIf
	I718Stare = 0 : I718StareStage = 0
End Function

;=====================================================================
; SCP-719
;=====================================================================

;called from FillRoom: TV at room-local (lx, ly, lz), facing yaw, settled on the desk below
Function IndevCreate719%(r.Rooms, lx#, ly#, lz#, yaw#)
	If I719TV <> 0 Then Return False
	I719Room = r
	I719TV = LoadMesh_Strict("GFX\map\Props\scp719.b3d", r\obj)
	EntityTexture(I719TV, LoadTexture_Strict("GFX\map\Props\scp719.png", 1))
	ScaleEntity(I719TV, 1.9, 1.9, 1.9)
	;straight onto the desk top (no settle ray at map generation - the desk isn't pickable yet and the TV fell
	;through it). room2offices4's desk top is at y -264, checked against the room mesh; the model is centred.
	If r\RoomTemplate\Name = "room2offices4" Then ly = -264.0 + 34.0 / 2 * 1.9
	PositionEntity(I719TV, lx, ly, lz, False)
	RotateEntity(I719TV, 0, yaw, 0, False)
	EntityType(I719TV, HIT_MAP)
	EntityPickMode(I719TV, 2)

	;(screen sprite made on the first frame, unparented, in world units - see UpdateIndev719)
	I719Screen = 0

	Local s%, f%
	For s = 0 To 3
		For f = 1 To 2
			I719Tex[s * 2 + f - 1] = LoadTexture_Strict("GFX\map\Props\scp719_ch" + s + "_" + f + ".png", 1)
		Next
	Next
	I719Tex[8] = LoadTexture_Strict("GFX\map\Props\scp719_off.png", 1)
	Return True
End Function

Function I719SetPower(onoff%)
	I719On = onoff
	I719T = 0 : I719MsgStage = 0
	If I719HumCHN <> 0 Then
		If ChannelPlaying(I719HumCHN) Then StopChannel(I719HumCHN)
		I719HumCHN = 0
	EndIf
	If I719On Then
		EntityTexture(I719Screen, I719Tex[0])
	Else
		EntityTexture(I719Screen, I719Tex[8])
	EndIf
End Function

Function UpdateIndev719()
	If I719TV = 0 Then Return
	If I719Screen = 0 Then
		;the picture tube: TV-local point (-7, 0, -18.2) cm, 13.4 x 12.6 cm -> world (1.9 x RoomScale per cm)
		TFormPoint(-7.0, 0.0, -18.4, I719TV, 0)
		I719Screen = CreateSprite()
		PositionEntity(I719Screen, TFormedX(), TFormedY(), TFormedZ(), True)
		RotateEntity(I719Screen, EntityPitch(I719TV, True), EntityYaw(I719TV, True), EntityRoll(I719TV, True), True)
		SpriteViewMode(I719Screen, 2)
		ScaleSprite(I719Screen, 13.4 * 1.9 * RoomScale, 12.6 * 1.9 * RoomScale)
		EntityFX(I719Screen, 1 + 16)
		If I719Dead Then
			EntityTexture(I719Screen, I719Tex[8]) : EntityColor(I719Screen, 40, 35, 30)
		Else
			EntityTexture(I719Screen, I719Tex[8])
		EndIf
		If I719Room <> Null Then EntityParent(I719Screen, I719Room\obj, True) ;hidden together with the room
		TFormPoint(0, 0, 0, I719TV, 0)
		I719Pick = CreatePivot()
		PositionEntity(I719Pick, TFormedX(), TFormedY(), TFormedZ(), True)
		EntityRadius(I719Pick, 0.2)
		EntityPickMode(I719Pick, 1, False)
	EndIf

	If IndevAimedAt(I719TV, I719Pick, 1.8) And (Not I719Dead) And KillTimer >= 0 Then
		DrawHandIcon = True
		If MouseHit1 Then
			MouseHit1 = False
			If I719On Then
				I719SetPower(False)
				Msg = "You switch the set off. The picture shrinks to a dot and is gone. The Geiger ticks slow down."
			Else
				I719SetPower(True)
				Msg = "You turn the ON/VOL knob. The old set warms up with a hum, and a picture comes in on channel 3: a family outside a little house, waving."
			EndIf
			MsgTimer = 70*5
		EndIf
	EndIf
	If (Not I719On) Then Return

	I719T = I719T + FPSfactor / 70.0
	I719Anim = I719Anim + FPSfactor

	;hum: an old tube set warming the room
	If I719Hum = 0 Then I719Hum = LoadSound_Strict("SFX\SCP\719\Hum.ogg")
	If I719HumCHN = 0 Or (Not ChannelPlaying(I719HumCHN)) Then I719HumCHN = PlaySound2(I719Hum, Camera, I719TV, 6.0, 0.6)

	;the broadcast drifts after a minute on the same signal (13.6 minutes, sped up)
	Local stage% = 0
	If I719T > 60 Then stage = 1
	If I719T > 105 Then stage = 2
	If I719T > 150 Then stage = 3
	If I719Anim > 20 Then
		I719Anim = 0
		I719Frame = 1 - I719Frame
		EntityTexture(I719Screen, I719Tex[stage * 2 + I719Frame])
	EndIf
	If stage > I719MsgStage And EntityDistance(Collider, I719TV) < 6 Then
		I719MsgStage = stage
		Select stage
			Case 1 Msg = "The picture on the old TV is brighter than it should be. The sun in the show looks bigger."
			Case 2 Msg = "On screen, the grass has gone brown. The family is kneeling now, all facing one of them. The TV is hot to be near."
			Case 3 Msg = "The screen is almost white. A figure on it is speaking, and the others burn as they kneel and listen."
		End Select
		MsgTimer = 70*5
	EndIf

	;radiation: doubles every 30 seconds of continuous operation (15 minutes, sped up)
	Local dist# = EntityDistance(Collider, I719TV)
	Local rate# = 0.0006 * 2 ^ (I719T / 30.0) / (1.0 + (dist / 1.5) ^ 2)
	If dist < 10 Then IHzIrradiate(rate)

	;the 75 minute limit (5 minutes, sped up): the tubes overload
	If I719T > 300 Then
		I719SetPower(False)
		I719Dead = True
		EntityColor(I719TV, 60, 55, 50)
		LightFlash = 3
		If dist < 5 And WearingHazmat = 0 Then
			DeathMSG = "Subject D-9341 was found beside SCP-719 with severe radiation burns over the entire body. Dosimeters in the room had failed. The last frame recorded on the security camera shows the television's screen, completely white."
			Kill()
		Else
			Msg = "The old TV flashes blinding white and dies with a crack. The picture tube is black and blistered."
			MsgTimer = 70*5
			If dist < 5 Then Injuries = Injuries + 1.5
		EndIf
	EndIf
End Function

;=====================================================================
; SCP-770
;=====================================================================

;releases the mould at a world position (floor below is found automatically)
Function IndevRelease770(x#, y#, z#)
	I770Active = True
	I770SporeT = 70*20
	If I770Tex = 0 Then I770Tex = LoadTexture_Strict("GFX\map\Props\scp770_mould.png", 1 + 2)
	I770AddPatch(x, y, z, 0.2)
End Function

Function I770AddPatch(x#, y#, z#, size#)
	If I770Patches >= 24 Then Return
	Local fy# = y
	If LinePick(x, y + 0.6, z, 0, -3.0, 0) <> 0 Then fy = PickedY() Else Return
	Local p.I770Patch = New I770Patch
	p\x = x : p\y = fy + 0.012 : p\z = z
	p\size = 0.05 : p\target = size
	p\spr = CreateSprite()
	EntityTexture(p\spr, I770Tex)
	SpriteViewMode(p\spr, 2)
	RotateEntity(p\spr, 90, Rnd(360), 0)
	PositionEntity(p\spr, p\x, p\y, p\z)
	EntityFX(p\spr, 1 + 16)
	EntityBlend(p\spr, 3)
	ScaleSprite(p\spr, p\size, p\size)
	I770Patches = I770Patches + 1
End Function

Function UpdateIndev770()
	If (Not I770Active) Then Return
	Local p.I770Patch, dx#, dz#, d#, burn% = False, rad# = 0
	For p = Each I770Patch
		;each patch keeps feeding and growing
		If p\size < p\target Then
			p\size = Min(p\target, p\size + FPSfactor * 0.0004)
			ScaleSprite(p\spr, p\size, p\size)
		EndIf
		EntityAlpha(p\spr, 0.75 + 0.25 * Sin(MilliSecs() / 7.0 + p\x * 300))
		dx = EntityX(Collider) - p\x : dz = EntityZ(Collider) - p\z
		d = Sqr(dx * dx + dz * dz)
		If d < p\size * 0.8 And Abs(EntityY(Collider) - p\y) < 1.0 Then burn = True
		If Abs(EntityY(Collider) - p\y) < 3.0 Then rad = rad + p\size * 0.02 / (1.0 + d * d)
	Next

	;spores: a new patch nearby every so often, bigger each time
	I770SporeT = I770SporeT - FPSfactor
	If I770SporeT <= 0 And I770Patches < 24 Then
		Local pick% = Rand(1, I770Patches), n% = 0
		For p = Each I770Patch
			n = n + 1
			If n = pick Then
				Local a# = Rnd(360), r# = Rnd(0.5, 1.3)
				I770AddPatch(p\x + Cos(a) * r, p\y, p\z + Sin(a) * r, Min(0.2 + I770Patches * 0.03, 0.7))
				Exit
			EndIf
		Next
		I770SporeT = 70*Rnd(14,22)
	EndIf

	If burn Then
		If WearingHazmat > 0 Then Injuries = Injuries + FPSfactor * 0.0015 Else Injuries = Injuries + FPSfactor * 0.004
		I770MsgT = I770MsgT - FPSfactor
		If I770MsgT <= 0 Then
			Msg = "The mould is white-hot. The soles of your shoes are melting into it."
			MsgTimer = 70*3
			I770MsgT = 70*5
		EndIf
		CameraShake = Max(CameraShake, 0.5)
	EndIf
	If rad > 0.0002 Then IHzIrradiate(rad)
End Function

;the flask item: first use reads the warning, second use opens it
Function IndevUse770(it.Items)
	If it\state < 1 Then
		it\state = 1
		Msg = "The iron flask is heavy and warm. The label warns that it must never be opened outside a sealed laboratory. (Use it again to unscrew the cap.)"
		MsgTimer = 70*6
		SelectedItem = Null
		Return
	EndIf
	Msg = "You unscrew the cap. Something colourless and wet slides out over your hand and onto the floor - and starts to glow."
	MsgTimer = 70*7
	Injuries = Injuries + 0.3
	IndevRelease770(EntityX(Collider), EntityY(Collider), EntityZ(Collider) + 0.3)
	RemoveItem(it)
	SelectedItem = Null
End Function
