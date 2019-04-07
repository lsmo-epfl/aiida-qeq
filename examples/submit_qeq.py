# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import aiida_qeq.tests as tests
import aiida_qeq.data.qeq as data
from aiida_qeq.data import DATA_DIR
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

# Prepare input parameters
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')

parameter_file = SinglefileData(
    file=os.path.join(DATA_DIR, data.DEFAULT_PARAM_FILE_NAME))

cif = CifData(
    file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'), parse_policy='lazy')

inputs = {
    # make sure the "qeq" binary is in your PATH
    'code': tests.get_code(entry_point='qeq.qeq'),
    # 'configure': data.QeqParameters()
    'structure': cif,
    'parameters': parameter_file,
    'metadata': {
        'options': {
            "resources": {
                "num_machines": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 120,
        },
        'label': "aiida_qeq QEQ test",
        'description': "Test QEQ job submission with the aiida_qeq plugin",
    },
}

result = run(CalculationFactory('qeq.qeq'), **inputs)
print(result)
