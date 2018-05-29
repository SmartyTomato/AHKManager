# import logging


class Logger(object):

    @staticmethod
    def log_info(msg):
        from core.utility.configuration import Configuration
        if Configuration.get().enable_logging:
            print(msg)
            # logging.debug(msg)

    @staticmethod
    def log_error(msg):
        from core.utility.configuration import Configuration
        if Configuration.get().enable_logging:
            print('ERROR: ' + msg)

    @staticmethod
    def log_warning(msg):
        from core.utility.configuration import Configuration
        if Configuration.get().enable_logging:
            print('Warning: ' + msg)
