#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'wheel==0.29.0',
    'urllib3==1.15.1',
    'pyasn1==0.1.9',
    'pyOpenSSL==16.2.0',
    'ndg-httpsclient==0.4.0',
    'colorlog==2.10.0',
    'ujson==5.4.0',
    'validictory==1.1.0',
    'attrdict==2.0.0',
    'decorator==4.1.2',
    'MySQL-python==1.2.5',
    'SQLAlchemy==1.1.13',
    'chardet==3.0.4',
    'falcon==1.2.0',
    'tox==2.3.1',
    'coverage==4.1',
    'Sphinx==1.4.8',
    'unicodecsv==0.14.1',
    'falcon-multipart==0.2.0',
]

setup_requirements = [
    'docutils==0.12',
    'sphinxcontrib-napoleon==0.6.1',
]

test_requirements = [
    'coverage',
    'nose',
]

setup(
    name='pabapi',
    version='0.2.1',
    description=("API backend for a simple address book implemented for the "
                 "PwC interview process."),
    long_description=readme + '\n\n' + history,
    author="Adamos Kyriakou",
    author_email='somada141@gmail.com',
    url='https://github.com/somada141/pabapi',
    packages=find_packages(include=['pabapi']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pabapi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
