# -*- coding: utf-8 -*-
"""
For pytest
initialise a test database and profile
"""
# pylint: disable=missing-function-docstring
import pytest

from aiida.plugins import DataFactory
import aiida_qeq.data as data
from tests import TEST_DIR, DATA_DIR

pytest_plugins = ['aiida.manage.tests.pytest_fixtures', 'aiida_testing.mock_code']  # pylint: disable=invalid-name

SinglefileData = DataFactory('singlefile')
CifData = DataFactory('cif')


@pytest.fixture(scope='function')
def hkust1_cif(aiida_profile):  # pylint: disable=unused-argument
    return CifData(file=str(TEST_DIR / 'HKUST1.cif'), parse_policy='lazy')


@pytest.fixture(scope='function')
def MgO_cif(aiida_profile):  # pylint: disable=unused-argument
    return CifData(file=str(TEST_DIR / 'MgO.cif'), parse_policy='lazy')


@pytest.fixture(scope='function')
def qeq_parameters(aiida_profile):  # pylint: disable=unused-argument
    """Sample parameters file for QEQ calculation."""
    return SinglefileData(file=str(data.DATA_DIR / data.qeq.DEFAULT_PARAM_FILE_NAME))


@pytest.fixture(scope='function')
def qeq_code(mock_code_factory):
    """Create mocked "qeq" code."""
    return mock_code_factory(
        label='egulp-2d61ca9',
        data_dir_abspath=DATA_DIR,
        entry_point='qeq.qeq',
        # files *not* to copy into the data directory
        ignore_paths=(
            '_aiidasubmit.sh',
            'GMP.param',
            'charges.xyz',
            'configure.inpu',
        ))


@pytest.fixture(scope='function')
def eqeq_code(mock_code_factory):
    """Create mocked "eqeq" code."""
    return mock_code_factory(
        label='eqeq-6490320',
        data_dir_abspath=DATA_DIR,
        entry_point='qeq.eqeq',
        # files *not* to copy into the data directory
        ignore_paths=('_aiidasubmit.sh', '*.car', '*.mol', '*.pdb', 'chargecenters.dat', 'ionizationdata.dat'))
