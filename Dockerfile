FROM pandoc/latex:latest

RUN apk --no-cache add make python3 perl ncurses rsync openjdk11
RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

# CACHE common packages
RUN tlmgr install latexmk 
RUN tlmgr install selnolig siunitx glossaries mfirstuc xfor datatool tracklang blindtext
RUN tlmgr install lastpage sectsty multibib ulthese pgf preprint cite tocloft glossaries-extra
RUN tlmgr install francais-bst bib2gls pdfpages

# OSA-ARTICLE
RUN tlmgr install fontaxes xstring silence newtx helvetic txfonts collection-fontsrecommended
RUN luaotfload-tool --update

ENTRYPOINT make pdf
