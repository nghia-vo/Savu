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
.. module:: parameter_utils
   :platform: Unix
   :synopsis: Parameter utilities

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""
from __future__ import print_function, division, absolute_import

import os
import h5py
import posixpath
import numpy as np
import configparser

from colorama import Fore

import savu.plugins.loaders.utils.yaml_utils as yu

def _intlist(value):
    '''['int'] '''
    parameter_valid = False
    # Currently the check is for a list, but this can later be more extensive
    if isinstance(value, list):
        parameter_valid = True
    return parameter_valid

def _range(value):
    '''range'''
    parameter_valid = False
    if isinstance(value, tuple):
        if len(value) == 2:
            if _integer(value[0]) and _integer(value[1]):
                    parameter_valid = True
        else:
            print(Fore.RED + 'Please enter two values.' + Fore.RESET)
    return parameter_valid

def _yamlfile(value):
    """ yaml_file """
    parameter_valid = False
    if _filepath(value):
        f = open(value)
        errors = yu.check_yaml_errors(f)
        try:
            yu.read_yaml(value)
            parameter_valid = True
        except:
            if errors:
                print('There were some errors with your yaml file structure.')
                for e in errors:
                    print(e)
    return parameter_valid


def _intgroup(value):
    """ [path, int_path, int] """
    # To be replaced
    parameter_valid = False
    try:
        if _list(value):
            entries = value
        if len(entries) == 3:
            file_path = entries[0]

            if _filepath(file_path):
                int_path = entries[1]
                hf = h5py.File(file_path, 'r')
                try:
                    # This returns a HDF5 dataset object
                    int_data = hf.get(int_path)
                    if int_data is None:
                        print('There is no data stored at that internal path.')
                    else:
                        # Internal path is valid
                        int_data = np.array(int_data)
                        if int_data.size >= 1:
                            try:
                                compensation_fact = entries[2]
                                parameter_valid = _integer(compensation_fact)
                            except (Exception, ValueError):
                                print('The compensation factor is not an integer.')

                except AttributeError:
                    print('Attribute error.')
                except:
                    print(Fore.BLUE + 'Please choose another interior'
                                      ' path.' + Fore.RESET)
                    print('Example interior paths: ')
                    for group in hf:
                        for subgroup in hf[group]:
                            subgroup_str = '/' + group + '/' + subgroup
                            print(u'\t' + subgroup_str)
                    raise
                hf.close()
        else:
            print(Fore.RED + 'Please enter three parameters.' + Fore.RESET)
    finally:
        return parameter_valid


def _intgroup1(value):
    """ [int_path, int] """
    parameter_valid = False
    try:
        if _list(value):
            entries = value
        if len(entries) == 2:
            int_path = entries[0]
            if _intpathway(int_path):
                try:
                    scale_fact = int(entries[1])
                    parameter_valid = _integer(scale_fact)
                except (Exception, ValueError):
                    print('The scale factor is not an integer.')
        else:
            print(Fore.RED + 'Please enter two parameters.' + Fore.RESET)
    finally:
        return parameter_valid


def _directory(value):
    """ directory """
    parameter_valid = False
    # take the directory from the path
    # path = os.path.dirname(value)
    path = value if value else '.'
    if os.path.isdir(path):
        parameter_valid = True
    return parameter_valid


def _filepath(value):
    """ file path """
    parameter_valid = False
    if os.path.isfile(value):
        parameter_valid = True
    return parameter_valid


def _intpathway(value):
    # Interior file path
    parameter_valid = False
    # Could check if valid, but only if file_path known for another parameter
    if isinstance(value, str):
        parameter_valid = True
    return parameter_valid


def _configfile(value):
    parameter_valid = False
    if _filepath(value):
        filetovalidate = configparser.ConfigParser()
        filetovalidate.read(value)
        content = filetovalidate.sections()
        if content:
            parameter_valid = True
    return parameter_valid


def _filename(value):
    """Check if the value is a valid filename string
    """
    parameter_valid = False
    if _string(value):
        filename = posixpath.normpath(value)
        # Normalise the pathname by collapsing redundant separators and
        # references so that //B, A/B/, A/./B and A/../B all become A/B.
        _os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                            if sep not in (None, '/'))
        # Find which separators the operating system provides, excluding slash
        for sep in _os_alt_seps:
            if sep in filename:
                return False
        # If path is an absolute pathname. On Unix, that means it begins with
        # a slash, on Windows that it begins with a (back)slash after removing
        # drive letter.
        if os.path.isabs(filename) or filename.startswith('../'):
            print('Please make sure the filename is absolute and doesn\'t'
                  ' change directory.')
            return False
        parameter_valid = True
    return parameter_valid


def _nptype(value):
    """Check if the value is a numpy data type. Return true if it is.
    """
    parameter_valid = False
    if (value in np.typecodes) or (value in np.sctypeDict.keys()):
        parameter_valid = True
    return parameter_valid


def _integer(value):
    parameter_valid = False
    if isinstance(value, int):
        parameter_valid = True
    return parameter_valid


def _boolean(value):
    parameter_valid = False
    if isinstance(value, bool):
        parameter_valid = True
    elif value == 'true' or value == 'false':
        parameter_valid = True
    return parameter_valid


def _string(value):
    parameter_valid = False
    if isinstance(value, str):
        parameter_valid = True
    return parameter_valid


def _float(value):
    parameter_valid = False
    if isinstance(value, float):
        parameter_valid = True
    return parameter_valid


def _tuple(value):
    parameter_valid = False
    if isinstance(value, tuple):
        parameter_valid = True
    return parameter_valid


def _list(value):
    parameter_valid = False
    if isinstance(value, list):
        # This is a list of integer values
        parameter_valid = True
    else:
        parameter_valid = _string_list(value)
    return parameter_valid


def _string_list(value):
    """ A list of string values"""
    parameter_valid = False
    try:
        if '[' and ']' in value:
            bracket_value = value.split('[')
            first_bracket_value = bracket_value[1].split(']')
            if first_bracket_value < 2:
                if first_bracket_value[1]:
                    print('There are values outside of the square brackets')
                else:
                    entries = first_bracket_value[0].split(',')
                    str_list = [v for v in entries]
                    parameter_valid = True
            else:
                print('Please enter three values inside your list.')
    finally:
        return parameter_valid

# If you are editing the type dictionary, please update the documentation
# files dev_plugin.rst and the files included inside dev_param_key.rst to
# provide guidance for plugin creators
type_dict = {'int_list': _intlist,
            'range': _range,
            'yaml_file': _yamlfile,
            'file_int_path_int': _intgroup,
            'int_path_int': _intgroup1,
            'filepath': _filepath,
            'directory': _directory,
            'int_path': _intpathway,
            'config_file': _configfile,
            'filename': _filename,
            'nptype': _nptype,
            'int': _integer,
            'bool': _boolean,
            'str': _string,
            'float': _float,
            'tuple': _tuple,
            'list': _list}

type_error_dict = {'int_list': 'list of integers',
            'range': 'range. Valid items have a format <value 1>, <value 2>',
            'yaml_file': 'yaml format',
            'file_int_path_int': 'input. Valid items have a format '
                                 '[<file path>, <interior file path>, int]',
            'int_path_int': 'input. Valid items have a format '
                            '[<interior file path>, int]',
            'filepath': 'filepath',
            'directory': 'directory',
            'int_path': 'string',
            'config_file': 'config file',
            'filename': 'file name',
            'nptype': 'numpy data type',
            'int': 'integer',
            'bool': 'boolean',
            'str': 'string',
            'float': 'float',
            'tuple': 'tuple',
            'list': 'list'}


def is_valid(param_name, value, current_parameter_details):
    """ Check if the value matches the default value.
    Then type check, followed by a check on whether it is present in options
    If the items in options have not been type checked, or have errors,
    it may cause problems.
    """
    dtype = current_parameter_details['dtype']
    default_value = current_parameter_details['default']
    # If a default value is used, this is a valid option
    pvalid = _check_default(value, default_value)
    type_error_str = ''
    if pvalid is False:
        if isinstance(dtype, list):
            # This is a list of possible types
            for individual_type in dtype:
                pvalid = type_dict[individual_type](value)
                if pvalid is True:
                    break

        elif dtype not in type_dict.keys():
            type_error_str = 'That type definition is not configured properly.'
            pvalid = False
        else:
            pvalid = type_dict[dtype](value)
        # Then check if the option is valid
        pvalid, option_error_str = _check_options(current_parameter_details, value, pvalid)

    if pvalid is False:
        type_error_str = option_error_str if option_error_str else _error_message(dtype, param_name)

    return pvalid, type_error_str

def _check_default(value, default_value):
    """ Return true if the new value is either a match for the default
    parameter value or the string 'default'
    """
    default_present = False
    if default_value == str(value) or default_value == value\
                or value == 'default' or str(default_value) == str(value):
        default_present = True
    return default_present

def _check_options(current_parameter_details, value, pvalid):
    """ Check if the input value matches one of the valid parameter options
    """
    option_error_str = ''
    options = current_parameter_details.get('options') or {}
    if len(options) >= 1:
        if value in options or str(value) in options:
            pvalid = True
        else:
            pvalid = False
            option_error_str = 'That does not match one of the required options.'
            option_error_str += Fore.CYAN + '\nSome options are:\n'
            option_error_str += '\n'.join(options) + Fore.RESET
    return pvalid, option_error_str


def _error_message(dtype, param_name):
    if isinstance(dtype, list):
        type_options = ' or '.join([str(t) for t in dtype])
        error_str = 'Your input for the parameter \'{}\' must match' \
                    ' the type {}.'.format(param_name, type_options)
    else:
        error_str = 'Your input for the parameter \'{}\' must match' \
                    ' the type \'{}\'.'.format(param_name, type_error_dict[dtype])
    return error_str