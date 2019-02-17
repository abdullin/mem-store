import hashlib
import os
import shutil
from os import path

FOLDER_NAME = 'mem-objects'


def find_root(file):
    folder = path.dirname(path.abspath(file))
    while folder and folder not in '/':
        join = path.join(folder, FOLDER_NAME)
        if path.isdir(join):
            return folder

        folder = path.dirname(folder)

    return None

def add_file(root, filename):


    sha = sha256sum(filename)

    target_dir = path.join(root, FOLDER_NAME, sha[0:2])
    target_file = path.join(root, FOLDER_NAME, sha[0:2], sha)

    os.makedirs(target_dir, exist_ok=True)

    if not path.isfile(target_file):
        shutil.copy(filename, target_file)
        print('importing new file')
    else:
        print('deduplicating file')

    rel_path = os.path.relpath(target_file, os.path.dirname(filename))

    os.remove(filename)
    os.symlink(rel_path, filename)


def sha256sum(filename):
    h  = hashlib.sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def fix_file(root, filename):
    link = os.readlink(filename)
    sha = path.basename(link)

    target_file = path.join(root, FOLDER_NAME, sha[0:2], sha)

    if not path.isfile(target_file):
        print("BLOB doesn't exist")
        return

    rel_path = os.path.relpath(target_file, os.path.dirname(filename))
    if link == rel_path:
        print("Link is ok")
        return

    os.remove(filename)
    os.symlink(rel_path, filename)

