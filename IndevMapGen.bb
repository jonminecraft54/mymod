;=====================================================================
; SCP: Containment Breach - Indev facility generation
;
; Additions on top of the stock generator in MapSystem.bb:
;   - 5 starting layouts ("styles") picked per seed
;   - rare loops (circular corridors / alternate routes / HCZ shortcuts)
;   - layout validation: everything reachable, no big enclosed empty areas
;   - "broken sections": a few doors that are jammed shut for good,
;     only where an alternate route exists
;   - a debug report for rooms that can't be reached after generation
;=====================================================================

Dim IndevVisited%(1, 1)
Dim IndevQX%(1), IndevQY%(1)

Type IndevBrokenDoor
	Field d.Doors
End Type

;---------------------------------------------------------------------
; Starting layouts
;---------------------------------------------------------------------

Function IndevSetLayoutStyle()
	IndevLayoutStyle = Rand(1,5)

	;defaults = the classic CB layout
	IndevLayoutStartX = Floor(MapWidth / 2)
	IndevWidthMin = 0.6 : IndevWidthMax = 0.85
	IndevHeightMin = 3 : IndevHeightMax = 4
	IndevBranchMin = 4 : IndevBranchMax = 5

	Select IndevLayoutStyle
		Case 1 ;Classic: centred spine, long hallways
		Case 2 ;West wing: starts on the left, shorter hallways
			IndevLayoutStartX = Floor(MapWidth * 0.3)
			IndevWidthMin = 0.5 : IndevWidthMax = 0.75
		Case 3 ;East wing: starts on the right, shorter hallways
			IndevLayoutStartX = Floor(MapWidth * 0.7)
			IndevWidthMin = 0.5 : IndevWidthMax = 0.75
		Case 4 ;Grid: wide hallways with many branches
			IndevWidthMin = 0.7 : IndevWidthMax = 0.9
			IndevBranchMin = 5 : IndevBranchMax = 6
		Case 5 ;Warren: narrow hallways, more floors, fewer branches (more dead ends)
			IndevLayoutStartX = Rand(Floor(MapWidth * 0.35), Floor(MapWidth * 0.65))
			IndevWidthMin = 0.45 : IndevWidthMax = 0.65
			IndevHeightMin = 2 : IndevHeightMax = 4
			IndevBranchMin = 3 : IndevBranchMax = 4
	End Select

	IndevLayoutStartX = Max(Min(IndevLayoutStartX, MapWidth - 3), 2)
End Function

;---------------------------------------------------------------------
; Loops: rare circular corridors, alternate routes and shortcuts
;---------------------------------------------------------------------

Function IndevAddLoops%()
	Local wanted% = 0
	Select Rand(1,10)
		Case 1, 2, 3, 4
			wanted = 1
		Case 5, 6
			wanted = 2
		Case 7 ;rare: several loops
			wanted = 3
	End Select

	Local placed% = 0, tries% = 0, x%, y%
	While placed < wanted And tries < 400
		tries = tries + 1
		x = Rand(2, MapWidth - 3)
		y = Rand(2, MapHeight - 3) ;never next to the starting room at the bottom row
		If MapTemp(x, y) = 0 Then
			If IndevCanConnect(x, y) Then
				MapTemp(x, y) = 1
				placed = placed + 1
				DebugLog "Indev: loop connector at ("+x+", "+y+")"
			EndIf
		EndIf
	Wend

	Return placed
End Function

;an empty cell can join two existing corridors if it sits exactly between them
;(forming a straight hallway) and doesn't touch a checkpoint or cross zones
Function IndevCanConnect%(x%, y%)
	Local horiz% = (MapTemp(x-1, y) > 0 And MapTemp(x+1, y) > 0 And MapTemp(x, y-1) = 0 And MapTemp(x, y+1) = 0)
	Local vert% = (MapTemp(x, y-1) > 0 And MapTemp(x, y+1) > 0 And MapTemp(x-1, y) = 0 And MapTemp(x+1, y) = 0)

	If horiz Then
		If MapTemp(x-1, y) = 255 Or MapTemp(x+1, y) = 255 Then Return False
		Return True
	ElseIf vert Then
		If MapTemp(x, y-1) = 255 Or MapTemp(x, y+1) = 255 Then Return False
		If GetZone(y-1) <> GetZone(y) Or GetZone(y) <> GetZone(y+1) Then Return False
		Return True
	EndIf

	Return False
End Function

;---------------------------------------------------------------------
; Layout validation
;---------------------------------------------------------------------

Function IndevLayoutIsValid%()
	Local x%, y%, total% = 0, sx% = -1, sy% = -1

	For y = 0 To MapHeight
		For x = 0 To MapWidth
			If MapTemp(x, y) > 0 Then
				total = total + 1
				If sx < 0 Then sx = x : sy = y
			EndIf
		Next
	Next

	If total = 0 Then Return False

	;too sparse = lots of empty space
	If total < Floor((MapWidth - 2) * (MapHeight - 2) * 0.25) Then
		DebugLog "Indev: layout rejected, too sparse ("+total+" cells)"
		Return False
	EndIf

	;every cell has to be reachable from every other cell
	If IndevFloodFill(sx, sy) < total Then
		DebugLog "Indev: layout rejected, unreachable cells"
		Return False
	EndIf

	;no big enclosed empty areas inside the facility
	If IndevHasEnclosedHole(4) Then
		DebugLog "Indev: layout rejected, enclosed empty area"
		Return False
	EndIf

	Return True
End Function

;returns the number of occupied cells reachable from (sx, sy)
Function IndevFloodFill%(sx%, sy%)
	Local x%, y%, nx%, ny%, dir%, qHead% = 0, qTail% = 0, reached% = 0
	Local size% = (MapWidth + 2) * (MapHeight + 2)

	Dim IndevVisited%(MapWidth + 1, MapHeight + 1)
	Dim IndevQX%(size), IndevQY%(size)

	IndevQX(0) = sx : IndevQY(0) = sy : qTail = 1
	IndevVisited(sx, sy) = True

	While qHead < qTail
		x = IndevQX(qHead) : y = IndevQY(qHead)
		qHead = qHead + 1
		reached = reached + 1

		For dir = 0 To 3
			nx = x : ny = y
			Select dir
				Case 0
					nx = x + 1
				Case 1
					nx = x - 1
				Case 2
					ny = y + 1
				Case 3
					ny = y - 1
			End Select
			If nx >= 0 And ny >= 0 And nx <= MapWidth And ny <= MapHeight Then
				If MapTemp(nx, ny) > 0 And (Not IndevVisited(nx, ny)) Then
					IndevVisited(nx, ny) = True
					IndevQX(qTail) = nx : IndevQY(qTail) = ny
					qTail = qTail + 1
				EndIf
			EndIf
		Next
	Wend

	Return reached
End Function

;an empty size*size block that has facility on all four sides of it
Function IndevHasEnclosedHole%(size%)
	Local x0%, y0%, x%, y%, empty%, hasL%, hasR%, hasU%, hasD%

	For y0 = 1 To MapHeight - 1 - size
		For x0 = 1 To MapWidth - 1 - size
			empty = True
			For y = y0 To y0 + size - 1
				For x = x0 To x0 + size - 1
					If MapTemp(x, y) > 0 Then empty = False : Exit
				Next
				If (Not empty) Then Exit
			Next

			If empty Then
				hasL = False : hasR = False : hasU = False : hasD = False
				For y = y0 To y0 + size - 1
					For x = 0 To x0 - 1
						If MapTemp(x, y) > 0 Then hasL = True
					Next
					For x = x0 + size To MapWidth
						If MapTemp(x, y) > 0 Then hasR = True
					Next
				Next
				For x = x0 To x0 + size - 1
					For y = 0 To y0 - 1
						If MapTemp(x, y) > 0 Then hasU = True
					Next
					For y = y0 + size To MapHeight
						If MapTemp(x, y) > 0 Then hasD = True
					Next
				Next
				If hasL And hasR And hasU And hasD Then Return True
			EndIf
		Next
	Next

	Return False
End Function

;---------------------------------------------------------------------
; Room-level checks (after the rooms and doors exist)
;---------------------------------------------------------------------

;rooms that are part of the facility grid (not the intro, dimensions or the surface)
Function IndevIsGridRoom%(r.Rooms)
	If r = Null Then Return False
	If r\y <> 0 Then Return False
	Select r\RoomTemplate\Name
		Case "173", "pocketdimension", "gatea", "dimension1499"
			Return False
	End Select
	Return True
End Function

;counts the grid rooms reachable from the starting room
;blocked = a door to treat as impassable, plus every door already broken
Function IndevCountReachableRooms%(blocked.Doors)
	Local r.Rooms, r2.Rooms, startRoom.Rooms = Null, i%, d.Doors, bd.IndevBrokenDoor
	Local count% = 0, grew% = True, isBroken%

	For r = Each Rooms
		r\found = False
		If r\RoomTemplate\Name = "start" Then startRoom = r
	Next
	If startRoom = Null Then Return 0

	startRoom\found = True
	count = 1

	;simple repeated expansion, the grid is small
	While grew
		grew = False
		For r = Each Rooms
			If r\found Then
				For i = 0 To 3
					r2 = r\Adjacent[i]
					d = r\AdjDoor[i]
					If r2 <> Null And d <> Null Then
						If (Not r2\found) And IndevIsGridRoom(r2) And d <> blocked Then
							isBroken = False
							For bd = Each IndevBrokenDoor
								If bd\d = d Then isBroken = True : Exit
							Next
							If (Not isBroken) Then
								r2\found = True
								count = count + 1
								grew = True
							EndIf
						EndIf
					EndIf
				Next
			EndIf
		Next
	Wend

	;reset the flag, the map screen uses it for discovered rooms
	For r = Each Rooms
		r\found = False
	Next

	Return count
End Function

Function IndevReportUnreachableRooms()
	Local r.Rooms, total% = 0
	For r = Each Rooms
		If IndevIsGridRoom(r) Then total = total + 1
	Next
	Local reached% = IndevCountReachableRooms(Null)
	If reached < total Then
		DebugLog "Indev WARNING: "+(total-reached)+" of "+total+" rooms can't be reached from the start"
	Else
		DebugLog "Indev: all "+total+" rooms are reachable"
	EndIf
End Function

;---------------------------------------------------------------------
; Broken sections
;---------------------------------------------------------------------

;a room can have a broken door if it is plain filler with no event attached
Function IndevCanBreakRoom%(r.Rooms)
	If (Not IndevIsGridRoom(r)) Then Return False
	If r\RoomTemplate\SetRoom >= 0 Then Return False
	If r\RoomTemplate\Commonness = 0 Then Return False
	Local e.Events
	For e = Each Events
		If e\room = r Then Return False
	Next
	Return True
End Function

;jams 0-2 doors shut for good, but only where the rest of the facility stays reachable,
;so there is always a way around
Function IndevBreakSections()
	Local wanted% = Rand(0,2), broken% = 0, tries% = 0
	Local r.Rooms, pick%, count%, i%, d.Doors, bd.IndevBrokenDoor

	Delete Each IndevBrokenDoor
	If wanted = 0 Then Return

	Local baseline% = IndevCountReachableRooms(Null)

	count = 0
	For r = Each Rooms
		If IndevCanBreakRoom(r) Then count = count + 1
	Next
	If count = 0 Then Return

	While broken < wanted And tries < 80
		tries = tries + 1

		pick = Rand(1, count)
		i = 0
		For r = Each Rooms
			If IndevCanBreakRoom(r) Then
				i = i + 1
				If i = pick Then Exit
			EndIf
		Next

		i = Rand(0,3)
		d = r\AdjDoor[i]
		If d <> Null And r\Adjacent[i] <> Null Then
			If IndevCanBreakRoom(r\Adjacent[i]) And (Not d\locked) And d\KeyCard = 0 And d\Code = "" And (Not d\IsElevatorDoor) Then
				If IndevCountReachableRooms(d) = baseline Then
					d\open = False
					d\locked = True
					bd = New IndevBrokenDoor
					bd\d = d
					broken = broken + 1
					DebugLog "Indev: broken door between "+r\RoomTemplate\Name+" and "+r\Adjacent[i]\RoomTemplate\Name
				EndIf
			EndIf
		EndIf
	Wend
End Function

;make sure the test rooms are in every map. CreateRooms hands the n-th 4-way tile (scanning y from the
;bottom/LCZ up, x left to right) MapRoom(ROOM4, n), so write the names into free slots in that same order.
Function IndevForceTestRooms()
	IndevForceRoom4("testroom3x3")
	IndevForceRoom4("testroom4x4")
End Function

Function IndevForceRoom4(name$)
	Local x%, y%, n% = 0, i%
	For i = 0 To MaxPositions(ROOM4, ZONEAMOUNT-1) - 1
		If MapRoom(ROOM4, i) = name Then Return
	Next
	;first pass: a free slot; second pass: take over a random filler slot if every 4-way is already claimed
	Local pass%
	For pass = 0 To 1
		n = 0
		For y = MapHeight - 1 To 0 Step -1
			For x = 1 To MapWidth - 2
				If MapTemp(x, y) = 4 Then
					If pass = 0 And MapRoom(ROOM4, n) = "" Then
						MapRoom(ROOM4, n) = name : DebugLog "Indev: forced " + name + " into ROOM4 slot " + n : Return
					ElseIf pass = 1 And MapRoom(ROOM4, n) <> "testroom3x3" And MapRoom(ROOM4, n) <> "testroom4x4" And MapRoom(ROOM4, n) <> "room4info" Then
						MapRoom(ROOM4, n) = name : DebugLog "Indev: " + name + " replaced ROOM4 slot " + n : Return
					EndIf
					n = n + 1
				EndIf
			Next
		Next
	Next
	DebugLog "Indev: no 4-way tile for " + name
End Function


;---------------------------------------------------------------------
; Checkpoints (zone border rooms)
;---------------------------------------------------------------------

;a checkpoint is a straight north-south room: a corridor above, a corridor below, nothing at its sides
Function IndevCheckpointOK%(x%, y%)
	If x < 1 Or x > MapWidth - 2 Then Return False
	If MapTemp(x, y - 1) = 0 Or MapTemp(x, y + 1) = 0 Then Return False
	If MapTemp(x - 1, y) <> 0 Or MapTemp(x + 1, y) <> 0 Then Return False
	Return True
End Function

;every corridor that crossed a zone border became a checkpoint - three to six per border, some of them dead
;ends (nothing behind the far door) or with rooms at their sides they can't connect to. Keep at most two good
;ones per border, make the rest ordinary rooms, and if a border has no good one, cut a fresh checkpoint where a
;corridor above meets one below. No Rand: the same seed still gives the same map.
Function IndevFixCheckpoints()
	Local x%, y%, kept%, made%
	For y = 2 To MapHeight - 2
		If GetZone(y) <> GetZone(y + 1) Then
			kept = 0
			For x = 1 To MapWidth - 2
				If MapTemp(x, y) = 255 Then
					If IndevCheckpointOK(x, y) And kept < 2 Then
						kept = kept + 1
					Else
						MapTemp(x, y) = 1
					EndIf
				EndIf
			Next
			If kept = 0 Then
				;no good checkpoint: turn a room on the border row into one, or fill a gap between two corridors
				made = False
				For x = 1 To MapWidth - 2
					If MapTemp(x, y) <> 0 And IndevCheckpointOK(x, y) Then
						MapTemp(x, y) = 255 : made = True : Exit
					EndIf
				Next
				If Not made Then
					For x = 1 To MapWidth - 2
						If MapTemp(x, y) = 0 And IndevCheckpointOK(x, y) Then
							MapTemp(x, y) = 255 : made = True : Exit
						EndIf
					Next
				EndIf
				If Not made Then
					;last resort: a corridor reaching the border from below - run it up until it meets the zone above
					Local y2%
					For x = 2 To MapWidth - 3
						If MapTemp(x, y + 1) <> 0 And MapTemp(x, y) = 0 And MapTemp(x - 1, y) = 0 And MapTemp(x + 1, y) = 0 Then
							For y2 = y - 1 To 1 Step -1
								If MapTemp(x, y2) <> 0 Then
									made = True : Exit
								EndIf
								If MapTemp(x - 1, y2) <> 0 Or MapTemp(x + 1, y2) <> 0 Then
									made = True : y2 = y2 - 1 : Exit
								EndIf
							Next
							If made Then
								Local yy%
								For yy = y2 + 1 To y - 1
									If MapTemp(x, yy) = 0 Then MapTemp(x, yy) = 1
								Next
								MapTemp(x, y) = 255
								Exit
							EndIf
						EndIf
					Next
				EndIf
			EndIf
		EndIf
	Next
End Function
