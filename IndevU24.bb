;=====================================================================
; SCP: Containment Breach - Indev: twenty-fourth batch, 25 SCPs
;
;   room2b24block1..4  six cells each; slot k holds the pivot of the block's k-th SCP (IndevU24Six).
;   room2b24store6h    Storage Room 6H, with a lift down to SCP-087's top landing (slot 0).
;
;   Every SCP is clicked (IS10Press, 2 m); what it does is in the generated IndevU24Table.bb (from
;   Tools\roomkit\scps_b24.py), and so is the message some of them give once when you first come near.
;   Once-flags per cell: "c0".."c5" (clicked before), "n0".."n5" (near message shown).
;   SCP texts are summaries of SCP Wiki articles (CC BY-SA 3.0). Idle rooms return at once.
;=====================================================================

Global Indev24Clicks%

Function IndevU24Dress(r.Rooms)
	If r\RoomTemplate\Name = "room2b24store6h" Then Return
	IndevScpDressList(r, IndevU24Six(r\RoomTemplate\Name)) ;real models for the SCPs that have one (IndevScpProps.bb)
End Function

;the SCPs of a room, in slot order, as "a|b|c|..."
Function IndevU24Six$(name$)
	Select name
		Case "room2b24block1" : Return "018|027|101|134|181|262"
		Case "room2b24block2" : Return "300|314|387|423|426|432"
		Case "room2b24block3" : Return "504|524|847|871|1230|1733"
		Case "room2b24block4" : Return "2030|2317|409|191|2399|1000"
		Case "room2b24store6h" : Return "087"
	End Select
	Return ""
End Function

Function UpdateIndevU24(e.Events)
	Local six$, k%, s%, n$
	If PlayerRoom <> e\room Then Return
	If e\room\RoomTemplate\Name = "room2b24store6h" Then
		;the lift owns slots 0 and 1 here, so SCP-087's pivot is its own slot
		IndevLiftTick(e) ;the lift down to SCP-087
		IndevU24Cell(e, "087", U24_S6H_S087)
		Return
	EndIf
	six = IndevU24Six(e\room\RoomTemplate\Name)
	IndevScpFiguresList(e, six) ;the SCPs that are people stand in their cells (IndevScpProps.bb)
	s = 0
	While six <> ""
		k = Instr(six, "|")
		If k = 0 Then
			n = six : six = ""
		Else
			n = Left(six, k - 1) : six = Mid(six, k + 1)
		EndIf
		IndevU24Cell(e, n, s)
		s = s + 1
	Wend
End Function

Function IndevU24Cell(e.Events, n$, slot%)
	Local p% = e\room\Objects[slot], msg$, isnew%
	If EntityDistance(Collider, p) < 2.5 And Abs(EntityY(Collider) - EntityY(p, True)) < 1.5 Then
		If Not IAxFlag(e, "n" + slot) Then
			IAxSetFlag(e, "n" + slot)
			msg = IndevU24Near(n)
			If msg <> "" Then IS16Tell(msg, 6)
		EndIf
	EndIf
	If IS10Press(p, 2.0) Then
		Indev24Clicks = Indev24Clicks + 1
		isnew = Not IAxFlag(e, "c" + slot)
		IAxSetFlag(e, "c" + slot)
		IndevU24Click(n, p, isnew)
		If IndevStress < 0 Then IndevStress = 0
		If IndevStress > 100 Then IndevStress = 100
		If Injuries < 0 Then Injuries = 0
	EndIf
End Function
