class GlobalVariable(object):
    # error and warning message that used in any component and return to the screen.
    # clear this in the manager before calling the functions
    error_messages = []
    warning_messages = []

    repo_manager = None
    process_manager = None

    @staticmethod
    def get_repo_manager():
        if GlobalVariable.repo_manager is None:
            from core.manager.repo_manager import RepoManager
            GlobalVariable.repo_manager = RepoManager()

        return GlobalVariable.repo_manager

    @staticmethod
    def get_process_manager():
        if GlobalVariable.process_manager is None:
            from core.manager.process_manager import ProcessManager
            GlobalVariable.process_manager = ProcessManager()

        return GlobalVariable.process_manager

    @staticmethod
    def clear_messages():
        GlobalVariable.error_messages = []
        GlobalVariable.warning_messages = []
