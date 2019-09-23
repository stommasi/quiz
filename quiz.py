#!/usr/bin/env python3

# Quiz

import re, sys
from random import randrange
from argparse import ArgumentParser

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

def get_input():
    try:
        return input()
    except (KeyboardInterrupt, EOFError):
        print("")
        sys.exit(1)

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

def list_sections(filename):
    pattern = re.compile(r'^#\s*(\S.*)$')
    l = []
    with open(filename, 'r') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                l.append(m.group(1))
        return l

def answers_equal(user_answer, answer):
    return ' '.join(user_answer.split()) == ' '.join(answer.split())

def unindent(text):
    text = text.rstrip()
    m = re.match(r'^\s+', text)
    return re.sub(r'(^|\n)' + m.group(), r'\1', text)

def get_random(qlist):
    i = randrange(0, len(qlist))
    question, answer = qlist[i]
    return (question, answer, i)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-s")
    parser.add_argument("filename")
    args = parser.parse_args()

    sections = args.s or None
    if sections:
        sections = [int(n) for n in sections.split(',')]

    if args.l:
        for i, s in enumerate(list_sections(args.filename)):
            print(i + 1, s)
    else:
        qlist = load_file(args.filename, sections)
        quiz_user(qlist)
