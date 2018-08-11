from enum import IntEnum


class MessageType(IntEnum):
    Log = 0
    WARNING = 1
    ERROR = 2


class Message():

    def __init__(self, msg_type: MessageType, message: str) -> None:
        self.type: MessageType = MessageType(msg_type)
        self.message: str = message

    def __str__(self):
        out = []
        out.append('Message:')
        out.append('\t Type: {}'.format(str(self.type)))
        out.append('\t Message: {}'.format(self.message))

        return '\n'.join(out)
