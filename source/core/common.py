import ntpath
import os

from source.configs.configure import configs


def get_file_name(path):
    """
    extract file name from path
    :param path:
    :return: file name
    """
    ntpath.basename('a/b/c')
    head, tail = ntpath.split(path)

    return tail or ntpath.basename(head)


def get_directories(dir_path):
    """
    get list of directory
    :param dir_path:
    :return: list of directory paths
    """
    dir_list = []

    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)

        # if path is a directory
        # add it into the list and search the concurrent folder
        if os.path.isdir(path):
            dir_list.append(path)
            dir_list.extend(get_directories(path))

    return dir_list


def get_files_in_directory(dir_path):
    """
    get all files in the intermediate directory
    :param dir_path:
    :return: list of file paths
    """
    file_list = []

    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)

        # only ad when path is a file
        if os.path.isfile(path):
            file_list.append(path)

    return file_list


def scan_directory(dir_path):
    """
    get all files and directories in the given directory
    :param dir_path:
    :return: list of file path
    :return: list of directory path
    """
    file_list = []
    dir_list = []

    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)

        # if path is directory, calling method itself to search the sub folder
        if os.path.isdir(path):
            dir_list.append(path)
            fl, dl = scan_directory(path)
            file_list.extend(fl)
            dir_list.extend(dl)

        match = False

        # only get the file with the selected extensions
        for extension in configs.file_types:
            if file_name.endswith(extension):
                match = True

        if match:
            file_list.append(path)

    return file_list, dir_list
