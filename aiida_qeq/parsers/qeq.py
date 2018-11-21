# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_qeq for QEQ calculations.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

from aiida.parsers.parser import Parser
from aiida.parsers.exceptions import OutputParsingError


class QeqParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, calculation):
        """
        Initialize Parser instance
        """
        super(QeqParser, self).__init__(calculation)

        # check for valid input
        from aiida.orm import CalculationFactory
        QeqCalculation = CalculationFactory('qeq.qeq')
        if not isinstance(calculation, QeqCalculation):
            raise OutputParsingError("Can only parse QeqCalculation")

    # pylint: disable=protected-access
    def parse_with_retrieved(self, retrieved):
        """
        Parse outputs, store results in database.

        :param retrieved: a dictionary of retrieved nodes, where
          the key is the link name
        :returns: a tuple with two values ``(bool, node_list)``, 
          where:

          * ``bool``: variable to tell if the parsing succeeded
          * ``node_list``: list of new nodes to be stored in the db
            (as a list of tuples ``(link_name, node)``)
        """
        from aiida.orm import DataFactory

        success = False
        node_list = []

        # Check that the retrieved folder is there
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")
            return success, node_list

        # Check the folder content is as expected
        list_of_files = out_folder.get_folder_list()

        if hasattr(self._calc.inp, 'configure'):
            output_files = self._calc.inp.configure.output_files
        else:
            QeqParameters = DataFactory('qeq.qeq')
            output_files = QeqParameters().output_files

        # Note: set(A) <= set(B) checks whether A is a subset
        if set(output_files) <= set(list_of_files):
            pass
        else:
            self.logger.error("Not all expected output files {} were found".
                              format(output_files))

        SinglefileData = DataFactory('singlefile')
        CifData = DataFactory('cif')

        for fname in output_files:
            if fname == 'charges.cif':
                # add cif file
                cif = CifData(
                    file=out_folder.get_abs_path(fname), parse_policy='lazy')
                # Note: we might want to either contribute this attribute upstream
                # or set up our own CifData class
                cif._set_attr('partial_charge_method', 'qeq')
                node_list.append(('structure_with_charges', cif))

            else:
                # add as singlefile
                node = SinglefileData(file=out_folder.get_abs_path(fname))
                node_list.append((fname, node))

        success = True
        return success, node_list
