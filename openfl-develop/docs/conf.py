"""Docs configuration module."""

# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------

PRODUCT_VERSION = 'Intel'

if PRODUCT_VERSION == 'Intel':
    project = 'OpenFL'
    copyright = f'{datetime.now().year}, Intel'  # NOQA
    author = 'Intel Corporation'
    version = f'{datetime.now().year}.{datetime.now().month}'
    release = version
    master_doc = 'index'

    # Global variables for rST
    rst_prolog = '''
    .. |productName| replace:: OpenFL
    .. |productZip| replace:: openfl.zip
    .. |productDir| replace:: openfl
    .. |productWheel| replace:: openfl
    '''
else:
    project = 'Open Federated Learning'
    author = 'FeTS'
    master_doc = 'index'
    version = f'{datetime.now().year}.{datetime.now().month}'
    release = version

    # Global variables for rST
    rst_prolog = '''
    .. |productName| replace:: Open Federated Learning
    .. |productZip| replace:: OpenFederatedLearning.zip
    .. |productDir| replace:: OpenFederatedLearning
    .. |productWheel| replace:: openfl
    .. _Makefile: https://github.com/IntelLabs/OpenFederatedLearning/blob/master/Makefile
    '''

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
    'sphinx-prompt',
    'sphinx_substitution_extensions',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.kroki'
]

napoleon_google_docstring = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'tutorials/*', 'graveyard/*']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autosectionlabel_prefix_document = True
