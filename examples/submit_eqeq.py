# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py

Note: This script assumes you have set up computer and code as in README.md.
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import aiida_qeq.tests as tests
import aiida_qeq.data as data
from aiida.orm import DataFactory

# make sure the "eqeq" binary is in your PATH
code = tests.get_code(entry_point='qeq.eqeq')

# Prepare input parameters
EQeqParameters = DataFactory('qeq.eqeq')
parameters = EQeqParameters({'method': 'ewald'})

SinglefileData = DataFactory('singlefile')
charge_file = SinglefileData(
    file=os.path.join(data.DATA_DIR, data.DEFAULT_CHARGE_FILE_NAME))
ionization_file = SinglefileData(
    file=os.path.join(data.DATA_DIR, data.DEFAULT_IONIZATION_FILE_NAME))

CifData = DataFactory('cif')
cif = CifData(
    file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'), parse_policy='lazy')

# set up calculation
calc = code.new_calc()
calc.label = "aiida_qeq test"
calc.description = "Test job submission with the aiida_qeq plugin"
calc.set_max_wallclock_seconds(60)
calc.set_withmpi(False)
calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

calc.use_parameters(parameters)
calc.use_charge_data(charge_file)
calc.use_ionization_data(ionization_file)
calc.use_structure(cif)

calc.store_all()

calc.submit()
print("submitted calculation; calc=Calculation(uuid='{}') # ID={}".format(
    calc.uuid, calc.dbnode.pk))
