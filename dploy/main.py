"""
The logic and workings behind the stow and unstow sub commands
"""

from collections import defaultdict
import pathlib
import dploy.actions
import dploy.utils

ERROR_HEAD = 'dploy {subcmd}: can not {subcmd} '

class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 subcmd,
                 sources,
                 dest,
                 invalid_source_message,
                 invalid_dest_message,
                 is_silent,
                 is_dry_run):
        self.subcmd = subcmd
        self.actions = []
        self.execptions = []
        self.invalid_source_message = invalid_source_message
        self.invalid_dest_message = invalid_dest_message
        self.is_silent = is_silent
        self.is_dry_run = is_dry_run

        for source in sources:
            source_input = pathlib.Path(source)
            dest_input = pathlib.Path(dest)
            source_absolute = dploy.utils.get_absolute_path(source_input)
            dest_absolute = dploy.utils.get_absolute_path(dest_input)
            self.validate_input(source_input, dest_input)
            self.collect_actions(source_absolute, dest_absolute)

        self.check_for_conflicting_actions()
        self.execute_actions()

    def check_for_conflicting_actions(self):
        """
        todo
        """
        pass

    def validate_input(self, source, dest):
        """
        todo
        """
        pass

    def collect_actions(self, source, dest):
        """
        todo
        """
        pass

    def execute_actions(self):
        """
        todo
        """
        if len(self.execptions) > 0:
            for execption in self.execptions:
                raise execption
        else:
            for action in self.actions:
                if not self.is_silent:
                    print(action)
                if not self.is_dry_run:
                    action.execute()

class AbstractBaseStow(AbstractBaseSubCommand):
    """
    todo
    """
    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, source, dest, is_silent, is_dry_run):
        invalid_source_message = ERROR_HEAD + "'{file}': No such directory"
        invalid_dest_message = ERROR_HEAD + "into '{file}': No such directory"
        self.is_unfolding = False
        super().__init__(subcmd,
                         source,
                         dest,
                         invalid_source_message,
                         invalid_dest_message,
                         is_silent,
                         is_dry_run)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.is_dir():
            raise ValueError(self.invalid_source_message.format(subcmd=self.subcmd, file=source))

        elif not dest.is_dir():
            raise ValueError(self.invalid_dest_message.format(subcmd=self.subcmd, file=dest))

        elif not dploy.utils.is_directory_readable(source):
            msg = ERROR_HEAD + "from '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=source)
            raise PermissionError(msg)

        elif not dploy.utils.is_directory_writable(dest):
            msg = ERROR_HEAD + "to '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            raise PermissionError(msg)

    def get_directory_contents(self, directory):
        """
        get the contents of a directory while handling permission errors that
        may occur
        """
        contents = []

        try:
            contents = dploy.utils.get_directory_contents(directory)
        except PermissionError:
            msg = ERROR_HEAD + "'{file}': Permission denied"
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

    def collect_actions(self, source, dest):
        """
        todo
        """
        sources = self.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)

            if dest_path.exists():
                if dploy.utils.is_same_file(dest_path, source):
                    if dest_path.is_symlink() or self.is_unfolding:
                        self.are_same_file(source, dest_path)
                    else:
                        # pylint: disable=line-too-long
                        msg = ERROR_HEAD + "'{file}': A source argument is the same as the dest argument"
                        msg = msg.format(subcmd=self.subcmd, file=dest_path)
                        self.execptions.append(ValueError(msg))

                elif dest_path.is_dir() and source.is_dir:
                    self.are_directories(source, dest_path)
                else:
                    msg = ERROR_HEAD + "'{file}': Conflicts with existing file"
                    msg = msg.format(subcmd=self.subcmd, file=dest_path)
                    self.execptions.append(ValueError(msg))

            elif dest_path.is_symlink():
                msg = ERROR_HEAD + "'{file}': Conflicts with existing link"
                msg = msg.format(subcmd=self.subcmd, file=dest_path)
                self.execptions.append(ValueError(msg))

            elif not dest_path.parent.exists() and not self.is_unfolding:
                msg = ERROR_HEAD + "'{file}': No such directory"
                msg = msg.format(subcmd=self.subcmd, file=dest_path.parent)
                self.execptions.append(ValueError(msg))

            else:
                self.are_other(source, dest_path)


class UnStow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest, is_silent=True, is_dry_run=False):
        super().__init__("unstow", source, dest, is_silent, is_dry_run)


    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        self.actions.append(dploy.actions.UnLink(self.subcmd, dest))

    def are_directories(self, source, dest):
        if not dest.is_symlink():
            self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(dploy.actions.AlreadyUnlinked(self.subcmd,
                                                          source,
                                                          dest))


class Link(AbstractBaseSubCommand):
    """
    todo
    """
    def __init__(self, source, dest, is_silent=True, is_dry_run=False):
        invalid_source_message = ERROR_HEAD + "'{file}': No such file or directory"
        invalid_dest_message = ERROR_HEAD + "into '{file}': directory"
        super().__init__("link", [source], dest, invalid_source_message,
                         invalid_dest_message, is_silent, is_dry_run)

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

        elif (not dploy.utils.is_file_readable(source)
              or not dploy.utils.is_directory_readable(source)):
            msg = ERROR_HEAD + "'{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=source)
            raise PermissionError(msg)

        elif (not dploy.utils.is_file_writable(dest.parent)
              or not dploy.utils.is_directory_writable(dest.parent)):
            msg = ERROR_HEAD + "to '{file}': Insufficient permissions"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            raise PermissionError(msg)

    def collect_actions(self, source, dest):
        """
        todo
        """

        if dest.exists():
            if dploy.utils.is_same_file(dest, source):
                self.actions.append(dploy.actions.AlreadyLinked(self.subcmd,
                                                                source,
                                                                dest))
            else:
                msg = ERROR_HEAD + "'{file}': Conflicts with existing file"
                msg = msg.format(subcmd=self.subcmd, file=dest)
                self.execptions.append(ValueError(msg))

        elif dest.is_symlink():
            msg = ERROR_HEAD + "'{file}': Conflicts with existing link"
            msg = msg.format(subcmd=self.subcmd, file=dest)
            self.execptions.append(ValueError(msg))

        elif not dest.parent.exists():
            msg = ERROR_HEAD + "into '{file}': No such directory"
            msg = msg.format(subcmd=self.subcmd, file=dest.parent)
            self.execptions.append(ValueError(msg))

        else:
            self.actions.append(dploy.actions.SymbolicLink(self.subcmd, source, dest))


class Stow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest, is_silent=True, is_dry_run=False):
        super().__init__("stow", source, dest, is_silent, is_dry_run)

    def unfold(self, source, dest):
        """
        todo
        """
        self.is_unfolding = True
        self.actions.append(dploy.actions.UnLink(self.subcmd, dest))
        self.actions.append(dploy.actions.MakeDirectory(self.subcmd, dest))
        self.collect_actions(source, dest)
        self.is_unfolding = False

    def list_duplicates(self):
        """
        todo
        """
        tally = defaultdict(list)
        for i, item in enumerate(self.actions):
            if isinstance(item, dploy.actions.SymbolicLink):
                tally[item.dest].append(i)
        return ((key, locs) for key, locs in tally.items()
                if len(locs) > 1)

    def check_for_conflicting_actions(self):
        """
        check for symbolic link actions that would cause conflicting symbolic
        links to the same destination.
        """
        dupes = []
        for dup in self.list_duplicates():
            dupes.append(dup)

        if len(dupes) == 0:
            return

        for _, indicies in dupes:
            first_index = indicies[0]
            if self.actions[first_index].source.is_dir():
                self.unfold(self.actions[first_index].source,
                            self.actions[first_index].dest)
                for index in indicies[1:]:
                    self.is_unfolding = True
                    self.collect_actions(self.actions[index].source,
                                         self.actions[index].dest)
                    self.is_unfolding = False
            else:
                msg = ERROR_HEAD + "'{file}': Conflicts with another source"
                msg = msg.format(subcmd=self.subcmd, file=self.actions[first_index].source)
                self.execptions.append(ValueError(msg))
                return

        for _, indicies in dupes:
            for index in reversed(indicies[1:]):
                del self.actions[index]

        self.check_for_conflicting_actions()

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        if self.is_unfolding:
            self.actions.append(
                dploy.actions.SymbolicLink(self.subcmd, source, dest))
        else:
            self.actions.append(
                dploy.actions.AlreadyLinked(self.subcmd, source, dest))

    def are_directories(self, source, dest):
        if dest.is_symlink():
            self.unfold(dest.resolve(), dest)
        self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(
            dploy.actions.SymbolicLink(self.subcmd, source, dest))
