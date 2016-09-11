"""
The logic and workings behind the stow and unstow sub commands
"""

from collections import defaultdict
from collections import Counter
import pathlib
import dploy.actions as actions
import dploy.utils as utils
import dploy.exceptions as exceptions


class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, sources, dest, is_silent, is_dry_run):
        self.subcmd = subcmd
        self.actions = []
        self.execptions = []
        self.is_silent = is_silent
        self.is_dry_run = is_dry_run

        for source in sources:
            source_input = pathlib.Path(source)
            dest_input = pathlib.Path(dest)
            source_absolute = utils.get_absolute_path(source_input)
            dest_absolute = utils.get_absolute_path(dest_input)
            self.validate_input(source_input, dest_input)
            self.collect_actions(source_absolute, dest_absolute)

        self.check_for_other_actions()
        self.execute_actions()

    def check_for_other_actions(self):
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
        self.is_unfolding = False
        super().__init__(subcmd, source, dest, is_silent, is_dry_run)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.is_dir():
            raise exceptions.no_such_directory(self.subcmd, source)

        elif not dest.is_dir():
            raise exceptions.no_such_directory_to_subcmd_into(self.subcmd, dest)

        elif not utils.is_directory_readable(source):
            raise exceptions.insufficient_permissions_to_subcmd_from(self.subcmd, source)

        elif not utils.is_directory_writable(dest):
            raise exceptions.insufficient_permissions_to_subcmd_to(self.subcmd, dest)

    def get_directory_contents(self, directory):
        """
        get the contents of a directory while handling permission errors that
        may occur
        """
        contents = []

        try:
            contents = utils.get_directory_contents(directory)
        except PermissionError:
            self.execptions.append(exceptions.permission_denied(self.subcmd, directory))

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
                if utils.is_same_file(dest_path, source):
                    if dest_path.is_symlink() or self.is_unfolding:
                        self.are_same_file(source, dest_path)
                    else:
                        self.execptions.append(
                            exceptions.source_is_same_as_dest(self.subcmd, dest_path))

                elif dest_path.is_dir() and source.is_dir:
                    self.are_directories(source, dest_path)
                else:
                    self.execptions.append(
                        exceptions.conflicts_with_existing_file(self.subcmd, dest_path))

            elif dest_path.is_symlink():
                self.execptions.append(
                    exceptions.conflicts_with_existing_link(self.subcmd, dest_path))

            elif not dest_path.parent.exists() and not self.is_unfolding:
                self.execptions.append(exceptions.no_such_directory(self.subcmd, dest_path.parent))

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
        self.actions.append(actions.UnLink(self.subcmd, dest))

    def are_directories(self, source, dest):
        if not dest.is_symlink():
            self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(actions.AlreadyUnlinked(self.subcmd, source, dest))

    def check_for_other_actions(self):
        self.collect_folding_actions()

    def collect_folding_actions(self):
        """
        find canidates for folding i.e. when replacing a directories containing
        links with a single symlink to the directory itself would work instead
        """

        unlink_actions = (
            [a for a in self.actions if isinstance(a, actions.UnLink)])
        unlink_actions_targets = [a.target for a in unlink_actions]
        unlink_actions_targets_parents = [a.target.parent for a in unlink_actions]

        for parent in unlink_actions_targets_parents:
            items = utils.get_directory_contents(parent)
            other_links = []
            source_parent = None

            for item in items:
                if item in unlink_actions_targets:
                    pass
                elif item.is_symlink():
                    source_parent = item.resolve().parent
                    other_links.append(item.resolve().parent)

            other_links_counter = Counter(other_links)
            if len(other_links_counter.keys()) == 1:
                self.fold(source_parent, parent)


    def fold(self, source, dest):
        """
        add the required actions for folding
        """
        rmdir_actions_targets = (
            [a.target for a in self.actions if isinstance(a, actions.RemoveDirectory)])

        if  dest not in rmdir_actions_targets:
            self.actions.append(actions.RemoveDirectory(self.subcmd, dest))
            self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


class Link(AbstractBaseSubCommand):
    """
    todo
    """
    def __init__(self, source, dest, is_silent=True, is_dry_run=False):
        super().__init__("link", [source], dest, is_silent, is_dry_run)

    def validate_input(self, source, dest):
        """
        todo
        """
        if not source.exists():
            raise exceptions.no_such_file_or_directory(self.subcmd, source)

        elif not dest.parent.exists():
            raise exceptions.no_such_directory(self.subcmd, dest.parent)

        elif (not utils.is_file_readable(source)
              or not utils.is_directory_readable(source)):
            raise exceptions.insufficient_permissions(self.subcmd, source)

        elif (not utils.is_file_writable(dest.parent)
              or not utils.is_directory_writable(dest.parent)):
            raise  exceptions.insufficient_permissions_to_subcmd_to(self.subcmd, dest)

    def collect_actions(self, source, dest):
        """
        todo
        """

        if dest.exists():
            if utils.is_same_file(dest, source):
                self.actions.append(actions.AlreadyLinked(self.subcmd,
                                                          source,
                                                          dest))
            else:
                self.execptions.append(exceptions.conflicts_with_existing_file(self.subcmd, dest))

        elif dest.is_symlink():
            self.execptions.append(exceptions.conflicts_with_existing_link(self.subcmd, dest))

        elif not dest.parent.exists():
            self.execptions.append(
                exceptions.no_such_directory_to_subcmd_into(self.subcmd, dest.parent))

        else:
            self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


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
        self.actions.append(actions.UnLink(self.subcmd, dest))
        self.actions.append(actions.MakeDirectory(self.subcmd, dest))
        self.collect_actions(source, dest)
        self.is_unfolding = False

    def list_duplicates(self):
        """
        todo
        """
        tally = defaultdict(list)
        for i, item in enumerate(self.actions):
            if isinstance(item, actions.SymbolicLink):
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
                self.execptions.append(
                    exceptions.conflicts_with_another_source(
                        self.subcmd, self.actions[first_index].source))
                return

        for _, indicies in dupes:
            for index in reversed(indicies[1:]):
                del self.actions[index]

        self.check_for_conflicting_actions()

    def check_for_other_actions(self):
        self.check_for_conflicting_actions()

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        if self.is_unfolding:
            self.actions.append(
                actions.SymbolicLink(self.subcmd, source, dest))
        else:
            self.actions.append(
                actions.AlreadyLinked(self.subcmd, source, dest))

    def are_directories(self, source, dest):
        if dest.is_symlink():
            self.unfold(dest.resolve(), dest)
        self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(
            actions.SymbolicLink(self.subcmd, source, dest))
