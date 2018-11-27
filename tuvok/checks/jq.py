from .base import BaseTuvokCheck, CheckResult

import os
import subprocess


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

    def readfile(self, f):
        content = None
        with open(os.path.abspath(f), 'r') as content_file:
            content = content_file.read()

        return content

    def hcl2json(self, text):
        query = 'json2hcl --reverse'.split(' ')

        proc = subprocess.Popen(
            args=query, shell=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        (stdout, stderr) = proc.communicate(input=text)

        if proc.returncode > 0:
            raise Exception(str(stderr))

        return str(stdout)

    def check(self, f):
        query = 'json2hcl --reverse < {} | jq -rc {}'.format(f, translate_jq(self.jq_command))
        proc = subprocess.Popen(
            args=query, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        (stdout, stderr) = proc.communicate()

        if 'Cannot iterate over null' in stderr or stdout is '':
            # nothing was found! pass, no JQ matches
            return CheckResult(True, str(f), self)

        if proc.returncode > 0:
            raise Exception(str(stderr))

        results = []
        for entry in stdout.split():
            explanation = "{}:{}".format(entry, str(f))
            results.append(CheckResult(False, explanation, self))

        return results
