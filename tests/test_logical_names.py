from tuvok import cli
from helpers.wrap import Wrap


class TestOutput(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_if_variable_not_using_snake_case(self, caplog):
        file = 'tests/test_logical_names/bad/variables.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:variable:FooBar:{}'.format(file)) in caplog.text
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:variable:foo-bar:{}'.format(file)) in caplog.text

    def test_passes_if_variable_using_snake_case(self, caplog):
        file = 'tests/test_logical_names/good/variables.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[PASS] name_snake_case:Logical names should use snake_case:{}'.format(file)) in caplog.text

    def test_fails_if_output_not_using_snake_case(self, caplog):
        file = 'tests/test_logical_names/bad/outputs.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:output:FooBar:{}'.format(file)) in caplog.text
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:output:foo-bar:{}'.format(file)) in caplog.text

    def test_passes_if_output_uses_snake_case(self, caplog, capsys):
        file = 'tests/test_logical_names/good/outputs.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[PASS] name_snake_case:Logical names should use snake_case:{}'.format(file)) in caplog.text
            err = capsys.readouterr().err
            assert err == ''

    def test_fails_if_resource_not_using_snake_case(self, caplog):
        file = 'tests/test_logical_names/bad/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[FAIL] resource_name_snake_case:Logical names should use snake_case:resource:aws_iam_role:FooBar:{}'.format(file)) in caplog.text
            assert ('[FAIL] resource_name_snake_case:Logical names should use snake_case:resource:aws_iam_role:foo-bar:{}'.format(file)) in caplog.text
            assert ('[FAIL] resource_name_snake_case:Logical names should use snake_case:resource:aws_iam_policy:FooBaz:{}'.format(file)) in caplog.text
            assert ('[FAIL] resource_name_snake_case:Logical names should use snake_case:resource:aws_iam_role_policy_attachment:foo-baz:{}'.format(file)) in caplog.text
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:module:FooBin:{}'.format(file)) in caplog.text
            assert ('[FAIL] name_snake_case:Logical names should use snake_case:module:foo-bin:{}'.format(file)) in caplog.text

    def test_passes_if_resource_using_snake_case(self, caplog, capsys):
        file = 'tests/test_logical_names/good/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[PASS] name_snake_case:Logical names should use snake_case:{}'.format(file)) in caplog.text
            assert ('[PASS] resource_name_snake_case:Logical names should use snake_case:{}'.format(file)) in caplog.text
            err = capsys.readouterr().err
            assert err == ''
