"""
todo
"""


class AbstractCommand():
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


class SymbolicLink(AbstractCommand):
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
        msg = "Link: {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class SymbolicLinkExists(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest

    def _logic(self):
        msg = "Link: Nothing To Do Already Linked {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class UnLink(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

    def _logic(self):
        self.target.unlink()


class MakeDirectory(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        super().__init__()
        self.target = target

    def _logic(self):
        self.target.mkdir()
