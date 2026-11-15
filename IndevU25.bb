;=====================================================================
; SCP: Containment Breach - Indev: twenty-fifth batch, 18 SCPs and the office suite
;
;   room2b25block1..3  six cells each; slot k holds the pivot of the block's k-th SCP (IndevU25Six). Click an
;                      SCP for its effect (IndevU25Click). Each SCP also has a low-frequency event: while you are
;                      within 6 m of it, every few minutes, a sound and a line (IndevU25Tick). 18 events.
;   room2b25offices    a researcher in the first office who faces you and talks; the HOIST panel in the control
;                      room; the intercom pages every 2 to 4 minutes while you are in the suite. 2 events.
;
;   The click and tick tables are generated (IndevU25Table.bb, from Tools\roomkit\scps_b25.py). Per-cell
;   countdowns live in Indev25St(block, cell). SCP texts summarise SCP Wiki articles (CC BY-SA 3.0).
;=====================================================================

Global Indev25Clicks%, Indev25Ticks%, Indev25Pages%
Dim Indev25St#(3, 5)

Function IndevU25Dress(r.Rooms)
	If r\RoomTemplate\Name = "room2b25offices" Then Return
	IndevScpDressList(r, IndevU25Six(r\RoomTemplate\Name)) ;real models for the SCPs that have one (IndevScpProps.bb)
End Function

Function IndevU25Six$(name$)
	Select name
		Case "room2b25block1" : Return "115|124|136|160|239|250"
		Case "room2b25block2" : Return "263|303|310|342|378|447"
		Case "room2b25block3" : Return "488|527|689|668|2662|040"
	End Select
	Return ""
End Function

Function UpdateIndevU25(e.Events)
	Local six$, k%, s%, n$, b%
	If PlayerRoom <> e\room Then Return
	If e\room\RoomTemplate\Name = "room2b25offices" Then
		UpdateU25Offices(e)
		Return
	EndIf
	six = IndevU25Six(e\room\RoomTemplate\Name)
	If six = "" Then Return
	IndevScpFiguresList(e, six) ;the SCPs that are people stand in their cells (IndevScpProps.bb)
	b = Int(Right(e\room\RoomTemplate\Name, 1)) - 1
	s = 0
	While six <> ""
		k = Instr(six, "|")
		If k = 0 Then
			n = six : six = ""
		Else
			n = Left(six, k - 1) : six = Mid(six, k + 1)
		EndIf
		IndevU25Cell(e, n, s, b)
		s = s + 1
	Wend
End Function

Function IndevU25Cell(e.Events, n$, slot%, b%)
	Local p% = e\room\Objects[slot], isnew%
	;the event: counts down only while you are near this SCP
	If EntityDistance(Collider, p) < 6.0 Then
		If Indev25St(b, slot) <= 0 Then Indev25St(b, slot) = 70 * Rand(IndevU25TickMin(n), IndevU25TickMax(n)) / 2
		Indev25St(b, slot) = Indev25St(b, slot) - FPSfactor
		If Indev25St(b, slot) <= 0 Then
			Indev25Ticks = Indev25Ticks + 1
			IndevU25Tick(n, p)
			Indev25St(b, slot) = 70 * Rand(IndevU25TickMin(n), IndevU25TickMax(n))
		EndIf
	EndIf
	If IS10Press(p, 2.0) Then
		Indev25Clicks = Indev25Clicks + 1
		isnew = Not IAxFlag(e, "c" + slot)
		IAxSetFlag(e, "c" + slot)
		IndevU25Click(n, p, isnew)
	EndIf
	If IndevStress < 0 Then IndevStress = 0
	If IndevStress > 100 Then IndevStress = 100
	If Injuries < 0 Then Injuries = 0
End Function

;the office suite. Flag n: the researcher is made. EventState: frames to the next page on the intercom.
Function UpdateU25Offices(e.Events)
	Local r.Rooms = e\room, n.NPCs, d#
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, U25_OFS_RESEARCHER, 90)
		IAxSkin(r\NPC[0], "GFX\npcs\indev_archivist.jpg")
		e\EventState = 70 * Rand(30, 60)
	EndIf
	n = r\NPC[0]
	If n <> Null Then
		d = EntityDistance(n\Collider, Collider)
		If d < 4.0 Then IAxFace(n, Collider)
		If d < 2.2 And MsgTimer <= 0 And Rand(500) = 1 Then
			Select Rand(4)
				Case 1 : IAxSay("Researcher", "Block two keeps paging me about the lamp. The lamp is fine. The lamp is always fine.", 6)
				Case 2 : IAxSay("Researcher", "If you are going into block three, do not look away from the dark corner. I mean it.", 6)
				Case 3 : IAxSay("Researcher", "Mr. Fish asked for a name tag again. Could you make him one? He likes 'Gerald'.", 6)
				Case 4 : IAxSay("Researcher", "The batteries are in the break room. Take one. Everyone else has.", 5)
			End Select
		EndIf
	EndIf
	If IS10Press(r\Objects[U25_OFS_PANEL], 2.0) Then
		IS10Sound("SFX\Indev\buzzer.wav", r\Objects[U25_OFS_PANEL], 6.0, 0.8)
		IS16Tell("HOIST: the motor turns over. DOOR: the light stays red. The panel says: SUPERVISOR REQUIRED.", 6)
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		e\EventState = 70 * Rand(120, 240)
		Indev25Pages = Indev25Pages + 1
		IS10Sound("SFX\Indev\page.wav", r\Objects[U25_OFS_SPEAKER], 20.0, 0.8)
		If MsgTimer <= 0 Then
			Select Rand(4)
				Case 1 : IS16Tell("Intercom: 'Containment check, block one, cell four. Bring a coat.'", 6)
				Case 2 : IS16Tell("Intercom: 'Would the owner of a toy dump truck please collect it from the canteen.'", 6)
				Case 3 : IS16Tell("Intercom: 'Reminder: the knife in block three stays in its case. Thank you.'", 6)
				Case 4 : IS16Tell("Intercom: 'Dr. ... please report to ... ' The rest is static.", 6)
			End Select
		EndIf
	EndIf
End Function
