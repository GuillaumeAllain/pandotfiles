from subprocess import run
from pathlib import path

data_dir = path(__file__).resolve().parents[1].joinpath("data")

pandoc_markdown_output_commands = (
    "-f markdown-raw_html "
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables-latex_macros "
    + "-l "
    + str(data_dir)
    + "/filters/math_spaces.lua"
    + " -s --markdown-headings=atx --wrap=preserve -v header-includes= -v include-before= -v include-after= "
)
pandoc_markdown_output_commands_noyaml = (
    "-t markdown+yaml_metadata_block-grid_tables-simple_tables-multiline_tables-latex_macros "
    + "-l "
    + str(data_dir)
    + "/filters/math_spaces.lua"
    + " --markdown-headings=atx --wrap=preserve -v header-includes= -v include-before= -v include-after= "
)
clean_comments = r"|sed 's/^\\<!--\(.*\)--\\>/<!--\1-->/g' "
clean_whitespace = (
    "| sed '/^$/n;/^\\n$/d' | sed 's/^```$/```\\n/g' |"
    + " awk '{{if (nr==1 && nf==0) next}};1' | awk 'nr > 1{{print t}} {{t = $0}}end{{if (nf) print }}' "
)
clean_codeblocks = "|sed 's/^```[[:space:]]/```/g' "


def clean_markdown(file=none):
    """if no input, use stdin"""

    local_pandoc_markdown_command = (
        "pandoc {filename} "
        + pandoc_markdown_output_commands
        + clean_whitespace
        + clean_comments
        + clean_codeblocks
    )
    if file is none:
        run(local_pandoc_markdown_command.format(filename=""), shell=true)
    else:
        run(
            (local_pandoc_markdown_command + " > tmp ; mv tmp {filename}").format(
                filename=file
            ),
            shell=true,
        )


if __name__ == "__main__":
    clean_markdown(file="~/scratch/hashtag/test.md")
