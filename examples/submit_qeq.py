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
from aiida.orm import DataFactory

# make sure the "eqeq" binary is in your PATH
code = tests.get_code(entry_point='qeq.qeq')

# Prepare input parameters
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')

configure = data.QeqParameters()

parameter_file = SinglefileData(
    file=os.path.join(DATA_DIR, data.DEFAULT_PARAM_FILE_NAME))

cif = CifData(
    file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'), parse_policy='lazy')

# set up calculation
calc = code.new_calc()
calc.label = "aiida_qeq Qeq test"
calc.description = "Test Qeq job submission with the aiida_qeq plugin"
calc.set_max_wallclock_seconds(10 * 60)
calc.set_withmpi(False)
calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

calc.use_parameters(parameter_file)
calc.use_structure(cif)
calc.use_configure(configure)

calc.store_all()

calc.submit()
print("submitted calculation; calc=Calculation(uuid='{}') # ID={}".format(
    calc.uuid, calc.dbnode.pk))
