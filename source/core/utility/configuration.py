import json
import os
from configparser import ConfigParser, NoSectionError

from core.model.singleton import Singleton
from core.service.message_service import MessageService
from core.utility.logger import Logger
from core.utility.message import Message, MessageType


class Configuration(Singleton):
    logger = Logger('Configuration')

    message_service = MessageService()

    # path
    utility_section_name = 'utility'
    main_window_section_name = 'main_window'

    # const paths
    config_path = os.getcwd() + '\\configs\\ahk_manager.config'
    library_config_path = os.getcwd() + '\\configs\\library.config'
    profile_config_path = os.getcwd() + '\\configs\\profile.config'

    # utility
    utility = {
        'enable_save': True,
        'enable_logging': False,
        'log_level': 2,
        'enable_debugging': True,
        'file_types': ['.ahk'],
        'ahk_executable': 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'
    }

    # main_window
    main_window = {
        'name': 'AHK Manager',
        'width': 1000,
        'height': 800
    }

    # add_script_window
    add_script_dialog = {
        'name': 'Add script to profile',
        'width': 1000,
        'height': 800
    }

    # region public methods

    def save(self, profile_repository, library_reopsitory):
        if not self.utility['enable_save']:
            # this should not happen in released version, so do not add warning message
            self.logger.info('Saving is not enabled')
            return

        self._save_general_configs()
        self._save_repository(profile_repository, self.profile_config_path)
        self._save_repository(library_reopsitory, self.library_config_path)

    def load(self):
        if not self.utility['enable_save']:
            self.logger.info('Load is not enabled')
            return

        # if config file is not found
        if not os.path.exists(self.config_path):
            self.logger.info('Configuration does not exists')
            self._save_general_configs()
            return

        config = ConfigParser()

        try:
            config.read(self.config_path)
        except OSError as error:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not read file: {}'.format(self.config_path)))
            self.logger.error('Could not read file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))
            return

        try:
            # utility configs
            for (key, value) in config.items(self.utility_section_name):
                if isinstance(self.utility[key], list):
                    self.utility[key] = []
                    # remove the bracket
                    value = value[1:-1]
                    for item in value.split(','):
                        item = self._find_between(item, "'", "'")
                        self.utility[key].append(item)
                    continue
                elif isinstance(self.utility[key], bool):
                    self.utility[key] = value == 'True'
                else:
                    self.utility[key] = type(self.utility[key])(value)

            # main window
            for (key, value) in config.items(self.main_window_section_name):
                self.main_window[key] = type(self.main_window[key])(value)

        except (NoSectionError, KeyError) as error:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not find section: {}'.format(error)))
            self.logger.error('Could not find section >>> {}'.format(error))
            # if error, then override the saved config to ensure no error next time
            self._save_general_configs()

    def load_profiles(self):
        return self._load_repository(self.profile_config_path)

    def load_libraries(self):
        return self._load_repository(self.library_config_path)

    # endregion public methods

    # region private methods

    def _save_general_configs(self):
        config = ConfigParser()

        # utility configs
        section = self.utility_section_name
        config.add_section(section)
        for (key, value) in self.utility.items():
            config.set(section, str(key), str(value))

        # main window settings
        section = self.main_window_section_name
        config.add_section(section)
        for (key, value) in self.main_window.items():
            config.set(section, str(key), str(value))

        if not self._make_dirs(self.config_path):
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not save configuration to path: {}'.format(self.config_path)))
            self.logger.error('Could not save configuration >>> {}'.format(repr(self)))
            return

        try:
            with open(self.config_path, 'w') as outfile:
                config.write(outfile)
        except OSError as error:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not write to file: {}'.format(self.config_path)))
            self.logger.error('Could not write to file >>> Path: {path} | Error: {error}'.format(
                path=self.config_path, error=error))

    def _save_repository(self, repository, path: str):
        if not self._make_dirs(path):
            self.message_service.add(Message(MessageType.ERROR, 'Could not save repository'))
            self.logger.error('Could not make directory >>> {path}'.format(path=path))
            return

        try:
            with open(path, 'w') as outfile:
                outfile.write(json.dumps(repository.to_json(), sort_keys=True, indent=4))
        except OSError as error:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not write file: {path}'.format(path=path)))
            self.logger.error('Could not write file >>> Path: {path} | Error: {error}'.format(
                path=path, error=error))

    def _load_repository(self, path: str)-> str:
        if not self.utility['enable_save']:
            return None

        if not os.path.exists(path):
            self.logger.info('Repository does not exists')
            return None

        try:
            with open(path, 'r') as infile:
                return json.load(infile)
        except OSError as error:
            self.message_service.add(
                Message(MessageType.ERROR, 'Could not read file: {path}'.format(path=self.config_path)))
            self.logger.error(
                'Could not read file >>> Path: {path} | Error: {error}'.format(path=self.config_path, error=error))
            return None

    @staticmethod
    def _find_between(in_str, first: str, last: str)->str:
        try:
            start = in_str.index(first) + len(first)
            end = in_str.index(last, start)
            return in_str[start:end]
        except ValueError:
            return ""

    @staticmethod
    def _make_dirs(path: str) -> bool:
        # create file and all folder required
        if not os.path.exists(path) and not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as error:
                Configuration.message_service.add(
                    Message(MessageType.ERROR, 'Could not make directory for file: {}'.format(path)))
                Configuration.logger.error(
                    'Could not make directory for file >>> Path: {path} | Error: {error}'.format(path=path,
                                                                                                 error=error))
                return False

        return True

    # endregion private methods


class DevConfig(Configuration):
    file_types = ['.ahk', '.txt']
