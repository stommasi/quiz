#!/usr/bin/env python3

# quiz - interactive quiz for command line that pulls question/answer pairs from
# a text file

# Drawing on a specially formatted text file as its source, quiz helps the user
# memorize a series of answers to questions or clues. The program prompts the
# user with a randomly selected question and the user types in the answer. If
# the answer is correct, the pair is withdrawn from the series and won't come up
# again during the session. A question in the text file must be one line and
# must not begin with any spaces or tabs. The answer must follow on the next
# line and can be any number of lines, each of which must begin with at least
# one space or tab. It is also possible to denote sections with a leading '#',
# which can then be listed and chosen from the command line to limit the scope
# of a study session. This program is useful for memorizing Unix commands and
# programming language syntax.

import re, sys
from random import randrange
from argparse import ArgumentParser

# The main quiz loop. Print a random question, get a potentially multi-line
# answer from the user until a blank line is entered, and test for equality. If
# the answers are equal, delete it from qlist. Print the correct solution in
# either case.
def quiz_user(qlist):
    while qlist:
        question, answer, i = get_random(qlist)
        print("\n{}\n".format(len(qlist)))
        print(question)

        user_answer = ''
        while True:
            line = get_input()
            if line == '':
                break
            else:
                user_answer += line + "\n"

        if answers_equal(user_answer, answer):
            del qlist[i]

        print(unindent(answer))

# Get user input. Quit the program on Ctrl-C or Ctrl-D.
def get_input():
    try:
        return input()
    except (KeyboardInterrupt, EOFError):
        print("")
        sys.exit(1)

# Take a filename and a list of section numbers, return a list of lists of
# question/answer pairs. If specific sections have been specified as an argument
# on the command line, only store pairs from those sections. Use regular
# expressions to distinguish questions from answers.
def load_file(filename, sections):
    q = re.compile(r'^\S')
    a = re.compile(r'^\s+\S+')
    s = 0
    with open(filename, 'r') as f:
        qlist = []
        for line in f:
            if line.startswith("#"):
                s += 1
            elif not sections or s in sections:
                if q.match(line):
                    qlist.append([line, ''])
                elif a.match(line):
                    qlist[-1][1] += line
    return qlist

# Take a filename and return a list of sections, if any, denoted in the text
# file by a leading '#' symbol.
def list_sections(filename):
    pattern = re.compile(r'^#\s*(\S.*)$')
    l = []
    with open(filename, 'r') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                l.append(m.group(1))
        return l

# Test the correctness of an answer. Take extra tabs and spaces out of
# consideration.
def answers_equal(user_answer, answer):
    return ' '.join(user_answer.split()) == ' '.join(answer.split())

# Remove the spaces or tabs used to indent the answer in the text file, but not
# the spaces or tabs that are part of the actual answer (as in programming
# syntax). This only works on multi-line answers if the lines are indented
# uniformly.
def unindent(text):
    text = text.rstrip()
    m = re.match(r'^\s+', text)
    return re.sub(r'(^|\n)' + m.group(), r'\1', text)

# Take a list of question/answer lists and return a tuple consisting of the
# question, answer, and the pair's index in the list (needed for deleting it
# later).
def get_random(qlist):
    i = randrange(0, len(qlist))
    question, answer = qlist[i]
    return (question, answer, i)

if __name__ == "__main__":
    # The command line option -l will list any sections denoted in the text
    # file. The option -s, followed by a series of comma-separated numbers (e.g.
    # -s 1,2,3) tells the program which sections of question/answer pairs to
    # draw from.
    parser = ArgumentParser()
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-s")
    parser.add_argument("filename")
    args = parser.parse_args()

    # Store a list of section numbers.
    sections = args.s or None
    if sections:
        sections = [int(n) for n in sections.split(',')]

    # Print the list of sections if -l called.
    if args.l:
        for i, s in enumerate(list_sections(args.filename)):
            print(i + 1, s)
    # Or load the file into qlist and run the quiz.
    else:
        qlist = load_file(args.filename, sections)
        quiz_user(qlist)
