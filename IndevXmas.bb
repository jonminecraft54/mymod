;=====================================================================
; SCP: Containment Breach - Indev seasonal music
;
;   In December only, a distant old-fashioned instrumental Christmas tune
;   drifts through any of the office rooms:
;     room2offices, room2offices2, room2offices4,
;     room2poffices, room2poffices2,
;     room2newoffices2   (the Indev-Zone offices with SCP-005 / SCP-1471)
;
;   It's kept quiet - meant to sound like it's coming through the vents
;   from somewhere else in the facility, not out of a speaker in the room.
;   It fades in and out as the player enters and leaves the room, and it
;   stops the moment December ends.
;
;   The tune is streamed rather than loaded, so nothing sits in memory the
;   rest of the year. StreamSound_Strict / StopStream_Strict are the same
;   calls the game's own MusicCHN uses; custommode 2 (the default) makes
;   the stream loop.
;
;   Blitz's CurrentDate() returns strings like "15 Apr 2026", so the
;   month is Mid(str, 4, 3).
;=====================================================================

Global IndevXmasCHN%, IndevXmasVol#, IndevXmasIsDec%

Function IndevXmasReset()
	If IndevXmasCHN <> 0 Then StopStream_Strict(IndevXmasCHN)
	IndevXmasCHN = 0
	IndevXmasVol = 0
End Function

;true only in December
Function IndevXmasInDec%()
	Return (Mid(CurrentDate(), 4, 3) = "Dec")
End Function

;true when the given room is one of the office rooms
Function IndevXmasIsOfficeRoom%(r.Rooms)
	If r = Null Then Return False
	If r\RoomTemplate = Null Then Return False
	Local n$ = r\RoomTemplate\Name
	If n = "room2offices" Or n = "room2offices2" Or n = "room2offices4" Then Return True
	If n = "room2poffices" Or n = "room2poffices2" Then Return True
	If n = "room2newoffices2" Then Return True
	Return False
End Function

Function UpdateIndevXmas()
	;cache the month check: no point testing CurrentDate() every frame
	If IndevXmasIsDec = 0 Then
		If IndevXmasInDec() Then IndevXmasIsDec = 1 Else IndevXmasIsDec = 2
	EndIf
	If IndevXmasIsDec <> 1 Then
		IndevXmasVol = 0
		If IndevXmasCHN <> 0 Then
			StopStream_Strict(IndevXmasCHN)
			IndevXmasCHN = 0
		EndIf
		Return
	EndIf

	Local want# = 0
	If IndevXmasIsOfficeRoom(PlayerRoom) And KillTimer >= 0 Then want = 0.28

	;fade in / out
	IndevXmasVol = CurveValue(want, IndevXmasVol, 40.0)

	If IndevXmasVol < 0.01 Then
		If IndevXmasCHN <> 0 Then
			StopStream_Strict(IndevXmasCHN)
			IndevXmasCHN = 0
		EndIf
		Return
	EndIf

	;start the stream on first fade-in (custommode default 2 = looped, matching MusicCHN)
	If IndevXmasCHN = 0 Then
		IndevXmasCHN = StreamSound_Strict("SFX\Radio\ChristmasOn-Site Radio.ogg", 0.0)
	EndIf
	If IndevXmasCHN <> 0 And IndevXmasCHN <> -1 Then
		SetStreamVolume_Strict(IndevXmasCHN, IndevXmasVol * SFXVolume)
	EndIf
End Function
