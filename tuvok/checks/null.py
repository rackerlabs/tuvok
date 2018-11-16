from .base import BaseTuvokCheck, CheckResult


class NullCheck(BaseTuvokCheck):
    """
        The null check always passes.
    """

    def __init__(self):
        super().__init__()

    def check(self, path):
        return CheckResult(check=self)
