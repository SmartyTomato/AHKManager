import json
import os

from src.core.model.configuration_models import (AddScriptDialogConfiguration,
                                             MainWindowConfiguration,
                                             SettingsDialogConfiguration,
                                             UtilityConfiguration)
from src.core.service.message_service import MessageService
from src.core.utility.logger import Logger


class Configuration:
    logger = Logger('Configuration')

    message_service = MessageService()

    config_path = os.getcwd() + '\\configs\\ahk_manager.config'
    library_config_path = os.getcwd() + '\\configs\\library.config'
    profile_config_path = os.getcwd() + '\\configs\\profile.config'

    # configuration paths
    utility = UtilityConfiguration()
    main_window = MainWindowConfiguration()
    add_script_dialog = AddScriptDialogConfiguration()
    settings_dialog = SettingsDialogConfiguration()

    # region public methods

    def save(self, profile_repository, library_repository):
        """
        Save configurations including general config and repositories

        Args:
            profile_repository (ProfileRepository): profile repository
            library_repository (LibraryRepository): library repository
        """

        # Save general settings
        self.save_general_configs()

        if not self.utility.enable_save:
            # ! This for testing purpose only
            # ! Save should always enabled in release version
            self.logger.info('Saving is not enabled')
            return

        # Save profile repository
        self._save_repository(profile_repository, self.profile_config_path)
        # Save library repository
        self._save_repository(library_repository, self.library_config_path)

    def save_general_configs(self):
        """
        Save general configurations, such as utility,
        and dialog sizes
        """

        # * Make parent directories
        if not self._make_dirs(self.config_path):
            # ! Failed to create parent directory, file cannot be saved
            return

        # Build output json string
        out = {}

        out['utility'] = self.utility.to_json()
        out['main_window'] = self.main_window.to_json()
        out['add_script_dialog'] = self.add_script_dialog.to_json()
        out['settings_dialog'] = self.settings_dialog.to_json()

        # Save json string to file
        try:
            with open(self.config_path, 'w') as outfile:
                outfile.write(json.dumps(out, indent=4))
        except Exception:
            # ! Something went wrong when saving the file
            return

    def load(self):
        """
        Load general configuration
        """

        # ? config file is not found?
        if not os.path.exists(self.config_path):
            self.logger.info('Configuration does not exists')
            self.save_general_configs()
            return

        try:
            with open(self.config_path, 'r') as infile:
                temp = json.load(infile)
                self.utility = UtilityConfiguration \
                    .from_json(temp['utility'])
                self.main_window = MainWindowConfiguration \
                    .from_json(temp['main_window'])
                self.add_script_dialog = AddScriptDialogConfiguration \
                    .from_json(temp['add_script_dialog'])
                self.settings_dialog = SettingsDialogConfiguration \
                    .from_json(temp['settings_dialog'])
        except Exception:
            # if error, then override the saved config
            # ensure no error next time
            self.save_general_configs()

    def load_profiles(self) -> str:
        """
        Load profile from config file

        Returns:
            str: json format string
        """

        return self._load_repository(self.profile_config_path)

    def load_libraries(self) -> str:
        """
        Load libray from config file

        Returns:
            str: json format string
        """

        return self._load_repository(self.library_config_path)

    # endregion public methods

    # region private methods

    def _save_repository(self, repository, path: str):
        if not self._make_dirs(path):
            return

        try:
            with open(path, 'w') as outfile:
                outfile.write(json.dumps(repository.to_json(), indent=4))
        except Exception:
            return

    def _load_repository(self, path: str)-> str:
        # ! This for testing purpose only
        # ! Save should always enabled in release version
        if not self.utility.enable_save:
            return ''

        if not os.path.exists(path):
            self.logger.info('Repository does not exists')
            return ''

        try:
            with open(path, 'r') as infile:
                return json.load(infile)
        except Exception:
            return ""

    def _find_between(self, in_str, first: str, last: str)->str:
        try:
            start = in_str.index(first) + len(first)
            end = in_str.index(last, start)
            return in_str[start:end]
        except Exception:
            return ""

    def _make_dirs(self, path: str) -> bool:
        """
        Create all required parent folder for the given file or directory

        Args:
            path (str): file or directory path

        Returns:
            bool: return true when all directories created
        """

        if (not os.path.exists(path) and
                not os.path.exists(os.path.dirname(path))):
            try:
                os.makedirs(os.path.dirname(path))
            except Exception:
                return False

        return True

    # endregion private methods


configuration = Configuration()
