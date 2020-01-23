import hcl2
import inspect
import logging
import pkgutil
import sys

from lark.exceptions import UnexpectedToken

JSON_CACHE = {}
LOG = logging.getLogger().getChild('tuvok')

def hcl2json(f):
    if f not in JSON_CACHE:
        try:
            with(open(f, 'r')) as file:
                JSON_CACHE[f] = hcl2.load(file)
        except UnexpectedToken as e:
            LOG.error("Error parsing {}: {}".format(f, e))
            sys.exit(1)
    return JSON_CACHE[f]

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def not_abstract_class(o):
    return inspect.isclass(o) and not inspect.isabstract(o)
