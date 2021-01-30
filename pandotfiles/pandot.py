import argparse
import os
import warnings

from pathlib import Path
from shutil import copy
# from re import sub
#
from xdg import xdg_data_home, xdg_cache_home

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

args = parser.parse_args()

VALIDOPTION = ['pdf','tikz','reactjs']

def main():
    option_list = args.option.split('+')
    FIGURETARGETS = ''
    TARGETS = ''
    MAKEFILE_CONTENT = ''
    CLEAN = ''
    for option in option_list:
        if option not in VALIDOPTION:
            raise ValueError(option+" is not a valid document output")
        elif option == 'reactjs':
            raise NotImplementedError(option+' is not yet implemented')
        elif option == 'pdf':
            os.makedirs("doc",exist_ok=True)
            Path("doc/main.md").touch()

            with open(str(xdg_data_home())+
                    '/pandoc/templates/makefile_template/pdf_makefile') as file:
                makefile = file.read()

            makefile =pdfmakefilemod(makefile,
                    "log",
                    "../build/pdf",
                    "",
                    "main.md")

            try:
                file_output = open("doc/Makefilepdf",'x')
            except FileExistsError:
                file_output = open("doc/Makefilepdf",'w')
            file_output.write(makefile)
            file_output.close()

            MAKEFILE_CONTENT += '''build/pdf/main.pdf: $(FIGURETARGETS)\n\t$(MAKE) -C doc -f Makefilepdf\n'''
            CLEAN += "\t$(MAKE) -C doc -f Makefilepdf clean\n"
            TARGETS += 'TARGETS += build/pdf/main.pdf\n'

        elif option == "tikz":

            srcdir = "src/tikz"

            os.makedirs(srcdir, exist_ok=True)

            with open(str(xdg_data_home())+
                    '/pandoc/templates/makefile_template/auto_tikz_makefile') as file:
                makefile = file.read()


            # copy yaml defaults
            try:
                file_output = open(srcdir+'/auto_tikz.yaml','x')
                with open(str(xdg_data_home())+
                        '/pandoc/defaults/auto_tikz_default-pandotfiles.yaml') as file:
                    autoyaml = file.read()
                file_output.write(autoyaml)
                file_output.close()
            except FileExistsError:
                warnings.warn("Using existing auto_tikz.yaml config file")

            yaml_config = tikzyamlparse(srcdir+'/auto_tikz.yaml')
            logdir = yaml_config['log_folder']
            tikzfiles = yaml_config['files_makestring']
            builddir = '../../build/tikzpictures'

            makefile = tikzmakefilemod(makefile,
                    'auto_tikz.yaml',
                    builddir,
                    logdir,
                    tikzfiles)

            try:
                file_output = open(srcdir+"/Makefiletikz",'x')
            except FileExistsError:
                file_output = open(srcdir+"/Makefiletikz",'w')
            file_output.write(makefile)
            file_output.close()

            MAKEFILE_CONTENT += '''build/tikz/tikz_stamp: \n\t$(MAKE) -C src/tikz -f Makefiletikz\n'''

            TARGETS += 'TARGETS += build/tikz/tikz_stamp\n'
            FIGURETARGETS += 'FIGURETARGETS += build/tikz/tikz_stamp\n'
            CLEAN += "\t$(MAKE) -C src/tikz -f Makefiletikz clean\n"

    print(TARGETS+FIGURETARGETS+'\n\nall: $(TARGETS)\n\n'+MAKEFILE_CONTENT+'\n\nclean:\n'+CLEAN)



    # with open(str(xdg_data_home())+'/pandoc/templates/makefile_template/auto_tikz_makefile') as file:
    #     makefile = file.read()
    #
    # yaml_config = tikzyamlparse(args.yamlfile)
    # logdir = yaml_config['log_folder']
    # tikzfiles = yaml_config['files_makestring']
    #
    # makefile = sub(r'(yamlfile\s=)(.*)','\\1 '+args.yamlfile, makefile)
    # makefile = sub(r'(builddir\s=)(.*)','\\1 '+args.builddir, makefile)
    # makefile = sub(r'(logdir\s=)(.*)','\\1 '+logdir, makefile)
    # makefile = sub(r'(tikzfiles\s=)(.*)','\\1 '+tikzfiles, makefile)

    # if args.output is not None:
    #     try:
    #         file_output = open(args.output,'x')
    #     except FileExistsError:
    #         file_output = open(args.output,'w')
    #     file_output.write(makefile)
    #     file_output.close()
    # else: print(makefile)

if __name__ == "__main__":
    main()

