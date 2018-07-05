import os
from shutil import copyfile
from typing import List

from core.service.message_service import MessageService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType


class Utility(object):
    logger = Logger('Utility')

    message_service = MessageService()

    @staticmethod
    def get_file_name(path: str) -> List[str]:
        """
        extract file name from path
        :param path:
        :return: file name
        """
        try:
            return os.path.basename(path)
        except Exception as error:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not get file name for path "{}"'.format(path)))
            Utility.logger.error(
                'Could not get file name >>> Path: {path} | Error: {error}'.format(path=path, error=error))
            return []

    @staticmethod
    def get_file_name_no_extension(path: str) -> str:
        """
        extract file name from path
        :param path:
        :return: file name without extension
        """

        base_name = Utility.get_file_name(path)

        if not base_name:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not get name for path: {}'.format(path)))
            Utility.logger.error('Could not get name for path >>> {}'.format(path))
            return ''

        return os.path.splitext(base_name)[0]

    @staticmethod
    def get_file_extension(path: str) -> str:
        """
        extract file name from path
        :param path:
        :return: file name without extension
        """

        base_name = Utility.get_file_name(path)

        if not base_name or len(base_name) < 2:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not get file extension for path: {}'.format(path)))
            Utility.logger.error('Could not get file extension for path >>> {}'.format(path))
            return ''

        return os.path.splitext(base_name)[1]

    @staticmethod
    def get_parent_directory(path: str) -> str:
        try:
            return os.path.dirname(path)
        except Exception as error:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not get parent directory for path: {}'.format(path)))
            Utility.logger.error(
                'Could not get parent directory for path >>> Path: {path} | Error: {error}'.format(
                    path=path, error=error))
            return ''

    @staticmethod
    def get_directories(dir_path: str) -> List[str]:
        """
        get list of directory
        :param dir_path:
        :return: list of directory paths
        """
        # invalid path
        if not os.path.isdir(dir_path):
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Path is not a directory path: {}'.format(dir_path)))
            Utility.logger.error('Path is not a directory path >>> {}'.format(dir_path))
            return []

        # path not exists
        if not Utility.path_exists(dir_path):
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Path does not exists: {}'.format(dir_path)))
            Utility.logger.error('Path does not exists >>> {}'.format(dir_path))
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
    def get_files_in_directory(dir_path: str) -> List[str]:
        """
        get all files in the intermediate directory
        :param dir_path:
        :return: list of file paths
        """
        # invalid path
        if not os.path.isdir(dir_path):
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Path is not a directory path: {}'.format(dir_path)))
            Utility.logger.error('Path is not a directory path >>> {}'.format(dir_path))
            return []

        # path not exists
        if not Utility.path_exists(dir_path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path does not exists: {}'.format(dir_path)))
            Utility.logger.error('Path does not exists >>> {}'.format(dir_path))
            return []

        file_list = []

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)

            # only ad when path is a file
            if os.path.isfile(path):
                file_list.append(path)

        return file_list

    @staticmethod
    def is_dir(path: str) -> bool:
        # check whether path is a valid directory
        if not os.path.isdir(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path is not a directory path: {}'.format(path)))
            Utility.logger.error('Path is not a directory path >>> {}'.format(path))
            return False

        # check whether path exists
        if not Utility.path_exists(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path does not exists: {}'.format(path)))
            Utility.logger.error('Path does not exists >>> {}'.format(path))
            return False

        return True

    @staticmethod
    def format_path(path: str) -> str:
        return os.path.normpath(path)

    @staticmethod
    def path_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        # check if path is a file
        if not os.path.isfile(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path is not a valid file path: {}'.format(path)))
            Utility.logger.error('Path is not a valid file path >>> {}'.format(path))
            return False

        # check if path exists
        if not Utility.path_exists(path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path does not exists: {}'.format(path)))
            Utility.logger.error('Path does not exists >>> {}'.format(path))
            return False

        return True

    @staticmethod
    def join_path(p_1: str, p_2: str) -> str:
        return os.path.join(p_1, p_2)

    @staticmethod
    def make_dirs(path: str) -> bool:
        # create file and all folder required
        if not Utility.path_exists(path) and not Utility.path_exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as error:
                Utility.message_service.add(
                    Message(MessageType.ERROR, 'Could not make directory for file: {}'.format(path)))
                Utility.logger.error(
                    'Could not make directory for file >>> Path: {path} | Error: {error}'.format(path=path,
                                                                                                 error=error))
                return False

        return True

    @staticmethod
    def remove_file(path: str) -> bool:
        try:
            os.remove(path)
            return True
        except OSError as error:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not delete file: {}'.format(path)))
            Utility.logger.error('Could not delete file >>> Path: {path} | Error: {msg}'.format(path=path, msg=error))
            return False

    @staticmethod
    def remove_dir(path: str) -> bool:
        try:
            os.rmdir(path)
            return True
        except OSError as error:
            Utility.message_service.add(Message(MessageType.ERROR, 'Could not delete folder: {}'.format(path)))
            Utility.logger.error(
                'Could not delete folder >>> Library path: {path} | Error: {error}'.format(
                    path=path, error=error))
            return False

    @staticmethod
    def scan_directory(dir_path: str) -> (List[str], List[str]):
        if not os.path.isfile(dir_path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path is not a file: {}'.format(dir_path)))
            Utility.logger.error('Path is not a file >>> {}'.format(dir_path))
            return False

        if not Utility.path_exists(dir_path):
            Utility.message_service.add(Message(MessageType.ERROR, 'Path does not exists: {}'.format(dir_path)))
            Utility.logger.error('Path does not exists >>> {}'.format(dir_path))
            return False

        file_list = []
        dir_list = []

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)

            # if path is directory, calling method itUtility to search the sub folder
            if os.path.isdir(path):
                dir_list.append(path)
                temp_file_list, temp_dir_list = Utility.scan_directory(path)
                file_list.extend(temp_file_list)
                dir_list.extend(temp_dir_list)

            file_list.append(path)

        return file_list, dir_list

    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        try:
            copyfile(src, dst)
            return True
        except OSError as error:
            Utility.message_service.add(
                Message(MessageType.ERROR, 'Could not copy file from "{source}" to "{dest}"'.format(
                    source=src, dest=dst)))
            Utility.logger.error('Could not copy file >>> Source: {source} | Destination: {dest} | Error: {error}'.format(
                source=src, dest=dst, error=error))
            return False
