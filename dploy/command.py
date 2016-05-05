"""
todo
"""

import dploy.util


class AbstractBaseCommand():
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self):
        pass

    def _logic(self):
        pass

    def execute(self):
        """
        todo
        """
        self._logic()


class SymbolicLink(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, command, source, dest):
        super().__init__()
        self._source = source
        self._source_relative = dploy.util.get_relative_path(source,
                                                             dest.parent)
        self.command = command
        self._dest = dest

    @property
    def dest(self):
        """
        todo
        """
        return self._dest

    @property
    def source(self):
        """
        todo
        """
        return self._source

    @property
    def source_relative(self):
        """
        todo
        """
        return self._source_relative

    def _logic(self):
        print(self)
        self.dest.symlink_to(self.source_relative)

    def __repr__(self):
        return "dploy {command}: link {dest} => {source}".format(
            command=self.command, dest=self.dest, source=self.source)


class SymbolicLinkExists(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, command, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest
        self.command = command

    def _logic(self):
        msg = "dploy {command}: already linked {dest} => {source}"
        print(msg.format(command=self.command, source=self.source, dest=self.dest))


class UnLink(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, command, target):
        super().__init__()
        self.target = target
        self.command = command

    def _logic(self):
        msg = "dploy {command}: unlink {target} => {source}"
        print(msg.format(command=self.command, target=self.target, source=self.target.resolve()))
        self.target.unlink()


class MakeDirectory(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, command, target):
        super().__init__()
        self.target = target
        self.command = command

    def _logic(self):
        msg = "dploy {command}: make directory {target}"
        print(msg.format(target=self.target, command=self.command))
        self.target.mkdir()
