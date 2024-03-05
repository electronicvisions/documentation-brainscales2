from datetime import date
# -- Project information -----------------------------------------------------

project = 'BrainScaleS-2 Documentation'
copyright = f'{date.today().year}, Electronic Vision(s)'
author = 'Electronic Vision(s)'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx_rtd_theme',
    'sphinxcontrib.jupyter',
    'IPython.sphinxext.ipython_console_highlighting',
    'breathe',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'brainscales2-demos/README.md',
    '_build',
    '_templates',
]

source_suffix = {
    '.rst': 'restructuredtext',
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [
    '_static',
    'brainscales2-demos/_static'
]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
            'css/visions.css',
]


# -- Extension configuration -------------------------------------------------

breathe_projects = {
    # TODO: fix ugly relative paths depending on our waf flow
    'haldls': '../../build/haldls/haldls/doc/xml',
    'lola': '../../build/haldls/lola/doc/xml',
    'stadls': '../../build/haldls/stadls/doc/xml',
    'fisch': '../../build/fisch/doc/xml',
    'hxcomm': '../../build/hxcomm/doc/xml',
    'hxtorch': '../../build/hxtorch/doc/xml',
    'grenade': '../../build/grenade/doc/xml',
    'calix': '../../build/calix/doc/xml',
    'hate': '../../build/hate/doc/xml',
}

# Display todos by setting to True
todo_include_todos = True

autosummary_generate = True
autodoc_default_options = {
    'undoc-members': True,
    'inherited-members': False
}
autosummary_imported_members = True
autosummary_ignore_module_all = False


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
