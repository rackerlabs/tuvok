# Copyright 2017 Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__title__ = 'tuvok'
__version__ = '0.1.0'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright Rackspace US, Inc. 2018'


import hcl2
import importlib
import inspect
import logging
import pkgutil

import tuvok.plugins


LOG = logging.getLogger()
JSON_CACHE = {}


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def not_abstract_class(o):
    return inspect.isclass(o) and not inspect.isabstract(o)


def hcl2json(f):
    if f not in JSON_CACHE:
        with(open(f, 'r')) as file:
            JSON_CACHE[f] = hcl2.load(file)
    return JSON_CACHE[f]


plugin_modules = [
    importlib.import_module(name)
    for (finder, name, ispkg)
    in iter_namespace(tuvok.plugins)
]
if(len(plugin_modules) > 0):
    LOG.info('Loaded plugin modules %s', plugin_modules)

tuvok_plugins = []
for module in plugin_modules:
    for clazz in inspect.getmembers(module, not_abstract_class):
        if clazz[1].__module__ is module.__name__:
            tuvok_plugins.append(clazz[1])
if(len(tuvok_plugins) > 0):
    LOG.info('Loaded plugins %s', tuvok_plugins)

tuvok_checks = []
for clazz in tuvok_plugins:
    for check in clazz().get_checks():
        tuvok_checks.append(check)
if(len(tuvok_checks) > 0):
    LOG.info('Loaded checks %s', tuvok_checks)
