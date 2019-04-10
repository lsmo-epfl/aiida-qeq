"""
Calculations provided by aiida_qeq for Qeq calculations.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

from __future__ import absolute_import
import io
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Data
from aiida.common.datastructures import (CalcInfo, CodeInfo)
from aiida.plugins import DataFactory
import six

QeqParameters = DataFactory('qeq.qeq')
CifData = DataFactory('cif')


class QeqCalculation(CalcJob):
    """
    AiiDA calculation plugin for the Qeq code.
    """

    _LOG_FILE_NAME = 'qeq.log'

    @classmethod
    def define(cls, spec):
        super(QeqCalculation, cls).define(spec)
        spec.input(
            'metadata.options.parser_name',
            valid_type=six.string_types,
            default='qeq.qeq')
        spec.input('metadata.options.withmpi', valid_type=bool, default=False)

        spec.input(
            'configure',
            valid_type=QeqParameters,
            help='Configuration input for QEQ (configure.input file)',
            required=False)
        spec.input(
            'parameters',
            valid_type=SinglefileData,
            help=
            'File containing electronegativity and Idempotential data of the elements.'
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
        from aiida_qeq.data.qeq import DEFAULT_CONFIGURE_FILE_NAME

        try:
            configure = self.inputs.configure
        except AttributeError:
            configure = QeqParameters()

        # Prepare CodeInfo object for aiida
        codeinfo = CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.cmdline_params = configure.cmdline_params(
            structure_file_name=self.inputs.structure.filename,
            param_file_name=self.inputs.parameters.filename)
        codeinfo.stdout_name = self._LOG_FILE_NAME

        # write configure.input file
        with io.StringIO(configure.configure_string) as handle:
            folder.create_file_from_filelike(
                handle, filename=DEFAULT_CONFIGURE_FILE_NAME, mode='w')

        # Prepare CalcInfo object for aiida
        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.local_copy_list = [
            [
                self.inputs.structure.uuid, self.inputs.structure.filename,
                self.inputs.structure.filename
            ],
            [
                self.inputs.parameters.uuid, self.inputs.parameters.filename,
                self.inputs.parameters.filename
            ],
        ]
        calcinfo.remote_copy_list = []
        calcinfo.retrieve_list = configure.output_files
        calcinfo.codes_info = [codeinfo]

        return calcinfo
