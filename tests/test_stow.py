"""
Tests for the stow stub command
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import pytest
import dploy
import dploy.errors as errors
import utils

SUBCMD = 'stow'

def test_stow_with_simple_senario(source_only_files, dest):
    dploy.stow([source_only_files], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_only_files', 'aaa')


def test_stow_with_basic_senario(source_a, dest):
    dploy.stow([source_a], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_a', 'aaa')


def test_stow_with_the_same_tree_twice(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.stow([source_a], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_a', 'aaa')


def test_stow_with_existing_file_conflicts(source_a, source_c, dest):
    dploy.stow([source_a], dest)
    with pytest.raises(ValueError) as e:
        dploy.stow([source_c], dest)
    source_file = os.path.join(source_c, 'aaa', 'aaa')
    conflicting_file = os.path.join(dest, 'aaa', 'aaa')
    assert (errors.ConflictsWithExistingFile(subcmd=SUBCMD,
                                             source=source_file,
                                             dest=conflicting_file).msg in str(e.value))


def test_stow_with_existing_broken_link(source_a, dest):
    conflicting_link = os.path.join(dest, 'aaa')
    os.symlink('non_existant_source', conflicting_link)
    with pytest.raises(ValueError) as e:
        dploy.stow([source_a], dest)
    source_file = os.path.join(source_a, 'aaa')
    assert (errors.ConflictsWithExistingLink(subcmd=SUBCMD,
                                             source=source_file,
                                             dest=conflicting_link).msg in str(e.value))


def test_stow_with_source_conflicts(source_a, source_c, dest):
    with pytest.raises(ValueError) as e:
        dploy.stow([source_a, source_c], dest)
    conflicting_source_files = [
        os.path.join(source_a, 'aaa', 'aaa'),
        os.path.join(source_c, 'aaa', 'aaa'),
    ]
    assert (errors.ConflictsWithAnotherSource(subcmd=SUBCMD,
                                              files=conflicting_source_files).msg in str(e.value))


def test_stow_with_non_existant_source(dest):
    non_existant_source = 'source'
    with pytest.raises(NotADirectoryError) as e:
        dploy.stow([non_existant_source], dest)
    assert (errors.NoSuchDirectory(subcmd=SUBCMD,
                                   file=non_existant_source).msg in str(e.value))


def test_stow_with_non_existant_dest(source_a):
    non_existant_dest = 'dest'
    with pytest.raises(NotADirectoryError) as e:
        dploy.stow([source_a], 'dest')
    assert (errors.NoSuchDirectoryToSubcmdInto(subcmd=SUBCMD,
                                               file=non_existant_dest).msg in str(e.value))


def test_stow_with_file_as_source(file_a, dest):
    with pytest.raises(NotADirectoryError) as e:
        dploy.stow([file_a], dest)
    assert (errors.NoSuchDirectory(subcmd=SUBCMD, file=file_a).msg
            in str(e.value))


def test_stow_with_file_as_dest(source_a, file_a):
    with pytest.raises(NotADirectoryError) as e:
        dploy.stow([source_a], file_a)
    assert (errors.NoSuchDirectoryToSubcmdInto(subcmd=SUBCMD, file=file_a).msg
            in str(e.value))


def test_stow_with_file_as_dest_and_source(file_a, file_b):
    with pytest.raises(NotADirectoryError) as e:
        dploy.stow([file_a], file_b)
    assert (errors.NoSuchDirectory(subcmd=SUBCMD, file=file_a).msg
            in str(e.value))


def test_stow_with_same_directory_used_as_source_and_dest(source_a):
    with pytest.raises(ValueError) as e:
        dploy.stow([source_a], source_a)
    assert (errors.SourceIsSameAsDest(subcmd=SUBCMD, file=source_a).msg
            in str(e.value))



def test_stow_with_same_simple_directory_used_as_source_and_dest(source_only_files):
    with pytest.raises(ValueError) as e:
        dploy.stow([source_only_files], source_only_files)
    assert (errors.SourceIsSameAsDest(subcmd=SUBCMD, file=source_only_files).msg
            in str(e.value))


def test_stow_with_read_only_dest(source_a, dest):
    utils.remove_write_permission(dest)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_a], dest)
    assert (errors.InsufficientPermissionsToSubcmdTo(subcmd=SUBCMD, file=dest).msg
            in str(e.value))


def test_stow_with_write_only_source(source_a, source_c, dest):
    utils.remove_read_permission(source_a)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_a, source_c], dest)
    assert (errors.InsufficientPermissions(subcmd=SUBCMD, file=source_a).msg
            in str(e.value))


def test_stow_with_source_with_no_executue_permissions(source_a, source_c, dest):
    utils.remove_execute_permission(source_a)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_a, source_c], dest)
    assert (errors.InsufficientPermissions(subcmd=SUBCMD, file=source_a).msg
            in str(e.value))


def test_stow_with_source_dir_with_no_executue_permissions(source_a, source_c, dest):
    source_dir = os.path.join(source_a, 'aaa')
    utils.remove_execute_permission(source_dir)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_a, source_c], dest)
    assert (errors.InsufficientPermissions(subcmd=SUBCMD, file=source_dir).msg
            in str(e.value))


def test_stow_with_write_only_source_file(source_a, source_c, dest):
    # FIXME this isn't a file
    source_file = os.path.join(source_a, 'aaa')
    utils.remove_read_permission(source_file)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_a, source_c], dest)
    assert (errors.InsufficientPermissions(subcmd=SUBCMD, file=source_file).msg
            in str(e.value))


def test_stow_unfolding_with_two_invocations(source_a, source_b, dest):
    dploy.stow([source_a], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_a', 'aaa')

    assert os.path.isfile(os.path.join(dest, 'aaa', 'aaa'))
    assert os.path.isfile(os.path.join(dest, 'aaa', 'bbb'))
    assert os.path.isdir(os.path.join(dest, 'aaa', 'ccc'))

    dploy.stow([source_b], dest)
    assert os.path.isdir(os.path.join(dest, 'aaa'))

    assert (os.readlink(os.path.join(dest, 'aaa', 'aaa')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'aaa'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'bbb')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'bbb'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'ccc')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'ccc'))

    assert (os.readlink(os.path.join(dest, 'aaa', 'ddd')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'ddd'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'eee')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'eee'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'fff')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'fff'))


def test_stow_unfolding_with_mutliple_sources(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest)

    assert os.path.isdir(os.path.join(dest, 'aaa'))

    assert (os.readlink(os.path.join(dest, 'aaa', 'aaa')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'aaa'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'bbb')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'bbb'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'ccc')) ==
            os.path.join('..', '..', 'source_a', 'aaa', 'ccc'))

    assert (os.readlink(os.path.join(dest, 'aaa', 'ddd')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'ddd'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'eee')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'eee'))
    assert (os.readlink(os.path.join(dest, 'aaa', 'fff')) ==
            os.path.join('..', '..', 'source_b', 'aaa', 'fff'))


def test_stow_unfolding_with_first_sources_execute_permission_removed(source_a, source_b, dest):
    dploy.stow([source_a], dest)
    utils.remove_execute_permission(source_a)
    with pytest.raises(PermissionError) as e:
        dploy.stow([source_b], dest)
    # FIXME it seems like the source should be used instead of dest and
    # InsufficientPermissionsToSubcmdFrom
    dest_dir = os.path.join(dest, 'aaa')
    assert (errors.PermissionDenied(subcmd=SUBCMD, file=dest_dir).msg
            in str(e.value))
