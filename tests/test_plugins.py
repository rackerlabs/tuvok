from tuvok import cli
from helpers.wrap import Wrap


class TestPlugins(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_list_plugins(self, caplog):
        file = '--list-plugins'
        with Wrap(self, [file], [], expect_exit=False):
            assert 'tuvok.plugins.null.NullPlugin' in caplog.text

    def test_default_null(self, caplog):
        file = 'tests/test_plugins/good'
        with Wrap(self, [file], [], expect_exit=False):
            assert ('NullCheck-None PASS in {}'.format(file)) in caplog.text

    def test_disable_null(self, caplog):
        file = 'tests/test_plugins/good'
        config = 'tests/test_plugins/notnull.tuvok.json'
        with Wrap(self, [file], [config], expect_exit=False):
            assert ('NullCheck-None PASS in {}'.format(file)) not in caplog.text

    def test_good_file_layout(self, caplog):
        file = 'tests/test_plugins/good'
        with Wrap(self, [file], [], expect_exit=False):
            assert 'FAIL' not in caplog.text
            assert 'variable:foo was not found in a file named variables.tf' not in caplog.text
            assert 'output:foo was not found in a file named outputs.tf' not in caplog.text

    def test_bad_file_layout(self, caplog):
        file = 'tests/test_plugins/bad'
        config = 'tests/test_plugins/notnull.tuvok.json'
        with Wrap(self, [file], [config], expect_exit=True):
            assert 'FAIL' in caplog.text
            assert 'variable:foo was not found in a file named variables.tf' in caplog.text
            assert 'output:foo was not found in a file named outputs.tf' in caplog.text
