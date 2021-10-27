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
    help="YAML defaults output file location. Default: ./",
    default="./",
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
    # temp fix for lualatex
    template_final = sub("bidi=basic", "bidi=default", template_final)

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

            with open(
                args.output_yaml + "template_default_ulthese.yaml", "w+"
            ) as file_output:
                file_output.write(yamldefault)

        elif maindocstyle == "osa-article":
            with open(
                str(
                    xdg_data_home()
                    / "pandot/defaults/latex_default_osa-article-pandotfiles.yaml"
                )
            ) as file:
                yamldefault = file.read()

            with open(
                args.output_yaml + "template_default_osa-article.yaml", "w+"
            ) as file_output:
                file_output.write(yamldefault)
            # template_final = sub(r"\\usepackage{amsmath,amssymb}", r"", template_final)
            # te

    if (args.output is not None) and (args.output != "T"):
        with open(args.output, "w+") as file_output:
            file_output.write(template_final)
    else:
        pass
    # print(template_final)


if __name__ == "__main__":
    main()
