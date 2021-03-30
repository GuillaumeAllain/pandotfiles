import argparse
from pathlib import Path
from subprocess import run, PIPE
import datetime
import warnings
from os import makedirs

from xdg import xdg_data_home

from pandotfiles.panotes.todomd import extract_todo
from pandotfiles.panotes.tagsmd import extract_tags

parser = argparse.ArgumentParser(
    description="""Panotes is a program designed to manage notes and todos.
                   Manages $NOTES_DIR by default.

                   newdiary: Creates a dated diary file: $NOTES_DIR/journal/YYYYmmdd.md
                   exporttodo: Extract and writes todo from all files ($NOTES_DIR/SUBDIR/*) to ~/org/SUBDIR.org
                   extracttag: Returns to Stdout all blocks with the occurence of a given tag (-t option defaults to empty string)""",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("command", choices=["newdiary", "exporttodo", "extracttag"])

parser.add_argument("-t", "--tag", help="Tag used for extracttag", type=str, default="")

parser.add_argument(
    "-d", "--dir", help="Notes directory", type=str, default="$NOTES_DIR"
)

args = parser.parse_args()


def main():
    if args.command == "newdiary":
        notesdir = (
            run("echo " + args.dir, shell=True, stderr=PIPE, stdout=PIPE)
            .stdout.decode("utf-8")
            .splitlines()[0]
        )

        makedirs(Path(notesdir).joinpath("journal"), exist_ok=True)

        fullname = (
            run("id -F", shell=True, stderr=PIPE, stdout=PIPE)
            .stdout.decode("utf-8")
            .splitlines()[0]
        )

        filename = str(
            Path(notesdir)
            .joinpath("journal")
            .joinpath(datetime.datetime.now().strftime("%Y%m%d") + ".md")
        )

        projectname = Path(filename).parts[-2]

        try:
            with open(filename, "x") as file_output:
                with open(
                    str(xdg_data_home()) + "/pandot/templates/documents/diary.md"
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
        print(filename)
    elif args.command == "exporttodo":
        extract_todo(args.dir, "$HOME/org")
    elif args.command == "extracttag":
        extract_tags(args.tag, args.dir, None)


if __name__ == "__main__":
    main()
