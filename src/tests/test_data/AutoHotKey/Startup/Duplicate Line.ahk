#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

!D::
	SetKeyDelay, -1

	clipboard = 
	
	Send ^c
	ClipWait, 0.1
	
	; Get selected text if has any
	selectedText := clipboard
		
	; If nothing is selected, copy current line
	if(StrLen(selectedText) == 0)
		CopyLine()
	; If something is selected, duplicate selected text
	else
		DuplicateSelectedText()

return

CopyLine()
{
	Send {Home}{Shift Down}{End}{Shift Up}^c
	Send {End}{Enter}^v
}


DuplicateSelectedText()
{
	Send ^c
	Send ^v
	Send ^v
}