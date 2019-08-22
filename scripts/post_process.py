import os
import shutil
import time

from typing import List

sys_param = {
    # Post process
    'dist_path': '../dist/AHK Manager',
    'required_files': ['../resources',
                       '../README.md'],

    'search_path': ['../dist/AHK Manager',
                    '../dist/AHK Manager/Qt'],
    'qt_file_name': 'Qt',
    'exclude': ['Qt',
                'QtCore',
                'QtGui',
                'QtWidgets',
                'Qt5Core',
                'Qt5Gui',
                'Qt5Widgets']
}


def get_all_unnecessary_files(path: str) -> List[str]:
    result: List[str] = []

    path = os.path.normpath(path)

    if not os.path.isdir(path):
        print('Path is not directory path: {}'.format(path))
        return result

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if not os.path.isfile(file_path):
            # path is directory
            continue

        file_name_with_no_extension = os.path.splitext(file_name)[0]

        if (sys_param['qt_file_name'] in file_path and
                not (file_name_with_no_extension in sys_param['exclude'])):
            result.append(file_path)

    return result


def delete_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except Exception:
            print('Could not delete file: {}'.format(file_path))


def cleanup_dist():
    for path in sys_param['search_path']:
        dll_files = get_all_unnecessary_files(path)
        delete_files(dll_files)


def post_process():
    for required_file in sys_param['required_files']:
        dest = sys_param['dist_path']+'/'+os.path.basename(required_file)
        try:
            if os.path.isdir(required_file):
                shutil.copytree(required_file, dest)
            else:
                shutil.copy2(required_file, dest)
        except Exception:
            print('Could not copy file or directory to destination: {}'
                  .format(dest))


# ! Currently disabled, only use it when use pyinstaller not single file option
# cleanup_dist()

post_process()

print('Success, you can close window or it will auto close after 3 seconds')
time.sleep(3)
