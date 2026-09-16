import os
import shutil
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
    public = os.path.abspath("public")
    shutil.rmtree(public)
    os.mkdir(public)
    static = os.path.abspath("static")
    recurse_copy(public, static)
    template = os.path.abspath("template.html")
    generate_pages_recursive(os.path.abspath("content"), template, public)


main()