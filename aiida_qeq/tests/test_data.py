from __future__ import absolute_import
from aiida.utils.fixtures import PluginTestCase


class TestEQeqParameters(PluginTestCase):
    def test_cmdline_1(self):
        from aiida.orm import DataFactory
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
        from aiida.orm import DataFactory
        from voluptuous import MultipleInvalid
        EQeqParameters = DataFactory('qeq.eqeq')

        d = {'method': 'badmethod'}

        with self.assertRaises(MultipleInvalid):
            EQeqParameters(d)
