from tuvok import cli
from helpers.wrap import Wrap


class TestModule(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_warns_if_module_isnt_pinned(self, capsys):
        file = 'tests/test_module/module_git_missingref.tf'
        with Wrap(self, [file], expect_exit=True):
            err = capsys.readouterr().err
            assert ('Modules sourced from GitHub should be pinned in {}'.format(file)) in err

    def test_passes_if_module_has_ref(self, capsys):
        with Wrap(self, ['tests/test_module/module_git_hasref.tf'], expect_exit=False):
            err = capsys.readouterr().err
            assert err == ''

    def test_passes_if_module_not_git(self, capsys):
        with Wrap(self, ['tests/test_module/module_notgit.tf'], expect_exit=False):
            err = capsys.readouterr().err
            assert err == ''
