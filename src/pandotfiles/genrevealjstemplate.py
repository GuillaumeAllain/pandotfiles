#!/usr/bin/env python

"""
File: update_pandoc_revealjs_template.py
Author: Guillaume Allain
Email: guillaum.allain@gmail.com
Github: https://github.com/guillaumeallain
Description: Inject your own template into pandoc's default
"""

import re
from codecs import decode
from subprocess import run


def main():

    result = run("/usr/local/bin/pandoc -D revealjs", shell=True, capture_output=True)

    base_template = decode(result.stdout)

    base_template = re.sub(
        r'<p class="subtitle">(.*)</p>', r'<h3 class="subtitle">\1</h3>', base_template
    )

    return base_template


if __name__ == "__main__":
    print(main())
