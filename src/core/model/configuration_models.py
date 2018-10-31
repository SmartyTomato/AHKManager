class UtilityConfiguration():
    def __init__(self):
        self.enable_save = True
        self.enable_logging = False
        self.log_level = 2
        self.enable_debugging = True
        self.file_types = ['.ahk', '.txt']
        self.ahk_executable = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'

    def to_json(self):
        out = {}

        out['enable_save'] = self.enable_save
        out['enable_logging'] = self.enable_logging
        out['log_level'] = self.log_level
        out['enable_debugging'] = self.enable_debugging
        out['file_types'] = self.file_types
        out['ahk_executable'] = self.ahk_executable

        return out

    @staticmethod
    def from_json(json_str):
        config = UtilityConfiguration()
        config.enable_save = json_str['enable_save']
        config.enable_logging = json_str['enable_logging']
        config.log_level = json_str['log_level']
        config.enable_debugging = json_str['enable_debugging']
        config.file_types = json_str['file_types']
        config.ahk_executable = json_str['ahk_executable']

        return config


class MainWindowConfiguration():
    def __init__(self):
        self.name = 'AHK Manager'
        self.width = 1000
        self.height = 800
        self.icon_path = 'resources/icon/icon.png'

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['width'] = self.width
        out['height'] = self.height
        out['icon_path'] = self.icon_path

        return out

    @staticmethod
    def from_json(json_str):
        config = MainWindowConfiguration()
        config.name = json_str['name']
        config.width = json_str['width']
        config.height = json_str['height']
        config.icon_path = json_str['icon_path']

        return config


class AddScriptDialogConfiguration():
    def __init__(self):
        self.name = 'Add script to profile'
        self.width = 1000
        self.height = 800

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['width'] = self.width
        out['height'] = self.height

        return out

    @staticmethod
    def from_json(json_str):
        config = AddScriptDialogConfiguration()
        config.name = json_str['name']
        config.width = json_str['width']
        config.height = json_str['height']

        return config


class SettingsDialogConfiguration():
    def __init__(self):
        self.name = 'Settings'
        self.width = 400
        self.height = 300

    def to_json(self):
        out = {}

        out['name'] = self.name
        out['width'] = self.width
        out['height'] = self.height

        return out

    @staticmethod
    def from_json(json_str):
        config = SettingsDialogConfiguration()
        config.name = json_str['name']
        config.width = json_str['width']
        config.height = json_str['height']

        return config
