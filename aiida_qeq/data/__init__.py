# -*- coding: utf-8 -*-
"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from __future__ import absolute_import
import os

from . import qeq, eqeq

DATA_DIR = os.path.dirname(os.path.realpath(__file__))

__all__ = ('qeq', 'eqeq', 'DATA_DIR')
