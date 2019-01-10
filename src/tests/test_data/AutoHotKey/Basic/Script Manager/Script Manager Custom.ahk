#NoEnv  						; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  						; Enable warnings to assist with detecting common errors.
SendMode Input  				; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  	; Ensures a consistent starting directory.

#SingleInstance force
DetectHiddenWindows, On	;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Define global variables

Global ActiveControl := ""
Global SelectedItemPath := ""


; Create image lists and populate it with icons for later use in GUI.
Global TreeImageList := IL_Create(4)		; Create an ImageList to hold 4 icons.
IL_Add(TreeImageList, "shell32.dll", 4)	; 'Folder' icon.
IL_Add(TreeImageList, "shell32.dll", 80)	; 'Logical disk' icon.
IL_Add(TreeImageList, "shell32.dll", 27)	; 'Removable disk' icon.
IL_Add(TreeImageList, "shell32.dll", 206)	; 'Folder with bookmarks' icon.

Global ScriptImageList := IL_Create(6)									; Create an ImageList to hold 5 icons.
IL_Add(ScriptImageList, A_AhkPath ? A_AhkPath : A_ScriptFullPath, 1)		; '[H]' default green AHK icon with letter 'H'.
IL_Add(ScriptImageList, A_AhkPath ? A_AhkPath : A_ScriptFullPath, 3)		; '[S]' default green AHK icon with letter 'S'.
IL_Add(ScriptImageList, A_AhkPath ? A_AhkPath : A_ScriptFullPath, 4)		; '[H]' default red AHK icon with letter 'H'.
IL_Add(ScriptImageList, A_AhkPath ? A_AhkPath : A_ScriptFullPath, 5)		; '[S]' default red AHK icon with letter 'S'.
IL_Add(ScriptImageList, "shell32.dll", 21)								; A sheet with a clock (suspended process).
IL_Add(ScriptImageList, "imageres.dll", 12)								; A program's window (default .exe icon).

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Main


; Event
;OnExit("ExitApp")


; GUI
CreateGUI()


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

CreateGUI()
{
	#Persistent

	
	; Create tray menu
	Menu, Tray, NoStandard						; Remove all standard items from tray menu.
	Menu, Tray, Add	
	Menu, Tray, Add, Manage Scripts, ShowGui	; Create a tray menu's menuitem and bind it to a label that opens main window.
	Menu, Tray, Default, Manage Scripts			; Set 'Manage Scripts' menuitem as default action (will be executed if tray icon is left-clicked).
	Menu, Tray, Add								; Add an empty line (divider).
	Menu, Tray, Standard						; Add all standard items to the bottom of tray menu.
	
	
	; Create main window
	Gui, Add, StatusBar,,	; Add status bar at the bottom of the window					
	
	
	; Create tree view
	Gui, Add, TreeView, ImageList%TreeImageList%	; Create tree view to select folder.	

	; Create disks
	DriveGet, fixedDrivesList, List, FIXED
	
	TreeRoot = %A_WorkingDir%
	AddSubFoldersToTree(TreeRoot,TV_Add("",ParentItemID, "Icon4"))
			
	TV_Modify(TV_GetNext(), "Select")				; Forcefully select topmost item in the TV.
	
	
	; Show GUI
	Gui, Show, w1000 h800 Center
}

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Implementation of methods

ShowGui()
{
	
}

OnExit(command)
{
	Exit
}

AddSubFoldersToTree(folder, parentItemId = 0)
{
	Loop %Folder%\*.*, 2  ; Retrieve all of Folder's sub-folders.
		AddSubFoldersToTree(A_LoopFileFullPath, TV_Add(A_LoopFileName, ParentItemID, "Icon4"))
}