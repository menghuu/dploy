"""
The logic and workings behind the stow and unstow sub-commands
"""

from collections import defaultdict
from collections import Counter
import pathlib
import dploy.actions as actions
import dploy.utils as utils
import dploy.errors as errors
import dploy.ignore as ignore


# pylint: disable=too-few-public-methods
class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, sources, dest, is_silent, is_dry_run, ignore_patterns):
        self.subcmd = subcmd

        self.actions = actions.Actions(is_silent, is_dry_run)
        self.errors = errors.Errors(is_silent)

        self.is_silent = is_silent
        self.is_dry_run = is_dry_run

        dest_input = pathlib.Path(dest)


        if not self._is_there_duplicate_sources(sources):
            for source in sources:
                source_input = pathlib.Path(source)
                ignore_file = source_input.parent / pathlib.Path('.dploystowignore')
                self.ignore = ignore.Ignore(ignore_patterns, ignore_file)

                if self.ignore.should_ignore(source_input):
                    self.ignore.ignore(source_input)
                    continue
                if self._is_valid_input(source_input, dest_input):
                    self._collect_actions(source_input, dest_input)

        self._check_for_other_actions()
        self._execute_actions()

    def _check_for_other_actions(self):
        """
        Abstract method for examine the existing action to see if more actions
        need to be added or if some actions need to be removed.
        """
        pass

    def _is_valid_input(self, source, dest):
        """
        Abstract method to check if the input to a sub-command is valid
        """
        pass

    def _collect_actions(self, source, dest):
        """
        Abstract method that collects the actions required to complete a
        sub-command.
        """
        pass

    def _is_there_duplicate_sources(self, sources):
        """
        Checks sources to see if there are any duplicates
        """

        is_there_duplicates = False

        tally = defaultdict(int)
        for source in sources:
            tally[source] += 1

        for source, count in tally.items():
            if count > 1:
                is_there_duplicates = True
                self.errors.add(errors.DuplicateSource(self.subcmd, source))

        return is_there_duplicates



    def _execute_actions(self):
        """
        Either executes collected actions by a sub command or raises collected
        exceptions.
        """
        self.errors.handle()
        self.actions.execute()


class AbstractBaseStow(AbstractBaseSubCommand):
    """
    Abstract Base class that contains the shared logic for all of the stow
    commands
    """
    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, source, dest, is_silent, is_dry_run, ignore_patterns):
        self.is_unfolding = False
        super().__init__(subcmd, source, dest, is_silent, is_dry_run, ignore_patterns)

    def _is_valid_input(self, source, dest):
        """
        Check to see if the input is valid
        """
        result = True

        if not self._is_valid_source(source):
            result = False

        if not self._is_valid_dest(dest):
            result = False

        return result

    def _is_valid_collection_input(self, source, dest):
        """
        Helper to validate the source and dest parameters passed to
        _collect_actions()
        """
        result = True
        if not self._is_valid_source(source):
            result = False

        if dest.exists():
            if not self._is_valid_dest(dest):
                result = False
        return result

    def _is_valid_dest(self, dest):
        """
        Check if the dest argument is valid
        """
        result = True

        if not dest.is_dir():
            self.errors.add(errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest))
            result = False
        else:
            if not utils.is_directory_writable(dest):
                self.errors.add(errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_readable(dest):
                self.errors.add(errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_executable(dest):
                self.errors.add(errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

        return result

    def _is_valid_source(self, source):
        """
        Check if the source argument is valid
        """
        result = True

        if not source.is_dir():
            self.errors.add(errors.NoSuchDirectory(self.subcmd, source))
            result = False
        else:
            if not utils.is_directory_readable(source):
                self.errors.add(errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

            if not utils.is_directory_executable(source):
                self.errors.add(errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

        return result

    def get_directory_contents(self, directory):
        """
        Get the contents of a directory while handling errors that may occur
        """
        contents = []

        try:
            contents = utils.get_directory_contents(directory)
        except PermissionError:
            self.errors.add(errors.PermissionDenied(self.subcmd, directory))
        except FileNotFoundError:
            self.errors.add(errors.NoSuchFileOrDirectory(self.subcmd, directory))
        except NotADirectoryError:
            self.errors.add(errors.NoSuchDirectory(self.subcmd, directory))

        return contents

    def _are_same_file(self, source, dest):
        """
        Abstract method that handles the case when the source and dest are the
        same file when collecting actions
        """
        pass

    def _are_directories(self, source, dest):
        """
        Abstract method that handles the case when the source and dest are directories
        same file when collecting actions
        """
        pass

    def _are_other(self, source, dest):
        """
        Abstract method that handles all other cases what to do if no particular
        condition is true cases are found
        """
        pass

    def _collect_actions_existing_dest(self, source, dest):
        """
        _collect_actions() helper to collect required actions to perform a stow
        command when the destination already exists
        """
        if utils.is_same_file(dest, source):
            if dest.is_symlink() or self.is_unfolding:
                self._are_same_file(source, dest)
            else:
                self.errors.add(errors.SourceIsSameAsDest(self.subcmd, dest.parent))

        elif dest.is_dir() and source.is_dir:
            self._are_directories(source, dest)
        else:
            self.errors.add(errors.ConflictsWithExistingFile(self.subcmd, source, dest))

    def _collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a stow
        sub-command
        """

        if self.ignore.should_ignore(source):
            self.ignore.ignore(source)
            return

        if not self._is_valid_collection_input(source, dest):
            return

        sources = self.get_directory_contents(source)

        for source in sources:
            if self.ignore.should_ignore(source):
                self.ignore.ignore(source)
                continue

            dest_path = dest / pathlib.Path(source.name)

            does_dest_path_exist = False
            try:
                does_dest_path_exist = dest_path.exists()
            except PermissionError:
                self.errors.add(errors.PermissionDenied(self.subcmd, dest_path))
                return

            if does_dest_path_exist:
                self._collect_actions_existing_dest(source, dest_path)
            elif dest_path.is_symlink():
                self.errors.add(errors.ConflictsWithExistingLink(self.subcmd, source, dest_path))
            elif not dest_path.parent.exists() and not self.is_unfolding:
                self.errors.add(errors.NoSuchDirectory(self.subcmd, dest_path.parent))
            else:
                self._are_other(source, dest_path)


class Stow(AbstractBaseStow):
    """
    Concrete class implementation of the stow sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("stow", source, dest, is_silent, is_dry_run, ignore_patterns)

    def _unfold(self, source, dest):
        """
        Method unfold a destination directory
        """
        self.is_unfolding = True
        self.actions.add(actions.UnLink(self.subcmd, dest))
        self.actions.add(actions.MakeDirectory(self.subcmd, dest))
        self._collect_actions(source, dest)
        self.is_unfolding = False

    def _handle_duplicate_actions(self):
        """
        check for symbolic link actions that would cause conflicting symbolic
        links to the same destination. Also check for actions that conflict but
        are candidates for unfolding instead.
        """
        has_conflicts = False
        dupes = self.actions.get_duplicates()

        if len(dupes) == 0:
            return

        for indices in dupes:
            first_action = self.actions.actions[indices[0]]
            remaining_actions = [self.actions.actions[i] for i in indices[1:]]

            if first_action.source.is_dir():
                self._unfold(first_action.source, first_action.dest)

                for action in remaining_actions:
                    self.is_unfolding = True
                    self._collect_actions(action.source, action.dest)
                    self.is_unfolding = False
            else:
                duplicate_action_sources = [str(self.actions.actions[i].source) for i in indices]
                self.errors.add(
                    errors.ConflictsWithAnotherSource(self.subcmd, duplicate_action_sources))
                has_conflicts = True

        if has_conflicts:
            return

        # remove duplicates
        for indices in dupes:
            for index in reversed(indices[1:]):
                del self.actions.actions[index]

        self._handle_duplicate_actions()

    def _check_for_other_actions(self):
        self._handle_duplicate_actions()

    def _are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        if self.is_unfolding:
            self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))
        else:
            self.actions.add(actions.AlreadyLinked(self.subcmd, source, dest))

    def _are_directories(self, source, dest):
        if dest.is_symlink():
            self._unfold(dest.resolve(), dest)
        self._collect_actions(source, dest)

    def _are_other(self, source, dest):
        self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))


class UnStow(AbstractBaseStow):
    """
    Concrete class implementation of the unstow sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("unstow", source, dest, is_silent, is_dry_run, ignore_patterns)

    def _are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        self.actions.add(actions.UnLink(self.subcmd, dest))

    def _are_directories(self, source, dest):
        self._collect_actions(source, dest)

    def _are_other(self, source, dest):
        self.actions.add(actions.AlreadyUnlinked(self.subcmd, source, dest))

    def _check_for_other_actions(self):
        self._collect_folding_actions()

    def _collect_folding_actions(self):
        """
        find candidates for folding i.e. when a directory contains symlinks to
        files that all share the same parent directory
        """
        for parent in self.actions.get_unlink_target_parents():
            items = utils.get_directory_contents(parent)
            other_links_parents = []
            other_links = []
            source_parent = None
            is_normal_files_detected = False

            for item in items:
                if item not in self.actions.get_unlink_targets():
                    does_item_exist = False
                    try:
                        does_item_exist = item.exists()
                    except PermissionError:
                        self.errors.add(errors.PermissionDenied(self.subcmd, item))
                        return

                    if does_item_exist and item.is_symlink():
                        source_parent = item.resolve().parent
                        other_links_parents.append(item.resolve().parent)
                        other_links.append(item)
                    else:
                        is_normal_files_detected = True
                        break

            if not is_normal_files_detected:
                other_links_parent_count = len(Counter(other_links_parents))

                if other_links_parent_count == 1:
                    assert source_parent != None
                    if utils.is_same_files(utils.get_directory_contents(source_parent),
                                           other_links):
                        self._fold(source_parent, parent)

                elif other_links_parent_count == 0:
                    self.actions.add(actions.RemoveDirectory(self.subcmd, parent))

    def _fold(self, source, dest):
        """
        add the required actions for folding
        """
        self._collect_actions(source, dest)
        self.actions.add(actions.RemoveDirectory(self.subcmd, dest))
        self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))


# pylint: disable=too-few-public-methods
class Link(AbstractBaseSubCommand):
    """
    Concrete class implementation of the link sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("link", [source], dest, is_silent, is_dry_run, ignore_patterns)

    def _is_valid_input(self, source, dest):
        """
        Check to see if the input is valid
        """
        if not source.exists():
            self.errors.add(errors.NoSuchFileOrDirectory(self.subcmd, source))
            return False

        elif not dest.parent.exists():
            self.errors.add(errors.NoSuchFileOrDirectory(self.subcmd, dest.parent))
            return False

        elif (not utils.is_file_readable(source)
              or not utils.is_directory_readable(source)):
            self.errors.add(errors.InsufficientPermissions(self.subcmd, source))
            return False

        elif (not utils.is_file_writable(dest.parent)
              or not utils.is_directory_writable(dest.parent)):
            self.errors.add(errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
            return False

        else:
            return True

    def _collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a link
        sub-command
        """

        if dest.exists():
            if utils.is_same_file(dest, source):
                self.actions.add(actions.AlreadyLinked(self.subcmd, source, dest))
            else:
                self.errors.add(errors.ConflictsWithExistingFile(self.subcmd, source, dest))
        elif dest.is_symlink():
            self.errors.add(errors.ConflictsWithExistingLink(self.subcmd, source, dest))

        elif not dest.parent.exists():
            self.errors.add(errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest.parent))

        else:
            self.actions.add(actions.SymbolicLink(self.subcmd, source, dest))
