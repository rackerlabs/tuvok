from tuvok import __version__
import argparse
import json
import os


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v',
                        action='version',
                        version='version %s' % __version__)
    # parser.add_argument('--hi', '-w', dest='hi',
    #                     help='Hi Everybody!!!',
    #                     required=False)
    parser.add_argument('--file', '-f', dest='files',
                        help='File to be scanned', action='append',
                        required=False)
    args = parser.parse_args()
    checks = [
        "'.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].description == null) | ._variable_name'",
        "'.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].type == null) | ._variable_name'"
    ]
    if args.files:
        for f in args.files:

            print(f)
            for check in checks:
                output = os.popen('json2hcl --reverse < {} | jq -rc {}'.format(f, check)).read()
                # output = os_popen('echo {} | jq ')
                print(output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
