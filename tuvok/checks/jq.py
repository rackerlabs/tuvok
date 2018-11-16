from .base import BaseTuvokCheck

import os
import platform
import subprocess
import shlex


def translate_jq(query):
    if platform.system() == 'Windows':
        return '\"{}\"'.format(query.replace('"', '\\\"'))
    return "'{}'".format(query)


class JqCheck(BaseTuvokCheck):

    jq_command = None
    explanation = None

    def __init__(self, name, description, severity, command, prevent):
        super().__init__(name, description, severity, prevent)
        self.jq_command = command

    def get_explanation(self):
        if self.explanation:
            return ",".join(self.explanation)
        return None

    # @lru_cache(maxsize=32)
    def readfile(self, f):
        content = None
        with open(os.path.abspath(f), 'r') as content_file:
            content = content_file.read()

        return content

    # @lru_cache(maxsize=32)
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
        query = 'jq -rc {}'.format(translate_jq(self.jq_command))
        text_hcl = self.readfile(f)
        test_json = self.hcl2json(text_hcl)

        proc = subprocess.Popen(
            args=query, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        (stdout, stderr) = proc.communicate(input=test_json)

        if 'Cannot iterate over null' in stderr:
            # nothing was found!
            return True
        if proc.returncode > 0:
            # self.explanation.append(str(stderr))
            raise Exception(str(stderr))

        encountered_problem = False
        self.explanation = []

        for entry in stdout.split():
            self.explanation.append(entry)
            encountered_problem = True

        return not encountered_problem
