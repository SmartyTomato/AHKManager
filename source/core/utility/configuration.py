import os
import json
from configparser import SafeConfigParser


# ------------------------------------------------------------------ #
# helper methods
# ------------------------------------------------------------------ #
def make_file_dirs(path):
    # create file and all folder required
    if not os.path.exists(path):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            return False

    return True


class Configuration(object):
    # const paths
    config_path_section_name = 'config path'
    config_path = 'configs\\ahk_manager.config'
    repo_config_path = 'configs\\repository.config'

    # utility
    enable_save = True
    enable_logging = True
    file_types = ['.ahk']
    ahk_executable = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'

    # application
    title_main_window = 'AHK Manager'

    instance = None

    @staticmethod
    def get():
        if Configuration.instance is None:
            instance = Configuration()
            return instance

        return instance

    def save(self):
        if not self.enable_save:
            return

        config = SafeConfigParser()

        # path configs
        config.add_section(self.config_path_section_name)
        config.set(self.config_path_section_name,
                   'config_path', self.config_path)

        make_file_dirs(self.config_path)

        with open(self.config_path, 'w') as outfile:
            config.write(outfile)

    def load(self):
        if not self.enable_save:
            return

        # if config file is not found
        if not os.path.exists(self.config_path):
            self.save()
            return

        config = SafeConfigParser()
        config.read(self.config_path)

        self.config_path = config.get(
            self.config_path_section_name, 'config_path')

    def save_repository(self, repo_manager):
        if not self.enable_save:
            return

        make_file_dirs(self.repo_config_path)

        with open(self.repo_config_path, 'w') as outfile:
            outfile.write(json.dumps(repo_manager.to_json(),
                                     sort_keys=True, indent=4))

    def load_repository(self):
        if not self.enable_save:
            return

        if not os.path.exists(self.repo_config_path):
            return

        with open(self.repo_config_path, 'r') as infile:
            return json.load(infile)

        return None

# class DevConfig(Configuration):
#     file_types = ['.ahk', '.txt']
