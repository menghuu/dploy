"""
All the exceptions and their messages used by the program
"""
# pylint: disable=missing-docstring


ERROR_HEAD = 'dploy {subcmd}: can not {subcmd} '


def source_is_same_as_dest(subcmd, file):
    msg = ERROR_HEAD + "'{file}': A source argument is the same as the dest argument"
    return ValueError(msg.format(subcmd=subcmd, file=file))


def conflicts_with_another_source(subcmd, files):
    files_list = '\n    '  + '\n    '.join(files)
    msg = ERROR_HEAD + "the following: Conflicts with other source {files}"
    return ValueError(msg.format(subcmd=subcmd, files=files_list))


def conflicts_with_existing_file(subcmd, source, dest):
    msg = ERROR_HEAD + "'{source}': Conflicts with existing '{dest}'"
    return ValueError(msg.format(subcmd=subcmd, source=source, dest=dest))


def conflicts_with_existing_link(subcmd, source, dest):
    msg = ERROR_HEAD + "'{source}': Conflicts with existing link '{dest}'"
    return ValueError(msg.format(subcmd=subcmd, source=source, dest=dest))


def insufficient_permissions(subcmd, file):
    msg = ERROR_HEAD + "'{file}': Insufficient permissions"
    return PermissionError(msg.format(subcmd=subcmd, file=file))


def no_such_directory(subcmd, file):
    msg = ERROR_HEAD + "'{file}': No such directory"
    return NotADirectoryError(msg.format(subcmd=subcmd, file=file))


def permission_denied(subcmd, file):
    msg = ERROR_HEAD + "'{file}': Permission denied"
    return PermissionError(msg.format(subcmd=subcmd, file=file))

# pylint: disable=invalid-name
def insufficient_permissions_to_subcmd_from(subcmd, file):
    msg = ERROR_HEAD + "from '{file}': Insufficient permissions"
    return PermissionError(msg.format(subcmd=subcmd, file=file))


# pylint: disable=invalid-name
def no_such_directory_to_subcmd_into(subcmd, file):
    msg = ERROR_HEAD + "into '{file}': No such directory"
    return NotADirectoryError(msg.format(subcmd=subcmd, file=file))


# pylint: disable=invalid-name
def insufficient_permissions_to_subcmd_to(subcmd, file):
    msg = ERROR_HEAD + "to '{file}': Insufficient permissions"
    return PermissionError(msg.format(subcmd=subcmd, file=file))


def no_such_file_or_directory(subcmd, file):
    msg = ERROR_HEAD + "'{file}': No such file or directory"
    return FileNotFoundError(msg.format(subcmd=subcmd, file=file))
