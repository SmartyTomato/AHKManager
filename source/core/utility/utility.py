import os

from core.utility.configuration import Configuration
from core.model.global_variable import GlobalVariable
from core.utility.logger import Logger, MethodBoundaryLogger


class Utility(object):
    _logger = Logger('Utility')

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_file_name(path):
        """
        extract file name from path
        :param path:
        :return: file name
        """
        try:
            return os.path.basename(path)
        except Exception as error:
            GlobalVariable.error_messages.append('Unable to get file name for path "{path}"'.format(path=path))
            Utility._logger.error(
                'Unable to get file name >>> Path: {path} | Error: {error}'.format(path=path, error=error))
            return []

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_file_name_no_extension(path):
        """
        extract file name from path
        :param path:
        :return: file name without extension
        """

        base_name = Utility.get_file_name(path)

        if not base_name:
            GlobalVariable.error_messages.append('Could not get name for path: {path}'.format(path=path))
            Utility._logger.error('Could not get name for path >>> {path}'.format(path=path))
            return ''

        return os.path.splitext(base_name)[0]

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_file_extension(path):
        """
        extract file name from path
        :param path:
        :return: file name without extension
        """

        base_name = Utility.get_file_name(path)

        if not base_name or len(base_name) < 2:
            GlobalVariable.error_messages.append('Could not get file extension for path: {path}'.format(path=path))
            Utility._logger.error('Could not get file extension for path >>> {path}'.format(path=path))
            return ''

        return os.path.splitext(base_name)[1]

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_parent_directory(path):
        try:
            return os.path.dirname(path)
        except Exception as error:
            GlobalVariable.error_messages.append('Could not get parent directory for path: {path}'.format(path=path))
            Utility._logger.error(
                'Could not get parent directory for path >>> Path: {path} | Error: {error}'.format(path=path,
                                                                                                   error=error))
            return ''

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_directories(dir_path):
        """
        get list of directory
        :param dir_path:
        :return: list of directory paths
        """
        # invalid path
        if not os.path.isdir(dir_path):
            GlobalVariable.error_messages.append('Path is not a directory path: {path}'.format(path=dir_path))
            Utility._logger.error('Path is not a directory path >>> {path}'.format(path=dir_path))
            return []

        # path not exists
        if not os.path.exists(dir_path):
            GlobalVariable.error_messages.append('Path does not exists: {path}'.format(path=dir_path))
            Utility._logger.error('Path does not exists >>> {path}'.format(path=dir_path))
            return []

        dir_list = []

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)

            # if path is a directory
            # add it into the list and search the concurrent folder
            if os.path.isdir(path):
                dir_list.append(path)
                dir_list.extend(Utility.get_directories(path))

        return dir_list

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def get_files_in_directory(dir_path):
        """
        get all files in the intermediate directory
        :param dir_path:
        :return: list of file paths
        """
        # invalid path
        if not os.path.isdir(dir_path):
            GlobalVariable.error_messages.append('Path is not a directory path: {path}'.format(path=dir_path))
            Utility._logger.error('Path is not a directory path >>> {path}'.format(path=dir_path))
            return []

        # path not exists
        if not os.path.exists(dir_path):
            GlobalVariable.error_messages.append('Path does not exists: {path}'.format(path=dir_path))
            Utility._logger.error('Path does not exists >>> {path}'.format(path=dir_path))
            return []

        file_list = []

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)

            # only ad when path is a file
            if os.path.isfile(path):
                file_list.append(path)

        return file_list

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def is_script_file(path):
        """
        whether should import file or not
        :param path:
        :return: is selected or not
        """
        if not os.path.isfile(path):
            GlobalVariable.error_messages.append('Path is not a file: {path}'.format(path=path))
            Utility._logger.error('Path is not a file >>> {path}'.format(path=path))
            return False

        if not os.path.exists(path):
            GlobalVariable.error_messages.append('Path does not exists: {path}'.format(path=path))
            Utility._logger.error('Path does not exists >>> {path}'.format(path=path))
            return False

        return Utility.get_file_extension(path) in Configuration.get().file_types

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def scan_directory(dir_path):
        """
        get all available scripts and directories in the given directory
        :param dir_path:
        :return: list of file path
        :return: list of directory path
        """

        if not os.path.isfile(dir_path):
            GlobalVariable.error_messages.append('Path is not a file: {path}'.format(path=dir_path))
            Utility._logger.error('Path is not a file >>> {path}'.format(path=dir_path))
            return False

        if not os.path.exists(dir_path):
            GlobalVariable.error_messages.append('Path does not exists: {path}'.format(path=dir_path))
            Utility._logger.error('Path does not exists >>> {path}'.format(path=dir_path))
            return False

        file_list = []
        dir_list = []

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)

            # if path is directory, calling method itself to search the sub folder
            if os.path.isdir(path):
                dir_list.append(path)
                temp_file_list, temp_dir_list = Utility.scan_directory(path)
                file_list.extend(temp_file_list)
                dir_list.extend(temp_dir_list)

            match = False

            # only get the file with the selected extensions
            for extension in Configuration.get().file_types:
                if file_name.endswith(extension):
                    match = True

            if match:
                file_list.append(path)

        return file_list, dir_list
