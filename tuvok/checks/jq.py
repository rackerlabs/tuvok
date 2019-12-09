import json
import subprocess

from tuvok import hcl2json
from tuvok.checks.base import BaseTuvokCheck, CheckResult


def translate_jq(query):
    import platform
    if platform.system() == 'Windows':
        return '\"{}\"'.format(query.replace('"', '\\\"'))
    return "'{}'".format(query)


class JqCheck(BaseTuvokCheck):

    jq_command = None

    def __init__(self, name, description, severity, command, prevent):
        super().__init__(name, description, severity, prevent)
        self.jq_command = command

    def check(self, f):
        parsed_json = json.dumps(hcl2json(f))
        query = "jq -r -c {}".format(translate_jq(self.jq_command))
        proc = subprocess.Popen(
            args=query, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        (stdout, stderr) = proc.communicate(input=parsed_json)

        if 'Cannot iterate over null' in stderr or stdout == '':
            # nothing was found! pass, no JQ matches
            return CheckResult(True, str(f), self)

        if proc.returncode > 0:
            raise Exception(str(stderr))

        results = []
        for entry in stdout.split():
            explanation = "{}:{}".format(entry, str(f))
            results.append(CheckResult(False, explanation, self))

        return results
