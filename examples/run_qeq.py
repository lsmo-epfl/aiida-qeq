#!/usr/bin/env python  # pylint: disable=invalid-name
# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
import os
import aiida_qeq.tests as tests
import aiida_qeq.data.qeq as data
from aiida_qeq.data import DATA_DIR
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

QeqCalc = CalculationFactory('qeq.qeq')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')

builder = QeqCalc.get_builder()
builder.code = tests.get_code(entry_point='qeq.qeq')
builder.metadata = {
    'options': {
        'resources': {
            'num_machines': 1,
            'num_mpiprocs_per_machine': 1,
        },
        'max_wallclock_seconds': 120,
    },
    'label': 'aiida_qeq QEQ test',
    'description': 'Test QEQ job submission with the aiida_qeq plugin',
}

builder.structure = CifData(file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'))
builder.parameters = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_PARAM_FILE_NAME))

result = run(builder)
print(result)
