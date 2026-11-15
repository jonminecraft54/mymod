;=====================================================================
; SCP: Containment Breach - Indev SCP-140 "A Chronicle of the Daevas"
;
;   A modern black-bound hardcover with an unremarkable jacket except for
;   the title, "A Chronicle of the Daevas", and an illegible author
;   signature inside the cover. It reads as a first-hand chronicle of the
;   Daevites, an ancient Siberian civilization that never officially
;   existed: militarism, ancestor worship, mass human sacrifice, and
;   apparently-efficacious thaumaturgic rituals. There are more pages
;   between the covers than could physically fit.
;
;   If the book contacts blood, ink, or any other writing fluid, the
;   chronicle keeps writing itself - not just elaborating the past, but
;   extending the Daevite timeline FORWARD. In the game we simplify this
;   to an item state that ticks forward while the book sits idle in your
;   inventory (standing in for undetected contact with something), each
;   tick giving the player another paragraph to read via doc140.
;
;   Purpose:     a slow-drip lore item, entirely optional
;   Effect:      each state adds a paragraph the player can read via the
;                doc140 file (drawn dynamically by Main.bb like note268)
;   Drawback:    every time it ticks a page forward, IndevStress +2 -
;                the book is uncanny to hold, and one in fifteen readers
;                report a faint smell of dried blood off it
;   Reason:      Daevite lore fills in the mod's history
;   Vanilla-first: reuses item state, Msg/MsgTimer, IndevStress. No new
;   key binds.
;=====================================================================

Global I140Book.Items          ;the copy the mod places on the desk
Global I140Timer#

Function Indev140Reset()
	I140Book = Null : I140Timer = 0
End Function

;called from MapSystem's Case "room2clipboardtextroom"
;
;PLACEMENT NOTE (fixed 2026-09-24 after in-game report): the previous
;coordinates used a desk-top height (r\y + 148 * RoomScale) that was
;copied from a different room's fill function. room2clipboardtextroom's
;own desk/table legs are at a different spot, and the book landed on the
;floor UNDER a table, wedged against leg colliders - close enough that
;EntityPickMode's raycast couldn't get a clean line to it, so it was
;unclickable.
;
;Fix: drop all three items directly on the open floor near the room
;centre, well clear of any leg geometry, at a small clearance height so
;gravity settles them flat without falling through. If a later pass
;wants them properly on the desk, get the desk's actual local (x,y,z)
;bounds from the .rmesh in CBRE first - don't guess a copied offset.
Function IndevFill140(r.Rooms)
	Local it.Items

	;the book itself
	it = CreateItem("scp140", r\x, r\y + 0.1, r\z)
	If it <> Null Then
		EntityParent(it\collider, r\obj)
		I140Book = it
		it\state = 0
	EndIf

	;the reader's summary doc, half a metre to the side
	it = CreateItem("doc140", r\x + 0.5, r\y + 0.1, r\z)
	If it <> Null Then EntityParent(it\collider, r\obj)

	;a clipboard of related paperwork, the other side
	it = CreateItem("clipboard", r\x - 0.5, r\y + 0.1, r\z)
	If it <> Null Then EntityParent(it\collider, r\obj)

	DebugLog "Indev: IndevFill140 - SCP-140 floor placement at (" + r\x + ", " + r\y + ", " + r\z + ")"
End Function

;every ~90 seconds while a state<3 copy of the book is in inventory, tick
;its state forward. Stress +2 per tick.
Function UpdateIndev140()
	If KillTimer < 0 Then Return
	I140Timer = I140Timer + FPSfactor
	If I140Timer < 70.0 * 90.0 Then Return
	I140Timer = 0

	Local i%, tickedOne% = False
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			If Inventory(i)\itemtemplate <> Null Then
				If Inventory(i)\itemtemplate\name = "scp140" And Inventory(i)\state < 3 Then
					Inventory(i)\state = Inventory(i)\state + 1
					IndevStress = Min(100, IndevStress + 2)
					tickedOne = True
				EndIf
			EndIf
		EndIf
	Next

	If tickedOne Then
		Msg = "The chronicle has more pages in it than it did an hour ago. The last paragraph is in a different hand."
		MsgTimer = 70 * 5
	EndIf
End Function
