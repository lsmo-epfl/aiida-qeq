# -*- coding: utf-8 -*-
"""Tests for qeq calculation plugin
"""

import os
from aiida.plugins import DataFactory, CalculationFactory
from aiida import engine

import aiida_qeq.data.qeq as data
from aiida_qeq.data import DATA_DIR
from tests import DATA_DIR as TEST_DATA_DIR

QeqCalc = CalculationFactory('qeq.qeq')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
Parameters = DataFactory('qeq.eqeq')


def test_qeq_failure(qeq_code):
    """Run qeq calculation on a structure where the SCF does not converge.
    """

    builder = QeqCalc.get_builder()

    builder = QeqCalc.get_builder()
    builder.code = qeq_code
    builder.structure = CifData(file=os.path.join(TEST_DATA_DIR, '08010N2_DDEC.cif'))
    builder.parameters = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_PARAM_FILE_NAME))

    _result, node = engine.run_get_node(builder)

    assert not node.is_finished_ok
    assert node.exit_status == 801
