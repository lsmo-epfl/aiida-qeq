# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_qeq for QEQ calculations.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
import os

from aiida.parsers.parser import Parser
from aiida.common import exceptions
from aiida.plugins import CalculationFactory, DataFactory

from aiida_qeq.data.qeq import LOG_FILE_NAME

QeqCalculation = CalculationFactory('qeq.qeq')
SinglefileData = DataFactory('singlefile')


class QeqParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance
        """
        super(QeqParser, self).__init__(node)  # pylint: disable=super-with-arguments
        if not issubclass(node.process_class, QeqCalculation):
            raise exceptions.ParsingError('Can only parse EQeqCalculation')

    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        # Check that the retrieved folder is there
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        # Check the folder content is as expected
        list_of_files = output_folder.list_object_names()

        if 'configure' in self.node.inputs:
            output_files = self.node.inputs.configure.output_files
        else:
            output_files = DataFactory('qeq.qeq')().output_files

        # Note: set(A) <= set(B) checks whether A is a subset
        if set(output_files) <= set(list_of_files):
            pass
        else:
            self.logger.error('Not all expected output files {} were found'.format(output_files))

        # Check code didn't segfault
        with output_folder.open(self.node.get_option('scheduler_stderr'), 'r') as handle:
            stderr = handle.read()
        if 'Segmentation fault' in stderr:
            return self.exit_codes.ERROR_SEGFAULT

        # Check log file for error detection
        retrieved_temporary_folder = kwargs.pop('retrieved_temporary_folder', None)
        if retrieved_temporary_folder:
            with open(os.path.join(retrieved_temporary_folder, LOG_FILE_NAME), 'r') as handle:
                log = handle.read()
            # Check that calculation converged
            if 'SCF NOT CONVERGED' in log:
                return self.exit_codes.ERROR_SCF_NOT_CONVERGED

        CifData = DataFactory('cif')  # pylint: disable=invalid-name

        for fname in output_files:
            if fname == 'charges.cif':
                # add cif file
                with output_folder.open(fname, 'rb') as handle:
                    cif = CifData(file=handle, parse_policy='lazy')
                # Note: we might want to either contribute this attribute upstream
                # or set up our own CifData class
                cif.set_attribute('partial_charge_method', 'qeq')
                self.out('structure_with_charges', cif)
            else:
                # add as singlefile
                with output_folder.open(fname, 'rb') as handle:
                    node = SinglefileData(file=handle)
                self.out(fname, node)
