#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for aiida-qeq"""
import json
from setuptools import setup, find_packages

if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically
    with open('setup.json', 'r') as info:
        kwargs = json.load(info)
    setup(packages=find_packages(),
          long_description=open('README.md').read(),
          long_description_content_type='text/markdown',
          **kwargs)
