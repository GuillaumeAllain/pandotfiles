import argparse
from xdg import xdg_data_home

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
    "-l", "--logdir", type=str, help="Pandoc log directory. Default: log", default="log"
)

parser.add_argument(
    "-b",
    "--builddir",
    type=str,
    help="Pandoc build directory. Default: build",
    default="build",
)

parser.add_argument(
    "-s", "--srcdir", type=str, help="Pandoc src directory. Default: .", default="."
)

parser.add_argument(
    "-m",
    "--mainfile",
    type=str,
    help="Pandoc main file. Default: main.md",
    default="main.md",
)

args = parser.parse_args()


def main():

    with open(
        str(xdg_data_home()) + "/pandot/templates/makefiles/pdf_makefile"
    ) as file:
        makefile = file.read()

    makefile = str(makefile).format(
        logdir=args.logdir,
        builddir=args.builddir,
        pandocfiles="$(wildcard "
        + str(args.srcdir)
        + "/*.md)"
        + " $(wildcard "
        + str(args.srcdir)
        + "/*.bib)",
        mainfile=args.mainfile,
    )

    if args.output is not None:

        with open(args.output, "w+") as file_output:
            file_output.write(makefile)
    else:
        print(makefile)


if __name__ == "__main__":
    main()
