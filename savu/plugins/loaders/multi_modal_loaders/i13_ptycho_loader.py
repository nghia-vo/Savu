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
.. module:: nxstxm_loader
   :platform: Unix
   :synopsis: A class for loading nxstxm data

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""

from savu.plugins.loaders.base_multi_modal_loader import BaseMultiModalLoader
import numpy as np
from savu.plugins.utils import register_plugin
import logging

@register_plugin
class I13PtychoLoader(BaseMultiModalLoader):
    """
    A class to load tomography data from an NXstxm file
    """

    def __init__(self, name='NxptychoLoader'):
        super(I13PtychoLoader, self).__init__(name)

    def setup(self):
        """
         Define the input nexus file

        :param path: The full path of the NeXus file to load.
        :type path: str
        """

        data_str = '/instrument/detector/data'
        data_obj, stxm_entry = self.multi_modal_setup('NXptycho', data_str)
        mono_energy = data_obj.backing_file[
            stxm_entry.name + '/instrument/monochromator/energy']
        self.exp.meta_data.set_meta_data("mono_energy", mono_energy)
        
        labels = []
        ### set the rotation
        rotation_angle = \
            data_obj.backing_file[stxm_entry.name + '/data/theta'].value
        if rotation_angle.ndim > 1:
            rotation_angle = rotation_angle[:, 0]
        # axis label
        labels.append('rotation_angle.degrees')
        
        data_obj.meta_data.set_meta_data('rotation_angle', rotation_angle)
        
        ### set the x
        x = \
            data_obj.backing_file[stxm_entry.name + '/data/lab_sxy/lab_sx'].value*1e-6
        data_obj.meta_data.set_meta_data('x', x)
        # axis label
        
        ### set the y
        y = \
            data_obj.backing_file[stxm_entry.name + '/data/lab_sxy/lab_sy'].value*1e-6
        pos = np.zeros((2,len(y)))
        pos[0,:] = y
        pos[1,:] = x
        data_obj.meta_data.set_meta_data('xy', pos)
        # axis label
        labels.append('xy.metres')
#         labels.append('y.microns')
        # now set them
        labels.extend(['detectorX.pixel','detectorY.pixel'])
        print labels
        data_obj.set_axis_labels(*tuple(labels))

        
        dims = range(len(data_obj.get_shape()))
        diff_core = (-2,-1) # it will always be this
        print diff_core
        
        diff_slice = tuple(dims[:-2])
        print diff_slice
        logging.debug("is a diffraction")
        logging.debug("the diffraction cores are:"+str(diff_core))
        logging.debug("the diffraction slices are:"+str(diff_slice))
        data_obj.add_pattern("DIFFRACTION", core_dir=diff_core,
                             slice_dir=diff_slice)
        
        data_obj.add_pattern("4D_SCAN", core_dir=(1,2,3),
                        slice_dir=(0,))
  
        self.set_data_reduction_params(data_obj)
