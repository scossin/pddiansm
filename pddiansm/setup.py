# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pddiansm',
    version='0.1.0',
    description='A package to detect potential drug drug interactions (PDDIs) according to the French National Agency for the Medicines and Health Products Safety guidelines',
    long_description=readme,
    author='Sebastien Cossin',
    url='https://github.com/scossin/pddiansm',
    license=license,
    packages=find_packages(exclude=('tests'))
)