import sys
import pathlib
import dploy.command
import dploy.util

class AbstractBaseStow():
    """
    An abstract class to unify shared functionality in stow commands
    """

    def __init__(self, sources, dest):
        self.commands = []
        self.abort = False

        for source in sources:
            source_input = pathlib.Path(source)
            dest_input = pathlib.Path(dest)
            source_absolute = dploy.util.get_absolute_path(source_input)
            dest_absolute = dploy.util.get_absolute_path(dest_input)

            self.validate_input(source_input, dest_input)
            assert source_absolute.is_dir()
            assert source_absolute.is_absolute()
            assert dest_absolute.is_absolute()
            self.collect_commands(source_absolute, dest_absolute)

        self.check_for_conflicting_commands()
        self.execute_commands()

    def validate_input(self, source, dest):
        if not source.exists():
            print(self.invalid_source_message.format(file=source))
            sys.exit(1)

        if not dest.exists():
            print(self.invalid_dest_message.format(file=dest))
            sys.exit(1)

    def collect_commands(self, source, dest):
        """
        todo
        """
        pass

    def check_for_conflicting_commands(self):
        """
        check for symbolic link commands that would cause conflicting symbolic
        links to the same destination.
        """
        link_commands_arugments = []
        for cmd in self.commands:
            if isinstance(cmd, dploy.command.SymbolicLink):
                link_commands_arugments.append(cmd.arguments)

        duplicates = []
        seen = []
        for source, dest in link_commands_arugments:
            if dest in seen:
                duplicates.append((source, dest))
            seen.append(dest)

        if len(duplicates) > 0:
            for duplicate in duplicates:
                source, dest = duplicate
                msg = "dploy stow: can not stow '{source}': Conflicts with another source"
                print(msg.format(source=source))
            self.abort = True

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
        self.invalid_source_message =  "dploy stow: can not unstow from '{file}': No such directory"
        self.invalid_dest_message =   "dploy stow: can not unstow '{file}': No such directory"
        super().__init__(source, dest)

    def collect_commands(self, source, dest):
        """
        todo
        """

        sources = dploy.util.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)
            source_relative = dploy.util.get_relative_path(source,
                                                 dest_path.parent)
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
                    # TODO add test for this
                    msg = "dploy stow: can not unstow '{file}': Conflicts with a broken link"
                    print(msg.format(file=dest_path))

            elif not dest_path.parent.exists():
                pass
                msg = "dploy stow: can not unstow '{dest}': No such directory"
                print(msg.format(dest=dest_path.parent))
            else:
                pass


class Stow(AbstractBaseStow):
    """
    todo
    """
    def __init__(self, source, dest):
        self.invalid_source_message =  "dploy stow: can not stow '{file}': No such directory"
        self.invalid_dest_message =  "dploy stow: can not stow into '{file}': No such directory"
        super().__init__(source, dest)

    def unfold(self, dest):
        """
        todo
        """
        self.commands.append(dploy.command.UnLink(dest))
        self.commands.append(dploy.command.MakeDirectory(dest))
        self.collect_commands(dest.resolve(), dest, is_unfolding=True)

    def collect_commands(self, source, dest, is_unfolding=False):
        """
        todo
        """

        sources = dploy.util.get_directory_contents(source)

        for source in sources:
            dest_path = dest / pathlib.Path(source.name)
            source_relative = dploy.util.get_relative_path(source,
                                                 dest_path.parent)
            if dest_path.exists():
                if dploy.util.is_same_file(dest_path, source):

                    if is_unfolding:
                        self.commands.append(
                            dploy.command.SymbolicLink(source_relative,
                                                       dest_path))
                    else:
                        self.commands.append(
                            dploy.command.SymbolicLinkExists(source_relative,
                                                             dest_path))
                elif dest_path.is_dir() and source.is_dir:
                    if dest_path.is_symlink():
                        self.unfold(dest_path)
                    self.collect_commands(source, dest_path)
                else:
                    msg = "dploy stow: can not stow '{file}': Conflicts with existing file"
                    print(msg.format(file=dest_path))
                    self.abort = True

            elif dest_path.is_symlink():
                    # TODO add test for this
                    msg = "dploy stow: can not stow '{file}': Conflicts with a broken link"
                    print(msg.format(file=dest_path))
                    self.abort = True

            elif not dest_path.parent.exists():
                msg = "dploy stow: can not stow into '{dest}': No such directory"
                print(msg.format(dest=dest_path.parent))
                self.abort = True

            else:
                self.commands.append(
                    dploy.command.SymbolicLink(source_relative, dest_path))
