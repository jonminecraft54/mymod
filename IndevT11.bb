;=====================================================================
; SCP: Containment Breach - Indev: eleventh batch, three rooms from the reference photos
;
;   room2hoistoffice   LCZ  Hoist Office. Filing cabinets, a monitor wall and a HOIST / DOOR panel. A keycard and
;                           an operator log on the desk.
;   room2shutterhall   HCZ  Shutter Hall. A long corridor with four grey containment shutters and hanging red lamps.
;                           A closure log lies on the floor in front of shutter 4.
;   room2machinecorr   LCZ  Machine Corridor. A corridor with a glass window onto a machine alcove. A service memo
;                           lies on the machine top.
;
;   IndevT11Data.bb is generated (Tools\roomkit\gen_b11.py): the T11_* constants, the FillRoom table and the
;   event list. This file holds the two things that table calls by name. No scripted behaviour is needed:
;   the keycard, notes and supplies are items, and the shutters are part of the geometry.
;=====================================================================

Function IndevT11Dress(r.Rooms)
	;nothing the generated table cannot place: these rooms are finished by their geometry and items
End Function

Function UpdateIndevT11(e.Events)
	;no scripted behaviour in this batch (see the header)
End Function
