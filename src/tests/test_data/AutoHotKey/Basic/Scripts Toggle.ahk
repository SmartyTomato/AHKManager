#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
DetectHiddenWindows, On

WM_COMMAND := 0x111
CMD_RELOAD := 65400
CMD_EDIT := 65401
CMD_PAUSE := 65403
CMD_SUSPEND := 65404

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


Process, Exist
this_pid := ErrorLevel
control_id := WinExist("ahk_class AutoHotkey ahk_pid " this_pid)

requiredState := false

; Press Control Pause to toggle Pause & Suspend state for all scripts.
^!+T::
	WinGet, id, list, ahk_class AutoHotkey
	Loop, %id%
	{
		this_id := id%A_Index%
		If (this_id <> control_id)
		{
			If (ScriptStatus(this_id, "Paused") == requiredState)
				PostMessage, WM_COMMAND, CMD_PAUSE,,, ahk_id %this_id%
			If (ScriptStatus(this_id, "Suspended") == requiredState)
				PostMessage, WM_COMMAND, CMD_SUSPEND,,, ahk_id %this_id%
		}
	}
	
	requiredState := !requiredState
return

^!+D::
	WinGet, id, list, ahk_class AutoHotkey
	Loop, %id%
	{
		this_id := id%A_Index%
		If (this_id <> control_id)
		{		
			If (!ScriptStatus(this_id, "Paused"))
				PostMessage, WM_COMMAND, CMD_PAUSE,,, ahk_id %this_id%			
			If (!ScriptStatus(this_id, "Suspended"))
				PostMessage, WM_COMMAND, CMD_SUSPEND,,, ahk_id %this_id%
		}
	}
	
	requiredState := true
return

^!+E::
	WinGet, id, list, ahk_class AutoHotkey
	Loop, %id%
	{
		this_id := id%A_Index%
		If (this_id <> control_id)
		{			
			If (ScriptStatus(this_id, "Paused"))
				PostMessage, WM_COMMAND, CMD_PAUSE,,, ahk_id %this_id%			
			If (ScriptStatus(this_id, "Suspended"))
				PostMessage, WM_COMMAND, CMD_SUSPEND,,, ahk_id %this_id%
		}
	}
	
	requiredState := false
return

^!+K::
	WinGet, List, List, ahk_class AutoHotkey 


	Loop, %List% 
	{ 
		WinGet, PID, PID, % "ahk_id " List%A_Index% 
		If ( PID <> DllCall("GetCurrentProcessId") ) 
			 PostMessage,0x111,65405,0,, % "ahk_id " List%A_Index% 
	}
return


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

ScriptStatus(script_id, cmd)
{
	SendMessage, 0x211,,,, ahk_id %script_id%  ; WM_ENTERMENULOOP
	SendMessage, 0x212,,,, ahk_id %script_id%  ; WM_EXITMENULOOP

	mainMenu := DllCall("GetMenu", "uint", script_id)
	fileMenu := DllCall("GetSubMenu", "uint", mainMenu, "int", 0)
	isPaused := DllCall("GetMenuState", "uint", fileMenu, "uint", 4, "uint", 0x400) >> 3 & 1
	isSuspended := DllCall("GetMenuState", "uint", fileMenu, "uint", 5, "uint", 0x400) >> 3 & 1
	DllCall("CloseHandle", "uint", fileMenu)
	DllCall("CloseHandle", "uint", mainMenu)
	If (cmd == "Paused")
		return isPaused
	If (cmd == "Suspended")
		return isSuspended
}