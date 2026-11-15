;=====================================================================
; SCP: Containment Breach - Indev: the thirtieth batch - Site-42 (sapient anomaly containment)
;
;   room2b30admin   Site Director Dr. T. Sherman's office, Media Relations & Support, the Ethics Subcommittee for
;                   Sentient & Sapient Anomalies, the Multi-U Dept.
;   room2b30a4      Room G14 (SCP-2758-A). Its door only takes the custom identification card kept in Safe-class
;                   locker #2758 (item card2758). He cannot leave the room; talk to him at the microphone rig.
;   room2b30b4      SCP-4427: a 60 cm sphere at 1.5 m, warm, visible only through the thermal camera (item
;                   thermal4427, use it to switch thermal on and off). 44 people have passed through it. If you
;                   are the 45th, it goes - and a minute and a half later one of the 45 changes. It might be you
;                   (heat flares; SCP-500 calms them). Room 35 holds SCP-4427-B, who forgets; use the intercom.
;   room2b30ocean   SCP-3069: a deep specimen in the tank, the Atlantic map, the SCP-3069-A replica, a specimen jar.
;   room2b30outpost SCP-4433: carry the flip phone (item phone4433) and sooner or later it rings - RESTRICTED. Answer
;                   it (use it) and "family" talks about mother and country; the third call says come home, and
;                   you will go, unless you hang up. On thermal, while they are calling, five figures stand round
;                   you. SCP-4434: the skull of an SCP-4434-C, the Figure A recreation (harmless).
;   room2b30store   SCP-2648 rolls about in its shipping container, humming. Anything dropped in there is gone.
;   Summaries of scp-wiki.wikidot.com/scp-2648, /scp-2758, /scp-3069, /scp-4427, /scp-4433, /scp-4434 and the
;   Site-42 hub page (CC BY-SA 3.0).
;=====================================================================

Global I4427Thermal%, I4427Count%, I4427Trait%, I4427Timer#, I4427In%, I4427Heat#
Global I4433Stage%, I4433Ring#, I4433Ringing#, I4433RingSnd#, I4433Pull#
Global I30Sphere%, I30Amal%, I30AmalScale#, I30Spec%, I30SpecY#, Indev30Uses%
Dim I30Ghost%(4)

Function Indev30Reset(newGame%)
	Local k%
	If newGame Then
		I4427Count = 44 : I4427Trait = 0 : I4427Timer = 0
		I4433Stage = 0 : I4433Pull = 0
	EndIf
	If I4427Count = 0 Then I4427Count = 44
	I4427Thermal = False : I4427In = False : I4427Heat = 70 * 30
	I4433Ring = 70 * 60 * 2 : I4433Ringing = 0
	;I30Sphere / I30Amal / I30Spec / I30AmalScale are not cleared: the rooms set them when built, and a quick
	;load keeps the rooms
	For k = 0 To 4
		I30Ghost(k) = 0
	Next
End Function

;a model at pivot p, standing on the floor below it (or at the pivot's height when atPivot), scaled
Function U30Prop%(r.Rooms, p%, file$, s#, atPivot%)
	Local m%, y#
	If FileType(file) <> 1 Then Return 0
	m = LoadMesh_Strict(file)
	If m = 0 Then Return 0
	ScaleEntity(m, RoomScale * s, RoomScale * s, RoomScale * s)
	If atPivot Then y = EntityY(p, True) Else y = EntityY(r\obj, True)
	PositionEntity(m, EntityX(p, True), y, EntityZ(p, True), True)
	RotateEntity(m, 0, EntityYaw(r\obj, True), 0, True)
	EntityParent(m, r\obj, True)
	Return m
End Function

Function IndevU30Dress(r.Rooms)
	Local m%
	Select r\RoomTemplate\Name
		Case "room2b30b4"
			I30Sphere = CreateSphere(16)
			ScaleEntity(I30Sphere, 0.19, 0.19, 0.19)
			EntityColor(I30Sphere, 255, 150, 40)
			EntityFX(I30Sphere, 1)
			EntityAlpha(I30Sphere, 0.7)
			PositionEntity(I30Sphere, EntityX(r\Objects[U30_B4_SPHERE], True), EntityY(r\Objects[U30_B4_SPHERE], True), EntityZ(r\Objects[U30_B4_SPHERE], True), True)
			EntityParent(I30Sphere, r\obj, True)
			HideEntity(I30Sphere)
		Case "room2b30ocean"
			I30Spec = U30Prop(r, r\Objects[U30_OCN_SPEC], "GFX\map\props\scp3069spec.b3d", 0.7, True)
			If I30Spec <> 0 Then I30SpecY = EntityY(I30Spec, True)
			m = U30Prop(r, r\Objects[U30_OCN_REPLICA], "GFX\map\props\scp3069a.b3d", 0.9, False)
			If m <> 0 Then TranslateEntity(m, 0, 20 * RoomScale, 0)
		Case "room2b30outpost"
			m = U30Prop(r, r\Objects[U30_OUT_SKULL], "GFX\map\props\scp4434c.b3d", 1.6, True)
			If m <> 0 Then TranslateEntity(m, 0, -12 * RoomScale, 0) : TurnEntity(m, 0, 140, 0)
		Case "room2b30store"
			I30Amal = U30Prop(r, r\Objects[U30_STR_AMAL], "GFX\map\props\scp2648.b3d", 0.85, False)
			I30AmalScale = 0.85
	End Select
End Function

;does the player carry an item of this name?
Function U30Has.Items(name$)
	Local i%
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			If Inventory(i)\itemtemplate\name = name Then Return Inventory(i)
		EndIf
	Next
	Return Null
End Function

;a sapient resident standing at pivot p (made the first time you come in), facing the room's door side
Function U30Figure(e.Events, p%, slot%)
	Local n.NPCs
	If e\room\NPC[slot] <> Null Then Return
	n = CreateNPC(NPCtypeD, EntityX(p, True), EntityY(p, True) + 0.3, EntityZ(p, True))
	n\State = 0
	RotateEntity(n\Collider, 0, EntityYaw(e\room\obj, True) + 90, 0)
	e\room\NPC[slot] = n
End Function

Function UpdateIndevU30(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b30admin" : U30Admin(e)
		Case "room2b30a4" : U30A4(e)
		Case "room2b30b4" : U30B4(e)
		Case "room2b30ocean" : U30Ocean(e)
		Case "room2b30outpost" : U30Outpost(e)
		Case "room2b30store" : U30Store(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- administration
Function U30Admin(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U30_ADM_SHERMAN], 1.8) Then
		Indev30Uses = Indev30Uses + 1
		e\EventState2 = (e\EventState2 + 1) Mod 4
		Select e\EventState2
			Case 0 : IS16Tell("A note on Site Director Dr. T. Sherman's desk: 'PRESS 3PM. Smile. They live here too.'", 6)
			Case 1 : IS16Tell("The Director's calendar: town council, Ethics Subcommittee, press, a ribbon-cutting for the new public wing.", 6)
			Case 2 : IS16Tell("A draft speech: 'Site-42 contains people. That is what makes us different, and that is why we answer your questions.'", 7)
			Default : IS16Tell("Sticky note on the monitor: 'Remind Media Relations: no photos past the yellow line. Residents have rights.'", 6)
		End Select
	EndIf
	If IS10Press(r\Objects[U30_ADM_BOARD], 2.0) Then
		IS16Tell("PUBLIC INQUIRIES TODAY: 1,204. The phones in Media Relations & Support never quite stop.", 5)
	EndIf
	If IS10Press(r\Objects[U30_ADM_ETHICS], 2.0) Then
		IS16Tell("The Ethics Subcommittee's agenda: an SCP-4427-A request to keep its civilian identity; Class IV privileges for Room 35.", 6)
	EndIf
	If IS10Press(r\Objects[U30_ADM_MULTIU], 1.8) Then
		IS16Tell("Researcher M. Wickerford's notes on G14: '19 attempts to get him out. None worked. Stop trying - just talk to him.'", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- Wing A4: SCP-2758
Function U30A4(e.Events)
	Local r.Rooms = e\room, d.Doors = r\RoomDoors[U30_A4_D_G14], lx#
	If PlayerRoom <> r Then Return
	U30Figure(e, r\Objects[U30_A4_FIGURE], 0)
	If IS10Press(r\Objects[U30_A4_READER], 1.4) Then
		If U30Has("card2758") <> Null Then
			If d <> Null Then d\locked = False : d\open = True
			IS10Sound("SFX\Indev\beep.wav", r\Objects[U30_A4_READER], 4.0, 0.8)
			IS16Tell("The reader takes Room G14's custom identification. The door unlocks.", 4)
		Else
			IS16Tell("ROOM G14: CUSTOM IDENTIFICATION REQUIRED. (Kept in Safe-class locker #2758.)", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[U30_A4_LOCKER], 1.6) Then
		If Not IAxFlag(e, "c") Then
			IAxSetFlag(e, "c")
			IS16Give("card2758", r\Objects[U30_A4_LOCKER])
			IS16Tell("Locker #2758: one identification card on a lanyard, ROOM G14 CUSTOM ID.", 5)
		Else
			IS16Tell("Locker #2758 is empty.", 3)
		EndIf
	EndIf
	;inside G14 for the first time: the echo of the old process
	TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
	lx = TFormedX()
	If lx > 256 And TFormedZ() < -100 And (Not IAxFlag(e, "v")) Then
		IAxSetFlag(e, "v")
		IS16Tell("For a moment you hear two voices arranging someone in the centre of the room - then only him, sitting there, looking up.", 7)
	EndIf
	If IS10Press(r\Objects[U30_A4_MIC], 1.6) Then
		Indev30Uses = Indev30Uses + 1
		e\EventState3 = (e\EventState3 + 1) Mod 4
		Select e\EventState3
			Case 0 : IAxSay("SCP-2758-A", "You're the new one. They always send a new one. I can't come out, you know - I tried. The door just... un-makes me.", 8)
			Case 1 : IAxSay("SCP-2758-A", "Three minutes and thirty-three seconds. That was how long it used to take for me to happen. Now I just stay.", 8)
			Case 2 : IAxSay("SCP-2758-A", "I remember two people setting me down here. I don't remember anything before that. Is that strange?", 8)
			Default : IAxSay("SCP-2758-A", "Tell the Multi-U people the table's fine. The chair's fine. Could I have a window? No. Of course not.", 8)
		End Select
	EndIf
End Function

;--------------------------------------------------------------------------------------------- Wing B4: SCP-4427
Function U30B4(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U30_B4_SPHERE], d#
	If I30Sphere <> 0 Then
		If I4427Thermal And I4427Count < 45 And PlayerRoom = r Then
			ShowEntity(I30Sphere)
		Else
			HideEntity(I30Sphere)
		EndIf
	EndIf
	If PlayerRoom <> r Then Return
	U30Figure(e, r\Objects[U30_B4_B35], 0)
	;walking through it
	If I4427Count < 45 Then
		d = EntityDistance(Camera, p)
		If d < 0.42 Then
			If Not I4427In Then
				I4427In = True
				I4427Count = I4427Count + 1
				Indev30Uses = Indev30Uses + 1
				If I4427Count >= 45 Then
					I4427Timer = 70 * 90
					IS16Tell("Forty-five. On the monitors the warm blip winks out. Somewhere among the forty-five, something has started.", 7)
				ElseIf I4427Thermal Then
					IS16Tell("You walk straight through the warm sphere. You feel nothing at all. CONTACTS: " + I4427Count + " / 45.", 5)
				EndIf
			EndIf
		ElseIf d > 0.8 Then
			I4427In = False
		EndIf
	EndIf
	If IS10Press(r\Objects[U30_B4_COUNT], 1.8) Then
		IS16Tell("SCP-4427 CONTACTS: " + Min(I4427Count, 45) + " / 45. Do not walk through.", 4)
	EndIf
	If IS10Press(r\Objects[U30_B4_HUME], 1.4) Then
		IS16Tell("ROOM 35 HUME: 112 Hm (minimum 100). Mk. XIII Scranton netting: nominal.", 5)
	EndIf
	If IS10Press(r\Objects[U30_B4_INTERCOM], 1.4) Then
		Indev30Uses = Indev30Uses + 1
		e\EventState3 = (e\EventState3 + 1) Mod 3
		Select e\EventState3
			Case 0 : IAxSay("SCP-4427", "Hello? Have we met? Sorry - I'm SCP-4427. That's what they call me. I think I knew my name this morning.", 8)
			Case 1 : IAxSay("SCP-4427", "The walls hum. They say it's the netting. Keeps me... steady. I don't know what I'd do without it. I don't want to know.", 8)
			Default : IAxSay("SCP-4427", "Do you ever feel like you walked through something? Like you're the one it picked? ...Never mind. Have we met?", 8)
		End Select
	EndIf
	If IS10Press(r\Objects[U30_B4_THERM], 2.0) Then
		IS16Tell("AC-27 RELAY: no new SCP-4427 manifestations. I-40 cameras clear. Nearest response team: Site-42 Media Relations on standby.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- SCP-3069
Function U30Ocean(e.Events)
	Local r.Rooms = e\room
	If I30Spec <> 0 Then
		TurnEntity(I30Spec, 0, 0.08 * FPSfactor, 0)
		PositionEntity(I30Spec, EntityX(I30Spec, True), I30SpecY + 0.06 * Sin(MilliSecs() * 0.02), EntityZ(I30Spec, True), True)
	EndIf
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U30_OCN_MAP], 2.4) Then
		IS16Tell("SCP-3069: some 6000 km of structure under the North Atlantic. Access Point I at 3500 m, II blocked at 3200 m, III at 4000 m round SCP-3069-A.", 7)
	EndIf
	If IS10Press(r\Objects[U30_OCN_CONSOLE], 2.0) Then
		IS16Tell("GAMMA-6 TELEMETRY: AP I hatch closed. New specimens released this week: 3. Excursions below explored depth: NOT AUTHORISED.", 6)
	EndIf
	If IS10Press(r\Objects[U30_OCN_REPLICA], 2.2) Then
		IS16Tell("A replica of SCP-3069-A: a two-metre steel pole and a phosphorescent green sphere. The real one cannot be moved, and bends space 4000 m down.", 7)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- Outposts 4433-A / 4434
Function U30Outpost(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U30_OUT_FEEDS], 2.4) Then
		IS16Tell("CAM 2: the burnt-out house behind its fence, nobody inside. CAM 5: the valley, the hole at the bottom. A drone went down it once.", 7)
	EndIf
	If IS10Press(r\Objects[U30_OUT_RADIO], 1.8) Then
		If I4433Ringing > 0 Or I4433Pull > 0 Then
			IS10Sound("SFX\Radio\static.ogg", r\Objects[U30_OUT_RADIO], 5.0, 0.8)
			IS16Tell("Every band is static. Outpost 4433-A logs radio, radar and microwave disruption - they are in the house.", 6)
		Else
			IS16Tell("Outpost 4433-A: radio clear. Outpost-4434: 15 personnel, no trespassers today.", 5)
		EndIf
	EndIf
	If IS10Press(r\Objects[U30_OUT_AD], 2.0) Then
		IS16Tell("Figure A: a non-anomalous recreation of an SCP-4434-A advertisement, the address blacked out. It is just paper. You still want to know where it is.", 7)
	EndIf
	If IS10Press(r\Objects[U30_OUT_SKULL], 2.0) Then
		IS16Tell("The skull of an SCP-4434-C: a deer's, with a wolf's teeth and too many tines. Twenty-five of them hunt the valley.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- SCP-2648
Function U30Store(e.Events)
	Local r.Rooms = e\room, it.Items, p% = r\Objects[U30_STR_AMAL], dx#, dz#
	If I30Amal <> 0 Then
		TurnEntity(I30Amal, 0, 0.06 * FPSfactor, 0)
		;anything left in the container is taken in, and it grows
		For it = Each Items
			If Not it\Picked Then
				dx = EntityX(it\collider, True) - EntityX(p, True) : dz = EntityZ(it\collider, True) - EntityZ(p, True)
				If dx * dx + dz * dz < 1.3 * 1.3 And Abs(EntityY(it\collider, True) - EntityY(p, True)) < 2.0 Then
					RemoveItem(it)
					I30AmalScale = Min(I30AmalScale * 1.03, 1.05)
					ScaleEntity(I30Amal, RoomScale * I30AmalScale, RoomScale * I30AmalScale, RoomScale * I30AmalScale)
					Indev30Uses = Indev30Uses + 1
					If PlayerRoom = r Then IS16Tell("SCP-2648 rolls over it. It's gone. The hum drops half a note; the mass is a little bigger.", 5)
					Exit
				EndIf
			EndIf
		Next
	EndIf
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U30_STR_GATE], 2.4) Then
		IS10Sound("SFX\Indev\uvhum.wav", r\Objects[U30_STR_GATE], 6.0, 0.6)
		IS16Tell("SCP-2648 hums, low, and leans towards the bars. Logs, bushes, pineapples, turf mesh, something red. It must not be fed anything.", 7)
	EndIf
	If IS10Press(r\Objects[U30_STR_LAMBDA], 2.4) Then
		IS16Tell("MTF Lambda-14's board: groundwater and soil readings, flagged. Mass gain +0.4 kg. LAST FEED: NONE - DO NOT FEED.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev30()
	Local k%, a#, ph%
	;SCP-4427: a minute and a half after the 45th contact, one of them changes
	If I4427Timer > 0 Then
		I4427Timer = I4427Timer - FPSfactor
		If I4427Timer <= 0 Then
			I4427Timer = 0
			If Rand(3) = 1 Then
				I4427Trait = 1 : I4427Heat = 70 * 20
				IS16Tell("Your palms are hot. The air above them shimmers. You were one of the forty-five - and the one it picked.", 8)
			Else
				IS16Tell("PA: 'Media Relations to the Entrance Zone. A visitor's coffee cup just boiled in her hand.' Not you. This time.", 7)
			EndIf
		EndIf
	EndIf
	If I4427Trait = 1 And KillTimer >= 0 Then
		I4427Heat = I4427Heat - FPSfactor
		If I4427Heat <= 0 Then
			I4427Heat = 70 * Rnd(35, 60)
			BlurTimer = Max(BlurTimer, 70 * 2)
			Injuries = Injuries + 0.05
			IS16Tell("A wave of heat rolls off your skin. The air shimmers; your sleeves smoke. (SCP-4427-A)", 4)
		EndIf
	EndIf
	;SCP-4433: the phone rings
	If U30Has("phone4433") <> Null And I4433Stage < 3 And I4433Pull <= 0 Then
		If I4433Ringing > 0 Then
			I4433Ringing = I4433Ringing - FPSfactor
			I4433RingSnd = I4433RingSnd - FPSfactor
			If I4433RingSnd <= 0 Then
				I4433RingSnd = 70 * 2.2
				IS10Sound("SFX\Indev\phonering.wav", Collider, 6.0, 0.9)
			EndIf
			If I4433Ringing <= 0 Then
				I4433Ring = 70 * Rnd(60, 150)
				IS16Tell("Missed call: RESTRICTED NUMBER.", 3)
			EndIf
		Else
			I4433Ring = I4433Ring - FPSfactor
			If I4433Ring <= 0 Then
				I4433Ringing = 70 * 9 : I4433RingSnd = 0
				IS16Tell("Your phone is ringing. RESTRICTED NUMBER. You feel you have to answer.", 4)
			EndIf
		EndIf
	EndIf
	If I4433Pull > 0 And KillTimer >= 0 Then
		I4433Pull = I4433Pull - FPSfactor
		Stamina = Min(Stamina, 35)
		IndevStress = Min(100, IndevStress + 0.01 * FPSfactor)
		If I4433Pull < 70 * 60 And I4433Pull + FPSfactor >= 70 * 60 Then IS16Tell("You could find the house with your eyes shut. Mom's waiting. (Hang up - use the phone.)", 6)
		If I4433Pull <= 0 Then
			I4433Pull = 0 : I4433Stage = 4
			LightFlash = 1.5 : BlurTimer = 70 * 10 : Stamina = 0 : Injuries = Injuries + 0.4
			IS16Tell("A warm kitchen, five people at the table, a place set for you... Agents shake you awake in a corridor. You had been talking to no one for an hour.", 9)
		EndIf
	EndIf
	;on thermal, while they are calling: five figures round you
	ph = I4427Thermal And (I4433Ringing > 0 Or I4433Pull > 0)
	For k = 0 To 4
		If ph And I30Ghost(k) = 0 Then
			I30Ghost(k) = CreateSphere(10)
			ScaleEntity(I30Ghost(k), 0.17, 0.85, 0.17)
			EntityColor(I30Ghost(k), 255, 90, 40)
			EntityFX(I30Ghost(k), 1)
			EntityAlpha(I30Ghost(k), 0.35)
		EndIf
		If I30Ghost(k) <> 0 Then
			If ph Then
				a = k * 72 + MilliSecs() * 0.004
				ShowEntity(I30Ghost(k))
				PositionEntity(I30Ghost(k), EntityX(Collider) + 2.2 * Cos(a), EntityY(Collider) + 0.3, EntityZ(Collider) + 2.2 * Sin(a))
			Else
				HideEntity(I30Ghost(k))
			EndIf
		EndIf
	Next
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse30(it.Items)
	Select it\itemtemplate\name
		Case "thermal4427"
			I4427Thermal = Not I4427Thermal
			If I4427Thermal Then
				IS16Tell("THERMAL ON. The world goes purple and orange. Warm things glow.", 3)
			Else
				IS16Tell("THERMAL OFF.", 2)
			EndIf
		Case "phone4433"
			If I4433Pull > 0 Then
				I4433Pull = 0 : I4433Stage = 2 : I4433Ring = 70 * 40
				IS16Tell("You hang up. Your hand shakes. They'll call again - they always call again.", 6)
			ElseIf I4433Ringing > 0 Then
				I4433Ringing = 0
				I4433Stage = I4433Stage + 1
				Indev30Uses = Indev30Uses + 1
				Select I4433Stage
					Case 1
						I4433Ring = 70 * Rnd(50, 90)
						IAxSay("Mom", "Honey, it's your mother. Your mother. We miss you. This country is so big and you're so far - your mother just wants you home.", 9)
					Case 2
						I4433Ring = 70 * Rnd(40, 70)
						IAxSay("Mom", "Jacob and Sam are here. Lindsay made dinner. Karen's on the porch. Your mother set a place. Mother. Country. Home.", 9)
					Default
						I4433Pull = 70 * 120
						IAxSay("Mom", "Come home.", 6)
				End Select
			Else
				IS16Tell("No signal. The call log: RESTRICTED NUMBER, RESTRICTED NUMBER, RESTRICTED NUMBER.", 4)
			EndIf
		Case "card2758"
			IS16Tell("ROOM G14 - CUSTOM IDENTIFICATION. Use it at the reader by G14's door.", 4)
		Case "jar3069"
			BlurTimer = Max(BlurTimer, 70)
			IS16Tell("SCP-3069 specimen 17. When you look at it, the lure brightens. Something taps the glass from the inside, twice.", 6)
	End Select
	SelectedItem = Null
End Function
