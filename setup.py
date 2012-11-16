#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import sys

setup(
    name='fhp',
    version='0.2.0',
    author='500px',
    author_email='help@500px.com',
    description='This is a wrapper for the 500px api.',
    url='https://github.com/500px/PxMagic',
    #packages=find_packages(exclude=['.*','config','tests','examples']),
    packages=find_packages(),
    install_requires=[],
    extras_require={ 'oauth': ["request-oauth"] },
    test_suite='tests',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
   ],
)
