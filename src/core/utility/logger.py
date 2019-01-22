import datetime
import logging


class Logger:
    _log_level = {
        'log': 0,
        'debug': 1,
        'warning': 2,
        'error': 3,
        'critical': 4,
    }

    def __init__(self, module):
        self.module = module
        self.logger = logging.getLogger(module)

    def log(self, msg):
        from core.utility.configuration import Configuration
        configuration = Configuration()
        if int(configuration.utility.log_level) > int(self._log_level['log']):
            return

        msg = self._format_message('', msg)
        if configuration.utility.enable_logging:
            self.logger.debug(msg)

        if configuration.utility.enable_debugging:
            print(msg)

    def info(self, msg):
        from core.utility.configuration import Configuration
        configuration = Configuration()
        if configuration.utility.log_level > self._log_level['debug']:
            return

        msg = self._format_message('Info', msg)
        if configuration.utility.enable_logging:
            self.logger.info(msg)

        if configuration.utility.enable_debugging:
            print(msg)

    def warning(self, msg):
        from core.utility.configuration import Configuration
        configuration = Configuration()
        if configuration.utility.log_level > self._log_level['warning']:
            return

        msg = self._format_message('Warning', msg)
        if configuration.utility.enable_logging:
            self.logger.warning(msg)

        if configuration.utility.enable_debugging:
            print(msg)

    def error(self, msg):
        from core.utility.configuration import Configuration
        configuration = Configuration()
        if configuration.utility.log_level > self._log_level['error']:
            return

        msg = self._format_message('ERROR', msg)
        if configuration.utility.enable_logging:
            self.logger.error(msg)

        if configuration.utility.enable_debugging:
            print(msg)

    def critical(self, msg):
        from core.utility.configuration import Configuration
        configuration = Configuration()
        if configuration.utility.log_level > self._log_level['critical']:
            return

        msg = self._format_message('CRITICAL', msg)
        if configuration.utility.enable_logging:
            self.logger.critical(msg)

        if configuration.utility.enable_debugging:
            print(msg)

    def _format_message(self, level, msg):
        if level:
            return '{level} - {time} - {module} - {msg}'.format(
                level=level, time=datetime.datetime.now(),
                module=self.module, msg=msg)

        return '{time} - {module} - {msg}'.format(
            time=datetime.datetime.now(), module=self.module, msg=msg)

# class MethodBoundaryLogger():
#     """
#     Log when enter and exist method use default logger or the logger provided
#     """

#     def __init__(self, logger=None):
#         self.logger= logger

#     def __call__(self, func):
#         if not self.logger:
#             self.logger= Logger(func.__module__)

#         @functools.wraps(func)
#         def wrapper(*args, **kwds):

#             # start logging
#             method_name= func.__name__
#             msg= ''
#             i= 0

#             # get argument names
#             arg_names= inspect.getfullargspec(func)[0]

#             # build arguments
#             for arg in args:
#                 arg_name= arg_names[i].capitalize()
#                 # if arg_name == 'Self':
#                 #     i += 1
#                 #     continue

#                 msg += '{arg_name}: {value} | '.format(arg_name=arg_name, \
#  value=repr(arg))
#                 i += 1

#             # remove the last two letter "| "
#             msg = msg[: -2]

#             result= func(*args, **kwds)

#             out= '{method_name} \n'.format(method_name=method_name)

#             if msg:
#                 out += '>>> {msg} \n'.format(msg=msg)

#             if result:
#                 out += '>>> {return_value}'.format(return_value=repr(result))

#             out += '\n'

#             self.logger.log(out)

#             return result

#         return wrapper
