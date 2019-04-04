""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import aiida_qeq.tests as tests
from aiida.engine import run


# pylint: disable=too-many-arguments,unused-argument
def test_submit(aiida_profile, clear_database, ionization_file, charge_file,
                hkust1_cif, basic_options):
    """Test submitting a calculation"""
    from aiida.plugins import CalculationFactory, DataFactory

    EqeqCalculation = CalculationFactory('qeq.eqeq')

    # Prepare input parameters
    EQeqParameters = DataFactory('qeq.eqeq')
    parameters = EQeqParameters({'method': 'ewald'})

    inputs = {
        'code': tests.get_code(entry_point='qeq.eqeq'),
        'structure': hkust1_cif,
        'parameters': parameters,
        'charge_data': charge_file,
        'ionization_data': ionization_file,
        'metadata': {
            'options': basic_options,
            'label': "aiida_qeq EQEQ test",
            'description':
            "Test EQEQ job submission with the aiida_qeq plugin",
        },
    }
    result = run(EqeqCalculation, **inputs)

    charges_list = result['json_with_charges'].get_content()
    assert charges_list.startswith('[0.878')
