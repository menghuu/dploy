"""
The logic and workings behind the stow and unstow sub commands
"""

from collections import defaultdict
from collections import Counter
import pathlib
import sys
import dploy.actions as actions
import dploy.utils as utils
import dploy.errors as errors


class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, sources, dest, is_silent, is_dry_run, ignores):
        self.subcmd = subcmd
        self.actions = []
        self.exceptions = []
        self.is_silent = is_silent
        self.is_dry_run = is_dry_run
        self.ignored = []
        if ignores is None:
            self.ignores = []
        else:
            self.ignores = ignores

        dest_input = pathlib.Path(dest)

        for source in sources:
            source_input = pathlib.Path(source)

            if self.is_ignored(source_input):
                self.ignored.append(source)
                continue
            if self.is_valid_input(source_input, dest_input):
                self.collect_actions(source_input, dest_input)

        self.check_for_other_actions()
        self.execute_actions()

    def check_for_other_actions(self):
        """
        todo
        """
        pass

    def is_valid_input(self, source, dest):
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
        if len(self.exceptions) > 0:
            if not self.is_silent:
                for exception in self.exceptions:
                    print(exception, file=sys.stderr)
            raise self.exceptions[0]
        else:
            for action in self.actions:
                if not self.is_silent:
                    print(action)
                if not self.is_dry_run:
                    action.execute()

    def add_exception(self, exception):
        """
        Add an exception to to be handled later
        """
        self.exceptions.append(exception.exception)

    def is_ignored(self, source):
        """
        check if a source should be ignored, based on the ignore patterns in
        self.ignores

        This checks if the ignore patterns match either the file exactly or
        its parents
        """
        for ignores in self.ignores:
            try:
                ignored_files = source.parent.glob(ignores)
            except ValueError: # TODO print this message for unacceptable glob pattern
                continue

            for file in ignored_files:
                if utils.is_same_file(file, source) or source in file.parents:
                    return True

        return False


class AbstractBaseStow(AbstractBaseSubCommand):
    """
    Abstract Base class that contains the shared logic for all of the stow
    commands
    """
    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, source, dest, is_silent, is_dry_run, ignores):
        self.is_unfolding = False
        super().__init__(subcmd, source, dest, is_silent, is_dry_run, ignores)

    def is_valid_input(self, source, dest):
        """
        valid the initial input to a stow command
        """
        result = True

        if not self.valid_source(source):
            result = False

        if not self.valid_dest(dest):
            result = False

        return result

    def valid_dest(self, dest):
        """
        valid dest arguments to for stowing
        """
        result = True

        if not dest.is_dir():
            self.add_exception(errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest))
            result = False
        else:
            if not utils.is_directory_writable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_readable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_executable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

        return result

    def valid_source(self, source):
        """
        valid source arguments to for stowing
        """
        result = True

        if not source.is_dir():
            self.add_exception(errors.NoSuchDirectory(self.subcmd, source))
            result = False
        else:
            if not utils.is_directory_readable(source):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

            if not utils.is_directory_executable(source):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

        return result

    def get_directory_contents(self, directory):
        """
        get the contents of a directory while handling errors that may occur
        """
        contents = []

        try:
            contents = utils.get_directory_contents(directory)
        except PermissionError:
            self.add_exception(errors.PermissionDenied(self.subcmd, directory))
        except FileNotFoundError:
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, directory))
        except NotADirectoryError:
            self.add_exception(errors.NoSuchDirectory(self.subcmd, directory))

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

    def is_valid_collection_input(self, source, dest):
        """
        Helper to validate the source and dest parameters passed to
        collect_actions()
        """
        result = True
        if not self.valid_source(source):
            result = False

        if dest.exists():
            if not self.valid_dest(dest):
                result = False
        return result

    def collect_actions_existing_dest(self, source, dest):
        """
        collect_actions() helper to collect required actions to perform a stow
        command when the destination exists
        """
        if utils.is_same_file(dest, source):
            if dest.is_symlink() or self.is_unfolding:
                self.are_same_file(source, dest)
            else:
                self.add_exception(errors.SourceIsSameAsDest(self.subcmd, dest.parent))

        elif dest.is_dir() and source.is_dir:
            self.are_directories(source, dest)
        else:
            self.add_exception(
                errors.ConflictsWithExistingFile(self.subcmd, source, dest))

    def collect_actions(self, source, dest):
        """
        collect required actions to perform a stow command
        """

        if self.is_ignored(source):
            self.ignored.append(source)
            return

        if not self.is_valid_collection_input(source, dest):
            return

        sources = self.get_directory_contents(source)

        for source in sources:
            if self.is_ignored(source):
                self.ignored.append(source)
                continue

            dest_path = dest / pathlib.Path(source.name)

            does_dest_path_exist = False
            try:
                does_dest_path_exist = dest_path.exists()
            except PermissionError:
                self.add_exception(errors.PermissionDenied(self.subcmd, dest_path))
                return

            if does_dest_path_exist:
                self.collect_actions_existing_dest(source, dest_path)
            elif dest_path.is_symlink():
                self.add_exception(
                    errors.ConflictsWithExistingLink(self.subcmd, source, dest_path))
            elif not dest_path.parent.exists() and not self.is_unfolding:
                self.add_exception(errors.NoSuchDirectory(self.subcmd, dest_path.parent))
            else:
                self.are_other(source, dest_path)


class UnStow(AbstractBaseStow):
    """
    Concrete class implementation of the unstow sub command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignores=None):
        super().__init__("unstow", source, dest, is_silent, is_dry_run, ignores)

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        self.actions.append(actions.UnLink(self.subcmd, dest))

    def are_directories(self, source, dest):
        self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(actions.AlreadyUnlinked(self.subcmd, source, dest))

    def check_for_other_actions(self):
        self.collect_folding_actions()

    def collect_folding_actions(self):
        """
        find candidates for folding i.e. when replacing a directories containing
        links with a single symlink to the directory itself would work instead
        """

        unlink_actions = (
            [a for a in self.actions if isinstance(a, actions.UnLink)])
        unlink_actions_targets = [a.target for a in unlink_actions]
        # sort for deterministic output
        unlink_actions_targets_parents = sorted(set([a.target.parent for a in unlink_actions]))

        for parent in unlink_actions_targets_parents:
            items = utils.get_directory_contents(parent)
            other_links = list(self.ignored)
            source_parent = None
            is_valid = True

            for item in items:
                if item in unlink_actions_targets:
                    pass
                else:
                    does_item_exist = False
                    try:
                        does_item_exist = item.exists()
                    except PermissionError:
                        self.add_exception(errors.PermissionDenied(self.subcmd, item))
                        return

                    if does_item_exist and item.is_symlink():
                        source_parent = item.resolve().parent
                        other_links.append(item.resolve().parent)
                    else:
                        is_valid = False
                        break

            other_links_counter = Counter(other_links)
            if len(other_links_counter.keys()) == 1 and is_valid:
                assert source_parent != None
                self.fold(source_parent, parent)
            if len(other_links_counter.keys()) == 0 and is_valid:
                self.actions.append(actions.RemoveDirectory(self.subcmd, parent))

    def fold(self, source, dest):
        """
        add the required actions for folding
        """
        self.collect_actions(source, dest)
        self.actions.append(actions.RemoveDirectory(self.subcmd, dest))
        self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


class Link(AbstractBaseSubCommand):
    """
    Concrete class implementation of the link sub command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignores=None):
        super().__init__("link", [source], dest, is_silent, is_dry_run, ignores)

    def is_valid_input(self, source, dest):
        """
        todo
        """
        if not source.exists():
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, source))
            return False

        elif not dest.parent.exists():
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, dest.parent))
            return False

        elif (not utils.is_file_readable(source)
              or not utils.is_directory_readable(source)):
            self.add_exception(errors.InsufficientPermissions(self.subcmd, source))
            return False

        elif (not utils.is_file_writable(dest.parent)
              or not utils.is_directory_writable(dest.parent)):
            self.add_exception(
                errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
            return False

        else:
            return True

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
                self.add_exception(
                    errors.ConflictsWithExistingFile(self.subcmd, source, dest))
        elif dest.is_symlink():
            self.add_exception(
                errors.ConflictsWithExistingLink(self.subcmd, source, dest))

        elif not dest.parent.exists():
            self.add_exception(
                errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest.parent))

        else:
            self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


class Stow(AbstractBaseStow):
    """
    Concrete class implementation of the stow sub command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignores=None):
        super().__init__("stow", source, dest, is_silent, is_dry_run, ignores)

    def unfold(self, source, dest):
        """
        todo
        """
        self.is_unfolding = True
        self.actions.append(actions.UnLink(self.subcmd, dest))
        self.actions.append(actions.MakeDirectory(self.subcmd, dest))
        self.collect_actions(source, dest)
        self.is_unfolding = False

    def get_duplicate_actions(self):
        """
        return a tuple containing tuples with the following structure
        (link destination, [indices of duplicates])
        """
        tally = defaultdict(list)
        for index, action in enumerate(self.actions):
            if isinstance(action, actions.SymbolicLink):
                tally[action.dest].append(index)
        # sort for deterministic output
        return sorted([indices for _, indices in tally.items() if len(indices) > 1])

    def handle_duplicate_actions(self):
        """
        check for symbolic link actions that would cause conflicting symbolic
        links to the same destination. Also check for actions that conflict but
        are candidates for unfolding instead.
        """
        has_conflicts = False
        dupes = self.get_duplicate_actions()

        if len(dupes) == 0:
            return

        for indices in dupes:
            first_action = self.actions[indices[0]]
            remaining_actions = [self.actions[i] for i in indices[1:]]

            if first_action.source.is_dir():
                self.unfold(first_action.source, first_action.dest)

                for action in remaining_actions:
                    self.is_unfolding = True
                    self.collect_actions(action.source, action.dest)
                    self.is_unfolding = False
            else:
                duplicate_action_sources = [str(self.actions[i].source) for i in indices]
                self.add_exception(
                    errors.ConflictsWithAnotherSource(self.subcmd, duplicate_action_sources))
                has_conflicts = True

        if has_conflicts:
            return

        # remove duplicates
        for indices in dupes:
            for index in reversed(indices[1:]):
                del self.actions[index]

        self.handle_duplicate_actions()

    def check_for_other_actions(self):
        self.handle_duplicate_actions()

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
