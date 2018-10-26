import sys
from unittest.mock import patch
import pytest


class Wrap():
    """
    Python ContextManager to serve as a wrapper around Tuvok's main() execution until that's been
    broken up into more granular classes and method calls. This handles the repeated steps of
    injecting the file parameter(s) and ensuring the script would exit after failing.
    """
    def __init__(self, test, files, configs=[], expect_exit=True):
        self.expect_exit = expect_exit
        self.test = test
        self.files = files
        self.configs = configs

    def __enter__(self):
        args = ['$/tuvok/cli.py']
        for file in self.files:
            args.append(file)

        for config in self.configs:
            args.extend(['-c', config])

        with patch.object(sys, 'argv', args):
            if self.expect_exit:
                with pytest.raises(SystemExit):
                    self.test.main()
            else:
                self.test.main()

    def __exit__(self, type, value, traceback):
        self.files = ""
        self.test = None
