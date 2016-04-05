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

class ChangeDirectory:
    # pylint: disable=too-few-public-methods
    """
    Context manager for changing the current working directory
    """
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

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

                with ChangeDirectory(directory):
                    create_tree(file_objs)
