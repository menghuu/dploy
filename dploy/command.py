import os
import pathlib

class AbstractCommand():
    def __init__(self):
        pass

    def logic(self):
        pass

    def execute(self):
        self.logic()



class SymbolicLink(AbstractCommand):
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def logic(self):
        self.dest.symlink_to(self.source)
        msg = "Link: {dest} => {source}"
        print(msg.format(source=self.source, dest=self.dest))


class UnLink(AbstractCommand):
    def __init__(self, target):
        self.target = target

    def logic(self):
        self.target.unlink()


class MakeDirectory(AbstractCommand):
    def __init__(self, target):
        self.target = target

    def logic(self):
        self.target.mkdir()
