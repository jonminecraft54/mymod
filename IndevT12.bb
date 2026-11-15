;=====================================================================
; SCP: Containment Breach - Indev: twelfth batch, one room from the reference photos
;
;   room2balconycells   HCZ  Balcony Cell Block. A double-height cell hall with a railed gallery up a stair on the
;                           west side. Red pendants over the pit. A cell log lies on the gallery desk.
;
;   IndevT12Data.bb is generated (Tools\roomkit\gen_b12.py): the T12_* constants, the FillRoom table and the
;   event list. This file holds the two things that table calls by name. No scripted behaviour is needed:
;   the log and supplies are items, and the stair and railing are part of the geometry.
;=====================================================================

Function IndevT12Dress(r.Rooms)
	;nothing the generated table cannot place: this room is finished by its geometry and items
End Function

Function UpdateIndevT12(e.Events)
	;no scripted behaviour in this batch (see the header)
End Function
