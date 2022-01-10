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
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        if ln.startswith('http'):
            continue
        if ln:
            reqs.append(ln)

    return reqs

setup_requirements = [
    'pytest-runner']

test_requirements = [
    'pytest>=3']

setup(
    author='Joeri Hermans, François Rozet, Arnaud Delaunoy',
    author_email='joeri@peinser.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description='Reusable acyclic workflows in Python. Execute code on HPC systems as if you executed them on your laptop!',
    extras_require={
        'dev': _load_requirements('requirements_dev.txt'),
        'examples': _load_requirements('requirements_examples.txt'),
    },
    include_package_data=True,
    install_requires=_load_requirements(),
    keywords='awflow workflow workflow-engine hpc slurm hpc-tools reproducible-science',
    license='BSD license',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='awflow',
    packages=find_packages(include=['awflow', 'awflow.*']),
    project_urls={
        'Documentation': 'https://github.com/JoeriHermans/awflow',
        'Source': 'https://github.com/JoeriHermans/awflow',
        'Tracker': 'https://github.com/JoeriHermans/awflow/issues',
        },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JoeriHermans/awflow',
    version='0.1.0',
    zip_safe=False,
    entry_points = {
        'console_scripts': [],
        },
)
