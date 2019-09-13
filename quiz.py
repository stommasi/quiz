#!/usr/bin/env python3

# Quiz

import re
import random
from argparse import ArgumentParser

def quiz_user(qlist):
    while qlist:
        total = len(qlist)
        i = random.randrange(0, total)
        question, answer = qlist[i]
        print("\n{}\n".format(total))
        print(question)

        user_answer = ''
        while True:
            line = input()
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

def load_file(filename):
    pattern = re.compile(r'^\S')
    with open(filename, 'r') as f:
        qlist = []
        question = ''
        answer = ''
        for line in f:
            if pattern.match(line):
                if question and answer:
                   qlist.append((question, unindent(answer)))
 
                question = line
                answer = ''
            else:
                answer += line
    return qlist

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    qlist = load_file(args.filename)
    quiz_user(qlist)
