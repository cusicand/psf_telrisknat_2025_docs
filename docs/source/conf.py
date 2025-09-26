# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PSF TelRiskNat 2025'
copyright = '2025, PSF TelRiskNat Optical team (D. Cusicanqui, P. Lacroix & R. Basantes)'
author = 'Diego Cusicanqui'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_immaterial",
    'myst_parser',
    'sphinx.ext.duration',
    "sphinx_pdf_generate",
    'sphinxcontrib.bibtex',
    'sphinx_togglebutton',
    # 'sphinx_immaterial.kbd_keys',
    'sphinxcontrib.programoutput',
    'sphinx.ext.mathjax',
]

# sphinx_immaterial_override_builtin_admonitions = False
# sphinx_immaterial_generate_extra_admonitions = False
# sphinx_immaterial_override_version_directives = False

bibtex_bibfiles = ['references.bib']
# APA 7 via CSL (requires sphinxcontrib-bibtex >=2.6 and citeproc-py installed)
# Map custom style key 'apa7' to the CSL file we placed under _static.
# bibtex_csl_styles = {
#     "apa7": "_static/apa.csl",
# }
# Use author-year in-text citations.
# bibtex_reference_style = "author_year"
# Use numeric labels ( [1], [2], ... )
bibtex_reference_style = "label"

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

numfig = True

math_number_all = True

templates_path = ['_templates']
exclude_patterns = []

google_fonts = [
    "Roboto",
    "Roboto Mono"
]

# Multiple languages extension
locale_dirs = ['locale/']
gettext_compact = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial'
# html_theme = 'piccolo_theme'
html_static_path = ['_static']

# material theme options (see theme.conf for more information)
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://jbms.github.io/sphinx-immaterial/",
    "repo_url": "https://github.com/jbms/sphinx-immaterial/",
    "repo_name": "PSF TelRiskNat 2025",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "navigation.tabs.sticky",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.footer",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "search.suggest",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "content.code.copy",
        # "content.action.edit",
        # "content.action.view",
        "content.tooltips",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme)",
            "toggle": {
                "icon": "material/brightness-auto",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "dark-blue",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to system preference",
            },
        },
    ],
    # # BEGIN: version_dropdown
    # "version_dropdown": True,
    # "version_info": [
    #     {
    #         "version": "https://sphinx-immaterial.rtfd.io",
    #         "title": "ReadTheDocs",
    #         "aliases": [],
    #     },
    #     {
    #         "version": "https://jbms.github.io/sphinx-immaterial",
    #         "title": "Github Pages",
    #         "aliases": [],
    #     },
    # ],
    # # END: version_dropdown
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/jbms/sphinx-immaterial",
            "name": "Source on github.com",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/sphinx-immaterial/",
        },
    ],
    # END: social icons
}
