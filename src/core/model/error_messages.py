class ErrorMessages():

    # region library

    library_already_exists = "Library already exists, reload library: {}"
    could_not_find_library = 'Could not find library: {}'
    could_not_remove_library = 'Could not remove library: {}'
    library_path_not_exists = 'Library path does not exists: {}'
    library_path_not_exists_library_removed = \
        'Library path does not exists, library removed: {}'
    could_not_remove_library_script_can_not_be_removed = \
        'Could not remove library, some script can not be removed: {}'

    # endregion library

    # region script

    could_not_find_script = 'Could not find script: {}'
    could_not_refresh_script_script_removed = \
        'Could not refresh script, script removed: {}'
    could_not_start_locked_script = \
        'Could not start locked script: {}'
    could_not_stop_locked_script = 'Could not stop script, script locked: {}'
    could_not_stop_script = 'Could not stop script: {}'
    could_not_restart_script = 'Could not restart script: {}'
    could_not_start_script = 'Could not start script: {}'
    script_path_not_valid = 'Script path is not valid: {}'
    could_not_remove_script_could_not_stop = \
        'Could not remove script, could not stop script: {}'
    # endregion script

    # region profile

    profile_name_already_exists = 'Profile name already exists: {}'
    could_not_find_profile = 'Could not find profile: {}'
    profile_already_contains_script = 'Profile already contains script: {}'
    script_not_in_profile = \
        'Script not in profile: Profile: {profile}, Script: {script}'

    # endregion profile

    # region utility

    path_is_not_directory_path = 'Path is not a valid directory path: {}'
    directory_is_empty = 'Directory is empty: {}'
    path_is_not_script_file = 'Path is not a script file: {}'
    path_is_not_file = 'Path is not a file: {}'
    autohotkey_path_is_not_valid = 'AutoHotKey path is not valid: {}'
    could_not_open_path = 'Could not open path: {}'

    # endregion utility
