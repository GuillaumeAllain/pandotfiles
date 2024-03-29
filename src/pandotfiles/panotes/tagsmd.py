from subprocess import run, PIPE


from pandotfiles.util.markdown import (
    PANDOC_MARKDOWN_OUTPUT_COMMANDS_NOYAML,
    CLEAN_WHITESPACE,
    # CLEAN_TAGS,
)

from pandotfiles.panotes.file_management import (
    escape,
    get_filename_regex,
)


def get_regex_blocks(filename, regex):
    LOCAL_PANDOC_MARKDOWN_COMMAND = (
        "/usr/local/bin/pandoc {filename}"
        + " -M greppattern={regex} -L ~/.local/share/pandot/filters/greppattern.lua --shift-heading-level-by=1 "
        + PANDOC_MARKDOWN_OUTPUT_COMMANDS_NOYAML
        + CLEAN_WHITESPACE
        # + CLEAN_TAGS
    ).format(filename=filename, regex=regex)
    pandocoutput = run(
        LOCAL_PANDOC_MARKDOWN_COMMAND, shell=True, stdout=PIPE, stderr=PIPE
    )
    return pandocoutput.stdout.decode("utf-8")


def extract_tags(tag, dir, output):

    DIR = escape(
        run("echo " + dir, shell=True, stderr=PIPE, stdout=PIPE)
        .stdout.decode("utf-8")
        .splitlines()[0]
    )
    allfiles = get_filename_regex(DIR, tag)
    buffer = ""
    for file in allfiles:
        buffer += "# " + file + "\n\n"
        buffer += get_regex_blocks(file, tag)
        buffer += "\n"
    if output is not None:
        with open(output, "a+") as fileoutput:
            fileoutput.write(buffer)
    else:
        print(buffer)
