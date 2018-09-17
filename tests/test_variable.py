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
            assert ('[' + file + '] ERROR-Variables must contain type: foo') in err

    def test_fails_if_variable_has_no_description(self, capsys):
        file = 'tests/test_variable/variable_has_no_description.tf'
        with Wrap(self, [file]):
            err = capsys.readouterr().err
            assert ('[' + file + '] ERROR-Variables must contain description: foo') in err

    def test_passes_if_variable_has_type_and_description(self, capsys):
        with Wrap(self, ['tests/test_variable/variable_has_type_and_description.tf'], False):
            err = capsys.readouterr().err
            assert err == ''
