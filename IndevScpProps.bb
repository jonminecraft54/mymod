;=====================================================================
; SCP: Containment Breach - Indev: real models for the SCPs of the containment blocks
;
;   The cells of batches 20, 21, 24 and 25 used to show each SCP as a coloured box. The SCPs listed in
;   Tools\roomkit\scp_models.py now get one of the game's own meshes (made with the room, IndevScpMesh) or, when
;   the SCP is a person, a figure standing in the cell (made the first time you enter the room, IndevScpFigure).
;   The table is generated: IndevScpModels.bb.
;=====================================================================

;the mesh of SCP n in the cell whose pivot is p: loaded, scaled to its height, stood on the floor (or its
;stand) and turned to face the cell door. Returns the mesh, or 0 when n has none.
Function IndevScpMesh%(r.Rooms, p%, n$)
	Local f$ = IndevScpMeshFile(n), dims$, h#, by#, xo#, m%, lx#, lz#, s#, k#, miny#, maxy#, sf%, v%, y#, i%, srf%, minx#, maxx#, minz#, maxz#, big#
	If f = "" Then Return 0
	If FileType(f) <> 1 Then Return 0
	dims = IndevScpMeshDims(n)
	i = Instr(dims, "|")
	h = Float(Left(dims, i - 1))
	dims = Mid(dims, i + 1)
	i = Instr(dims, "|")
	by = Float(Left(dims, i - 1))
	xo = Float(Mid(dims, i + 1))
	m = LoadMesh_Strict(f)
	If m = 0 Then Return 0
	;the SCP-993 television is textured by code in the game, not in its file: give it its switched-off screen
	If Instr(f, "tv993") > 0 And FileType("GFX\map\props\tv993_off.png") = 1 Then
		Local tvtex% = LoadTexture_Strict("GFX\map\props\tv993_off.png")
		EntityTexture(m, tvtex)
		FreeTexture(tvtex)
	EndIf
	;its size and lowest point, in its own units: the longest side is fitted to h, so flat things stay small
	miny = 99999 : maxy = -99999 : minx = 99999 : maxx = -99999 : minz = 99999 : maxz = -99999
	For sf = 1 To CountSurfaces(m)
		srf = GetSurface(m, sf)
		For v = 0 To CountVertices(srf) - 1
			y = VertexY(srf, v)
			If y < miny Then miny = y
			If y > maxy Then maxy = y
			If VertexX(srf, v) < minx Then minx = VertexX(srf, v)
			If VertexX(srf, v) > maxx Then maxx = VertexX(srf, v)
			If VertexZ(srf, v) < minz Then minz = VertexZ(srf, v)
			If VertexZ(srf, v) > maxz Then maxz = VertexZ(srf, v)
		Next
	Next
	big = Max(maxy - miny, Max(maxx - minx, maxz - minz))
	If big < 0.0001 Then big = 1
	k = h * RoomScale / big
	ScaleEntity(m, k, k, k)
	;where the pivot is, in room units; the far wall is the way the pivot's x points
	TFormPoint(EntityX(p, True), EntityY(p, True), EntityZ(p, True), 0, r\obj)
	lx = TFormedX() : lz = TFormedZ()
	s = Sgn(lx)
	If s = 0 Then s = 1
	TFormPoint(lx + s * xo, by, lz, r\obj, 0)
	PositionEntity(m, TFormedX(), TFormedY() - miny * k, TFormedZ(), True)
	RotateEntity(m, 0, EntityYaw(r\obj, True) + 90 * s, 0, True)
	EntityParent(m, r\obj, True)
	;collision only for simple models: a dense one (the SCP-983 monkey) would cost every frame for nothing
	Local tris% = 0
	For sf = 1 To CountSurfaces(m)
		tris = tris + CountTriangles(GetSurface(m, sf))
	Next
	If tris < 1500 Then EntityType(m, HIT_MAP)
	Return m
End Function

;the figure of SCP n (a person) standing at pivot p, facing the door; Null when n is not a figure
Function IndevScpFigure.NPCs(r.Rooms, p%, n$)
	Local skin$ = IndevScpNPCSkin(n), nn.NPCs, lx#, s#
	If skin = "" Then Return Null
	TFormPoint(EntityX(p, True), EntityY(p, True), EntityZ(p, True), 0, r\obj)
	lx = TFormedX()
	s = Sgn(lx)
	If s = 0 Then s = 1
	nn = CreateNPC(NPCtypeD, EntityX(p, True), EntityY(r\obj, True) + 0.5, EntityZ(p, True))
	nn\State = 0
	RotateEntity(nn\Collider, 0, EntityYaw(r\obj, True) + 90 * s, 0)
	If FileType(skin) = 1 Then IAxSkin(nn, skin)
	Return nn
End Function

;made with the room: a mesh for each SCP of a block that has one ("a|b|c|...", slot k = k-th SCP)
Function IndevScpDressList(r.Rooms, list$)
	Local k%, s%, n$
	s = 0
	While list <> ""
		k = Instr(list, "|")
		If k = 0 Then
			n = list : list = ""
		Else
			n = Left(list, k - 1) : list = Mid(list, k + 1)
		EndIf
		If r\Objects[s] <> 0 Then IndevScpMesh(r, r\Objects[s], n)
		s = s + 1
	Wend
End Function

;on first entry: the figures of a block (flag "F" in the event). They use NPC slots from 4 up, so the
;earlier batches' own NPCs (slots 0-2) are left alone.
Function IndevScpFiguresList(e.Events, list$)
	Local k%, s%, n$, r.Rooms = e\room, slot% = 4, nn.NPCs
	If IAxFlag(e, "F") Then Return
	IAxSetFlag(e, "F")
	s = 0
	While list <> ""
		k = Instr(list, "|")
		If k = 0 Then
			n = list : list = ""
		Else
			n = Left(list, k - 1) : list = Mid(list, k + 1)
		EndIf
		If r\Objects[s] <> 0 And slot <= 11 Then
			nn = IndevScpFigure(r, r\Objects[s], n)
			If nn <> Null Then
				r\NPC[slot] = nn
				slot = slot + 1
			EndIf
		EndIf
		s = s + 1
	Wend
End Function
