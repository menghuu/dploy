"""
todo
"""


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
    def __init__(self, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest

    def _logic(self):
        self.dest.symlink_to(self.source)
        msg = "dploy stow: link {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class SymbolicLinkExists(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest

    def _logic(self):
        msg = "dploy stow: already linked {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class UnLink(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

    def _logic(self):
        msg = "dploy stow: unlink {target} => {source}"
        print(msg.format(target=self.target, source=self.target.resolve()))
        self.target.unlink()


class MakeDirectory(AbstractBaseCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

    def _logic(self):
        msg = "dploy stow: make directory {target}"
        print(msg.format(target=self.target))
        self.target.mkdir()
