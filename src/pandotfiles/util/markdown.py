from subprocess import run

PANDOC_MARKDOWN_OUTPUT_COMMANDS = (
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables"
    + " -s --markdown-headings=atx --wrap=preserve -V header-includes= -V include-before= -V include-after= "
)
PANDOC_MARKDOWN_OUTPUT_COMMANDS_NOYAML = (
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables"
    + " --markdown-headings=atx --wrap=preserve -V header-includes= -V include-before= -V include-after= "
)
CLEAN_WHITESPACE = (
    "| sed '/^$/N;/^\\n$/D' | sed 's/^```\\s*$/```\\n/g' |"
    + " awk '{{if (NR==1 && NF==0) next}};1' | awk 'NR > 1{{print t}} {{t = $0}}END{{if (NF) print }}' "
)
CLEAN_TAGS = r"| perl -p -i -e 's/\\(#\S+)/$1/g'"


def clean_markdown(file=None):
    """If no input, use Stdin"""

    LOCAL_PANDOC_MARKDOWN_COMMAND = (
        "/usr/local/bin/pandoc {filename} "
        + PANDOC_MARKDOWN_OUTPUT_COMMANDS
        + CLEAN_WHITESPACE
        + CLEAN_TAGS
    )
    if file is None:
        run(LOCAL_PANDOC_MARKDOWN_COMMAND.format(filename=""), shell=True)
    else:
        run(
            (LOCAL_PANDOC_MARKDOWN_COMMAND + " > tmp ; mv tmp {filename}").format(
                filename=file
            ),
            shell=True,
        )
