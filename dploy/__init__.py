"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 3), "Requires Python 3.3 or Greater"
import os
import pathlib

from dploy.util import resolve_abs_path
import dploy.command as command

class Stow():
    def __init__(self, source, dest):
        source_input = source
        dest_input = dest

        if not pathlib.Path(source_input).exists():
            msg = "dploy stow: can not stow '{file}': No such directory"
            print(msg.format(file=source_input))
            sys.exit(1)

        if not pathlib.Path(dest_input).exists():
            msg = "dploy stow: can not stow into '{file}': No such directory"
            print(msg.format(file=dest_input))
            sys.exit(1)

        source_absolute = resolve_abs_path(source_input)
        dest_absolute = resolve_abs_path(dest_input)

        source_pathlib = pathlib.Path(source_absolute)
        dest_pathlib = pathlib.Path(dest_absolute)

        self.commands = []
        self.abort = False

        self.basic(source_pathlib, dest_pathlib)
        self.execute_commands()


    def execute_commands(self):
        if self.abort:
            sys.exit(1)
        else:
            for command in self.commands:
                print(command)
                command.execute()


    def unfold(self, dest):
        children = []

        for child in dest.iterdir():
            child_relative = _get_pathlib_relative_path(child.resolve(), dest.parent)
            children.append(child)

        self.commands.append(command.UnLink(dest))
        self.commands.append(command.MakeDirectory(dest))
        self.collect_commands(children, dest, is_unfolding=True)


    def basic(self, source, dest):
        assert source.is_dir()
        assert source.is_absolute()
        assert dest.is_absolute()

        src_files = []

        for src_file in source.iterdir():
            src_files.append(src_file)

        self.collect_commands(src_files, dest)


    def collect_commands(self, sources, dest, is_unfolding=False):
        for source in sources:
            dest_path = dest / pathlib.Path(source.name)
            source_relative = _get_pathlib_relative_path(source,
                                                         dest_path.parent)
            if dest_path.exists():
                if _is_pathlib_same_file(dest_path, source):
                    if is_unfolding:
                        self.commands.append(command.SymbolicLink(source_relative, dest_path))
                    else:
                        self.commands.append(command.SymbolicLinkExists(source_relative, dest_path))
                elif dest_path.is_dir() and source.is_dir:
                    if dest_path.is_symlink():
                        self.unfold(dest_path)
                    self.basic(source, dest_path)
                else:
                    msg = "dploy stow: can not stow '{file}': Conflicts with existing file"
                    print(msg.format(file=dest_path))
                    self.abort = True
            elif not dest_path.parent.exists():
                    msg = "dploy stow: can not stow into '{dest}': No such directory"
                    print(msg.format(dest=dest_path.parent))
                    self.abort = True
            else:
                self.commands.append(command.SymbolicLink(source_relative, dest_path))



def stow(source, dest):
    """
    sub command stow
    """

    Stow(source, dest)


def link(source, dest):
    """
    sub command link
    """
    source_absolute = resolve_abs_path(source)
    dest_absolute = resolve_abs_path(dest)

    _link_absolute_paths(pathlib.Path(source_absolute),
                        pathlib.Path(dest_absolute))


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


def _is_pathlib_same_file(file1, file2):
    # NOTE: python 3.5 supports pathlib.Path.samefile(file)
    return file1.resolve() == file2.resolve()


def _get_pathlib_relative_path(path, start_at):
    return pathlib.Path(os.path.relpath(path.__str__(), start_at.__str__()))
