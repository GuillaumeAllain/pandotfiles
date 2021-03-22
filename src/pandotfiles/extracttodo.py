import argparse
from subprocess import run, PIPE
from pathlib import Path
from datetime import date


parser = argparse.ArgumentParser(
    description=""" Utility to extract todo from inside markdown documents in a directory.
                    Output to org mode format from Pandoc Markdown format.
                    Will output to an org file which is named after the first subdirectory.
                       """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    help="Input directory where Markdown files are situated. Default: $PWD (Current directory)",
    default="$PWD",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output org directory. Default: $HOME/org",
    default="$HOME/org",
)

args = parser.parse_args()


def get_todo_filenames(PATH):
    rgoutput = run(
        'rg -ln "\t*# (TODO|DONE)" ' + PATH, shell=True, stdout=PIPE, stderr=PIPE
    )
    return rgoutput.stdout.decode("utf-8").splitlines()


def get_line(FILENAME, STRING_TO_FIND, TRESHOLD=0):
    rgoutput = run(
        "rg -nI '" + STRING_TO_FIND + "' " + FILENAME,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
    )
    return [
        x
        for x in [
            int(x.split(":")[0]) for x in rgoutput.stdout.decode("utf-8").splitlines()
        ]
        if x > TRESHOLD
    ]


def remove_todo(PATH):

    # pandoc main.md -t markdown+yaml_metadata_block --wrap=preserve -s > main2.md
    PANDOC_ORG_COMMAND = """pandoc \
                        {filename} \
                        -t markdown+yaml_metadata_block \
                        --wrap=preserve \
                        -s \
                        -L ~/.local/share/pandot/filters/remove-todo.lua \
                        --atx-header \
                        -o {filename}\
                        """
    run(PANDOC_ORG_COMMAND.format(filename=PATH), shell=True)


def get_org(PATH):
    PANDOC_ORG_COMMAND = """pandoc \
                        -t org \
                        -L ~/.local/share/pandot/filters/get-todo.lua \
                        --wrap=preserve"""
    pandocoutput = run(
        PANDOC_ORG_COMMAND + " " + PATH, shell=True, stdout=PIPE, stderr=PIPE
    )
    return pandocoutput.stdout.decode("utf-8")


def extract():
    DIR = (
        run("echo " + args.input, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )
    ORGDIR = (
        run("echo " + args.output, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )

    if Path(ORGDIR).exists:
        allfiles = get_todo_filenames(DIR)
        newtodo = ""
        if allfiles:
            for file in allfiles:
                local_org_file = Path(file.split(DIR + "/")[1]).parts[0] + ".org"
                absolute_org_file = str(ORGDIR) + "/" + local_org_file
                newtodo += (
                    "# "
                    + file
                    + " <"
                    + date.today().strftime("%d/%m/%Y")
                    + ">"
                    + "\n"
                    + get_org(file)
                    + "\n"
                )
                remove_todo(file)

            with open(absolute_org_file, "a+") as orgfile:
                orgfile.write(newtodo)
        else:
            pass
    else:
        raise FileNotFoundError("Can't find org directory")


if __name__ == "__main__":
    extract()
