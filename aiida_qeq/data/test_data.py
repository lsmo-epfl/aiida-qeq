from __future__ import absolute_import
from __future__ import print_function
from aiida.manage.fixtures import PluginTestCase


class TestEQeqParameters(PluginTestCase):
    def test_cmdline_1(self):
        from aiida.plugins import DataFactory
        EQeqParameters = DataFactory('qeq.eqeq')

        d = {'method': 'ewald'}
        p = EQeqParameters(d)

        cmdline = p.cmdline_params(structure_file_name='test.cif')
        expected_cmdline = [
            'test.cif', '1.2', '-2.0', '3', 'ewald', '2', '2', '50',
            'ionizationdata.dat', 'chargecenters.dat'
        ]

        self.assertEqual(cmdline, expected_cmdline)

    def test_params_1(self):
        """Test passing disallowed value to input parameters."""
        from aiida.plugins import DataFactory
        from voluptuous import MultipleInvalid
        EQeqParameters = DataFactory('qeq.eqeq')

        d = {'method': 'badmethod'}

        with self.assertRaises(MultipleInvalid):
            EQeqParameters(d)


class TestQeqParameters(PluginTestCase):
    def test_cmdline_1(self):
        from aiida.plugins import DataFactory
        QeqParameters = DataFactory('qeq.qeq')

        d = {'imethod': 0}
        p = QeqParameters(d)

        cmdline = p.cmdline_params(structure_file_name='test.cif')
        expected_cmdline = ['test.cif', 'GMP.param', 'configure.input']

        self.assertEqual(cmdline, expected_cmdline)

    def test_configure_1(self):
        """Test configure file output"""
        from aiida.plugins import DataFactory
        QeqParameters = DataFactory('qeq.qeq')

        d = {'imethod': 0}
        p = QeqParameters(d)

        expected_string = \
"""build_grid 0
build_grid_from_scratch 1 none 0.25 0.25 0.25 1.0 2.0 0 3.0
save_grid 0 grid.cube
calculate_pot_diff 0
calculate_pot 0 repeat.cube
skip_everything 0
point_charges_present 0
include_pceq 0
imethod 0"""

        self.assertEqual(p.configure_string, expected_string)
