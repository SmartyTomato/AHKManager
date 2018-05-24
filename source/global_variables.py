# error and warning message that used in any component and return to the screen.
# clear this in the manager before calling the functions
error_messages = []
warning_messages = []

from core.manager.process_manager import ProcessManager
process_manager = ProcessManager()

from core.manager.repo_manager import RepoManager
repo_manager = RepoManager()
