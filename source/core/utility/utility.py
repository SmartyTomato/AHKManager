import os
from shutil import copyfile
from typing import List


class Utility():
    @staticmethod
    def get_file_name(path: str) -> str:
        """
        Get file name for the given path

        Args:
            path (str): file path

        Returns:
            str: file name
        """

        try:
            return os.path.basename(path)
        except Exception:
            return ""

    @staticmethod
    def get_file_name_no_extension(path: str) -> str:
        """
        Get file name without file extension

        Args:
            path (str): file path

        Returns:
            str: file name
        """

        try:
            base_name = Utility.get_file_name(path)

            if not base_name:
                return ""

            return os.path.splitext(base_name)[0]
        except Exception:
            return ""

    @staticmethod
    def get_file_extension(path: str) -> str:
        """
        Get file extension

        Args:
            path (str): file path

        Returns:
            str: file extension (.*)
        """

        try:
            base_name = Utility.get_file_name(path)

            if not base_name or len(base_name) < 2:
                return ""
            else:
                return os.path.splitext(base_name)[1]
        except Exception:
            return ""

    @staticmethod
    def get_parent_directory(path: str) -> str:
        """
        Get file parent parent direcotry (containng folder)

        Args:
            path (str): file path

        Returns:
            str: parent folder path
        """

        try:
            return os.path.dirname(path)
        except Exception:
            return ""

    @staticmethod
    def get_directories(dir_path: str) -> List[str]:
        """
        Get all sub-directories in the given directory

        Args:
            dir_path (str): directory path

        Returns:
            List[str]: list of directory path
        """

        try:
            # invalid path
            is_dir = Utility.is_dir(dir_path)
            if not is_dir:
                return []

            dir_list = []

            for file_name in os.listdir(dir_path):
                path = Utility.join_path(dir_path, file_name)
                if not Utility.is_dir(path):
                    continue

                dir_list.append(path)

                # if path is a directory
                # add it into the list and search the concurrent folder
                child_dirs = Utility.get_directories(path)
                if child_dirs:
                    dir_list.extend(child_dirs)

            return dir_list
        except Exception:
            return []

    @staticmethod
    def get_files_in_directory(dir_path: str) -> List[str]:
        """
        Get all filles in the immediate directory

        Will not return the files in the sub-directory

        Args:
            dir_path (str): directory path

        Returns:
            List[str]: list of file path
        """

        try:
            # invalid path
            is_dir = Utility.is_dir(dir_path)
            if not is_dir:
                return []

            file_list = []

            for file_name in os.listdir(dir_path):
                path = Utility.join_path(dir_path, file_name)

                # only ad when path is a file
                is_file = Utility.is_file(path)
                if is_file:
                    file_list.append(path)

            return file_list
        except Exception:
            return []

    @staticmethod
    def is_dir(path: str) -> bool:
        """
        Check whether given path is directory path

        Args:
            path (str): file/directory path

        Returns:
            bool:
        """

        try:
            Utility.format_path(path)

            # check whether path is a valid directory
            if not os.path.isdir(path):
                return False

            # check whether path exists
            if not Utility.path_exists(path):
                return False

            return True
        except Exception:
            return False

    @staticmethod
    def format_path(path: str) -> str:
        """
        Format file path

        Args:
            path (str): file path

        Returns:
            str: formatted file path
        """

        try:
            return os.path.normpath(path)
        except Exception:
            return ""

    @staticmethod
    def path_exists(path: str) -> bool:
        """
        Check whether path exists

        Args:
            path (str): file path

        Returns:
            bool:
        """

        try:
            return os.path.exists(path)
        except Exception:
            return False

    @staticmethod
    def is_file(path: str) -> bool:
        """
        Check whether path is a valid file

        Args:
            path (str): file path

        Returns:
            bool:
        """

        try:
            # check if path is a file
            if not os.path.isfile(path):
                return False

            # check if path exists
            if not Utility.path_exists(path):
                return False

            return True
        except Exception:
            return False

    @staticmethod
    def join_path(p_1: str, p_2: str) -> str:
        """
        Join two file path. e.g. file directory + file name

        Args:
            p_1 (str):
            p_2 (str):

        Returns:
            str: combined file path
        """

        try:
            return os.path.join(p_1, p_2)
        except Exception:
            return ""

    @staticmethod
    def make_dirs(path: str) -> bool:
        """
        Create all required parent directory for the given path

        Args:
            path (str): file path

        Returns:
            bool: return true if all parnet directory
                successfully created
        """

        try:
            # create file and all folder required
            if not Utility.path_exists(path) and \
               not Utility.path_exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                    return True
                except Exception:
                    return False

            return True
        except Exception:
            return False

    @staticmethod
    def remove_file(path: str) -> bool:
        """
        Delete file

        Args:
            path (str): file path

        Returns:
            bool:
        """

        try:
            os.remove(path)
            return True
        except Exception:
            return False

    @staticmethod
    def remove_dir(path: str) -> bool:
        """
        Delete directory

        Args:
            path (str): directory path

        Returns:
            bool:
        """

        try:
            os.rmdir(path)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """
        Copy file from source to destination

        Args:
            src (str): source file path
            dst (str): destination file path

        Returns:
            bool: return true if copy success
        """

        try:
            copyfile(src, dst)
            return True
        except Exception:
            return False
