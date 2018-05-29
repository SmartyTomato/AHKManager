class State:

    def __init__(self):
        self.lock = False
        self.hide = False
        self.exclude = False
        self.startup = False

        self.running = False

    def to_json(self):
        out = {}
        out['lock'] = self.lock
        out['hide'] = self.hide
        out['exclude'] = self.exclude
        out['startup'] = self.startup

        return out

    @staticmethod
    def from_json(jstr):
        status = State()

        status.lock = jstr['lock']
        status.hide = jstr['hide']
        status.exclude = jstr['exclude']
        status.startup = jstr['startup']

        return status
