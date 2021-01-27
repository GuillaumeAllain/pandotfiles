import warnings
from os import listdir
from pathlib import Path
from os.path import splitext

from ruamel_yaml import YAML

def tikzyamlparse(file_path):
    yaml = YAML()

    try:
        yaml_config = yaml.load(Path(file_path))
    except FileNotFoundError as fnofe:
        raise FileNotFoundError("No configuration file found in "+file_path) from fnofe

    if 'log_folder' not in yaml_config.keys():
        warnings.warn("No explicit source folder defined for tikz file, using 'log'")
        yaml_config["log_folder"] = 'log'

    if 'files' in yaml_config.keys():
        yaml_config['files'] = (list(set(yaml_config['files'])))
        yaml_config['files_makestring'] = str(' ').join(yaml_config['files'])

    else:
        warning_string = "No explicit file list defined for tikz file, "
        warning_string += "using all tex files in source folder."
        if 'src_folder' not in yaml_config.keys():
            warnings.warn("No explicit source folder defined for tikz file, using 'tikz'")
            yaml_config["src_folder"] = 'tikz'
        warnings.warn(warning_string)
        yaml_config['files'] = [yaml_config['src_folder']+'/'+x for x in
                                listdir(yaml_config['src_folder']) if splitext(x)[1] == '.tikz']
        yaml_config['files_makestring'] = "$(wildcard " + yaml_config['src_folder'] + "/*.tikz)"


    if 'font_size' not in yaml_config.keys():
        yaml_config['font_size'] = str(12)

    return yaml_config
