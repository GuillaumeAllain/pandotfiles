from subprocess import run, PIPE
from pathlib import Path


def get_todo_filenames(PATH):
    rgoutput = run('rg -ln "(TODO|DONE)" ' + PATH, shell=True, stdout=PIPE, stderr=PIPE)
    return [escape(x) for x in rgoutput.stdout.decode("utf-8").splitlines()]


def get_project_name(file, directory):
    projectname = str(Path(file).relative_to(directory).parent)
    if projectname == ".":
        projectname = Path(file).stem
    return projectname


def escape(stringtoescape):
    return stringtoescape.replace(" ", r"\ ")


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
