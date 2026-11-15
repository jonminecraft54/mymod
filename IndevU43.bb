;=====================================================================
; SCP: Containment Breach - Indev: the forty-third batch - the lift lobby, the checkpoint, the offices
;
;   room2b45lobby       the working lift down to the hoist control office (UpdateElevators); the dead lifts'
;                       call panel; the HOIST and DOOR switches; a locker you can hide in (106 and the guards lose
;                       you while you stand in it)
;   room2b45checkpoint  the guard in the booth talks to you through the window - and lets you through if you
;                       carry a Level 3 card or better; the scanner arch beeps at you whatever you carry
;   room2b45offices     the telephone on the open floor rings and rings; answer it if you like
;=====================================================================

Global I43Hoist%, I43Phone#, I43PhoneN%, I43Guard%, I43Hide%

Function Indev43Reset(newGame%)
	If newGame Then
		I43Hoist = 0 : I43PhoneN = 0 : I43Guard = 0
	EndIf
	I43Phone = 70 * 20 : I43Hide = False
End Function

Function IndevU43Dress(r.Rooms)
End Function

;the best keycard in the inventory (1..5, 0 for none)
Function U43BestCard%()
	Local k%, best% = 0, n$
	For k = 0 To MaxItemAmount - 1
		If Inventory(k) <> Null Then
			n = Inventory(k)\itemtemplate\name
			If Left(n, 3) = "key" And Len(n) = 4 Then best = Max(best, Int(Right(n, 1)))
		EndIf
	Next
	Return best
End Function

Function UpdateIndevU43(e.Events)
	Local r.Rooms = e\room, n.NPCs, d.Doors
	Select r\RoomTemplate\Name
		;---------------- the lift lobby
		Case "room2b45lobby"
			If PlayerRoom <> r Then
				If I43Hide Then NoTarget = False
				I43Hide = False
				Return
			EndIf
			e\EventState2 = UpdateElevators(e\EventState2, r\RoomDoors[0], r\RoomDoors[1], r\Objects[0], r\Objects[1], e)
			If IS10Press(r\Objects[U43_LBY_DEADLIFT], 1.8) Then
				IS16Tell("The call button for lift 3 is dead. You press it anyway. Far down the shaft, very faintly, the car bell rings - once.", 6)
			EndIf
			If IS10Press(r\Objects[U43_LBY_HOIST], 1.4) Then
				I43Hoist = 1 - I43Hoist
				CameraShake = 1.5
				IS10Sound("SFX\Indev\creak.wav", r\Objects[U43_LBY_HOIST], 8.0, 0.9)
				If I43Hoist Then
					IS16Tell("HOIST: ON. Somewhere behind the wall, cables take up a heavy load. Shaft 2 groans. Nothing should be in shaft 2.", 7)
				Else
					IS16Tell("HOIST: OFF. The load settles. For a moment there is a scraping in shaft 2, going down.", 6)
				EndIf
			EndIf
			If IS10Press(r\Objects[U43_LBY_DOORSW], 1.4) Then
				IS16Tell("DOOR: the switch clacks over and back. Lifts 2 and 3 - DOOR CIRCUIT FUSED. A sticky note: 'don't'.", 6)
			EndIf
			;the locker: stand in it and you are hidden
			If EntityDistance(Collider, r\Objects[U43_LBY_LOCKER]) < 0.55 Then
				If Not I43Hide Then
					I43Hide = True : NoTarget = True
					IS16Tell("You squeeze into the locker and pull the door to. Through the slats, the office. Breathe quietly.", 5)
				EndIf
			ElseIf I43Hide Then
				I43Hide = False : NoTarget = False
			EndIf
		;---------------- the checkpoint
		Case "room2b45checkpoint"
			If e\EventState = 0 And r\dist < 12 Then
				e\EventState = 1
				n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U43_CHK_GUARD], True), EntityY(r\Objects[U43_CHK_GUARD], True) + 0.35, EntityZ(r\Objects[U43_CHK_GUARD], True))
				n\State = 9 : r\NPC[0] = n
				RotateEntity(n\Collider, 0, EntityYaw(r\obj, True) + 270, 0)
			EndIf
			U37Pin(r\NPC[0], r\Objects[U43_CHK_GUARD], 0.0, 0.35)
			If PlayerRoom <> r Then Return
			If IS10Press(r\Objects[U43_CHK_WINDOW], 1.8) Then
				I43Guard = I43Guard + 1
				If U43BestCard() >= 3 Then
					;open the screening hall door for them
					For d = Each Doors
						If d\room = r And d\KeyCard >= 3 Then d\locked = False : d\open = True
					Next
					IAxSay("Guard", "(taps the glass) Card. ...Level " + U43BestCard() + ". Fine. Go. Screening hall's open - don't touch anything on the table.", 7)
				Else
					Select I43Guard
						Case 1 : IAxSay("Guard", "Stop. Lockdown. Nobody through without a Level 3 card. Where's yours?", 6)
						Case 2 : IAxSay("Guard", "No card, no entry. I'm not opening this window and I'm not coming out.", 6)
						Default : IAxSay("Guard", "Look - I haven't seen anyone come back from the screening hall in an hour. Get a card or go back.", 7)
					End Select
				EndIf
			EndIf
			If EntityDistance(Collider, r\Objects[U43_CHK_SCANNER]) < 0.9 And e\EventState3 <= 0 Then
				e\EventState3 = 70 * 6
				IS10Sound("SFX\Indev\clicks.wav", r\Objects[U43_CHK_SCANNER], 6.0, 1.0)
				IS16Tell("BEEP. The scanner arch lights red. You're carrying nothing it should care about. It beeps again, as if something behind you walked through too.", 6)
			EndIf
			If e\EventState3 > 0 Then e\EventState3 = e\EventState3 - FPSfactor
		;---------------- the offices
		Case "room2b45offices"
			If PlayerRoom <> r Then Return
			I43Phone = I43Phone - FPSfactor
			If I43Phone <= 0 Then
				I43Phone = 70 * Rnd(8, 14)
				IS10Sound("SFX\Indev\clicks.wav", r\Objects[U43_OFC_PHONE], 10.0, 0.7)
				If Rand(3) = 1 Then IS16Tell("Somewhere on the open floor, a telephone is ringing.", 3)
			EndIf
			If IS10Press(r\Objects[U43_OFC_PHONE], 1.4) Then
				I43PhoneN = I43PhoneN + 1
				Select I43PhoneN
					Case 1 : IS16Tell("You pick up. Office noise - typing, a kettle, people laughing - a normal day. Then someone close to the receiver says: 'Who's that standing in the open office?'", 9)
					Case 2
						IndevStress = Min(100, IndevStress + 10)
						IS16Tell("You pick up. Silence. Then your own breathing, a second behind your breathing.", 6)
					Default : IS16Tell("The line is dead. The cable is cut. It rang a moment ago.", 5)
				End Select
				I43Phone = 70 * 30
			EndIf
	End Select
End Function
