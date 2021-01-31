# Pandotfiles

Dotfiles to create Pandoc project templates and makefile

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


## Todo

- [ ] add .gitignore to pandot project templates.


