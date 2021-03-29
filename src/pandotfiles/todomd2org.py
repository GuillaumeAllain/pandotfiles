import argparse
from subprocess import run, PIPE
from pathlib import Path
import datetime
from pandotfiles.util.filenames import get_todo_filenames, get_project_name, escape


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


def remove_todo(PATH):
    PANDOC_ORG_COMMAND = """/usr/local/bin/pandoc \
                        {filename} \
                        -t markdown+yaml_metadata_block \
                        --wrap=preserve \
                        -o {filename} \
                        -s \
                        -L ~/.local/share/pandot/filters/remove-todo.lua \
                        --markdown-headings=atx \
                        -V header-includes= \
                        -V include-before= \
                        -V include-after= \
                        ; sed '/^$/N;/^\\n$/D' {filename} \
                        | sed 's/^```\\s*$/```\\n/g' \
                        | awk '{{if (NR==1 && NF==0) next}};1' \
                        | awk 'NR > 1{{print t}} {{t = $0}}END{{if (NF) print }}' > tmp \
                        ;mv tmp {filename}
                        """
    run(PANDOC_ORG_COMMAND.format(filename=PATH), shell=True)


def get_org(PATH):
    PANDOC_ORG_COMMAND = """/usr/local/bin/pandoc \
                        -t org \
                        -L ~/.local/share/pandot/filters/get-todo.lua \
                        --wrap=preserve"""
    pandocoutput = run(
        PANDOC_ORG_COMMAND + " " + PATH, shell=True, stdout=PIPE, stderr=PIPE
    )
    return pandocoutput.stdout.decode("utf-8")


def extracttodo():
    DIR = escape(
        run("echo " + args.input, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )
    ORGDIR = escape(
        run("echo " + args.output, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )

    if Path(ORGDIR).exists:
        allfiles = get_todo_filenames(DIR)
        newtodo = ""
        if allfiles:
            for file in allfiles:
                projectname = get_project_name(file, DIR)
                local_org_file = projectname + ".org"
                absolute_org_file = str(ORGDIR) + "/" + local_org_file
                newtodo += (
                    "# "
                    + file
                    + datetime.datetime.now().strftime("<%Y-%m-%d %H:%M:%S %A>")
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
    extracttodo()
