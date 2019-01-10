import pytest
from unittest.mock import MagicMock

from src.core.model.action_result import ActionResult
from src.core.model.library import Library
from src.core.model.script import Script
from src.core.model.message import MessageType
from src.core.service.library_service import LibraryService
from core.model.library_repository import LibraryRepository


class LibraryServiceTest():
    test_dir = 'C:\\test'
    test_dir_2 = 'C:\\test2'

    @pytest.fixture
    def target(self):
        library_service = LibraryService()
        library_service.repository = LibraryRepository()
        return library_service

    # region add

    def add_test_new(self, target: LibraryService):
        '''
        Success
        Add new library into repository
        '''

        formatted_path = 'C:\\test'
        sub_directories = [
            'C:\\test\\test1',
            'C:\\test\\test2',
        ]

        # * Prepare
        target.utility.format_path = MagicMock(return_value=formatted_path)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(
            return_value=sub_directories)

        # * Key
        # Could not find library in repository
        target.find = MagicMock(return_value=None)
        target.library_manager.init_library = MagicMock(
            side_effect=lambda path: (ActionResult(), Library(path)))
        target.library_manager.reload = MagicMock()

        # * Act
        result = target.add(self.test_dir)

        # * Assert
        assert target.library_manager.init_library.call_count == 3
        assert not target.library_manager.reload.called
        assert result.success()
        assert not result.messages
        assert len(target.repository.library_list) == 3

        target.utility.format_path.assert_called_with(self.test_dir)
        target.utility.is_dir.assert_called_with(formatted_path)

    def add_test_reload(self, target: LibraryService):
        '''
        Success
        Call reload method instead initialize new library
        '''

        formatted_path = 'C:\\test'
        sub_directories = [
            'C:\\test\\test1',
            'C:\\test\\test2',
        ]

        # * Prepare
        target.utility.format_path = MagicMock(return_value=formatted_path)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(
            return_value=sub_directories)

        # * Key
        # Could library found in repository, reload
        target.find = MagicMock(side_effect=lambda path: Library(path))
        target.library_manager.init_library = MagicMock()
        target.library_manager.reload = MagicMock(
            side_effect=lambda library: (ActionResult(), library))

        # * Act
        result = target.add(self.test_dir)

        # * Assert
        assert not target.library_manager.init_library.called
        assert target.library_manager.reload.call_count == 3
        assert result.success()
        assert len(result.messages) == 3
        assert result.messages[0].type == MessageType.INFO
        assert not target.repository.library_list

        target.utility.format_path.assert_called_with(self.test_dir)
        target.utility.is_dir.assert_called_with(formatted_path)

    def add_test_init_failed(self, target: LibraryService):
        '''
        Success
        New library failed to initialize
        '''

        formatted_path = 'C:\\test'
        sub_directories = [
            'C:\\test\\test1',
            'C:\\test\\test2',
        ]
        failed_result = ActionResult()
        failed_result.add_error('Failed')

        # * Prepare
        target.utility.format_path = MagicMock(return_value=formatted_path)
        target.utility.is_dir = MagicMock(return_value=True)
        target.utility.get_directories = MagicMock(
            return_value=sub_directories)

        # * Key
        # Could not find library in repository
        target.find = MagicMock(return_value=None)
        target.library_manager.init_library = MagicMock(
            side_effect=lambda path: (failed_result, None))
        target.library_manager.reload = MagicMock()

        # * Act
        result = target.add(self.test_dir)

        # * Assert
        assert target.library_manager.init_library.call_count == 3
        assert not target.library_manager.reload.called
        assert result.success()
        assert len(result.messages) == 3
        assert not target.repository.library_list

        target.utility.format_path.assert_called_with(self.test_dir)
        target.utility.is_dir.assert_called_with(formatted_path)

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

    # def find_test(self, target: LibraryService):
    #     # * Prepare
    #     library = Library(self.test_dir)
    #     target.utility.format_path = MagicMock(return_value=self.test_dir)

    #     # * Key
    #     target.repository.add(library)

    #     # * Act
    #     result = target.find('C://')

    #     # * Assert
    #     assert bool(result)
    #     assert result.path == self.test_dir

    # def find_script_test(self, target: LibraryService):
    #     # * Prepare
    #     script_path = 'C:\\Script'

    #     library = Library(self.test_dir)
    #     target.utility.format_path = MagicMock(return_value=self.test_dir)

    #     # * Key
    #     library.add(Script(script_path))
    #     target.repository.add(library)

    #     # * Act
    #     result = target.find_script(script_path)

    #     # * Assert
    #     assert bool(result)
    #     assert result.path == script_path

    # endregion find

    # region remove

    def remove_test_library_not_exists(self, target: LibraryService):
        """
        Success
        Library does not exists in the repository
        """

        # * Prepare
        remove_library_id = "C:\\"

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result = target.remove(remove_library_id)

        # * Assert
        assert result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.WARNING

    def remove_test_library_failed(self, target: LibraryService):
        """
        Remove library failed
        Returns error messages
        """

        # * Prepare
        library = Library(self.test_dir)
        remove_result = ActionResult()
        remove_result.add_error("Error")

        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.remove = MagicMock(return_value=remove_result)

        # * Act
        result = target.remove(self.test_dir)

        # * Assert
        assert not result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.ERROR

    def remove_test_library(self, target: LibraryService):
        """
        Remove library failed
        Returns error messages
        """

        # * Prepare
        library = Library(self.test_dir)
        remove_result = ActionResult()

        target.find = MagicMock(return_value=library)

        # * Key
        target.repository.add(library)
        target.repository.remove = MagicMock()
        target.library_manager.remove = MagicMock(return_value=remove_result)

        # * Act
        result = target.remove(self.test_dir)

        # * Assert
        assert result.success()
        assert not result.messages

        assert target.repository.remove.called

    # endregion remove

    # region remove script

    def remove_script_test_script_not_exists(self, target: LibraryService):
        """
        Success
        Script does not exist, return warning
        """

        # * Prepare
        script_id = 'C:\\test.ahk'

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result = target.remove_script(script_id)

        # * Assert
        assert result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.WARNING

    def remove_script_test_failed(self, target: LibraryService):
        """
        Remove script failed
        Return error messages
        """

        # * Prepare
        script_id = 'C:\\test.ahk'
        script = Script(script_id)
        remove_result = ActionResult()
        remove_result.add_error("Error")

        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.remove = MagicMock(return_value=remove_result)
        target.find_library_contains_script = MagicMock()

        # * Act
        result = target.remove_script(script_id)

        # * Assert
        assert not result.success()
        assert result.messages
        assert result.messages[0].type == MessageType.ERROR

        assert not target.find_library_contains_script.called

    def remove_script_test(self, target: LibraryService):
        """
        Success
        """

        # * Prepare
        script_id = 'C:\\test.ahk'
        script = Script(script_id)

        remove_result = ActionResult()
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.remove = MagicMock(return_value=remove_result)
        target.find_library_contains_script = MagicMock()

        # * Act
        result = target.remove_script(script_id)

        # * Assert
        assert result.success()
        assert not result.messages

    # endregion remove script

    # region start

    def start_test_library_not_exists(self, target: LibraryService):
        """
        Library not exists
        Return error
        """

        # * Prepare

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result, library = target.start(self.test_dir)

        # * Assert
        assert not result.success()
        assert library is None

    def start_test(self, target: LibraryService):
        """
        Success
        Return library
        """

        # * Prepare
        library = Library(self.test_dir)
        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.start = MagicMock(
            return_value=(ActionResult(), library))

        # * Act
        result, result_library = target.start(self.test_dir)

        # * Assert
        assert result.success()
        assert result_library.identifier() == library.identifier()

    # endregion start

    # region start script

    def start_script_test_script_not_exists(self, target: LibraryService):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare
        script_id = 'C:\\script.ahk'

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.start_script(script_id)

        # * Assert
        assert not result.success()
        assert result_script is None

    def start_script_test(self, target: LibraryService):
        """
        Success
        """

        # * Prepare
        script_id = 'C:\\script.ahk'
        script = Script(script_id)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.start = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.start_script(script_id)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion start script

    # region restart script

    def restart_script_test_script_not_exists(self, target: LibraryService):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare
        script_id = 'C:\\script.ahk'

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.restart_script(script_id)

        # * Assert
        assert not result.success()
        assert result_script is None

    def restart_script_test(self, target: LibraryService):
        """
        Success
        """

        # * Prepare
        script_id = 'C:\\script.ahk'
        script = Script(script_id)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.restart = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.restart_script(script_id)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion restart script

    # region stop

    def stop_test_library_not_exists(self, target: LibraryService):
        """
        Library not exists
        Return error
        """

        # * Prepare

        # * Key
        target.find = MagicMock(return_value=None)

        # * Act
        result, library = target.stop(self.test_dir)

        # * Assert
        assert not result.success()
        assert library is None

    def stop_test(self, target: LibraryService):
        """
        Success
        Return library
        """

        # * Prepare
        library = Library(self.test_dir)
        target.find = MagicMock(return_value=library)

        # * Key
        target.library_manager.stop = MagicMock(
            return_value=(ActionResult(), library))

        # * Act
        result, result_library = target.stop(self.test_dir)

        # * Assert
        assert result.success()
        assert result_library.identifier() == library.identifier()

    # endregion stop

    # region stop script

    def stop_script_test_script_not_exists(self, target: LibraryService):
        """
        Script not exist in any library
        Return error
        """

        # * Prepare
        script_id = 'C:\\script.ahk'

        # * Key
        target.find_script = MagicMock(return_value=None)

        # * Act
        result, result_script = target.stop_script(script_id)

        # * Assert
        assert not result.success()
        assert result_script is None

    def stop_script_test(self, target: LibraryService):
        """
        Success
        """

        # * Prepare
        script_id = 'C:\\script.ahk'
        script = Script(script_id)
        target.find_script = MagicMock(return_value=script)

        # * Key
        target.script_manager.stop = MagicMock(
            return_value=(ActionResult(), script))

        # * Act
        result, result_script = target.stop_script(script_id)

        # * Assert
        assert result.success()
        assert script.identifier() == result_script.identifier()

    # endregion stop script

    # region stop all

    def stop_all_test_could_not_stop_some_script(
            self, target: LibraryService):
        """
        Could not stop some script in the library
        Return warning message
        """

        # * Prepare
        target.repository.add(Library(self.test_dir))
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
            self, target: LibraryService):
        """
        Success
        """

        # * Prepare
        library = Library(self.test_dir)
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

    def refresh_test_library_path_not_exists(self, target: LibraryService):
        """
        Library path not exists on disk
        """

        # * Prepare
        target.repository.add(Library(self.test_dir))
        refresh_result = ActionResult()
        refresh_result.add_error('Could not find library')

        # * Key
        target.library_manager.refresh = MagicMock(return_value=refresh_result)

        # * Act
        target.refresh()

        # * Assert
        assert target.library_manager.refresh.called

    def refresh_test(self, target: LibraryService):
        """
        Library path not exists on disk
        """

        # * Prepare
        target.repository.add(Library(self.test_dir))
        refresh_result = ActionResult()

        # * Key
        target.library_manager.refresh = MagicMock(return_value=refresh_result)

        # * Act
        target.refresh()

        # * Assert
        assert target.library_manager.refresh.called

    # endregion refresh

    # region get all scripts

    def get_all_scripts_test(self, target: LibraryService):
        # * Prepare
        script_path = "C:\\script.py"
        library = Library(self.test_dir)
        library.add(Script(script_path))
        target.repository.add(library)

        # * Key
        # * Act
        result = target.get_all_scripts()

        # * Assert
        assert result
        assert result[0].identifier() == script_path

    # endregion get all scripts

    # region pause all

    def test_pause_all(self, target: LibraryService):
        """
        Pause all success
        """

        # * Prepare
        library_1 = Library(self.test_dir)
        library_1.add(Script('Test1'))
        library_1.add(Script('Test2'))

        library_2 = Library(self.test_dir_2)
        library_2.add(Script('Test3'))
        library_2.add(Script('Test4'))

        target.repository.add(library_1)
        target.repository.add(library_2)
        target.library_manager.pause = MagicMock(
            side_effect=self._pause_all_library_manager_pause)

        # * Key

        # * Act
        result = target.pause_all()

        # * Assert
        assert result.success()
        assert not result.messages

        for library in target.repository.library_list:
            assert library.is_paused()

    def _pause_all_library_manager_pause(self, library: Library):
        library.pause()
        return ActionResult(), library

    # endregion pause all


if __name__ == '__main__':
    pytest.main()
