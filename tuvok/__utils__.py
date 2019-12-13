import  hcl2
import inspect
import pkgutil

JSON_CACHE = {}

def hcl2json(f):
    if f not in JSON_CACHE:
        with(open(f, 'r')) as file:
            JSON_CACHE[f] = hcl2.load(file)
    return JSON_CACHE[f]

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def not_abstract_class(o):
    return inspect.isclass(o) and not inspect.isabstract(o)
