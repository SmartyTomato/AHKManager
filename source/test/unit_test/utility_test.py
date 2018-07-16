import os
from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock, mock_open, patch

from core.utility.configuration import Configuration
from core.utility.utility import (get_directories, get_file_name,
                                  get_files_in_directory, scan_directory)

listdir = {'Z:\OneDrive\Sync\Scripts\AutoHotKey': ['A', 'B', 'C.txt'], 'Z:\OneDrive\Sync\Scripts\AutoHotKey\A': [],
           'Z:\OneDrive\Sync\Scripts\AutoHotKey\B': []}
isdir = {
    'Z:\OneDrive\Sync\Scripts\AutoHotKey\A': True, 'Z:\OneDrive\Sync\Scripts\AutoHotKey\B': True,
    'Z:\OneDrive\Sync\Scripts\AutoHotKey\C.txt': False}
isfile = {
    'Z:\OneDrive\Sync\Scripts\AutoHotKey\A': False, 'Z:\OneDrive\Sync\Scripts\AutoHotKey\B': False,
    'Z:\OneDrive\Sync\Scripts\AutoHotKey\C.txt': True}


def os_listdir(arg):
    return listdir[arg]


def os_isdir(arg):
    return isdir[arg]


def os_isfile(arg):
    return isfile[arg]


class UtilityTest(TestCase):

    def test_get_file_name(self):
        file_path = 'C:/Windows/Prefetch/SEARCHFILTERHOST.EXE-77482212.pf'
        file_name = get_file_name(file_path)

        self.assertEqual(file_name, 'SEARCHFILTERHOST.EXE-77482212.pf')

    """"""

    @mock.patch('source.core.utility.os.listdir', side_effect=os_listdir)
    @mock.patch('source.core.utility.os.path.isdir', side_effect=os_isdir)
    def test_scan_directory(self, listdir, isdir):
        # setup
        Configuration.get_instance().file_types = ['.txt']

        path = "Z:\OneDrive\Sync\Scripts\AutoHotKey"
        list1, list2 = scan_directory(path)

        self.assertEqual(len(list1), 1)
        self.assertEqual(len(list2), 2)

    @mock.patch('source.core.utility.os.listdir', side_effect=os_listdir)
    @mock.patch('source.core.utility.os.path.isdir', side_effect=os_isdir)
    def test_get_directories(self, listdir, isdir):
        list1 = get_directories("Z:\OneDrive\Sync\Scripts\AutoHotKey")

        self.assertEqual(len(list1), 2)

    @mock.patch('source.core.utility.os.listdir', side_effect=os_listdir)
    @mock.patch('source.core.utility.os.path.isfile', side_effect=os_isfile)
    def test_get_files_in_dir(self, listdir, isfile):
        list1 = get_files_in_directory("Z:\OneDrive\Sync\Scripts\AutoHotKey")

        self.assertEqual(len(list1), 1)
