from tuvok import cli
from helpers.wrap import Wrap


class TestOutput(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_warns_if_output_has_no_description(self, caplog):
        file = 'tests/test_output/bad/outputs.tf'
        with Wrap(self, [file], expect_exit=False):
            assert ('Outputs should contain description FAIL in {}:foo'.format(file)) in caplog.text

    def test_passes_if_output_has_description(self, capsys):
        with Wrap(self, ['tests/test_output/good/outputs.tf'], expect_exit=False):
            err = capsys.readouterr().err
            assert err == ''
