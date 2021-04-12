#import recommonmark
#from recommonmark.transform import AutoStructify
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'pytep'
copyright = '2021, Christopher Reinartz, Technical University of Denmark'
author = 'Christopher Reinartz, Thomas Thuesen Enevoldsen'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.napoleon',
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.coverage'
#        'recommonmark'
]

source_suffix = {
    '.rst': 'restructuredtext'
#    '.md': 'markdown'
}
# autodoc_mock_imports = ["matlab"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# sort in same order as in source code
autodoc_member_order = 'bysource'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..','..'))

github_doc_root = 'https://github.com/ChristopherReinartz/pytep/tree/master/docs'
sys.path.insert(0, os.path.abspath(os.path.join(github_doc_root, '..','..')))

#def setup(app):
#    app.add_config_value('recommonmark_config', {
#            'url_resolver': lambda url: github_doc_root + url,
#            'auto_toc_tree_section': 'Contents',
#            }, True)
#    app.add_transform(AutoStructify)
