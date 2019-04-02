""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import aiida_qeq.tests as tests
from aiida.engine import run_get_node


# pylint: disable=too-many-arguments,unused-argument
def test_submit(aiida_profile, clear_database, ionization_file, charge_file,
                hkust1_cif, qeq_parameters, basic_options):
    """Test submitting a calculation"""
    from aiida.plugins import CalculationFactory
    EqeqCalculation = CalculationFactory('qeq.qeq')

    inputs = {
        'code': tests.get_code(entry_point='qeq.qeq'),
        'structure': hkust1_cif,
        'parameters': qeq_parameters,
        'metadata': {
            'options': basic_options,
            'label': "aiida_qeq QEQ test",
            'description': "Test QEQ job submission with the aiida_qeq plugin",
        },
    }

    _result, node = run_get_node(EqeqCalculation, **inputs)

    print(node)

    assert (_result == 0)
