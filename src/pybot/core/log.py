# -*- coding: utf-8 -*-

""" A couple of convenience settings and functions for using the logging facility
in a homogeneous way across applications."""

import copy

# surface logging module public definitions (do not remove although PyLint saying it is not used)
# noinspection PyUnresolvedReferences
from logging import INFO, WARN, WARNING, ERROR, DEBUG, getLogger, NullHandler
import logging.config

import re
import os
import datetime

try:
    import colorlog

    def ColoredFormatter(
            fmt="%(log_color)s[%(levelname).1s] %(name)-15s > %(message)s",
            datefmt="%m-%d %H:%M:%S"
    ):
        return colorlog.ColoredFormatter(
            fmt=fmt,
            datefmt=datefmt,
            log_colors={
                    'DEBUG':    'reset',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'bold_red',
            }
        )

except ImportError:
    colorlog = None


_default_configuration = {
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s.%(msecs).3d [%(levelname).1s] %(name)s (%(filename)s:%(lineno)d) %(message)s',
            'datefmt': '%H:%M:%S'
        },
        'brief': {
            'format': '[%(levelname).1s] %(name)s > %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'pybot.core.log.ColoredFormatter' if colorlog else 'brief',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'filename': '',
            'maxBytes': 1024*50,
            'backupCount': 3
        }
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG'
    }
}


def deep_update(d, u):
    """ Recursively update a dictionary, walking down its nested levels.
    :param dict d: dictionary to be updated
    :param dict u: dictionary containing the updates
    """
    for k, v in u.iteritems():
        if k in d and isinstance(v, dict):
            deep_update(d[k], v)
        else:
            d[k] = v


def get_logging_configuration(override=None):
    """ Returns a full logging configuration, based on the default one
    overridden with the passed one.
    :param dict override: a dictionary containing the overridden settings
    :return: the complete configuration
    :rtype: dict
    """
    cfg = copy.deepcopy(_default_configuration)
    if override:
        deep_update(cfg, override)
    return cfg


def abbrev(fqn):
    """ Given a fully qualified module name, returns an abbreviated form by replacing
    the parent full names by their initial.

    Ex: pybot.dynamixel.joints -> p.d.joints
    """
    parts = fqn.split('.')
    return '.'.join([s[0] for s in parts[:-1]] + [parts[-1]])


_regex = re.compile(r'\033.*?m')


def uncolorify(s):
    return _regex.sub('', s)


def log_file_path(log_name):
    """ Returns the full path of the log file, depending on the currently running used.

    In case the log_name parameter includes the ".log" extension already, it ia used as is.
    Otherwise the extension will be appended.

    :param str log_name: the log name (i.e. its filename without the extension)
    :return: the log file full path
    :rtype: str
    """
    log_dir = "/var/log" if os.getuid() == 0 else os.path.expanduser("~/")
    if not log_name.endswith('.log'):
        log_name += '.log'
    return os.path.join(log_dir, log_name)


def setup_logging(log_name):
    logging.config.dictConfig(get_logging_configuration({
        'handlers': {
            'file': {
                'filename': log_file_path(log_name)
            }
        }
    }))


class LogMixin(object):
    """ Adds logging function to a class.

    Bundles more common methods from logging standard module and takes care of configuration
    so that all classes using this Mixin will use an homogeneous logging without having the
    burden of low level stuff.

    The ``logger`` attribute gives access to the embedded logger instance for advanced usages
    if needed.
    """
    def __init__(self, parent=None, name=None, width=40):
        name = name or self.__class__.__name__
        self._log_width = width

        self.logger = parent.getChild(name) if parent else getLogger(name)

        self.log_info = self.logger.info
        self.log_warning = self.logger.warning
        self.log_error = self.logger.error
        self.log_critical = self.logger.critical
        self.log_exception = self.logger.exception
        self.log_debug = self.logger.debug
        self.log_setLevel = self.logger.setLevel
        self.log_getEffectiveLevel = self.logger.getEffectiveLevel

    def log_banner(self, text):
        separator = '-' * self._log_width
        self.logger.info(separator)
        if isinstance(text, basestring):
            if '\n' in text:
                lines = text.splitlines()
            else:
                lines = [text]
        else:
            lines = text
        for line in lines:
            self.logger.info(line)
        self.logger.info(separator)

    def log_error_banner(self, error, unexpected=False):
        title = 'unexpected error' if unexpected else 'abnormal termination '
        self.logger.fatal((' ' + title + ' ').center(self._log_width, '!'))
        self.logger.fatal(error)
        self.logger.fatal('!' * self._log_width)

    def log_starting_banner(self, version=None):
        text = ['starting on %s' % datetime.datetime.now()]
        if version:
            text.append('version ' + version)
        self.log_banner(text)
