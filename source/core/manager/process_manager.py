import subprocess

from core.utility.configuration import Configuration


class ProcessManager(object):

    @staticmethod
    def start(path):
        return subprocess.Popen([Configuration.get().ahk_executable, path], shell=False)
