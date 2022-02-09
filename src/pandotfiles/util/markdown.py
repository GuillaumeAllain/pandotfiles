from subprocess import run
from pathlib import Path

data_dir = Path(__file__).resolve().parents[1].joinpath("data")

PANDOC_MARKDOWN_OUTPUT_COMMANDS = (
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables-latex_macros "
    + '-L '
    + str(data_dir)
    + '/filters/math_spaces.lua'
    + " -s --markdown-headings=atx --wrap=preserve -V header-includes= -V include-before= -V include-after= "
)
PANDOC_MARKDOWN_OUTPUT_COMMANDS_NOYAML = (
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables-latex_macros"
    + '-L '
    + str(data_dir)
    + '/filters/math_spaces.lua'
    + " --markdown-headings=atx --wrap=preserve -V header-includes= -V include-before= -V include-after= "
)
CLEAN_WHITESPACE = (
    "| sed '/^$/N;/^\\n$/D' | sed 's/^```\\s*$/```\\n/g' |"
    + " awk '{{if (NR==1 && NF==0) next}};1' | awk 'NR > 1{{print t}} {{t = $0}}END{{if (NF) print }}' "
)


def clean_markdown(file=None):
    """If no input, use Stdin"""

    LOCAL_PANDOC_MARKDOWN_COMMAND = (
        "pandoc {filename} "
        + PANDOC_MARKDOWN_OUTPUT_COMMANDS
        + CLEAN_WHITESPACE
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

if __name__ == "__main__":
    clean_markdown(file="~/scratch/hashtag/test.md")
