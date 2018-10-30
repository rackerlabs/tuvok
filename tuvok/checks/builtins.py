from .base import BaseTuvokCheck, Severity
from tuvok import hcl2json
import os


class FileLayoutCheck(BaseTuvokCheck):
    """
        1. Outputs, and only outputs, should only be in outputs.tf
        2. Variables, and only variables, should only be in variables.tf
    """

    def __init__(self):
        super().__init__(
            None,
            'Ensure variables and outputs are only in files of the same name',
            Severity.ERROR
        )

    def get_explanation(self):
        return '\n'.join(set(self.reasons))

    def check(self, path):
        parsed_json = hcl2json(path)
        self.reasons = []
        self.failed = False

        # output/input/variable have been put in the wrong file
        TYPES = set(['output', 'variable'])
        for prefix in TYPES:
            found_top_level_objs = parsed_json.get(prefix, [])
            actual_filename = os.path.basename(path)
            expected_filename = '{}s.tf'.format(prefix)

            if len(found_top_level_objs) > 0 and actual_filename != expected_filename:
                self.failed = True
                bad_names = [','.join(list(x.keys())) for x in found_top_level_objs]
                expl = '{}:{} was not found in a file named {}'.format(prefix, ','.join(bad_names), expected_filename)
                self.reasons.append(expl)

        return not self.failed
