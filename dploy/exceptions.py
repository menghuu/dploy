"""
All the exceptions and their messages used by the program
"""
# pylint: disable=missing-docstring


ERROR_HEAD = 'dploy {subcmd}: can not {subcmd} '


class SourceIsSameAsDest():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "'{file}': A source argument is the same as the dest argument"
        self.exception = ValueError(self.msg.format(subcmd=subcmd, file=file))


class ConflictsWithAnotherSource():
    def __init__(self, subcmd, files):
        self.msg = ERROR_HEAD + "the following: Conflicts with other source {files}"
        files_list = '\n    '  + '\n    '.join(files)
        self.exception = ValueError(self.msg.format(subcmd=subcmd, files=files_list))


class ConflictsWithExistingFile():
    def __init__(self, subcmd, source, dest):
        self.msg = ERROR_HEAD + "'{source}': Conflicts with existing '{dest}'"
        self.exception = ValueError(self.msg.format(subcmd=subcmd, source=source, dest=dest))


class ConflictsWithExistingLink():
    def __init__(self, subcmd, source, dest):
        self.msg = ERROR_HEAD + "'{source}': Conflicts with existing link '{dest}'"
        self.exception = ValueError(self.msg.format(subcmd=subcmd, source=source, dest=dest))


class InsufficientPermissions():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "'{file}': Insufficient permissions"
        self.exception = PermissionError(self.msg.format(subcmd=subcmd, file=file))


class NoSuchDirectory():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "'{file}': No such directory"
        self.exception = NotADirectoryError(self.msg.format(subcmd=subcmd, file=file))


class PermissionDenied():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "'{file}': Permission denied"
        self.exception = PermissionError(self.msg.format(subcmd=subcmd, file=file))

# pylint: disable=invalid-name
class InsufficientPermissionsToSubcmdFrom():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "from '{file}': Insufficient permissions"
        self.exception = PermissionError(self.msg.format(subcmd=subcmd, file=file))


# pylint: disable=invalid-name
class NoSuchDirectoryToSubcmdInto():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "into '{file}': No such directory"
        self.exception = NotADirectoryError(self.msg.format(subcmd=subcmd, file=file))


# pylint: disable=invalid-name
class InsufficientPermissionsToSubcmdTo():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "to '{file}': Insufficient permissions"
        self.exception = PermissionError(self.msg.format(subcmd=subcmd, file=file))


class NoSuchFileOrDirectory():
    def __init__(self, subcmd, file):
        self.msg = ERROR_HEAD + "'{file}': No such file or directory"
        self.exception = FileNotFoundError(self.msg.format(subcmd=subcmd, file=file))
