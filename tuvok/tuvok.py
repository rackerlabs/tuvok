from tuvok.plugins import BaseTuvokPlugin
from tuvok.checks.builtins import FileLayoutCheck


class TuvokPlugin(BaseTuvokPlugin):
    """
        These are the checks that ship with Tuvok by default.
    """

    def get_checks(self):
        return [FileLayoutCheck()]
