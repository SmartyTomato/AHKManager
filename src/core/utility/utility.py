import os
from shutil import copyfile
from typing import List


class Utility:
    def get_file_name(self, path: str) -> str:
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

    def get_file_name_no_extension(self, path: str) -> str:
        """
        Get file name without file extension

        Args:
            path (str): file path

        Returns:
            str: file name
        """

        try:
            base_name = self.get_file_name(path)

            if not base_name:
                return ""

            return os.path.splitext(base_name)[0]
        except Exception:
            return ""

    def get_file_extension(self, path: str) -> str:
        """
        Get file extension

        Args:
            path (str): file path

        Returns:
            str: file extension (.*)
        """

        try:
            base_name = self.get_file_name(path)

            if not base_name or len(base_name) < 2:
                return ""
            else:
                return os.path.splitext(base_name)[1]
        except Exception:
            return ""

    def get_parent_directory(self, path: str) -> str:
        """
        Get file parent parent direcotry (containing folder)

        Args:
            path (str): file path

        Returns:
            str: parent folder path
        """

        try:
            return os.path.dirname(path)
        except Exception:
            return ""

    def get_directories(self, dir_path: str) -> List[str]:
        """
        Get all sub-directories in the given directory

        Args:
            dir_path (str): directory path

        Returns:
            List[str]: list of directory path
        """

        try:
            # invalid path
            is_dir = self.is_dir(dir_path)
            if not is_dir:
                return []

            dir_list = []

            for file_name in os.listdir(dir_path):
                path = self.join_path(dir_path, file_name)
                if not self.is_dir(path):
                    continue

                dir_list.append(path)

                # if path is a directory
                # add it into the list and search the concurrent folder
                child_dirs = self.get_directories(path)
                if child_dirs:
                    dir_list.extend(child_dirs)

            return dir_list
        except Exception:
            return []

    def get_files_in_directory(self, dir_path: str) -> List[str]:
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
            is_dir = self.is_dir(dir_path)
            if not is_dir:
                return []

            file_list = []

            for file_name in os.listdir(dir_path):
                path = self.join_path(dir_path, file_name)

                # only ad when path is a file
                is_file = self.is_file(path)
                if is_file:
                    file_list.append(path)

            return file_list
        except Exception:
            return []

    def is_dir(self, path: str) -> bool:
        """
        Check whether given path is directory path

        Args:
            path (str): file/directory path

        Returns:
            bool:
        """

        try:
            self.format_path(path)

            # check whether path is a valid directory
            if not os.path.isdir(path):
                return False

            # check whether path exists
            if not self.path_exists(path):
                return False

            return True
        except Exception:
            return False

    def format_path(self, path: str) -> str:
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

    def path_exists(self, path: str) -> bool:
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

    def is_file(self, path: str) -> bool:
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
            if not self.path_exists(path):
                return False

            return True
        except Exception:
            return False

    def join_path(self, p_1: str, p_2: str) -> str:
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

    def make_dirs(self, path: str) -> bool:
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
            if not self.path_exists(path) and \
               not self.path_exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                    return True
                except Exception:
                    return False

            return True
        except Exception:
            return False

    def remove_file(self, path: str) -> bool:
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

    def remove_dir(self, path: str) -> bool:
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

    def copy_file(self, src: str, dst: str) -> bool:
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


utility = Utility()
