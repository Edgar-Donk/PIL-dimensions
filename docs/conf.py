
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('./scripts/')) # sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'PIL Dimensions'
copyright = '2021, Edgar Donk'
author = 'Edgar Donk'

# The full version, including alpha/beta/rc tags
release = '0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [#'matplotlib.sphinxext.only_directives',
    #'matplotlib.sphinxext.plot_directive',
    "sphinx.ext.autodoc",
    'sphinx.ext.napoleon',
    "sphinx.ext.autosummary",
    # "numpydoc",
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    #'sphinx_toolbox.confval',
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_theme_options = {
  "show_prev_next": True,
  # search bar options are ‘navbar’ and ‘sidebar’.
  "search_bar_position": "sidebar",
  #  "use_edit_page_button": True,
}

html_sidebars = {
    "contributing": ["sidebar-search-bs.html", "custom-template.html"],
    "changelog": [],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# option for show/hide code
def setup(app):
    app.add_css_file('custom.css')

html_theme_options = {
   "logo": {
      "text": "a whole new dimension",
      "image_light": 'bigbenc.png',
      "image_dark": "bigbencneon.png",
   }
}

#html_logo = '_static/ben_dim.png'


html_favicon = '_static/ben1.ico'