import os

from core.utility.configuration import Configuration

def get_file_name(path):
    """
    extract file name from path
    :param path:
    :return: file name
    """
    return os.path.basename(path)


def get_file_name_no_extension(path):
    """
    extract file name from path
    :param path:
    :return: file name without extension
    """
    base_name = get_file_name(path)
    return os.path.splitext(base_name)[0]


def get_file_extension(path):
    """
    extract file name from path
    :param path:
    :return: file name without extension
    """
    base_name = get_file_name(path)
    return os.path.splitext(base_name)[1]


def get_parent_directory(path):
    return os.path.dirname(path)


def get_directories(dir_path):
    """
    get list of directory
    :param dir_path:
    :return: list of directory paths
    """
    # invalid path
    if not os.path.isdir(dir_path):
        return

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
    # invalid path
    if not os.path.isdir(dir_path):
        return

    file_list = []

    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)

        # only ad when path is a file
        if os.path.isfile(path):
            file_list.append(path)

    return file_list


def is_script_file(path):
    """
    whether should import file or not
    :param path:
    :return: is selected or not
    """
    if not os.path.isfile(path) and os.path.exists(path):
        return False

    return get_file_extension(path) in Configuration.get().file_types


def scan_directory(directory):
    """
    get all available scripts and directories in the given directory
    :param directory:
    :return: list of file path
    :return: list of directory path
    """
    file_list = []
    dir_list = []

    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)

        # if path is directory, calling method itself to search the sub folder
        if os.path.isdir(path):
            dir_list.append(path)
            temp_file_list, temp_dir_list = scan_directory(path)
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
