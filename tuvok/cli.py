from tuvok import __version__
import argparse
import json
import logging
import os
import platform
import re
import subprocess
import sys

EXCLUSIONS = [r'.git', r'.terraform', r'.circleci', '__pycache__', r'*.egg-info']
LOG = logging.getLogger()


def load_config(file, merge=None):
    if not os.path.exists(file) and merge is None:
        raise Exception("Configuration file {} does not exist".format(file))
    elif not os.path.exists(file):
        LOG.warn("Custom configuration file {} does not exist".format(file))
        return merge

    with open(file) as f:
        config = json.load(f)
    if merge is None:
        if 'checks' not in config:
            err = "No checks defined in Configuration file {}".format(file)
            LOG.error(err)
            raise Exception(err)
        if 'ignore' not in config:
            config['ignore'] = []
        return config
    else:
        for (key, value) in config.get('checks', {}).items():
            if key in merge['checks']:
                if merge['checks'][key].get('prevent_override', False):
                    err = "Error: Cannot override check {} in Configuration file {}".format(key, file)
                    LOG.error(err)
                    sys.exit(2)
                LOG.info("Rule {} will be set to severity {} by custom config {}".format(key, value['severity'], file))
                merge['checks'][key]['severity'] = value['severity']
            else:
                LOG.info("Adding new config rule {}:{}-{}".format(key, value['severity'], value['description']))
                merge['checks'][key] = value
        for rule in config.get('ignore', []):
            if rule in merge['checks'] and merge['checks'][rule].get('prevent_override', False):
                    LOG.error("Cannot ignore check {} in Configuration file {}".format(rule, file))
                    sys.exit(2)
            if rule not in merge['ignore']:
                LOG.info("Rule {} will be ignored by custom config {}".format(rule, file))
                merge['ignore'].append(rule)
        return merge


def translate_jq(query):
    if platform.system() == 'Windows':
        return '\"{}\"'.format(query.replace('"', '\\\"'))
    return "'{}'".format(query)


def build_file_list(path):
    files = []
    configs = []

    LOG.debug('Loading specified files: %s', ",".join(path))
    for p in set(path):

        # if it doesn't exist, complain
        if not os.path.exists(p):
            err = "File does not exist: {}".format("] [".join(p))
            LOG.warn(err)
            raise Exception(err)

        # ensure any customizations are loaded from directories
        if os.path.isdir(p):
            custom_config = os.path.join(p, '.tuvok.json')
            if os.path.exists(custom_config):
                configs.append(custom_config)

            # get any files underneath
            for root, subdir_list, file_list in os.walk(p):
                if any(re.search(r'[\\/]{}([\\/].*)?$'.format(x), root) is not None for x in EXCLUSIONS):
                    continue

                files.extend([os.path.join(root, file) for file in file_list if re.search(r'.tf$', file)])
        else:
            files.extend([p])

    return (sorted(set(files)), configs)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v',
                        action='version',
                        version='version %s' % __version__)

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('-V', dest='loglevel', action='store_const',
                         const=logging.INFO,
                         help="Set log-level to INFO.")
    verbose.add_argument('-VV', dest='loglevel', action='store_const',
                         const=logging.DEBUG,
                         help="Set log-level to DEBUG.")
    parser.set_defaults(loglevel=logging.WARNING)

    parser.add_argument('--config', '-c', dest='config', default=[],
                        help='Custom configuration files to be loaded', action='append',
                        required=False)
    parser.add_argument('path', action='store', nargs='*', default=['.'],
                        help='files or directories to scan')

    args = parser.parse_args()

    # configure logging before doing anything else
    level = args.loglevel
    logging.basicConfig(level=int(os.environ.get('LOG_LEVEL', level)))
    LOG.setLevel(int(os.environ.get('LOG_LEVEL', level)))

    # find any files and configs we might be interested in
    (files_to_scan, extra_configs) = build_file_list(args.path)

    # load the builtin config
    configs_to_load = [os.path.join(os.path.dirname(__file__), '.tuvok.json')]
    # load any specified configs on commandline
    configs_to_load.extend(args.config)
    # load any found configs from the scan
    configs_to_load.extend(extra_configs)

    config = None
    for c in configs_to_load:
        LOG.debug('Loading configuration file %s', c)
        config = load_config(c, config)

    error_encountered = False
    LOG.info('Scanning %s files and executing checks', len(files_to_scan))
    for f in files_to_scan:
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
        LOG.info("Validation errors reported.")
        sys.exit(1)


if __name__ == "__main__":
    main()
