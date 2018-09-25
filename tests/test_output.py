from tuvok import cli
from helpers.wrap import Wrap


class TestOutput(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_warns_if_output_has_no_description(self, capsys):
        file = 'tests/test_output/output_has_no_description.tf'
        with Wrap(self, [file], expect_exit=False):
            err = capsys.readouterr().err
            assert ('Outputs should contain description in {}:foo'.format(file)) in err

    def test_passes_if_output_has_description(self, capsys):
        with Wrap(self, ['tests/test_output/output_has_description.tf'], expect_exit=False):
            err = capsys.readouterr().err
            assert err == ''
