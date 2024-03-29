---
lang: en-us
---

# Abstract

This document is prepared using LaTeX2e\cite{Lamport94} and shows the desired format and appearance of a manuscript prepared for the Proceedings of the SPIE.\footnote{The basic format was developed in 1995 by Rick Hermann (SPIE) and Ken Hanson (Los Alamos National Lab.).} It contains general formatting instructions and hints about how to use LaTeX. The LaTeX source file that produced this document, \verb|article.tex| (Version 3.4), provides a template, used in conjunction with \verb|spie.cls| (Version 3.4). These files are available on the Internet at \url{https://www.overleaf.com}. The font used throughout is the LaTeX default font, Computer Modern Roman, which is equivalent to the Times Roman font available on many systems.

# INTRODUCTION

\label{sec:intro}
<!-- % \label{} allows reference to this section-->

Begin the Introduction below the Keywords. The manuscript should not have headers, footers, or page numbers. It should be in a one-column format. References are often noted in the text and cited at the end of the paper.

```{=tex}
\begin{table}[ht]
\caption{Fonts sizes to be used for various parts of the manuscript.  Table captions should be centered above the table.  When the caption is too long to fit on one line, it should be justified to the right and left margins of the body of the text.} 
\label{tab:fonts}
\begin{center}       
\begin{tabular}{|l|l|} %% this creates two columns
%% |l|l| to left justify each column entry
%% |c|c| to center each column entry
%% use of \rule[]{}{} below opens up each row
\hline
\rule[-1ex]{0pt}{3.5ex}  Article title & 16 pt., bold, centered  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Author names and affiliations & 12 pt., normal, centered   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Keywords & 10 pt., normal, left justified   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Abstract Title & 11 pt., bold, centered   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Abstract body text & 10 pt., normal, justified   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Section heading & 11 pt., bold, centered (all caps)  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Subsection heading & 11 pt., bold, left justified  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Sub-subsection heading & 10 pt., bold, left justified  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Normal text & 10 pt., normal, justified  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Figure and table captions & \, 9 pt., normal \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Footnote & \, 9 pt., normal \\
\hline 
\rule[-1ex]{0pt}{3.5ex}  Reference Heading & 11 pt., bold, centered   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Reference Listing & 10 pt., normal, justified   \\
\hline
\end{tabular}
\end{center}
\end{table}
```

```{=tex}
\begin{table}[ht]
\caption{Margins and print area specifications.} 
\label{tab:Paper Margins}
\begin{center}       
\begin{tabular}{|l|l|l|} 
\hline
\rule[-1ex]{0pt}{3.5ex}  Margin & A4 & Letter  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Top margin & 2.54 cm & 1.0 in.   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Bottom margin & 4.94 cm & 1.25 in.  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Left, right margin & 1.925 cm & .875 in.  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Printable area & 17.15 x 22.23 cm & 6.75 x 8.75 in.  \\
\hline 
\end{tabular}
\end{center}
\end{table}
```

LaTeX margins are related to the document's paper size. The paper size is by default set to USA letter paper. To format a document for A4 paper, the first line of this LaTeX source file should be changed to \verb|\documentclass[a4paper]{spie}|.

Authors are encouraged to follow the principles of sound technical writing, as described in Refs.\citenum{Alred03} and \citenum{Perelman97}, for example. Many aspects of technical writing are addressed in the *AIP Style Manual*, published by the American Institute of Physics. It is available on line at \url{https://publishing.aip.org/authors}. A spelling checker is helpful for finding misspelled words.

An author may use this LaTeX source file as a template by substituting his/her own text in each field. This document is not meant to be a complete guide on how to use LaTeX. For that, please see the list of references at \url{http://latex-project.org/guides/} and for an online introduction to LaTeX please see \citenum{Lees-Miller-LaTeX-course-1}.

# FORMATTING OF MANUSCRIPT COMPONENTS

This section describes the normal structure of a manuscript and how each part should be handled. The appropriate vertical spacing between various parts of this document is achieved in LaTeX through the proper use of defined constructs, such as \verb|\section{}|. In LaTeX, paragraphs are separated by blank lines in the source file.

At times it may be desired, for formatting reasons, to break a line without starting a new paragraph. This situation may occur, for example, when formatting the article title, author information, or section headings. Line breaks are inserted in LaTeX by entering \verb|\\| or \verb|\linebreak| in the LaTeX source file at the desired location.

## Title and Author Information

\label{sec:title}

The article title appears centered at the top of the first page. The title font is 16 point, bold. The rules for capitalizing the title are the same as for sentences; only the first word, proper nouns, and acronyms should be capitalized. Avoid using acronyms in the title. Keep in mind that people outside your area of expertise might read your article. At the first occurrence of an acronym, spell it out, followed by the acronym in parentheses, e.g., noise power spectrum (NPS).

The author list is in 12-pt. regular, centered. Omit titles and degrees such as Dr., Prof., Ph.D., etc. The list of affiliations follows the author list. Each author's affiliation should be clearly noted. Superscripts may be used to identify the correspondence between the authors and their respective affiliations. Further author information, such as e-mail address, complete postal address, and web-site location, may be provided in a footnote by using \verb|\authorinfo{}|, as demonstrated above.

## Abstract and Keywords

The title and author information is immediately followed by the Abstract. The Abstract should concisely summarize the key findings of the paper. It should consist of a single paragraph containing no more than 250 words. The Abstract does not have a section number. A list of up to eight keywords should immediately follow the Abstract after a blank line. These keywords will be included in a searchable database at SPIE.

## Body of Paper

The body of the paper consists of numbered sections that present the main findings. These sections should be organized to best present the material. See Sec.\ref{sec:sections} for formatting instructions.

## Appendices

Auxiliary material that is best left out of the main body of the paper, for example, derivations of equations, proofs of theorems, and details of algorithms, may be included in appendices. Appendices are enumerated with uppercase Latin letters in alphabetic order, and appear just before the Acknowledgments and References. Appendix\ref{sec:misc} contains more about formatting equations and theorems.

## Acknowledgments

In the Acknowledgments section, appearing just before the References, the authors may credit others for their guidance or help. Also, funding sources may be stated. The Acknowledgments section does not have a section number.

## References

SPIE is able to display the references section of your paper in the SPIE Digital Library, complete with links to referenced journal articles, proceedings papers, and books, when available. This added feature will bring more readers to your paper and improve the usefulness of the SPIE Digital Library for all researchers. The References section does not have a section number. The references are numbered in the order in which they are cited. Examples of the format to be followed are given at the end of this document.

The reference list at the end of this document is created using BibTeX, which looks through the file \verb|report.bib| for the entries cited in the LaTeX source file. The format of the reference list is determined by the bibliography style file \verb|spiebib.bst|, as specified in the \verb|\bibliographystyle{spiebib}| command. Alternatively, the references may be directly formatted in the LaTeX source file.

For books\cite{Lamport94,Alred03,Goossens97}, the listing includes the list of authors, book title, publisher, city, page or chapter numbers, and year of publication. A reference to a journal article\cite{Metropolis53} includes the author list, title of the article (in quotes), journal name (in italics, properly abbreviated), volume number (in bold), inclusive page numbers, and year. By convention\cite{Lamport94}, article titles are capitalized as described in Sec.\ref{sec:title}. A reference to a proceedings paper or a chapter in an edited book\cite{Gull89a} includes the author list, title of the article (in quotes), volume or series title (in italics), volume number (in bold), if applicable, inclusive page numbers, publisher, city, and year. References to an article in the SPIE Proceedings may include the conference name (in italics), as shown in Ref.\citenum{Hanson93c}. For websites\cite{Lees-Miller-LaTeX-course-1} the listing includes the list of authors, title of the article (in quotes), website name, article date, website address either enclosed in chevron symbols ('(\<)' and '(\>)'), underlined or linked, and the date the website was accessed.

If you use this formatting, your references will link your manuscript to other research papers that are in the CrossRef system. Exact punctuation is required for the automated linking to be successful.

Citations to the references are made using superscript numerals, as demonstrated in the above paragraph. One may also directly refer to a reference within the text, e.g., \`\`as shown in Ref.\citenum{Metropolis53} ...''

## Footnotes

Footnotes\footnote{Footnotes are indicated as superscript symbols to avoid confusion with citations.} may be used to provide auxiliary information that doesn't need to appear in the text, e.g., to explain measurement units. They should be used sparingly, however.

Only nine footnote symbols are available in LaTeX. If you have more than nine footnotes, you will need to restart the sequence using the command \verb|\footnote[1]{Your footnote text goes here.}|. If you don't, LaTeX will provide the error message \verb|Counter too large.|, followed by the offending footnote command.

# SECTION FORMATTING

\label{sec:sections}

Section headings are centered and formatted completely in uppercase 11-point bold font. Sections should be numbered sequentially, starting with the first section after the Abstract. The heading starts with the section number, followed by a period. In LaTeX, a new section is created with the \verb|\section{}| command, which automatically numbers the sections.

Paragraphs that immediately follow a section heading are leading paragraphs and should not be indented, according to standard publishing style\cite{Lamport94}. The same goes for leading paragraphs of subsections and sub-subsections. Subsequent paragraphs are standard paragraphs, with 14-pt. (5 mm) indentation. An extra half-line space should be inserted between paragraphs. In LaTeX, this spacing is specified by the parameter \verb|\parskip|, which is set in \verb|spie.cls|. Indentation of the first line of a paragraph may be avoided by starting it with \verb|\noindent|.

## Subsection Attributes

The subsection heading is left justified and set in 11-point, bold font. Capitalization rules are the same as those for book titles. The first word of a subsection heading is capitalized. The remaining words are also capitalized, except for minor words with fewer than four letters, such as articles (a, an, and the), short prepositions (of, at, by, for, in, etc.), and short conjunctions (and, or, as, but, etc.). Subsection numbers consist of the section number, followed by a period, and the subsection number within that section.

```{=tex}
\subsubsection{Sub-subsection attributes}
```

The sub-subsection heading is left justified and its font is 10 point, bold. Capitalize as for sentences. The first word of a sub-subsection heading is capitalized. The rest of the heading is not capitalized, except for acronyms and proper names.

# FIGURES AND TABLES

Figures are numbered in the order of their first citation. They should appear in numerical order and on or after the same page as their first reference in the text. Alternatively, all figures may be placed at the end of the manuscript, that is, after the Reference section. It is preferable to have figures appear at the top or bottom of the page. Figures, along with their captions, should be separated from the main text by at least 0.2 in. or 5 mm.

Figure captions are centered below the figure or graph. Figure captions start with the figure number in 9-point bold font, followed by a period; the text is in 9-point normal font; for example, \`\`Figure 3. Original image...''. See Fig.\ref{fig:example} for an example of a figure caption. When the caption is too long to fit on one line, it should be justified to the right and left margins of the body of the text.

Tables are handled identically to figures, except that their captions appear above the table.

<!-- ```{=tex} -->
<!-- \begin{figure} [ht] -->
<!--    \begin{center} -->
<!--    \begin{tabular}{c} %% tabular useful for creating an array of images  -->
<!--    \includegraphics[height=5cm]{mcr3b.eps} -->
<!--    \end{tabular} -->
<!--    \end{center} -->
<!--    \caption[example]  -->
<!-- %>>>> use \label inside caption to get Fig. number with \ref{} -->
<!--    { \label{fig:example}  -->
<!-- Figure captions are used to describe the figure and help the reader understand it's significance.  The caption should be centered underneath the figure and set in 9-point font.  It is preferable for figures and tables to be placed at the top or bottom of the page. LaTeX tends to adhere to this standard.} -->
<!--    \end{figure} -->
<!-- ``` -->
![ Figure captions are used to describe the figure and help the reader understand it's significance.  The caption should be centered underneath the figure and set in 9-point font.  It is preferable for figures and tables to be placed at the top or bottom of the page. LaTeX tends to adhere to this standard.](mcr3b.eps){#fig:example height=5cm}

# MULTIMEDIA FIGURES - VIDEO AND AUDIO FILES

Video and audio files can be included for publication. See Tab.\ref{tab:Multimedia-Specifications} for the specifications for the mulitimedia files. Use a screenshot or another .jpg illustration for placement in the text. Use the file name to begin the caption. The text of the caption must end with the text \`\`http://dx.doi.org/doi.number.goes.here'' which tells the SPIE editor where to insert the hyperlink in the digital version of the manuscript.

Here is a sample illustration and caption for a multimedia file:

<!-- ```{=tex} -->
<!-- \begin{figure} [ht] -->
<!--    \begin{center} -->
<!--    \begin{tabular}{c}  -->
<!--    \includegraphics[height=5cm]{MultimediaFigure.jpg} -->
<!--     \end{tabular} -->
<!--     \end{center} -->
<!--    \caption[example]  -->
<!--    { \label{fig:video-example}  -->
<!-- A label of “Video/Audio 1, 2, …” should appear at the beginning of the caption to indicate to which multimedia file it is linked . Include this text at the end of the caption: \url{http://dx.doi.org/doi.number.goes.here}} -->
<!--    \end{figure} -->
<!-- ``` -->
![A label of “Video/Audio 1, 2, …” should appear at the beginning of the caption to indicate to which multimedia file it is linked . Include this text at the end of the caption: \url{http://dx.doi.org/doi.number.goes.here}](MultimediaFigure.jpg){#fig:video-example height=5cm}

```{=tex}
\begin{table}[ht]
\caption{Information on video and audio files that must accompany a manuscript submission.} 
\label{tab:Multimedia-Specifications}
\begin{center}       
\begin{tabular}{|l|l|l|}
\hline
\rule[-1ex]{0pt}{3.5ex}  Item & Video & Audio  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  File name & Video1, video2... & Audio1, audio2...   \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Number of files & 0-10 & 0-10  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  Size of each file & 5 MB & 5 MB  \\
\hline
\rule[-1ex]{0pt}{3.5ex}  File types accepted & .mpeg, .mov (Quicktime), .wmv (Windows Media Player) & .wav, .mp3  \\
\hline 
\end{tabular}
\end{center}
\end{table}
```

\appendix    

# MISCELLANEOUS FORMATTING DETAILS

\label{sec:misc}

It is often useful to refer back (or forward) to other sections in the article. Such references are made by section number. When a section reference starts a sentence, Section is spelled out; otherwise use its abbreviation, for example, `In Sec.~2 we showed...'' or`Section 2.1 contained a description...''. References to figures, tables, and theorems are handled the same way.

## Formatting Equations

Equations may appear in line with the text, if they are simple, short, and not of major importance; e.g., $\beta = b/r$. Important equations appear on their own line. Such equations are centered. For example, \`\`The expression for the field of view is
\begin{equation}
\label{eq:fov}
2 a = \frac{(b + 1)}{3c} \, ,
\end{equation}
where $a$ is the ...'' Principal equations are numbered, with the equation number placed within parentheses and right justified.

Equations are considered to be part of a sentence and should be punctuated accordingly. In the above example, a comma follows the equation because the next line is a subordinate clause. If the equation ends the sentence, a period should follow the equation. The line following an equation should not be indented unless it is meant to start a new paragraph. Indentation after an equation is avoided in LaTeX by not leaving a blank line between the equation and the subsequent text.

References to equations include the equation number in parentheses, for example, `Equation~(\ref{eq:fov}) shows ...'' or`Combining Eqs.(2) and (3), we obtain...'' Using a tilde in the LaTeX source file between two characters avoids unwanted line breaks.

## Formatting Theorems

To include theorems in a formal way, the theorem identification should appear in a 10-point, bold font, left justified and followed by a period. The text of the theorem continues on the same line in normal, 10-point font. For example,

\noindent\textbf{Theorem 1.} For any unbiased estimator...

Formal statements of lemmas and algorithms receive a similar treatment.

<!--\acknowledgments % equivalent to-->

# ACKNOWLEDGMENTS {#acknowledgments-1 .unnumbered}

This unnumbered section is used to identify those who have aided the authors in understanding or accomplishing the work presented and to acknowledge sources of funding.
