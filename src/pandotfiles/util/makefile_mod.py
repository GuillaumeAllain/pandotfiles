from re import escape


def pdfmakefilemod(makefile_string, logdir, builddir, srcdir, mainfile):

    makefile_string = str(makefile_string).format(
        logdir=escape(logdir),
        builddir=escape(builddir),
        pandocfiles="\\1 $(wildcard "
        + escape(str(srcdir))
        + "/*.md)"
        + " $(wildcard "
        + escape(str(srcdir))
        + "/*.bib)",
        mainfile=escape(mainfile),
    )
    # makefile_string = sub(r"(logdir\s=)(.*)", "\\1 " + str(logdir), makefile_string)
    # makefile_string = sub(r"(builddir\s=)(.*)", "\\1 " + str(builddir), makefile_string)
    # makefile_string = sub(
    #     r"(pandocfiles\s=)(.*)",
    #     "\\1 $(wildcard "
    #     + str(srcdir)
    #     + "/*.md)"
    #     + " $(wildcard "
    #     + str(srcdir)
    #     + "/*.bib)",
    #     makefile_string,
    # )
    # makefile_string = sub(r"(mainfile\s=)(.*)", "\\1 " + str(mainfile), makefile_string)

    return makefile_string


def tikzmakefilemod(makefile_string, yamlfile, builddir, logdir, tikzfiles):

    makefile_string = str(makefile_string).format(
        yamlfile=escape(yamlfile),
        builddir=escape(builddir),
        logdir=escape(logdir),
        tikzfiles=escape(tikzfiles),
    )

    # makefile_string = sub(r"(yamlfile\s=)(.*)", "\\1 " + yamlfile, makefile_string)
    # makefile_string = sub(r"(builddir\s=)(.*)", "\\1 " + builddir, makefile_string)
    # makefile_string = sub(r"(logdir\s=)(.*)", "\\1 " + logdir, makefile_string)
    # makefile_string = sub(r"(tikzfiles\s=)(.*)", "\\1 " + tikzfiles, makefile_string)

    return makefile_string
