from subprocess import run, PIPE
from pathlib import Path


def get_todo_filenames(PATH):
    rgoutput = run('rg -ln "(TODO|DONE)" ' + PATH, shell=True, stdout=PIPE, stderr=PIPE)
    return rgoutput.stdout.decode("utf-8").splitlines()


def get_project_name(file, directory):
    projectname = str(Path(file).relative_to(directory).parent)
    if projectname == ".":
        projectname = Path(file).stem
    return projectname


def escape(stringtoescape):
    return stringtoescape.replace(" ", r"\ ")
