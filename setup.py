#!/usr/bin/env python

"""The setup script."""

import glob
import os
import shutil

from setuptools import setup, find_packages



with open('README.md') as readme_file:
    readme = readme_file.read()

def _load_requirements(file_name="requirements.txt", comment_char='#'):
    with open(file_name, 'r') as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        # filer all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith('http'):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)

    return reqs

setup_requirements = [
    'pytest-runner']

test_requirements = [
    'pytest>=3']

# Install Hypothesis
setup(
    author='Joeri Hermans',
    author_email='joeri@peinser.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ],
    description='Pythonic reusable acyclic workflows. Execute code on HPC systems as if you executed them on your laptop!',
    install_requires=_load_requirements(),
    license='BSD license',
    long_description=readme,
    include_package_data=True,
    keywords='awflow',
    name='awflow',
    packages=find_packages(include=['awflow', 'awflow.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JoeriHermans/awflow',
    version='0.0.1',
    zip_safe=False,
)
