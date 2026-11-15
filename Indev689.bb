;=====================================================================
; SCP: Containment Breach - Indev: the old SCP-689 room (room1scp689old, GFX\map\statueroom.b3d - an old .b3d room
; with its own baked lightmap) and SCP-689, "the Haunter in the Dark", using the old statue.x model.
;
; SCP-689 (summary of scp-wiki.wikidot.com/scp-689 in our own words, CC BY-SA 3.0): a small soapstone statue of a
; seated skeletal figure. It never moves while anyone is watching it. The moment nobody is watching, everyone who
; has looked at it dies, and it is found again beside one of the bodies.
;
; Here: once you have looked at it, it must stay in view while you are in the room. Look away for too long (turn
; your back, blink in the dark) and it is beside you. Walk out through the door and the room camera takes over.
;=====================================================================

Global I689Seen%, I689Away#, I689Warn%

Function Indev689Reset(newGame%)
	I689Seen = False : I689Away = 0 : I689Warn = 0
End Function

;an old .b3d room mesh, built into the same shape LoadRMesh returns (pivot: [1] pivot, [2] the visible mesh,
;[3] the invisible collision mesh, [4] [5] pivots, [6] the collision-mesh holder), so the rest of the room code
;treats it like any .rmesh room. Called from LoadRoomMesh (MapSystem.bb).
Function IndevLoadB3DRoom%(file$)
	Local vis% = LoadMesh_Strict(file)
	If vis = 0 Then Return 0
	EntityFX(vis, 1)
	Local hidden% = CopyMesh(vis)
	EntityAlpha(hidden, 0.0)
	EntityType(hidden, HIT_MAP)
	EntityPickMode(hidden, 2)
	Local obj% = CreatePivot()
	CreatePivot(obj)
	EntityParent(vis, obj)
	EntityParent(hidden, obj)
	CreatePivot(obj)
	CreatePivot(obj)
	CreatePivot(obj)
	Return obj
End Function

;r\Objects[0] the statue, [1] its pedestal spot
Function IndevFill689(r.Rooms)
	Local o% = LoadMesh_Strict("GFX\npcs\statue.x")
	Local h# = MeshHeight(o)
	If h <= 0 Then h = 1
	ScaleEntity(o, 0.42 / h, 0.42 / h, 0.42 / h)
	EntityColor(o, 150, 190, 150) ;green soapstone
	r\Objects[1] = CreatePivot()
	PositionEntity(r\Objects[1], r\x + I689X * RoomScale, r\y + I689Y * RoomScale, r\z + I689Z * RoomScale, True)
	EntityParent(r\Objects[1], r\obj)
	PositionEntity(o, EntityX(r\Objects[1], True), EntityY(r\Objects[1], True), EntityZ(r\Objects[1], True), True)
	EntityParent(o, r\obj)
	r\Objects[0] = o
	CreateItem("doc25_689", r\x + 300 * RoomScale, r\y + 20 * RoomScale, r\z + 100 * RoomScale)
End Function

Const I689X# = 0.0, I689Y# = 144.0, I689Z# = 512.0 ;the top of the pedestal in statueroom.b3d

Function U689Watched%(o%)
	If LightBlink > 0 Then Return False
	If Not (BlinkTimer < -16 Or BlinkTimer > -6) Then Return False
	If Not EntityInView(o, Camera) Then Return False
	Return EntityVisible(o, Camera)
End Function

Function UpdateIndev689(e.Events)
	Local r.Rooms = e\room, o% = r\Objects[0]
	If o = 0 Then Return
	If PlayerRoom <> r Then
		I689Away = 0 : I689Warn = 0
		Return
	EndIf
	If U689Watched(o) Then
		If Not I689Seen Then
			I689Seen = True
			IS16Tell("A small green statue on the pedestal: a seated skeleton, hands clasped over its knees. You have the feeling you should not look away.", 7)
		EndIf
		I689Away = 0 : I689Warn = 0
		Return
	EndIf
	If Not I689Seen Then Return
	I689Away = I689Away + FPSfactor
	If I689Away > 70 * 3 And I689Warn = 0 Then
		I689Warn = 1
		IS16Tell("The back of your neck prickles. Where is the statue?", 4)
	ElseIf I689Away > 70 * 6 And I689Warn = 1 Then
		I689Warn = 2
		IndevStress = Min(100, IndevStress + 10)
		IS16Tell("LOOK AT IT.", 3)
	ElseIf I689Away > 70 * 9 And KillTimer >= 0 Then
		;it is beside you
		TFormPoint(0.35, 0, 0.25, Collider, 0)
		PositionEntity(o, TFormedX(), EntityY(Collider, True) - 0.3, TFormedZ(), True)
		DeathMSG = "Subject D-9341 was found dead in the old SCP-689 room with no visible injuries. SCP-689 was found beside the body, not on its pedestal. Camera coverage in the room had been interrupted for nine seconds."
		Kill()
	EndIf
End Function
