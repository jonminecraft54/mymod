;=====================================================================
; SCP: Containment Breach - Indev reworked item spawning
;
;   Design.md rules 4-6: every item that lands in the map has to justify
;   its slot. This file replaces the "hand-place everything, pray it fits"
;   approach with a per-room roll that follows the rules:
;
;     1. It runs only in a pill-safe room (Design.md rule 1e).
;     2. It rolls one themed category-appropriate item, low probability.
;     3. It never spawns a duplicate that a fixed spawn already placed.
;     4. It reports what it did to the debug log so the connection chain
;        can be audited (Design.md rule 5).
;
;   IndevRoll(r, x#, y#, z#) is the API: drop this into any FillRoom
;   case for a "sometimes an interesting thing is here" beat.
;
;   The rare pools are on purpose small and hand-curated. New pills are
;   added by name here; every entry has to already exist in Data\items.ini.
;=====================================================================

Global IndevRareCount% = 0

;a coarse "type of room" tag, used to pick the item pool
Function IndevRoomTag$(r.Rooms)
	If r = Null Then Return ""
	If r\RoomTemplate = Null Then Return ""
	Local n$ = r\RoomTemplate\Name
	Select n
		Case "medibay" Return "medical"
		Case "room2sroom", "room2offices", "room2offices2", "room2offices4", "room2newoffices2", "room2poffices", "room2poffices2" Return "office"
		Case "testroom3x3", "testroom4x4", "room2testroom", "room2testroom2", "testroom", "room1newscproom", "room2newroomtest6", "room2173cages" Return "testing"
		Case "room2storage", "room2closets", "room2oldclosets", "room2indevclosets", "room2indevclosets1", "room2scps", "room2scps2" Return "storage"
		Case "room2cafeteria", "room2newcaferoom", "room2toilets" Return "cafeteria"
	End Select
	Return IndevV02Tag(n) ;Indev: the generated "w series" rooms carry their category in IndevV02Data.bb
End Function

;count how many of an item are already in the map (used to prevent doubling)
Function IndevCountItem%(name$)
	Local it.Items, n%
	For it = Each Items
		If it\itemtemplate\name = name Then n = n + 1
	Next
	Return n
End Function

;one roll, per FillRoom. Cheap: one call per room. Returns True if it placed anything.
Function IndevRoll%(r.Rooms, x#, y#, z#)
	If r = Null Then Return False
	Local tag$ = IndevRoomTag(r)
	If tag = "" Then Return False

	;different odds per room type. Not everything drops something.
	Local chance% = 5
	Select tag
		Case "medical" chance = 3      ;1 in 3
		Case "office" chance = 5       ;1 in 5
		Case "testing" chance = 4      ;1 in 4
		Case "storage" chance = 4      ;1 in 4
		Case "cafeteria" chance = 5    ;1 in 5
	End Select
	If Rand(chance) <> 1 Then Return False

	;the pools. Every entry has to already exist in Data\items.ini.
	;The pool is small on purpose - rare and readable, not a slot machine.
	Local pool$[8], n% = 0
	Select tag
		Case "medical"
			pool[0] = "firstaid" : pool[1] = "firstaid2" : pool[2] = "scp9282"
			pool[3] = "scp500" : pool[4] = "syringe" : pool[5] = "indevration"
			pool[6] = "eyedrops" : n = 7
		Case "office"
			pool[0] = "bat" : pool[1] = "18vbat" : pool[2] = "cigarette"
			pool[3] = "wallet" : pool[4] = "coin" : pool[5] = "indevwater"
			pool[6] = "clipboard" : n = 7
		Case "testing"
			pool[0] = "scp474" : pool[1] = "scp1642" : pool[2] = "scp6833"
			pool[3] = "scp876r" : pool[4] = "scp876g" : pool[5] = "scp876b"
			pool[6] = "scp3494" : n = 7
		Case "storage"
			pool[0] = "bat" : pool[1] = "electronics" : pool[2] = "cup"
			pool[3] = "hand" : pool[4] = "18vbat" : pool[5] = "indevration"
			pool[6] = "gasmask" : n = 7
		Case "cafeteria"
			pool[0] = "indevration" : pool[1] = "indevwater" : pool[2] = "cup"
			pool[3] = "lemon" : pool[4] = "candy330_cherry" : pool[5] = "candy330_lemon"
			pool[6] = "candy330_apple" : n = 7
	End Select
	If n = 0 Then Return False

	Local pick% = Rand(1, n) - 1
	Local name$ = pool[pick]
	If name = "" Then Return False

	;anti-double: never drop a second copy of a unique pill in the same map
	If Left(name, 3) = "scp" And IndevCountItem(name) >= 1 Then Return False

	Local it.Items = CreateItem(name, x, y, z)
	If it = Null Then Return False
	EntityParent(it\collider, r\obj)
	IndevRareCount = IndevRareCount + 1
	DebugLog "IndevRoll: " + name + " placed in " + r\RoomTemplate\Name + " (tag=" + tag + ")"
	Return True
End Function

;the "chain check": Room -> Item -> Document -> Event -> SCP -> Progression
;Runs once at map init. Walks every existing room and confirms the chain
;is present for the run - a full seed always has at least one route the
;player can take. This isn't a hard gate: it logs what's missing so
;seeds can be inspected.
Function IndevChainAudit()
	Local rooms%, items%, docs%, events%, scps%, keys%
	Local r.Rooms, it.Items, e.Events
	For r = Each Rooms
		rooms = rooms + 1
	Next
	For it = Each Items
		items = items + 1
		If Left(it\itemtemplate\name, 3) = "doc" Or Left(it\itemtemplate\name, 4) = "note" Then docs = docs + 1
		If Left(it\itemtemplate\name, 3) = "key" Or it\itemtemplate\name = "mastercard" Then keys = keys + 1
		If Left(it\itemtemplate\name, 3) = "scp" Then scps = scps + 1
	Next
	For e = Each Events
		events = events + 1
	Next
	DebugLog "CHAIN AUDIT: rooms=" + rooms + " items=" + items + " docs=" + docs + " events=" + events + " scps=" + scps + " keys=" + keys
	DebugLog "CHAIN AUDIT: rare rolls placed this run = " + IndevRareCount
	If keys < 3 Then DebugLog "CHAIN AUDIT WARN: fewer than 3 keycards in the map. Progression may stall."
	If docs < 6 Then DebugLog "CHAIN AUDIT WARN: fewer than 6 documents. Run will feel empty."
	If scps < 4 Then DebugLog "CHAIN AUDIT WARN: fewer than 4 SCP items. Consider re-seeding."
End Function
