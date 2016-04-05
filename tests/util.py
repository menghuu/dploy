"""
todo
"""

import os
import shutil


def remove_tree(tree):
    """
    todo
    """
    shutil.rmtree(tree)

def remove_file(file_name):
    """
    todo
    """
    os.remove(file_name)

def create_file(file_name):
    """
    todo
    """
    open(file_name, 'w').close()

def create_directory(directory_name):
    """
    todo
    """
    os.makedirs(directory_name)

class cd:
    # pylint: disable=too-few-public-methods
    """
    Context manager for changing the current working directory
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def create_tree(tree):
    """
    todo
    """
    for branch in tree:
        if type(branch) == type(''):
            create_file(branch)
        elif type(branch) == type({}):
            for directory, file_objs in branch.items():
                create_directory(directory)
                with cd(directory):
                    create_tree(file_objs)
