# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import setuptools
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QKDSimkit",
    version="0.0.6",
    license= "MIT License",
    author="Alberto Di Meglio and Gabriele Morello",
    author_email="gabriele.morello@cern.ch",
    description="Quantum Key Distribution simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CERN/Quantumacy/tree/main/QKDSimkit",
    project_urls={
        "Bug Tracker": "https://github.com/CERN/Quantumacy/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    packages=['QKDSimkit', 'QKDSimkit.core'],
    python_requires=">=3.8",
    development_status = "3 - Alpha",
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'QKDSimkit = QKDSimkit.cli:cli',
        ],
    },
)
