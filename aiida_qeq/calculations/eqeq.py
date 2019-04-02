"""
Calculations provided by aiida_qeq.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from __future__ import absolute_import
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Data
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.plugins import DataFactory
import six

EQeqParameters = DataFactory('qeq.eqeq')
CifData = DataFactory('cif')


class EQeqCalculation(CalcJob):
    """
    AiiDA calculation plugin for the EQeq code.
    """

    _LOG_FILE_NAME = 'eqeq.log'

    @classmethod
    def define(cls, spec):
        super(EQeqCalculation, cls).define(spec)
        spec.input(
            'metadata.options.parser_name',
            valid_type=six.string_types,
            default='qeq.eqeq')
        spec.input('metadata.options.withmpi', valid_type=bool, default=False)

        spec.input(
            'parameters',
            valid_type=EQeqParameters,
            help='Command line parameters for EQEQ')
        spec.input(
            'ionization_data',
            valid_type=SinglefileData,
            help='File containing ionization data on the elements.')
        spec.input(
            'charge_data',
            valid_type=SinglefileData,
            help=
            'File containing information on common oxidation state of the elements.'
        )
        spec.input(
            'structure',
            valid_type=CifData,
            help='Input structure, for which atomic charges are to be computed.'
        )

        spec.outputs.dynamic = True
        spec.outputs.valid_type = Data

    def prepare_for_submission(self, folder):
        """Create the input files from the input nodes passed to this instance of the `CalcJob`.

        :param folder: an `aiida.common.folders.Folder` to temporarily write files on disk
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        # Prepare CodeInfo object for aiida
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
            structure_file_name=self.inputs.structure.filename,
            ionization_file_name=self.inputs.ionization_data.filename,
            charge_file_name=self.inputs.charge_data.filename)
        codeinfo.stdout_name = self._LOG_FILE_NAME

        # Prepare CalcInfo object for aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            [
                self.inputs.structure.uuid, self.inputs.structure.filename,
                self.inputs.structure.filename
            ],
            [
                self.inputs.ionization_data.uuid,
                self.inputs.ionization_data.filename,
                self.inputs.ionization_data.filename
            ],
            [
                self.inputs.charge_data.uuid, self.inputs.charge_data.filename,
                self.inputs.charge_data.filename
            ],
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = self.inputs.parameters.output_files(
            self.inputs.structure.filename)
        calcinfo.codes_info = [codeinfo]

        return calcinfo
