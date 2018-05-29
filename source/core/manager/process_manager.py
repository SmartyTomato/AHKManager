import subprocess

from core.utility.configuration import Configuration
from core.utility.logger import Logger


class ProcessManager(object):

    @staticmethod
    def start(path):
        Logger.log_info('Launch >>> {path}'.format(path=path))

        return subprocess.Popen([Configuration.get().ahk_executable, path], shell=False)
