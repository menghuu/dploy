import sys
import pathlib
import dploy.util

def link(source, dest):
    """
    sub command link
    """
    source_input = pathlib.Path(source)
    dest_input = pathlib.Path(dest)

    if not source_input.exists():
        msg = "dploy link: can not link '{file}': No such directory"
        print(msg.format(file=source_input))
        sys.exit(1)

    source_absolute = dploy.util.get_absolute_path(source_input)
    dest_absolute = dploy.util.get_absolute_path(dest_input)

    _link_absolute_paths(source_absolute, dest_absolute)


def _link_absolute_paths(source, dest):
    """
    todo
    """
    assert source.is_absolute()
    assert dest.is_absolute()
    assert source.exists()

    src_file_relative = dploy.util.get_relative_path(source,
                                           dest.parent)
    try:
        dest.symlink_to(src_file_relative)
        msg = "Link: {dest} => {source}"
        print(msg.format(source=src_file_relative, dest=dest))

    except FileExistsError:
        if dploy.util.is_same_file(dest, source):
            msg = "Link: Already Linked {dest} => {source}"
            print(msg.format(source=src_file_relative, dest=dest))

        else:
            msg = "Abort: {file} Already Exists"
            print(msg.format(file=dest))
            sys.exit(1)

    except FileNotFoundError:
        msg = "Abort: {dest} Not Found"
        print(msg.format(dest=dest))
        sys.exit(1)
