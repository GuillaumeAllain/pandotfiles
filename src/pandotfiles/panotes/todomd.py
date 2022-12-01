from subprocess import run, PIPE
from pathlib import Path
from pandotfiles.panotes.file_management import (
    escape,
    get_filename_regex,
    get_relative_parent_name,
)
from pandotfiles.util.markdown import (
    PANDOC_MARKDOWN_OUTPUT_COMMANDS,
    CLEAN_WHITESPACE,
    # CLEAN_TAGS,
)


def remove_todo(PATH):
    LOCAL_PANDOC_MARKDOWN_COMMAND = (
        "/usr/local/bin/pandoc {filename} -L ~/.local/share/pandot/filters/remove-todo.lua "
        + PANDOC_MARKDOWN_OUTPUT_COMMANDS
        + CLEAN_WHITESPACE
        # + CLEAN_TAGS
        + " > tmp ; mv tmp {filename}"
    )
    run(LOCAL_PANDOC_MARKDOWN_COMMAND.format(filename=PATH), shell=True)


def get_org(PATH):
    PANDOC_ORG_COMMAND = """/usr/local/bin/pandoc \
                        -t org \
                        -L ~/.local/share/pandot/filters/get-todo.lua \
                        --wrap=preserve"""
    pandocoutput = run(
        PANDOC_ORG_COMMAND + " " + PATH, shell=True, stdout=PIPE, stderr=PIPE
    )
    return pandocoutput.stdout.decode("utf-8")


def extract_todo(dir, orgdir):
    DIR = escape(
        run("echo " + dir, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )
    ORGDIR = escape(
        run("echo " + orgdir, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )

    if Path(ORGDIR).exists:
        allfiles = get_filename_regex(DIR, "(TODO|DONE)")
        newtodo = ""
        if allfiles:
            for file in allfiles:
                projectname = get_relative_parent_name(file, DIR)
                local_org_file = projectname + ".org"
                absolute_org_file = str(ORGDIR) + "/" + local_org_file
                newtodo += (
                    get_org(file)
                    + "\n"
                    # + "# "
                    # + file
                    # + datetime.datetime.now().strftime("<%Y-%m-%d %H:%M:%S %A>")
                    # + "\n"
                )
                remove_todo(file)

            with open(absolute_org_file, "a+") as orgfile:
                orgfile.write(newtodo)
        else:
            pass
    else:
        raise FileNotFoundError("Can't find org directory")
