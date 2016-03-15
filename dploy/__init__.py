"""
Sets up the dotfiles in this repository

Requires python 3
"""

import sys
assert sys.version_info >= (3, 4), 'Requires Python 3.4 or Greater'
import os
import shutil

from dploy.util import resolve_abs_path


def link(source, dest):
    """
    create symbolic link relative to the source file or directory
    """

    dest_dir = os.path.dirname(dest)
    source_relative = os.path.relpath(source, start=dest_dir)

    try:
        os.symlink(source_relative, dest)
        print("Link: {dest} => {source}".format(source=source, dest=dest))
    except Exception as exception_message:
        print(exception_message)

def dploy(source, dest):
    """
    main script entry point
    """
    source_absolute = resolve_abs_path(source)
    dest_dir = os.path.dirname(dest)
    source_relative = os.path.relpath(source, start=dest_dir)
    dest_absolute = resolve_abs_path(dest)

    if os.path.islink(dest_absolute):
        link_location = os.readlink(dest_absolute)
        if os.readlink(dest_absolute) == source_relative:
            print("Link: Already Linked {dest} => {source}".format(source=source_relative,
                                                                   dest=dest_absolute))
        else:
            print("Abort: Dest Is A Link That Points To {link_location}".format(
                link_location=link_location))
    elif os.path.isfile(dest_absolute):
        print("Abort: file Already Exists")
    elif os.path.isdir(dest_absolute):
        for file in os.listdir(source_absolute):
            link(os.path.join(source_absolute, file),
                 os.path.join(dest_absolute, file))
    else:
        os.makedirs(os.path.dirname(dest_absolute), exist_ok=True)
        link(source_absolute, dest_absolute)
