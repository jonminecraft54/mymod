;=====================================================================
; SCP: Containment Breach - Indev: the forty-first batch - staff, medical, security, recreation and D-block rooms
; (from the community's room ideas). Light on code: one or two interactions per room.
;
;   room2b43staff     the projector that shows a face; SCP-860 sometimes left by the coffee (an item)
;   room2b43medical   the fume hood, the x-ray with too many ribs, the dissection table
;   room2b43security  dead guards in the armory; a body falls out of a locker when you open it
;   room2b43rec       the theater screen flashes hard enough to blind you while you are in there; the gym is
;                     different every game - barricaded survivors who shout at you, bodies, or nothing
;   room2b43dblock    the dead of D-block
;=====================================================================

Global I41Locker%, I41ProjN%

Function Indev41Reset(newGame%)
	If newGame Then
		I41Locker = False : I41ProjN = 0
	EndIf
End Function

Function IndevU41Dress(r.Rooms)
End Function

;a body on the floor at a pivot (the dead D-class pose the other Indev rooms use)
Function U41Body.NPCs(r.Rooms, p%, yaw#)
	Local n.NPCs = CreateNPC(NPCtypeD, EntityX(p, True), EntityY(p, True) + 0.5, EntityZ(p, True))
	RotateEntity(n\Collider, 0, yaw, 0)
	n\State = 3
	SetNPCFrame(n, 19)
	n\IsDead = True
	Return n
End Function

Function UpdateIndevU41(e.Events)
	Local r.Rooms = e\room, n.NPCs, lx#, k%
	;the bodies and the gym's survivors are made once, the first time the room is near
	If e\EventState = 0 And r\dist < 12 Then
		e\EventState = 1
		Select r\RoomTemplate\Name
			Case "room2b43security"
				r\NPC[0] = U41Body(r, r\Objects[U41_SEC_DEAD1], 40)
			Case "room2b43dblock"
				r\NPC[0] = U41Body(r, r\Objects[U41_DBK_DEAD1], 120)
				r\NPC[1] = U41Body(r, r\Objects[U41_DBK_DEAD2], 300)
			Case "room2b43rec"
				e\EventState2 = Rand(1, 3)
				If e\EventState2 = 1 Then
					For k = 0 To 1
						n = CreateNPC(NPCtypeGuard, EntityX(r\Objects[U41_REC_GYM], True) + 0.6, EntityY(r\Objects[U41_REC_GYM], True) + 0.35, EntityZ(r\Objects[U41_REC_GYM], True) + k * 1.2 - 0.6)
						n\State = 9 : r\NPC[k] = n
						RotateEntity(n\Collider, 0, 270, 0)
					Next
				ElseIf e\EventState2 = 3 Then
					r\NPC[0] = U41Body(r, r\Objects[U41_REC_GYM], 10)
					PositionEntity(r\NPC[0]\Collider, EntityX(r\NPC[0]\Collider) - 0.8, EntityY(r\NPC[0]\Collider), EntityZ(r\NPC[0]\Collider) - 1.4)
					r\NPC[1] = U41Body(r, r\Objects[U41_REC_GYM], 200)
					PositionEntity(r\NPC[1]\Collider, EntityX(r\NPC[1]\Collider) + 0.5, EntityY(r\NPC[1]\Collider), EntityZ(r\NPC[1]\Collider) + 1.6)
				EndIf
		End Select
	EndIf
	If e\EventState2 = 1 And r\RoomTemplate\Name = "room2b43rec" Then
		U37Pin(r\NPC[0], r\Objects[U41_REC_GYM], -0.6, 0.35)
		U37Pin(r\NPC[1], r\Objects[U41_REC_GYM], 0.6, 0.35)
	EndIf
	If PlayerRoom <> r Then Return
	lx = U37LX(r)
	Select r\RoomTemplate\Name
		Case "room2b43staff"
			If IS10Press(r\Objects[U41_STF_PROJ], 2.4) Then
				I41ProjN = I41ProjN + 1
				If I41ProjN = 1 Then
					IS16Tell("The projector isn't plugged in. On the screen, a face made of static turns, slowly, to look at you.", 7)
				Else
					IS16Tell("The face on the screen mouths something. You read it twice to be sure: 'I SEE YOU TOO.'", 7)
					IndevStress = Min(100, IndevStress + 6)
				EndIf
			EndIf
		Case "room2b43medical"
			If IS10Press(r\Objects[U41_MED_HOOD], 1.6) Then IS16Tell("The fume hood is still running. Something in a beaker under it is bubbling without any heat.", 6)
			If IS10Press(r\Objects[U41_MED_XRAY], 2.0) Then IS16Tell("Three chest x-rays on the lightbox. You count the ribs on the third. Then you count them again. Twelve pairs is right. That one has twenty.", 7)
			If IS10Press(r\Objects[U41_MED_DISSECT], 1.8) Then IS16Tell("The dissection table has been wiped down in a hurry. The straps are still buckled - around nothing.", 6)
		Case "room2b43security"
			If IS10Press(r\Objects[U41_SEC_LOCKER], 1.8) And (Not I41Locker) Then
				I41Locker = True
				CameraShake = 3.0
				IndevStress = Min(100, IndevStress + 15)
				U41Body(r, r\Objects[U41_SEC_LOCKER], 180)
				IS16Tell("You pull the locker open and a guard falls out on top of you - dead, cold, wedged in there for hours. He was hiding.", 7)
			EndIf
		Case "room2b43rec"
			;the theater screen: rapid, blinding flashes
			If lx < -256 And Rand(3) = 1 Then LightFlash = Rnd(0.5, 1.8)
			If IS10Press(r\Objects[U41_REC_SCREEN], 3.0) Then IS16Tell("The projector booth is empty and the bulb is out. The screen goes on flashing.", 5)
			If lx > 400 And e\EventState3 = 0 Then
				e\EventState3 = 1
				Select e\EventState2
					Case 1 : IAxSay("Guard", "Stop right there! You came in through the east door? Go back and make sure it's shut - then we'll talk.", 7)
					Case 2 : IS16Tell("The gym is empty. Barricades of benches and mats, kicked aside. Blood on the court lines. Whoever was here left in a hurry.", 7)
					Default : IS16Tell("They didn't make it. The barricade is down, and something big went through it.", 6)
				End Select
			EndIf
	End Select
End Function
