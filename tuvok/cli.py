from tuvok import __version__
import argparse
import json
import os
import platform
import re
import subprocess
import sys

EXCLUSIONS = [r'.git', r'.terraform', r'.circleci', '__pycache__', r'*.egg-info']


def load_config(file, merge=None):
    if not os.path.exists(file) and merge is None:
        raise Exception("Error:  Configuration file {} does not exist".format(file))
    elif not os.path.exists(file):
        print("Warning:  Custom configuration file {} does not exist".format(file))
        return merge

    with open(file) as f:
        config = json.load(f)
    if merge is None:
        if 'checks' not in config:
            raise Exception("Error:  No checks defined in Configuration file {}".format(file))
        if 'ignore' not in config:
            config['ignore'] = []
        return config
    else:
        for (key, value) in config.get('checks', {}).items():
            if key in merge['checks']:
                if merge['checks'][key].get('prevent_override', False):
                    print("Error: Cannot override check {} in Configuration file {}".format(key, file), file=sys.stderr)
                    sys.exit('Exiting...')
                print("Rule {} will be set to severity {} by custom config {}".format(key, value['severity'], file))
                merge['checks'][key]['severity'] = value['severity']
            else:
                print("Adding new config rule {}:{}-{}".format(key, value['severity'], value['description']))
                merge['checks'][key] = value
        for rule in config.get('ignore', []):
            if rule in merge['checks'] and merge['checks'][rule].get('prevent_override', False):
                    print("Error: Cannot ignore check {} in Configuration file {}".format(rule, file), file=sys.stderr)
                    sys.exit('Exiting...')
            if rule not in merge['ignore']:
                print("Rule {} will be ignored by custom config {}".format(rule, file))
                merge['ignore'].append(rule)
        return merge


def translate_jq(query):
    if platform.system() == 'Windows':
        return '\"{}\"'.format(query.replace('"', '\\\"'))
    return "'{}'".format(query)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v',
                        action='version',
                        version='version %s' % __version__)
    parser.add_argument('--config', '-c', dest='config', default=[],
                        help='Custom configuration files to be loaded', action='append',
                        required=False)
    parser.add_argument('path', action='store', nargs='*', default=['.'],
                        help='files or directories to scan')

    args = parser.parse_args()
    print(args.path)

    config = load_config(os.path.join(os.path.dirname(__file__), '.tuvok.json'))

    files = []  # awkward double list comprehension due to argparse
    for p in set(args.path):

        # if it doesn't exist, complain
        if not os.path.exists(p):
            raise Exception("Error:  File does not exist: {}".format("] [".join(p)))

        # ensure any customizations are loaded from directories
        if os.path.isdir(p):
            custom_config = os.path.join(p, '.tuvok.json')
            if os.path.exists(custom_config):
                args.config.append(custom_config)

            # get any files underneath
            for root, subdir_list, file_list in os.walk(p):
                if any(re.search(r'[\\/]{}([\\/].*)?$'.format(x), root) is not None for x in EXCLUSIONS):
                    continue

                files.extend([os.path.join(root, file) for file in file_list if re.search(r'.tf$', file)])
        else:
            files.extend([p])

    for c in args.config:
        config = load_config(c, config)

    error_encountered = False
    for f in sorted(set(files)):
        for check, check_details in config['checks'].items():
            if check in config['ignore']:
                continue
            if check_details['type'] == 'jq':
                query = 'json2hcl --reverse < {} | jq -rc {}'.format(f, translate_jq(check_details['jq']))
                (stdout, stderr) = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, universal_newlines=True).communicate()
                if 'Cannot iterate over null' in stderr:
                    continue
                for entry in stdout.split():
                    if 'ERROR' in check_details['severity'].upper():
                            error_encountered = True
                    print("[{}] {}-{} in {}:{}".format(check_details['severity'].upper(), check,
                                                       check_details['description'], f, entry), file=sys.stderr)

    if error_encountered:
        sys.exit("Validation errors reported.")


if __name__ == "__main__":
    main()
