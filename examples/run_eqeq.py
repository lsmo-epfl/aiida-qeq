#!/usr/bin/env python  # pylint: disable=invalid-name
# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
import os
import aiida_qeq.tests as tests
import aiida_qeq.data.eqeq as data
from aiida_qeq.data import DATA_DIR
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

EqeqCalc = CalculationFactory('qeq.eqeq')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
Parameters = DataFactory('qeq.eqeq')

builder = EqeqCalc.get_builder()
builder.code = tests.get_code(entry_point='qeq.eqeq')
builder.metadata = {
    'options': {
        'resources': {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        },
        'max_wallclock_seconds': 120,
    },
    'label': 'aiida_qeq EQEQ test',
    'description': 'Test EQEQ job submission with the aiida_qeq plugin',
}

builder.structure = CifData(file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'))
builder.parameters = Parameters({'method': 'ewald'})
builder.charge_data = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_CHARGE_FILE_NAME))
builder.ionization_data = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_IONIZATION_FILE_NAME))

result = run(builder)
print(result)
