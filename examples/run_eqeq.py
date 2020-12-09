# -*- coding: utf-8 -*-
"""Submit a test calculation with eqeq.
"""

import os
import click
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida import cmdline

import aiida_qeq.data.eqeq as data
from aiida_qeq.data import DATA_DIR
from . import EXAMPLE_DIR

EqeqCalc = CalculationFactory('qeq.eqeq')
CifData = DataFactory('cif')
SinglefileData = DataFactory('singlefile')
Parameters = DataFactory('qeq.eqeq')


def run_eqeq_hkust1(eqeq_code):  # pylint: disable=
    """Run eqeq calculation on HKUST-1
    """

    builder = EqeqCalc.get_builder()
    builder.code = eqeq_code
    builder.structure = CifData(file=os.path.join(EXAMPLE_DIR, 'HKUST1.cif'))
    builder.parameters = Parameters({'method': 'ewald'})
    builder.charge_data = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_CHARGE_FILE_NAME))
    builder.ionization_data = SinglefileData(file=os.path.join(DATA_DIR, data.DEFAULT_IONIZATION_FILE_NAME))

    result = run(builder)

    cif_content = result['structure_with_charges'].get_content()
    assert 'Cu' in cif_content

    print(result)


@click.command()
@cmdline.utils.decorators.with_dbenv()
@click.option('--eqeq-code', type=cmdline.params.types.CodeParamType())
def cli(eqeq_code):
    """Run eqeq calculation on HKUST-1
    """
    run_eqeq_hkust1(eqeq_code=eqeq_code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
