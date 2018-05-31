import os
import sys
from shutil import copyfile

from core.utility.logger import Logger, MethodBoundaryLogger
from core.utility.utility import Utility
from core.model.global_variable import GlobalVariable
from core.model.script import Script
from core.model.state import State


class Library(object):
    _logger = Logger('Library')

    def __init__(self):
        self.script_list = []
        self.title = ''
        self.library_path = ''
        self.state = State()

    def init(self):
        """
        initialize library
        :return: void
        """
        self.script_list = []
        self.title = ''
        self.library_path = ''
        self.state = State()

    @MethodBoundaryLogger(_logger)
    def init_library(self, path):
        """
        initialize library with given path
        :param path: directory path
        :return: bool, whether success
        """
        # check whether path is a valid directory
        if not os.path.isdir(path):
            GlobalVariable.error_messages.append('Path is not a directory path: {path}'.format(path=path))
            self._logger.error('Path is not a directory path >>> {path}'.format(path=path))
            return False

        # check whether path exists
        if not os.path.exists(path):
            GlobalVariable.error_messages.append('Path does not exists: {path}'.format(path=path))
            self._logger.error('Path does not exists >>> {path}'.format(path=path))
            return False

        self.init()
        self.title = Utility.get_file_name_no_extension(path)
        self.library_path = os.path.normpath(path)

        # add script in the directory into the list
        files = Utility.get_files_in_directory(path)

        # initialize script file
        for file in files:
            if Utility.is_script_file(file):
                script = Script()

                # only add script when no error returned.
                if script.init_script(file):
                    self.script_list.append(script)
            else:
                # add warning when file is not script
                GlobalVariable.warning_messages.append('Path is not a script file: {path}'.format(path=path))
                self._logger.warning('Path is not a script file >>> {path}'.format(path=path))

        return True

    # ------------------------------------------------------------------ #
    # add
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def add_script(self, path):
        """
        add script into the library
        the file has to be script file and then copied to the library
        :param path: file path
        :return: bool whether success
        """

        # This directory is missing
        if not self.exists():
            GlobalVariable.error_messages.append('Library path does not exists: {path}'.format(path=self.library_path))
            self._logger.error('Library path does not exists >>> {library}'.format(library=repr(self)))
            return False

        # check whether path is a file before copy the file to the directory
        if not os.path.isfile(path):
            GlobalVariable.error_messages.append('Path is not a file: {path}'.format(path=path))
            self._logger.error('Path is not a file >>> {path}'.format(path=path))
            return False

        if not Utility.is_script_file(path):
            GlobalVariable.error_messages.append('Path is not a script file: {path}'.format(path=path))
            self._logger.error('Path is not a script file >>> {path}'.format(path=path))
            return False

        # generate script path in the library
        file_name = Utility.get_file_name(path)
        script_path = os.path.join(self.library_path, file_name)

        # copy script file into library folder
        try:
            copyfile(path, script_path)
        except OSError as error:
            GlobalVariable.error_messages.append('Could not copy file from "{from_path}" to "{to}"'.format(
                from_path=path, to=script_path, error=error))
            self._logger.error('Could not copy file >>> From: {from_path} | To: {to} | Error: {error}'.format(
                from_path=path, to=script_path, error=error))

        # initialize script with the new file path
        script = Script()

        if not script.init_script(script_path):
            GlobalVariable.error_messages.append('Could not initialize script: {path}'.format(path=script_path))
            self._logger.error('Could not initialize script >>> {path}'.format(path=script_path))
            return False

        self.script_list.append(script)
        return True

    # ------------------------------------------------------------------ #
    # find
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def find_script(self, path):
        """
        find script with the given path
        :param path: file path
        :return: Script object or None
        """

        # below statement will benefit when large amount script in the library
        # if path name not containing folder name, not possible exists in this library
        if not self.may_contains_script(path):
            self._logger.info(
                'Library never contains script, script is not in library directory'
                ' >>> Library: {library_path} | Script: {script_path}'.format(
                    library_path=self.library_path, script_path=path))
            return None

        # if path is not script file name, not possible exists in this library
        if not Utility.is_script_file(path):
            self._logger.info('Path is not a script file >>> {path}'.format(path=path))
            return None

        # loop to find the script
        for script in self.script_list:
            if script.has_path(path):
                return script

        self._logger.info('Script not found')
        return None

    @MethodBoundaryLogger(_logger)
    def find_all_running_scripts(self):
        scripts = []

        for script in self.script_list:
            if script.is_running():
                scripts.append(script)

        return scripts

    # ------------------------------------------------------------------ #
    # delete
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def remove(self):
        """
        remove library
        :return: void
        """

        has_error = False

        # remove all script as well
        for script in self.script_list:
            success = script.remove()
            if not success:
                has_error = True

        if has_error:
            GlobalVariable.error_messages.append(
                'Unable to remove library, some script can not be removed: {path}'.format(path=self.library_path))
            self._logger.error(
                'Unable to remove library, some script can not be removed >>> {library}'.format(library=repr(self)))
            return False

        self.state.exclude = True
        self.state.hide = True
        return True

    @MethodBoundaryLogger(_logger)
    def remove_script(self, path):
        """
        remove script
        :return: void
        """

        script = self.find_script(path)

        if script is None:
            self._logger.info('Unable to remove script, script not in library >>> {path}'.format(path=path))
            return True

        return script.remove(path)

    @MethodBoundaryLogger(_logger)
    def delete(self):
        """
        delete library
        :return: bool, whether success
        """

        # if folder not exists, nothing should be done
        if not self.exists():
            self._logger.info('Library path does not exist >>> {library}'.format(library=repr(self)))
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
            GlobalVariable.error_messages.append(
                'Unable to delete library, some script can not be deleted: {path}'.format(path=self.library_path))
            self._logger.info(
                'Unable to delete library, some script can not be deleted >>> {library}'.format(library=repr(self)))
            return False

        # delete directory when no error occurs
        try:
            os.rmdir(self.library_path)
        except OSError as error:
            GlobalVariable.error_messages.append(
                'Unable to delete folder: {path}'.format(path=self.library_path))
            self._logger.info(
                'Unable to delete folder >>> Library path: {path} | Error: {error}'.format(path=self.library_path,
                                                                                           error=error))
            return False

        return True

    @MethodBoundaryLogger(_logger)
    def delete_script(self, path):
        """
        delete script with given path
        :param path: file path
        :return: bool, whether success
        """

        script = self.find_script(path)

        if script is None:
            # library don't contains script
            self._logger.info(
                'Script does not exists in library >>> Script: {script_path}. Library: {library_path}'.format(
                    script_path=path, library_path=self.library_path))
            return True

        if not script.delete():
            return False

        # only remove from the list when no error occurs
        self.script_list.remove(script)
        return True

    # ------------------------------------------------------------------ #
    # refresh
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def refresh(self):
        """
        refresh library status and all scripts
        :return: bool, whether success
        """
        if not self.exists():
            GlobalVariable.error_messages.append('Library does not exists: {path}'.format(path=self.library_path))
            self._logger.error('Library does not exists >>> {library}'.format(library=repr(self)))
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
        files = Utility.get_files_in_directory(self.library_path)

        # initialize script file
        for file in files:
            # check whether script already loaded in the library
            found = self.find_script(file)
            if found:
                continue

            if Utility.is_script_file(file):
                script = Script()
                success = script.init_script(file)

                # only add script when no error returned
                if success:
                    self.script_list.append(script)
                    self._logger.info(
                        'Add new script file to library >>> Library: {library} | Script: {script}'.format(
                            library=repr(self), script=repr(script)))
            else:
                # add warning when file is not script
                self._logger.info('Path not a script file: {path}'.format(path=file))

        return True

    # ------------------------------------------------------------------ #
    # others
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def show(self):
        """
        should show library or not
        :return: bool
        """
        return not (self.state.exclude and self.state.hide)

    @MethodBoundaryLogger(_logger)
    def has_path(self, path):
        return self.library_path == os.path.normpath(path)

    @MethodBoundaryLogger(_logger)
    def exists(self):
        return os.path.exists(self.library_path)

    @MethodBoundaryLogger(_logger)
    def may_contains_script(self, path):
        return self.library_path == os.path.normpath(Utility.get_parent_directory(path))

    # ------------------------------------------------------------------ #
    # to string
    # ------------------------------------------------------------------ #

    @MethodBoundaryLogger(_logger)
    def __str__(self):
        """
        to string
        :return: single string value include library and all scripts
        """
        out = ['Library:\n\tTitle: {library}\n\tPath: {path}\n'.format(library=self.title, path=self.library_path)]

        for script in self.script_list:
            out.append(script.__str__())

        return '\n'.join(out)

    @MethodBoundaryLogger(_logger)
    def to_json(self):
        out = {}

        out['library_path'] = self.library_path
        out['title'] = self.title
        out['state'] = self.state.to_json()
        out['scripts'] = []

        for script in self.script_list:
            out['scripts'].append(script.to_json())

        return out

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def from_json(json_str):
        library = Library()
        library.library_path = json_str['library_path']
        library.title = json_str['title']
        library.state = State.from_json(json_str['state'])

        for script in json_str['scripts']:
            library.script_list.append(Script.from_json(script))

        return library

    def __repr__(self):
        out = 'Library(title={title}, path={path}, is_running={is_running}, script_count={count})'.format(
            title=self.title, path=self.library_path, is_running=self.state.running, count=len(self.script_list))
        return out
