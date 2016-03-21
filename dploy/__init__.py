"""
dploy script
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

        src_file_relative = os.path.relpath(src_file.__str__(),
                                            dploy_path.parent.__str__())
        try:
            dploy_path.symlink_to(src_file_relative)
            msg = "Link: {dest} => {source}"
            print(msg.format(source=src_file_relative, dest=dploy_path))
        except FileExistsError:
            if dploy_path.samefile(src_file):
                msg = "Link: Already Linked {dest} => {source}"
                print(msg.format(source=src_file_relative, dest=dploy_path))
            elif dploy_path.is_dir() and src_file.is_dir:
                _dploy_absolute_paths(src_file, dploy_path)
            else:
                msg = "Abort: {file} Already Exists"
                print(msg.format(file=dploy_path))
                sys.exit(1)
        except FileNotFoundError:
            msg = "Abort: {dest} Not Found"
            print(msg.format(dest=dest))
            sys.exit(1)
