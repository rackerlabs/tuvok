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

    def __init__(self, success=True, explanation=[], check=None):
        self.explanation = []
        self.success = success
        self.check = check

    def add_explanation(self, expl):
        self.explanation.append(expl)

    def get_explanation(self):
        return None if len(self.explanation) == 0 else ','.join(self.explanation)

    def get_success(self):
        return self.success

    def set_success(self, success):
        self.success = success

    def get_severity(self):
        return self.check.get_severity()

    def get_name(self):
        return self.check.get_name()

    def get_description(self):
        return self.check.get_description()


class BaseTuvokCheck(metaclass=abc.ABCMeta):

    def __init__(self, name=None, description=None, severity=Severity.WARNING, prevent=False):
        self.name = name or self.__class__.__name__
        self.description = description
        self.prevent = prevent

        # in case someone passes a str
        self.severity = severity if isinstance(severity, Severity) else Severity[severity]

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_severity(self):
        return self.severity

    def safe_check(self, path):
        try:
            return self.check(path)
        except Exception as e:
            LOG.log(self.severity.value, e)
            return CheckResult(success=False, explanation=[str(e)], check=self)

    @abc.abstractmethod
    def check(self, path):
        pass
