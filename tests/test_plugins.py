from tuvok import cli
from helpers.wrap import Wrap


class TestPlugins(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_list_plugins(self, capsys):
        file = '--list-plugins'
        expected_checks = [
            {
                'check': 'FileLayoutCheck:FileLayoutCheck',
                'severity': 'ERROR',
                'description': 'Ensure variables and outputs are only in files of the same name',
            },
            {
                'check': 'NullCheck:NullCheck',
                'severity': 'WARNING',
                'description': 'None',
            },
            {
                'check': 'JqCheck:variable_description',
                'severity': 'ERROR',
                'description': 'Variables must contain description',
            },
            {
                'check': 'JqCheck:output_description',
                'severity': 'WARNING',
                'description': 'Outputs should contain description',
            },
        ]

        with Wrap(self, [file], [], expect_exit=False):
            out, err = capsys.readouterr()
            for plugin in ['BuiltinPlugin', 'NullPlugin']:
                assert plugin in out
            for check in expected_checks:
                assert "[Severity.{severity}] {check}\n\t{description}".format(**check) in out

    def test_default_null(self, caplog):
        file = 'tests/test_plugins/good'
        with Wrap(self, [file], [], expect_exit=False):
            assert ('[PASS] NullCheck:{}'.format(file)) in caplog.text

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
