import logging
import datetime
import functools
import inspect



class Logger(object):
    _log_level = {
        'log': 0,
        'debug': 1,
        'warning': 2,
        'error': 3,
        'critical': 4,
    }

    def __init__(self, module):
        self.module = module
        self._logger = logging.getLogger(module)

    def log(self, msg):
        from core.utility.configuration import Configuration
        if Configuration.get().log_level <= self._log_level['log']:
            return

        self._format_message('', msg)
        if Configuration.get().enable_logging:
            self._logger.debug(msg)

        if Configuration.get().enable_debugging:
            print(msg)

    def info(self, msg):
        from core.utility.configuration import Configuration
        if Configuration.get().log_level <= self._log_level['info']:
            return

        if Configuration.get().log_level <= 1:
            return

        self._format_message('Info', msg)
        if Configuration.get().enable_logging:
            self._logger.info(msg)

        if Configuration.get().enable_debugging:
            print(msg)

    def warning(self, msg):
        from core.utility.configuration import Configuration
        if Configuration.get().log_level <= self._log_level['warning']:
            return

        if Configuration.get().log_level <= 2:
            return

        self._format_message('Warning', msg)
        if Configuration.get().enable_logging:
            self._logger.warning(msg)

        if Configuration.get().enable_debugging:
            print(msg)

    def error(self, msg):
        from core.utility.configuration import Configuration
        if Configuration.get().log_level <= self._log_level['error']:
            return

        if Configuration.get().log_level <= 3:
            return

        self._format_message('ERROR', msg)
        if Configuration.get().enable_logging:
            self._logger.error(msg)

        if Configuration.get().enable_debugging:
            print(msg)

    def critical(self, msg):
        from core.utility.configuration import Configuration
        if Configuration.get().log_level <= self._log_level['critical']:
            return

        self._format_message('CRITICAL', msg)
        if Configuration.get().enable_logging:
            self._logger.critical(msg)

        if Configuration.get().enable_debugging:
            print(msg)

    def _format_message(self, level, msg):
        if level:
            return '{level} - {time} - {module} - {msg}'.format(level=level, time=datetime.datetime.now(),
                                                                module=self.module, msg=msg)

        return '{time} - {module} - {msg}'.format(time=datetime.datetime.now(), module=self.module, msg=msg)


class MethodBoundaryLogger(object):
    """
    Log when enter and exist method use default logger or the logger provided
    """

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        if not self.logger:
            self.logger = Logger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):

            # start logging
            method_name = func.__name__.replace('_', ' ')
            msg = ''
            i = 0

            # get argument names
            arg_names = inspect.getfullargspec(func)[0]

            # build arguments
            for arg in args:
                arg_name = arg_names[i].capitalize()

                msg += '{arg_name}: {value} | '.format(arg_name=arg_name, value=repr(arg))
                i += 1

            # remove the last letter "|"
            msg = msg[:-1]

            self.logger.log('{method_name} >>> {msg}'.format(method_name=method_name, msg=msg))

            result = func(*args, **kwds)

            return result

        return wrapper

# @MethodBoundaryLogger()
# def test(name, age):
#     pass
#
# test('tommy',1)
