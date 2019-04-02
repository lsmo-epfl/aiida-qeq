"""
For pytest 
initialise a test database and profile
"""
from __future__ import absolute_import
import tempfile
import shutil
import pytest
import os

from aiida.manage.fixtures import fixture_manager


def get_backend_str():
    """ Return database backend string.
    Reads from 'TEST_AIIDA_BACKEND' environment variable.
    Defaults to django backend.
    """
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    backend_env = os.environ.get('TEST_AIIDA_BACKEND')
    if not backend_env:
        return BACKEND_DJANGO
    elif backend_env in (BACKEND_DJANGO, BACKEND_SQLA):
        return backend_env

    raise ValueError(
        "Unknown backend '{}' read from TEST_AIIDA_BACKEND environment variable"
        .format(backend_env))


@pytest.fixture(scope='session')
def aiida_profile():
    """setup a test profile for the duration of the tests"""
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='function')
def clear_database(aiida_profile):  # pylint: disable=unused-argument
    """clear the database after each test"""
    yield
    aiida_profile.reset_db()


@pytest.fixture(scope='function')
def new_workdir():
    """get a new temporary folder to use as the computer's workdir"""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


@pytest.fixture(scope='function')
def charge_file(aiida_profile):  # pylint: disable=unused-argument
    from aiida.plugins import DataFactory
    import aiida_qeq.data as data
    SinglefileData = DataFactory('singlefile')

    return SinglefileData(
        file=os.path.join(data.DATA_DIR, data.eqeq.DEFAULT_CHARGE_FILE_NAME))


@pytest.fixture(scope='function')
def ionization_file(aiida_profile):  # pylint: disable=unused-argument
    from aiida.plugins import DataFactory
    import aiida_qeq.data as data
    SinglefileData = DataFactory('singlefile')

    return SinglefileData(
        file=os.path.join(data.DATA_DIR,
                          data.eqeq.DEFAULT_IONIZATION_FILE_NAME))


@pytest.fixture(scope='function')
def hkust1_cif(aiida_profile):  # pylint: disable=unused-argument
    from aiida.plugins import DataFactory
    from aiida_qeq.tests import TEST_DIR
    CifData = DataFactory('cif')

    return CifData(
        file=os.path.join(TEST_DIR, 'HKUST1.cif'), parse_policy='lazy')


@pytest.fixture(scope='function')
def qeq_parameters(aiida_profile):  # pylint: disable=unused-argument
    """Sample parameters file for QEQ calculation."""
    from aiida.plugins import DataFactory
    import aiida_qeq.data as data
    SinglefileData = DataFactory('singlefile')

    return SinglefileData(
        file=os.path.join(data.DATA_DIR, data.qeq.DEFAULT_PARAM_FILE_NAME))


@pytest.fixture(scope='function')
def basic_options():
    options = {
        "resources": {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        },
        "max_wallclock_seconds": 120,
    }
    return options
