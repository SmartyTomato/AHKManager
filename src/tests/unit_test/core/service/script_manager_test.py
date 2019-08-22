import pytest

from unittest.mock import MagicMock

from src.core.model.script import Script
from src.core.model.action_result import ActionResult
from src.core.manager.script_manager import ScriptManager


class ScriptProcessMock:
    def kill(self):
        pass


class ScriptManagerTest:
    script_path = 'C:\\test.py'

    @pytest.fixture()
    def target(self) -> ScriptManager:
        return ScriptManager()

    @pytest.fixture()
    def script(self) -> Script:
        return Script(self.script_path)

    def pause_test_script_not_running(
            self, target: ScriptManager, script: Script):
        # * Prepare

        # * Act
        result, script = target.pause(script)

        # * Assert
        assert result.success()

    def pause_test_not_allow_state_change(
            self, target: ScriptManager, script: Script):
        # * Prepare
        script.start(ScriptProcessMock())
        script.lock()

        # * Act
        result, script = target.pause(script)

        # * Assert
        assert not result.success()
        assert not script.is_paused()

    def pause_test_could_not_kill_process(
            self, target: ScriptManager, script: Script):
        # * Prepare
        script.start(ScriptProcessMock())
        script.process.kill = MagicMock(side_effect=Exception())

        # * Act
        result, script = target.pause(script)

        # * Assert
        assert not result.success()
        assert not script.is_paused()

    def pause_test(
            self, target: ScriptManager, script: Script):
        # * Prepare
        script.start(ScriptProcessMock())

        # * Act
        result, script = target.pause(script)

        # * Assert
        assert result.success()
        assert script.is_paused()

    def resume_test_not_paused(self, target: ScriptManager, script: Script):
        # * Prepare

        # * Act
        result, script = target.resume(script)

        # * Assert
        assert result.success()
        assert not script.is_running()

    def resume_test_script_locked(
            self, target: ScriptManager, script: Script):
        # * Prepare
        script.pause()
        script.lock()

        # * Act
        result, script = target.resume(script)

        # * Assert
        assert not result.success()

    def resume_test(
            self, target: ScriptManager, script: Script):
        # * Prepare
        script.pause()
        script.start('123')

        target._start_script = MagicMock(
            side_effect=lambda x: (ActionResult(), x))

        # * Act
        result, script = target.resume(script)

        # * Assert
        assert result.success()


if __name__ == '__main__':
    pytest.main()
