import argparse
import warnings
from os.path import splitext, basename

from pandotfiles.util.parser import tikzyamlparse

parser = argparse.ArgumentParser(
    description="""Auto generate a TEX file to compile all tikz (*.tikz) file from a repo.
                   Can use configuration provided by a YAML file with the following fields,
                   all of which are optional:"""
    + r"""
                       packages :
                           - {name: "name", options: "option1", "option2"}
                       tikzlibraries :
                           - {name: "name", options: "option1", "option2"}
                       font: "Font police name"
                       font_size: "12 pt"
                       src_folder: "tikz"
                       log_folder: "log"
                       output: "output_filename"
                       files:
                           - file1.tikz
                           - file2.tikz
                       """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output file location. Overrides YAML file. Default: output to terminal (T)",
    default=None,
)

parser.add_argument(
    "-y",
    "--yamlfile",
    type=str,
    help="YAML file location. Default: ./auto_tikz.yaml",
    default="auto_tikz.yaml",
)

args = parser.parse_args()


def generate_latex_file(data_dic):

    LATEX_FILE_HEADER = "%    TIKZ PREPROCESSOR\n"
    LATEX_FILE_HEADER += "%AUTOGENERATED BY AUTO_TIKZ\n"
    LATEX_FILE_HEADER += "%---------------------------\n"
    LATEX_FILE_HEADER += "\\documentclass[" + data_dic["font_size"] + "]{article}\n"
    if "font" in data_dic.keys():
        LATEX_FILE_HEADER += "\\usepackage{fontspec}\n"
        LATEX_FILE_HEADER += "\\setmainfont{" + data_dic["font"] + "}\n"
    LATEX_FILE_HEADER += "\\usepackage{tikz}\n"
    LATEX_FILE_HEADER += "\\usetikzlibrary{external}\n"
    LATEX_FILE_HEADER += (
        r"\immediate\write18{mkdir -p " + data_dic["log_folder"] + "/log}\n"
    )
    LATEX_FILE_HEADER += (
        r"\tikzexternalize[prefix=" + data_dic["log_folder"] + "/ ,optimize=false]\n"
    )

    LATEX_PACKAGES = ""
    try:
        for packages in data_dic["packages"]:
            latex_package_local = "\\usepackage"
            if "options" in packages.keys():
                latex_package_local += "["
                if isinstance(packages["options"], list):
                    for locoptions in packages["options"]:
                        latex_package_local += locoptions + ", "
                else:
                    latex_package_local += packages["options"]
                latex_package_local += "]"
            latex_package_local += "{"
            try:
                latex_package_local += packages["name"] + "}\n"
            except KeyError:
                raise KeyError("Package entry must have name")
            LATEX_PACKAGES += latex_package_local
    except KeyError:
        LATEX_PACKAGES = ""

    LATEX_TIKZLIBRARY = ""
    try:
        for tikzlibraries in data_dic["tikzlibraries"]:
            latex_tikzlibrary_local = "\\usetikzlibrary"
            if "options" in tikzlibraries.keys():
                latex_tikzlibrary_local += latex_package_local + "["
                for locoptions in tikzlibraries["options"]:
                    latex_tikzlibrary_local += locoptions
                latex_tikzlibrary_local += "]"
            latex_tikzlibrary_local += "{"
            try:
                latex_tikzlibrary_local += tikzlibraries["name"] + "}\n"
            except KeyError:
                raise KeyError("Package entry must have name")
            LATEX_TIKZLIBRARY += latex_tikzlibrary_local
    except KeyError:
        LATEX_TIKZLIBRARY = ""

    LATEX_BEGIN_DOCUMENT = "\\begin{document}\n"

    LATEX_FILE_INPUT = ""
    for file in data_dic["files"]:
        LATEX_FILE_INPUT += (
            "\\tikzsetnextfilename{" + splitext(basename(file))[0] + "}\n"
        )
        LATEX_FILE_INPUT += "\\input{" + file + "}\n"

    LATEX_END_DOCUMENT = "\\end{document}"
    content = ""
    content += LATEX_FILE_HEADER
    content += LATEX_PACKAGES
    content += LATEX_TIKZLIBRARY
    content += LATEX_BEGIN_DOCUMENT
    content += LATEX_FILE_INPUT
    content += LATEX_END_DOCUMENT
    return content


def main():

    yaml_config = tikzyamlparse(args.yamlfile)

    if "output" not in yaml_config.keys() and args.output is None:
        warnings.warn(
            "No explicit output file defined for tikz file, directing to terminal."
        )
        yaml_config["output"] = None

    elif ("output" in yaml_config.keys()) and (args.output is not None):
        warnings.warn("Conflicting output definition, using CLI argument definition")
        yaml_config["output"] = args.output

    elif ("output" not in yaml_config.keys()) and (args.output is not None):
        # warnings.warn("Conflicting output definition, using YAML config definition")
        yaml_config["output"] = args.output

    content = generate_latex_file(yaml_config)

    if yaml_config["output"] == "T":
        print(content)
    elif yaml_config["output"] is not None:
        try:
            file_output = open(yaml_config["output"], "x")
        except FileExistsError:
            file_output = open(yaml_config["output"], "w")
        file_output.write(content)
        file_output.close()
    else:
        print(content)


if __name__ == "__main__":
    main()
