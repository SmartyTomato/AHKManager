class State():

    def __init__(self):
        self.lock: bool = False
        self.startup: bool = False
        self.running: bool = False
        self.paused: bool = False

    # region to string

    def to_json(self):
        out = {}
        out['lock'] = self.lock
        out['startup'] = self.startup

        return out

    @staticmethod
    def from_json(json_str):
        state = State()

        state.lock = json_str['lock']
        state.startup = json_str['startup']

        return state

    def __str__(self):
        out = []
        out.append('State:')
        out.append('\t Running: {}'.format(str(self.running)))
        out.append('\t Lock: {}'.format(str(self.lock)))
        out.append('\t Startup: {}'.format(str(self.startup)))
        out.append('\t Paused: {}'.format(str(self.paused)))

        return '\n'.join(out)

    def __repr__(self):
        out = 'State('
        out += 'running={}, '.format(self.running)
        out += 'lock={}, '.format(self.lock)
        out += 'startup={}'.format(self.startup)
        out += 'paused={}'.format(self.paused)
        out += ')'

        return out

    # endregion to string
