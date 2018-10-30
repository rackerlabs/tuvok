from tuvok import cli
from helpers.wrap import Wrap


class TestVariable(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_if_variable_has_no_type_or_no_description(self, caplog):
        file = 'tests/test_variable/bad/variables.tf'

        with Wrap(self, [file]):
            assert ('Variables must contain description FAIL in {}:foo'.format(file)) in caplog.text
            assert ('Variables must contain type FAIL in {}:bar'.format(file)) in caplog.text

    def test_passes_if_variable_has_type_and_description(self, caplog):
        file = 'tests/test_variable/good/variables.tf'
        with Wrap(self, [file], expect_exit=False):
            assert ('Variables must contain description PASS in {}:'.format(file)) in caplog.text
            assert ('Variables must contain type PASS in {}:'.format(file)) in caplog.text
