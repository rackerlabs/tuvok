from tuvok import __version__
import argparse
import os
import platform


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
    args = parser.parse_args()
    checks = [
        {
            'errorfmt': "Error: Variables must contain description",
            'jq': '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].description == null) | ._variable_name',
        },
        {
            'errorfmt': "Error: Variables must contain type",
            'jq': '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].type == null) | ._variable_name'
        }
    ]
    if args.files:
        for f in args.files:
            for check in checks:
                output = os.popen('json2hcl --reverse < {} | jq -rc {}'.format(f, translate_jq(check['jq']))).read()
                for entry in output.split():
                    print("[{}] {}: {}".format(f, check['errorfmt'], entry))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
