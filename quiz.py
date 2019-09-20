#!/usr/bin/env python3

# Quiz

import re
import random
import sys
from argparse import ArgumentParser

def get_input():
    try:
        return input()
    except (KeyboardInterrupt, EOFError):
        print("")
        sys.exit(1)

def quiz_user(qlist):
    while qlist:
        total = len(qlist)
        i = random.randrange(0, total)
        question, answer = qlist[i]
        print("\n{}\n".format(total))
        print(question)

        user_answer = ''
        while True:
            line = get_input()
            if line == '':
                break
            else:
                user_answer += line

        if ' '.join(user_answer.split()) == ' '.join(answer.split()):
            del qlist[i]

        print(answer)

def unindent(text):
    text = text.rstrip()
    m = re.match(r'^\s+', text)
    return re.sub(r'(^|\n)' + m.group(), r'\1', text)

def load_file(filename, sections):
    pattern = re.compile(r'^\S')
    s = 0
    with open(filename, 'r') as f:
        qlist = []
        question = ''
        answer = ''
        for line in f:
            if line.startswith("#"):
                s += 1
            elif pattern.match(line):
                if question and answer and (not sections or s in sections):
                   qlist.append((question, unindent(answer)))
 
                question = line
                answer = ''
            else:
                answer += line
    return qlist

def list_sections(filename):
    pattern = re.compile(r'^#\s*')
    c = 0
    print("")
    with open(filename, 'r') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                c += 1
                print(re.sub(m.group(), str(c) + ' - ', line))

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
        list_sections(args.filename)
    else:
        qlist = load_file(args.filename, sections)
        quiz_user(qlist)
