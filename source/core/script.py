from source.core.common import get_file_name


class Script(object):
    def __init__(self, path):
        """
        initialize script with a file path.
        :param path:
        """
        self.lock = False
        self.startup = False
        self.script = "ahk script"
        self.hide = False
        self.exclude = False
        self.script_path = path
        self.title = get_file_name(path)
        self.enabled = False