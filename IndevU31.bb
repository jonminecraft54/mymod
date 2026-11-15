;=====================================================================
; SCP: Containment Breach - Indev: the thirty-first batch - SCP-467 and five anomalous items
;
;   SCP-467  the confessional phone booth (room2b31booth). Stand inside it with a communication device (a radio,
;            the SCP-1471 phone, the SCP-4433 phone, the SCP-2935 phone) and after a moment the device rings: someone
;            you know, telling you something you did not know. Once a "day" (six minutes). Around Thanksgiving and
;            Christmas (by the PC's clock) the calls turn darker: yourself, the dead, people who never existed.
;            The recorder keeps the call; the phone log says no call was made.
;   SCP-178  3-D glasses (use to put them on / take them off): tall entities stand around you, curious. Walk into one
;            or click on one and the lacerations start - they do not stop.
;   SCP-198  a striped mug in a sealed case on a digital scale. Open the case and the alarm goes. Use it twice to
;            hold it: it bonds to your hand, fills itself, and you waste away unless you drink from it. Only death
;            frees you; it will not stay dropped.
;   SCP-207  a bottle of cola (SCP-207-B). One swallow: no more need to rest, and faster, and faster - until the
;            body gives out (five minutes). SCP-500 saves you.
;   SCP-1079 Bubblebath Bonbons: one per sitting. Each more in the same sitting makes it much worse; four kill.
;   SCP-1650 the oil pot: use to tilt it to the next angle and pour (45, 50, 65, 90 degrees, upright); use again
;            straight away to drink what it poured.
;   Summaries of scp-wiki.wikidot.com/scp-467, /scp-178, /scp-198, /scp-207, /scp-1079, /scp-1650 (CC BY-SA 3.0).
;=====================================================================

Global I467Cool#, I467In#, I467Calls%
Global I178On%, I178Cut#, I178Cuts%, I178Room.Rooms, I178Base%
Dim I178E%(3)
Global I198Bond%, I198Hunger#, I198Starve#, I198Ask#, I198Fluid$
Global I207On%, I207T#, I207Boost#
Global I1079Left%, I1079Count%, I1079Win#
Global I1650Ang%, I1650Pour#, I1650Poison#
Global Indev31Uses%

Function Indev31Reset(newGame%)
	Local k%
	If newGame Then
		I467Cool = 0 : I198Bond = False : I207On = False : I1079Left = 8 : I1650Ang = 0
	EndIf
	I467In = 0 : I178On = False : I178Cut = 0 : I178Cuts = 0 : I178Room = Null : I178Base = 0
	For k = 0 To 3
		I178E(k) = 0
	Next
	I198Ask = 0 : I1079Win = 0 : I1650Pour = 0 : I1650Poison = 0 : I207Boost = 0
	If I1079Left = 0 Then I1079Left = 8 ;the side save (read after this) puts back what was eaten
End Function

;player speed multiplier (Main.bb, MovePlayer): SCP-207
Function IndevSpeedMul#()
	If I207On Then Return (1.0 + I207Boost) * U36SpeedMul()
	Return U36SpeedMul() ;SCP-1916's gravity, SCP-1200's Running (IndevU36.bb)
End Function

Function IndevU31Dress(r.Rooms)
	Select r\RoomTemplate\Name
		Case "room2b31booth"
			U30Prop(r, r\Objects[U31_BTH_BOOTH], "GFX\map\props\scp467.b3d", 1.0, False)
		Case "room2b31items"
			U30Prop(r, r\Objects[U31_ITM_CRATE207], "GFX\map\props\scp207crate.b3d", 1.0, False)
	End Select
End Function

;a communication device in the inventory?
Function U31HasDevice%()
	Local i%, n$
	For i = 0 To MaxItemAmount - 1
		If Inventory(i) <> Null Then
			n = Inventory(i)\itemtemplate\name
			Select n
				Case "radio", "fineradio", "veryfineradio", "18vradio", "scp1471", "item2935phone", "phone4433"
					Return True
			End Select
		EndIf
	Next
	Return False
End Function

Function U31Holiday%()
	Local m$ = Mid(CurrentDate(), 4, 3)
	Return (m = "Nov" Or m = "Dec")
End Function

Function UpdateIndevU31(e.Events)
	Select e\room\RoomTemplate\Name
		Case "room2b31booth" : U31Booth(e)
		Case "room2b31items" : U31Items(e)
	End Select
End Function

;--------------------------------------------------------------------------------------------- SCP-467
Function U31Booth(e.Events)
	Local r.Rooms = e\room, p% = r\Objects[U31_BTH_BOOTH], dx#, dz#
	If PlayerRoom <> r Then Return
	dx = EntityX(Collider) - EntityX(p, True) : dz = EntityZ(Collider) - EntityZ(p, True)
	If dx * dx + dz * dz < 0.3 * 0.3 Then
		I467In = I467In + FPSfactor
		If I467In >= 70 * 2 And (Not IAxFlag(e, "i")) Then
			IAxSetFlag(e, "i")
			If Not U31HasDevice() Then
				IS16Tell("An empty phone booth. A plate with four screw holes where the phone used to be. It feels like it is waiting for something to ring.", 7)
			ElseIf I467Cool > 0 Then
				IS16Tell("Your device stays silent. It has not been a day since the booth last spoke to you.", 5)
			Else
				U31Call(e)
			EndIf
		EndIf
	Else
		I467In = 0
		IS13Drop(e, "i")
	EndIf
	If IS10Press(r\Objects[U31_BTH_RECORDER], 1.8) Then
		If I467Calls > 0 Then
			IS16Tell("The recorder has your last call on tape, every word. The phone log beside it says no call was made.", 6)
		Else
			IS16Tell("The recorder is armed and waiting. The tape counter reads 0000.", 4)
		EndIf
	EndIf
	If IS10Press(r\Objects[U31_BTH_LOG], 2.0) Then
		IS16Tell("TEST LOG 467: mothers, victims, a researcher's opinion of a haircut, a man's own voice. Near the holidays, worse.", 6)
	EndIf
	If IS10Press(r\Objects[U31_BTH_RIGHTS], 1.8) Then
		IS16Tell("Dr. Rights' desk: a test sheet for SCP-467, 'Nature of call: unknown', and two days of crossed-out resignation drafts.", 7)
	EndIf
	If IS10Press(r\Objects[U31_BTH_ICEBERG], 1.8) Then
		IS16Tell("Dr. Iceberg's desk: a reprimand form for a fight at Site 17, signed with very little remorse.", 6)
	EndIf
	If IS10Press(r\Objects[U31_BTH_BREAK], 1.8) Then
		IS16Tell("The break room. Someone has written on the fridge: 'NOBODY tell Iceberg what the booth said about him.'", 6)
	EndIf
End Function

;someone you know calls: what they tell you, and what it does to you
Function U31Call(e.Events)
	Local n% = 6, k%
	If U31Holiday() Then n = 9
	k = Rand(1, n)
	I467Cool = 70 * 60 * 6
	I467Calls = I467Calls + 1
	Indev31Uses = Indev31Uses + 1
	IS10Sound("SFX\Indev\phonering.wav", Collider, 6.0, 1.0)
	Select k
		Case 1
			IAxSay("Your mother", "I'm so disappointed in what you did. And I keep thinking it's my fault. I should have raised you better.", 10)
			IndevStress = Min(100, IndevStress + 15)
		Case 2
			IAxSay("A stranger", "We are the family. We never forgot what you did. But we're learning, slowly, to forgive you.", 10)
			IndevStress = Max(0, IndevStress - 10) : BlurTimer = Max(BlurTimer, 70 * 3)
		Case 3
			IAxSay("A researcher", "It's me - from the room next door. I just wanted you to know your haircut looks ridiculous.", 8)
			IndevStress = Max(0, IndevStress - 8)
		Case 4
			IAxSay("Your own voice", "Listen. They made you forget. Here is what happened, before the amnestics - all of it.", 10)
			IndevMemory = Max(0, IndevMemory - 20)
			BlurTimer = Max(BlurTimer, 70 * 4)
		Case 5
			IAxSay("Today's guard", "Since you'll hear it anyway: I left a level 3 keycard in the break room. By the vending machine. Please don't tell.", 10)
			If Not IAxFlag(e, "k") Then
				IAxSetFlag(e, "k")
				IS16Give("key3", e\room\Objects[U31_BTH_BREAK])
			EndIf
		Case 6
			IAxSay("Someone you worked with", "I'm the one who gave them your name. That's how you ended up as a D. I'm sorry. I'm not sorry enough.", 10)
			IndevStress = Min(100, IndevStress + 12)
		Case 7
			IAxSay("A voice you buried", "It's cold where I am. Are you eating? You never ate properly at the holidays.", 10)
			IndevStress = Min(100, IndevStress + 25) : BlurTimer = Max(BlurTimer, 70 * 6)
		Case 8
			IAxSay("Your sister", "You never call. You never call your sister. ...You don't have a sister? Don't be silly.", 10)
			IndevStress = Min(100, IndevStress + 18)
		Default
			IAxSay("Your victim", "(screaming, without words, for five full minutes)", 10)
			IndevStress = Min(100, IndevStress + 30) : CameraShake = 3.0
	End Select
End Function

;--------------------------------------------------------------------------------------------- the item wing
Function U31Items(e.Events)
	Local r.Rooms = e\room
	If PlayerRoom <> r Then Return
	If IS10Press(r\Objects[U31_ITM_CASE198], 1.6) Then
		If Not IAxFlag(e, "m") Then
			IAxSetFlag(e, "m")
			IS16Give("scp198", r\Objects[U31_ITM_CASE198])
			IS10Sound("SFX\Alarm\Alarm2_1.ogg", r\Objects[U31_ITM_SCALE], 10.0, 0.8)
			IS16Tell("You unlatch the case. The scale's display jumps - WEIGHT DEVIATION - and an alarm starts. CONTAINMENT PROTOCOL 198.", 7)
		Else
			IS16Tell("The case is empty. The scale reads 0.000 kg.", 3)
		EndIf
	EndIf
	If IS10Press(r\Objects[U31_ITM_SCALE], 1.8) Then
		If IAxFlag(e, "m") Then
			IS16Tell("SCP-198 CASE: 0.000 kg. DEVIATION. PROTOCOL 198 IN EFFECT.", 4)
		Else
			IS16Tell("SCP-198 CASE: 1.284 kg. NO DEVIATION.", 3)
		EndIf
	EndIf
	If IS10Press(r\Objects[U31_ITM_CRATE207], 2.0) Then
		IS16Tell("The SCP-207 crate: 24 slots, 23 bottles. -B, the testing bottle, is out on the table.", 5)
	EndIf
	If IS10Press(r\Objects[U31_ITM_WARN], 2.0) Then
		IS16Tell("INCIDENT REPORT 178-14-ALPHA: Level 4 eyes only. Below the sign someone has written: DON'T. TOUCH. THEM.", 6)
	EndIf
End Function

;--------------------------------------------------------------------------------------------- every frame
Function UpdateIndev31()
	Local k%, a#, d#, p%, dx#, dz#, it.Items
	;SCP-467's day
	If I467Cool > 0 Then I467Cool = I467Cool - FPSfactor
	;SCP-178: the entities, and the cuts once you have touched one
	If I178On Then
		If I178Base = 0 And FileType("GFX\map\props\scp178e.b3d") = 1 Then
			I178Base = LoadMesh_Strict("GFX\map\props\scp178e.b3d")
			ScaleEntity(I178Base, RoomScale, RoomScale, RoomScale)
			HideEntity(I178Base)
		EndIf
		If I178Base <> 0 Then
			If PlayerRoom <> I178Room Then
				I178Room = PlayerRoom
				For k = 0 To 3
					If I178E(k) = 0 Then I178E(k) = CopyEntity(I178Base)
					a = Rnd(360)
					d = Rnd(2.2, 3.6)
					PositionEntity(I178E(k), EntityX(Collider) + d * Cos(a), EntityY(Collider), EntityZ(Collider) + d * Sin(a))
					If LinePick(EntityX(I178E(k)), EntityY(Collider), EntityZ(I178E(k)), 0, -3.0, 0) <> 0 Then
						PositionEntity(I178E(k), EntityX(I178E(k)), PickedY(), EntityZ(I178E(k)))
					EndIf
				Next
			EndIf
			For k = 0 To 3
				If I178E(k) <> 0 Then
					ShowEntity(I178E(k))
					dx = EntityX(Collider) - EntityX(I178E(k)) : dz = EntityZ(Collider) - EntityZ(I178E(k))
					d = Sqr(dx * dx + dz * dz)
					RotateEntity(I178E(k), 0, CurveAngle(VectorYaw(dx, 0, dz), EntityYaw(I178E(k)), 30.0), 0)
					If d < 1.3 And d > 0.01 Then TranslateEntity(I178E(k), -dx / d * 0.006 * FPSfactor, 0, -dz / d * 0.006 * FPSfactor)
					If I178Cut <= 0 And KillTimer >= 0 Then
						If d < 0.5 Then
							U31Cut("You brush against something you can see and nothing else can.")
						ElseIf MouseHit1 And EntityDistance(Camera, I178E(k)) < 2.5 And EntityInView(I178E(k), Camera) Then
							U31Cut("You reach out towards it.")
						EndIf
					EndIf
				EndIf
			Next
		EndIf
	Else
		For k = 0 To 3
			If I178E(k) <> 0 Then HideEntity(I178E(k))
		Next
		I178Room = Null
	EndIf
	If I178Cut > 0 And KillTimer >= 0 Then
		I178Cut = I178Cut - FPSfactor
		If I178Cut <= 0 Then
			I178Cuts = I178Cuts + 1
			Injuries = Injuries + 0.55 : Bloodloss = Min(100, Bloodloss + 9) : CameraShake = 2.0
			IS10Sound("SFX\Indev\thump.wav", Collider, 4.0, 0.9)
			If I178Cuts >= 6 Then
				DeathMSG = "Subject D-9341 was found wearing SCP-178, covered in deep parallel lacerations in sets of three. No witness saw or heard anything. Incident Report 178-14-Alpha has been updated."
				Kill()
			Else
				I178Cut = 70 * 1.2
				IS16Tell("Three long cuts open across you at once. Then three more. Nobody is there.", 3)
			EndIf
		EndIf
	EndIf
	;SCP-198: the bond, the hunger, and it will not stay dropped
	If I198Ask > 0 Then I198Ask = I198Ask - FPSfactor
	If I198Bond And KillTimer >= 0 Then
		If U30Has("scp198") = Null Then
			For it = Each Items
				If it\itemtemplate\name = "scp198" And (Not it\Picked) Then
					PickItem(it)
					IS16Tell("You let go. It doesn't. The mug is still fused to your hand.", 4)
					Exit
				EndIf
			Next
		EndIf
		I198Hunger = I198Hunger - FPSfactor
		If I198Hunger <= 0 Then
			I198Hunger = 0
			I198Starve = I198Starve + FPSfactor
			Stamina = Min(Stamina, 20)
			Injuries = Injuries + 0.0012 * FPSfactor
			If I198Starve > 70 * 20 And I198Starve - FPSfactor <= 70 * 20 Then IS16Tell("Your skin is drying, your cheeks hollow. The cup is full. You know what it wants.", 6)
			If I198Starve > 70 * 70 Then
				DeathMSG = "Subject D-9341 died of dehydration and emaciation with SCP-198 bonded to the right hand, full. The bond released on death; Containment Protocol 198 was concluded."
				Kill()
			EndIf
		EndIf
	EndIf
	;SCP-207: no rest, faster and faster, then the body fails
	If I207On And KillTimer >= 0 Then
		I207T = I207T + FPSfactor
		Stamina = 100
		I207Boost = Min(0.25 + I207T / (70 * 60) * 0.25, 1.0)
		If I207T > 70 * 180 Then
			Injuries = Injuries + 0.0009 * FPSfactor
			If I207T - FPSfactor <= 70 * 180 Then IS16Tell("You misjudge a step and slam into the wall. Your heart is going like a drill. You can't slow down.", 6)
		EndIf
		If I207T > 70 * 300 Then
			DeathMSG = "Subject D-9341 died of massive organ failure some five minutes after ingesting SCP-207-1. Witnesses describe the subject as 'too fast to follow'."
			Kill()
		EndIf
	EndIf
	;SCP-1079: the sitting ends after a minute and a half without a sweet
	If I1079Win > 0 Then
		I1079Win = I1079Win - FPSfactor
		If I1079Win <= 0 Then I1079Count = 0
	EndIf
	;SCP-1650: oleander
	If I1650Pour > 0 Then I1650Pour = I1650Pour - FPSfactor
	If I1650Poison > 0 And KillTimer >= 0 Then
		I1650Poison = I1650Poison - FPSfactor
		CameraShake = Max(CameraShake, 1.5) : BlurTimer = Max(BlurTimer, 70)
		If I1650Poison <= 0 Then
			k = Rand(100)
			If k <= 87 Then
				DeathMSG = "Subject D-9341 died of severe oleandrin poisoning after drinking oil poured from SCP-1650 at 50 degrees. No oleandrin was present in the vessel."
				Kill()
			ElseIf k <= 99 Then
				IndevMemory = Min(100, IndevMemory + 35) : BlurTimer = 70 * 10
				IS16Tell("The seizures stop. You are alive. Whole pieces of you are missing - words, faces, why you are here.", 8)
			Else
				IS16Tell("The shaking stops. Nothing else happens. You are the one in a hundred.", 6)
			EndIf
		EndIf
	EndIf
End Function

Function U31Cut(why$)
	I178Cut = 70 * 0.6
	I178Cuts = 0
	IS16Tell(why + " Something moves faster than you can see.", 4)
End Function

;--------------------------------------------------------------------------------------------- items
Function IndevUse31(it.Items)
	Local n% = 0
	Select it\itemtemplate\name
		Case "scp178"
			I178On = Not I178On
			If I178On Then
				IS16Tell("You put on the 3-D glasses. The room is full of them - tall, thin, leaning in to watch you. Don't touch them.", 7)
			Else
				IS16Tell("You take off the glasses. The room is empty again. You know it isn't.", 5)
			EndIf
		Case "scp198"
			If I198Bond Then
				I198Hunger = 70 * 80 : I198Starve = 0
				IndevStress = Min(100, IndevStress + 6)
				Stamina = 100
				IS16Tell("You drink. It's " + I198Fluid + ". Warm. You keep it down. It is already filling again.", 6)
			ElseIf I198Ask > 0 Then
				I198Bond = True : I198Ask = 0
				I198Hunger = 70 * 80 : I198Starve = 0
				Select Rand(5)
					Case 1 : I198Fluid = "sweat"
					Case 2 : I198Fluid = "saliva"
					Case 3 : I198Fluid = "blood"
					Case 4 : I198Fluid = "bile"
					Default : I198Fluid = "something you won't name"
				End Select
				Indev31Uses = Indev31Uses + 1
				BlurTimer = Max(BlurTimer, 70 * 2)
				IS16Tell("A searing pain through your palm - the mug is part of your hand now. It fills from the bottom up with " + I198Fluid + ".", 8)
			Else
				I198Ask = 70 * 5
				IS16Tell("A white mug with blue stripes. 'Under no circumstances are personnel to handle SCP-198.' (Use again to pick it up anyway.)", 6)
			EndIf
		Case "scp207"
			If Not I207On Then
				I207On = True : I207T = 0
				Indev31Uses = Indev31Uses + 1
				IS16Tell("Sweet, flat, far too strong. Your tiredness simply leaves. Everything around you seems to slow down.", 6)
			Else
				IS16Tell("You drink more. Nothing more happens - five millilitres was already enough.", 4)
			EndIf
		Case "scp1079"
			If I1079Left <= 0 Then
				IS16Tell("The packet is empty. 'Only one sweet is to be taken per sitting.'", 4)
			Else
				I1079Left = I1079Left - 1
				If I1079Win > 0 Then
					I1079Count = I1079Count + 1
				Else
					I1079Count = 1
				EndIf
				I1079Win = 70 * 90
				Indev31Uses = Indev31Uses + 1
				Select I1079Count
					Case 1
						Bloodloss = Min(100, Bloodloss + 3)
						IS16Tell("A tingle. Then pink, bubblegum-scented foam seeps from your arms and back. It's your blood. Not much.", 6)
					Case 2
						Bloodloss = Min(100, Bloodloss + 12)
						IS16Tell("Much more foam this time. Your sleeves are soaked pink. Your heart pounds.", 6)
					Case 3
						Bloodloss = Min(100, Bloodloss + 32) : BlurTimer = Max(BlurTimer, 70 * 6)
						IS16Tell("Your blood fizzes. You can feel it boiling in your veins. One more would be the end.", 7)
					Default
						If Rand(100) <= 95 Then
							DeathMSG = "Subject D-9341 died of exsanguination after eating four or more SCP-1079 sweets in one sitting; the lungs were full of pink, bubblegum-scented foam."
							Kill()
						Else
							Bloodloss = 90
							IS16Tell("You should be dead. You are covered in pink foam and very nearly empty, but you are breathing.", 7)
						EndIf
				End Select
			EndIf
		Case "scp1650"
			If I1650Pour > 0 And I1650Ang > 0 Then
				I1650Pour = 0
				Indev31Uses = Indev31Uses + 1
				Select I1650Ang
					Case 1
						Injuries = Max(0, Injuries - 0.4)
						IS16Tell("Olive oil, the finest you have ever tasted. Your cuts ache less.", 5)
					Case 2
						I1650Poison = 70 * 8
						IS16Tell("It tastes exactly like the olive oil. Then your stomach turns over, and your heart stumbles.", 6)
					Case 3
						IS16Tell("You gag on the clear oil. It isn't food. It would burn in a lamp for days - without heat, without air.", 6)
					Default
						DeathMSG = "Subject D-9341 swallowed the red oil of SCP-1650 (90 degrees). Every trace of blood in the body was erased within seconds."
						Kill()
				End Select
			Else
				I1650Ang = (I1650Ang + 1) Mod 5
				I1650Pour = 70 * 4
				Select I1650Ang
					Case 0 : IS16Tell("You stand the pot upright. Empty. It will fill again, in time.", 4)
					Case 1 : IS16Tell("45 degrees. After half a minute golden olive oil pours from the spout. (Use again to drink.)", 5)
					Case 2 : IS16Tell("50 degrees. The same golden oil - it looks identical. (Use again to drink.)", 5)
					Case 3 : IS16Tell("65 degrees. A clear, thin oil. (Use again to drink.)", 5)
					Default : IS16Tell("90 degrees. A red oil, the colour of everlasting flowers. It stings your fingers. (Use again to drink.)", 6)
				End Select
				If I1650Ang = 4 Then Injuries = Injuries + 0.05
			EndIf
	End Select
	SelectedItem = Null
End Function
