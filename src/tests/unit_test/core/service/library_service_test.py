import pytest

from typing import List
from typing import Dict
from unittest.mock import MagicMock

from src.core.model.action_result import ActionResult
from src.core.model.library import Library
from src.core.model.script import Script
from src.core.model.message import MessageType
from src.core.service.library_service import LibraryService


class LibraryServiceTest():
    example_paths: List[Dict] = [
        {
            'directory': 'C:\\test',
            'files': [
                'C:\\test\\script.ahk',
                'C:\\test\\script1.ahk',
                'C:\\test\\script2.ahk',
                'C:\\test\\script3.ahk',
                'C:\\test\\script4.ahk'],
        },
        {
            'directory': 'C:\\test\\subfolder',
            'files': [
                'C:\\test\\subfolder\\script10.ahk',
                'C:\\test\\subfolder\\script11.ahk',
                'C:\\test\\subfolder\\script12.ahk',
                'C:\\test\\subfolder\\script13.ahk',
                'C:\\test\\subfolder\\script14.ahk']
        },
        {
            'directory': 'C:\\test\\subfolder2',
            'files': [
                'C:\\test\\subfolder2\\script15.ahk',
                'C:\\test\\subfolder2\\script16.ahk',
                'C:\\test\\subfolder2\\script17.ahk',
                'C:\\test\\subfolder2\\script18.ahk',
                'C:\\test\\subfolder2\\script19.ahk']
        },
        {
            'directory': 'D:\\test2',
            'files': [
                'D:\\test2\\script5.ahk',
                'D:\\test2\\script6.ahk',
                'D:\\test2\\script7.ahk',
                'D:\\test2\\script8.ahk',
                'D:\\test2\\script9.ahk']
        }]

    @pytest.fixture()
    def target(self) -> LibraryService:
        library_service = LibraryService()
        library_service.remove_all()

        return LibraryService()

    @pytest.fixture()
    def test_dir(self) -> str:
        return self.example_paths[0]['directory']

    @pytest.fixture()
    def sub_dirs(self) -> List[str]:
        return [
            self.example_paths[1]['directory'],
            self.example_paths[2]['directory']
        ]

    @pytest.fixture()
    def test_script(self) -> str:
        return self.example_paths[0]['files'][0]

    @pytest.fixture()
    def scripts_count(self):
        count = 0
        for path in self.example_paths:
            count += len(path['files'])

        return count

    def _setup_data(self):
        # > Create new library service and initialize
        library_service = LibraryService()
        for item in self.example_paths:
            library = Library(item['directory'])
            for script_path in item['files']:
                script = Script(script_path)
                library.add(script)

            library_service.repository.add(library)

    # region add

    def add_test_new(self, target: LibraryService,
                     test_dir: str, sub_dirs: List):
        '''
        Success
        Add new library into repository
        '''

        # * Prepare
        target.utility.format_path = MagicMock(return_value=test_dir)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(
            return_value=sub_dirs)

        # * Key
        # Could not find library in repository
        target.find = MagicMock(return_value=None)
        target.library_manager.init_library = MagicMock(
            side_effect=lambda path: (ActionResult(), Library(path)))
        target.library_manager.reload = MagicMock(ActionResult(), None)

        # * Act
        result = target.add(test_dir)

        # * Assert
        assert len(sub_dirs) + \
            1 == target.library_manager.init_library.call_count
        assert not target.library_manager.reload.called
        assert result.success()
        assert not result.messages
        assert len(sub_dirs) + 1 == len(target.repository.library_list)

        target.utility.format_path.assert_called_with(test_dir)
        target.utility.is_dir.assert_called_with(test_dir)

    def add_test_reload(self, target: LibraryService,
                        test_dir: str, sub_dirs: List):
        '''
        Success
        Call reload method instead initialize new library
        '''

        # * Prepare
        target.utility.format_path = MagicMock(return_value=test_dir)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(return_value=sub_dirs)

        # * Key
        # Could library found in repository, reload
        target.find = MagicMock(side_effect=lambda path: Library(path))
        target.library_manager.init_library = MagicMock()
        target.library_manager.reload = MagicMock(
            side_effect=lambda library: (ActionResult(), library))

        # * Act
        result = target.add(test_dir)

        # * Assert
        assert not target.library_manager.init_library.called
        assert len(sub_dirs) + 1 == target.library_manager.reload.call_count
        assert result.success()
        assert len(result.messages) == 3
        for msg in result.messages:
            assert msg.type == MessageType.INFO

        assert not target.repository.library_list

        target.utility.format_path.assert_called_with(test_dir)
        target.utility.is_dir.assert_called_with(test_dir)

    def add_test_init_failed(self, target: LibraryService,
                             test_dir: str, sub_dirs: List):
        '''
        Success
        New library failed to initialize
        '''

        failed_result = ActionResult()
        failed_result.add_error('Failed')

        # * Prepare
        target.utility.format_path = MagicMock(return_value=test_dir)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(
            return_value=sub_dirs)

        # * Key
        # Could not find library in repository
        target.find = MagicMock(return_value=None)
        target.library_manager.init_library = MagicMock(
            side_effect=lambda path: (failed_result, None))
        target.library_manager.reload = MagicMock()

        # * Act
        result = target.add(test_dir)

        # * Assert
        assert len(sub_dirs) + \
            1 == target.library_manager.init_library.call_count
        assert not target.library_manager.reload.called
        assert result.success()
        assert len(result.messages) == 3
        assert not target.repository.library_list

        target.utility.format_path.assert_called_with(test_dir)
        target.utility.is_dir.assert_called_with(test_dir)

    def add_test_invalid_directory_path(self, target: LibraryService):
        '''
        Invalid directory path
        Returns error message
        '''

        # * Prepare
        dir_path = 'invalid dir path'

        # * Key
        target.utility.is_dir = MagicMock(return_value=False)

        # * Act
        result = target.add(dir_path)

        # * Assert
        assert not result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.ERROR
        assert not target.repository.library_list

    # endregion add

    # region find

    def find_test(self, target: LibraryService, test_dir: str):
        """
        Success
        """

        # * Prepare
        self._setup_data()
        target.utility.format_path = MagicMock(return_value=test_dir)

        # * Key

        # * Act
        result = target.find(test_dir)

        # * Assert
        assert result
        assert result.path == test_dir

    def find_test_library_not_found(self, target: LibraryService):
        """
        Library not found
        Return None
        """

        # * Prepare
        test_dir = "C:\\test100"
        self._setup_data()
        target.utility.format_path = MagicMock(return_value=test_dir)

        # * Key

        # * Act
        result = target.find(test_dir)

        # * Assert
        assert not result

    def find_script_test(self, target: LibraryService, test_script: str):
        # * Prepare
        self._setup_data()

        # * Key
        # * Act
        result = target.find_script(test_script)

        # * Assert
        assert result
        assert result.identifier() == test_script

    def find_library_contains_script_test(self, target: LibraryService,
                                          test_script: str):
        # * Prepare
        self._setup_data()
        target.utility.format_path = MagicMock(return_value=test_script)

        # * Act
        result = target.find_library_contains_script(test_script)

        # * Assert
        assert bool(result)

    def find_library_contains_script_test_script_not_found(
            self, target: LibraryService):
        # * Prepare
        script_path = 'C:\\test123456789.ahk'
        target.utility.format_path = MagicMock(return_value=script_path)

        # * Act
        result = target.find_library_contains_script(script_path)

        # * Assert
        assert not bool(result)

    # endregion find

    # region remove

    def remove_test_library_not_exists(self, target: LibraryService,
                                       test_dir: str):
        """
        Success
        Library does not exists in the repository
        """

        # * Prepare
        self._setup_data()

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result = target.remove(test_dir)

        # * Assert
        assert result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.WARNING

    def remove_test_failed(self, target: LibraryService, test_dir: str):
        """
        Remove library failed
        Returns error messages
        """

        # * Prepare
        library = Library(test_dir)
        remove_result = ActionResult()
        remove_result.add_error("Error")

        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.remove = MagicMock(return_value=remove_result)

        # * Act
        result = target.remove(test_dir)

        # * Assert
        assert not result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.ERROR

    def remove_test(self, target: LibraryService, test_dir: str):
        """
        Success
        """

        # * Prepare
        library = Library(test_dir)
        target.find = MagicMock(return_value=library)

        # * Key
        target.repository.remove = MagicMock()
        target.library_manager.remove = MagicMock(return_value=ActionResult())

        # * Act
        result = target.remove(test_dir)

        # * Assert
        assert result.success()
        assert not result.messages

        assert target.repository.remove.called

    # endregion remove

    # region remove script

    def remove_script_test_script_not_exists(self, target: LibraryService,
                                             test_script: str):
        """
        Success
        Script does not exist, return warning
        """

        # * Prepare
        self._setup_data()

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result = target.remove_script(test_script)

        # * Assert
        assert result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.WARNING

    def remove_script_test_failed(self, target: LibraryService,
                                  test_script: str):
        """
        Remove script failed
        Return error messages
        """

        # * Prepare
        script = Script(test_script)
        remove_result = ActionResult()
        remove_result.add_error("Error")

        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.remove = MagicMock(return_value=remove_result)
        target.find_library_contains_script = MagicMock()

        # * Act
        result = target.remove_script(test_script)

        # * Assert
        assert not result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.ERROR

        assert not target.find_library_contains_script.called

    def remove_script_test(self, target: LibraryService, test_script: str):
        """
        Success
        """

        # * Prepare
        script = Script(test_script)

        remove_result = ActionResult()
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.remove = MagicMock(return_value=remove_result)
        target.find_library_contains_script = MagicMock()

        # * Act
        result = target.remove_script(test_script)

        # * Assert
        assert result.success()
        assert not result.messages

    def remove_all_test(self, target: LibraryService):
        # * Prepare
        target.stop_all = MagicMock(return_value=ActionResult())

        # * Key
        # * Act
        result = target.remove_all()

        # * Assert
        assert result.success()
        assert len(target.repository.library_list) == 0

    def remove_all_test_stop_all_failed(self, target: LibraryService):
        # * Prepare
        self._setup_data()
        failed_result = ActionResult()
        failed_result.add_error('')
        target.stop_all = MagicMock(return_value=failed_result)

        # * Key
        # * Act
        result = target.remove_all()

        # * Assert
        assert not result.success()
        assert len(target.repository.library_list) != 0

    # endregion remove script

    # region start

    def start_test_library_not_exists(self, target: LibraryService,
                                      test_dir: str):
        """
        Library not exists
        Return error
        """

        # * Prepare

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result, library = target.start(test_dir)

        # * Assert
        assert not result.success()
        assert library is None

    def start_test(self, target: LibraryService, test_dir: str):
        """
        Success
        Return library
        """

        # * Prepare
        library = Library(test_dir)
        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.start = MagicMock(
            return_value=(ActionResult(), library))

        # * Act
        result, result_library = target.start(test_dir)

        # * Assert
        assert result.success()
        assert result_library.identifier() == library.identifier()

    # endregion start

    # region start script

    def start_script_test_script_not_exists(self, target: LibraryService,
                                            test_script: str):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.start_script(test_script)

        # * Assert
        assert not result.success()
        assert result_script is None

    def start_script_test(self, target: LibraryService, test_script: str):
        """
        Success
        """

        # * Prepare
        script = Script(test_script)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.start = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.start_script(test_script)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion start script

    # region restart script

    def restart_script_test_script_not_exists(self, target: LibraryService,
                                              test_script: str):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.restart_script(test_script)

        # * Assert
        assert not result.success()
        assert result_script is None

    def restart_script_test(self, target: LibraryService, test_script: str):
        """
        Success
        """

        # * Prepare
        script = Script(test_script)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.restart = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.restart_script(test_script)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion restart script

    # region stop

    def stop_test_library_not_exists(self, target: LibraryService,
                                     test_dir: str):
        """
        Library not exists
        Return error
        """

        # * Prepare

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result, library = target.stop(test_dir)

        # * Assert
        assert not result.success()
        assert library is None

    def stop_test(self, target: LibraryService, test_dir: str):
        """
        Success
        Return library
        """

        # * Prepare
        library = Library(test_dir)
        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.stop = MagicMock(
            return_value=(ActionResult(), library))

        # * Act
        result, result_library = target.stop(test_dir)

        # * Assert
        assert result.success()
        assert result_library.identifier() == library.identifier()

    # endregion stop

    # region stop script

    def stop_script_test_script_not_exists(self, target: LibraryService,
                                           test_script: str):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.stop_script(test_script)

        # * Assert
        assert not result.success()
        assert result_script is None

    def stop_script_test(self, target: LibraryService, test_script: str):
        """
        Success
        """

        # * Prepare
        script = Script(test_script)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.stop = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.stop_script(test_script)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion stop script

    # region stop all

    def stop_all_test_could_not_stop_some_script(self, target: LibraryService,
                                                 test_dir: str):
        """
        Could not stop some script in the library
        Return warning message
        """

        # * Prepare
        target.repository.add(Library(test_dir))
        stop_result = ActionResult()
        stop_result.add_error("Error")

        # * Key
        target.library_manager.stop = MagicMock(
            return_value=(stop_result, None))

        # * Act
        result = target.stop_all()

        # * Assert
        assert result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.WARNING

    def stop_all_test(
            self, target: LibraryService, test_dir: str):
        """
        Success
        """

        # * Prepare
        library = Library(test_dir)
        target.repository.add(library)
        stop_result = ActionResult()

        # * Key
        target.library_manager.stop = MagicMock(
            return_value=(stop_result, library))

        # * Act
        result = target.stop_all()

        # * Assert
        assert result.success()
        assert not result.messages

    # endregion stop all

    # region refresh

    def refresh_test_library_path_not_exists(self, target: LibraryService,
                                             test_dir: str):
        """
        Library path not exists on disk
        """

        # * Prepare
        target.repository.add(Library(test_dir))
        refresh_result = ActionResult()
        refresh_result.add_error('Could not find library')

        # * Key
        target.library_manager.refresh = MagicMock(return_value=refresh_result)

        # * Act
        target.refresh()

        # * Assert
        assert target.library_manager.refresh.called

    def refresh_test(self, target: LibraryService, test_dir: str):
        """
        Library path not exists on disk
        """

        # * Prepare
        target.repository.add(Library(test_dir))
        refresh_result = ActionResult()

        # * Key
        target.library_manager.refresh = MagicMock(return_value=refresh_result)

        # * Act
        target.refresh()

        # * Assert
        assert target.library_manager.refresh.called

    # endregion refresh

    # region get all scripts

    def get_all_scripts_test(self, target: LibraryService, scripts_count: int):
        # * Prepare
        self._setup_data()

        # * Act
        result = target.get_all_scripts()

        # * Assert
        assert result
        assert len(result) == scripts_count

    # endregion get all scripts

    # region pause all

    def pause_all_test(self, target: LibraryService, scripts_count: int):
        """
        Pause all success
        """

        # * Prepare
        self._setup_data()
        target.library_manager.pause = MagicMock(
            side_effect=self._pause_all_library_manager_pause)

        # * Act
        result = target.pause_all()

        # * Assert
        assert result.success()
        assert not result.messages

        for library in target.repository.library_list:
            assert library.is_paused()

        target.library_manager.pause.call_count == scripts_count

    def _pause_all_library_manager_pause(self, library: Library):
        library.pause()
        return ActionResult(), library

    # endregion pause all

    # region resume all

    def resume_all_test(self, target: LibraryService, scripts_count: int):
        # * Prepare
        self._setup_data()

        target.library_manager.resume = MagicMock(
            side_effect=lambda library: (ActionResult(), library))

        # * Act
        result = target.resume_all()

        # * Assert
        assert result.success()
        target.library_manager.resume.call_count == scripts_count

    def resume_all_test_has_error(
            self, target: LibraryService, scripts_count: int):
        # * Prepare
        self._setup_data()
        error_result = ActionResult()
        error_result.add_error('')

        target.library_manager.resume = MagicMock(
            side_effect=lambda library: (error_result, library))

        # * Act
        result = target.resume_all()

        # * Assert
        assert result.success()
        target.library_manager.resume.call_count == scripts_count

    # endregion resume all


if __name__ == '__main__':
    pytest.main()
