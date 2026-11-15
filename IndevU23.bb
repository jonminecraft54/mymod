;=====================================================================
; SCP: Containment Breach - Indev: twenty-third batch, SCP-6483 (Nicolas Roberts)
;
;   room2b23santa  Nick stands in his quarters in a maintenance uniform; he faces you and talks, quietly.
;                  Click the reality anchor monitor and it goes OFFLINE: a Nativitatis Event. Sleigh bells, a warm
;                  red-gold glow, Nick in a red suit; supper appears on the table (stress -20, stamina full, health
;                  a little better) and he laughs again. After 60 s, or a second click, the anchor comes back on, the
;                  glow goes, the suit goes, and he is quiet again.
;
;   EventState: frames left in the Nativitatis Event (0 = anchor active).  Flags: n Nick made.
;   A summary of scp-wiki.wikidot.com/scp-6483 (CC BY-SA 3.0).
;=====================================================================

Global Indev23Events%, Indev23Light%

Function IndevU23Dress(r.Rooms)
	Local m%, tex%
	;the OFFLINE screen, laid over the baked ACTIVE one and hidden until the anchor is switched off
	m = IS10Quad(100.0, 70.0, True, False)
	IS10OnPivot(m, r\Objects[U23_SNT_SRA])
	RotateEntity(m, 0, 90, 0)
	PositionEntity(m, 0, 0, -6 * RoomScale)
	tex = LoadTexture_Strict("GFX\map\indev_6483sraoff.png")
	EntityTexture(m, tex)
	FreeTexture(tex)
	HideEntity(m)
	r\Objects[U23_SNT_GLOW] = m
End Function

Function UpdateIndevU23(e.Events)
	Local r.Rooms = e\room, n.NPCs, d#
	If PlayerRoom <> r Then Return
	If Not IAxFlag(e, "n") Then
		IAxSetFlag(e, "n")
		r\NPC[0] = IS16Person(r, U23_SNT_NICK, 270)
		IAxSkin(r\NPC[0], "GFX\npcs\indev_tech.jpg")
	EndIf
	n = r\NPC[0]
	If IS10Press(r\Objects[U23_SNT_SRA], 2.0) Then
		If e\EventState > 0 Then e\EventState = 1 Else IndevU23Start(e)
	EndIf
	If e\EventState > 0 Then
		e\EventState = e\EventState - FPSfactor
		If e\EventState <= 0 Then IndevU23Stop(e)
	EndIf
	If n = Null Then Return
	d = EntityDistance(n\Collider, Collider)
	If d < 4.0 Then IAxFace(n, Collider)
	If d < 2.2 And MsgTimer <= 0 And Rand(500) = 1 Then
		If e\EventState > 0 Then
			Select Rand(3)
				Case 1 : IAxSay("SCP-6483", "Ho ho ho! Sit, sit! There's turkey, and there's the kind of thing your gran used to make.", 7)
				Case 2 : IAxSay("SCP-6483", "Every night was Christmas Eve, once. Just for a minute, let it be again.", 6)
				Case 3 : IAxSay("SCP-6483", "Don't tell Dr. Rivera I touched the anchor. Well - you touched it. Ho ho!", 6)
			End Select
		Else
			Select Rand(3)
				Case 1 : IAxSay("SCP-6483", "Maintenance. The vents on this floor rattle. I'll get to them.", 5)
				Case 2 : IAxSay("SCP-6483", "You can call me Nick. Most people here do now.", 5)
				Case 3 : IAxSay("SCP-6483", "I used to do the Christmas displays at hotels. They said I looked too young to be Santa.", 6)
			End Select
		EndIf
	EndIf
End Function

Function IndevU23Start(e.Events)
	Local r.Rooms = e\room, l%
	e\EventState = 70 * 60
	Indev23Events = Indev23Events + 1
	ShowEntity(r\Objects[U23_SNT_GLOW])
	l = CreateLight(2, r\Objects[U23_SNT_FIRE])
	LightRange(l, 6.0)
	LightColor(l, 255, 150, 80)
	Indev23Light = l
	If r\NPC[0] <> Null Then IAxSkin(r\NPC[0], "GFX\npcs\indev_112spirit.jpg")
	IS10Sound("SFX\Indev\jingle.wav", r\Objects[U23_SNT_TABLE], 10.0, 0.9)
	IndevStress = IndevStress - 20 : If IndevStress < 0 Then IndevStress = 0
	Stamina = 100
	Injuries = Injuries - 0.3 : If Injuries < 0 Then Injuries = 0
	IS16Tell("The monitor flickers to OFFLINE. Pine and cinnamon. Carols from nowhere. The table is set for supper, and Nick is in a red suit.", 8)
End Function

Function IndevU23Stop(e.Events)
	Local r.Rooms = e\room
	e\EventState = 0
	HideEntity(r\Objects[U23_SNT_GLOW])
	If Indev23Light <> 0 Then
		FreeEntity(Indev23Light)
		Indev23Light = 0
	EndIf
	If r\NPC[0] <> Null Then IAxSkin(r\NPC[0], "GFX\npcs\indev_tech.jpg")
	IS16Tell("The anchor hums back to ACTIVE. The supper, the glow and the suit are gone. Nick sits down, and says nothing for a while.", 7)
End Function
