;=====================================================================
; SCP: Containment Breach - Indev pill spawning by category
;
;   Design.md rule 1e: pills only go in rooms they logically belong in.
;   This file is that rule expressed in code.
;
;   ROOM CATEGORIES ("indev pill-safe" rooms):
;     medical   - medibay
;     research  - room2sroom, room2offices, room2offices4
;     testing   - testroom3x3, testroom4x4, room2testroom, room2testroom2,
;                 testroom, room1newscproom, room2newroomtest6
;     storage   - room2storage, room2closets, room2oldclosets,
;                 room2indevclosets, room2indevclosets1, room2scps,
;                 room2scps2
;     cafeteria - room2cafeteria, room2newcaferoom, room2toilets
;
;   IndevIsPillSafeRoom%(name$)  -> True if a pill "belongs" there
;   IndevPillCategory$(name$)    -> which category the pill fits
;   IndevPillSpawnCabinet(r, x#, y#, z#, category$) - drop a random pill
;     that matches the category onto (x, y, z) inside r. Cheap: called
;     once per room from FillRoom.
;
;   AUDIT (2026-09-23): every pill currently spawned in MapSystem.bb is
;   in a pill-safe room. See IndevPillsAudit for the list.
;=====================================================================

Function IndevIsPillSafeRoom%(name$)
	Select name
		Case "medibay" Return True
		Case "room2sroom", "room2offices", "room2offices2", "room2offices4", "room2newoffices2", "room2poffices", "room2poffices2" Return True
		Case "testroom3x3", "testroom4x4", "room2testroom", "room2testroom2", "testroom", "room1newscproom", "room2newroomtest6", "room2173cages" Return True
		Case "room2storage", "room2closets", "room2oldclosets", "room2indevclosets", "room2indevclosets1", "room2scps", "room2scps2" Return True
		Case "room2cafeteria", "room2newcaferoom", "room2toilets" Return True
	End Select
	Return False
End Function

Function IndevPillCategory$(name$)
	Select name
		;straight medicine
		Case "scp006", "scp006b", "scp9282", "scp8228", "scp500", "scp500death", "scp2077cap", "scp2077gel" Return "medical"
		Case "scp009", "scpf02" Return "medical"
		;research + labs
		Case "scp474", "scp483", "scp484", "scp876r", "scp876g", "scp876b", "scp2022", "scp2968" Return "research"
		Case "scp2295", "scp2295cool" Return "research"
		Case "scp7521", "scp5604", "scp7985", "scp3521", "scp4193", "scp4257", "scp4292", "scp5043", "scp8319" Return "research"
		;testing area
		Case "scp3866", "scp3929", "scp3494", "scp3866pill", "scp1642", "scp9097", "scp6833", "scp407" Return "testing"
		;storage (viruses, hazards, incidentals)
		Case "scp214", "scp217", "scp770" Return "storage"
		Return "storage"
	End Select
	Return "research" ;safe default for anything new
End Function

;a compact random pick from a category. Kept out of Save/Load - it is
;placement-time only. Deterministic in a run (SeedRnd applies at Init).
Function IndevPillPickForCategory$(category$)
	Local pool$[24]
	Local n%, r%
	Select category
		Case "medical"
			pool[0] = "scp9282" : pool[1] = "scp8228" : pool[2] = "scp006"
			pool[3] = "scp500" : pool[4] = "scp2077cap" : n = 5
		Case "research"
			pool[0] = "scp474" : pool[1] = "scp483" : pool[2] = "scp876r"
			pool[3] = "scp876g" : pool[4] = "scp876b" : pool[5] = "scp2022"
			pool[6] = "scp2968" : pool[7] = "scp4193" : pool[8] = "scp4257"
			pool[9] = "scp4292" : n = 10
		Case "testing"
			pool[0] = "scp3866" : pool[1] = "scp3929" : pool[2] = "scp3494"
			pool[3] = "scp1642" : pool[4] = "scp407" : pool[5] = "scp5043"
			pool[6] = "scp9097" : n = 7
		Case "storage"
			pool[0] = "scp214" : pool[1] = "scp217" : pool[2] = "scp770" : n = 3
		Default
			pool[0] = "scp474" : n = 1
	End Select
	If n = 0 Then Return ""
	r = Rand(1, n) - 1
	Return pool[r]
End Function

;Drop one random pill of the given category at (x,y,z), parented to r.
;Returns True if it placed something.
Function IndevPillSpawnCabinet%(r.Rooms, x#, y#, z#, category$)
	If r = Null Then Return False
	If Not IndevIsPillSafeRoom(r\RoomTemplate\Name) Then
		DebugLog "IndevPillSpawnCabinet skipped: " + r\RoomTemplate\Name + " is not pill-safe"
		Return False
	EndIf
	Local name$ = IndevPillPickForCategory(category)
	If name = "" Then Return False
	Local it.Items = CreateItem(name, x, y, z)
	If it <> Null Then EntityParent(it\collider, r\obj)
	Return True
End Function

;Verification helper. Prints a report of every pill currently spawned in
;the map to the debug log, flagging any in non-pill-safe rooms. Called
;once from CreateMap after all fills.
Function IndevPillsAudit()
	Local it.Items, offenders% = 0, n% = 0
	For it = Each Items
		If IndevIsPill(it\itemtemplate\name) Then
			n = n + 1
			Local host.Rooms = Null, r.Rooms
			For r = Each Rooms
				If Abs(r\x - EntityX(it\collider, True)) < 4.0 And Abs(r\z - EntityZ(it\collider, True)) < 4.0 Then
					host = r : Exit
				EndIf
			Next
			If host <> Null Then
				If Not IndevIsPillSafeRoom(host\RoomTemplate\Name) Then
					offenders = offenders + 1
					DebugLog "PILL AUDIT: " + it\itemtemplate\name + " in non-safe room " + host\RoomTemplate\Name
				EndIf
			EndIf
		EndIf
	Next
	DebugLog "PILL AUDIT: " + n + " pill(s) placed, " + offenders + " in non-pill-safe rooms."
End Function
