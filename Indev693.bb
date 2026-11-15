;=====================================================================
; SCP: Containment Breach - Indev SCP-693 "The Knotty Stalker"
;
;   String dolls in four colours (scp693r / scp693b / scp693y / scp693k).
;   Use an unbound doll: you thread one of your own hairs through the
;   loop and it binds to you (item state = 1, state2 = time left).
;   While it mimics you (the "nine days" - nine minutes here), using it
;   again makes it whisper the truth: the nearest danger, which way, how far.
;   When the time runs out it turns and lies, and starts working on you
;   by its colour, every so often:
;     red     anger    - stress spikes, the view shakes, you can't keep still
;     blue    despair  - stamina won't come back past a point, heavy blinking
;     yellow  obsession- you keep pulling it out to look at it
;     black   danger   - it tells you the threat is the safe way to go
;   Its hold weakens with distance - leave it far behind, or destroy it in
;   SCP-914 (rough / coarse), and it's over. Only one doll holds a hair
;   at a time.
;=====================================================================

Global I693Doll.Items, I693Next#, I693TalkCD#, I693Warned%

Function Indev693Reset()
	I693Doll = Null : I693Next = 0 : I693TalkCD = 0 : I693Warned = False
End Function

Function IsDoll693%(name$)
	Return (name = "scp693r" Or name = "scp693b" Or name = "scp693y" Or name = "scp693k")
End Function

Function Doll693Colour$(name$)
	Return Right(name, 1)
End Function

;0 = no bound doll, 1 = mimicking, 2 = turned
Function Doll693Stage%()
	If I693Doll = Null Then Return 0
	If I693Doll\state < 1 Then Return 0
	If I693Doll\state2 > 0 Then Return 1
	Return 2
End Function

;how strongly a turned doll reaches you: full while carried or close, nothing past ~24 units
Function Doll693Hold#()
	If I693Doll = Null Then Return 0
	Local n%
	For n = 0 To MaxItemAmount - 1
		If Inventory(n) = I693Doll Then Return 1.0
	Next
	If I693Doll\Picked Then Return 1.0
	Local d# = EntityDistance(I693Doll\collider, Collider)
	Return Max(0, Min(1, 1.0 - (d - 6.0) / 18.0))
End Function

;the nearest active danger: returns its name and sets the globals below
Global I693ThreatDist#, I693ThreatYaw#
Function Doll693Threat$()
	Local best$ = "", d#
	I693ThreatDist = 99999
	If Curr173 <> Null Then
		d = EntityDistance(Collider, Curr173\Collider)
		If d < I693ThreatDist Then I693ThreatDist = d : best = "the statue" : I693ThreatYaw = DeltaYaw(Camera, Curr173\Collider)
	EndIf
	If Curr106 <> Null Then
		If Curr106\State <= 0 And (Not Curr106\Idle) And (Not Contained106) Then
			d = EntityDistance(Collider, Curr106\Collider)
			If d < I693ThreatDist Then I693ThreatDist = d : best = "the old man" : I693ThreatYaw = DeltaYaw(Camera, Curr106\Collider)
		EndIf
	EndIf
	If Curr096 <> Null Then
		d = EntityDistance(Collider, Curr096\Collider)
		If d < I693ThreatDist Then I693ThreatDist = d : best = "the shy one" : I693ThreatYaw = DeltaYaw(Camera, Curr096\Collider)
	EndIf
	Return best
End Function

Function Doll693Dir$(yaw#)
	If Abs(yaw) < 45 Then Return "ahead of you"
	If Abs(yaw) > 135 Then Return "behind you"
	If yaw > 0 Then Return "to your left"
	Return "to your right"
End Function

Function Doll693Far$(d#)
	If d < 6 Then Return "very close"
	If d < 16 Then Return "close"
	If d < 40 Then Return "a way off"
	Return "far away"
End Function

;called every frame while a doll is selected in the inventory
Function IndevUse693(it.Items)
	Local col$ = Doll693Colour(it\itemtemplate\name)

	If it\state < 1 Then
		If I693Doll <> Null And I693Doll <> it Then
			IndevPillMsg("You reach for a hair and stop. Another doll already has one of yours. It wouldn't like sharing.", 5)
			SelectedItem = Null
			Return
		EndIf
		it\state = 1 : it\state2 = 70*60*9
		I693Doll = it : I693Warned = False : I693Next = 70*25
		PlaySound_Strict(PickSFX(0))
		IndevPillMsg("You pull a single hair from your head and thread it through the loop. The doll's arms lift exactly as yours do.", 7)
		SelectedItem = Null
		Return
	EndIf

	If it <> I693Doll Then I693Doll = it
	If I693TalkCD > 0 Then SelectedItem = Null : Return
	I693TalkCD = 70*4

	Local threat$ = Doll693Threat()
	If Doll693Stage() = 1 Then
		;it tells the truth
		If threat = "" Then
			IndevPillMsg("The doll mouths the words with you, in your own voice: " + Chr(34) + "Nothing is hunting me right now." + Chr(34), 6)
		Else
			IndevPillMsg("The doll speaks in your voice: " + Chr(34) + "Something is " + Doll693Far(I693ThreatDist) + ", " + Doll693Dir(I693ThreatYaw) + ". It's " + threat + "." + Chr(34), 7)
		EndIf
	Else
		;turned: lies
		If threat = "" Then
			IndevPillMsg("The doll whispers in your voice: " + Chr(34) + "It's right behind you. Don't turn around." + Chr(34), 6)
			IndevStress = Min(100, IndevStress + 10)
		Else
			Select col
				Case "k"
					IndevPillMsg("The doll points, smiling: " + Chr(34) + "It's safe " + Doll693Dir(I693ThreatYaw) + ". Go that way." + Chr(34), 7)
				Default
					IndevPillMsg("The doll speaks in your voice: " + Chr(34) + "It's " + Doll693Dir(I693ThreatYaw + 180) + ", nowhere near here." + Chr(34), 7)
			End Select
		EndIf
	EndIf
	SelectedItem = Null
End Function

Function UpdateIndev693()
	If I693TalkCD > 0 Then I693TalkCD = I693TalkCD - FPSfactor

	;find a bound doll again after loading a save
	If I693Doll = Null Then
		Local i.Items
		For i = Each Items
			If IsDoll693(i\itemtemplate\name) And i\state >= 1 Then I693Doll = i : Exit
		Next
		If I693Doll = Null Then Return
	EndIf
	If KillTimer < 0 Then Return

	Local stage% = Doll693Stage()
	If stage = 1 Then
		I693Doll\state2 = Max(0, I693Doll\state2 - FPSfactor)
		If I693Doll\state2 <= 70*60 And (Not I693Warned) And Doll693Hold() > 0.5 Then
			I693Warned = True
			IndevPillMsg("The doll's movements lag a half-second behind yours now. Just for a moment.", 5)
		EndIf
		If I693Doll\state2 <= 0 Then
			I693Next = 70*8
			If Doll693Hold() > 0.2 Then IndevPillMsg("The onyx beads catch the light. The doll is still copying you, but it isn't quite copying your face any more.", 7)
		EndIf
		Return
	EndIf
	If stage <> 2 Then Return

	Local hold# = Doll693Hold()
	If hold <= 0 Then Return
	Local col$ = Doll693Colour(I693Doll\itemtemplate\name)

	;constant pull
	Select col
		Case "b"
			If Stamina > 100 - 55 * hold Then Stamina = Max(0, Stamina - FPSfactor * 0.35)
			IndevBlinkModify(1.0 + 0.35 * hold, 1)
		Case "r"
			IndevStress = Min(100, IndevStress + FPSfactor / 70.0 * 0.6 * hold)
	End Select

	I693Next = I693Next - FPSfactor * hold
	If I693Next > 0 Then Return
	I693Next = 70 * Rnd(22, 38)

	Select col
		Case "r"
			IndevStress = Min(100, IndevStress + 18 * hold)
			CameraShake = Max(CameraShake, 1.2 * hold)
			Select Rand(1, 4)
				Case 1 IndevPillMsg("Your jaw is clenched so hard it aches. Somebody did this to you. Somebody is going to pay.", 5)
				Case 2 IndevPillMsg("You slam your fist against the wall before you know you've done it.", 5)
				Case 3 IndevPillMsg("In your pocket, the red doll's arms are raised. Yours are too.", 5)
				Default IndevPillMsg("Everything in this place is out to get you. You're so angry you're shaking.", 5)
			End Select
		Case "b"
			IndevStress = Min(100, IndevStress + 12 * hold)
			BlurTimer = Max(BlurTimer, 70 * 2 * hold)
			Select Rand(1, 4)
				Case 1 IndevPillMsg("A heavy grey feeling settles over you. What's the point of any of this?", 5)
				Case 2 IndevPillMsg("Your legs don't want to move. You could just sit down here. Just for a while.", 5)
				Case 3 IndevPillMsg("The blue doll whispers in your voice that nobody is coming for you.", 5)
				Default IndevPillMsg("You can't remember the last time you felt anything but tired.", 5)
			End Select
		Case "y"
			;it wants to be looked at
			Local n%, carried% = False
			For n = 0 To MaxItemAmount - 1
				If Inventory(n) = I693Doll Then carried = True
			Next
			IndevStress = Min(100, IndevStress + 8 * hold)
			If carried And SelectedItem = Null And (Not InvOpen) And OtherOpen = Null And (Not MenuOpen) Then
				I693TalkCD = 70*2   ;don't make it talk on this forced look
				IndevPillMsg("You realise you've taken the yellow doll out again. You can't stop wanting to hold it. You put it away.", 6)
			Else
				IndevPillMsg("Your thoughts keep sliding back to the yellow doll. You want it with a hunger that isn't yours.", 6)
				If (Not carried) Then CameraShake = Max(CameraShake, 0.4)
			EndIf
		Default
			;black: pushes you toward whatever is out there
			Local threat$ = Doll693Threat()
			IndevStress = Min(100, IndevStress + 6 * hold)
			If threat <> "" Then
				IndevPillMsg("A whisper in your own voice: " + Chr(34) + "The way out is " + Doll693Dir(I693ThreatYaw) + ". Hurry." + Chr(34), 6)
			Else
				IndevPillMsg("A whisper in your own voice: " + Chr(34) + "The next door is safe. Open it." + Chr(34), 6)
			EndIf
	End Select
End Function

;SCP-914: rough/coarse unravel it for good, 1:1 re-knots it in another colour, fine pulls the hair out,
;very fine knots the hair in tight - and it wakes up already turned
Function IndevRefine693(item.Items, setting$, x#, y#, z#)
	Local col$ = Doll693Colour(item\itemtemplate\name)
	Local it2.Items, d.Decals
	Local wasBound% = (item = I693Doll)
	Select setting
		Case "rough", "coarse"
			d = CreateDecal(0, x, 8 * RoomScale + 0.010, z, 90, Rand(360), 0)
			Select col
				Case "r" EntityColor(d\obj, 196, 32, 30)
				Case "b" EntityColor(d\obj, 40, 150, 205)
				Case "y" EntityColor(d\obj, 232, 196, 40)
				Default EntityColor(d\obj, 30, 30, 30)
			End Select
			d\Size = 0.1 : ScaleSprite(d\obj, d\Size, d\Size)   ;a tangle of loose string
		Case "1:1"
			Local other$ = Mid("rbyk", Rand(1, 4), 1)
			While other = col
				other = Mid("rbyk", Rand(1, 4), 1)
			Wend
			it2 = CreateItem("scp693" + other, x, y, z)
		Case "fine"
			it2 = CreateItem("scp693" + col, x, y, z)
		Default
			it2 = CreateItem("scp693" + col, x, y, z)
			If wasBound Or I693Doll = Null Then
				it2\state = 1 : it2\state2 = 0
				I693Doll = it2 : I693Next = 70*10
			EndIf
	End Select
	If wasBound And (it2 = Null Or it2\state < 1) Then I693Doll = Null
	RemoveItem(item)
End Function
