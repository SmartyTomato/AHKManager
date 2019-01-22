import pytest

from typing import Dict
from unittest.mock import MagicMock

from core.model.script import Script
from core.model.library import Library
from core.model.action_result import ActionResult
from core.manager.library_manager import LibraryManager


class LibraryManagerTest:
    example_paths: Dict = {
        'directory': 'C:\\test',
        'files': [
            'C:\\test\\script.ahk',
            'C:\\test\\script1.ahk',
            'C:\\test\\script2.ahk',
            'C:\\test\\script3.ahk',
            'C:\\test\\script4.ahk'],
    }

    @pytest.fixture()
    def target(self) -> LibraryManager:
        return LibraryManager()

    @pytest.fixture()
    def library(self) -> Library:
        lib = Library(self.example_paths['directory'])
        for file in self.example_paths['files']:
            lib.add(Script(file))

        return lib

    def pause_test(self, target: LibraryManager, library: Library):
        # * Prepare
        library.start()

        target.script_manager.pause = MagicMock(
            side_effect=lambda script: (ActionResult(), script))

        # * Act
        result, library = target.pause(library)

        # * Assert
        assert result.success()
        assert not result.messages
        assert library.is_paused()

    def resume_test(self, target: LibraryManager, library: Library):
        # * Prepare
        target.script_manager.resume = MagicMock(
            side_effect=lambda script: (ActionResult(), script))

        # * Act
        result, library = target.resume(library)

        # * Assert
        assert result.success()
        assert library.is_running()

    def resume_test_has_error(self, target: LibraryManager, library: Library):
        # * Prepare
        error_result = ActionResult()

        target.script_manager.resume = MagicMock(
            side_effect=lambda x: (error_result, x))

        # * Act
        result, library = target.resume(library)

        # * Assert
        assert result.success()
        assert library.is_running()


if __name__ == '__main__':
    pytest.main()
