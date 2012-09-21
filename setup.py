#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import sysconfig
import shutil
import os
import sys
DISTUTILS_DEBUG = True
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

fhp_dir = 'fhp'
data_files = []
packages = []
root_dir = os.path.dirname(__file__)
lib_dir = sysconfig.get_paths()['purelib']
lib_dir = os.path.join(lib_dir, fhp_dir)

if root_dir != '':
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(fhp_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        for f in filenames:
            record = (os.path.join(root_dir, fhp_dir, 'config', f),f)
            data_files.append(record)
print data_files
config_dir = os.path.join(lib_dir, "config")
try:
    os.makedirs(config_dir, 0777)
except OSError:
    pass

setup(
    name='fhp',
    version='0.2.0',
    description='This is a wrapper for the 500px api.',
    author='500px',
    author_email='help@500px.com',
    url='https://github.com/500px/PxMagic',
    packages=packages,
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

# I know I shouldn't have to do this, but no files were 
# copying in certain debian situations, so I finally just gave up.
# If you fix it by doing it the "right" way, be prepared for it not to 
# work when I test it.
for data_file in data_files:
    with open(data_file[0]) as f:
        file_contents = f.read()
        write_filename = os.path.join(config_dir, data_file[1])
        with open(write_filename, 'w') as write_f:
            print "writing", write_filename
            write_f.write(file_contents)


