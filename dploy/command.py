"""
todo
"""

import os
import pathlib


class AbstractCommand():
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self):
        pass

    def logic(self):
        pass

    def execute(self):
        """
        todo
        """
        self.logic()


class SymbolicLink(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def logic(self):
        self.dest.symlink_to(self.source)
        msg = "Link: {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class SymbolicLinkExists(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def logic(self):
        msg = "Link: Nothing To Do Already Linked {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class UnLink(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        self.target = target

    def logic(self):
        self.target.unlink()


class MakeDirectory(AbstractCommand):
    # pylint: disable=too-few-public-methods
    """
    todo
    """
    def __init__(self, target):
        self.target = target

    def logic(self):
        self.target.mkdir()
