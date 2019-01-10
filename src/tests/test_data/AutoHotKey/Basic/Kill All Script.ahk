#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DetectHiddenWindows, On 
WinGet, List, List, ahk_class AutoHotkey 


Loop %List% 
  { 
    WinGet, PID, PID, % "ahk_id " List%A_Index% 
    If ( PID <> DllCall("GetCurrentProcessId") ) 
         PostMessage,0x111,65405,0,, % "ahk_id " List%A_Index% 
  }