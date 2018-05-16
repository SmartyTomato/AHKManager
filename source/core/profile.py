class Profile(object):
    def __init__(self, name):
        self.script_list = []
        self.name = name

    def add(self, script):
        """
        add script into the profile
        :param script:
        :return:
        """
        if script is not None:
            self.script_list.append(script)

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
