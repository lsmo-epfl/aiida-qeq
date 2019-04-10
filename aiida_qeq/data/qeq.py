# -*- coding: utf-8 -*-
"""
Data types provided by plugin for Qeq calculation.

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from __future__ import absolute_import
import os
from aiida.orm import Dict
from voluptuous import Schema, Optional, Any, ExactSequence
from collections import OrderedDict

# key : [ accepted values, label ]
cmdline_options = OrderedDict([
    (Optional('build_grid', default=False), bool),
    # true/false input_grid_file dh1sz dh2sz dh3sz vdw_factor_e vdw_factor_f use_vdw_factor offset
    # e.g. build_grid_from_scratch 1 none 0.25 0.25 0.25 1.0 2.0 0 3.0
    (Optional('build_grid_from_scratch', default=[True, 'none']),
     ExactSequence([bool, str])),
    (Optional('grid_spacing', default=[0.25, 0.25, 0.25]),
     ExactSequence([float, float, float])),
    # where to print the potential (e.g. between 1x vdw radius and 2x vdw radius)
    (Optional('vdw_factors', default=[False, 1.0, 2.0]),
     ExactSequence([bool, float, float])),
    (Optional('offset', default=3.0), float),
    (Optional('save_grid', default=[False, 'grid.cube']),
     ExactSequence([bool, str])),
    (Optional('calculate_pot_diff', default=False), bool),
    (Optional('calculate_pot', default=[0, 'repeat.cube']),
     ExactSequence([int, str])),
    (Optional('skip_everything', default=False), bool),
    (Optional('point_charges_present', default=False), bool),
    (Optional('include_pceq', default=False), bool),
    (Optional('imethod', default=0), int),
])

DEFAULT_PARAM_FILE_NAME = 'GMP.param'
DEFAULT_CONFIGURE_FILE_NAME = 'configure.input'
DEFAULT_OUTPUT_FILES = ['charges.cif']

ALL_OUTPUT_FILES = ["charges.cif", "charges.dat", "charges.xyz", "energy.dat"]

output_options = {
    Optional('retrieve', default=DEFAULT_OUTPUT_FILES):
    [Any(*ALL_OUTPUT_FILES)]
}

options = dict(cmdline_options)
options.update(output_options)


class QeqParameters(Dict):
    """
    Command line options for qeq.
    """

    _schema = Schema(options)
    schema = _schema.schema  # alias for easier printing

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``QeqParameters(dict{'lambda': 1.4})``

        .. note:: As of 2017-09, the constructor must also support a single dbnode
          argument (to reconstruct the object from a database node).
          For this reason, positional arguments are not allowed.
        """
        if 'dbnode' in kwargs:
            super(QeqParameters, self).__init__(**kwargs)
        else:
            # validate dictionary
            if dict is None:
                dict = {}
            dict = self.validate(dict)
            super(QeqParameters, self).__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options."""
        return QeqParameters._schema(parameters_dict)

    def cmdline_params(self,
                       structure_file_name,
                       param_file_name=DEFAULT_PARAM_FILE_NAME):
        """Synthesize command line parameters.

        e.g. [ 'HKUST-1.cif', 'GMP.param', 'configure.input']

        :param structure_file_name: Name of input structure (cif format)
        :param param_file_name: Name of parameter file name (e.g. GMP.param)

        """
        parameters = []

        parameters += [structure_file_name]
        parameters += [param_file_name]
        parameters += [DEFAULT_CONFIGURE_FILE_NAME]

        return [str(p) for p in parameters]

    @property
    def output_files(self):
        """Returns list of expected output files.
        
        :param structure_file_name: Name of input structure (cif format)
        """
        pm_dict = self.get_dict()
        return pm_dict["retrieve"]

    @property
    def configure_string(self):
        """Create configure.input string from dictionary.

        Example configure.input:

        build_grid 0
        build_grid_from_scratch 1 none 0.25 0.25 0.25 1.0 2.0 0 3.0
        save_grid 0 grid.cube
        calculate_pot_diff 0
        calculate_pot 0 repeat.cube
        skip_everything 0
        point_charges_present 0
        include_pceq 0
        imethod 0
        """

        pm_dict = self.get_dict()

        br = os.linesep

        s = ""
        s += "build_grid {}".format(int(pm_dict["build_grid"]))
        s += br + "build_grid_from_scratch {} {} {} {} {} {} {} {} {}".format(
            int(pm_dict["build_grid_from_scratch"][0]),
            pm_dict["build_grid_from_scratch"][1],
            pm_dict["grid_spacing"][0],
            pm_dict["grid_spacing"][1],
            pm_dict["grid_spacing"][2],
            pm_dict["vdw_factors"][1],
            pm_dict["vdw_factors"][2],
            int(pm_dict["vdw_factors"][0]),
            pm_dict["offset"],
        )
        s += br + "save_grid {} {}".format(
            int(pm_dict["save_grid"][0]), pm_dict["save_grid"][1])
        s += br + "calculate_pot_diff {}".format(
            int(pm_dict["calculate_pot_diff"]))
        s += br + "calculate_pot {} {}".format(*pm_dict["calculate_pot"])
        s += br + "skip_everything {}".format(int(pm_dict["skip_everything"]))
        s += br + "point_charges_present {}".format(
            int(pm_dict["point_charges_present"]))
        s += br + "include_pceq {}".format(int(pm_dict["include_pceq"]))
        s += br + "imethod {}".format(pm_dict["imethod"])

        return s
