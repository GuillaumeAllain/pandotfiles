import argparse
from os import makedirs
import warnings

from pathlib import Path
from re import sub

#
from xdg import xdg_data_home

from pandotfiles.util.parser import tikzyamlparse
from pandotfiles.util.makefile_mod import pdfmakefilemod, tikzmakefilemod

parser = argparse.ArgumentParser(
    description=""" Pandot can init document templates and makefiles for
                           compiling academic documents or presentations.
                       """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("command", choices=["init", "newfile"])

parser.add_argument("option", type=str)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file location. Default: output to terminal (T)",
    default="Makefile",
)

args = parser.parse_args()

VALIDOPTIONINIT = ["pdf", "tikz", "reactjs", "python", "codev"]
VALIDOPTIONNEWFILE = ["python", "tikz"]


def main():

    if args.command == "init":

        option_list = args.option.split("+")
        FIGURETARGETS = ""
        DATATARGETS = ""
        TARGETS = ""
        MAKEFILE_CONTENT = ""
        CLEAN = ""
        OPEN = ""
        for option in option_list:

            if option not in VALIDOPTIONINIT:

                raise ValueError(
                    option + " is not a valid document output:\n" + str(VALIDOPTIONINIT)
                )

            elif option == "reactjs":

                raise NotImplementedError(option + " is not yet implemented")

            elif option == "pdf":

                builddir = "build/pdf"
                srcdir = "doc"
                makedirs("doc", exist_ok=True)
                Path("doc/main.md").touch()
                with open("doc/Makefile", "w+") as file_output:
                    with open(
                        str(xdg_data_home())
                        + "/pandot/templates/makefile_template/pdf_makefile"
                    ) as file:
                        makefile = file.read()
                    makefile = pdfmakefilemod(
                        makefile, "log", "../" + builddir, ".", "main.md"
                    )

                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(xdg_data_home()) + "/pandot/gitignore/doc.gitignore"
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite gitignore file")

                sources = (
                    "$(wildcard doc/*.md) "
                    + " $(wildcard doc/*.bib) "
                    + "$(FIGURETARGETS)"
                )
                MAKEFILE_CONTENT += (
                    builddir + "/main.pdf: " + sources + "\n\t$(MAKE) -C doc \n"
                )
                CLEAN += "\t$(MAKE) -C doc clean\n"
                TARGETS += "TARGETS += " + builddir + "/main.pdf\n"
                OPEN += "\topen " + builddir + "/main.pdf\n"

            elif option == "tikz":

                srcdir = "src/tikz"
                makedirs(srcdir, exist_ok=True)
                # copy yaml defaults
                try:
                    with open(srcdir + "/auto_tikz.yaml", "x") as file_output:
                        with open(
                            str(xdg_data_home())
                            + "/pandot/defaults/auto_tikz_default-pandotfiles.yaml"
                        ) as file:
                            autoyaml = file.read()
                        file_output.write(autoyaml)
                except FileExistsError:
                    warnings.warn("Using existing auto_tikz.yaml config file")

                yaml_config = tikzyamlparse(srcdir + "/auto_tikz.yaml")
                logdir = yaml_config["log_folder"]
                tikzfiles = yaml_config["files_makestring"]
                builddir = "build/tikz"

                with open(srcdir + "/Makefile", "w+") as file_output:
                    with open(
                        str(xdg_data_home())
                        + "/pandot/templates/makefile_template/auto_tikz_makefile"
                    ) as file:
                        makefile = file.read()

                    makefile = tikzmakefilemod(
                        makefile,
                        "auto_tikz.yaml",
                        "../../" + builddir,
                        logdir,
                        tikzfiles,
                    )
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(xdg_data_home()) + "/pandot/gitignore/tikz.gitignore"
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Tikz init: Won't overwrite gitignore file")

                sources = "$(wildcard src/tikz/*.tikz)"
                MAKEFILE_CONTENT += (
                    builddir
                    + "/tikz_stamp:"
                    + sources
                    + " \n\t$(MAKE) -C "
                    + srcdir
                    + " \n"
                )
                TARGETS += "TARGETS += " + builddir + "/tikz_stamp\n"
                FIGURETARGETS += "FIGURETARGETS += " + builddir + "/tikz_stamp\n"
                CLEAN += "\t$(MAKE) -C " + srcdir + " clean\n"

            elif option == "python":

                srcdir = "src/python"
                builddir = "build/python"
                makedirs(srcdir, exist_ok=True)
                with open(
                    str(xdg_data_home())
                    + "/pandot/templates/makefile_template/python_makefile"
                ) as file:
                    makefile = file.read()
                makefile = sub(
                    r"(builddir\s=)(.*)", "\\1 ../../" + str(builddir), makefile
                )
                with open(srcdir + "/Makefile", "w+") as file_output:
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(xdg_data_home()) + "/pandot/gitignore/python.gitignore"
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Python init: Won't overwrite gitignore file")

                try:
                    with open(srcdir + "/environment.yaml", "x") as file_output:
                        with open(
                            str(xdg_data_home()) + "/pandot/defaults/environment.yaml"
                        ) as file:
                            environment = file.read()
                        file_output.write(environment)
                except FileExistsError:
                    warnings.warn("Python init: Won't overwrite environment file")

                sources = "$(wildcard src/python/*.py) $(DATATARGETS)"
                MAKEFILE_CONTENT += (
                    builddir
                    + "/python_stamp: "
                    + sources
                    + " \n\t$(MAKE) -C "
                    + srcdir
                    + "\n"
                )

                TARGETS += "TARGETS += " + builddir + "/python_stamp\n"
                FIGURETARGETS += "FIGURETARGETS += " + builddir + "/python_stamp\n"
                CLEAN += "\t$(MAKE) -C " + srcdir + " clean\n"

            elif option == "codev":

                srcdir = "src/codev"
                builddir = "build/codev"
                outputdir = "output"
                makedirs(srcdir, exist_ok=True)
                # copy yaml defaults
                try:
                    with open(srcdir + "/codev_remote.yaml", "x") as file_output:
                        with open(
                            str(xdg_data_home())
                            + "/pandot/defaults/codev_remote_default-pandotfiles.yaml"
                        ) as file:
                            codev_remote = file.read()
                        file_output.write(codev_remote)
                except FileExistsError:
                    warnings.warn("Using existing codev_remote.yaml config file")

                with open(srcdir + "/Makefile", "w+") as file_output:
                    with open(
                        str(xdg_data_home())
                        + "/pandot/templates/makefile_template/codev_makefile"
                    ) as file:
                        makefile = file.read()
                    makefile = sub(
                        r"(builddir\s=)(.*)", "\\1 ../../" + str(builddir), makefile
                    )
                    makefile = sub(
                        r"(outputdir\s=)(.*)", "\\1 " + str(outputdir), makefile
                    )

                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(xdg_data_home()) + "/pandot/gitignore/codev.gitignore"
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Codev init: Won't overwrite gitignore file")

                sources = "$(wildcard src/codev/*/*.seq) $(wildcard src/codev/*.seq)"
                MAKEFILE_CONTENT += (
                    builddir
                    + "/codev_stamp:"
                    + sources
                    + " \n\t$(MAKE) -C "
                    + srcdir
                    + "\n"
                )
                TARGETS += "TARGETS += " + builddir + "/codev_stamp\n"
                DATATARGETS += "DATATARGETS+= " + builddir + "/codev_stamp\n"
                FIGURETARGETS += "FIGURETARGETS += " + builddir + "/codev_stamp\n"
                CLEAN += "\t$(MAKE) -C " + srcdir + " clean\n"

        projectmakefile = (
            TARGETS
            + FIGURETARGETS
            + DATATARGETS
            + "export TARGETS\nexport FIGURETARGETS\nexport DATATARGETS"
            + "\n\n.PHONY: all clean open\n\nall: $(TARGETS)\n\n"
            + "\n\nclean:\n"
            + CLEAN
            + "\t-@ rm -r build/"
            + "\n\nopen:\n"
            + OPEN
            + MAKEFILE_CONTENT
        )
        if (args.output is not None) and (args.output != "T"):

            with open(args.output, "w+") as file_output:
                file_output.write(projectmakefile)

        else:
            print(projectmakefile)

        try:
            with open(".gitignore", "x") as file_output:
                with open(
                    str(xdg_data_home()) + "/pandot/gitignore/project.gitignore"
                ) as file:
                    gitignore = file.read()
                file_output.write(gitignore)
        except FileExistsError:
            warnings.warn("Project init: Won't overwrite gitignore file")

    elif args.command == "newfile":

        if args.option not in VALIDOPTIONNEWFILE:
            raise ValueError(
                option + " is not a valid document output:\n" + str(VALIDOPTIONNEWFILE)
            )

        elif args.option == "python":
            print("Enter filename (without extension)")
            filename = input()
            try:
                with open(filename + ".py", "x") as file_output:
                    file_output.write(
                        "#!/usr/bin/env conda run -p " "../../build/python/env ipython"
                    )
                    file_output.close()
            except FileExistsError:
                raise FileExistsError("Won't overwrite file if it already exists")

        elif args.option == "tikz":
            print("Enter filename (without extension)")
            filename = input()
            try:
                with open(filename + ".tikz", "x") as file_output:
                    file_output.write("\\begin{tikzpicture}\n\\end{tikzpicture}")
                    file_output.close()
            except FileExistsError:
                raise FileExistsError("Won't overwrite file if it already exists")


if __name__ == "__main__":
    main()
