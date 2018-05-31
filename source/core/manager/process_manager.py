import subprocess

from core.utility.configuration import Configuration
from core.utility.logger import MethodBoundaryLogger, Logger


class ProcessManager(object):
    _logger = Logger('ProcessManager')

    @staticmethod
    @MethodBoundaryLogger(_logger)
    def start(path):
        return subprocess.Popen([Configuration.get().ahk_executable, path], shell=False)
