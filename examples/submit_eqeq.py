# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import aiida_qeq.tests as tests
import aiida_qeq.data.eqeq as data
from aiida_qeq.data import DATA_DIR
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

# Prepare input parameters
parameters = DataFactory('qeq.eqeq')({'method': 'ewald'})

SinglefileData = DataFactory('singlefile')
charge_file = SinglefileData(
    file=os.path.join(DATA_DIR, data.DEFAULT_CHARGE_FILE_NAME))
ionization_file = SinglefileData(
    file=os.path.join(DATA_DIR, data.DEFAULT_IONIZATION_FILE_NAME))

cif = DataFactory('cif')(
    file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'), parse_policy='lazy')

inputs = {
    # make sure the "eqeq" binary is in your PATH
    'code': tests.get_code(entry_point='qeq.eqeq'),
    'structure': cif,
    'parameters': parameters,
    'charge_data': charge_file,
    'ionization_data': ionization_file,
    'metadata': {
        'options': {
            "resources": {
                "num_machines": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 120,
        },
        'label': "aiida_qeq EQEQ test",
        'description': "Test EQEQ job submission with the aiida_qeq plugin",
    },
}

result = run(CalculationFactory('qeq.eqeq'), **inputs)
print(result)
