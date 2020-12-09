# -*- coding: utf-8 -*-
""" tests for the plugin

Use the aiida.utils.fixtures.PluginTestCase class for convenient
testing that does not pollute your profiles/databases.
"""

# Helper functions for tests
import os
import tempfile

from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
DATA_DIR = TEST_DIR / 'data'

TEST_COMPUTER = 'localhost-test'
