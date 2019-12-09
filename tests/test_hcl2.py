from tuvok import cli
from helpers.wrap import Wrap


class TestHcl2(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_good_hcl2(self, caplog):
        file = 'tests/test_hcl2/good'
        with Wrap(self, [file], [], expect_exit=False):
            assert 'FAIL' not in caplog.text
            assert 'variable:foo was not found in a file named variables.tf' not in caplog.text
            assert 'output:foo was not found in a file named outputs.tf' not in caplog.text
            assert 'github_module_ref:Modules sourced from GitHub should be pinned:some_module:' not in caplog.text

    def test_bad_hcl2(self, caplog):
        file = 'tests/test_hcl2/bad'
        with Wrap(self, [file], [], expect_exit=True):
            assert 'FAIL' in caplog.text
            assert 'variable:foo was not found in a file named variables.tf' in caplog.text
            assert 'output:foo was not found in a file named outputs.tf' in caplog.text
            assert 'github_module_ref:Modules sourced from GitHub should be pinned:some_module:' in caplog.text
