#!/usr/bin/env python
#-*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pagseguro-python',
    version='0.34',
    description='PagSeguro API v.2 client library ',
    author='Ricardo Silva',
    author_email='rsas79@gmail.com',
    url='https://github.com/ricardosasilva/pagseguro-python',
    packages=find_packages(),
    install_requires=[
        'voluptuous>=0.8.3',
        'requests>=2.0.1',
        'xmltodict>=0.8.3',
        'python-dateutil>=2.2'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ]
)
