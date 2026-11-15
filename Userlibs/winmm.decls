; Windows system DLLs export stdcall functions under their UNDECORATED names,
; so the aliases here carry no @N byte-count suffix. Getting that wrong is
; what produces "Function <name> not found" at compile time.
;
; Blitz3D only reads userlibs at IDE start - restart BlitzX3D after editing.

.lib "winmm.dll"

waveInGetNumDevs%():"waveInGetNumDevs"
waveInGetDevCapsA%(uDeviceID%, pwic*, cbwic%):"waveInGetDevCapsA"
waveInOpen%(phwi*, uDeviceID%, pwfx*, dwCallback%, dwInstance%, fdwOpen%):"waveInOpen"
waveInPrepareHeader%(hwi%, pwh*, cbwh%):"waveInPrepareHeader"
waveInUnprepareHeader%(hwi%, pwh*, cbwh%):"waveInUnprepareHeader"
waveInAddBuffer%(hwi%, pwh*, cbwh%):"waveInAddBuffer"
waveInStart%(hwi%):"waveInStart"
waveInStop%(hwi%):"waveInStop"
waveInReset%(hwi%):"waveInReset"
waveInClose%(hwi%):"waveInClose"

.lib "kernel32.dll"

; Returns the address of its destination buffer, which is how we hand a
; Blitz3D bank address to WAVEHDR.lpData. Called with n = 1 before any audio
; is captured, so the single NUL it writes is harmless.
BankAddress%(dest*, src*, n%):"lstrcpynA"
