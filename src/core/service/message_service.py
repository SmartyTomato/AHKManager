from typing import List

from src.core.model.message import Message


class MessageService:
    """
    ! Currently not used, avoid use it if possible
    """

    messages: List[Message] = []

    def add(self, message: Message):
        if not message and not isinstance(message, Message):
            return

        self.messages.append(message)
