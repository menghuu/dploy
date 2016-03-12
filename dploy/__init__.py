"""
Sets up the dotfiles in this repository

Requires python 3
"""

import sys
import os
import shutil

from dploy.util import resolve_abs_path

def link_file(target, dest):
    dest_dir = os.path.dirname(dest)
    # get a relative path to the target from the destination location of
    # the file, this way we will have a relative symlink
    target_relative = os.path.relpath(target, start=dest_dir)

    try:
        os.symlink(target_relative, dest)
    except Exception as exception_message:
        print(exception_message)

def deploy_files(target, dest):
    target_absolute = resolve_abs_path(target)
    dest_absolute = resolve_abs_path(dest)

    print("{dest_absolute} = dest_absolute".format(dest_absolute=dest_absolute))
    print("{target_absolute} = target_absolute".format(target_absolute=target_absolute))

    if os.path.islink(dest_absolute):
        link_location = os.readlink(dest_absolute)
        print("dest is a link that points to {link_location}".format(
            link_location=link_location))

        print("dest is a link that points to {link_location}".format(
            link_location=resolve_abs_path(link_location)))

        if resolve_abs_path(os.readlink(dest_absolute)) == target_absolute:
            print("already linked")
        else:
            print("Abort other link exits")
    elif os.path.isfile(dest_absolute):
        print("Abort File Already Exists")
    elif os.path.isdir(dest_absolute):
        for file in os.listdir(target_absolute):
            link_file(os.path.join(target_absolute, file),
                      os.path.join(dest_absolute, file))
    else:
        link_file(target_absolute, dest_absolute)
        print("Creating link {dest} pointing to {target}".format(
            target=target,
            dest=dest))

def create_directories(directories):
    print("Creating Directories")

    for directory in directories:
        directory = resolve_abs_path(directory)
        print("Creating Directory: {0}".format(directory))

        try:
            os.makedirs(directory)
        except Exception as exception_message:
            print(exception_message)
