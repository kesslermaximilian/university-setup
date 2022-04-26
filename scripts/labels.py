#!/usr/bin/python3
from pathlib import Path
from rofi import rofi
import sys


def fancy(label, number):
    return f"{label} ({number})"


def remove_duplicates(ls):
    new_list = []
    [new_list.append(elem) for elem in ls if not elem in new_list]
    return new_list


def get_labels(path):
    file = open(path, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    file.close()
    lines = [line for line in lines if
             '\\newlabel' in line and '{' in line and not '@' in line and not 'gdef' in line and not 'LastPage' in line]

    labels = [line.split('{')[1].split('}')[0] for line in lines]
    numbers = [line.split('{')[3].split('}')[0] for line in lines]
    options = [fancy(label, number) for (label, number) in zip(labels, numbers)]
    return labels, options


def get_all_labels(pathlist):
    labels = []
    options = []
    for path in pathlist:
        try:
            nlabels, noptions = get_labels(path)
        except:
            continue

        labels += nlabels
        options += noptions
    unique = remove_duplicates(zip(labels, options))
    return [a for (a, b) in unique], [b for (a, b) in unique]


def main(args):
    arglist = []
    if len(args) > 1:
        path = Path(args[1])
        arglist = list(path.glob('*.aux')) + list(path.glob('build/*.aux'))
    else:
        arglist = ['/home/maximilian/current_course/full.aux']

    labels, options = get_all_labels(arglist)

    key, index, selected = rofi('Select label', options, [
        '-lines', min(40, max(len(options), 5)), '-width', '1700'
    ])

    if index >= 0:
        command = labels[index]
    else:
        command = selected
    return command.strip()
   


if __name__ == '__main__':
    selected_label = main(sys.argv)
    print(selected_label)
