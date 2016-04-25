"""
The logic and workings behind the stow and unstow sub commands
"""

import sys
from collections import defaultdict
import pathlib
import dploy.command
import dploy.util


class AbstractBaseStow():
    """
    An abstract class to unify shared functionality in stow commands
    """

    def __init__(self, sources, dest, invalid_source_message,
                 invalid_dest_message):
        self.commands = []
        self.abort = False
        self.invalid_source_message = invalid_source_message
        self.invalid_dest_message = invalid_dest_message

        for source in sources:
            source_input = pathlib.Path(source)
            dest_input = pathlib.Path(dest)
            source_absolute = dploy.util.get_absolute_path(source_input)
            dest_absolute = dploy.util.get_absolute_path(dest_input)
            self.validate_input(source_input, dest_input)
            self.collect_commands(source_absolute, dest_absolute)

        self.check_for_conflicting_commands()
        self.execute_commands()

    def check_for_conflicting_commands(self):
        """
        todo
        """
        pass

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.is_dir():
            print(self.invalid_source_message.format(file=source))
            sys.exit(1)

        if not dest.is_dir():
            print(self.invalid_dest_message.format(file=dest))
            sys.exit(1)

        if not dploy.util.is_directory_readable(source):
            msg = "dploy link: can not stow from '{file}': Insufficient permissions"
            print(msg.format(file=source))
            sys.exit(1)

        if not dploy.util.is_directory_writable(dest):
            msg = "dploy stow: can not stow to '{file}': Insufficient permissions"
            print(msg.format(file=dest))
            sys.exit(1)

    def collect_commands(self, source, dest):
        """
        todo
        """
        pass

    def execute_commands(self):
        """
        todo
        """
        if self.abort:
            sys.exit(1)
        else:
            for cmd in self.commands:
                cmd.execute()


class UnStow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        invalid_source_message = "dploy stow: can not unstow from '{file}': No such directory"
        invalid_dest_message = "dploy stow: can not unstow '{file}': No such directory"
        super().__init__(source, dest, invalid_source_message,
                         invalid_dest_message)

    def collect_commands(self, source, dest):
        """
        todo
        """

        sources = dploy.util.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)

            if dest_path.exists():
                if dploy.util.is_same_file(dest_path, source):
                    self.commands.append(
                        dploy.command.UnLink(dest_path))

                elif dest_path.is_dir() and source.is_dir:
                    if not dest_path.is_symlink():
                        self.collect_commands(source, dest_path)
                else:
                    msg = "dploy stow: can not unstow '{file}': Conflicts with existing file"
                    print(msg.format(file=dest_path))

            elif dest_path.is_symlink():
                msg = "dploy stow: can not unstow '{file}': Conflicts with a existing link"
                print(msg.format(file=dest_path))

            elif not dest_path.parent.exists():
                msg = "dploy stow: can not unstow '{file}': No such directory"
                print(msg.format(file=dest_path.parent))
            else:
                pass


class Link(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        invalid_source_message = "dploy link: can not link '{file}': No such file or directory"
        invalid_dest_message = ""
        super().__init__(source, dest, invalid_source_message,
                         invalid_dest_message)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.exists():
            print(self.invalid_source_message.format(file=source))
            sys.exit(1)

        if not dploy.util.is_file_readable(source) or not dploy.util.is_directory_readable(source):
            msg = "dploy link: can not link '{file}': Insufficient permissions"
            print(msg.format(file=source))
            sys.exit(1)

        if (not dploy.util.is_file_writable(dest.parent) or
                not dploy.util.is_directory_writable(dest.parent)):
            msg = "dploy link: can not link to '{file}': Insufficient permissions"
            print(msg.format(file=dest))
            sys.exit(1)


    def collect_commands(self, source, dest):
        """
        todo
        """

        if dest.exists():
            if dploy.util.is_same_file(dest, source):
                self.commands.append(dploy.command.SymbolicLinkExists(source,
                                                                      dest))
            else:
                msg = "dploy link: can not link '{file}': Conflicts with existing file"
                print(msg.format(file=dest))
                self.abort = True

        elif dest.is_symlink():
            msg = "dploy link: can not link '{file}': Conflicts with existing link"
            print(msg.format(file=dest))
            self.abort = True

        elif not dest.parent.exists():
            msg = "dploy link: can not link into '{dest}': No such directory"
            print(msg.format(dest=dest.parent))
            self.abort = True

        else:
            self.commands.append(dploy.command.SymbolicLink(source, dest))


class Stow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        invalid_source_message = "dploy stow: can not stow '{file}': No such directory"
        invalid_dest_message = "dploy stow: can not stow into '{file}': No such directory"
        self.is_unfolding = False
        super().__init__(source, dest, invalid_source_message,
                         invalid_dest_message)

    def unfold(self, source, dest):
        """
        todo
        """
        self.is_unfolding = True
        self.commands.append(dploy.command.UnLink(dest))
        self.commands.append(dploy.command.MakeDirectory(dest))
        self.collect_commands(source, dest)
        self.is_unfolding = False

    def list_duplicates(self):
        """
        todo
        """
        tally = defaultdict(list)
        for i, item in enumerate(self.commands):
            if isinstance(item, dploy.command.SymbolicLink):
                tally[item.dest].append(i)
        return ((key, locs) for key, locs in tally.items()
                if len(locs) > 1)

    def check_for_conflicting_commands(self):
        """
        check for symbolic link commands that would cause conflicting symbolic
        links to the same destination.
        """
        dupes = []
        for dup in self.list_duplicates():
            dupes.append(dup)

        if len(dupes) == 0:
            return

        for _, indicies in dupes:
            first_index = indicies[0]
            if self.commands[first_index].source.is_dir():
                self.unfold(self.commands[first_index].source,
                            self.commands[first_index].dest)
                for index in indicies[1:]:
                    self.collect_commands(self.commands[index].source,
                                          self.commands[index].dest)
            else:
                msg = "dploy stow: can not stow '{source}': Conflicts with another source"
                print(msg.format(source=self.commands[first_index].source))
                self.abort = True
                return

        for _, indicies in dupes:
            for index in reversed(indicies[1:]):
                del self.commands[index]

        self.check_for_conflicting_commands()

    def collect_commands(self, source, dest):
        """
        todo
        """

        sources = dploy.util.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)
            if dest_path.exists():
                if dploy.util.is_same_file(dest_path, source):

                    if self.is_unfolding:
                        self.commands.append(
                            dploy.command.SymbolicLink(source, dest_path))
                    else:
                        self.commands.append(
                            dploy.command.SymbolicLinkExists(source,
                                                             dest_path))
                elif dest_path.is_dir() and source.is_dir:
                    if dest_path.is_symlink():
                        self.unfold(dest_path.resolve(), dest_path)
                    self.collect_commands(source, dest_path)
                else:
                    msg = "dploy stow: can not stow '{file}': Conflicts with existing file"
                    print(msg.format(file=dest_path))
                    self.abort = True

            elif dest_path.is_symlink():
                msg = "dploy stow: can not stow '{file}': Conflicts with existing link"
                print(msg.format(file=dest_path))
                self.abort = True

            elif not dest_path.parent.exists() and not self.is_unfolding:
                msg = "dploy stow: can not stow into '{dest}': No such directory"
                print(msg.format(dest=dest_path.parent))
                self.abort = True

            else:
                self.commands.append(
                    dploy.command.SymbolicLink(source, dest_path))
