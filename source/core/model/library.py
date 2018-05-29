import os
import sys
from shutil import copyfile

from core.utility.logger import Logger
from core.utility.utility import (get_file_name, get_file_name_no_extension,
                                  get_files_in_directory, get_parent_directory,
                                  is_script_file)
from core.model.global_variable import GlobalVariable
from core.model.script import Script
from core.model.state import State


class Library(object):

    def __init__(self):
        self.script_list = []
        self.title = ''
        self.library_path = ''
        self.status = State()

    def init(self):
        """
        initialize library
        :return: void
        """
        self.script_list = []
        self.title = ''
        self.library_path = ''
        self.status = State()

    def init_library(self, path):
        """
        initialize library with given path
        :param path: directory path
        :return: bool, whether success
        """
        Logger.log_info('Initialize library >>> {path}'.format(path=path))

        # check whether path is a valid directory
        if not os.path.isdir(path):
            GlobalVariable.add_error_message('Path is not a directory path >>> {path}'.format(path=path))
            return False

        # check whether path exists
        if not os.path.exists(path):
            GlobalVariable.add_error_message('Path does not exists >>> {path}'.format(path=path))
            return False

        self.init()
        self.title = get_file_name_no_extension(path)
        self.library_path = os.path.normpath(path)

        # add script in the directory into the list
        files = get_files_in_directory(path)

        # initialize script file
        for file in files:
            if is_script_file(file):
                script = Script()

                # only add script when no error returned.
                if script.init_script(file):
                    self.script_list.append(script)
            else:
                # add warning when file is not script
                GlobalVariable.add_warning_message('Path is not a script file >>> {path}'.format(path=path))

        return True

    # ------------------------------------------------------------------ #
    # add
    # ------------------------------------------------------------------ #

    def add_script(self, path):
        """
        add script into the library
        the file has to be script file and then copied to the library
        :param path: file path
        :return: bool whether success
        """
        Logger.log_info('Add script to library >>> Script: {script_path} | Library: {library_path}'.format(
            script_path=path, library_path=self.library_path))

        # This directory is missing
        if not self.exists():
            GlobalVariable.add_error_message('Library path does not exists >>> {path}'.format(path=self.library_path))
            return False

        # check whether path is a file before copy the file to the directory
        if not os.path.isfile(path):
            GlobalVariable.add_error_message('Path is not a file >>> {path}'.format(path=path))
            return False

        if not is_script_file(path):
            GlobalVariable.add_error_message('Path is not a script file >>> {path}'.format(path=path))
            return False

        # generate script path in the library
        file_name = get_file_name(path)
        script_path = os.path.join(self.library_path, file_name)

        # copy script file into library folder
        try:
            copyfile(path, script_path)
        except OSError as error:
            GlobalVariable.add_error_message('Unable to copy file >>> From: {from_path} | To: {to} | Error: {error}'.format(
                from_path=path, to=script_path, error=error))

        # initialize script with the new file path
        script = Script()

        if not script.init_script(script_path):
            return False

        self.script_list.append(script)
        return True

    # ------------------------------------------------------------------ #
    # find
    # ------------------------------------------------------------------ #

    def find_script(self, path):
        """
        find script with the given path
        :param path: file path
        :return: Script object or None
        """
        Logger.log_info('Find script >>> {path}'.format(path=path))

        # below statement will benefit when large amount script in the library
        # if path name not containing folder name, not possible exists in this library
        if not self.may_contains_script(path):
            Logger.log_info(
                'Library never contains script, script is not in library directory >>> Library: {library_path} | Script: {script_path}'.format(
                    library_path=self.library_path, script_path=path))
            return None

        # if path is not script file name, not possible exists in this library
        if not is_script_file(path):
            Logger.log_info('Path is not a script file'.format(path=path))
            return None

        # loop to find the script
        for script in self.script_list:
            if script.has_path(path):
                return script

        Logger.log_info('Script not found')
        return None

    def find_all_running_scripts(self):
        Logger.log_info('Find all running scripts for library >>> {path}'.format(path=self.library_path))
        scripts = []

        for script in self.script_list:
            if script.is_running():
                scripts.append(script)

        return scripts

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    def remove(self):
        """
        remove library
        :return: void
        """
        Logger.log_info('Remove library >>> {path}'.format(path=self.library_path))

        has_error = False

        # remove all script as well
        for script in self.script_list:
            success = script.remove()
            if not success:
                has_error = True

        if has_error:
            GlobalVariable.add_error_message(
                'Unable to remove library, some script can not be removed >>> {path}'.format(path=self.library_path))
            return False

        self.status.exclude = True
        self.status.hide = True
        return True

    def remove_script(self, path):
        """
        remove script
        :return: void
        """
        Logger.log_info('Remove script >>> {path}'.format(path=path))

        script = self.find_script(path)

        if script is None:
            Logger.log_info('Unable to remove script, script not in library')
            return True

        return script.remove(path)

    def delete(self):
        """
        delete library
        :return: bool, whether success
        """
        Logger.log_info('Delete library >>> {path}'.format(path=self.library_path))

        # if folder not exists, nothing should be done
        if not self.exists():
            Logger.log_info('Library path does not exist >>> {path}'.format(path=self.library_path))
            return True

        has_error = False

        # delete scripts in the library
        for script in self.script_list:
            success = script.delete()

            # remove script from the list when script is deleted successfully
            if success:
                self.script_list.remove(script)
            else:
                has_error = True

        # do not delete library when any file unable to delete or script list has items.
        if has_error or self.script_list:
            GlobalVariable.add_error_message(
                'Unable to delete library, some script can not be deleted >>> {path}'.format(path=self.library_path))
            return False

        # delete directory when no error occurs
        try:
            os.rmdir(self.library_path)
        except OSError as error:
            GlobalVariable.add_error_message(
                'Unable to delete folder >>> Library path: {path} | Error: {error}'.format(path=self.library_path, error=error))
            return False
        except BaseException:
            # unknown error
            GlobalVariable.add_error_message('Unknown error when delete folder {path}. {error}'.format(
                path=self.library_path, error=sys.exc_info()[0].value))
            return False

        return True

    def delete_script(self, path):
        """
        delete script with given path
        :param path: file path
        :return: bool, whether success
        """
        Logger.log_info('Delete script >>> {path}'.format(path=path))

        script = self.find_script(path)

        if script is None:
            # library don't contains script
            Logger.log_info('Script does not exists in library >>> Script: {script_path}. Library: {library_path}'.format(
                script_path=path, library_path=self.library_path))
            return True

        if not script.delete():
            return False

        # only remove from the list when no error occurs
        Logger.log_info('Script deleted from library: Script: {script_path}. Library: {library_path}'.format(
            script_path=path, library_path=self.library_path))
        self.script_list.remove(script)
        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    def refresh(self):
        """
        refresh library status and all scripts
        :return: bool, whether success
        """
        if not self.exists():
            GlobalVariable.warning_messages.append(
                'Library does not exists: {path}'.format(path=self.library_path))
            return False

        # fresh all script in the library
        # remove script that is not found
        for script in self.script_list:
            success = script.refresh()

            # remove from the script list script failed to refresh
            if not success:
                self.script_list.remove(script)

        # insert additional script in the folder
        # add script in the directory into the list
        files = get_files_in_directory(self.library_path)

        # initialize script file
        for file in files:
            # check whether script already loaded in the library
            found = self.find_script(file)
            if found:
                continue

            if is_script_file(file):
                script = Script()
                success = script.init_script(file)

                # only add script when no error returned
                if success:
                    self.script_list.append(script)
            else:
                # add warning when file is not script
                GlobalVariable.warning_messages.append(
                    'Path not a script file: {path}'.format(path=file))

        Logger.log_info('Library refreshed: {path}'.format(
            path=self.library_path))
        return True

    # ------------------------------------------------------------------ #
    # others
    # ------------------------------------------------------------------ #

    def show(self):
        """
        should show library or not
        :return: bool
        """
        return not (self.status.exclude and self.status.hide)

    def has_path(self, path):
        return self.library_path == os.path.normpath(path)

    def exists(self):
        return os.path.exists(self.library_path)

    def may_contains_script(self, path):
        return self.library_path == os.path.normpath(get_parent_directory(path))

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    def __str__(self):
        """
        to string
        :return: single string value include library and all scripts
        """
        out = ['Library:\n\tTitle: {library}\n\tPath: {path}\n'.format(library=self.title, path=self.library_path)]

        for script in self.script_list:
            out.append(script.__str__())

        return '\n'.join(out)

    def to_json(self):
        out = {}
        out['library_path'] = self.library_path
        out['title'] = self.title
        out['status'] = self.status.to_json()

        out['scripts'] = []
        for script in self.script_list:
            out['scripts'].append(script.to_json())

        return out

    @staticmethod
    def from_json(jstr):
        library = Library()
        library.library_path = jstr['library_path']
        library.title = jstr['title']
        library.status = State.from_json(jstr['status'])

        for script in jstr['scripts']:
            library.script_list.append(Script.from_json(script))

        return library
