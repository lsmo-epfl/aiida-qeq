# -*- coding: utf-8 -*-
"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'

from pathlib import Path
from . import qeq, eqeq

DATA_DIR = Path(__file__).resolve().parent

__all__ = ('qeq', 'eqeq', 'DATA_DIR')
