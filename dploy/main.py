"""
The logic and workings behind the stow and unstow sub commands
"""

from collections import defaultdict
import pathlib
import dploy.command
import dploy.util


class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # TODO
    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, sources, dest, invalid_source_message,
                 invalid_dest_message):
        self.subcmd = subcmd
        self.commands = []
        self.execptions = []
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
        pass

    def collect_commands(self, source, dest):
        """
        todo
        """
        pass

    def execute_commands(self):
        """
        todo
        """
        if len(self.execptions) > 0:
            for execption in self.execptions:
                raise execption
        else:
            for cmd in self.commands:
                cmd.execute()


class AbstractBaseStow(AbstractBaseSubCommand):
    """
    todo
    """
    def __init__(self, subcmd, source, dest):
        invalid_source_message = "dploy {subcmd}: can not {subcmd} '{file}': No such directory"
        invalid_dest_message = "dploy {subcmd}: can not {subcmd} into '{file}': No such directory"
        self.is_unfolding = False
        super().__init__(subcmd, source, dest, invalid_source_message, invalid_dest_message)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.is_dir():
            raise ValueError(self.invalid_source_message.format(subcmd=self.subcmd, file=source))

        elif not dest.is_dir():
            raise ValueError(self.invalid_dest_message.format(subcmd=self.subcmd, file=dest))

        elif not dploy.util.is_directory_readable(source):
            msg = "dploy {subcmd}: can not {subcmd} from '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=source)
            raise PermissionError(msg)

        elif not dploy.util.is_directory_writable(dest):
            msg = "dploy {subcmd}: can not {subcmd} to '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            raise PermissionError(msg)

    def get_directory_contents(self, directory):
        """
        get the contents of a directory while handling permission errors that
        may occur
        """
        contents = []

        try:
            contents = dploy.util.get_directory_contents(directory)
        except PermissionError:
            msg = "dploy {subcmd}: can not {subcmd} '{file}': Permission denied"
            msg = msg.format(subcmd=self.subcmd, file=directory)
            self.execptions.append(PermissionError(msg))

        return contents

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        pass

    def are_directories(self, source, dest):
        """
        what to do if the source and dest are directories
        """
        pass

    def are_other(self, source, dest):
        """
        what to do if no particular condition is true cases are found
        """
        pass

    def collect_commands(self, source, dest):
        """
        todo
        """
        sources = self.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)

            if dest_path.exists():
                if dploy.util.is_same_file(dest_path, source):
                    self.are_same_file(source, dest_path)

                elif dest_path.is_dir() and source.is_dir:
                    self.are_directories(source, dest_path)
                else:
                    msg = (
                        "dploy {subcmd}: can not {subcmd} '{file}': Conflicts with existing file"
                    )
                    msg = msg.format(subcmd=self.subcmd, file=dest_path)
                    self.execptions.append(ValueError(msg))

            elif dest_path.is_symlink():
                msg = "dploy {subcmd}: can not {subcmd} '{file}': Conflicts with existing link"
                msg = msg.format(subcmd=self.subcmd, file=dest_path)
                self.execptions.append(ValueError(msg))

            elif not dest_path.parent.exists() and not self.is_unfolding:
                msg = "dploy {subcmd}: can not {subcmd} '{file}': No such directory"
                msg = msg.format(subcmd=self.subcmd, file=dest_path.parent)
                self.execptions.append(ValueError(msg))

            else:
                self.are_other(source, dest_path)


class UnStow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        super().__init__("unstow", source, dest)


    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        self.commands.append(dploy.command.UnLink(self.subcmd, dest))

    def are_directories(self, source, dest):
        if not dest.is_symlink():
            self.collect_commands(source, dest)

    def are_other(self, source, dest):
        pass


class Link(AbstractBaseSubCommand):
    """
    todo
    """
    def __init__(self, source, dest):
        invalid_source_message = (
            "dploy {subcmd}: can not {subcmd} '{file}': No such file or directory"
        )
        invalid_dest_message = (
            "dploy {subcmd}: can not {subcmd} into '{file}': directory"
        )
        super().__init__("link", [source], dest, invalid_source_message,
                         invalid_dest_message)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.exists():
            msg = self.invalid_source_message.format(subcmd=self.subcmd,
                                                     file=source)
            raise ValueError(msg)

        elif not dest.parent.exists():
            msg = self.invalid_dest_message.format(subcmd=self.subcmd,
                                                   file=dest.parent)
            raise ValueError(msg)

        elif (not dploy.util.is_file_readable(source)
              or not dploy.util.is_directory_readable(source)):
            msg = "dploy {subcmd}: can not {subcmd} '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=source)
            raise PermissionError(msg)

        elif (not dploy.util.is_file_writable(dest.parent)
              or not dploy.util.is_directory_writable(dest.parent)):
            msg = "dploy {subcmd}: can not {subcmd} to '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            raise PermissionError(msg)

    def collect_commands(self, source, dest):
        """
        todo
        """

        if dest.exists():
            if dploy.util.is_same_file(dest, source):
                self.commands.append(dploy.command.SymbolicLinkExists(self.subcmd,
                                                                      source,
                                                                      dest))
            else:
                msg = "dploy {subcmd}: can not {subcmd} '{file}': Conflicts with existing file"
                msg = msg.format(subcmd=self.subcmd, file=dest)
                self.execptions.append(ValueError(msg))

        elif dest.is_symlink():
            msg = "dploy {subcmd}: can not {subcmd} '{file}': Conflicts with existing link"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            self.execptions.append(ValueError(msg))

        elif not dest.parent.exists():
            msg = "dploy {subcmd}: can not {subcmd} into '{dest}': No such directory"
            msg = msg.format(subcmd=self.subcmd, dest=dest.parent)
            self.execptions.append(ValueError(msg))

        else:
            self.commands.append(dploy.command.SymbolicLink(self.subcmd, source, dest))


class Stow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        super().__init__("stow", source, dest)

    def unfold(self, source, dest):
        """
        todo
        """
        self.is_unfolding = True
        self.commands.append(dploy.command.UnLink(self.subcmd, dest))
        self.commands.append(dploy.command.MakeDirectory(self.subcmd, dest))
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
                    self.is_unfolding = True
                    self.collect_commands(self.commands[index].source,
                                          self.commands[index].dest)
                    self.is_unfolding = False
            else:
                msg = "dploy {subcmd}: can not {subcmd} '{source}': Conflicts with another source"
                msg = msg.format(subcmd=self.subcmd, source=self.commands[first_index].source)
                self.execptions.append(ValueError(msg))
                return

        for _, indicies in dupes:
            for index in reversed(indicies[1:]):
                del self.commands[index]

        self.check_for_conflicting_commands()

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        if self.is_unfolding:
            self.commands.append(
                dploy.command.SymbolicLink(self.subcmd, source, dest))
        else:
            self.commands.append(
                dploy.command.SymbolicLinkExists(self.subcmd, source, dest))

    def are_directories(self, source, dest):
        if dest.is_symlink():
            self.unfold(dest.resolve(), dest)
        self.collect_commands(source, dest)

    def are_other(self, source, dest):
        self.commands.append(
            dploy.command.SymbolicLink(self.subcmd, source, dest))
