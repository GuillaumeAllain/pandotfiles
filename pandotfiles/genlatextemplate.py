#!/usr/bin/env python

"""
File: update_pandoc_latex_template.py
Author: Guillaume Allain
Email: guillaum.allain@gmail.com
Github: https://github.com/guillaumeallain
Description: Inject your own template into pandoc's default
"""

import argparse

from re import split, findall, MULTILINE, sub
from codecs import decode
from subprocess import run
from xdg import xdg_data_home


parser = argparse.ArgumentParser(
    description=""" Pandot can init document templates and makefiles for
                        compiling academic documents or presentations.
                    """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-m",
    "--mainfile",
    type=str,
    help="Main file location in which yaml config data is parsed from. Default: None",
    default=None,
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file location. Default: output to terminal (T)",
    default=None,
)

parser.add_argument(
    "-y",
    "--output_yaml",
    type=str,
    help="YAML defaults output file location. Default: ./template_default.yaml",
    default="template_default.yaml",
)

args = parser.parse_args()


def main():

    with open(
        str(xdg_data_home() / "pandot/templates/injection/latex_custom_injection.tex")
    ) as file:
        injection = file.read()

    result = run("/usr/local/bin/pandoc -D latex", shell=True, capture_output=True)

    base_template = decode(result.stdout)

    template_split = split(r"\\begin{document}", (base_template))

    template_final = (
        template_split[0] + injection + "\\begin{document}" + template_split[1]
    )

    if args.mainfile is not None:
        try:
            with open(args.mainfile) as file:
                mainfile = file.read()
        except FileNotFoundError as e:
            raise e
        try:
            maindocstyle = findall(r"(?<=docstyle)\s*:\s*(\S*)", mainfile, MULTILINE)[
                -1
            ]
        except Exception as e:
            maindocstyle = None
        if maindocstyle in ["ulthese", "ulthese-min"]:
            with open(
                str(
                    xdg_data_home()
                    / "pandot/defaults/latex_default_ulthese-pandotfiles.yaml"
                )
            ) as file:
                yamldefault = file.read()

            try:
                uldiploma = findall(r"(?<=uldiploma)\s*:\s*(\S*)", mainfile, MULTILINE)[
                    -1
                ]
                diploma_list = [
                    "LLD",
                    "DMus",
                    "DPsy",
                    "DThP",
                    "PhD",
                    "MATDR",
                    "MArch",
                    "MA",
                    "LLM",
                    "MErg",
                    "MMus",
                    "MPht",
                    "MSc",
                    "MScGeogr",
                    "MServSoc",
                    "MPsEd",
                ]
                if uldiploma not in diploma_list:
                    raise ValueError("Wrong uldiploma Value in YAML block")
            except Exception as e:
                uldiploma = "PhD"

            yamldefault = sub("ULDIPLOMA", uldiploma, yamldefault)

            try:
                file_output = open(args.output_yaml, "x")
            except FileExistsError:
                file_output = open(args.output_yaml, "w")
            file_output.write(yamldefault)
            file_output.close()

    if (args.output is not None) and (args.output != "T"):
        try:
            file_output = open(args.output, "x")
        except FileExistsError:
            file_output = open(args.output, "w")
        file_output.write(template_final)
        file_output.close()
    else:
        pass
    # print(template_final)


if __name__ == "__main__":
    main()
