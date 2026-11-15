;=====================================================================
; SCP: Containment Breach - Indev: tenth batch, three rooms from the reference photos
;
;   room2researchoffice  LCZ  Research Office. Filing cabinets along the back wall, a desk under a pendant
;                             lamp. A keycard and a note on the desk: the team left after the samples went
;                             to Lab 4 and nobody signed them back in.
;   room2medexam         LCZ  Medical Examination. A steel table, toilet and basin, a dead monitor. A patient
;                             record, first aid and a syringe on the table.
;   room2liftlobby       HCZ  Lift Lobby. A round pillar in the hub. The lift on its west side goes down to a
;                             basement hall, where the maintenance log lies on the bench.
;
;   IndevT10Data.bb is generated (Tools\roomkit\gen_b10.py): the T10_* constants, the FillRoom table and the
;   event list. This file holds the two things that table calls by name. No scripted behaviour is needed:
;   the keycard, notes and supplies are items, and the lift is the generic IAxElevator.
;=====================================================================

Function IndevT10Dress(r.Rooms)
	;nothing the generated table cannot place: these rooms are finished by their geometry and items
End Function

Function UpdateIndevT10(e.Events)
	;no scripted behaviour in this batch (see the header)
End Function
