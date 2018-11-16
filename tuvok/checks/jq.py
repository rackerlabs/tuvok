from .base import BaseTuvokCheck, CheckResult

import os
import subprocess


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
        res = CheckResult()

        query = ['jq', '-rc', '{}'.format(self.jq_command)]
        text_hcl = self.readfile(f)
        test_json = self.hcl2json(text_hcl)

        proc = subprocess.Popen(
            args=query, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        (stdout, stderr) = proc.communicate(input=test_json)

        if 'Cannot iterate over null' in stderr:
            # nothing was found!
            return res

        if proc.returncode > 0:
            raise Exception(str(stderr))

        for entry in stdout.split():
            res.add_explanation(entry)
            res.set_success(False)

        return res
