from tuvok import __version__
import argparse
import os
import platform
import re
import subprocess
import sys

EXCLUSIONS = ['\.git', '\.terraform', '\.circleci', '__pycache__', '.*\.egg-info']


def translate_jq(query):
    if platform.system() == 'Windows':
        return '\"{}\"'.format(query.replace('"', '\\\"'))
    return "'{}'".format(query)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v',
                        action='version',
                        version='version %s' % __version__)
    parser.add_argument('--file', '-f', dest='files',
                        help='File to be scanned', action='append',
                        required=False)
    parser.add_argument('--directory', '-d', dest='directory',
                        help='Directory to be scanned', default=os.getcwd(),
                        required=False)
    args = parser.parse_args()
    checks = {
        'error': [
            {
                'errorfmt': "Variables must contain description",
                'jq': '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].description == null) | ._variable_name',
            },
            {
                'errorfmt': "Variables must contain type",
                'jq': '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].type == null) | ._variable_name'
            }
        ],
        'warning': [
            {
                'errorfmt': "Outputs should contain description",
                'jq': '.output[] | {_output_name: . | keys[], _data: .[]} | select(._data[].description == null) | ._output_name'
            }
        ],
    }
    files = []
    if args.files:
        file_not_exist = [file for file in args.files if not os.path.exists(file)]
        if file_not_exist:
            raise Exception("Error:  File does not exist: [{}]".format("] [".join(file_not_exist)))
        files.extend(args.files)
    else:
        if not os.path.isdir(args.directory):
            raise Exception("Error: Directory {} does not exist".format(args.directory))
        for root, subdir_list, file_list in os.walk(args.directory):
            if any(re.search('[\\\\/]{}([\\\\/].*)?$'.format(x), root) is not None for x in EXCLUSIONS):
                continue
            files.extend([os.path.join(root, file) for file in file_list if re.search('\.tf$', file)])

    error_encountered = False
    for f in sorted(set(files)):
        for check_type, check_list in checks.items():
            for check in check_list:
                query = 'json2hcl --reverse < {} | jq -rc {}'.format(f, translate_jq(check['jq']))
                (stdout, stderr) = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, universal_newlines=True).communicate()
                if 'Cannot iterate over null' in stderr:
                    continue
                for entry in stdout.split():
                    if 'error' in check_type:
                            error_encountered = True
                    print("[{}] {}-{}: {}".format(f, check_type.upper(), check['errorfmt'], entry), file=sys.stderr)

    if error_encountered:
        sys.exit("Validation errors reported.")


if __name__ == "__main__":
    main()
