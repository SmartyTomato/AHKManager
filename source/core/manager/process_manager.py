import subprocess
from subprocess import Popen

from core.model.singleton import Singleton
from core.service.message_service import MessageService
from core.utility.configuration import Configuration
from core.utility.logger import Logger
from core.utility.message import Message, MessageType


class ProcessManager(Singleton):
    logger = Logger('ProcessManager')

    message_service = MessageService()
    configuration = Configuration()

    @staticmethod
    def start(path: str) -> Popen:
        ahk_path = ProcessManager.configuration.utility['ahk_executable']
        if not ahk_path:
            ProcessManager.message_service.add(
                Message(MessageType.ERROR, 'AutoHotKey path is not valid: {}'.format(ahk_path)))
            ProcessManager.logger.error(
                Message(MessageType.ERROR, 'AutoHotKey path is not valid >>> {}'.format(ahk_path)))
            return None

        return subprocess.Popen([ahk_path, path], shell=False)
