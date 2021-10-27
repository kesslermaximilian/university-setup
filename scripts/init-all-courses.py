#!/bin/python3
from courses import Courses

MASTER_FILE_TEXT=[
    r'\documentclass[a4paper, {language}, fancyfoot, git]{{mkessler-script}}',
    r'',
    r'\course{{{course}}}',
    r'\lecturer{{{lecturer}}}',
    r'\assistant{{{assistant}}}',
    r'\author{{{author}}}',
    r'',
    r'',
    r'\usepackage{{{package_name}}}',
    r'\restatesetup{{strict=false}}',
    r'',
    r'\begin{{document}}',
    r'    \maketitle',
    r'    \begin{{abstract}}',
    r'        {{\color{{red}} Caution: This version is only intended for editing. Some parts are missing, todo notes are compiled. For the correct version of the notes, please see the full version on\href{{{github}}}{{GitHub}}}}.',
    r'    \end{{abstract}}',
    r'    \newpage',
    r'    \listoftodos',
    r'    \newpage',
    r'    \summaryoflectures',
    r'    \newpage',
    r'    % start lectures',
    r'    % end lectures',
    r'\end{{document}}'
]

FULL_FILE_TEXT= [
    r'\documentclass[a4paper, {language}, fancyfoot, git, dvipsnames]{{mkessler-script}}',
    r'',
    r'\course{{{course}}}',
    r'\lecturer{{{lecturer}}}',
    r'\assistant{{{assistant}}}',
    r'\author{{{author}}}',
    r'',
    r'\usepackage{{{package_name}}}',
    r'\setuptodonotes{{disable}}',
    r'\restatesetup{{strict=true}}',
    r'',
    r'\import{inputs/exercises/}{preamble_exercise_sheets.tex}',
    r'',
    r'\begin{document}',
    r'    \maketitle',
    r'',
    r'    \import{inputs/}{abstract.tex}',
    r'',
    r'    %Table of contents',
    r'    \cleardoublepage',
    r'    \tableofcontents',
    r'',
    r'    %List of lectures with their corresponding keywords',
    r'    \cleardoublepage',
    r'    \summaryoflectures',
    r'',
    r'    \cleardoublepage',
    r'    % start lectures',
    r'    % end lectures',
    r'',
    r'    %Start appendix',
    r'    \cleardoublepage',
    r'    \appendix',
    r'    \part{Appendix}',
    r'',
    r'    %Index',
    r'    \cleardoublepage',
    r'    \printvocabindex',
    r'',
    r'    %Image attributions',
    r'    %\cleardoublepage',
    r'    %\printimageattributions',
    r'',
    r'    %Literature',
    r'    %\cleardoublepage',
    r'    %\printliterature',
    r'\end{document}'
]

for course in Courses():
        lectures = course.lectures
        course_title = lectures.course.info["title"]
        lines = [r'\documentclass[a4paper]{article}',
                 r'\input{../preamble.tex}',
                 fr'\title{{{course_title}}}',
                 r'\begin{document}',
                 r'    \maketitle',
                 r'    \tableofcontents',
                 fr'    % start lectures',
                 fr'    % end lectures',
                 r'\end{document}'
                ]
        lectures.master_file.touch()
        lectures.master_file.write_text('\n'.join(lines))
        (lectures.root / 'master.tex.latexmain').touch()
        (lectures.root / 'figures').mkdir(exist_ok=True)
