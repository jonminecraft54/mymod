;=====================================================================
; SCP: Containment Breach - Indev: the very old SCP-173 (GFX\npcs\173.3ds + 173tex.jpg) and the old SCP-106
; (GFX\npcs\106.b3d + oldman.jpg). Both are EXTRA NPCs of the normal types (NPCtype173 / NPCtypeOldMan), so they
; run the same AI as the new ones; Curr173 / Curr106 and their models are never touched.
;
; n\Model holds the old model path, so a save keeps the old look (Save.bb already reloads n\Model).
; The old 106 has 300 animation frames, the new one 494: the AI keeps counting in new-model frames (n\Frame)
; and IndevOldSCPsUpdate shows the matching point of the old animation.
;=====================================================================

Const OLD173_MODEL$ = "GFX\npcs\173.3ds"
Const OLD106_MODEL$ = "GFX\npcs\106.b3d"
Const OLD106_FRAMES# = 300.0, NEW106_FRAMES# = 494.0
Global IndevOld106Textured%, IndevOld173Move#

;swap a freshly created NPCtype173 to the old look
Function IndevMakeOld173(n.NPCs)
	If n\obj3 <> 0 Then FreeEntity(n\obj3) : n\obj3 = 0 ;party hat, sized for the new model
	FreeEntity(n\obj)
	n\obj = LoadMesh_Strict(OLD173_MODEL) ;one mesh (LoadAnimMesh gives an empty root for a .3ds)
	Local tex% = LoadTexture_Strict("GFX\npcs\173tex.jpg")
	If tex <> 0 Then EntityTexture(n\obj, tex) : FreeTexture(tex)
	Local h# = MeshHeight(n\obj)
	If h <= 0 Then h = 1
	;the same height as the new statue (its 0.35 scale on MeshDepth comes out about 3.23 x the ini scale)
	Local s# = GetModdedINIFloat("DATA\NPCs.ini", "SCP-173", "scale") * 3.23 / h
	ScaleEntity(n\obj, s, s, s)
	n\Model = OLD173_MODEL : n\ModelScaleX = s : n\ModelScaleY = s : n\ModelScaleZ = s
	n\NVName = "SCP-173 (old)"
End Function

Function IndevMakeOld106(n.NPCs)
	FreeEntity(n\obj)
	n\obj = LoadAnimMesh_Strict(OLD106_MODEL)
	IndevOld106Tex(n) : IndevOld106Textured = n\obj
	Local s# = GetModdedINIFloat("DATA\NPCs.ini", "SCP-106", "scale") / 2.2
	ScaleEntity(n\obj, s, s, s)
	n\Model = OLD106_MODEL : n\ModelScaleX = s : n\ModelScaleY = s : n\ModelScaleZ = s
	n\NVName = "SCP-106 (old)"
	n\Frame = 0
End Function

;the .b3d points at an old project folder for oldman.jpg - put the texture on every surface mesh ourselves
Function IndevOld106Tex(n.NPCs)
	Local tex% = LoadTexture_Strict("GFX\npcs\oldman.jpg")
	If tex = 0 Then Return
	IndevOldTexAll(n\obj, tex)
	FreeTexture(tex)
End Function

Function IndevOldTexAll(ent%, tex%)
	Local i%
	If EntityClass(ent) = "Mesh" Then
		If CountSurfaces(ent) > 0 Then EntityTexture(ent, tex)
	EndIf
	For i = 1 To CountChildren(ent)
		IndevOldTexAll(GetChild(ent, i), tex)
	Next
End Function

Function IndevSpawnOld173.NPCs(x#, y#, z#)
	Local n.NPCs = CreateNPC(NPCtype173, x, y, z)
	IndevMakeOld173(n)
	Return n
End Function

Function IndevSpawnOld106.NPCs(x#, y#, z#)
	Local n.NPCs = CreateNPC(NPCtypeOldMan, x, y, z)
	IndevMakeOld106(n)
	n\State = 70 * 60 * Rand(20, 30) ;comes out later than the new one
	Return n
End Function

;called from InitNewGame right after Curr173 / Curr106: the old statue waits in a Light Containment room,
;the old 106 is out in the facility like the new one
Function IndevOldPickRoom.Rooms(zone%, avoid.Rooms)
	Local r.Rooms, pick.Rooms, cnt%
	For r = Each Rooms
		If r <> avoid And (zone < 0 Or r\zone = zone) And r\RoomTemplate\Shape <> ROOM1 Then
			Select r\RoomTemplate\Name
				Case "start", "173", "room2scp173oldercell", "room2closets", "room2tesla_lcz", "room2tesla", "pocketdimension", "dimension1499", "gatea", "gateaentrance", "exit1", "room2nuke", "room2sl", "checkpoint1", "checkpoint2", "room860", "room2elevator"
				Default
					If EntityY(r\obj) > -5 And EntityY(r\obj) < 5 Then
						cnt = cnt + 1
						If Rand(cnt) = 1 Then pick = r
					EndIf
			End Select
		EndIf
	Next
	Return pick
End Function

;called from InitNewGame right after Curr173 / Curr106: the old statue waits in a room of the facility,
;the old 106 runs on SCP-106's own timer
Function IndevSpawnOldSCPs()
	Local r.Rooms, pick.Rooms = IndevOldPickRoom(0, Null)
	If pick <> Null Then
		IndevSpawnOld173(EntityX(pick\obj), EntityY(pick\obj) + 0.5, EntityZ(pick\obj))
	Else
		IndevSpawnOld173(0, -30.0, 0)
	EndIf
	IndevOld173Move = 70 * 60 * Rnd(2, 4)
	Local o106.NPCs = IndevSpawnOld106(0, -30.0, 0)
	If Curr106 <> Null Then o106\State = Curr106\State + 70 * 60 * Rand(1, 3) ;SCP-106's timer, a little after it
	If GetCLIInt("testold", 0) = 1 Then ;room test: both of them in the old SCP-689 room, in front of the camera
		For r = Each Rooms
			If r\RoomTemplate\Name = "room2offices2" Then
				TFormPoint(60, 60, 380, r\obj, 0) : IndevSpawnOld173(TFormedX(), TFormedY(), TFormedZ())
				TFormPoint(160, 20, 700, r\obj, 0) : Local n.NPCs = IndevSpawnOld106(TFormedX(), TFormedY(), TFormedZ())
				n\State = -10
				Exit
			EndIf
		Next
	EndIf
End Function

Function IndevIsOldNPC%(n.NPCs)
	If n = Null Then Return False
	Return (n\Model = OLD173_MODEL Or n\Model = OLD106_MODEL)
End Function

;every frame, after UpdateNPCs
Function IndevOldSCPsUpdate()
	Local n.NPCs, n2.NPCs
	;after loading a save the last 173 / 106 read becomes Curr173 / Curr106 - hand it back to the new one
	If IndevIsOldNPC(Curr173) Then
		For n2 = Each NPCs
			If n2\NPCtype = NPCtype173 And (Not IndevIsOldNPC(n2)) Then Curr173 = n2 : Exit
		Next
	EndIf
	If IndevIsOldNPC(Curr106) Then
		For n2 = Each NPCs
			If n2\NPCtype = NPCtypeOldMan And (Not IndevIsOldNPC(n2)) Then Curr106 = n2 : Exit
		Next
	EndIf
	;the old statue moves to another room of the player's zone now and then, while nobody sees it
	IndevOld173Move = IndevOld173Move - FPSfactor
	If IndevOld173Move <= 0 And PlayerRoom <> Null Then
		IndevOld173Move = 70 * 60 * Rnd(2, 4)
		For n = Each NPCs
			If n\NPCtype = NPCtype173 And n\Model = OLD173_MODEL Then
				If EntityDistance(n\Collider, Collider) > HideDistance And (Not EntityInView(n\obj, Camera)) Then
					Local mr.Rooms = IndevOldPickRoom(PlayerRoom\zone, PlayerRoom)
					If mr <> Null Then
						If EntityDistance(mr\obj, Collider) > 6.0 Then
							PositionEntity(n\Collider, EntityX(mr\obj), EntityY(mr\obj) + 0.5, EntityZ(mr\obj))
							ResetEntity(n\Collider)
						EndIf
					EndIf
				EndIf
			EndIf
		Next
	EndIf
	For n = Each NPCs
		If n\NPCtype = NPCtypeOldMan And n\Model = OLD106_MODEL Then
			If n\obj <> IndevOld106Textured Then IndevOld106Tex(n) : IndevOld106Textured = n\obj ;once (also after a load)
			SetAnimTime(n\obj, Min(n\Frame * OLD106_FRAMES / NEW106_FRAMES, OLD106_FRAMES))
		EndIf
	Next
End Function
