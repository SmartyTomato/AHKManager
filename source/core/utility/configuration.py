import os
import json
from configparser import ConfigParser
from core.utility.logger import Logger, MethodBoundaryLogger
from core.model.global_variable import GlobalVariable


class Configuration(object):
    # private variables
    _instance = None
    _logger = Logger('Configuration')

    @staticmethod
    def get():
        if Configuration._instance is None:
            Configuration._instance = DevConfig()

        return Configuration._instance

    config_path_section_name = 'config path'
    utility_section_name = 'utility'
    application_section_name = 'application'

    # const paths
    config_path = 'configs\\ahk_manager.config'
    repo_config_path = 'configs\\repository.config'

    # utility
    enable_save = True
    enable_logging = False
    log_level = 0
    enable_debugging = True
    file_types = ['.ahk']
    ahk_executable = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'

    # application
    title_main_window = 'AHK Manager'

    @MethodBoundaryLogger(_logger)
    def save(self):
        if not self.enable_save:
            # this should not happen in released version, so do not add warning message
            self._logger.info('Saving is not enabled')
            return

        config = ConfigParser()

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

        if not self._make_file_dirs(self.config_path):
            GlobalVariable.error_messages.append(
                'Could not save configuration to path: {path}'.format(path=self.config_path))
            self._logger.error('Could not save configuration >>> Path: {path}'.format(path=self.config_path))
            return

        try:
            with open(self.config_path, 'w') as outfile:
                config.write(outfile)
        except OSError as error:
            GlobalVariable.error_messages.append('Could not write to file: {path}'.format(path=self.config_path))
            self._logger.error('Could not write to file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))

    @MethodBoundaryLogger(_logger)
    def load(self):
        if not self.enable_save:
            self._logger.info('Load is not enabled')
            return

        # if config file is not found
        if not os.path.exists(self.config_path):
            self._logger.info('Configuration does not exists')
            self.save()
            return

        config = ConfigParser()

        try:
            config.read(self.config_path)
        except OSError as error:
            GlobalVariable.error_messages.append('Could not read file: {path}'.format(path=self.config_path))
            self._logger.error('Could not read file >>> Path: {path} | Error: {error}'.format(
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

    @MethodBoundaryLogger(_logger)
    def save_repository(self, repo_manager):
        if not self.enable_save:
            self._logger.info('Save is not enabled')
            return

        if not self._make_file_dirs(self.repo_config_path):
            GlobalVariable.error_messages.append('Could not save repository')
            self._logger.error('Could not make directory >>> {path}'.format(path=self.repo_config_path))
            return

        try:
            with open(self.repo_config_path, 'w') as outfile:
                outfile.write(json.dumps(repo_manager.to_json(), sort_keys=True, indent=4))
        except OSError as error:
            GlobalVariable.error_messages.append('Could not write file: {path}'.format(path=self.repo_config_path))
            self._logger.error('Could not write file >>> Path: {path} | Error: {error}'.format(
                path=self.repo_config_path, error=error))

    @MethodBoundaryLogger(_logger)
    def load_repository(self):
        if not self.enable_save:
            return None

        if not os.path.exists(self.repo_config_path):
            self._logger.info('Repository does not exists')
            return None

        try:
            with open(self.repo_config_path, 'r') as infile:
                return json.load(infile)
        except OSError as error:
            GlobalVariable.error_messages.append('Unable to read file: {path}'.format(path=self.config_path))
            self._logger.error(
                'Unable to read file >>> Path: {path} | Error: {error}'.format(path=self.config_path, error=error))
            return None

    # ------------------------------------------------------------------ #
    # helper methods
    # ------------------------------------------------------------------ #
    @MethodBoundaryLogger(_logger)
    def _make_file_dirs(self, path):
        # create file and all folder required
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as error:
                GlobalVariable.error_messages.append('Unable to make directory for file: {path}'.format(path=path))
                self._logger.error(
                    'Unable to make directory >>> Path: {path} | Error: {error}'.format(path=path, error=error))
                return False

        return True


class DevConfig(Configuration):
    file_types = ['.ahk', '.txt']
