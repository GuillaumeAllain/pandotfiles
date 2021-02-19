import argparse
import os
import warnings

from pathlib import Path
from re import sub
#
from xdg import xdg_data_home

from pandotfiles.util.parser import tikzyamlparse
from pandotfiles.util.makefile_mod import pdfmakefilemod, tikzmakefilemod

parser = argparse.ArgumentParser(
        description=''' Pandot can init document templates and makefiles for
                        compiling academic documents or presentations.
                    ''',
                   formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
        'command', choices=['init']
        )

parser.add_argument(
        'option', type=str
        )

parser.add_argument(
                '-o', '--output', type=str,
                help='Output file location. Default: output to terminal (T)',
                default=None)

args = parser.parse_args()

VALIDOPTION = ['pdf', 'tikz', 'reactjs', 'python', 'codev']

def main():
    option_list = args.option.split('+')
    FIGURETARGETS = ''
    DATATARGETS = ''
    TARGETS = ''
    MAKEFILE_CONTENT = ''
    CLEAN = ''
    OPEN = ''
    for option in option_list:
        if option not in VALIDOPTION:
            raise ValueError(option+" is not a valid document output")
        elif option == 'reactjs':
            raise NotImplementedError(option+' is not yet implemented')
        elif option == 'pdf':
            builddir = "build/pdf"
            os.makedirs("doc",exist_ok=True)
            Path("doc/main.md").touch()

            with open(str(xdg_data_home()) +
                    '/pandot/templates/makefile_template/pdf_makefile') as file:
                makefile = file.read()

            makefile = pdfmakefilemod(makefile,
                                      "log",
                                      "../"+builddir,
                                      ".",
                                      "main.md")

            try:
                file_output = open("doc/Makefile", 'x')
            except FileExistsError:
                file_output = open("doc/Makefile", 'w')
            file_output.write(makefile)
            file_output.close()
            sources = '$(wildcard doc/*.md) '+' $(wildcard doc/*.bib) ' + '$(FIGURETARGETS)'
            MAKEFILE_CONTENT += builddir+'/main.pdf: ' + sources + '\n\t$(MAKE) -C doc \n'
            CLEAN += "\t$(MAKE) -C doc clean\n"
            TARGETS += 'TARGETS += '+builddir+'/main.pdf\n'
            OPEN += "\topen "+builddir+"/main.pdf\n"

        elif option == "tikz":

            srcdir = "src/tikz"

            os.makedirs(srcdir, exist_ok=True)

            with open(str(xdg_data_home()) +
                    '/pandot/templates/makefile_template/auto_tikz_makefile') as file:
                makefile = file.read()


            # copy yaml defaults
            try:
                file_output = open(srcdir+'/auto_tikz.yaml', 'x')
                with open(str(xdg_data_home()) +
                        '/pandot/defaults/auto_tikz_default-pandotfiles.yaml') as file:
                    autoyaml = file.read()
                file_output.write(autoyaml)
                file_output.close()
            except FileExistsError:
                warnings.warn("Using existing auto_tikz.yaml config file")

            yaml_config = tikzyamlparse(srcdir+'/auto_tikz.yaml')
            logdir = yaml_config['log_folder']
            tikzfiles = yaml_config['files_makestring']
            builddir = 'build/tikz'

            makefile = tikzmakefilemod(makefile,
                                       'auto_tikz.yaml',
                                       '../../'+builddir,
                                       logdir,
                                       tikzfiles)

            try:
                file_output = open(srcdir+"/Makefile", 'x')
            except FileExistsError:
                file_output = open(srcdir+"/Makefile", 'w')
            file_output.write(makefile)
            file_output.close()

            sources = '$(wildcard src/tikz/*.tikz)'
            MAKEFILE_CONTENT += builddir+'/tikz_stamp:'+sources+' \n\t$(MAKE) -C '+srcdir+' \n'

            TARGETS += 'TARGETS += '+builddir+'/tikz_stamp\n'
            FIGURETARGETS += 'FIGURETARGETS += '+builddir+'/tikz_stamp\n'
            CLEAN += '\t$(MAKE) -C '+srcdir+' clean\n'

        elif option == "python":

            srcdir = "src/python"
            builddir = 'build/python'

            os.makedirs(srcdir, exist_ok=True)

            Path(srcdir+"/environment.yaml").touch()

            with open(str(xdg_data_home()) +
                      '/pandot/templates/makefile_template/python_makefile') as file:
                makefile = file.read()

            makefile = sub(r'(builddir\s=)(.*)',
                           '\\1 ../../'+str(builddir),
                           makefile)

            try:
                file_output = open(srcdir+"/Makefile", 'x')
            except FileExistsError:
                file_output = open(srcdir+"/Makefile", 'w')
            file_output.write(makefile)
            file_output.close()

            sources = '$(wildcard src/python/*.py) $(DATATARGETS)'
            MAKEFILE_CONTENT += builddir+'/python_stamp: '+sources+' \n\t$(MAKE) -C '+srcdir+'\n'

            TARGETS += 'TARGETS += '+builddir+'/python_stamp\n'
            FIGURETARGETS += 'FIGURETARGETS += '+builddir+'/python_stamp\n'
            CLEAN += '\t$(MAKE) -C '+srcdir+' clean\n'

        elif option == "codev":

            srcdir = "src/codev"
            builddir = 'build/codev'
            outputdir = 'output'

            os.makedirs(srcdir, exist_ok=True)

            # copy yaml defaults
            try:
                file_output = open(srcdir+'/codev_remote.yaml','x')
                with open(str(xdg_data_home())+
                        '/pandot/defaults/codev_remote_default-pandotfiles.yaml') as file:
                    codev_remote = file.read()
                file_output.write(codev_remote)
                file_output.close()
            except FileExistsError:
                warnings.warn("Using existing codev_remote.yaml config file")

            with open(str(xdg_data_home())+
                    '/pandot/templates/makefile_template/codev_makefile') as file:
                makefile = file.read()

            makefile = sub(r'(builddir\s=)(.*)','\\1 ../../'+str(builddir), makefile)
            makefile = sub(r'(outputdir\s=)(.*)','\\1 '+str(outputdir), makefile)

            try:
                file_output = open(srcdir+"/Makefile",'x')
            except FileExistsError:
                file_output = open(srcdir+"/Makefile",'w')

            file_output.write(makefile)
            file_output.close()

            sources = '$(wildcard src/codev/*/*.seq)'
            MAKEFILE_CONTENT += builddir+'/codev_stamp:'+sources+' \n\t$(MAKE) -C '+srcdir+'\n'

            TARGETS += 'TARGETS += '+builddir+'/codev_stamp\n'
            DATATARGETS += 'DATATARGETS+= '+builddir+'/codev_stamp\n'
            FIGURETARGETS += 'FIGURETARGETS += '+builddir+'/codev_stamp\n'
            CLEAN += '\t$(MAKE) -C '+srcdir+' clean\n'

    projectmakefile = (TARGETS+FIGURETARGETS+DATATARGETS+
                       'export TARGETS\nexport FIGURETARGETS\nexport DATATARGETS'+
                       '\n\n.PHONY: all clean open\n\nall: $(TARGETS)\n\n'+
                       '\n\nclean:\n'+CLEAN+
                       '\n\nopen:\n'+OPEN+
                       MAKEFILE_CONTENT)

    if (args.output is not None) and (args.output != 'T'):
        try:
            file_output = open(args.output,'x')
        except FileExistsError:
            file_output = open(args.output,'w')
        file_output.write(projectmakefile)
        file_output.close()
    else: print(projectmakefile)

if __name__ == "__main__":
    main()

