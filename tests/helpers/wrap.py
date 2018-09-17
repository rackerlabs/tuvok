import sys
from unittest.mock import patch
import pytest

"""
Python ContextManager to serve as a wrapper around Tuvok's main() execution until that's been
broken up into more granular classes and method calls. This handles the repeated steps of
injecting the file parameter(s) and ensuring the script would exit after failing.
"""
class Wrap():
    def __init__(self, test, files):
        self.test = test
        self.files = files

    def __enter__(self):
        args = ['$/tuvok/cli.py']
        for file in self.files:
            args.extend(['-f', file])

        with patch.object(sys, 'argv', args):
            with pytest.raises(SystemExit) as s:
                self.test.main()

    def __exit__(self, type, value, traceback):
        self.files = ""
        self.test = None
