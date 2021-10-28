FROM pandoc/latex:latest

RUN apk --no-cache add make python3 perl ncurses
RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip
RUN tlmgr install latexmk

# CACHE common packages
RUN tlmgr install selnolig siunitx glossaries mfirstuc xfor datatool tracklang blindtext
RUN tlmgr install lastpage sectsty multibib ulthese pgf 


# OSA-ARTICLE
RUN tlmgr install fontaxes xstring silence newtx helvetic txfonts
RUN luaotfload-tool --update
ENTRYPOINT make pdf
