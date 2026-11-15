;=====================================================================
; SCP: Containment Breach - Indev: SCP-914 refines ANY item
;
;   Refinement: improving something - breaking a raw substance down and making
;   it purer. Every item now has an outcome on every setting.
;
;   1. Data\refine914.ini (checked first, for every item):
;        [itemname]
;        rough = <item> | destroy | same
;        coarse = ...    1:1 = ...    fine = ...    very fine = ...
;      Several results can be listed with commas: one is picked at random.
;      A missing key falls through to the item's normal recipe.
;
;   2. The stock / Indev recipes in Use914 (unchanged).
;
;   3. Everything else (items that used to come out untouched):
;        Rough     - broken down to its raw substance: dust on the floor, item gone
;        Coarse    - stripped down: comes out "Worn", charge/uses halved
;        1:1       - reworked into another item of the same kind (same group), if any
;        Fine      - refined one grade: plain -> "Refined" -> "Pure"; charge/uses x1.5
;        Very Fine - straight to "Pure" (full charge) - but 1 in 5 is refined past the
;                    point of holding together and comes out as fine powder
;      Grades show in the item's name. A Pure item can't be refined further on Fine.
;=====================================================================

Const REFINE914_INI$ = "Data\refine914.ini"

;returns True if the ini had a recipe for this item/setting (the item has been handled)
Function IndevRefineFromIni%(item.Items, setting$, x#, y#, z#)
	If FileType(REFINE914_INI) <> 1 Then Return False
	Local res$ = GetINIString(REFINE914_INI, item\itemtemplate\name, setting, "")
	res = Trim(Lower(res))
	If res = "" Then Return False

	;pick one of a comma-separated list
	Local count% = 1, i%, pick%, cur$ = "", n% = 0
	For i = 1 To Len(res)
		If Mid(res, i, 1) = "," Then count = count + 1
	Next
	pick = Rand(1, count)
	For i = 1 To Len(res)
		If Mid(res, i, 1) = "," Then
			n = n + 1
			If n = pick Then Exit
			cur = ""
		Else
			cur = cur + Mid(res, i, 1)
		EndIf
	Next
	cur = Trim(cur)

	Select cur
		Case "destroy"
			IndevRefineDust(x, z, 200, 200, 190)
			RemoveItem(item)
		Case "same", ""
			PositionEntity(item\collider, x, y, z)
			ResetEntity(item\collider)
		Default
			;(an unknown item name in the ini would crash CreateItem: check first, and don't eat the item)
			Local t.ItemTemplates, known% = False, it2.Items
			For t = Each ItemTemplates
				If Lower(t\name) = cur Then known = True : Exit
			Next
			If known Then
				it2 = CreateItem(cur, x, y, z)
				RemoveItem(item)
			Else
				PositionEntity(item\collider, x, y, z)
				ResetEntity(item\collider)
			EndIf
	End Select
	Return True
End Function

;----------------------------------------------------------------- grades in saves
;The .cbsav format has no room for item names, so grades go in a small side file next to the save:
;  <save>.refine  =  Int count, then (Int item ID, Byte grade) pairs. Items keep their IDs across saves.

Function IndevRefineSave(savefile$)
	Local it.Items, n% = 0
	For it = Each Items
		If IndevRefineGrade(it) <> 0 Then n = n + 1
	Next
	Local path$ = savefile + ".refine"
	If n = 0 Then
		If FileType(path) = 1 Then DeleteFile(path)
		Return
	EndIf
	Local f% = WriteFile(path)
	If f = 0 Then Return
	WriteInt f, n
	For it = Each Items
		If IndevRefineGrade(it) <> 0 Then
			WriteInt f, it\ID
			WriteByte f, IndevRefineGrade(it) + 1 ;(-1..2 stored as 0..3)
		EndIf
	Next
	CloseFile f
End Function

Function IndevRefineLoad(savefile$)
	Local path$ = savefile + ".refine"
	If FileType(path) <> 1 Then Return
	Local f% = ReadFile(path)
	If f = 0 Then Return
	Local n% = ReadInt(f), i%, id%, grade%, it.Items
	For i = 1 To n
		If Eof(f) Then Exit
		id = ReadInt(f)
		grade = ReadByte(f) - 1
		For it = Each Items
			If it\ID = id Then IndevRefineSetGrade(it, grade) : Exit
		Next
	Next
	CloseFile f
End Function

Function IndevRefineDust(x#, z#, r%, g%, b%)
	Local d.Decals = CreateDecal(0, x, 8 * RoomScale + 0.005, z, 90, Rand(360), 0)
	d\Size = Rnd(0.10, 0.16)
	EntityColor(d\obj, r, g, b)
	ScaleSprite(d\obj, d\Size, d\Size)
End Function

;"Worn " / "Refined " / "Pure " prefix -> grade -1 / 1 / 2, and the bare name
Function IndevRefineGrade%(item.Items)
	If Left(item\displayname, 5) = "Pure " Then Return 2
	If Left(item\displayname, 8) = "Refined " Then Return 1
	If Left(item\displayname, 5) = "Worn " Then Return -1
	Return 0
End Function

Function IndevRefineSetGrade(item.Items, grade%)
	Local base$ = item\itemtemplate\displayname
	Select grade
		Case -1 item\displayname = "Worn " + base
		Case 1 item\displayname = "Refined " + base
		Case 2 item\displayname = "Pure " + base
		Default item\displayname = base
	End Select
End Function

;the fallback for items with no recipe of their own
Function IndevRefineAny(item.Items, setting$, x#, y#, z#)
	Local grade% = IndevRefineGrade(item)
	Local it2.Items, t.ItemTemplates, n%, pick%

	Select setting
		Case "rough"
			;back to raw substance
			IndevRefineDust(x, z, 150, 140, 130)
			RemoveItem(item)
			Return

		Case "coarse"
			IndevRefineSetGrade(item, -1)
			If item\state > 0 Then item\state = item\state * 0.5

		Case "1:1"
			;rework it into another item of the same kind
			If item\itemtemplate\group <> "" Then
				n = 0
				For t = Each ItemTemplates
					If t\group = item\itemtemplate\group And t\name <> item\itemtemplate\name Then n = n + 1
				Next
				If n > 0 Then
					pick = Rand(1, n) : n = 0
					For t = Each ItemTemplates
						If t\group = item\itemtemplate\group And t\name <> item\itemtemplate\name Then
							n = n + 1
							If n = pick Then
								it2 = CreateItem(t\name, x, y, z)
								RemoveItem(item)
								Return
							EndIf
						EndIf
					Next
				EndIf
			EndIf

		Case "fine"
			If grade < 2 Then IndevRefineSetGrade(item, Max(grade, 0) + 1)
			If item\state > 0 Then item\state = Min(item\state * 1.5, 100)

		Case "very fine"
			If Rand(5) = 1 Then
				;refined past the point of holding together
				IndevRefineDust(x, z, 245, 245, 240)
				RemoveItem(item)
				Return
			EndIf
			IndevRefineSetGrade(item, 2)
			If item\state > 0 Then item\state = 100
	End Select

	PositionEntity(item\collider, x, y, z)
	ResetEntity(item\collider)
End Function
