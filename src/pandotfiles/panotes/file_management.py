from subprocess import run, PIPE
from pathlib import Path


def get_filename_regex(path, regex):
    rgoutput = run(
        'rg -ln "' + regex + '" ' + path, shell=True, stdout=PIPE, stderr=PIPE
    )
    return [escape(x) for x in rgoutput.stdout.decode("utf-8").splitlines()]


def get_relative_parent_name(file, directory):
    projectname = str(Path(file).relative_to(directory).parent)
    if projectname == ".":
        projectname = Path(file).stem
    return projectname


def escape(stringtoescape):
    return stringtoescape.replace(" ", r"\ ")


def get_line(path, regex, threshold=0):
    rgoutput = run(
        "rg -nI '" + regex + "' " + path, shell=True, stdout=PIPE, stderr=PIPE,
    )
    return [
        x
        for x in [
            int(x.split(":")[0]) for x in rgoutput.stdout.decode("utf-8").splitlines()
        ]
        if x > threshold
    ]
