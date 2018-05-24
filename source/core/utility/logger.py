import logging
from core.utility.configuration import Configuration

class Logger(object):

    @staticmethod
    def log_info(info):
        if Configuration.get().enable_logging:
            print(info)
            # logging.info(info)
            