;=====================================================================
; SCP: Containment Breach - Indev: state that the save format has no room for, kept in <save>.indev
;
;   Written next to the save by SaveGame and read back by LoadGame / LoadGameQuick (the same way the SCP-914
;   item grades are, Indev914Refine.bb). Without it these would reset or re-roll on every load:
;     SCP-513    whether this playthrough hears the bell, when, and whether it already has
;     memory     the Alzheimer's meter, its stage, whether SCP-500 cured it, the medicine timer
;     SCP-113    how many times it has changed you, its cooldown, and your sex now (the HUD icon)
;     SCP-2107   cans drunk, and how long until / how much haunting is left (version 2)
;     SCP-983    whether today is your birthday, the years it took, the luminescent candy's timer (version 3)
;     batch 29   SCP-120's configuration, an SCP-867 seed or its agony, whether SCP-820-JP is out, how long you
;                have looked at it (version 4)
;   A save made before this file existed has no .indev: the bell is rolled once, as for a new game, and the
;   next save keeps that roll; the rest keep their new-game values.
;=====================================================================

Global IndevFemale%           ;True after an odd number of SCP-113 changes (the Class-D starts male)
Global IndevGenderShown%      ;True once SCP-113 has changed you at least once: the HUD icon shows from then on
Global GenderIconM% = 0, GenderIconF% = 0

Const INDEV_SIDE_VERSION% = 17

Function IndevSideSave(savefile$)
	Local f% = WriteFile(savefile + ".indev")
	If f = 0 Then Return
	WriteInt f, INDEV_SIDE_VERSION
	WriteByte f, Indev513Active
	WriteFloat f, Indev513Timer
	WriteByte f, Indev513Rings
	WriteFloat f, IndevMemory
	WriteByte f, IndevMemoryCured
	WriteFloat f, IndevMemorySlow
	WriteInt f, I113Uses
	WriteFloat f, I113LastUse
	WriteByte f, IndevFemale
	WriteByte f, IndevGenderShown
	;version 2: SCP-2107
	WriteInt f, I2107Cans
	WriteFloat f, I2107Delay
	WriteFloat f, I2107Time
	;version 3: SCP-983
	WriteByte f, I983Birthday
	WriteFloat f, I983Age
	WriteFloat f, I983Glow
	;version 4: batch 29
	WriteByte f, I120Dest
	WriteFloat f, I867Seed
	WriteFloat f, I867Pain
	WriteByte f, I820Taken
	WriteFloat f, I820Look
	;version 5: Site-42
	WriteByte f, I4427Count
	WriteByte f, I4427Trait
	WriteFloat f, I4427Timer
	WriteByte f, I4433Stage
	WriteFloat f, I4433Pull
	;version 6: SCP-467 and the five items
	WriteFloat f, I467Cool
	WriteByte f, I178On
	WriteByte f, I198Bond
	WriteFloat f, I198Hunger
	WriteFloat f, I198Starve
	WriteString f, I198Fluid
	WriteByte f, I207On
	WriteFloat f, I207T
	WriteByte f, I1079Left
	WriteByte f, I1650Ang
	;version 7: Gate V
	WriteByte f, I32Open
	WriteByte f, I32Alarm
	WriteByte f, I32MTF
	WriteByte f, I32Blown
	;version 8: the Gate V lockdown countdown
	WriteFloat f, I32Lock
	;version 9: batch 33
	WriteFloat f, I1007Age
	WriteByte f, I1007Dead
	WriteByte f, I232Bat
	WriteInt f, I762Flips
	WriteByte f, IL043Line
	WriteByte f, I2394Woke
	WriteByte f, I7042Uses
	WriteByte f, I865Shots
	WriteByte f, I3938Rides
	WriteByte f, I696Press
	WriteFloat f, I4612Akiva
	;version 10: batch 34
	WriteFloat f, I34Sprout
	WriteByte f, I34Photo
	WriteFloat f, I34PhotoInj
	WriteFloat f, I34Fearless
	WriteByte f, I34Caps
	WriteByte f, I34Clean
	;version 11: batch 35
	WriteByte f, I1779Fed
	WriteByte f, I35Hat
	;version 12: batch 36
	WriteByte f, I36GumLeft
	WriteByte f, I1916Next
	WriteFloat f, I36Cotton
	WriteByte f, I36Scratch
	;version 13: batch 37
	WriteByte f, I37Uses
	WriteByte f, I37Recipe
	WriteByte f, I37Codes
	WriteByte f, I37Knocks
	WriteByte f, I37Vent
	;version 14: batch 38
	WriteFloat f, I38Fed
	WriteByte f, I38Rations
	WriteByte f, I38Taken
	;version 15: batch 39
	WriteByte f, I39Compat
	WriteByte f, I39Calc
	WriteByte f, I39RobotN
	;version 16: batch 40
	WriteByte f, I40Tape
	WriteByte f, I40Mute
	WriteByte f, I40BirdN
	WriteByte f, I40DoorN
	;version 17: batch 42
	WriteByte f, I42Ear
	WriteByte f, I42Flares
	WriteByte f, I42FridgeN
	CloseFile f
End Function

Function IndevSideLoad(savefile$)
	Local path$ = savefile + ".indev", f%, v%
	If FileType(path) <> 1 Then
		;a save from before this file existed: roll SCP-513 once, as a new game does. The next save writes the
		;roll into the .indev file, so it is never rolled again for this playthrough.
		Indev513Active = (Rand(100) <= 35)
		Indev513Timer = 70*60*Rnd(8,25)
		Indev513Rings = 0
		Return
	EndIf
	f = ReadFile(path)
	If f = 0 Then Return
	v = ReadInt(f)
	Indev513Active = ReadByte(f)
	Indev513Timer = ReadFloat(f)
	Indev513Rings = ReadByte(f)
	IndevMemory = ReadFloat(f)
	IndevMemoryShown = IndevMemory
	IndevMemoryCured = ReadByte(f)
	IndevMemorySlow = ReadFloat(f)
	IndevMemoryStage = IndevMemoryStageOf(IndevMemory)
	I113Uses = ReadInt(f)
	I113LastUse = ReadFloat(f)
	IndevFemale = ReadByte(f)
	IndevGenderShown = ReadByte(f)
	If v >= 2 Then
		I2107Cans = ReadInt(f)
		I2107Delay = ReadFloat(f)
		I2107Time = ReadFloat(f)
		I2107Next = 70 * 5
	EndIf
	If v >= 3 Then
		I983Birthday = ReadByte(f)
		I983Age = ReadFloat(f)
		I983Glow = ReadFloat(f)
	EndIf
	If v >= 4 Then
		I120Dest = ReadByte(f)
		I867Seed = ReadFloat(f)
		I867Pain = ReadFloat(f)
		I820Taken = ReadByte(f)
		I820Look = ReadFloat(f)
	EndIf
	If I120Dest < 1 Or I120Dest > 11 Then I120Dest = Rand(1, 11)
	If v >= 5 Then
		I4427Count = ReadByte(f)
		I4427Trait = ReadByte(f)
		I4427Timer = ReadFloat(f)
		I4433Stage = ReadByte(f)
		I4433Pull = ReadFloat(f)
	EndIf
	If I4427Count = 0 Then I4427Count = 44 ;a save from before Site-42: 44 people have walked through it
	If v >= 6 Then
		I467Cool = ReadFloat(f)
		I178On = ReadByte(f)
		I198Bond = ReadByte(f)
		I198Hunger = ReadFloat(f)
		I198Starve = ReadFloat(f)
		I198Fluid = ReadString(f)
		I207On = ReadByte(f)
		I207T = ReadFloat(f)
		I1079Left = ReadByte(f)
		I1650Ang = ReadByte(f)
	Else
		I1079Left = 8
	EndIf
	If v >= 7 Then
		I32Open = ReadByte(f)
		I32Alarm = ReadByte(f)
		I32MTF = ReadByte(f)
		I32Blown = ReadByte(f)
	EndIf
	If v >= 8 Then I32Lock = ReadFloat(f)
	If v >= 9 Then
		I1007Age = ReadFloat(f)
		I1007Dead = ReadByte(f)
		I232Bat = ReadByte(f)
		I762Flips = ReadInt(f)
		IL043Line = ReadByte(f)
		I2394Woke = ReadByte(f)
		I7042Uses = ReadByte(f)
		I865Shots = ReadByte(f)
		I3938Rides = ReadByte(f)
		I696Press = ReadByte(f)
		I4612Akiva = ReadFloat(f)
	EndIf
	If v >= 10 Then
		I34Sprout = ReadFloat(f)
		I34Photo = ReadByte(f)
		I34PhotoInj = ReadFloat(f)
		I34Fearless = ReadFloat(f)
		I34Caps = ReadByte(f)
		I34Clean = ReadByte(f)
	EndIf
	If v >= 11 Then
		I1779Fed = ReadByte(f)
		I35Hat = ReadByte(f)
	EndIf
	If v >= 12 Then
		I36GumLeft = ReadByte(f)
		I1916Next = ReadByte(f)
		I36Cotton = ReadFloat(f)
		I36Scratch = ReadByte(f)
	Else
		I36GumLeft = 5 : I1916Next = 1
	EndIf
	If v >= 13 Then
		I37Uses = ReadByte(f)
		I37Recipe = ReadByte(f)
		I37Codes = ReadByte(f)
		I37Knocks = ReadByte(f)
		I37Vent = ReadByte(f)
	EndIf
	If v >= 14 Then
		I38Fed = ReadFloat(f)
		I38Rations = ReadByte(f)
		I38Taken = ReadByte(f)
	EndIf
	If v >= 15 Then
		I39Compat = ReadByte(f)
		I39Calc = ReadByte(f)
		I39RobotN = ReadByte(f)
	EndIf
	If v >= 16 Then
		I40Tape = ReadByte(f)
		I40Mute = ReadByte(f)
		I40BirdN = ReadByte(f)
		I40DoorN = ReadByte(f)
	EndIf
	If v >= 17 Then
		I42Ear = ReadByte(f)
		I42Flares = ReadByte(f)
		I42FridgeN = ReadByte(f)
	EndIf
	If I1007Age <= 0 And (Not I1007Dead) Then I1007Age = 52 ;a save from before batch 33
	If I4612Akiva < 214 Then I4612Akiva = 214
	CloseFile f
End Function

;SCP-113 finished a change (Indev113.bb, and the stone in the batch-20 cell)
Function IndevGenderSwap()
	IndevFemale = Not IndevFemale
	IndevGenderShown = True
End Function

;drawn from DrawHUD, one row above the memory meter, only once SCP-113 has changed you
Function DrawIndevGenderIcon(x%)
	Local y%, img%
	If Not IndevGenderShown Then Return
	If GenderIconM = 0 Then GenderIconM = LoadImageHUDScaled("GFX\gendermale.png")
	If GenderIconF = 0 Then GenderIconF = LoadImageHUDScaled("GFX\genderfemale.png")
	y = HUDEndY - 215 * HUDScale
	Color 0, 0, 0
	Rect(x - 50 * HUDScale, y, 30 * HUDScale, 30 * HUDScale)
	Color 255, 255, 255
	Rect(x - 50 * HUDScale - 1, y - 1, 30 * HUDScale + 2, 30 * HUDScale + 2, False)
	If IndevFemale Then img = GenderIconF Else img = GenderIconM
	DrawImage img, x - 50 * HUDScale, y
End Function
