from typing import List

from core.model.message import Message
from core.model.singleton import Singleton


class MessageService(metaclass=Singleton):

    def __init__(self):
        self.messages: List[Message] = []

    def add(self, message: Message):
        if not message and not isinstance(message, Message):
            return

        self.messages.append(message)
