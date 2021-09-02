# -*- coding: utf-8 -*-
import os
from typing import List

# https://github.com/pypa/setuptools/issues/1806#issuecomment-678377209
def find_files_in_folder(top: str) -> List[str]:
    data_files = []
    for root, _, files in os.walk(top):
        folder = root.split(os.path.sep, 1)[-1] # remove 'top'
        for f in files:
            if os.path.sep in root:
                f = os.path.join(folder, f)
            data_files.append(f)
    return data_files

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pddiansm',
    version='0.2.0',
    description='A package to detect potential drug drug interactions (PDDIs) according to the French National Agency for the Medicines and Health Products Safety (ANSM) guidelines',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Sebastien Cossin',
    author_email="cossin.sebastien@gmail.com",
    url='https://github.com/scossin/pddiansm',
    license="MIT",
    packages=find_packages(exclude=('tests')),
    package_data={'pddiansm': find_files_in_folder('pddiansm/data')},
    include_package_data=True,
    install_requires=required
)
