header = r'''
\documentclass{book}

\usepackage[utf8]{inputenc} % utf-8 encoding: always use this!
% specify hot links

%% specify the page size and margins. Here, we use A4 paper
\usepackage[a4paper,top=20mm,bottom=25mm,left=25mm,right=25mm]{geometry}
%		Typically, the margins will not be specified but, in this case, they are specified in 
%		order to minimise line wrapping in the content.
%		For reference, format for First Folio page size:
%		\usepackage[height=335mm,width=235mm,top=20mm,bottom=25mm,left=20mm,right=25mm]{geometry}

% specify the styles of the title and section headings
\usepackage[small,bf,it,sc,rm,center,compact]{titlesec}
%		the titles are specified to be small, bold, italic, small caps, roman, centered and compact.
%		try removing any or all of the parameters to alter the display.

%% keep open the option of using balanced multicolumns:
\usepackage{multicol}

\usepackage{graphicx} % include graphics, as on our title page
\usepackage{fancyhdr} % fancy page headers: definitely the way to go

% Code for creating empty pages
% No headers on empty pages before new chapter see http://www.markschenk.com/tensegrity/latexexplanation.html
\makeatletter
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
    \hbox{}
    \thispagestyle{empty}
    \newpage
    \if@twocolumn\hbox{}\newpage\fi\fi\fi}
\makeatother \clearpage{\pagestyle{plain}\cleardoublepage}

% parindent allows us to control the appearance of text blocks.
% a positive value indents the first line, while a negative value outdents the first line,
% so that any wrapped lines appear indented. This is worth experimenting with.

% it is normally not necessary to specify the space between lines and between columns, but space is at a premium
% when setting out columns
 
\setlength\parindent{0em}% wrapped lines are aligned with the first line (try indenting them).
\setlength\parskip{2pt plus1pt minus1pt} % limit the space between paras (here, they are mostly single lines).
\setlength\columnsep{20mm} % setting for the body of the document

%% choice of standard fonts (font height and line height). You will not need all of these!
\newcommand{\chanceryfont}{\fontsize{9}{10.5}\usefont{T1}{pzc}{m}{il}}
\newcommand{\avantgardefont}{\fontsize{9}{10.5}\usefont{T1}{pag}{m}{n}}
\newcommand{\helveticafont}{\fontsize{10}{11.5}\usefont{T1}{phv}{m}{n}}
\newcommand{\courierfont}{\fontsize{10}{11.5}\usefont{T1}{pcr}{m}{n}}
\newcommand{\timesfont}{\fontsize{10}{10.5}\usefont{T1}{ptm}{m}{n}}
\newcommand{\charterfont}{\fontsize{10}{11.5}\usefont{T1}{pch}{m}{n}}
\newcommand{\bookmanfont}{\fontsize{10}{11.5}\usefont{T1}{pbk}{m}{n}}
\newcommand{\palatinofont}{\fontsize{10}{11.5}\usefont{T1}{ppl}{m}{n}}
\setcounter{secnumdepth}{-2} % suppress automatic numbering of headings: try commenting this out!

\newcommand{\HRule}{\noindent\rule{\linewidth}{1.5pt}} % rules on the title page.
\newcommand{\FRule}{\noindent\rule{\linewidth}{0.25pt}} % rules for section headings.

% The following are new definitions for styling a play, with Act/Scene headings and speeches
% that include: speaker, speech content, as well as inline and block stage directions.
% They are intended to interact and simplify the restyling of the final document.
% Note that most start with an uppercase letter to avoid clashes with standard LaTeX definitions.

%% Content blocks
\newcommand{\Act}[1]{\chapter{#1}}
\newcommand{\Scene}[1]{\FRule\section{#1}\vspace*{-1ex}\FRule\vspace*{2ex}}
\newcommand{\PgScene}[1]{\NewPage\FRule\section{#1}\vspace*{-1ex}\FRule\vspace*{2ex}}

%% Verse control
\newcommand{\Speaker}{\textsc } % speaker in small caps
\newcommand{\Spk}[1]{\Tab\Speaker{#1}} % full stop (period) after the speaker.
\newcommand{\Indent}[1]{\begin{quote}#1\end{quote}} 
\newcommand{\Tab}{\vspace*{1ex}\hspace*{-1.0em}}% negative indent gives outdent: used for the speaker line
\newcommand{\I}{\hspace*{1em}}
\newcommand{\V}{\vspace*{2ex}}

%% page header management
\newcommand{\HideHeaderLine}{\renewcommand\headrulewidth{0.0pt}}
\newcommand{\ShowHeaderLine}{\renewcommand\headrulewidth{0.4pt}}

%% line and block management
\newenvironment{indentpar}[1]
{\begin{list}{}%
  {\setlength{\leftmargin}{#1} \setlength{\rightmargin}{#1}} \item[]}
{\end{list}}

\newenvironment{smallquote}{\vspace*{-5ex}\list{}{\leftmargin=0.5em\rightmargin=2em}\item[]}{\endlist}

\newcommand{\Gap}{{\vspace{0.5ex}}}% gap above a block
\newcommand{\Blk}[1]{\setlength\topsep{-0.5ex}\begin{trivlist}\item[]#1\end{trivlist}}% compact indented block: reduced space above and below and no indentation.
\newcommand{\sd}[1]{\emph{#1}}
% 		This is an inline emphasis string.
\newcommand{\ActSD}[1]{\begin{center}\large\textsc{#1}\end{center}}
%		This is an emphasis block for at the start of an Act, and not inside a Scene
\newcommand{\SD}[1]{{\setlength\topsep{-0.5ex}\begin{trivlist}\item[]\textit{#1}\end{trivlist}}}
%		This is a compact italicised emphasis block: reduced space above and below and no indentation.
\newcommand{\IB}[1]{{\begin{smallquote}\item[]#1\end{smallquote}}}

\newcommand{\Sf}{\sffamily } % sansserif font: better than a typewriter font
%		Note that this is a declaration, and requires no braces (note the trailing space)

%		Hooks for page breaks: to simplify testing of final layout and hard page breaks
%\newcommand{\NewPage}{}% a dummy page break.
\newcommand{\NewPage}{\vfill\pagebreak}% use this definition to disable all page breaks.
\newcommand{\ForcePage}{\vfill\pagebreak}% a necessary page break without vfill
\newcommand{\NoPage}{}% no page break: to simplify testing of individual page breaks.
\newcommand{\Page}{\pagebreak}% a hook for a page break that can be redefined. Here, there is no vfill.

\newcommand{\Globals}{\timesfont\raggedright}
%		remove these declarations from the document body
\newcommand{\Columns}{\twocolumn}
%		beware: this declaration can trigger an unwanted page break

\usepackage[colorlinks, linkcolor=blue]{hyperref}
\begin{document}
'''


book_sample = {
    'title': "Stormen",
    'intro':
        [
        "ALONZO, konung af Neapel.",
        "SEBASTIAN, hans bror."
        ],
    'acts':
        [
            {
            'title': "Act I",
            'scenes':
                [
                    {
                    'title': "Scene I",
                    'lines':
                        [
                        "Vill ägget lära hönan värpa?",
                        "Den trösten smakar honom som kall soppa."
                        ]
                    }
                ]
            }
        ]
    }


def generate_title(title):
    return r'''
\thispagestyle{empty} %% no headers or footers
\HideHeaderLine
\vspace*{\stretch{2}}
\HRule
\begin{center}\Huge\itshape\bfseries {%s}\end{center}
\HRule
\pagestyle{fancy}
\fancyhead{}
\NewPage\pagenumbering{roman}
''' % (title)

def generate_intro(intro):
    return ''

def generate_scene(scene):
    result = r'''
\Scene{%s}
''' % (scene['title'])
    for line in scene['lines']:
        result += line
        result += '\n\n'
    return result

def generate_act(act):
    result = r'''
    \Columns
\pagestyle{fancy}
\fancyhead{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\rightmark}

\Act{%s}

''' % (act['title'])
    for scene in act['scenes']:
        result += generate_scene(scene)
    return result

def generate_book(book):
    result = header
    result += generate_title(book['title'])
    result += generate_intro(book['intro'])
    for act in book['acts']:
        result += generate_act(act)
    result += r'''\end{document}'''
    return result


if __name__ == '__main__':
    book = generate_book(book_sample)
    print(book)