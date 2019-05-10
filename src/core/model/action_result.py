from enum import IntEnum
from typing import List

from core.model.message import Message, MessageType


class ResultCode(IntEnum):
    SUCCESS = 0
    WARNING = 1
    ERROR = 2


class ActionResult():
    """
    ActionResult contains result code (e.g. success)
    and messages for the action performed
    """

    def __init__(self):
        self.code: ResultCode = ResultCode.SUCCESS
        self.messages: List[Message] = []

    # region public methods

    def add(self, code: ResultCode, message: str = ""):
        """
        Add new message to the result

        Args:
            code (ResultCode): message code:
                SUCCESS = 0
                WARNING = 1
                ERROR = 2
            message (str):
        """

        self._set_code(code)
        self.messages.append(Message(MessageType(int(code)), message))

    def add_info(self, message: str = ""):
        """
        Add new message to the result

        Args:
            code (ResultCode): message code:
                SUCCESS = 0
                WARNING = 1
                ERROR = 2
            message (str):
        """

        self._set_code(ResultCode.SUCCESS)
        self.messages.append(
            Message(MessageType(int(ResultCode.SUCCESS)), message))

    def add_warning(self, message: str):
        """
        Add new warning message to the result

        Args:
            message (str): warning message
        """

        self._set_code(ResultCode.WARNING)
        self.messages.append(Message(MessageType.WARNING, message))

    def add_error(self, message: str):
        """
        Add new error message to the result

        Args:
            message (str): error message
        """

        self._set_code(ResultCode.ERROR)
        self.messages.append(Message(MessageType.ERROR, message))

    def merge(self, result):
        """
        Merge result code and messages
        The result code will in this order:
            error -> warning -> success

        Args:
            result (ActionResult): the other result
                object
        """

        self._set_code(result.code)
        self.messages.extend(result.messages)

    def success(self) -> bool:
        """
        Check whether action success

        Returns:
            bool: return True when message does not
                contain error
        """

        return self.code < ResultCode.ERROR

    def ignore_error(self):
        """
        Ignore all errors, convert error to warnings
        """

        if not self.success():
            self._force_set_code(ResultCode.WARNING)

        for i in range(0, len(self.messages)):
            message = self.messages[i]
            if message.type > MessageType.WARNING:
                self.messages[i].type = MessageType.WARNING

    def get_result_code(self) -> ResultCode:
        """
        Get result type code

        Returns:
            ResultCode: return error if any message is error
                        return warning if any message is warning but no error
                        return success if all success
        """

        # Find whether message contains error
        error = list(filter(
            lambda x: x.type == MessageType.ERROR, self.messages))
        if error:
            return ResultCode.ERROR

        # Find whether message contains warning
        warning = list(filter(
            lambda x: x.type == MessageType.WARNING, self.messages))

        if warning:
            return ResultCode.WARNING

        # Message only contains infos
        return ResultCode.SUCCESS

    # endregion public methods

    # region private methods

    def _force_set_code(self, code: ResultCode):
        self.code = code

    def _set_code(self, code: ResultCode):
        if self.code > code:
            return

        self.code = code

    # endregion private methods
