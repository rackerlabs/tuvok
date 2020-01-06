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

import importlib
import logging
import inspect

import tuvok.plugins

from .__utils__ import hcl2json, iter_namespace, not_abstract_class
from .__version__ import __version__, __title__, __copyright__, __license__

LOG = logging.getLogger()

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
