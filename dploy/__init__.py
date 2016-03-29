"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 3), 'Requires Python 3.3 or Greater'
import os
import pathlib

from dploy.util import resolve_abs_path

def stow(source, dest):
    """
    sub command stow
    """
    source_absolute = resolve_abs_path(source)
    dest_absolute = resolve_abs_path(dest)

    _stow_absolute_paths(pathlib.Path(source_absolute),
                          pathlib.Path(dest_absolute))


def link(source, dest):
    """
    sub command link
    """
    source_absolute = resolve_abs_path(source)
    dest_absolute = resolve_abs_path(dest)

    _link_absolute_paths(pathlib.Path(source_absolute),
                        pathlib.Path(dest_absolute))


def _stow_absolute_paths(source, dest):
    assert source.is_dir()
    assert source.is_absolute()
    assert dest.is_absolute()

    src_files = []
    src_files_relative = []
    stow_paths = []

    for src_file in source.iterdir():
        stow_path = dest / pathlib.Path(src_file.name)
        src_file_relative = _get_pathlib_relative_path(src_file,
                                                       stow_path.parent)
        src_files.append(src_file)
        src_files_relative.append(src_file_relative)
        stow_paths.append(stow_path)

        if stow_path.exists():
            if _is_pathlib_same_file(stow_path, src_file):
                pass
            elif stow_path.is_dir():
                pass
            else:
                msg = "Abort: {file} Already Exists"
                print(msg.format(file=stow_path))
                sys.exit(1)
        elif not stow_path.parent.parent.exists():
                msg = "Abort: {dest} Not Found"
                print(msg.format(dest=dest))
                sys.exit(1)

    files = zip(src_files, src_files_relative, stow_paths)

    for src_file, src_file_relative, stow_path in files:
        try:
            stow_path.symlink_to(src_file_relative)
            msg = "Link: {dest} => {source}"
            print(msg.format(source=src_file_relative, dest=stow_path))

        except FileExistsError:
            if _is_pathlib_same_file(stow_path, src_file):
                msg = "Link: Already Linked {dest} => {source}"
                print(msg.format(source=src_file_relative, dest=stow_path))

            elif stow_path.is_dir() and src_file.is_dir:
                if stow_path.is_symlink():
                    _stow_unfold(stow_path)

                _stow_absolute_paths(src_file, stow_path)

            else:
                msg = "Abort: {file} Already Exists"
                print(msg.format(file=stow_path))
                sys.exit(1)

        except FileNotFoundError:
            msg = "Abort: {dest} Not Found"
            print(msg.format(dest=dest))
            sys.exit(1)


def _link_absolute_paths(source, dest):
    assert source.is_absolute()
    assert dest.is_absolute()
    assert source.exists()

    src_file_relative = _get_pathlib_relative_path(source,
                                                   dest.parent)
    try:
        dest.symlink_to(src_file_relative)
        msg = "Link: {dest} => {source}"
        print(msg.format(source=src_file_relative, dest=dest))

    except FileExistsError:
        if _is_pathlib_same_file(dest, source):
            msg = "Link: Already Linked {dest} => {source}"
            print(msg.format(source=src_file_relative, dest=dest))

        else:
            msg = "Abort: {file} Already Exists"
            print(msg.format(file=dest))
            sys.exit(1)

    except FileNotFoundError:
        msg = "Abort: {dest} Not Found"
        print(msg.format(dest=dest))
        sys.exit(1)


def _stow_unfold(dest):
    """
    we are stowing some more files and we have a conflict
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
    for child in dest.iterdir():
        # TODO re-implement as a list comprehension
        child_relative = _get_pathlib_relative_path(child.resolve(), dest.parent)
        children.append(child_relative)

    dest.unlink()
    dest.mkdir()

    for child in children:
        source = pathlib.Path(child)
        stow_path = dest / source.stem
        stow_path.symlink_to(source)


def _is_pathlib_same_file(file1, file2):
    # Note python 3.5 supports pathlib.Path(...).samefile(file)
    return file1.resolve() == file2.resolve()


def _get_pathlib_relative_path(path, start_at):
    return pathlib.Path(os.path.relpath(path.__str__(), start_at.__str__()))
