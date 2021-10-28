# Pandotfiles

Dotfiles to create Pandoc project templates and makefile

## Requirements

For PDF:

    - [pandoc](https://github.com/jgm/pandoc)
    - [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)
    - [mermaid-filter](https://github.com/raghur/mermaid-filter)

For CODEV:

    - Unreleased library CODEV-TOOLS

For Python:

    - [conda](https://github.com/conda/conda)

Some python packages are required for the scripts, but these requirements are handled with pip.

## Installation

Clone and install with 

```console
foo@bar:pandotfiles$ pip install .
```
ou

```console
foo@bar:pandotfiles$ pip install git+https://github.com/GuillaumeAllain/pandotfiles.git
```

## How to use

Intended use is with the high level template script "pandot". Initialize and new (or existing) project with:

```console
foo@bar: pandot init pdf+tikz+python -o Makefile
```

The script will create all necessary makefiles and directories to compile all the different sources required by the document.

A docker image is also available at `guillaumeallain/pandotfiles`


## Todo

- [x] add .gitignore to pandot project templates.
- [ ] Add ReactJS support


