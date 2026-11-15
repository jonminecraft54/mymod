;=====================================================================
; SCP: Containment Breach - Indev: fifteenth batch, the usable items of the thirteenth batch
;
;   cookie377    eat it: a fortune. Some are kind, some are not, and the box always has another one
;   camera978    take a photograph of yourself: it shows what you want to be doing. It is not used up
;   knife3041    use it: a dream. Carry it for two minutes and the dream comes back on its own
;   sweater1337  put it on: you feel the urge to take it to the grave. It leaves your hands
;
;   Called from DrawGUI (the item-use list) and from the main loop (IndevUsableTick). The items themselves are
;   in Data\items.ini and the rooms of IndevU13Data.bb.
;=====================================================================

Global Indev15KnifeT#      ;frames the knife has been carried, for the dream
Global Indev15Fortune%     ;the last fortune given, so two in a row do not repeat

Function IndevUseU15(it.Items)
	Select it\itemtemplate\name
		Case "cookie377"
			;the fortune: the same kind of thing every time, as written for the eater
			Local f% = Rand(0, 5)
			If f = Indev15Fortune Then f = (f + 1) Mod 6
			Indev15Fortune = f
			Select f
				Case 0
					Msg = "The fortune reads: Someone will be glad you came in today."
					Stamina = 100
				Case 1
					Msg = "The fortune reads: You will sleep well, and dream of a door that opens."
					Injuries = Max(0, Injuries - 0.5)
				Case 2
					Msg = "The fortune reads: The stairs you took for the lift will be the ones you remember."
				Case 3
					Msg = "The fortune reads: You will take the wrong door, and be pleased with it."
					IndevStress = Min(100, IndevStress + 10)
				Case 4
					Msg = "The fortune reads: Something you were told to forget is sitting in the room with you."
					IndevStress = Min(100, IndevStress + 20)
				Case 5
					Msg = "The fortune reads: It is not a good day to ask for it back."
					IndevStress = Min(100, IndevStress + 15)
			End Select
			MsgTimer = 70 * 8
			RemoveItem(it)
			SelectedItem = Null
		Case "camera978"
			;the photograph: what you want to be doing, which is never what you were doing
			Local k% = Rand(0, 4)
			Select k
				Case 0
					Msg = "The photograph shows you asleep in a bed you have never seen."
				Case 1
					Msg = "The photograph shows you outside, with the sun on your face, not running."
				Case 2
					Msg = "The photograph shows you eating something hot, alone, and not sorry."
				Case 3
					Msg = "The photograph shows you walking out of the gate, with nobody watching."
				Case 4
					Msg = "The photograph shows you at the window of a house, waiting for a child to come home."
			End Select
			MsgTimer = 70 * 8
			Stamina = 100
			IndevStress = Max(0, IndevStress - 10)
			SelectedItem = Null
		Case "knife3041"
			Msg = "You dream of a stranger's heart, in your hand, in the place you first picked the knife up."
			MsgTimer = 70 * 8
			IndevStress = Min(100, IndevStress + 15)
			SelectedItem = Null
		Case "sweater1337"
			Msg = "The sweater is warm, and you are very sure it is not yours. You let go of it, or it lets go of you."
			MsgTimer = 70 * 8
			IndevStress = Min(100, IndevStress + 20)
			RemoveItem(it)
			SelectedItem = Null
	End Select
End Function

;the knife's dream comes on by itself after two minutes in the inventory (called every frame of the game)
Function IndevUsableTick()
	If IndevHasItem("knife3041") Then
		Indev15KnifeT = Indev15KnifeT + FPSfactor
		If Indev15KnifeT > 70 * 120 Then
			Indev15KnifeT = 0
			Msg = "Something from the knife's dream stays with you: a face you do not know, very close."
			MsgTimer = 70 * 8
			IndevStress = Min(100, IndevStress + 15)
		EndIf
	Else
		Indev15KnifeT = 0
	EndIf
End Function
