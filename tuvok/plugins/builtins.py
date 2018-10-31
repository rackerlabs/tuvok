from tuvok.plugins import BaseTuvokPlugin
from tuvok.checks.builtins import FileLayoutCheck


class BuiltinPlugin(BaseTuvokPlugin):
    """
        The null plugin always passes.
    """

    def get_checks(self):
        return [FileLayoutCheck()]
