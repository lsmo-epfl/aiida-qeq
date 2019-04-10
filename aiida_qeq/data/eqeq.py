# -*- coding: utf-8 -*-
"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from __future__ import absolute_import
from aiida.orm import Dict
from voluptuous import Schema, Optional, Any
from collections import OrderedDict

# key : [ accepted values, label ]
cmdline_options = OrderedDict([
    (Optional('lambda', default=1.2), float),
    (Optional('hI0', default=-2.0), float),
    (Optional('charge-precision', default=3), int),
    (Optional('method', default='ewald'), Any("ewald", "nonperiodic")),
    (Optional('mr', default=2), int),
    (Optional('mk', default=2), int),
    (Optional('eta', default=50), int),
])

DEFAULT_CHARGE_FILE_NAME = 'chargecenters.dat'
DEFAULT_IONIZATION_FILE_NAME = 'ionizationdata.dat'
DEFAULT_OUTPUT_FILE_EXTENSIONS = ['json', 'cif']

output_options = {
    Optional('retrieve', default=DEFAULT_OUTPUT_FILE_EXTENSIONS):
    [Any("car", "cif", "json", "mol", "pdb")]
}

options = dict(cmdline_options)
options.update(output_options)


class EQeqParameters(Dict):
    """
    Command line options for eqeq.
    """

    _schema = Schema(options)
    schema = _schema.schema  # alias for easier printing

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``EQeqParameters(dict{'lambda': 1.4})``

        .. note:: As of 2017-09, the constructor must also support a single dbnode
          argument (to reconstruct the object from a database node).
          For this reason, positional arguments are not allowed.
        """
        if 'dbnode' in kwargs:
            super(EQeqParameters, self).__init__(**kwargs)
        else:
            # validate dictionary
            dict = self.validate(dict)
            super(EQeqParameters, self).__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options."""
        return EQeqParameters._schema(parameters_dict)

    def cmdline_params(self,
                       structure_file_name,
                       ionization_file_name=DEFAULT_IONIZATION_FILE_NAME,
                       charge_file_name=DEFAULT_CHARGE_FILE_NAME):
        """Synthesize command line parameters.

        e.g. [ 'HKUST-1.cif', '1.4']

        :param structure_file_name: Name of input structure (cif format)

        """
        parameters = []

        parameters += [structure_file_name]

        pm_dict = self.get_dict()
        # note: ParameterData uses python dictionaries, which do not preserve order
        # We assume all keys are provided (using validation) and use the correct order
        # from cmdline_options
        for k in cmdline_options.keys():
            parameters += [pm_dict[k]]

        parameters += [ionization_file_name]
        parameters += [charge_file_name]

        return [str(p) for p in parameters]

    def output_files_dict(self, structure_file_name):
        """Returns dictionary with names of output files to be retrieved.
        
        Keys are the file extension, values are the full file name.

        :param structure_file_name: Name of input structure (cif format)
        """
        pm_dict = self.get_dict()

        name = "{s}_EQeq_{m}_{la:.2f}_{h:.2f}".format(
            s=structure_file_name,
            m=pm_dict['method'],
            la=pm_dict['lambda'],
            h=pm_dict['hI0'],
        )

        output_dict = {
            ext: "{}.{}".format(name, ext)
            for ext in pm_dict['retrieve']
        }

        return output_dict

    def output_files(self, structure_file_name):
        """Returns list of expected output files.
        
        :param structure_file_name: Name of input structure (cif format)
        """
        return list(self.output_files_dict(structure_file_name).values())
