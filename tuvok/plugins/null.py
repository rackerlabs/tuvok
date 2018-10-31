from tuvok.plugins import BaseTuvokPlugin
from tuvok.checks.null import NullCheck


class NullPlugin(BaseTuvokPlugin):
    """
        The null plugin always passes.
    """

    def get_checks(self):
        return [NullCheck()]
