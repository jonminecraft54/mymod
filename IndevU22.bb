;=====================================================================
; SCP: Containment Breach - Indev: twenty-second batch, SCP-112-PT ("Santa Claus's bones")
;
;   room2b22xmas  stand near the reliquary for ten seconds and SCP-112-PT-1 manifests beside it: an old man in a
;                 red bishop's robe. He faces you and talks; click him once for a gift (a random item, sometimes
;                 an odd one). Two minutes after he came he fades (poof), and may come again on a later visit.
;
;   EventState: frames near the reliquary / then frames until he fades.  Flags: m he is here, g gift given.
;   A summary of scp-pt-br.wikidot.com/scp-112-pt (CC BY-SA 3.0).
;=====================================================================

Global Indev22Visits%, Indev22Gifts%

Function IndevU22Dress(r.Rooms)
End Function

Function UpdateIndevU22(e.Events)
	Local r.Rooms = e\room, relic% = r\Objects[U22_XMS_RELIC], n.NPCs, d#
	If PlayerRoom <> r Then Return
	n = r\NPC[0]
	If Not IAxFlag(e, "m") Then
		If EntityDistance(Collider, relic) < 2.5 Then e\EventState = e\EventState + FPSfactor Else e\EventState = 0
		If e\EventState < 70 * 10 Then Return
		IAxSetFlag(e, "m")
		IS13Drop(e, "g")
		e\EventState = 70 * 120
		Indev22Visits = Indev22Visits + 1
		r\NPC[0] = IS16Person(r, U22_XMS_SPIRIT, 90)
		IAxSkin(r\NPC[0], "GFX\npcs\indev_112spirit.jpg")
		IS10Sound("SFX\Indev\bells.wav", relic, 8.0, 0.8)
		IS16Tell("Sleigh bells, very faint. An old man with a long white beard is standing by the reliquary, as if he had always been.", 8)
		Return
	EndIf
	If n = Null Then Return
	d = EntityDistance(n\Collider, Collider)
	If d < 4.0 Then IAxFace(n, Collider)
	If d < 2.2 And MsgTimer <= 0 And Rand(500) = 1 Then
		Select Rand(3)
			Case 1 : IAxSay("SCP-112-PT-1", "Have you been good this year? Do not answer quickly. I always know.", 6)
			Case 2 : IAxSay("SCP-112-PT-1", "They keep me in a box with a tree. It is kind of them. Myra was warmer.", 6)
			Case 3 : IAxSay("SCP-112-PT-1", "I cannot stay long. I never can. That was always the hard part.", 6)
		End Select
	EndIf
	If IS10Press(n\Collider, 2.0) Then
		If IAxFlag(e, "g") Then
			IAxSay("SCP-112-PT-1", "One gift each. That was always the rule.", 4)
		Else
			IAxSetFlag(e, "g")
			Indev22Gifts = Indev22Gifts + 1
			Select Rand(4)
				Case 1
					IS16Give("firstaid", n\Collider)
					IAxSay("SCP-112-PT-1", "For the cuts you have not got yet.", 5)
				Case 2
					IS16Give("bat", n\Collider)
					IAxSay("SCP-112-PT-1", "Batteries. Children always forgot the batteries.", 5)
				Case 3
					IS16Give("key3", n\Collider)
					IAxSay("SCP-112-PT-1", "A key. I am told I am good with doors and chimneys.", 5)
				Case 4
					IS16Give("cookie377", n\Collider)
					IAxSay("SCP-112-PT-1", "A biscuit. Read the fortune quietly; it is meant for you.", 5)
			End Select
		EndIf
	EndIf
	e\EventState = e\EventState - FPSfactor
	If e\EventState <= 0 Then
		IS10Sound("SFX\Indev\poof.wav", relic, 8.0, 0.8)
		RemoveNPC(n)
		r\NPC[0] = Null
		IS13Drop(e, "m")
		e\EventState = 0
		IS16Tell("The old man is gone. The air smells of pine and candle smoke.", 6)
	EndIf
End Function
