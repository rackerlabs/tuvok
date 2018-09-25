from tuvok import cli
from helpers.wrap import Wrap


class TestVariable(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_if_variable_has_no_type(self, capsys):
        file = 'tests/test_variable/variable_has_no_type.tf'

        with Wrap(self, [file]):
            err = capsys.readouterr().err
            assert ('Variables must contain type in {}:foo'.format(file)) in err

    def test_fails_if_variable_has_no_description(self, capsys):
        file = 'tests/test_variable/variable_has_no_description.tf'
        with Wrap(self, [file]):
            err = capsys.readouterr().err
            assert ('Variables must contain description in {}:foo'.format(file)) in err

    def test_warns_if_output_has_no_description(self, capsys):
        file = 'tests/test_variable/output_has_no_description.tf'
        with Wrap(self, [file], expect_exit=False):
            err = capsys.readouterr().err
            assert ('Outputs should contain description in {}:foo'.format(file)) in err

    def test_fails_prevent_override_severity(self, capsys):
        file = 'tests/test_variable/variable_has_type_and_description.tf'
        config = 'tests/test_variable/override.tuvok.json'
        with Wrap(self, [file], [config]):
            err = capsys.readouterr().err
            assert ('Cannot override check V100 in Configuration file {}'.format(config)) in err

    def test_fails_prevent_override_ignore(self, capsys):
        file = 'tests/test_variable/variable_has_type_and_description.tf'
        config = 'tests/test_variable/ignore.tuvok.json'
        with Wrap(self, [file], [config]):
            err = capsys.readouterr().err
            assert ('Cannot ignore check V100 in Configuration file {}'.format(config)) in err

    def test_passes_override_success(self, capsys):
        file = 'tests/test_variable/variable_has_type_and_description.tf'
        config = 'tests/test_variable/success.tuvok.json'
        with Wrap(self, [file], [config], expect_exit=False):
            out, err = capsys.readouterr()
            assert err == ''
            assert ('Rule O100 will be set to severity INFO by custom config {}'.format(config)) in out
            assert ('Rule V101 will be ignored by custom config {}'.format(config)) in out

    def test_passes_if_variable_has_type_and_description(self, capsys):
        with Wrap(self, ['tests/test_variable/variable_has_type_and_description.tf'], expect_exit=False):
            err = capsys.readouterr().err
            assert err == ''
