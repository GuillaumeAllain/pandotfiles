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

    with open(str("../.pandot/pandoc/injection/latex_custom_injection.tex")) as file:
        injection = file.read()

    result = run("pandoc -D latex", shell=True, capture_output=True)

    base_template = decode(result.stdout)

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
                str("../.pandot/latex/defaults/latex_default_ulthese-pandotfiles.yaml")
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

        elif maindocstyle in ["spie", "osa-article", "spieman"]:
            #     with open(str("../.pandot/pandoc/injection/latex_custom_injection_spie.tex")) as file:
            #         injection = file.read()
            #     with open(
            #         str(
            #             "../.pandot/latex/defaults/latex_default_spie-pandotfiles.yaml"
            #         )
            #     ) as file:
            #         yamldefault = file.read()
            #     with open(
            #         args.output_yaml + "template_default_spie.yaml", "w+"
            #     ) as file_output:
            #         file_output.write(yamldefault)
            # elif maindocstyle == "osa-article":
            with open(
                str(
                    f"../.pandot/pandoc/injection/latex_custom_injection_{maindocstyle}.tex"
                )
            ) as file:
                injection = file.read()
            with open(
                str(
                    f"../.pandot/latex/defaults/latex_default_{maindocstyle}-pandotfiles.yaml"
                )
            ) as file:
                yamldefault = file.read()

            with open(
                args.output_yaml + f"template_default_{maindocstyle}.yaml", "w+"
            ) as file_output:
                file_output.write(yamldefault)
            # template_final = sub(r"\\usepackage{amsmath,amssymb}", r"", template_final)
            base_template = [
                r"\documentclass[$if(fontsize)$",
                r"$fontsize$",
                "$endif$]{$documentclass$}",
                r"",
                r"\usepackage{ifthen}" r"\begin{document}",
                r"$if(has-frontmatter)$",
                r"\frontmatter",
                r"$endif$",
                r"$if(title)$",
                r"\maketitle",
                r"$endif$",
                r"$if(abstract)$",
                r"\begin{abstract}",
                r"$abstract$",
                r"\end{abstract}",
                r"$endif$",
                r"$if(keywords)$" r"\keywords{$for(keywords)$$keywords$$sep$,$endfor$}",
                r"$endif$"
                r"",
                r"$if(spie_main_author)$"
                r"{\noindent \footnotesize\textbf{*}$spie_main_author$}",
                r"$endif$",
                r"$for(include-before)$",
                r"$include-before$",
                r"$endfor$",
                r"$if(toc)$",
                r"$if(toc-title)$",
                r"\renewcommand*\contentsname{$toc-title$}",
                r"$endif$",
                r"$if(beamer)$",
                r"\begin{frame}[allowframebreaks]",
                r"$if(toc-title)$",
                r"\frametitle{$toc-title$}",
                r"$endif$",
                r"\tableofcontents[hideallsubsections]",
                r"\end{frame}",
                r"$else$",
                r"{",
                r"$if(colorlinks)$",
                r"\hypersetup{linkcolor=$if(toccolor)$$toccolor$$else$$endif$}",
                r"$endif$",
                r"\setcounter{tocdepth}{$toc-depth$}",
                r"\tableofcontents",
                r"}",
                r"$endif$",
                r"$endif$",
                r"$if(lof)$",
                r"\listoffigures",
                r"$endif$",
                r"$if(lot)$",
                r"\listoftables",
                r"$endif$",
                r"$if(linestretch)$",
                r"\setstretch{$linestretch$}",
                r"$endif$",
                r"$if(has-frontmatter)$",
                r"\mainmatter",
                r"$endif$",
                r"$body$",
                r"$if(has-frontmatter)$",
                r"\backmatter",
                r"$endif$",
                r"$if(bibliography)$",
                r"\bibliography{$for(bibliography)$$bibliography$$sep$,$endfor$}",
                r"$endif$",
                r"$if(biography)$" r"\vspace{1ex}",
                r"\vspace{2ex}\noindent$biography$",
                r"",
                r"\noindent Biographies and photographs of the other authors are not available.",
                r"$endif$" r"$for(include-after)$",
                r"$include-after$",
                r"",
                r"$endfor$",
                r"\end{document}",
            ]
            base_template = "\n".join(base_template)
        elif maindocstyle is not None:
            with open(
                str("../.pandot/pandoc/injection/latex_custom_injection.tex")
            ) as file:
                injection = file.read()
            with open(
                str(f"../.pandot/latex/docstyle_latex/docstyle-{maindocstyle}.tex")
            ) as file:
                injection += file.read()

    template_split = split(r"\\begin{document}", (base_template))

    template_final = (
        template_split[0] + injection + r"\begin{document}" + template_split[1]
    )

    # temp fix for lualatex
    template_final = sub("bidi=basic", "bidi=default", template_final)

    if (args.output is not None) and (args.output != "T"):
        with open(args.output, "w+") as file_output:
            file_output.write(template_final)
    else:
        pass


if __name__ == "__main__":
    main()
