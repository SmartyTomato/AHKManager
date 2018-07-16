# Design
***

## Definitions
Word | Desctription
--- | ---
AHK | AutoHotKey
test | test

## Programming language
Python

## Scope
This application used for manage script for AutoHotKey. Intended to provide simple UI to manage multi profiles and repository to the user.

## Functionalities
1. Export settings to a file
2. Import old settings
3. Organize AHK into local folders
4. Create profile, be able to create, quick switch between many profile either use 
5. Create easy accessible UI
6. Auto start script on system start

## Major components
- RepositoryManager - file management class. Read and write files (script files) and manage folders
  - Script - the script file in the repository.
  - ScriptFile
- ConfigManager - configuration management class. Read and write settings
- Setting - class to store all settings
  - ProfileSetting - list of profiles
- ScriptManager - actually manages scripts
	- Scripts - list of scripts
- UI
	- Tree view - to display all the profiles
	- List view - to display a list of script in that profiles
	- Menu
    - Add - add script to repository
		- Remove - remove script from the repository but won delete the file
	  - Delete - delete the local file
 
## Requirements
Single script should be able to assign to multiply profile instead store multiple copies
Always have "All" available to display all scripts.
Auto start script in a separate view or tab. An script should be able to mark as startup instead only available for profiles.
Configuration manager should allow to export, import and save user settings for profile
Scripts should have unique name in repository

## Planned feature
1. Multiple repository support
	  - For example, one for work and one for home
2. Simple edit function
	  - Allow edit simple key press use interface instead dealing with script itself
3. Edit support complex UI
4. Backup profile to an account. Cloud access
5. Profile link to focused application

## UI design
This section will post all UI screenshots that ideal for the application

