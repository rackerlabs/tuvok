from tuvok import cli
from helpers.wrap import Wrap


class TestProvider(object):
    def setup(self):
        self.main = cli.main

    def teardown(self):
        self.main = None

    def test_fails_if_region_not_in_provider_block(self, caplog):
        file = 'tests/test_provider/bad/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[FAIL] provider_has_region:Provider block should have region declared:aws:{}'.format(file)) in caplog.text

    def test_passes_if_region_in_provider_block(self, caplog):
        file = 'tests/test_provider/good/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[PASS] provider_has_region:Provider block should have region declared:{}'.format(file)) in caplog.text

    def test_fails_if_version_not_in_provider_block(self, caplog):
        file = 'tests/test_provider/bad/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[FAIL] provider_has_version:Provider block should have version pinned:aws:{}'.format(file)) in caplog.text

    def test_passes_if_version_in_provider_block(self, caplog):
        file = 'tests/test_provider/good/main.tf'

        with Wrap(self, [file], expect_exit=False):
            assert ('[PASS] provider_has_version:Provider block should have version pinned:{}'.format(file)) in caplog.text
