;=====================================================================
; SCP: Containment Breach - Indev main menu
;
;   The menu keeps the stock button layout (so every sub-tab still lines
;   up) and adds, on top of the new GFX\menu\indev_back.jpg background:
;     - a "FACILITY LOG" terminal panel on the front page that types out
;       what's new in this build, one entry at a time
;     - the build tag in the bottom-left corner
;=====================================================================

Const INDEV_BUILD$ = "Indev v0.1"
Const INDEV_LOGS% = 16

Global IndevMenuLog$[INDEV_LOGS]
Global IndevMenuLogI%, IndevMenuLogChars#, IndevMenuLogHold#, IndevMenuInit%

Function IndevMenuInitLog()
	IndevMenuLog[0] = "ROSTER REDUCED. 173, 106, 079, 895, 914, 513, 990 REMAIN ACTIVE."
	IndevMenuLog[1] = "SCP-693 RECOVERED: FOUR STRING DOLLS. DO NOT FEED THEM HAIR."
	IndevMenuLog[2] = "SCP-113 LOGGED IN STORAGE. HANDLE WITH GLOVES ONLY."
	IndevMenuLog[3] = "MJOLNIR TYPE 1 ARMOUR ISSUED TO STORAGE ROOM 2S."
	IndevMenuLog[4] = "SCP-202 WATCH NEEDLE POINTS AT THE NEAREST ANOMALY."
	IndevMenuLog[5] = "SCP-330: TAKE ONLY TWO. PLEASE."
	IndevMenuLog[6] = "SCP-993 BROADCAST DETECTED IN OFFICES. LOOK AWAY."
	IndevMenuLog[7] = "SCP-718 CONTAINED IN THE PROTOTYPE ROOM. IT IS WATCHING."
	IndevMenuLog[8] = "CF-1 COGNITIVE FILTER GLASSES NOW STANDARD ISSUE."
	IndevMenuLog[9] = "CONDITION METERS ONLINE: HEALTH, RADIATION, INFECTION, MEMETICS."
	IndevMenuLog[10] = "STRESS MONITORING ENABLED FOR ALL CLASS-D PERSONNEL."
	IndevMenuLog[11] = "SCP-914 DOOR NOW KEYPAD LOCKED. CODE KEPT IN THE CLOSETS."
	IndevMenuLog[12] = "FACILITY LAYOUT REGENERATED. SOME DOORS WILL NOT OPEN."
	IndevMenuLog[13] = "SCP-122 NIGHT LIGHT INSTALLED IN THE MEDICAL BAY."
	IndevMenuLog[14] = "NEW PILL SCPs IN CIRCULATION. READ THE LABEL."
	IndevMenuLog[15] = "SCP-079 HAS ACCESS TO THE INTERCOM. DON'T TRUST IT."
	IndevMenuLogI = Rand(0, INDEV_LOGS - 1) : IndevMenuLogChars = 0 : IndevMenuLogHold = 0
	IndevMenuInit = True
End Function

;replaces the stock background + logo strip (called at the top of UpdateMainMenu)
Function DrawIndevMenuBack()
	If Not IndevMenuInit Then IndevMenuInitLog()
	DrawImage(MenuBack, 0, 0)

	;(the build tag is drawn by the stock version text in Menu.bb)
End Function

;the "FACILITY LOG" panel, front page only
Function DrawIndevMenuLog()
	Local x% = 800 * MenuScale, y% = 430 * MenuScale
	Local w% = Min(440 * MenuScale, GraphicWidth - x - 20 * MenuScale), h% = 150 * MenuScale
	If w < 200 * MenuScale Then Return

	DrawFrame(x, y, w, h)
	SetFont Font1
	Color 214, 150, 40
	Text(x + 14 * MenuScale, y + 12 * MenuScale, "FACILITY LOG")
	Color 90, 90, 90
	Text(x + w - 14 * MenuScale - StringWidth("SITE-19"), y + 12 * MenuScale, "SITE-19")
	Color 214, 150, 40
	Rect(x + 14 * MenuScale, y + 34 * MenuScale, w - 28 * MenuScale, 1 * MenuScale)

	;type the current entry out, hold it, then move on
	Local entry$ = IndevMenuLog[IndevMenuLogI]
	If IndevMenuLogChars < Len(entry) Then
		IndevMenuLogChars = Min(Len(entry), IndevMenuLogChars + FPSfactor * 0.6)
	Else
		IndevMenuLogHold = IndevMenuLogHold + FPSfactor
		If IndevMenuLogHold > 70 * 4 Then
			IndevMenuLogHold = 0 : IndevMenuLogChars = 0
			IndevMenuLogI = (IndevMenuLogI + 1) Mod INDEV_LOGS
		EndIf
	EndIf
	Local shown$ = "> " + Left(entry, Int(IndevMenuLogChars))
	If (MilliSecs() Mod 800) < 400 Then shown = shown + "_"
	Color 210, 210, 210
	RowText(shown, x + 14 * MenuScale, y + 48 * MenuScale, w - 28 * MenuScale, h - 60 * MenuScale)

	;the previous entry, dimmed
	Local prev% = (IndevMenuLogI + INDEV_LOGS - 1) Mod INDEV_LOGS
	Color 80, 80, 80
	RowText(IndevMenuLog[prev], x + 14 * MenuScale, y + 105 * MenuScale, w - 28 * MenuScale, 40 * MenuScale)
End Function
