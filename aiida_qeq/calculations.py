"""
Calculations provided by aiida_qeq.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from __future__ import absolute_import
from aiida.orm.calculation.job import JobCalculation
from aiida.orm.data.singlefile import SinglefileData
from aiida.common.utils import classproperty
from aiida.common.exceptions import (InputValidationError, ValidationError)
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.orm import DataFactory

EQeqParameters = DataFactory('qeq.eqeq')
CifData = DataFactory('cif')


class EQeqCalculation(JobCalculation):
    """
    AiiDA calculation plugin for the EQeq code.
    """

    _LOG_FILE_NAME = 'eqeq.log'

    def _init_internal_params(self):
        """
        Init internal parameters at class load time
        """
        # reuse base class function
        super(EQeqCalculation, self)._init_internal_params()

        # qeq.eqeq entry point defined in setup.json
        self._default_parser = 'qeq.eqeq'

    @classproperty
    def _use_methods(cls):
        """
        Add use_* methods for calculations.
        
        """
        use_dict = JobCalculation._use_methods
        use_dict.update({
            "parameters": {
                'valid_types': EQeqParameters,
                'additional_parameter': None,
                'linkname': 'parameters',
                'docstring': ("Command line parameters for EQEQ")
            },
            "ionization_data": {
                'valid_types': SinglefileData,
                'additional_parameter': None,
                'linkname': 'ionization_data',
                'docstring':
                ("File containin ionization data on the elements.")
            },
            "charge_data": {
                'valid_types':
                SinglefileData,
                'additional_parameter':
                None,
                'linkname':
                'charge_data',
                'docstring':
                ("File containin information on common oxidation state of the elements."
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
            parameters = inputdict.pop(self.get_linkname('parameters'))
        except KeyError:
            raise InputValidationError("No parameters specified for this "
                                       "calculation")
        if not isinstance(parameters, EQeqParameters):
            raise InputValidationError("parameters not of type "
                                       "EQeqParameters")

        try:
            structure = inputdict.pop(self.get_linkname('structure'))
        except KeyError:
            raise InputValidationError("Missing input structure")
        if not isinstance(structure, CifData):
            raise InputValidationError("input structure not of type CifData")

        try:
            ionization_data = inputdict.pop(
                self.get_linkname('ionization_data'))
        except KeyError:
            raise InputValidationError("Missing ionization data file.")
        if not isinstance(ionization_data, SinglefileData):
            raise InputValidationError(
                "ionization_data not of type SinglefileData")

        try:
            charge_data = inputdict.pop(self.get_linkname('charge_data'))
        except KeyError:
            raise InputValidationError("Missing charge data file.")
        if not isinstance(charge_data, SinglefileData):
            raise InputValidationError(
                "charge_data not of type SinglefileData")

        if inputdict:
            raise ValidationError("Unknown inputs {}".format(str(inputdict)))

        return code, parameters, structure, ionization_data, charge_data

    def _prepare_for_submission(self, tempfolder, inputdict):
        """
        Create input files.

            :param tempfolder: aiida.common.folders.Folder subclass where
                the plugin should put all its files.
            :param inputdict: dictionary of the input nodes as they would
                be returned by get_inputs_dict
        """
        code, parameters, structure, ionization_data, charge_data = self._validate_inputdict(
            inputdict)

        # Prepare CodeInfo object for aiida
        codeinfo = CodeInfo()
        codeinfo.code_uuid = code.uuid
        codeinfo.cmdline_params = parameters.cmdline_params(
            structure_file_name=structure.filename,
            ionization_file_name=ionization_data.filename,
            charge_file_name=charge_data.filename)
        codeinfo.stdout_name = self._LOG_FILE_NAME

        # Prepare CalcInfo object for aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            [structure.get_file_abs_path(), structure.filename],
            [ionization_data.get_file_abs_path(), ionization_data.filename],
            [charge_data.get_file_abs_path(), charge_data.filename],
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = parameters.output_files(structure.filename)
        calcinfo.codes_info = [codeinfo]

        return calcinfo
