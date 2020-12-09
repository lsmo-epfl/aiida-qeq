# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_qeq.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from aiida.parsers.parser import Parser
from aiida.common import exceptions

from aiida.plugins import CalculationFactory, DataFactory

EQeqCalculation = CalculationFactory('qeq.eqeq')
SinglefileData = DataFactory('singlefile')


class EQeqParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance
        """
        super(EQeqParser, self).__init__(node)  # pylint: disable=super-with-arguments
        if not issubclass(node.process_class, EQeqCalculation):
            raise exceptions.ParsingError('Can only parse EQeqCalculation')

    def parse(self, **kwargs):  # pylint: disable=inconsistent-return-statements
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        CifData = DataFactory('cif')  # pylint: disable=invalid-name

        # Check that the retrieved folder is there
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        # Check the folder content is as expected
        list_of_files = output_folder.list_object_names()
        output_dict = self.node.inputs.parameters.output_files_dict(self.node.inputs.structure.filename)
        output_files = list(output_dict.values())
        # Note: set(A) <= set(B) checks whether A is a subset
        if set(output_files) <= set(list_of_files):
            pass
        else:
            self.logger.error('Not all expected output files {} were found'.format(output_files))

        for ext in output_dict.keys():
            fname = output_dict[ext]
            if ext == 'cif':
                # add cif file
                with output_folder.open(fname, 'rb') as handle:
                    cif = CifData(file=handle, parse_policy='lazy')
                # Note: we might want to either contribute this attribute upstream
                # or set up our own CifData class
                cif.set_attribute('partial_charge_method', 'eqeq')
                self.out('structure_with_charges', cif)
            else:
                # add as singlefile
                with output_folder.open(fname, 'rb') as handle:
                    node = SinglefileData(file=handle)
                self.out('{}_with_charges'.format(ext), node)
