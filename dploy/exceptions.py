"""
All the exceptions and their messages used by the program
"""
# pylint: disable=missing-docstring


ERROR_HEAD = 'dploy {subcmd}: can not {subcmd} '


def source_is_same_as_dest(subcmd, file):
    msg = ERROR_HEAD + "'{file}': A source argument is the same as the dest argument"
    return ValueError(msg.format(subcmd=subcmd, file=file))


def conflicts_with_another_source(subcmd, file):
    msg = ERROR_HEAD + "'{file}': Conflicts with another source"
    return ValueError(msg.format(subcmd=subcmd, file=file))


def conflicts_with_existing_file(subcmd, file):
    msg = ERROR_HEAD + "'{file}': Conflicts with existing file"
    return ValueError(msg.format(subcmd=subcmd, file=file))


def conflicts_with_existing_link(subcmd, file):
    msg = ERROR_HEAD + "'{file}': Conflicts with existing link"
    return ValueError(msg.format(subcmd=subcmd, file=file))


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
