"""
Sets up the dotfiles in this repository

Requires python 3
"""

import sys
import os
import shutil

from dploy.util import resolve_abs_path

def link(target, dest):
    """
    create symbolic link relative to the target file or directory
    """

    dest_dir = os.path.dirname(dest)
    target_relative = os.path.relpath(target, start=dest_dir)

    try:
        os.symlink(target_relative, dest)
        print("Link: {dest} => {target}".format(target=target, dest=dest))
    except Exception as exception_message:
        print(exception_message)

def dploy(target, dest):
    """
    main script entry point
    """
    target_absolute = resolve_abs_path(target)
    dest_absolute = resolve_abs_path(dest)

    if os.path.islink(dest_absolute):
        link_location = os.readlink(dest_absolute)
        if resolve_abs_path(os.readlink(dest_absolute)) == target_absolute:
            print("Link: Already Linked {dest} => {target}".format(target=target_absolute,
                                                                   dest=dest_absolute))
        else:
            print("Abort: Dest Is A Link That Points To {link_location}".format(
                link_location=resolve_abs_path(link_location)))
    elif os.path.isfile(dest_absolute):
        print("Abort: file Already Exists")
    elif os.path.isdir(dest_absolute):
        for file in os.listdir(target_absolute):
            link(os.path.join(target_absolute, file),
                 os.path.join(dest_absolute, file))
    else:
        os.makedirs(os.path.dirname(dest_absolute), exist_ok=True)
        link(target_absolute, dest_absolute)
