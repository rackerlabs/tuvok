from .base import BaseTuvokCheck

import os
import platform
import subprocess


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
        return ",".join(self.explanation)

    def check(self, f):
        query = 'json2hcl --reverse < {} | jq -rc {}'.format(os.path.abspath(f), translate_jq(self.jq_command))
        (stdout, stderr) = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, universal_newlines=True).communicate()

        encountered_problem = False
        self.explanation = []

        # nothing was found!
        if 'Cannot iterate over null' in stderr:
            return True

        for entry in stdout.split():
            self.explanation.append(entry)
            encountered_problem = True

        return not encountered_problem
