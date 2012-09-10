#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
 

setup(
    name='fhp',
    version='0.1.5',
    description='This is a wrapper for the 500px api.',
    author='500px',
    author_email='help@500px.com',
    url='https://github.com/500px/PxMagic',
    packages=find_packages(),
    package_data={"config": ['authentication.json',
                             'test_settings.json']}
)
