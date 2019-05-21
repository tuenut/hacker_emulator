import os
import sys
import random

from coder import CodePrinter

def massive_run(path):
    paths = list()
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if file_.endswith(('.h', '.c')):
                file_path = os.path.join(root, file_)
                paths.append(file_path)

    coder = CodePrinter()

    while True:
        file_path = random.choice(paths)
        if coder.file_path != file_path:
            coder.file_path = file_path
            coder.print()

def single_run(path):
    coder = CodePrinter(path)
    coder.print()

if __name__ == "__main__":
    if '-single' in sys.argv:
        single_run(sys.argv[sys.argv.index('-single')+1])
    else:
        massive_run(sys.argv[1])


