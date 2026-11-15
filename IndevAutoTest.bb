;=====================================================================
; SCP: Containment Breach - Indev: unattended room test
;
;   Game.exe -roomtest -nolauncher -window [-testseed <seed>] [-testlist <file>] [-testms <n>]
;
;   Starts a new game straight from the menu, then visits rooms one by one, lets each settle (-testms, 1500 ms
;   by default), saves the frame as RoomTest\<nnn>_<room>.bmp and writes RoomTest\log.txt. Every log line is
;   flushed to disk, so after a crash the last VISIT line names the room the game was in. The game quits by
;   itself at the end.
;
;   -testlist: a text file, one view per line:   <room template name> [ex ey ez lx ly lz]
;              the six numbers are room units (as in Tools\roomkit): where the player stands and the point
;              looked at. The player is dropped from ey and settles at standing height.
;              Without a list every placed room that has "set room" in rooms.ini is visited at its centre.
;
;   The log also lists, for every "set room" template, whether the map generator found a slot for it
;   (PLACED / MISSING), and the frame rate measured in each room with vsync and the frame limiter off.
;
;   While the test runs the mouse is left alone, sound is muted and the player cannot be hurt.
;=====================================================================

;counters of the seventeenth batch's events (IndevU17.bb), written to the log so a test can count them
Global Indev17Flicks%, Indev17Flips%, Indev17Rings%, Indev17Steps%
;counters of The Hollowcrest's events (IndevU18.bb)
Global Indev18Flips%, Indev18Rings%, Indev18Clicks%, Indev18Echoes%, Indev18Panel%
;the bug-fix checks: frames a lift moved, frames its moving sound played (IndevS08.bb); SCP-173 in the silo
Global IndevLiftMove%, IndevLiftSnd%, IndevT173Start#, IndevT173Min#

Global IndevTestOn% = HasCLIFlag("roomtest")
Global IndevTestState%                      ;0 = not started, 1 = running, 2 = finished
Global IndevTestMs% = 1500, IndevTestT0%, IndevTestT10%, IndevTestFrameN%, IndevTestShots%
Global IndevTestYaw#, IndevTestPitch#
Global IndevTestCur.IndevTestView

Type IndevTestView
	Field room$
	Field has%                              ;True: stand at e, look at l; False: the room's centre
	Field ex#, ey#, ez#, lx#, ly#, lz#
End Type

Function IndevTestLog(txt$)
	Local path$ = "RoomTest\log.txt", f%
	If FileType(path) = 1 Then
		f = OpenFile(path)
		If f <> 0 Then SeekFile(f, FileSize(path))
	Else
		f = WriteFile(path)
	EndIf
	If f = 0 Then Return
	WriteLine(f, txt)
	CloseFile(f)
End Function

;the n-th word of a line (words are separated by spaces or tabs); "" when there is none
Function IndevTestTok$(l$, n%)
	Local i%, c$, cur$ = "", k% = 1
	l = Replace(l, Chr(9), " ")
	For i = 1 To Len(l) + 1
		If i <= Len(l) Then c = Mid(l, i, 1) Else c = " "
		If c = " " Then
			If cur <> "" Then
				If k = n Then Return cur
				k = k + 1 : cur = ""
			EndIf
		Else
			cur = cur + c
		EndIf
	Next
	Return ""
End Function

;called from the main menu instead of UpdateMainMenu(): the same steps as the START button
Function IndevTestStart()
	Local rt.RoomTemplates, r.Rooms, v.IndevTestView, n%, f%, l$, list$
	IndevTestState = 1
	If FileType("RoomTest") <> 2 Then CreateDir("RoomTest")
	If FileType("RoomTest\log.txt") = 1 Then DeleteFile("RoomTest\log.txt")
	IndevTestMs = GetCLIInt("testms", 1500)
	Vsync = False : Framelimit = 0
	MusicVolume = 0.0 : SFXVolume = 0.0
	IntroEnabled = False
	TimerStopped = True
	CurrSave = "roomtest"
	If UseNumericSeeds Then
		RandomSeedNumeric = GetCLIInt("testseed", 4666)
	Else
		RandomSeed = GetCLIString("testseed", "roomtest")
	EndIf
	SeedRnd GetRandomSeed()
	IndevTestLog("START seed=" + GetSeedString(False))
	Local pt% = MilliSecs()
	IndevTestLog("PROF boot-to-menu " + (pt - IndevBootMs))
	LoadEntities()
	IndevTestLog("PROF LoadEntities " + (MilliSecs() - pt)) : pt = MilliSecs()
	LoadAllSounds()
	IndevTestLog("PROF LoadAllSounds " + (MilliSecs() - pt)) : pt = MilliSecs()
	InitRoomTemplates()
	IndevTestLog("PROF InitRoomTemplates " + (MilliSecs() - pt)) : pt = MilliSecs()
	InitNewGame()
	IndevTestLog("PROF InitNewGame " + (MilliSecs() - pt) + " (room meshes " + IndevProfMesh + " ms for " + IndevProfMeshN + ", FillRoom " + IndevProfFill + " ms, new textures " + IndevProfTex + " ms for " + IndevProfTexN + ")")
	MainMenuOpen = False
	FlushKeys()
	FlushMouse()
	GodMode = True : NoTarget = True : InfiniteStamina = True
	IndevTestLog("MAP ready")
	;-testmemory <0-100>: set the Alzheimer's meter, with the next symptom two seconds away (IndevMemory.bb)
	If GetCLIInt("testmemory", -1) >= 0 Then IndevMemory = GetCLIInt("testmemory", 0) : IndevMemoryNext = 140
	;-testsave: a real save and quick-load round trip of the state kept in <save>.indev, then an old save (no .indev)
	If HasCLIFlag("testsave") Then IndevTestSave()
	;-test2107: drink three cans of SCP-2107 at once, the haunting starting after 2 seconds
	If HasCLIFlag("test2107") Then
		Local dk%
		For dk = 1 To 3
			IndevUse2107(CreateItem("scp2107", EntityX(Collider), EntityY(Collider), EntityZ(Collider)))
		Next
		I2107Delay = 140
		IndevTestLog("DRINK cans=" + I2107Cans + " haunting for " + Int(I2107Time / 70) + " s")
	EndIf
	;-testmiss: start Miss J's lesson in room2incidents at once, so the screen can be seen (IndevU13.bb)
	If HasCLIFlag("testmiss") Then
		For ev.Events = Each Events
			If ev\room <> Null Then
				If ev\room\RoomTemplate\Name = "room2incidents" Then ev\EventState = 1 : ev\EventState2 = 0 : ev\EventState3 = 0
			EndIf
		Next
	EndIf
	;-testuse: fire the effects of the usable items and the SCP-4035 lamp, one after another, and log each result
	If HasCLIFlag("testuse") Then
		Local un%, uname$, ut.Items, ust#, usta#
		For un = 0 To 3
			If un = 0 Then
				uname = "cookie377"
			ElseIf un = 1 Then
				uname = "camera978"
			ElseIf un = 2 Then
				uname = "knife3041"
			Else
				uname = "sweater1337"
			EndIf
			ut = CreateItem(uname, EntityX(Collider), EntityY(Collider), EntityZ(Collider))
			ust = IndevStress : usta = Stamina
			Msg = ""
			IndevUseU15(ut)
			IndevTestLog("USE " + uname + " stress " + Int(ust) + "->" + Int(IndevStress) + " stamina " + Int(usta) + "->" + Int(Stamina) + " msg=" + Msg)
		Next
		For un = 0 To 3
			ust = IndevStress : usta = Stamina
			Msg = ""
			IndevLamp14Ability()
			IndevTestLog("LAMP ability " + un + " stress " + Int(ust) + "->" + Int(IndevStress) + " stamina " + Int(usta) + "->" + Int(Stamina) + " msg=" + Msg)
		Next
	EndIf
	;which of the forced rooms found a slot
	For rt = Each RoomTemplates
		If rt\SetRoom >= 0 Then
			n = 0
			For r = Each Rooms
				If r\RoomTemplate = rt Then n = n + 1
			Next
			If n = 0 Then IndevTestLog("MISSING " + rt\Name) Else IndevTestLog("PLACED " + rt\Name + " x" + n)
		EndIf
	Next
	;the views
	list = GetCLIString("testlist", "")
	If list <> "" And FileType(list) = 1 Then
		f = ReadFile(list)
		While Not Eof(f)
			l = Trim(ReadLine(f))
			If l <> "" And Left(l, 1) <> ";" Then
				v = New IndevTestView
				v\room = Lower(IndevTestTok(l, 1))
				If IndevTestTok(l, 7) <> "" Then
					v\has = True
					v\ex = Float(IndevTestTok(l, 2)) : v\ey = Float(IndevTestTok(l, 3)) : v\ez = Float(IndevTestTok(l, 4))
					v\lx = Float(IndevTestTok(l, 5)) : v\ly = Float(IndevTestTok(l, 6)) : v\lz = Float(IndevTestTok(l, 7))
				EndIf
			EndIf
		Wend
		CloseFile(f)
	Else
		For rt = Each RoomTemplates
			If rt\SetRoom >= 0 Then
				v = New IndevTestView
				v\room = Lower(rt\Name)
			EndIf
		Next
	EndIf
	IndevTestCur = Null
	IndevTestNext()
End Function

;move on to the next view whose room is in this map, or finish
Function IndevTestNext()
	Local r.Rooms, it.Items, pvt%, tgt%
	If IndevTestCur = Null Then IndevTestCur = First IndevTestView Else IndevTestCur = After IndevTestCur
	While IndevTestCur <> Null
		For r = Each Rooms
			If Lower(r\RoomTemplate\Name) = IndevTestCur\room Then Exit
		Next
		If r <> Null Then Exit
		IndevTestLog("SKIP " + IndevTestCur\room + " (not in this map)")
		IndevTestCur = After IndevTestCur
	Wend
	If IndevTestCur = Null Then
		IndevTestLog("DONE " + IndevTestShots + " views")
		IndevTestState = 2
		IsRunning = False
		Return
	EndIf
	IndevTestLog("VISIT " + IndevTestCur\room)
	If IndevTestCur\has Then
		TFormPoint(IndevTestCur\ex, IndevTestCur\ey, IndevTestCur\ez, r\obj, 0)
		pvt = CreatePivot()
		PositionEntity pvt, TFormedX(), TFormedY(), TFormedZ()
		TFormPoint(IndevTestCur\lx, IndevTestCur\ly, IndevTestCur\lz, r\obj, 0)
		tgt = CreatePivot()
		PositionEntity tgt, TFormedX(), TFormedY(), TFormedZ()
		PointEntity pvt, tgt
		IndevTestYaw = EntityYaw(pvt) : IndevTestPitch = EntityPitch(pvt)
		PositionEntity Collider, EntityX(pvt), EntityY(pvt), EntityZ(pvt)
		FreeEntity pvt
		FreeEntity tgt
	Else
		PositionEntity Collider, EntityX(r\obj), EntityY(r\obj) + 0.7, EntityZ(r\obj)
		IndevTestYaw = r\angle : IndevTestPitch = 0
	EndIf
	ResetEntity Collider
	DropSpeed = 0
	IndevTestExtras(r)
	UpdateDoors()
	UpdateRooms()
	For it = Each Items
		it\disttimer = 0
	Next
	PlayerRoom = r
	IndevTestT0 = MilliSecs() : IndevTestFrameN = 0
End Function

;called every frame before MouseLook(): hold the view still
Function IndevTestPose()
	If IndevTestState <> 1 Or IndevTestCur = Null Then Return
	RotateEntity Collider, 0, IndevTestYaw, 0
	user_camera_pitch = IndevTestPitch
	BlinkTimer = 500.0
	If HasCLIFlag("test983") Then IndevTest983()
	If HasCLIFlag("test120") Or HasCLIFlag("test867") Then IndevTest29()
	If HasCLIFlag("test4427") Then I4427Thermal = True ;thermal on: SCP-4427 and the SCP-4433 figures show
	If HasCLIFlag("test178") Then I178On = True ;the 3-D glasses on: SCP-178's entities show
	If HasCLIFlag("test467") Then IndevTest467()
	If HasCLIFlag("testgatev") Then IndevTestGateV()
	If HasCLIFlag("testgatevhand") Then IndevTestGateHand()
	If HasCLIFlag("testgatevsave") Then IndevTestGateSave()
	If HasCLIFlag("testgatevcard") Then IndevTestGateCard()
	If HasCLIFlag("test33") Then IndevTest33()
	If HasCLIFlag("test34") Then IndevTest34()
	If HasCLIFlag("test35") Then IndevTest35()
	If HasCLIFlag("test36") Then IndevTest36()
	If HasCLIFlag("testwalk") Then IndevTestWalk()
	If HasCLIFlag("testgatevlook") And PlayerRoom <> Null Then
		If PlayerRoom\RoomTemplate\Name = "room2b32gatev" And IndevTestFrameN >= 10 Then
			Local lookIt.Items
			For lookIt = Each Items
				If lookIt\itemtemplate\name = "keygatev" Then Exit
			Next
			If IndevTestFrameN = 10 Then U32TestGo(318, 60, -232)
			If lookIt <> Null And IndevTestFrameN > 12 Then
				IndevTestYaw = VectorYaw(EntityX(lookIt\collider) - EntityX(Camera), 0, EntityZ(lookIt\collider) - EntityZ(Camera))
				IndevTestPitch = VectorPitch(EntityX(lookIt\collider) - EntityX(Camera), EntityY(lookIt\collider) - EntityY(Camera), EntityZ(lookIt\collider) - EntityZ(Camera))
			EndIf
		EndIf
	EndIf
	If IndevT173Start > 0 And Curr173 <> Null Then IndevT173Min = Min(IndevT173Min, EntityDistance(Curr173\Collider, Collider))
End Function

;called every frame before Flip: when the room has settled, save the frame and move on
Function IndevTestFrame()
	Local ms%, name$, fps#
	If IndevTestState <> 1 Or IndevTestCur = Null Or MainMenuOpen Then Return
	IndevTestFrameN = IndevTestFrameN + 1
	If IndevTestFrameN = 10 Then IndevTestT10 = MilliSecs()
	ms = MilliSecs() - IndevTestT0
	If ms < IndevTestMs Or IndevTestFrameN < 40 Then Return
	fps = (IndevTestFrameN - 10) * 1000.0 / Max(MilliSecs() - IndevTestT10, 1)
	IndevTestShots = IndevTestShots + 1
	name = "RoomTest\" + Right("00" + IndevTestShots, 3) + "_" + IndevTestCur\room + ".bmp"
	SaveBuffer(BackBuffer(), name)
	IndevTestLog("OK " + IndevTestCur\room + " fps=" + Int(fps) + " frames=" + IndevTestFrameN + " y=" + (EntityY(Collider) / RoomScale) + " dead=" + (KillTimer < 0) + " h17flips=" + Indev17Flips + " flicks=" + Indev17Flicks + " rings=" + Indev17Rings + " steps=" + Indev17Steps + " r18flips=" + Indev18Flips + " r18rings=" + Indev18Rings + " clicks=" + Indev18Clicks + " echoes=" + Indev18Echoes + " panel=" + Indev18Panel + " liftmove=" + IndevLiftMove + " liftsnd=" + IndevLiftSnd + " d173=" + IndevTest173Dist() + "/" + Int(IndevT173Start * 100) + " min173=" + Int(IndevT173Min * 100) + " h2107=" + Indev27Events + "/" + I2107Cans + " v983=" + Indev28Verses + " age983=" + Int(I983Age) + " candy983=" + IndevTestCandy983() + " end=" + SelectedEnding + " u31=" + I467Calls + "/" + I178On + " u29=" + Indev29Uses + "/" + I120Dest + "/" + Int(I867Seed) + "/" + Int(I867Pain) + "/" + I820Taken + " mem=" + Int(IndevMemory) + " stage=" + IndevMemoryStage + " memmsg=" + Msg + " shot=" + name)
	IndevTestNext()
End Function

;---- the bug-fix checks

;-testsave: write known values, save, scramble them, quick-load, and log what came back; then the same with the
;.indev file removed, as for a save made before it existed
Function IndevTestSave()
	Local path$ = SavePath + CurrSave
	DropSpeed = 0
	Indev513Active = True : Indev513Timer = 4321 : Indev513Rings = 0
	IndevMemory = 42 : IndevMemoryCured = False
	I113Uses = 1 : IndevFemale = True : IndevGenderShown = True
	SaveGame(path)
	IndevTestLog("SAVE wrote .indev=" + (FileType(path + ".indev") = 1) + " .cbsav=" + (FileType(path + ".cbsav") = 1))
	Indev513Active = False : Indev513Timer = 0 : Indev513Rings = 1
	IndevMemory = 5 : I113Uses = 0 : IndevFemale = False : IndevGenderShown = False
	LoadGameQuick(path)
	IndevTestLog("LOAD 513active=" + Indev513Active + " timer=" + Int(Indev513Timer) + " rings=" + Indev513Rings + " memory=" + Int(IndevMemory) + " uses113=" + I113Uses + " female=" + IndevFemale + " icon=" + IndevGenderShown)
	DeleteFile(path + ".indev")
	Indev513Active = False : Indev513Timer = 0 : Indev513Rings = 1
	LoadGameQuick(path)
	IndevTestLog("OLDSAVE 513active=" + Indev513Active + " timer=" + Int(Indev513Timer) + " rings=" + Indev513Rings)
End Function

;per view: -test173 puts SCP-173 at the far end of the silo's lower tunnel with the player looking away;
;-testitem <name> puts that item 0.7 in front of the camera
Function IndevTestExtras(r.Rooms)
	Local n$ = GetCLIString("testitem", ""), it.Items
	IndevLiftMove = 0 : IndevLiftSnd = 0 : IndevT173Start = 0 : IndevT173Min = 0
	If HasCLIFlag("test173") And r\RoomTemplate\Name = "room2newroom8" And Curr173 <> Null Then
		NoTarget = False
		Curr173\Idle = 0
		Indev173Started = True : Indev173SightTimer = 70 * 600 ;no relocation away from the test spot
		TFormPoint(1600, 20, 0, r\obj, 0)
		PositionEntity(Curr173\Collider, TFormedX(), TFormedY(), TFormedZ())
		ResetEntity(Curr173\Collider)
		IndevT173Start = EntityDistance(Curr173\Collider, Collider)
		IndevT173Min = IndevT173Start
	EndIf
	If n <> "" Then
		it = CreateItem(n, EntityX(Collider) + Sin(-IndevTestYaw) * 0.7, EntityY(Collider) + 0.4, EntityZ(Collider) + Cos(IndevTestYaw) * 0.7)
		EntityType(it\collider, HIT_ITEM)
	EndIf
End Function

Function IndevTest173Dist%()
	If Curr173 = Null Or IndevT173Start = 0 Then Return -1
	Return Int(EntityDistance(Curr173\Collider, Collider) * 100)
End Function

;-test983: today is your birthday; in SCP-983's room the monkey wakes at once and the test sings along
;perfectly (a click 1.4 s into every verse), so the run should end with the luminescent candy
Function IndevTest983()
	Local e.Events
	I983Birthday = True
	If PlayerRoom = Null Then Return
	If PlayerRoom\RoomTemplate\Name <> "room2b28monkey" Then Return
	For e = Each Events
		If e\room = PlayerRoom Then Exit
	Next
	If e = Null Then Return
	If e\EventState = 0 And (Not IAxFlag(e, "d")) Then
		e\EventState = 1 : e\EventState2 = 0 : e\EventState3 = 0
	EndIf
	If e\EventState = 1 And e\EventState2 >= 70 * 1.35 And e\EventState2 <= 70 * 1.5 And (Not IAxFlag(e, "c")) Then MouseHit1 = True
End Function

;-test120: in SCP-120's outbuilding, set it to destination 9 and step in on the 20th frame (the log's y should be
;~3072, on the Moon). -test867: in Section E, stand against a spruce on the 20th frame (the log shows the seed)
Function IndevTest29()
	Local e.Events, p%
	If PlayerRoom = Null Or IndevTestFrameN <> 20 Then Return
	For e = Each Events
		If e\room = PlayerRoom Then Exit
	Next
	If e = Null Then Return
	If HasCLIFlag("test120") And PlayerRoom\RoomTemplate\Name = "room2b29pool" Then
		I120Dest = 9
		I120In = True
		U29Jump(e)
	EndIf
	If HasCLIFlag("test867") And PlayerRoom\RoomTemplate\Name = "room2b29spruce" Then
		p = PlayerRoom\Objects[U29_SPR_T0]
		PositionEntity(Collider, EntityX(p, True) + 0.3, EntityY(Collider), EntityZ(p, True))
		ResetEntity(Collider)
		U29Spruce(e)
	EndIf
End Function

;-test467: in SCP-467's room, on the 10th frame, a radio goes into the inventory and the player into the booth;
;the call should come two seconds later (the log's u31= shows the number of calls)
Function IndevTest467()
	Local it.Items, p%
	If PlayerRoom = Null Or IndevTestFrameN <> 10 Then Return
	If PlayerRoom\RoomTemplate\Name <> "room2b31booth" Then Return
	it = CreateItem("radio", EntityX(Collider), EntityY(Collider), EntityZ(Collider))
	PickItem(it)
	p = PlayerRoom\Objects[U31_BTH_BOOTH]
	PositionEntity(Collider, EntityX(p, True), EntityY(Collider), EntityZ(p, True))
	ResetEntity(Collider)
End Function

;-testgatev <v1|v2|v3>: in Gate V, on the 30th frame, set the gate up for that ending and put the player in the
;hatch; the log's end= shows which ending fired
Function IndevTestGateV()
	Local m$ = Lower(GetCLIString("testgatev", "v1")), k%
	If PlayerRoom = Null Or IndevTestFrameN <> 30 Then Return
	If PlayerRoom\RoomTemplate\Name <> "room2b32gatev" Then Return
	I32Alarm = False : I32MTF = False : I32Blown = False
	If m = "v2" Then
		I32MTF = True
		U32TestGo(-700, -1024 + 60, 640) ;walk up to the unit: they stop you in front of them
		PointEntity(Collider, PlayerRoom\Objects[U32_GV_PORTAL])
		IndevTestYaw = EntityYaw(Collider) : IndevTestPitch = 0
		TranslateEntity(Collider, 0, 0, 0)
		U32TestGo(-820, -1024 + 60, 640)
		Return
	EndIf
	If m = "v3" Then I32MTF = True : I32Blown = True
	If m = "mtf" Then
		I32MTF = True
		For k = 0 To 2
			If I32Fig(k) <> 0 Then ShowEntity(I32Fig(k))
		Next
		TFormPoint(-560, -1024 + 40, 640, PlayerRoom\obj, 0)
		PositionEntity(Collider, TFormedX(), TFormedY(), TFormedZ())
		ResetEntity(Collider)
		PointEntity(Collider, PlayerRoom\Objects[U32_GV_PORTAL])
		IndevTestYaw = EntityYaw(Collider) : IndevTestPitch = 0
		Return
	EndIf
	TFormPoint(-950, -1024 + 40, 640, PlayerRoom\obj, 0)
	PositionEntity(Collider, TFormedX(), TFormedY(), TFormedZ())
	ResetEntity(Collider)
End Function

;-testgatevhand: Gate V by hand - real clicks (aim at the thing, MouseHit1) on the break-glass, then the breaker in
;the tunnel, then (alarm re-armed so the unit comes) the console's seal charges, then a walk into the hatch.
;Every step is logged as GATEV ...
Global IndevGVStep%, IndevGVT%
;-test33: the batch-33 mechanics, driven directly, one room per view; results in the log as T33 lines.
;  toys: the key on SCP-1007 (age down a year), the Guide to History (purple), then a ride on SCP-3938 (another room)
;  archive: a battery into SCP-232 and two uses, SCP-865 fired at the hand, SCP-762-EX flipped six times, then a
;           save / scramble / quick-load round trip of the batch-33 state
;  bio: SCP-2394 woken (it hops), then the player walked up to SCP-1563's stake (it grabs)
;  deep: down to the vault, SCP-L043 played twice
Function IndevTest33()
	Local r.Rooms = PlayerRoom, it.Items, n$, k%, a#, p%, x#, z#
	If r = Null Then Return
	n = r\RoomTemplate\Name
	Select n
		Case "room2b33toys"
			If IndevTestFrameN = 10 Then
				I1007Dead = False : I1007Age = 40
				it = CreateItem("key1007", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				U32TestGo(560, 80, -480)
				a = I1007Age
				IndevUse33(it)
				IndevTestLog("T33 key1007 age " + Int(a) + " -> " + Int(I1007Age) + " (expect one less)")
			EndIf
			If IndevTestFrameN = 14 Then
				it = CreateItem("book4890", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				IndevUse33(it)
				IndevTestLog("T33 book4890 purple=" + (I4890T > 0) + " msg=" + Msg)
				InvOpen = False
			EndIf
			If IndevTestFrameN = 36 Then
				For k = 1 To 12
					If I3938Rides > 0 Then Exit
					I3938Cool = 0
					U33Ride()
				Next
				If PlayerRoom <> Null Then IndevTestLog("T33 ride3938 now in " + PlayerRoom\RoomTemplate\Name + " rides=" + I3938Rides + " cool=" + Int(I3938Cool))
			EndIf
		Case "room2b33archive"
			If IndevTestFrameN = 10 Then
				it = CreateItem("bat", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				it = CreateItem("zapper232", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				IndevUse33(it) : IndevUse33(it) : IndevUse33(it)
				IndevTestLog("T33 zapper232 bat=" + I232Bat + " uses=" + I232Uses + " batteryleft=" + (U30Has("bat") <> Null))
				it = CreateItem("gun865", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				a = Injuries
				IndevUse33(it) : IndevUse33(it)
				IndevTestLog("T33 gun865 shots=" + I865Shots + " injuries+" + (Injuries - a))
				it = CreateItem("coin762", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
				For k = 1 To 6
					IndevUse33(it)
				Next
				IndevTestLog("T33 coin762 flips=" + I762Flips + " msg=" + Msg)
				InvOpen = False : I4890T = 0
			EndIf
			If IndevTestFrameN = 20 Then
				I1007Age = 33 : I1007Dead = False : I2394Woke = 2 : IL043Line = 4 : I4612Akiva = 300
				SaveGame(SavePath + CurrSave)
				I1007Age = 1 : I232Bat = False : I762Flips = 0 : I2394Woke = 0 : IL043Line = 0 : I4612Akiva = 0
				LoadGameQuick(SavePath + CurrSave)
				IndevTestLog("T33 save age1007=" + Int(I1007Age) + " bat232=" + I232Bat + " flips762=" + I762Flips + " woke2394=" + I2394Woke + " l043=" + IL043Line + " akiva=" + Int(I4612Akiva) + " (expect 33 1 6 2 4 300)")
			EndIf
		Case "room2b33bio"
			If IndevTestFrameN = 10 Then
				I2394Woke = 1 : I2394T = 70 * 30 : I2394Hop = 1
				If I33Frog <> 0 Then IndevTestLog("T33 frog2394 at " + Int(EntityX(I33Frog, True) * 100) + "," + Int(EntityZ(I33Frog, True) * 100))
			EndIf
			If IndevTestFrameN = 30 Then
				If I33Frog <> 0 Then IndevTestLog("T33 frog2394 woke=" + I2394Woke + " now at " + Int(EntityX(I33Frog, True) * 100) + "," + Int(EntityZ(I33Frog, True) * 100))
				I1563Cool = 0
				U32TestGo(520, 80, -360)
			EndIf
			If IndevTestFrameN = 36 Then IndevTestLog("T33 marker1563 grab=" + (I1563Grab > 0) + " msg=" + Msg)
		Case "room2b33deep"
			If IndevTestFrameN = 10 Then
				U32TestGo(700, -768 + 80, 640)
				U33L043(r) : U33L043(r)
				IndevTestLog("T33 l043 line=" + IL043Line + " msg=" + Msg)
			EndIf
			If IndevTestFrameN = 30 Then IndevTestLog("T33 vault y=" + Int(EntityY(Collider) / RoomScale) + " room=" + PlayerRoom\RoomTemplate\Name)
	End Select
End Function

;-test34: in each deep storage room on frame 10, use every item of batch 34 and the special units, and log
Function IndevTest34()
	Local r.Rooms = PlayerRoom, it.Items, e.Events, n$, k%, a#, i%, nm$
	If r = Null Or IndevTestFrameN <> 10 Then Return
	For e = Each Events
		If e\room = r Then Exit
	Next
	n = r\RoomTemplate\Name
	If Left(n, 9) <> "room2b34h" And Left(n, 9) <> "room2b34o" And Left(n, 9) <> "room2b34b" And Left(n, 9) <> "room2b34s" Then Return
	k = 0
	For i = 0 To U34Count - 1
		If U34PRoom(i) = r Then k = k + 1
	Next
	IndevTestLog("T34 " + n + " units=" + k + " models=" + U34CountModels(r))
	Select n
		Case "room2b34humanoid"
			it = CreateItem("pills3866", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse34(it)
			IndevTestLog("T34 3866 sleep=" + Int(I34Sleep))
			it = CreateItem("dice1974", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse34(it)
			IndevTestLog("T34 1974 msg=" + Msg)
			i = U34Find("1508") : Injuries = 1.0 : U34Use(e, i) : IndevTestLog("T34 1508 injuries=" + Injuries)
			i = U34Find("3634") : U34Use(e, i) : IndevTestLog("T34 3634 msg=" + Msg)
		Case "room2b34objects"
			it = CreateItem("stapler3709", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
			U32TestGo(150, 80, 0) : IndevUse34(it) : IndevTestLog("T34 3709 msg=" + Left(Msg, 40))
			it = CreateItem("cards3803", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse34(it)
			it = CreateItem("book1841", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
			i = U34Find("1667") : U34Use(e, i) : IndevTestLog("T34 1667 shoe=" + Int(I34Shoe))
			i = U34Find("2414") : U34Use(e, i) : U34Use(e, i) : IndevTestLog("T34 2414 faces=" + I34Faces)
			IndevUse34(it) : IndevTestLog("T34 1841 now in " + PlayerRoom\RoomTemplate\Name)
		Case "room2b34bio"
			For k = 1 To 5
				nm = Mid("grapes1255caps4193  tabs5604  cereal2983camera5701", (k - 1) * 10 + 1, 10)
				IndevTestLog("T34 item " + Trim(nm)) : it = CreateItem(Trim(nm), EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse34(it)
			Next
			IndevTestLog("T34 bio items sprout=" + Int(I34Sprout) + " caps=" + I34Caps + " photo=" + I34Photo)
			IndevTestLog("T34 steal...") : i = U34Find("5582") : U34Use(e, i) : IndevTestLog("T34 5582 msg=" + Left(Msg, 90))
			i = U34Find("711-FR") : U34Use(e, i) : IndevTestLog("T34 711 dodo=" + Int(I34Dodo))
			I34Sprout = 0
		Case "room2b34site45"
			i = U34Find("3811") : U34Use(e, i) : IndevTestLog("T34 3811 fearless=" + Int(I34Fearless))
			I865Shots = 1 : a = Injuries : i = U34Find("5151") : U34Use(e, i) : IndevTestLog("T34 5151 hurt=" + (Injuries - a))
			I34Caps = 7 : I34Clean = 1
			SaveGame(SavePath + CurrSave)
			I34Caps = 0 : I34Clean = 0 : I34Fearless = 0
			LoadGameQuick(SavePath + CurrSave)
			IndevTestLog("T34 save caps=" + I34Caps + " clean=" + I34Clean + " fearless>0=" + (I34Fearless > 0) + " (expect 7 1 1)")
	End Select
	InvOpen = False
End Function

;-test35: in the cell block and the bunker on frame 10, drive the specials and the four items, and log
Function IndevTest35()
	Local r.Rooms = PlayerRoom, it.Items, e.Events, n$, k%, i%, a#
	If r = Null Or IndevTestFrameN <> 10 Then Return
	n = r\RoomTemplate\Name
	If n <> "room2b35cellblock" And n <> "room2b35bunker" Then Return
	For e = Each Events
		If e\room = r Then Exit
	Next
	k = 0
	For i = 0 To U34Count - 1
		If U34PRoom(i) = r Then k = k + 1
	Next
	IndevTestLog("T35 " + n + " units=" + k + " models=" + U34CountModels(r) + " count=" + U34Count)
	If n = "room2b35cellblock" Then
		it = CreateItem("coin762", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
		i = U34Find("1779") : U34Use(e, i) : IndevTestLog("T35 1779 fed=" + I1779Fed + " coin=" + (U30Has("coin762") <> Null))
		i = U34Find("517") : U34Use(e, i) : IndevTestLog("T35 517 fortune=" + Int(I35Fortune) + " msg=" + Left(Msg, 60))
		i = U34Find("799") : a = Injuries : U34Use(e, i) : U34Use(e, i) : U34Use(e, i) : IndevTestLog("T35 799 hurt=" + (Injuries - a))
	Else
		it = CreateItem("hat2890", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
		i = U34Find("1579") : PositionEntity(Collider, EntityX(U34Piv(i), True) - 1.0, EntityY(Collider), EntityZ(U34Piv(i), True)) : ResetEntity(Collider)
		IndevUse35(it) : IndevTestLog("T35 2890 hat=" + I35Hat)
		it = CreateItem("briefs1388", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse35(it)
		it = CreateItem("watch1912", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse35(it)
		it = CreateItem("brush2816", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse35(it)
		IndevTestLog("T35 items power=" + Int(I35Power) + " watch=" + Int(I35Watch) + " paint=" + Int(I35Paint))
		SaveGame(SavePath + CurrSave)
		I1779Fed = 0 : I35Hat = 0
		LoadGameQuick(SavePath + CurrSave)
		IndevTestLog("T35 save fed=" + I1779Fed + " hat=" + I35Hat + " (expect 1 1)")
	EndIf
	InvOpen = False
End Function

;-test36: the candy items in the confectionery room; in SCP-1479's room, walk into the taiga and toward an eye
Function IndevTest36()
	Local r.Rooms = PlayerRoom, it.Items, n$, k%, a#, vis%
	If r = Null Then Return
	n = r\RoomTemplate\Name
	If n = "room2b36confect" And IndevTestFrameN = 10 Then
		it = CreateItem("gum1200", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
		For k = 1 To 4
			IndevUse36(it)
		Next
		IndevTestLog("T36 gum left=" + I36GumLeft + " glow=" + Int(I36Glow) + " run=" + Int(I36Run))
		it = CreateItem("jar1916", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it)
		IndevUse36(it) : IndevUse36(it) : IndevUse36(it) : IndevUse36(it)
		IndevTestLog("T36 jawbreaker next=" + I1916Next + " kind=" + I1916K + " speed=" + U36SpeedMul() + " mul=" + IndevSpeedMul())
		it = CreateItem("pop3147", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse36(it)
		IndevTestLog("T36 lollipop msg=" + Left(Msg, 50))
		it = CreateItem("cotton1921", EntityX(Collider), EntityY(Collider), EntityZ(Collider)) : PickItem(it) : IndevUse36(it)
		IndevTestLog("T36 cotton=" + Int(I36Cotton) + " still held=" + (U30Has("cotton1921") <> Null))
		SaveGame(SavePath + CurrSave)
		I36GumLeft = 5 : I1916Next = 1 : I36Cotton = 0
		LoadGameQuick(SavePath + CurrSave)
		IndevTestLog("T36 save gum=" + I36GumLeft + " jar=" + I1916Next + " cotton>0=" + (I36Cotton > 0) + " (expect 1 5 1)")
		InvOpen = False
	EndIf
	If n = "room2b36taiga" Then
		If IndevTestFrameN = 10 Then U32TestGo(560, 80, -300)
		If IndevTestFrameN = 30 Then
			vis = 0
			For k = 0 To 5
				If I36Eye(k) <> 0 Then
					If Not EntityHidden(I36Eye(k)) Then vis = vis + 1
				EndIf
			Next
			IndevTestLog("T36 taiga in=" + I36InTaiga + " eyes visible=" + vis)
			If I36Eye(0) <> 0 Then
				PositionEntity(Collider, EntityX(I36Eye(0), True) - 0.5, EntityY(Collider), EntityZ(I36Eye(0), True)) : ResetEntity(Collider)
			EndIf
		EndIf
		If IndevTestFrameN = 36 And I36Eye(0) <> 0 Then IndevTestLog("T36 eye0 hidden when near=" + EntityHidden(I36Eye(0)))
	EndIf
End Function

;-testwalk: open (and unlock) every door of the room on frame 10, then walk straight ahead (the view's direction)
;until frame 200 and log where the player got to, in the room's own coordinates
Global IndevWalkStep%, IndevWalkRoom.Rooms
Function IndevTestWalk()
	Local r.Rooms = IndevWalkRoom, d.Doors, k%
	If IndevTestFrameN < 5 Then IndevWalkStep = 0 : IndevWalkRoom = PlayerRoom : Return
	If r = Null Then Return
	If IndevWalkStep = 0 And IndevTestFrameN >= 10 Then
		IndevWalkStep = 1
		For d = Each Doors
			If d\room = r Then d\locked = False : d\open = True : k = k + 1
		Next
		IndevTestLog("WALK " + r\RoomTemplate\Name + " opened " + k + " doors")
	EndIf
	If IndevWalkStep >= 1 And IndevTestFrameN > 30 And IndevTestFrameN < 700 Then
		TranslateEntity(Collider, Sin(-IndevTestYaw) * 0.02 * FPSfactor, 0, Cos(IndevTestYaw) * 0.02 * FPSfactor)
	EndIf
	If IndevWalkStep = 1 And IndevTestFrameN >= 700 Then
		IndevWalkStep = 2
		TFormPoint(EntityX(Collider), EntityY(Collider), EntityZ(Collider), 0, r\obj)
		IndevTestLog("WALK " + r\RoomTemplate\Name + " reached " + Int(TFormedX()) + "," + Int(TFormedY()) + "," + Int(TFormedZ()))
	EndIf
End Function

Function U34CountModels%(r.Rooms)
	Local i%, k%, n%
	For i = 0 To U34Count - 1
		If U34PRoom(i) = r Then
			For k = 0 To 2
				If U34Mdl(i, k) <> 0 Then n = n + 1
			Next
		EndIf
	Next
	Return n
End Function

Function U32TestGo(lx#, ly#, lz#)
	TFormPoint(lx, ly, lz, PlayerRoom\obj, 0)
	PositionEntity(Collider, TFormedX(), TFormedY(), TFormedZ())
	ResetEntity(Collider)
End Function

Function U32TestAim(p%)
	Local dx# = EntityX(p, True) - EntityX(Camera, True)
	Local dy# = EntityY(p, True) - EntityY(Camera, True)
	Local dz# = EntityZ(p, True) - EntityZ(Camera, True)
	IndevTestYaw = VectorYaw(dx, dy, dz)
	IndevTestPitch = VectorPitch(dx, dy, dz)
End Function

;-testgatevcard: find the Gate V access card on the checkpoint desk, pick it up, and use the reader with it
Function IndevTestGateCard()
	Local r.Rooms = PlayerRoom, t%, it.Items, found.Items, d.Doors
	If r = Null Then Return
	If r\RoomTemplate\Name <> "room2b32gatev" Then Return
	t = MilliSecs() - IndevTestT0
	If t < IndevGVT Then Return
	d = r\RoomDoors[0]
	Select IndevGVStep
		Case 0
			For it = Each Items
				If it\itemtemplate\name = "keygatev" Then found = it : Exit
			Next
			If found <> Null Then
				Local rr.Rooms, best.Rooms, bd# = 99999, dd#
				For rr = Each Rooms
					dd = Abs(EntityX(rr\obj, True) - EntityX(found\collider, True)) + Abs(EntityZ(rr\obj, True) - EntityZ(found\collider, True))
					If dd < bd Then bd = dd : best = rr
				Next
				IndevTestLog("GATEVCARD lies in: " + best\RoomTemplate\Name + " picked=" + found\Picked)
				PickItem(found)
				IndevTestLog("GATEVCARD picked up: in inventory=" + (U30Has("keygatev") <> Null) + " door locked=" + d\locked)
			Else
				IndevTestLog("GATEVCARD not found in the room")
			EndIf
			U32TestGo(520, 60, -390)
		Case 1 : U32TestAim(r\Objects[U32_GV_READER])
		Case 2 : MouseHit1 = True
		Case 3 : IndevTestLog("GATEVCARD reader: open=" + I32Open + " alarm=" + I32Alarm + " door open=" + d\open + " locked=" + d\locked + " msg=" + Msg)
		Default : Return
	End Select
	IndevGVStep = IndevGVStep + 1
	IndevGVT = t + 600
End Function

Function U32TestFlags$()
	Local e.Events
	For e = Each Events
		If e\room = PlayerRoom Then Return e\EventStr
	Next
	Return "?"
End Function

Function IndevTestGateHand()
	Local r.Rooms = PlayerRoom, t%, p%, d.Doors
	If r = Null Then Return
	If r\RoomTemplate\Name <> "room2b32gatev" Then Return
	t = MilliSecs() - IndevTestT0
	If t < IndevGVT Then Return
	d = r\RoomDoors[0]
	Select IndevGVStep
		Case 0 : U32TestGo(430, 60, -390)
		Case 1 : U32TestAim(r\Objects[U32_GV_GLASS])
		Case 2 : MouseHit1 = True
		Case 3
			IndevTestLog("GATEV glass: open=" + I32Open + " alarm=" + I32Alarm + " lock=" + Int(I32Lock / 70) + "s door open=" + d\open + " locked=" + d\locked)
			U32TestGo(900, -1024 + 60, 100)
		Case 4 : U32TestAim(r\Objects[U32_GV_BREAKER])
		Case 5 : MouseHit1 = True
		Case 6
			IndevTestLog("GATEV breaker: alarm=" + I32Alarm + " (0 = cut)")
			U32TestGo(860, -1024 + 60, 400)
		Case 7
			IndevTestLog("GATEV tunnel: events=" + U32TestFlags() + " (s = the steam burst)")
			U32TestGo(600, -1024 + 60, -620)
		Case 8
			IndevTestLog("GATEV stair bottom: events=" + U32TestFlags() + " (f = the footsteps) blink=" + LightBlink)
			I32Alarm = True
			U32TestGo(-300, -1024 + 60, 640)
		Case 9
			IndevTestLog("GATEV atrium with the alarm live: mtf=" + I32MTF + " events=" + U32TestFlags() + " (r = the radio)")
			U32TestGo(-760, -1024 + 60, 880)
		Case 10 : U32TestAim(r\Objects[U32_GV_CONSOLE])
		Case 11 : MouseHit1 = True
		Case 12 : IndevTestLog("GATEV console: charge=" + Int(I32Charge / 70) + "s blown=" + I32Blown)
		Case 13
			IndevTestLog("GATEV after the charges: blown=" + I32Blown + " mtf=" + I32MTF)
			U32TestGo(-950, -1024 + 60, 640)
		Case 14 : IndevTestLog("GATEV hatch: ending=" + SelectedEnding)
		Default : Return
	End Select
	IndevGVStep = IndevGVStep + 1
	If IndevGVStep = 13 Then
		IndevGVT = t + 6500
	Else
		IndevGVT = t + 600
	EndIf
End Function

;-testgatevsave: set Gate V mid-way (glass broken, alarm live, the unit at the hatch, 50 s of lockdown left),
;save, scramble, quick-load, and log what came back - the state and the door/figures it drives
Function IndevTestGateSave()
	Local r.Rooms = PlayerRoom, t%, d.Doors, k%, vis%
	If r = Null Then Return
	If r\RoomTemplate\Name <> "room2b32gatev" Then Return
	t = MilliSecs() - IndevTestT0
	If t < IndevGVT Then Return
	Select IndevGVStep
		Case 0
			I32Open = 2 : I32Alarm = True : I32MTF = True : I32Blown = False : I32Lock = 70 * 50
			SaveGame(SavePath + CurrSave)
			IndevTestLog("GATEVSAVE saved: open=2 alarm=1 mtf=1 lock=50s")
			I32Open = 0 : I32Alarm = False : I32MTF = False : I32Lock = 0
			LoadGameQuick(SavePath + CurrSave)
		Case 1
			r = PlayerRoom
			d = Null
			For r = Each Rooms
				If r\RoomTemplate\Name = "room2b32gatev" Then d = r\RoomDoors[0] : Exit
			Next
			vis = 0
			For k = 0 To 2
				If I32Fig(k) <> 0 Then
					If Not EntityHidden(I32Fig(k)) Then vis = vis + 1
				EndIf
			Next
			IndevTestLog("GATEVSAVE figures: handles " + I32Fig(0) + " " + I32Fig(1) + " " + I32Fig(2) + " room=" + PlayerRoom\RoomTemplate\Name)
			If d <> Null Then
				IndevTestLog("GATEVSAVE loaded: open=" + I32Open + " alarm=" + I32Alarm + " mtf=" + I32MTF + " lock=" + Int(I32Lock / 70) + "s door open=" + d\open + " locked=" + d\locked + " figures shown=" + vis)
			Else
				IndevTestLog("GATEVSAVE loaded: no Gate V room after the load")
			EndIf
		Default : Return
	End Select
	IndevGVStep = IndevGVStep + 1
	IndevGVT = t + 1500
End Function

Function IndevTestCandy983$()
	Local it.Items, s$ = ""
	For it = Each Items
		If Left(it\itemtemplate\name, 9) = "candy983_" Then s = s + Mid(it\itemtemplate\name, 10) + ","
	Next
	Return s
End Function
