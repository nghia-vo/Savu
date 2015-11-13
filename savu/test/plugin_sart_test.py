# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
.. module:: plugins_test
   :platform: Unix
   :synopsis: unittest test classes for plugins

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""

import unittest

import savu.test.test_utils as tu
from savu.test.plugin_runner_test import \
    run_protected_plugin_runner_no_process_list


class SimpleReconTest(unittest.TestCase):

    def test_simple_recon(self):
        options = tu.set_experiment('tomo')
        plugin = 'savu.plugins.reconstructions.simple_recon'
        run_protected_plugin_runner_no_process_list(options, plugin)

#
#class ScikitimageSartTest(unittest.TestCase):
#
#    def test_scikit_sart(self):
#        options = tu.set_experiment('tomo')
#        plugin = 'savu.plugins.reconstructions.scikitimage_sart'
#        loader_dict = {'starts': [0, 0, 0],
#                       'stops': [-1, -1, -1],
#                       'steps': [20, 20, 20]}
#        data_dict = {'in_datasets': ['tomo'], 'out_datasets': ['test']}
#        saver_dict = {}
#        all_dicts = [loader_dict, data_dict, saver_dict]
#        run_protected_plugin_runner_no_process_list(options, plugin, all_dicts)

if __name__ == "__main__":
    unittest.main()
