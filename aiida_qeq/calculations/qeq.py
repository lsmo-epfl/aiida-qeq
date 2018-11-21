"""
Calculations provided by aiida_qeq for Qeq calculations.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from __future__ import absolute_import
import tempfile
import os
from aiida.orm.calculation.job import JobCalculation
from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import (InputValidationError, ValidationError)
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.orm import DataFactory

QeqParameters = DataFactory('qeq.qeq')
CifData = DataFactory('cif')


class QeqCalculation(JobCalculation):
    """
    AiiDA calculation plugin for the Qeq code.
    """

    _LOG_FILE_NAME = 'qeq.log'

    def _init_internal_params(self):
        """
        Init internal parameters at class load time
        """
        # reuse base class function
        super(QeqCalculation, self)._init_internal_params()

        # qeq.qeq entry point defined in setup.json
        self._default_parser = 'qeq.qeq'

    @classproperty
    def _use_methods(cls):
        """
        Add use_* methods for calculations.
        
        """
        use_dict = JobCalculation._use_methods
        use_dict.update({
            "configure": {
                'valid_types': QeqParameters,
                'additional_parameter': None,
                'linkname': 'configure',
                'docstring':
                ("Configuration input for QEQ (configure.input file)")
            },
            "parameters": {
                'valid_types':
                SinglefileData,
                'additional_parameter':
                None,
                'linkname':
                'parameters',
                'docstring':
                ("File containing electronegativity and Idempotential data of the elements."
                 )
            },
            "structure": {
                'valid_types':
                CifData,
                'additional_parameter':
                None,
                'linkname':
                'structure',
                'docstring':
                ("Input structure, for which atomic charges are to be computed."
                 )
            },
        })
        return use_dict

    def _validate_inputdict(self, inputdict):  # noqa: MC0001
        """Validates inputdict of calculation.

        Checks that (only) expected keys are present and that values are of the expected type.
        """
        # Check inputdict
        try:
            code = inputdict.pop(self.get_linkname('code'))
        except KeyError:
            raise InputValidationError("No code specified for this "
                                       "calculation")
        try:
            configure = inputdict.pop(self.get_linkname('configure'))
            if not isinstance(configure, QeqParameters):
                raise InputValidationError("configure not of type "
                                           "QeqParameters")
        except KeyError:
            configure = QeqParameters()

        try:
            parameters = inputdict.pop(self.get_linkname('parameters'))
        except KeyError:
            raise InputValidationError("No parameters specified for this "
                                       "calculation")
        if not isinstance(parameters, SinglefileData):
            raise InputValidationError("parameters not of type "
                                       "SinglefileData")

        try:
            structure = inputdict.pop(self.get_linkname('structure'))
        except KeyError:
            raise InputValidationError("Missing input structure")
        if not isinstance(structure, CifData):
            raise InputValidationError("input structure not of type CifData")

        if inputdict:
            raise ValidationError("Unknown inputs {}".format(str(inputdict)))

        return code, parameters, structure, configure

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """
        from aiida_qeq.data.qeq import DEFAULT_CONFIGURE_FILE_NAME

        code, parameters, structure, configure = self._validate_inputdict(
            inputdict)

        # Prepare CodeInfo object for aiida
        codeinfo = CodeInfo()
        codeinfo.code_uuid = code.uuid
        codeinfo.cmdline_params = configure.cmdline_params(
            structure_file_name=structure.filename,
            param_file_name=parameters.filename)
        codeinfo.stdout_name = self._LOG_FILE_NAME

        # write configure.input file
        fd, configure_path = tempfile.mkstemp()
        with open(configure_path, 'w') as f:
            f.write(configure.configure_string)
        os.close(fd)

        # Prepare CalcInfo object for aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            [structure.get_file_abs_path(), structure.filename],
            [parameters.get_file_abs_path(), parameters.filename],
            [configure_path, DEFAULT_CONFIGURE_FILE_NAME],
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = configure.output_files
        calcinfo.codes_info = [codeinfo]

        return calcinfo
