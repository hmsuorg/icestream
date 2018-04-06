#!/usr/bin/env python3
from setuptools import setup, find_packages

_dev = {'develop': ["pylint", "coverage", ]}

def get_version():
    """get_version"""
    with open('VERSION') as version:
        return version.read()

setup(
    name='icestream',
    version=get_version(),
    description='This script provide us an easy way to stream HMSU radio shows to icecast server',
    author='Dimitar Dimitrov',
    author_email='targy@hmsu.org',
    url='https://github.com/hmsuorg/icestream',
    packages=find_packages(),
    # test_suite='hctlp.tests',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - 5',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'click',
    ],

    scripts=['icestream.py'],
    extras_require=_dev
)
