#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
 

setup(
    name='fhp',
    version='0.1.1',
    description='This is a wrapper for the 500px api.',
    author='arthurnn',
    url='https://github.com/zachaysan/fivehundred-python',
    packages=find_packages(),
    package_data={"config": ['authentication.json',
                             'test_settings.json']}

)
