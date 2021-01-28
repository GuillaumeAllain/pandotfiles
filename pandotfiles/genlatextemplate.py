#!/usr/bin/env python

"""
File: update_pandoc_latex_template.py
Author: Guillaume Allain
Email: guillaum.allain@gmail.com
Github: https://github.com/guillaumeallain
Description: Inject your own template into pandoc's default
"""

import re
from codecs import decode
from subprocess import run
from xdg import xdg_data_home

def main():

    with open(str(xdg_data_home()/"pandoc/templates/latex_custom_injection.tex")) as file:
        injection = file.read()

    result = run('/usr/local/bin/pandoc -D latex',shell=True,capture_output=True)

    base_template = decode(result.stdout)

    template_split = re.split(r'\\begin{document}',(base_template))

    template_final = template_split[0]+injection+'\\begin{document}'+template_split[1]

    print(template_final)

if __name__ == "__main__":
    main()
