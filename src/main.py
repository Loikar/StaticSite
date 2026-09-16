import os
import shutil
import sys
from convert import generate_page, generate_pages_recursive

def recurse_copy(curr_public_dir, curr_static_dir):
    curr_dir = os.listdir(curr_static_dir)
    for i in curr_dir:
        j = os.path.join(curr_static_dir, i)
        if os.path.isfile(j):
            shutil.copy(j, curr_public_dir)
        else:
            next = os.path.join(curr_public_dir, i)
            os.mkdir(next)
            recurse_copy(next, j)

def main():
    if sys.argv:
        basepath = sys.argv
    else:
        basepath = "/"
    docs = os.path.abspath("docs")
    shutil.rmtree(docs)
    os.mkdir(docs)
    static = os.path.abspath("static")
    recurse_copy(docs, static)
    template = os.path.abspath("template.html")
    generate_pages_recursive(os.path.abspath("content"), template, docs, basepath)


main()