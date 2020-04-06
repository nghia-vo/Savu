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
.. module:: nx_xrd_loader_test
   :platform: Unix
   :synopsis: testing the nx_xrd loader

.. moduleauthor:: Aaron Parsons <scientificsoftware@diamond.ac.uk>

"""
import unittest
from savu.test import test_utils as tu
from savu.test.travis.framework_tests.plugin_runner_test import \
    run_protected_plugin_runner

class NxTomoLoaderTest(unittest.TestCase):
    global data_file, experiment
    data_file = '24737.nxs'
    experiment = None

    def test_nx_tomo(self):
        process_list = 'loaders/basic_tomo_process.nxs'
        options = tu.initialise_options(data_file, experiment, process_list)
        run_protected_plugin_runner(options)
        tu.cleanup(options)

#    def test_separate_flats(self):
#        data_file = tu.get_test_data_path('24737.nxs')
#        process_file = tu.get_test_process_path(
#                'basic_tomo_process_separate_flats.nxs')
#        run_protected_plugin_runner(tu.set_options(data_file,
#                                                   process_file=process_file))

#    def test_separate_darks(self):
#        data_file = tu.get_test_data_path('24737.nxs')
#        process_file = tu.get_test_process_path(
#                'basic_tomo_process_separate_darks.nxs')
#        run_protected_plugin_runner(tu.set_options(data_file,
#                                                   process_file=process_file))


if __name__ == "__main__":
    unittest.main()
