import argparse
from re import sub

from pandotfiles.util.parser import tikzyamlparse

parser = argparse.ArgumentParser(
    description='''Generate a Makefile to compile all tikz (*.tikz) file from a repo.''',
                   formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
                '-o','--output', type=str,
                help='Output file location. Default: output to terminal',
                default=None)

parser.add_argument(
                '-y', '--yamlfile', type=str,
                help='Auto_tikz YAML file location. Default: auto_tikz.yaml',
                default='auto_tikz.yaml')

parser.add_argument(
                '-b', '--builddir', type=str,
                help='Auto_tikz build directory. Default: build',
                default='build')

args = parser.parse_args()

def main():

    with open('../data/makefile_template/auto_tikz_makefile') as file:
        makefile = file.read()

    yaml_config = tikzyamlparse(args.yamlfile)
    logdir = yaml_config['log_folder']
    tikzfiles = yaml_config['files_makestring']

    makefile = sub(r'(yamlfile\s=)(.*)','\\1 '+args.yamlfile, makefile)
    makefile = sub(r'(builddir\s=)(.*)','\\1 '+args.builddir, makefile)
    makefile = sub(r'(logdir\s=)(.*)','\\1 '+logdir, makefile)
    makefile = sub(r'(tikzfiles\s=)(.*)','\\1 '+tikzfiles, makefile)

    if args.output is not None:
        try:
            file_output = open(args.output,'x')
        except FileExistsError:
            file_output = open(args.output,'w')
        file_output.write(makefile)
        file_output.close()
    else: print(makefile)

if __name__ == "__main__":
    main()

