## Auto Tikz

This is a simple python script used to generate a LaTeX file that may be used to pre-compute all tikz file in a directory. 

Uses YAML configuration file to pass general LaTeX options, tikzlibraries and files locations.

## Installation

Install with
```console
foo@bar:auto-tikz$ pip install .
```
ou

```console
foo@bar:auto-tikz$ pip install git+https://github.com/GuillaumeAllain/auto-tikz.git
```

## How to use

auto_tikz -y {YAML_FILE_LOCATION} -o {OUTPUT_FILE_NAME}

By default will output to terminal.

Default YAML file location is ./auto_tikz.tex

## Todo

- [ ] Copy all PDF to a chosen directory in YAML file


