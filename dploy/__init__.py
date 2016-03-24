"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 4), 'Requires Python 3.4 or Greater'
import os
import pathlib

from dploy.util import resolve_abs_path


def dploy(source, dest):
    """
    main script entry point
    """
    source_absolute = resolve_abs_path(source)
    dest_absolute = resolve_abs_path(dest)

    _dploy_absolute_paths(pathlib.Path(source_absolute),
                          pathlib.Path(dest_absolute))



def _dploy_absolute_paths(source, dest):
    assert source.is_dir()
    assert source.is_absolute()
    assert dest.is_absolute()

    for src_file in source.iterdir():
        dploy_path = dest / pathlib.Path(src_file.stem)
        src_file_relative = _pathlib_relative_path(src_file,
                                                   dploy_path.parent)

        try:
            dploy_path.symlink_to(src_file_relative)
            msg = "Link: {dest} => {source}"
            print(msg.format(source=src_file_relative, dest=dploy_path))

        except FileExistsError:
            if dploy_path.samefile(src_file):
                msg = "Link: Already Linked {dest} => {source}"
                print(msg.format(source=src_file_relative, dest=dploy_path))

            elif dploy_path.is_dir() and src_file.is_dir:
                if dploy_path.is_symlink():
                    unfold(dploy_path)

                _dploy_absolute_paths(src_file, dploy_path)

            else:
                msg = "Abort: {file} Already Exists"
                print(msg.format(file=dploy_path))
                sys.exit(1)

        except FileNotFoundError:
            msg = "Abort: {dest} Not Found"
            print(msg.format(dest=dest))
            sys.exit(1)

def unfold(dest):
    """
    we are dploying some more files and we have a conflic
    top level dest is a symlink that now needs to be a plain directory

    steps:
    - record children of the top level dest dir
    - unlink top level dir
    - create directory in place of the top level dest dir
    - individually symlink recorded children

    todo:
    there is also the case were this will need to be undone
    """

    children = []
    for child in dest.iterdir(): # TODO re-implement as a list comprehension
        child_relative = _pathlib_relative_path(child.resolve(), dest.parent)
        children.append(child_relative)

    print(children)
    dest.unlink()
    dest.mkdir()

    for child in children:
        source = pathlib.Path(child)
        dploy_path = dest / source.stem
        dploy_path.symlink_to(source)

def _pathlib_relative_path(path, start_at):
    return os.path.relpath(path.__str__(), start_at.__str__())

