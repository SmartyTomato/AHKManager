#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

#Persistent  ; Keep the script running until the user exits it.
Menu, tray, add  ; Creates a separator line.
Menu, tray, add, Item1, MenuHandler  ; Creates a new menu item.
return

MenuHandler:
MsgBox You selected %A_ThisMenuItem% from menu %A_ThisMenu%.
return