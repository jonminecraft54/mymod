;=====================================================================
; SCP: Containment Breach - Indev batch 49: SCP-087-B.
;
; room2scp087b (Tools\roomkit\rooms_b49.py) is the way in: an old brick room with a stairwell going down. Past the
; bottom step you are in SCP-087-B: narrow brick hallways and staircases, made one floor at a time as you go down,
; different every time, with no bottom. Only three floors exist at once (the one you are on, the one above, the one
; below) and short black fog does the rest, so it costs next to nothing however deep you go.
;
; Something lives down there. From the third floor it stands at the far end of hallways and is gone when you get
; close; you hear it walking a floor behind you; from the tenth floor it stops waiting - it comes after you whenever
; you are not looking at it, a little faster every floor. The only way is deeper. Now and then (every fifteenth
; floor) a door stands at the end of a dead end that should not be there: it leads back out.
;
; Built far outside the map (x, z = -300) so no room claims it; PlayerRoom stays the entrance room.
;=====================================================================

Const B87C# = 1.25        ;hallway cell size (world units)
Const B87WH# = 1.45       ;wall height
Const B87FH# = 1.7        ;drop per staircase
Const B87BX# = -300.0, B87BY# = -60.0, B87BZ# = -300.0
Const B87MAXC% = 40

Type B87Floor
	Field idx%
	Field mesh%, steps%, ramp%, cap%, door%
	Field y#
	Field n%                          ;path cells (0 = arrival)
	Field cx#[B87MAXC], cz#[B87MAXC]
	Field sx#, sz#                    ;the top of its staircase
	Field ax#, az#                    ;where you arrive
	Field dir%
	Field nx#, nz#                    ;where the next floor starts
	Field ex#, ez#, hasExit%
End Type

Global B87In%, B87Cur%, B87Deepest%
Global B87Lurk%, B87LurkState%, B87LurkSeen#, B87LurkTimer#, B87Steps#
Global B87Tex%[4]                     ;0 brick, 1 concrete, 2 numbers, 3 door
Global B87Fog# = 6.0
Global B87TestPlaced%
Global B87FN%                       ;cells the floor being built must keep clear (B87FX / B87FZ)
Dim B87FX#(1), B87FZ#(1)

Function Indev49Reset(newGame%)
	;everything down there is freed with the world - just forget it
	Delete Each B87Floor
	B87In = False : B87Cur = 0
	B87Lurk = 0 : B87LurkState = 0 : B87LurkSeen = 0 : B87LurkTimer = 0 : B87Steps = 0
	Local i%
	For i = 0 To 3
		B87Tex[i] = 0
	Next
End Function

Function IndevU49Dress(r.Rooms)
End Function

Function B87LoadTex()
	If B87Tex[0] <> 0 Then Return
	B87Tex[0] = LoadTexture_Strict("GFX\map\indev_087bbrick.png", 1)
	B87Tex[1] = LoadTexture_Strict("GFX\map\concretefloor.jpg", 1)
	B87Tex[2] = LoadTexture_Strict("GFX\map\indev_087bnum.png", 1)
	B87Tex[3] = LoadTexture_Strict("GFX\map\door.jpg", 1)
End Function

Function B87DX%(d%)
	Select d Mod 4
		Case 0 Return 1
		Case 2 Return -1
	End Select
	Return 0
End Function

Function B87DZ%(d%)
	Select d Mod 4
		Case 1 Return 1
		Case 3 Return -1
	End Select
	Return 0
End Function

;a quad, corners in order, uv over (u0,v0)-(u1,v1), a little grime in the vertex colour
Function B87Quad(s%, x0#, y0#, z0#, x1#, y1#, z1#, x2#, y2#, z2#, x3#, y3#, z3#, u0#, v0#, u1#, v1#)
	Local c% = Rand(135, 195), c2% = Rand(135, 195)
	Local a% = AddVertex(s, x0, y0, z0, u0, v1)
	Local b% = AddVertex(s, x1, y1, z1, u1, v1)
	Local cc% = AddVertex(s, x2, y2, z2, u1, v0)
	Local d% = AddVertex(s, x3, y3, z3, u0, v0)
	VertexColor(s, a, c, c, c) : VertexColor(s, b, c2, c2, c2)
	VertexColor(s, cc, c2, c2, c2) : VertexColor(s, d, c, c, c)
	AddTriangle(s, a, cc, b)
	AddTriangle(s, a, d, cc)
	;double-sided: the walls are seen from inside only, but this keeps the collision honest from both sides
	AddTriangle(s, a, b, cc)
	AddTriangle(s, a, cc, d)
End Function

;the wall on side `side` of the cell centred at (x, z), floor y0 / top y1 at the near end and y2 / y3 at the far
;(sloped walls on the stairs: along = the run direction, h0 at the start of the run, h1 at its end)
Function B87Wall(s%, x#, z#, side%, yb0#, yt0#, yb1#, yt1#, runDir%)
	Local h# = B87C / 2.0
	Local ax#, az#, bx#, bz#
	Select side Mod 4
		Case 0 : ax = x + h : az = z - h : bx = x + h : bz = z + h
		Case 1 : ax = x + h : az = z + h : bx = x - h : bz = z + h
		Case 2 : ax = x - h : az = z + h : bx = x - h : bz = z - h
		Default : ax = x - h : az = z - h : bx = x + h : bz = z - h
	End Select
	;which end of the wall is nearer the start of the run (for the sloped stairwell walls)
	Local ya0# = yb0, ya1# = yt0, yb0b# = yb1, yb1b# = yt1
	If runDir >= 0 Then
		Local pa# = ax * B87DX(runDir) + az * B87DZ(runDir), pb# = bx * B87DX(runDir) + bz * B87DZ(runDir)
		If pa > pb Then
			ya0 = yb1 : ya1 = yt1 : yb0b = yb0 : yb1b = yt0
		EndIf
	EndIf
	B87Quad(s, ax, ya0, az, bx, yb0b, bz, bx, yb1b, bz, ax, ya1, az, 0, 0, B87C, B87WH)
End Function

Function B87Has%(f.B87Floor, x#, z#)
	Local i%
	;the two cells under the staircase of the floor above are off limits: anything built there would have its
	;ceiling inside that staircase, and you'd walk down onto it instead of down the steps
	For i = 0 To B87FN - 1
		If Abs(B87FX(i) - x) < 0.01 And Abs(B87FZ(i) - z) < 0.01 Then Return True
	Next
	For i = 0 To f\n - 1
		If Abs(f\cx[i] - x) < 0.01 And Abs(f\cz[i] - z) < 0.01 Then Return True
	Next
	Return False
End Function

;build floor idx: you arrive at (ox, oz) at height oy, walking in direction dir
Function B87Build.B87Floor(idx%, ox#, oy#, oz#, dir%)
	B87LoadTex()
	B87FN = 0
	Local up.B87Floor = B87Get(idx - 1)
	If up <> Null Then
		B87FX(0) = up\sx : B87FZ(0) = up\sz
		B87FX(1) = up\sx + B87DX(up\dir) * B87C : B87FZ(1) = up\sz + B87DZ(up\dir) * B87C
		B87FN = 2
	EndIf
	Local f.B87Floor = New B87Floor
	f\idx = idx : f\y = oy : f\ax = ox : f\az = oz
	Local x# = ox, z# = oz, d% = dir, i%, k%, tries%, nd%
	;connections: link[i] = the side of cell i that opens to the cell before it (-1 for none)
	Local prevSide%[B87MAXC], branchOf%[B87MAXC]
	f\cx[0] = x : f\cz[0] = z : f\n = 1
	prevSide[0] = (dir + 2) Mod 4 : branchOf[0] = -1
	Local want% = Rand(5, 9) + Min(idx / 3, 6)
	;the main path: mostly straight, sometimes a turn, never into itself; keeps room for the stairs at the end
	For i = 1 To want
		tries = 0
		Repeat
			Local roll% = Rand(10)
			If roll <= 6 Then
				nd = d
			ElseIf roll <= 8 Then
				nd = (d + 1) Mod 4
			Else
				nd = (d + 3) Mod 4
			EndIf
			tries = tries + 1
		Until (Not B87Has(f, x + B87DX(nd) * B87C, z + B87DZ(nd) * B87C)) Or tries > 12
		If tries > 12 Then Exit
		d = nd
		x = x + B87DX(d) * B87C : z = z + B87DZ(d) * B87C
		f\cx[f\n] = x : f\cz[f\n] = z : prevSide[f\n] = (d + 2) Mod 4 : branchOf[f\n] = -1
		f\n = f\n + 1
	Next
	;the staircase must run two clear cells straight on - turn if it can't, drop path cells if it must
	Local ok% = False
	While Not ok
		For k = 0 To 3
			nd = (d + k) Mod 4
			If k = 2 Then nd = (d + 3) Mod 4
			If k = 3 Then nd = (d + 2) Mod 4
			If (Not B87Has(f, x + B87DX(nd) * B87C, z + B87DZ(nd) * B87C)) And (Not B87Has(f, x + B87DX(nd) * B87C * 2, z + B87DZ(nd) * B87C * 2)) And (Not B87Has(f, x + B87DX(nd) * B87C * 3, z + B87DZ(nd) * B87C * 3)) Then
				If nd <> (prevSide[f\n - 1]) Then
					ok = True : d = nd : Exit
				EndIf
			EndIf
		Next
		If Not ok Then
			If f\n <= 1 Then
				ok = True ;(cannot happen on an empty grid)
			Else
				f\n = f\n - 1
				x = f\cx[f\n - 1] : z = f\cz[f\n - 1]
				d = (prevSide[f\n] + 2) Mod 4
			EndIf
		EndIf
	Wend
	Local lastMain% = f\n - 1
	Local outSide% = d
	;dead-end branches off the main path (and on every fifteenth floor, the door out at the end of one)
	Local branches% = Rand(0, 2) + (idx > 4), b%, blen%, bx#, bz#, bd%
	If idx Mod 15 = 14 Then branches = Max(branches, 1)
	For b = 1 To branches
		Local from% = Rand(1, Max(1, lastMain - 1))
		bd = (Rand(0, 1) * 2 + 1 + d) Mod 4
		bx = f\cx[from] : bz = f\cz[from]
		blen = Rand(1, 2)
		Local made% = 0
		For k = 1 To blen
			Local tx# = bx + B87DX(bd) * B87C, tz# = bz + B87DZ(bd) * B87C
			If B87Has(f, tx, tz) Or (f\n >= B87MAXC - 1) Then Exit
			;keep the stair run clear
			If Abs(tx - (x + B87DX(outSide) * B87C)) < 0.01 And Abs(tz - (z + B87DZ(outSide) * B87C)) < 0.01 Then Exit
			If Abs(tx - (x + B87DX(outSide) * B87C * 2)) < 0.01 And Abs(tz - (z + B87DZ(outSide) * B87C * 2)) < 0.01 Then Exit
			f\cx[f\n] = tx : f\cz[f\n] = tz : prevSide[f\n] = (bd + 2) Mod 4 : branchOf[f\n] = 1
			f\n = f\n + 1 : bx = tx : bz = tz : made = made + 1
		Next
		If made > 0 And (idx Mod 15 = 14) And (Not f\hasExit) Then
			f\hasExit = True : f\ex = bx : f\ez = bz
			f\door = bd ;(the side the door is on)
		EndIf
	Next
	;---------------------------------------------------------------- the mesh
	Local m% = CreateMesh()
	Local sw% = CreateSurface(m), sf% = CreateSurface(m)
	Local br% = CreateBrush() : BrushTexture(br, B87Tex[0]) : PaintSurface(sw, br) : FreeBrush(br)
	br = CreateBrush() : BrushTexture(br, B87Tex[1]) : PaintSurface(sf, br) : FreeBrush(br)
	Local wallMask%[B87MAXC]
	Local h# = B87C / 2.0, y# = oy, side%, open%, j%
	For i = 0 To f\n - 1
		x = f\cx[i] : z = f\cz[i]
		B87Quad(sf, x - h, y, z - h, x + h, y, z - h, x + h, y, z + h, x - h, y, z + h, 0, 0, B87C, B87C)
		B87Quad(sf, x - h, y + B87WH, z + h, x + h, y + B87WH, z + h, x + h, y + B87WH, z - h, x - h, y + B87WH, z - h, 0, 0, B87C, B87C)
		For side = 0 To 3
			open = (prevSide[i] = side)
			If i = 0 And idx = 0 And side = prevSide[0] Then open = False ;the first floor: the way back is a wall
			If i = lastMain And side = outSide Then open = True
			;a cell is also open towards any later cell that came from it
			For j = i + 1 To f\n - 1
				If Abs(f\cx[j] + B87DX(prevSide[j]) * B87C - x) < 0.01 And Abs(f\cz[j] + B87DZ(prevSide[j]) * B87C - z) < 0.01 Then
					If B87DX(side) = -B87DX(prevSide[j]) And B87DZ(side) = -B87DZ(prevSide[j]) Then open = True
				EndIf
			Next
			If Not open Then B87Wall(sw, x, z, side, y, y + B87WH, y, y + B87WH, -1) : wallMask[i] = wallMask[i] Or (1 Shl side)
		Next
	Next
	;the staircase: two cells, floor and ceiling sloping down by one drop
	x = f\cx[lastMain] : z = f\cz[lastMain]
	Local s1x# = x + B87DX(outSide) * B87C, s1z# = z + B87DZ(outSide) * B87C
	Local s2x# = s1x + B87DX(outSide) * B87C, s2z# = s1z + B87DZ(outSide) * B87C
	f\sx = s1x : f\sz = s1z : f\dir = outSide
	f\nx = s2x + B87DX(outSide) * B87C : f\nz = s2z + B87DZ(outSide) * B87C
	Local yA# = y, yM# = y - B87FH / 2.0, yB# = y - B87FH
	For k = 0 To 1
		Local cxs#, czs#, y0#, y1#
		If k = 0 Then
			cxs = s1x : czs = s1z : y0 = yA : y1 = yM
		Else
			cxs = s2x : czs = s2z : y0 = yM : y1 = yB
		EndIf
		B87Wall(sw, cxs, czs, outSide + 1, y0, y0 + B87WH, y1, y1 + B87WH, outSide)
		B87Wall(sw, cxs, czs, outSide + 3, y0, y0 + B87WH, y1, y1 + B87WH, outSide)
	Next
	;the sloped ceiling over the whole run
	Local px# = B87DZ(outSide) * h, pz# = B87DX(outSide) * h   ;perpendicular half-width
	Local rsx# = x + B87DX(outSide) * h, rsz# = z + B87DZ(outSide) * h          ;start of the run
	Local rex# = s2x + B87DX(outSide) * h, rez# = s2z + B87DZ(outSide) * h      ;end of the run
	B87Quad(sf, rsx + px, yA + B87WH, rsz + pz, rsx - px, yA + B87WH, rsz - pz, rex - px, yB + B87WH, rez - pz, rex + px, yB + B87WH, rez + pz, 0, 0, B87C, B87C * 2)
	EntityFX(m, 1 + 2)
	EntityType(m, HIT_MAP)
	EntityPickMode(m, 2)
	f\mesh = m
	;the steps you see (no collision) and the ramp you walk on (invisible)
	Local st% = CreateMesh(), ss% = CreateSurface(st)
	br = CreateBrush() : BrushTexture(br, B87Tex[1]) : PaintSurface(ss, br) : FreeBrush(br)
	Local nSteps% = 10, sl# = (B87C * 2) / nSteps, sh# = B87FH / nSteps
	For k = 0 To nSteps - 1
		Local t0x# = rsx + B87DX(outSide) * sl * k, t0z# = rsz + B87DZ(outSide) * sl * k
		Local t1x# = t0x + B87DX(outSide) * sl, t1z# = t0z + B87DZ(outSide) * sl
		Local ty# = yA - sh * (k + 1)
		B87Quad(ss, t0x - px, ty, t0z - pz, t1x - px, ty, t1z - pz, t1x + px, ty, t1z + pz, t0x + px, ty, t0z + pz, 0, 0, sl, B87C)
		B87Quad(ss, t0x - px, ty, t0z - pz, t0x + px, ty, t0z + pz, t0x + px, ty + sh, t0z + pz, t0x - px, ty + sh, t0z - pz, 0, 0, B87C, sh)
	Next
	EntityFX(st, 1 + 2)
	f\steps = st
	Local rp% = CreateMesh(), rs% = CreateSurface(rp)
	;through the middle of every tread, so you walk on the steps instead of floating over their edges
	B87Quad(rs, rsx - px, yA - sh / 2, rsz - pz, rex - px, yB - sh / 2, rez - pz, rex + px, yB - sh / 2, rez + pz, rsx + px, yA - sh / 2, rsz + pz, 0, 0, 1, 1)
	EntityAlpha(rp, 0)
	EntityType(rp, HIT_MAP)
	f\ramp = rp
	;the number plate: on some wall of the floor
	Local pl% = CreateMesh(), ps% = CreateSurface(pl)
	br = CreateBrush() : BrushTexture(br, B87Tex[2]) : PaintSurface(ps, br) : FreeBrush(br)
	;a cell that really has a wall (never a plate hanging in a doorway)
	Local pc% = Rand(0, lastMain), num% = idx Mod 16, tryc%
	For tryc = 1 To 20
		If wallMask[pc] <> 0 Then Exit
		pc = Rand(0, f\n - 1)
	Next
	Local u0# = (num Mod 4) * 0.25, v0# = (num / 4) * 0.25
	x = f\cx[pc] : z = f\cz[pc]
	For side = 0 To 3
		;a closed side: use the first one that isn't the way on
		If wallMask[pc] And (1 Shl side) Then
			Local ins# = h - 0.02, ps2# = 0.16
			Local wx# = x + B87DX(side) * ins, wz# = z + B87DZ(side) * ins
			Local qx# = B87DZ(side) * ps2, qz# = B87DX(side) * ps2
			Local ua# = u0, ub# = u0 + 0.25
			If side = 0 Or side = 3 Then ua = u0 + 0.25 : ub = u0 ;(so the number reads the right way round on every wall)
			B87QuadUV(ps, wx - qx, y + 0.8, wz - qz, wx + qx, y + 0.8, wz + qz, wx + qx, y + 1.12, wz + qz, wx - qx, y + 1.12, wz - qz, ua, v0, ub, v0 + 0.25)
			Exit
		EndIf
	Next
	EntityFX(pl, 1 + 16)
	EntityParent(pl, m)
	;the cap that closes the way back up once the floor above is gone
	Local cp% = CreateMesh(), cs% = CreateSurface(cp)
	br = CreateBrush() : BrushTexture(br, B87Tex[0]) : PaintSurface(cs, br) : FreeBrush(br)
	B87Wall(cs, f\cx[0], f\cz[0], prevSide[0], y, y + B87WH, y, y + B87WH, -1)
	EntityFX(cp, 1 + 2)
	EntityType(cp, HIT_MAP)
	HideEntity(cp)
	f\cap = cp
	;the door out
	If f\hasExit Then
		Local dm% = CreateMesh(), ds% = CreateSurface(dm)
		br = CreateBrush() : BrushTexture(br, B87Tex[3]) : PaintSurface(ds, br) : FreeBrush(br)
		Local dwx# = f\ex + B87DX(f\door) * (h - 0.03), dwz# = f\ez + B87DZ(f\door) * (h - 0.03)
		Local dqx# = B87DZ(f\door) * 0.42, dqz# = B87DX(f\door) * 0.42
		B87QuadUV(ds, dwx - dqx, y, dwz - dqz, dwx + dqx, y, dwz + dqz, dwx + dqx, y + 1.3, dwz + dqz, dwx - dqx, y + 1.3, dwz - dqz, 0, 0, 1, 1)
		EntityFX(dm, 1)
		EntityParent(dm, m)
	EndIf
	Return f
End Function

;a one-sided textured quad with explicit uv (plates, the door)
Function B87QuadUV(s%, x0#, y0#, z0#, x1#, y1#, z1#, x2#, y2#, z2#, x3#, y3#, z3#, u0#, v0#, u1#, v1#)
	Local a% = AddVertex(s, x0, y0, z0, u0, v1)
	Local b% = AddVertex(s, x1, y1, z1, u1, v1)
	Local c% = AddVertex(s, x2, y2, z2, u1, v0)
	Local d% = AddVertex(s, x3, y3, z3, u0, v0)
	AddTriangle(s, a, c, b) : AddTriangle(s, a, d, c)
	AddTriangle(s, a, b, c) : AddTriangle(s, a, c, d)
End Function

Function B87Free(f.B87Floor)
	If f\mesh <> 0 Then FreeEntity(f\mesh)
	If f\steps <> 0 Then FreeEntity(f\steps)
	If f\ramp <> 0 Then FreeEntity(f\ramp)
	If f\cap <> 0 Then FreeEntity(f\cap)
	Delete f
End Function

Function B87Get.B87Floor(idx%)
	Local f.B87Floor
	For f = Each B87Floor
		If f\idx = idx Then Return f
	Next
	Return Null
End Function

;down the stairs in the entrance room: build the first two floors and put the player at the top
Function B87Enter()
	Local f.B87Floor
	For f = Each B87Floor
		B87Free(f)
	Next
	B87In = True : B87Cur = 0 : B87LurkState = 0 : B87LurkTimer = 0
	SeedRnd MilliSecs()
	f = B87Build(0, B87BX, B87BY, B87BZ, 0)
	B87Build(1, f\nx, f\y - B87FH, f\nz, f\dir)
	PositionEntity(Collider, f\ax, f\y + 0.45, f\az, True)
	ResetEntity(Collider)
	RotateEntity(Collider, 0, -90, 0, True)
	If B87Lurk = 0 Then
		Local t% = LoadTexture_Strict("GFX\map\indev_087blurk.png", 1 + 2)
		B87Lurk = CreateSprite()
		EntityTexture(B87Lurk, t)
		FreeTexture(t)
		SpriteViewMode(B87Lurk, 3)
		ScaleSprite(B87Lurk, 0.32, 0.64)
		EntityFX(B87Lurk, 1)
		HideEntity(B87Lurk)
	EndIf
	HideEntity(B87Lurk)
	IS16Tell("The stairs go down further than they should. Behind you there is only brick.", 5)
End Function

;out through the door that shouldn't be there
Function B87Leave(r.Rooms)
	Local f.B87Floor
	For f = Each B87Floor
		B87Free(f)
	Next
	B87In = False
	If B87Lurk <> 0 Then HideEntity(B87Lurk)
	If r <> Null Then
		PositionEntity(Collider, EntityX(r\obj, True), EntityY(r\obj, True) + 0.5, EntityZ(r\obj, True), True)
		ResetEntity(Collider)
	EndIf
	IS16Tell("You push the door open and stumble out into a room you know. You went down " + B87Cur + " floors. Your deepest: " + B87Deepest + ".", 8)
End Function

Function B87EntranceRoom.Rooms()
	Local r.Rooms
	For r = Each Rooms
		If r\RoomTemplate\Name = "room2scp087b" Then Return r
	Next
	Return Null
End Function

;the entrance room's event: walk down to the bottom step
Function UpdateIndevU49(e.Events)
	Local r.Rooms = e\room
	If B87In Or PlayerRoom <> r Then Return
	If e\EventState = 0 Then
		e\EventState = 1
		IS16Tell("An old brick room. In the east wall a narrow opening, and stairs going down into the dark.", 5)
	EndIf
	If U37LX(r) > 760 And U37LY(r) < -150 Then B87Enter()
End Function

;every frame (Main.bb, after IndevOutdoorFrame): the fog, the floors, the thing below
Function IndevB87Frame()
	If Not B87In Then
		;loaded a save made down there: the stairwell has rearranged itself - start again at the top of it
		If EntityX(Collider, True) < -150 And EntityZ(Collider, True) < -150 And EntityY(Collider, True) < -30 Then B87Enter()
		Return
	EndIf
	;darkness: whatever you can see, you see by your own eyes
	B87Fog = Max(4.5, 8.0 - B87Cur * 0.05)
	CameraFogRange(Camera, 1.0, B87Fog)
	CameraFogColor(Camera, 0, 0, 0)
	CameraFogMode(Camera, 1)
	CameraRange(Camera, 0.05, B87Fog * 1.4)
	CameraClsColor(Camera, 0, 0, 0)
	Local f.B87Floor = B87Get(B87Cur), nf.B87Floor
	If f = Null Then
		B87Enter()
		Return
	EndIf
	Local py# = EntityY(Collider, True)
	;room test: walk straight down to floor -testdeep, then look along the hall
	If IndevTestOn And B87Cur < GetCLIInt("testdeep", 0) Then
		PositionEntity(Collider, f\nx, f\y - B87FH + 0.45, f\nz, True)
		ResetEntity(Collider)
		py = f\y - B87FH
	EndIf
	If IndevTestOn And B87Cur = GetCLIInt("testdeep", 0) And GetCLIInt("teststair", 0) = 1 Then
		;stand halfway down this floor's staircase and look down it
		If B87TestPlaced = 0 Then : B87TestPlaced = 1
			PositionEntity(Collider, f\sx - B87DX(f\dir) * 0.3, f\y + 0.05, f\sz - B87DZ(f\dir) * 0.3, True)
			ResetEntity(Collider)
		EndIf
		IndevTestYaw = VectorYaw(B87DX(f\dir), 0, B87DZ(f\dir)) : IndevTestPitch = 12
		If IndevTestFrameN Mod 60 = 30 Then IndevTestLog("B87STAIR feet=" + (EntityY(Collider, True) - f\y))
		Return
	EndIf
	If IndevTestOn And GetCLIInt("testdeep", 0) > 0 And f\n > 1 Then
		IndevTestYaw = VectorYaw(f\cx[1] - f\cx[0], 0, f\cz[1] - f\cz[0]) : IndevTestPitch = 5
	EndIf
	;down a floor
	If py < f\y - B87FH * 0.75 Then
		B87Cur = B87Cur + 1
		If B87Cur > B87Deepest Then B87Deepest = B87Cur
		nf = B87Get(B87Cur)
		If nf = Null Then nf = B87Build(B87Cur, f\nx, f\y - B87FH, f\nz, f\dir)
		If B87Get(B87Cur + 1) = Null Then B87Build(B87Cur + 1, nf\nx, nf\y - B87FH, nf\nz, nf\dir)
		;two floors up is gone: free it, and wall off the stairs that led to it
		Local old.B87Floor = B87Get(B87Cur - 2)
		If old <> Null Then B87Free(old)
		Local above.B87Floor = B87Get(B87Cur - 1)
		If above <> Null Then ShowEntity(above\cap)
		B87NewFloor(nf)
		Return
	EndIf
	;back up a floor (as far as the floor above goes)
	If py > f\y + 0.6 And B87Cur > 0 And B87Get(B87Cur - 1) <> Null Then
		B87Cur = B87Cur - 1
		Return
	EndIf
	;fell through somewhere: back to where this floor starts
	If py < f\y - B87FH * 2.5 Then
		PositionEntity(Collider, f\ax, f\y + 0.45, f\az, True)
		ResetEntity(Collider)
	EndIf
	;the door out
	If f\hasExit Then
		If Abs(EntityX(Collider, True) - f\ex) < 0.45 And Abs(EntityZ(Collider, True) - f\ez) < 0.45 Then
			B87Leave(B87EntranceRoom())
			Return
		EndIf
	EndIf
	B87UpdateLurker(f)
End Function

;each new floor: the plate, the odd sound, and maybe the figure at the end of the hall
Function B87NewFloor(f.B87Floor)
	If f\idx Mod 5 = 0 Then IS16Tell("The plate on the wall says " + ((f\idx Mod 16) + 1) + ". You have stopped counting the stairs.", 4)
	If f\hasExit Then IS16Tell("Somewhere on this floor there's a draught. Fresh air, from a dead end.", 5)
	If B87LurkState = 2 Then Return ;it is already coming
	HideEntity(B87Lurk) : B87LurkState = 0
	If f\idx >= 10 And Rand(100) <= Min(30 + f\idx * 3, 85) Then
		;it follows you down
		B87LurkState = 2 : B87LurkTimer = 70 * Rnd(4, 9)
		Return
	EndIf
	If f\idx >= 2 And Rand(100) <= Min(25 + f\idx * 5, 80) Then
		;it waits at the far end
		Local c% = f\n - 1
		PositionEntity(B87Lurk, f\cx[c], f\y + 0.66, f\cz[c], True)
		ShowEntity(B87Lurk)
		B87LurkState = 1 : B87LurkSeen = 0
	EndIf
End Function

Function B87Seen%()
	If Not (BlinkTimer < -16 Or BlinkTimer > -6) Then Return False
	If Not EntityInView(B87Lurk, Camera) Then Return False
	Return EntityDistance(B87Lurk, Camera) < B87Fog * 1.2
End Function

Function B87UpdateLurker(f.B87Floor)
	Local d#
	;footsteps a floor behind you
	B87Steps = B87Steps - FPSfactor
	If B87Steps <= 0 Then
		B87Steps = 70 * Rnd(12, 30) - Min(B87Cur * 40, 70 * 8)
		If B87Cur >= 4 Then PlaySound_Strict(LoadTempSound("SFX\Indev\thump.wav"))
	EndIf
	Select B87LurkState
		Case 1 ;--------------------------------------------- standing at the end of the hall
			d = EntityDistance(B87Lurk, Collider)
			If B87Seen() Then B87LurkSeen = B87LurkSeen + FPSfactor
			If d < 2.2 Or B87LurkSeen > 70 * 1.4 Then
				HideEntity(B87Lurk)
				B87LurkState = 0
				IndevStress = Min(100, IndevStress + 6)
				PlaySound_Strict(LoadTempSound("SFX\Indev\thump.wav"))
			EndIf
		Case 2 ;--------------------------------------------- coming down after you
			If B87LurkTimer > 0 Then
				B87LurkTimer = B87LurkTimer - FPSfactor
				If B87LurkTimer <= 0 Then
					;it comes out of the stairs behind you
					PositionEntity(B87Lurk, f\ax, f\y + 0.66, f\az, True)
					ShowEntity(B87Lurk)
					PlaySound_Strict(LoadTempSound("SFX\Character\D9341\Heartbeat.ogg"))
					IS16Tell("Something is coming down the stairs behind you.", 3)
				EndIf
				Return
			EndIf
			d = EntityDistance(B87Lurk, Collider)
			Local spd#
			If B87Seen() Then spd = 0.003 Else spd = 0.012 + Min(B87Cur, 40) * 0.0006
			Local dx# = EntityX(Collider, True) - EntityX(B87Lurk, True), dz# = EntityZ(Collider, True) - EntityZ(B87Lurk, True)
			Local dy# = (EntityY(Collider, True) + 0.2) - EntityY(B87Lurk, True)
			Local l# = Sqr(dx * dx + dy * dy + dz * dz)
			If l > 0.01 Then TranslateEntity(B87Lurk, dx / l * spd * FPSfactor, dy / l * spd * FPSfactor, dz / l * spd * FPSfactor, True)
			If d < 1.6 Then HeartBeatRate = Max(HeartBeatRate, 120)
			If d < 0.5 And KillTimer >= 0 Then
				DeathMSG = "Subject D-9341 went down the SCP-087-B stairwell and did not come back. Audio from his radio picked up footsteps that were not his, getting closer, on floor " + B87Cur + "."
				Kill()
				HideEntity(B87Lurk)
				B87LurkState = 0
			EndIf
	End Select
End Function
