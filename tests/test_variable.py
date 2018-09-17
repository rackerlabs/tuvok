from tuvok import cli
from helpers.wrap import Wrap

class TestVariable(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_if_variable_has_no_type(self, capsys):
        with Wrap(self, ['tests/test_variable/variable_has_no_type.tf']):
            err = capsys.readouterr().err
            assert ('[tests/test_variable/variable_has_no_type.tf] '
                    'ERROR-Variables must contain type: foo') in err
