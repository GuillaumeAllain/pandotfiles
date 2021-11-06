import argparse
from pathlib import Path

from pandotfiles.util.parser import tikzyamlparse
from pandotfiles.util.makefile_mod import tikzmakefilemod

parser = argparse.ArgumentParser(
    description="""Generate a Makefile to compile all tikz (*.tikz) file from a repo.""",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file location. Default: output to terminal",
    default=None,
)

parser.add_argument(
    "-y",
    "--yamlfile",
    type=str,
    help="Auto_tikz YAML file location. Default: auto_tikz.yaml",
    default="auto_tikz.yaml",
)

parser.add_argument(
    "-b",
    "--builddir",
    type=str,
    help="Auto_tikz build directory. Default: build",
    default="build",
)

args = parser.parse_args()

data_dir = Path(__file__).resolve().parents[0].joinpath("data")


def main():

    with open(
        str(data_dir.joinpath("templates", "makefiles", "auto_tikz_makefile"))
    ) as file:
        makefile = file.read()

    yaml_config = tikzyamlparse(args.yamlfile)
    logdir = yaml_config["log_folder"]
    tikzfiles = yaml_config["files_makestring"]

    makefile = tikzmakefilemod(
        makefile, args.yamlfile, args.builddir, logdir, tikzfiles
    )

    if args.output is not None:
        with open(args.output, "w+") as file_output:
            file_output.write(makefile)
    else:
        print(makefile)


if __name__ == "__main__":
    main()
