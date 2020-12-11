# -*- coding: utf-8 -*-
"""Submit a test calculation with qeq.
"""

import os
import click
from aiida.plugins import DataFactory, CalculationFactory
from aiida import engine
from aiida import cmdline

import aiida_qeq.data.qeq as data
from aiida_qeq.data import DATA_DIR
from . import EXAMPLE_DIR

QeqCalc = CalculationFactory('qeq.qeq')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
Parameters = DataFactory('qeq.qeq')


def run_qeq_hkust1(qeq_code):
    """Run qeq calculation on HKUST-1
    """

    builder = QeqCalc.get_builder()

    builder = QeqCalc.get_builder()
    builder.code = qeq_code
    builder.structure = CifData(file=os.path.join(EXAMPLE_DIR, 'HKUST1.cif'))
    builder.parameters = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_PARAM_FILE_NAME))

    result, node = engine.run_get_node(builder)

    assert node.is_finished_ok, result
    print(result)
    cif_content = result['structure_with_charges'].get_content()
    assert 'Cu' in cif_content


@click.command()
@cmdline.utils.decorators.with_dbenv()
@click.option('--qeq-code', type=cmdline.params.types.CodeParamType())
def cli(qeq_code):
    """Run qeq calculation on HKUST-1
    """
    run_qeq_hkust1(qeq_code=qeq_code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
