from tuvok import cli
from helpers.wrap import Wrap


class TestConfig(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_prevent_override_severity(self, capsys):
        file = 'tests/test_config/valid.tf'
        config = 'tests/test_config/override.tuvok.json'
        with Wrap(self, [file], [config]):
            err = capsys.readouterr().err
            assert ('Cannot override check TUVOK100 in Configuration file {}'.format(config)) in err

    def test_fails_prevent_override_ignore(self, capsys):
        file = 'tests/test_config/valid.tf'
        config = 'tests/test_config/ignore.tuvok.json'
        with Wrap(self, [file], [config]):
            err = capsys.readouterr().err
            assert ('Cannot ignore check TUVOK100 in Configuration file {}'.format(config)) in err

    def test_passes_override_success(self, capsys):
        file = 'tests/test_config/valid.tf'
        config = 'tests/test_config/success.tuvok.json'
        with Wrap(self, [file], [config], expect_exit=False):
            out, err = capsys.readouterr()
            assert err == ''
            assert ('Rule TUVOK103 will be set to severity INFO by custom config {}'.format(config)) in out
            assert ('Rule TUVOK101 will be ignored by custom config {}'.format(config)) in out
