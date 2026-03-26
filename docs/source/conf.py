project = "INFAL 222 – Administration avancée des réseaux étendus"
author = "Paul Imbert"
copyright = "2026, Paul Imbert"
language = "fr"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]

source_suffix = {
    ".md": "markdown",
}

master_doc = "index"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "attrs_inline",
    "attrs_block",
    "substitution",
    "tasklist",
]

mermaid_output_format = "raw"

latex_engine = "xelatex"

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "figure_align": "H",
    "fontpkg": r"""
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Menlo}
""",
    "preamble": r"""
\usepackage{fontspec}
\usepackage{fvextra}
\usepackage{microtype}
\setlength{\headheight}{14pt}
""",
}

latex_documents = [
    ("index", "infal222.tex", project, author, "manual"),
]
