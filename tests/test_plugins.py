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
        file = 'tests/test_plugins/valid.tf'
        with Wrap(self, [file], [], expect_exit=False):
            assert ('NullCheck-None PASS in {}'.format(file)) in caplog.text

    def test_disable_null(self, caplog):
        file = 'tests/test_plugins/valid.tf'
        config = 'tests/test_plugins/notnull.tuvok.json'
        with Wrap(self, [file], [config], expect_exit=False):
            assert ('NullCheck-None PASS in {}'.format(file)) not in caplog.text
