import os
import json
from configparser import SafeConfigParser
from core.utility.logger import Logger
from core.model.global_variable import GlobalVariable


# ------------------------------------------------------------------ #
# helper methods
# ------------------------------------------------------------------ #
def make_file_dirs(path):
    Logger.log_info('Make directory for file >>> {path}'.format(path=path))
    # create file and all folder required
    if not os.path.exists(path):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as error:
            GlobalVariable.add_error_message('Unable to make directory >>> Path: {path} | Error: {error}'.format(path=path, error=error))
            return False

    return True


class Configuration(object):
    instance = None

    @staticmethod
    def get():
        if Configuration.instance is None:
            Configuration.instance = DevConfig()

        return Configuration.instance

    config_path_section_name = 'config path'
    utility_section_name = 'utility'
    application_section_name = 'application'

    # const paths
    config_path = 'configs\\ahk_manager.config'
    repo_config_path = 'configs\\repository.config'

    # utility
    enable_save = True
    enable_logging = True
    file_types = ['.ahk']
    ahk_executable = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'

    # application
    title_main_window = 'AHK Manager'

    def save(self):
        Logger.log_info('Save configuration >>> {path}'.format(path=self.config_path))
        if not self.enable_save:
            # this should not happen in released version, so do not add warning message
            Logger.log_warning('Saving is not enabled')
            return

        config = SafeConfigParser()

        # path configs
        config.add_section(self.config_path_section_name)
        config.set(self.config_path_section_name,
                   'config_path', self.config_path)
        config.set(self.config_path_section_name,
                   'repo_config_path', self.repo_config_path)

        # utility configs
        config.add_section(self.utility_section_name)
        config.set(self.utility_section_name,
                   'enable_save', self.enable_save)
        config.set(self.utility_section_name,
                   'enable_logging', self.enable_logging)
        config.set(self.utility_section_name,
                   'file_types', self.file_types)
        config.set(self.utility_section_name,
                   'ahk_executable', self.ahk_executable)

        # application configs
        config.add_section(self.application_section_name)
        config.set(self.utility_section_name,
                   'title_main_window', self.title_main_window)

        if not make_file_dirs(self.config_path):
            GlobalVariable.add_error_message('Unable to save configuration')
            return

        try:
            with open(self.config_path, 'w') as outfile:
                config.write(outfile)
        except OSError as error:
            GlobalVariable.add_error_message('Unable to save file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))

    def load(self):
        Logger.log_info('Load configuration >>> {path}'.format(
            path=self.config_path))
        if not self.enable_save:
            Logger.log_warning('Load is not enabled')
            return

        # if config file is not found
        if not os.path.exists(self.config_path):
            Logger.log_warning('Configuration does not exists')
            self.save()
            return

        config = SafeConfigParser()

        try:
            config.read(self.config_path)
        except OSError as error:
            GlobalVariable.add_error_message('Unable to read file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))
            return

        # path configs
        self.config_path = config.get(
            self.config_path_section_name, 'config_path')
        self.repo_config_path = config.get(
            self.config_path_section_name, 'repo_config_path')

        # utility configs
        self.enable_save = config.get(
            self.utility_section_name, 'enable_save')
        self.enable_logging = config.get(
            self.utility_section_name, 'enable_logging')
        self.file_types = config.get(
            self.utility_section_name, 'file_types')
        self.ahk_executable = config.get(
            self.utility_section_name, 'ahk_executable')

        # application
        self.title_main_window = config.get(
            self.application_section_name, 'title_main_window')

    def save_repository(self, repo_manager):
        Logger.log_info('Save repository >>> {path}'.format(
            path=self.repo_config_path))
        if not self.enable_save:
            Logger.log_warning('Save is not enabled')
            return

        if not make_file_dirs(self.repo_config_path):
            GlobalVariable.add_error_message('Unable to save repository')
            return

        try:
            with open(self.repo_config_path, 'w') as outfile:
                outfile.write(json.dumps(repo_manager.to_json(),
                                         sort_keys=True, indent=4))
        except OSError as error:
            GlobalVariable.add_error_message('Unable to write file >>> Path: {path} | Error: {error}'.format(
                path=self.repo_config_path, error=error))

    def load_repository(self):
        Logger.log_info('Load repository >>> {path}'.format(
            path=self.repo_config_path))
        if not self.enable_save:
            return

        if not os.path.exists(self.repo_config_path):
            Logger.log_warning('Repository does not exists')
            return

        try:
            with open(self.repo_config_path, 'r') as infile:
                return json.load(infile)
        except OSError as error:
            GlobalVariable.add_error_message('Unable to read file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))
            return None


class DevConfig(Configuration):
    file_types = ['.ahk', '.txt']
