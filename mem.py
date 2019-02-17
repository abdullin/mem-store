import os
import sys
from os import path

import click

import store


@click.group()
def main():
   pass





@main.command()
def init():

    if os.path.isdir(store.FOLDER_NAME):
        print("{0} folder already exists".format(store.FOLDER_NAME))
        pass


    os.makedirs(store.FOLDER_NAME)
    print("{0} folder created".format(store.FOLDER_NAME))



def _ensure_root(file):
    root = store.find_root(file)
    if not root:
        sys.exit("Error: No memory store found in parent path")
    return root

@main.command()
@click.argument('file')
def fix(file):
    root = _ensure_root(file)
    store.fix_file(root, file)


@main.command()
@click.argument('file')
def add(file):
    root = _ensure_root(file)

    if path.islink(file):
        sys.exit("Error: file is a link")
    store.add_file(root, file)





if __name__ == "__main__":
    main()