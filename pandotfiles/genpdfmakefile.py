import argparse
from re import sub
from xdg import xdg_data_home

parser = argparse.ArgumentParser(
    description='''Generate a Makefile to compile all tikz (*.tikz) file from a repo.''',
                   formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
                '-o','--output', type=str,
                help='Output file location. Default: output to terminal',
                default=None)

parser.add_argument(
                '-l', '--logdir', type=str,
                help='Pandoc log directory. Default: log',
                default='log')

parser.add_argument(
                '-b', '--builddir', type=str,
                help='Pandoc build directory. Default: build',
                default='build')

parser.add_argument(
                '-s', '--srcdir', type=str,
                help='Pandoc src directory. Default: .',
                default='.')

parser.add_argument(
                '-m', '--mainfile', type=str,
                help='Pandoc main file. Default: main.md',
                default='main.md')

args = parser.parse_args()

def main():

    with open(str(xdg_data_home())+'/pandoc/templates/makefile_template/pdf_makefile') as file:
        makefile = file.read()

    makefile = sub(r'(logdir\s=)(.*)','\\1 '+args.logdir, makefile)
    makefile = sub(r'(builddir\s=)(.*)','\\1 '+args.builddir, makefile)
    makefile = sub(r'(pandocfiles\s=)(.*)',"\\1 $(wildcard " + args.srcdir + '/*.md)'+
            '$(wildcard ' + args.srcdir + '/*.bib)', makefile)
    makefile = sub(r'(mainfile\s=)(.*)','\\1 '+args.mainfile, makefile)

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

