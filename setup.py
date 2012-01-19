#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
 
setup(
    name='fivehundred-python-sdk',
    version='0.1',
    description='This is a wrapper for the 500px api.',
    author='arthurnn',
    url='https://github.com/arthurnn/fivehundred-python',
    package_dir={'': 'src'},
    py_modules=[
        'fivehundred',
    ],
)