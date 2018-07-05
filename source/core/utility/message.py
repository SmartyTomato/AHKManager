from enum import Enum


class Message(object):

    def __init__(self, msg_type, message):
        self.type = msg_type
        self.message = message

    def __str__(self):
        out = []
        out.append('Message:')
        out.append('\t Type: {}'.format(str(self.type)))
        out.append('\t Message: {}'.format(str(self.message)))

        return '\n'.join(out)


class MessageType(Enum):
    WARNING = 2
    ERROR = 3
