;=====================================================================
; SCP: Containment Breach - Indev SCP-2935 "O, Death"
;
;   A phased single-room anomaly sequence, built entirely from assets
;   already in the mod (StreamSound_Strict, PlaySound_Strict, Fog,
;   AmbientLight, CreateItem). No new rooms or meshes - the "discovery
;   -> transition -> abandoned reality -> evidence -> distress log ->
;   lockdown -> silence" beats all happen inside room1scp2935.
;
;   The sequence does NOT start automatically on room entry. A wall
;   button is placed right beside the radio prop (same pattern as
;   IndevMakeButton/IndevBtnNear in IndevRoomExtras.bb - proximity +
;   view-cone check, MouseHit1 to trigger). The player has to walk up
;   and click it themselves.
;
;   PHASES (state machine driven by I2935Phase):
;     0  idle - waiting for the player to click the radio button
;     1  discovery   - button clicked, radio crackles to life
;     2  static      - a few seconds of pure static, lights flicker
;     3  broadcast   - the emergency broadcast plays (Buzz.ogg stand-in
;                      for the announcer track + Msg text carries the
;                      words, since we have no VO recording)
;     4  transition  - screen darkens/fog thickens for a beat: the
;                      "space-time" crossing. Room ambience swaps from
;                      normal facility drone to near-silence + wind.
;     5  active      - the room is now "inside" SCP-2935: no NPCs, dead
;                      quiet, evidence items are live and readable.
;                      Occasional (1% per tick) stingers: static burst,
;                      distant radio, wind gust, door creak. No monster.
;     6  distress    - triggered by reading the distress log doc2935c;
;                      the actual 0313->0500 log lines print through Msg
;                      one at a time (matches source timestamps exactly)
;     7  lockdown    - after the distress phase finishes: door slams
;                      shut, emergency light reddens, alarm blip, then
;                      cuts to silence. This is the last beat.
;
;   Evidence items (new, small, meaningful - not loot):
;     item2935paper   - Hendricks County Flyer, dated Apr 19 2016
;     item2935phone   - dead Samsung Note 5, last message Apr 19 2016
;     item2935calendar- Site-81 desk calendar, last mark Apr 19 2016
;   Each CreateItem + a Use-time Msg drawn straight from source material.
;   The full documents (doc2935/b/c/d) remain for players who want the
;   complete file; the evidence items are the "find it yourself" layer.
;
;   Vanilla-first: reuses IndevStress, StreamSound_Strict/PlaySound_Strict,
;   Fog, AmbientLight, Msg/MsgTimer, CreateItem, RoomAmbience. No new
;   rooms, no new meshes beyond the 3 small evidence props.
;=====================================================================

Global I2935Room.Rooms
Global I2935CHN%, I2935Volume#
Global I2935Phase%              ;0..7, see header
Global I2935PhaseT#             ;seconds-equivalent timer within a phase
Global I2935DistressLine%       ;which distress-log line we're on
Global I2935LockdownDone%
Global I2935StingerT#           ;cooldown between rare active-phase stingers
Global I2935Radio.Items         ;the radio item itself - we click on IT

;-----------------------------------------------------------------------
; room variables, named to match the design doc 1:1 (kept as fields on
; the globals above rather than separate booleans - I2935Phase >= N
; already encodes "Discovered", "Entered", "RadioPlayed" etc, so we
; don't duplicate state. Mapping for reference:
;   SCP2935_Discovered    -> I2935Phase >= 1
;   SCP2935_Entered       -> I2935Phase >= 1  (single room, so same beat)
;   SCP2935_RadioPlayed   -> I2935Phase >= 2
;   SCP2935_BroadcastPlayed -> I2935Phase >= 3
;   SCP2935_Active        -> I2935Phase >= 5
;   SCP2935_Lockdown      -> I2935Phase >= 7
;-----------------------------------------------------------------------

Function Indev2935Reset()
	If I2935CHN <> 0 Then
		StopStream_Strict(I2935CHN)
		I2935CHN = 0
	EndIf
	I2935Room = Null
	I2935Volume = 0
	I2935Phase = 0
	I2935PhaseT = 0
	I2935DistressLine = 0
	I2935LockdownDone = False
	I2935StingerT = 0
	I2935Radio = Null
End Function

;called from PickItem (Items.bb) when the player clicks ON the radio in
;the world. Starts the sequence and returns True to tell PickItem NOT to
;pick the radio up. Returns False (rare) so the radio behaves normally if
;the sequence has already started.
Function Indev2935RadioClicked%()
	If I2935Phase = 0 Then
		I2935Phase = 1
		I2935PhaseT = 0
		PlaySound_Strict(LoadTempSound("SFX\Interact\Button2.ogg"))
		Msg = "SITE-81 SIGNAL RX - 162.475 MHz - SRC: JOPPA, TN. The radio crackles to life."
		MsgTimer = 70 * 5
		DebugLog "Indev: SCP-2935 phase 1 (discovery) - radio clicked"
		Return True
	EndIf
	;already running - clicking it again does nothing but is still not loot
	Msg = "The receiver is already running. You can hear it from here."
	MsgTimer = 70 * 3
	Return True
End Function

;called from MapSystem's Case "room1scp2935"
Function IndevFill2935(r.Rooms)
	I2935Room = r

	;--- documents, same placement as before
	Local it.Items = CreateItem("doc2935", r\x + 200.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 40.0 * RoomScale)
	If it <> Null Then EntityParent(it\collider, r\obj)

	it = CreateItem("doc2935b", r\x + 160.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 80.0 * RoomScale)
	If it <> Null Then EntityParent(it\collider, r\obj)

	it = CreateItem("doc2935c", r\x + 240.0 * RoomScale, r\y + 68.0 * RoomScale, r\z + 0.0 * RoomScale)
	If it <> Null Then EntityParent(it\collider, r\obj)

	it = CreateItem("doc2935d", r\x, r\y + 68.0 * RoomScale, r\z - 150.0 * RoomScale)
	If it <> Null Then EntityParent(it\collider, r\obj)

	;--- the radio. Clicking ON this item (vanilla item raycast -> PickItem
	;-> Indev2935RadioClicked) starts the whole SCP-2935 sequence. Placed
	;on the open floor near room centre so it's always visible and
	;reachable - the same safe placement used for the SCP-140 book, after
	;desk-height guesses kept clipping into furniture on this mesh.
	it = CreateItem("radio", r\x, r\y + 0.1, r\z + 0.4)
	If it <> Null Then
		EntityParent(it\collider, r\obj)
		I2935Radio = it
	EndIf

	;--- evidence items, small clearance offsets so nothing clips into
	;    other props. All in plain metres from room centre.
	it = CreateItem("item2935paper", r\x + 0.6, r\y + 0.1, r\z + 0.3)
	If it <> Null Then EntityParent(it\collider, r\obj)

	it = CreateItem("item2935phone", r\x - 0.6, r\y + 0.1, r\z + 0.3)
	If it <> Null Then EntityParent(it\collider, r\obj)

	it = CreateItem("item2935calendar", r\x, r\y + 0.1, r\z + 0.6)
	If it <> Null Then EntityParent(it\collider, r\obj)

	DebugLog "Indev: IndevFill2935 - SCP-2935 chamber at (" + r\x + ", " + r\y + ", " + r\z + ")"
End Function

;=========================================================== main update
Function UpdateIndev2935()
	If I2935Room = Null Then Return
	If KillTimer < 0 Then
		If I2935CHN <> 0 Then StopStream_Strict(I2935CHN) : I2935CHN = 0
		Return
	EndIf

	Local inRoom% = (PlayerRoom = I2935Room)

	;--- Phase 0: idle. The sequence is started by clicking the radio,
	;handled in PickItem -> Indev2935RadioClicked (Items.bb). We just wait.
	If I2935Phase = 0 Then Return

	;--- ambient dose / stress regardless of phase, same as before
	If inRoom Then
		IndevStress = Min(100, IndevStress + FPSfactor * 0.03)
	EndIf

	I2935PhaseT = I2935PhaseT + FPSfactor / 70.0   ;seconds

	;--- Phase 1: discovery -> static begins after ~2s
	If I2935Phase = 1 Then
		If I2935PhaseT > 2.0 Then
			I2935Phase = 2
			I2935PhaseT = 0
			I2935CHN = StreamSound_Strict("SFX\Radio\Buzz.ogg", 0.0)
			DebugLog "Indev: SCP-2935 phase 2 (static)"
		EndIf

	;--- Phase 2: pure static + light flicker for ~4s
	ElseIf I2935Phase = 2 Then
		I2935Volume = CurveValue(0.7, I2935Volume, 20.0)
		If I2935CHN <> 0 And I2935CHN <> -1 Then SetStreamVolume_Strict(I2935CHN, I2935Volume * SFXVolume)
		;flicker: cheap fake using AmbientLight jitter is risky (global), so
		;we settle for a stress tick + a screen shake pulse instead
		If I2935PhaseT > 0.5 And I2935PhaseT < 0.6 Then CameraShake = Max(CameraShake, 0.15)
		If I2935PhaseT > 4.0 Then
			I2935Phase = 3
			I2935PhaseT = 0
			Msg = "AUTOMATED EMERGENCY BROADCAST - SCP Foundation and your national government."
			MsgTimer = 70 * 5
			DebugLog "Indev: SCP-2935 phase 3 (broadcast)"
		EndIf

	;--- Phase 3: the broadcast - staged Msg lines standing in for the VO
	ElseIf I2935Phase = 3 Then
		If I2935PhaseT > 0.1 And I2935PhaseT < 0.2 Then
			Msg = "One or more Foundation sites is experiencing a communication breakdown."
			MsgTimer = 70 * 4
		EndIf
		If I2935PhaseT > 4.5 And I2935PhaseT < 4.6 Then
			Msg = "All citizens are ordered to remain indoors. Containment teams are responding."
			MsgTimer = 70 * 4
		EndIf
		If I2935PhaseT > 9.0 And I2935PhaseT < 9.1 Then
			Msg = "This message will continue until-"
			MsgTimer = 70 * 3
		EndIf
		If I2935PhaseT > 11.0 Then
			I2935Phase = 4
			I2935PhaseT = 0
			If I2935CHN <> 0 Then StopStream_Strict(I2935CHN) : I2935CHN = 0
			Msg = "[SIGNAL LOST]"
			MsgTimer = 70 * 3
			DebugLog "Indev: SCP-2935 phase 4 (transition)"
		EndIf

	;--- Phase 4: the space-time crossing. Fog thickens briefly, then the
	;    room settles into its "active" (dead-world) ambience.
	ElseIf I2935Phase = 4 Then
		If I2935PhaseT > 0.0 And I2935PhaseT < 3.0 Then
			CameraFogMode(Camera, 1)
			CameraFogRange(Camera, CameraFogNear * 0.3, CameraFogFar * 0.3)
		Else
			CameraFogRange(Camera, CameraFogNear, CameraFogFar)
		EndIf
		If I2935PhaseT > 3.0 Then
			I2935Phase = 5
			I2935PhaseT = 0
			Msg = "The air changes. The facility hum is gone. You can hear your own heartbeat."
			MsgTimer = 70 * 6
			DebugLog "Indev: SCP-2935 phase 5 (active - dead world)"
		EndIf

	;--- Phase 5: active. Dead quiet, rare stingers, no monster.
	ElseIf I2935Phase = 5 Then
		Local want# = 0
		If inRoom Then want = 0.12   ;very low ambience once "active"
		I2935Volume = CurveValue(want, I2935Volume, 20.0)
		If I2935Volume < 0.01 Then
			If I2935CHN <> 0 Then StopStream_Strict(I2935CHN) : I2935CHN = 0
		Else
			If I2935CHN = 0 Then I2935CHN = StreamSound_Strict("SFX\Radio\Buzz.ogg", 0.0)
			If I2935CHN <> 0 And I2935CHN <> -1 Then SetStreamVolume_Strict(I2935CHN, I2935Volume * SFXVolume)
		EndIf

		;rare stingers: ~1% chance per second while the player is in the room
		If inRoom Then
			I2935StingerT = I2935StingerT + FPSfactor / 70.0
			If I2935StingerT > 1.0 Then
				I2935StingerT = 0
				If Rand(1, 100) <= 1 Then
					Select Rand(1, 4)
						Case 1 Msg = "[STATIC]" : MsgTimer = 70 * 2
						Case 2 Msg = "[VERY DISTANT RADIO]" : MsgTimer = 70 * 2
						Case 3 Msg = "[WIND]" : MsgTimer = 70 * 2
						Case 4 PlaySound_Strict(LoadTempSound("SFX\Radio\Buzz.ogg"))
					End Select
				EndIf
			EndIf
		EndIf

		;phase 6 (distress log) is triggered externally, from doc2935c's
		;pickup/read in IndevPills.bb - see Indev2935TriggerDistress()

	;--- Phase 6: distress log, one line every ~2.2s, matches source
	;    timestamps exactly
	ElseIf I2935Phase = 6 Then
		Local lines$[11]
		lines[0]  = "0313 - MASSIVE TRANSMITTER ERROR, REQUESTING MAINTENANCE"
		lines[1]  = "0314 - MASSIVE TRANSMITTER ERROR, REQUESTING MAINTENANCE"
		lines[2]  = "0315 - POSSIBLE BREACH OF CONTAINMENT, REQUESTING MAINTENANCE"
		lines[3]  = "0316 - (To Site-81 Command) TRANSMITTER ERROR, PLEASE ADVISE"
		lines[4]  = "0321 - (To Site-81 Command) TRANSMITTER ERROR, PLEASE ADVISE"
		lines[5]  = "0326 - BEGINNING LOCKDOWN PROCEDURES. SITE WILL LOCKDOWN IN 10 MINUTES"
		lines[6]  = "0331 - SITE WILL LOCKDOWN IN 5 MINUTES"
		lines[7]  = "0335 - SITE WILL LOCKDOWN IN 1 MINUTE"
		lines[8]  = "0336 - SITE LOCKDOWN COMPLETE. PLEASE ADVISE."
		lines[9]  = "0400 - (To Site-17) TRANSMITTER ERROR. LOCKDOWN INITIATED. ADVISE."
		lines[10] = "0500 - (To Overwatch) MULTIPLE SITES UNRESPONSIVE. ADVISE."

		If I2935PhaseT > 2.2 Then
			I2935PhaseT = 0
			If I2935DistressLine <= 10 Then
				Msg = lines[I2935DistressLine]
				MsgTimer = 70 * 3
				I2935DistressLine = I2935DistressLine + 1
			Else
				I2935Phase = 7
				I2935PhaseT = 0
				DebugLog "Indev: SCP-2935 phase 7 (lockdown)"
			EndIf
		EndIf

	;--- Phase 7: lockdown. Door slams (if we have one), red light pulse,
	;    alarm blip, then silence forever.
	ElseIf I2935Phase = 7 Then
		If Not I2935LockdownDone Then
			I2935LockdownDone = True
			PlaySound_Strict(LoadTempSound("SFX\Alarm\Alarm.ogg"))
			CameraShake = Max(CameraShake, 0.3)
			Msg = "[LOCKDOWN COMPLETE]"
			MsgTimer = 70 * 4
			If I2935CHN <> 0 Then StopStream_Strict(I2935CHN) : I2935CHN = 0
		EndIf
		;stays here forever - the room goes properly silent from here on
	EndIf
End Function

;called from IndevPills.bb when the player reads doc2935c (the distress
;log document) for the first time, to kick off phase 6 if we're already
;in the "active" dead-world phase
Function Indev2935TriggerDistress()
	If I2935Phase = 5 Then
		I2935Phase = 6
		I2935PhaseT = 0
		I2935DistressLine = 0
		DebugLog "Indev: SCP-2935 phase 6 (distress log) triggered by reading doc2935c"
	EndIf
End Function
