#/usr/bin/env python
import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
setup(
    name="ttpbot",
    version='0.0.1',
    description="Turtable.fm Python bot",
    packages=['ttpbot'],
    install_requires=['ttapi==1.2.0'] + test_requirements,
    scripts  = [
        'bin/ttpbot'
    ],
    zip_safe=False,
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Other Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    )