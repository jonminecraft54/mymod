;=====================================================================
; SCP: Containment Breach - Indev: fourteenth batch, SCP-4035 and SCP-3886
;
;   room2lampshop      LCZ  SCP-4035, Prey on Words. Put a bulb in the lamp (click the shade while carrying one).
;                           A gaseous salesman steps out and asks you something. Any answer, any key, and you get
;                           a "lackluster" ability: a harmful one, or none at all. Then he goes back in.
;   room2saddlestall   HCZ  SCP-3886. Lift the saddle from its rack (click it) and the animal in the straw gets up
;                           and walks to you, and stops by your feet.
;
;   IndevU14Data.bb is generated (Tools\roomkit\gen_b14.py): the U14_* constants, the FillRoom table and the events.
;   This file holds the scripted parts. The bulb, notes and photograph are items; the lamp, saddle and animal are
;   pivots and props in the room.
;=====================================================================

;SCP-3886's animal: a dark block in the straw until it is modelled. Its centre is the ANIMAL pivot.
Function IndevU14Dress(r.Rooms)
	Select r\RoomTemplate\Name
		Case "room2saddlestall"
			r\Objects[U14_STL_ANIMALM] = IS04Box(r, r\Objects[U14_STL_ANIMAL], 34.0, 40.0, 84.0, "GFX\map\misc.jpg")
	End Select
End Function

Function UpdateIndevU14(e.Events)
	Local r.Rooms = e\room
	Select r\RoomTemplate\Name
		Case "room2lampshop"
			UpdateU14Lamp(e)
		Case "room2saddlestall"
			UpdateU14Saddle(e)
	End Select
End Function

;SCP-4035. EventState: 0 waiting for a bulb, 1 the salesman is asking, 2 he has gone back into the shade.
;EventState2: the frames he has waited for an answer.
Function UpdateU14Lamp(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U14_LSH_LAMP]
	If PlayerRoom <> r Then Return
	Select Int(e\EventState)
		Case 0
			If IS10Press(p, 2.5) Then
				If IndevHasItem("bulb") Then
					IndevTakeBulb14()
					e\EventState = 1
					e\EventState2 = 0
					IS16Tell("The bulb goes in and the shade lights up blue. A gaseous man in a brown coat steps out, a cigar in his hand. " + Chr(34) + "Interested in something to buy? Say anything." + Chr(34), 12)
				Else
					IS16Tell("The socket is empty, and the shade gives no light.", 6)
				EndIf
			EndIf
		Case 1
			e\EventState2 = e\EventState2 + FPSfactor
			If GetKey() <> 0 Lor MouseHit1 Then
				MouseHit1 = False
				IndevLamp14Ability()
				e\EventState = 2
			ElseIf e\EventState2 > 70 * 30 Then
				IS16Tell("He sighs, puts the cigar out on the shade and goes back in. " + Chr(34) + "Sorry kid, no refunds." + Chr(34), 8)
				e\EventState = 2
			EndIf
		Case 2
			If IS10Press(p, 2.5) Then IS16Tell(Chr(34) + "Sorry kid, no refunds." + Chr(34), 5)
	End Select
End Function

;the lamp's price: one of four disappointments, each with a small real effect
Function IndevLamp14Ability()
	Select Rand(0, 3)
		Case 0
			IS16Tell("You can tell when a shop is about to close now. Nobody has ever asked you to.", 8)
		Case 1
			Stamina = Min(Stamina, 15)
			IS16Tell("Your legs remember every step you have ever taken, and they would like you to stop.", 8)
		Case 2
			Injuries = Injuries + 0.5
			IS16Tell("A cramp shoots up your arm, like the one from the job you did not want.", 8)
		Case 3
			IndevStress = Min(100, IndevStress + 25)
			IS16Tell("You can see exactly how this ends. It is not a good ending, and it is not a surprise.", 8)
	End Select
End Function

;take one bulb out of the inventory (the first one found)
Function IndevTakeBulb14()
	Local n%
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) <> Null Then
			If Inventory(n)\itemtemplate\name = "bulb" Then
				RemoveItem(Inventory(n))
				Return
			EndIf
		EndIf
	Next
End Function

;SCP-3886. EventState: 0 the saddle is on the rack, 1 the animal walks to you, 2 it has stopped by your feet.
;EventState2: the frames it has walked.
Function UpdateU14Saddle(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U14_STL_SADDLE], m% = r\Objects[U14_STL_ANIMALM]
	Local left#
	If PlayerRoom <> r Then Return
	Select Int(e\EventState)
		Case 0
			If IS10Press(p, 2.5) Then
				e\EventState = 1
				e\EventState2 = 0
				IS16Tell("You lift the saddle off the rack. Behind you, something stands up in the straw. It is walking towards you, quickly, for something its size.", 10)
			EndIf
		Case 1
			e\EventState2 = e\EventState2 + FPSfactor
			IAxLocal(r)
			left = IS10Walk(m, TFormedX(), TFormedZ(), 2.2)
			If left < 90.0 Lor e\EventState2 > 70 * 25 Then
				e\EventState = 2
				IS16Tell("It stops by your feet. It waits for an instruction, and it is not yet sure which of you it should obey.", 9)
			EndIf
		Case 2
			If IS10Press(p, 2.5) Then IS16Tell("It lies back down in the straw, more slowly than it got up.", 6)
	End Select
End Function
