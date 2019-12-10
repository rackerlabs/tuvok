import abc
from enum import Enum
import logging


LOG = logging.getLogger()


# using logging levels enables a nice trick to call LOG.log(level, ...)
class Severity(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class CheckResult(metaclass=abc.ABCMeta):

    def __init__(self, success=True, explanation=None, check=None):
        self.success = success
        self.explanation = explanation

        # values copied from check
        self.severity = check.get_severity()
        self.name = check.get_name()
        self.description = check.get_description()

    def get_explanation(self):
        return self.explanation

    def get_success(self):
        return self.success

    def get_severity(self):
        return self.severity

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class BaseTuvokCheck(metaclass=abc.ABCMeta):

    def __init__(self, name=None, description=None, severity=Severity.WARNING, prevent=False):
        self.name = name or self.__class__.__name__
        self.description = description
        self.prevent = prevent

        # in case someone passes a str
        self.severity = severity if isinstance(severity, Severity) else Severity[severity]

    def get_name(self):
        return self.name

    def get_type(self):
        return self.__class__.__name__

    def get_description(self):
        return self.description

    def get_severity(self):
        return self.severity

    @abc.abstractmethod
    def check(self, path):
        pass
