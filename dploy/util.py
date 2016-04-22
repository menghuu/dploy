"""
todo
"""

import os
import pathlib

def get_directory_contents(directory):
    """
    todo
    """
    contents = []

    for child in directory.iterdir():
        contents.append(child)

    return contents


def is_same_file(file1, file2):
    """
    todo

    NOTE: python 3.5 supports pathlib.Path.samefile(file)
    NOTE: this can raise exception FileNotFoundError
    """
    return file1.resolve() == file2.resolve()


def get_absolute_path(file):
    """
    todo
    """
    absolute_path = os.path.abspath(os.path.expanduser(file.__str__()))
    return pathlib.Path(absolute_path)


def get_relative_path(path, start_at):
    """
    NOTE: python 3.4.5 & 3.5.2 support pathlib.Path.path = pathlib.Path.__str__()
    """
    return pathlib.Path(os.path.relpath(path.__str__(), start_at.__str__()))
