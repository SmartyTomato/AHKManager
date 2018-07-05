from typing import List

from core.model.singleton import Singleton
from core.utility.message import Message


class MessageService(Singleton):

    def __init__(self):
        self.messages: List[Message] = []

    def add(self, message: Message):
        if not message and not isinstance(message, Message):
            return

        self.messages.append(message)
