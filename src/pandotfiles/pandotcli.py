import argparse
from os import makedirs
from shutil import copytree, copy, ignore_patterns
from subprocess import run, PIPE
import warnings
import datetime

from pathlib import Path

from pandotfiles.util.parser import tikzyamlparse

parser = argparse.ArgumentParser(
    description=""" Pandot can init document templates and makefiles for
                           compiling academic documents or presentations.
                       """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("command", choices=["init", "newfile"])

parser.add_argument("option", type=str, default="")

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file location. Default: output to terminal (T)",
    default="Makefile",
)

args = parser.parse_args()

VALIDOPTIONINIT = ["pdf", "tikz", "reactjs", "python", "codev", "julia"]
VALIDOPTIONNEWFILE = ["python", "tikz", "diary", "julia"]
data_dir = Path(__file__).resolve().parents[0].joinpath("data")


def main():

    if args.command == "init":

        option_list = args.option.split("+")

        for option in option_list:

            if option not in VALIDOPTIONINIT:

                raise ValueError(
                    option + " is not a valid document output:\n" + str(VALIDOPTIONINIT)
                )

            elif option == "reactjs":

                raise NotImplementedError(option + " is not yet implemented")

        FIGURETARGETS = ""
        DATATARGETS = ""
        TARGETS = ""
        MAKEFILE_CONTENT = ""
        CLEAN = ""
        OPEN = ""
        makedirs(".pandot", exist_ok=True)
        for option in option_list:

            if option == "pdf":

                builddir = "build/pdf"
                buildlatexdir = "build/latex"
                srcdir = "doc"
                makedirs("doc", exist_ok=True)
                Path("doc/main.md").touch()
                try:
                    with open("doc/options.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults", "pdf_default-pandotfiles.yaml"
                                )
                            )
                        ) as file:
                            options = file.read()
                        file_output.write(options)
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite option file")
                try:
                    with open("doc/crossref.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults", "pandoc-crossref-pandotfiles.yaml"
                                )
                            )
                        ) as file:
                            options = file.read()
                        file_output.write(options)
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite crossref file")
                try:
                    with open("doc/metadata.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults", "metadata_default-pandotfiles.yaml"
                                )
                            )
                        ) as file:
                            options = file.read()
                        file_output.write(options)
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite metadata file")
                try:
                    with open("doc/latexmkrc", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("defaults", "latexmkrc"))
                        ) as file:
                            options = file.read()
                        file_output.write(options)
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite latexmkrc")
                try:
                    copytree(
                        str(data_dir.joinpath("templates", "latex_classes")),
                        "doc/texinputs",
                        dirs_exist_ok=True,
                    )
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite latexmkrc")
                try:
                    copytree(
                        str(data_dir.joinpath("templates", "bst")),
                        "doc/texinputs/bst",
                        dirs_exist_ok=True,
                    )
                except FileExistsError:
                    warnings.warn("Pdf init: Won't overwrite latexmkrc")

                with open("doc/Makefile", "w+") as file_output:
                    with open(
                        str(data_dir.joinpath("templates", "makefiles", "pdf_makefile"))
                    ) as file:
                        makefile = file.read()

                    makefile = str(makefile).format(
                        logdir="log",
                        builddir="../" + builddir,
                        buildlatexdir="../" + buildlatexdir,
                        pandocfiles="$(wildcard "
                        + str(".")
                        + "/*.md) "
                        + "$(wildcard "
                        + str(".")
                        + "/*/*.md) "
                        + " $(wildcard "
                        + str(".")
                        + "/*.bib)",
                        mainfile="main.md",
                    )
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("gitignore", "doc.gitignore"))
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
                MAKEFILE_CONTENT += (
                    "pdf: $(wildcard doc/*.md) $(wildcard doc/*.bib)\n"
                    "\t$(MAKE) -C doc FIGURETARGETS=\n"
                )
                CLEAN += "\t$(MAKE) -C doc clean\n"
                TARGETS += "TARGETS += " + builddir + "/main.pdf\n"
                OPEN += "\topen " + builddir + "/main.pdf\n"

                # copy docstyle and relevent files for pandoc
                makedirs(".pandot/latex", exist_ok=True)
                copytree(
                    str(data_dir.joinpath("templates", "docstyle_latex")),
                    ".pandot/latex/docstyle_latex",
                    dirs_exist_ok=True,
                    ignore=ignore_patterns(".*", "_*"),
                )
                makedirs(".pandot/latex/defaults", exist_ok=True)
                copytree(
                    str(data_dir.joinpath("defaults")),
                    ".pandot/latex/defaults",
                    dirs_exist_ok=True,
                    ignore=ignore_patterns(".*", "_*"),
                )
                # makedirs(".pandot/latex/texmf/tex", exist_ok=True)
                # copytree(
                #     str(data_dir.joinpath("templates", "latex_classes")),
                #     ".pandot/latex/texinputs/",
                #     dirs_exist_ok=True,
                #     ignore=ignore_patterns(".*", "_*"),
                # )
                makedirs(".github/workflows/", exist_ok=True)
                copy(
                    str(
                        data_dir.joinpath(
                            "templates", "actions", "github-actions-pdf.yml"
                        )
                    ),
                    ".github/workflows/convert-pdf.yml",
                )
                makedirs(".pandot/pandoc", exist_ok=True)
                copytree(
                    str(data_dir.joinpath("filters")),
                    ".pandot/pandoc/filters",
                    dirs_exist_ok=True,
                    ignore=ignore_patterns(".*", "_*", "lua-filters", "pandoc-gls"),
                )
                copy(
                    str(
                        data_dir.joinpath(
                            "filters",
                            "lua-filters",
                            "include-files",
                            "include-files.lua",
                        )
                    ),
                    ".pandot/pandoc/filters/",
                )
                # copy(
                #     str(
                #         data_dir.joinpath(
                #             "filters",
                #             "lua-filters",
                #             "abstract-to-meta",
                #             "abstract-to-meta.lua",
                #         )
                #     ),
                #     ".pandot/pandoc/filters/",
                # )
                copy(
                    str(data_dir.joinpath("filters", "pandoc-gls", "pandoc-gls.lua")),
                    ".pandot/pandoc/filters/",
                )
                makedirs(".pandot/pandoc/injection", exist_ok=True)
                copytree(
                    str(data_dir.joinpath("injection")),
                    ".pandot/pandoc/injection",
                    dirs_exist_ok=True,
                    ignore=ignore_patterns(".*", "_*"),
                )

            elif option == "tikz":

                srcdir = "src/tikz"
                makedirs(srcdir, exist_ok=True)
                # copy yaml defaults
                try:
                    with open(srcdir + "/auto_tikz.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults", "auto_tikz_default-pandotfiles.yaml"
                                )
                            )
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
                        str(
                            data_dir.joinpath(
                                "templates", "makefiles", "auto_tikz_makefile"
                            )
                        )
                    ) as file:
                        makefile = file.read()

                    makefile = str(makefile).format(
                        yamlfile="auto_tikz.yaml",
                        builddir="../../" + builddir,
                        logdir=logdir,
                        tikzfiles=tikzfiles.replace(r"wildcard\ ", "wildcard "),
                    )
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("gitignore", "tikz.gitignore"))
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
                    str(data_dir.joinpath("templates", "makefiles", "python_makefile"))
                ) as file:
                    makefile = file.read()
                makefile = makefile.format(builddir=str("../../" + builddir))
                with open(srcdir + "/Makefile", "w+") as file_output:
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("gitignore", "python.gitignore"))
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Python init: Won't overwrite gitignore file")

                try:
                    with open(srcdir + "/environment.yaml", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("defaults", "environment.yaml"))
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

            elif option == "julia":

                srcdir = "src/julia"
                builddir = "build/julia"
                run(
                    "julia --project=" + srcdir + " -e 'using Pkg; Pkg.instantiate()'",
                    shell=True,
                )
                makedirs(srcdir, exist_ok=True)
                with open(
                    str(data_dir.joinpath("templates", "makefiles", "julia_makefile"))
                ) as file:
                    makefile = file.read()
                makefile = makefile.format(builddir=str("../../" + builddir))
                with open(srcdir + "/Makefile", "w+") as file_output:
                    file_output.write(makefile)

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("gitignore", "julia.gitignore"))
                        ) as file:
                            gitignore = file.read()
                        file_output.write(gitignore)
                except FileExistsError:
                    warnings.warn("Julia init: Won't overwrite gitignore file")

                sources = "$(wildcard src/julia/*.jl) $(DATATARGETS)"
                MAKEFILE_CONTENT += (
                    builddir
                    + "/julia_stamp: "
                    + sources
                    + " \n\t$(MAKE) -C "
                    + srcdir
                    + "\n"
                )

                TARGETS += "TARGETS += " + builddir + "/julia_stamp\n"
                FIGURETARGETS += "FIGURETARGETS += " + builddir + "/julia_stamp\n"
                CLEAN += "\t$(MAKE) -C " + srcdir + " clean\n"

            elif option == "codev":

                srcdir = "src/codev"
                builddir = "build/codev"
                outputdir = "output"
                bindir = "build/codevbin"
                makedirs(srcdir, exist_ok=True)
                makedirs(bindir, exist_ok=True)
                makedirs(srcdir + "/src/liseq", exist_ok=True)
                makedirs(srcdir + "/src/fortran", exist_ok=True)
                # copy yaml defaults
                try:
                    with open(srcdir + "/codev_remote.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults", "codev_remote_default-pandotfiles.yaml"
                                )
                            )
                        ) as file:
                            codev_remote = file.read()
                        file_output.write(codev_remote)
                except FileExistsError:
                    warnings.warn("Using existing codev_remote.yaml config file")

                with open(srcdir + "/Makefile", "w+") as file_output:
                    with open(
                        str(
                            data_dir.joinpath(
                                "templates", "makefiles", "codev_makefile"
                            )
                        )
                    ) as file:
                        makefile = file.read()
                    makefile = makefile.format(
                        builddir="../../" + str(builddir),
                        outputdir=str(outputdir),
                        bindir="../../" + str(bindir),
                    )
                    file_output.write(makefile)

                with open(srcdir + "/src/fortran/Makefile", "w+") as file_output:
                    with open(
                        str(
                            data_dir.joinpath(
                                "templates", "makefiles", "codev_build_makefile"
                            )
                        )
                    ) as file:
                        makefile = file.read()
                    file_output.write(makefile)
                try:
                    with open(srcdir + "/codev_remote_build.yaml", "x") as file_output:
                        with open(
                            str(
                                data_dir.joinpath(
                                    "defaults",
                                    "codev_remote_build_default-pandotfiles.yaml",
                                )
                            )
                        ) as file:
                            codev_remote = file.read()
                        file_output.write(codev_remote)
                except FileExistsError:
                    warnings.warn("Using existing codev_remote_build.yaml config file")

                try:
                    with open(srcdir + "/.gitignore", "x") as file_output:
                        with open(
                            str(data_dir.joinpath("gitignore", "codev.gitignore"))
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
                    str(data_dir.joinpath("gitignore", "project.gitignore"))
                ) as file:
                    gitignore = file.read()
                file_output.write(gitignore)
        except FileExistsError:
            warnings.warn("Project init: Won't overwrite gitignore file")

    elif args.command == "newfile":

        optionnewfile = args.option

        if optionnewfile not in VALIDOPTIONNEWFILE:
            raise ValueError(
                optionnewfile
                + " is not a valid document output:\n"
                + str(VALIDOPTIONNEWFILE)
            )

        elif optionnewfile == "python":
            print("Enter filename (without extension)")
            filename = input()
            try:
                with open(filename + ".py", "x") as file_output:
                    file_output.write(
                        "#! shebangrun()"
                        " { conda activate ../../build/python/env > /dev/null;"
                        "ipython $1;"
                        "conda deactivate > /dev/null; };"
                        " shebangrun"
                    )
                    file_output.close()
            except FileExistsError:
                raise FileExistsError("Won't overwrite file if it already exists")

        elif optionnewfile == "julia":
            print("Enter filename (without extension)")
            filename = input()
            try:
                with open(filename + ".jl", "x") as file_output:
                    file_output.write("#! julia --project=.")
                    file_output.close()
            except FileExistsError:
                raise FileExistsError("Won't overwrite file if it already exists")

        elif optionnewfile == "tikz":
            print("Enter filename (without extension)")
            filename = input()
            try:
                with open(filename + ".tikz", "x") as file_output:
                    file_output.write("\\begin{tikzpicture}\n\\end{tikzpicture}")
            except FileExistsError:
                raise FileExistsError("Won't overwrite file if it already exists")

        elif optionnewfile == "diary":
            pwd = (
                run("echo $PWD", shell=True, stderr=PIPE, stdout=PIPE)
                .stdout.decode("utf-8")
                .splitlines()[0]
            )
            fullname = (
                run("id -F", shell=True, stderr=PIPE, stdout=PIPE)
                .stdout.decode("utf-8")
                .splitlines()[0]
            )

            filename = str(
                Path(pwd).joinpath(datetime.datetime.now().strftime("%Y%m%d") + ".md")
            )

            projectname = Path(filename).parts[-2]

            try:
                with open(filename, "x") as file_output:
                    with open(
                        str(data_dir.joinpath("templates", "documents", "diary.md"))
                    ) as file:
                        diary_template = file.read()
                    file_output.write(
                        diary_template.format(
                            fullname=fullname,
                            diaryname="Notes du "
                            + datetime.datetime.now().strftime("%Y-%m-%d"),
                            date=datetime.datetime.now().strftime("%Y-%m-%d"),
                            projectname=projectname,
                            docstyle="diary",
                        )
                    )

            except FileExistsError:
                warnings.warn(
                    "Diary file {filename} already exists".format(filename=filename)
                )


if __name__ == "__main__":
    pass
    # main()
