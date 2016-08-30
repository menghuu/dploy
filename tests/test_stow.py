"""
Tests for the stow stub command
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import pytest
import dploy
import utils


def test_stow_with_basic_senario(source_a, dest):
    dploy.stow([source_a], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_a', 'aaa')


def test_stow_with_the_same_tree_twice(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.stow([source_a], dest)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_a', 'aaa')


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


def test_stow_with_existing_file_conflicts(source_a, source_c, dest):
    dploy.stow([source_a], dest)

    with pytest.raises(ValueError):
        dploy.stow([source_c], dest)


def test_stow_with_existing_broken_link(source_a, dest):
    os.symlink('non_existant_source', os.path.join(dest, 'aaa'))

    with pytest.raises(ValueError):
        dploy.stow([source_a], dest)


def test_stow_with_source_conflicts(source_a, source_c, dest):
    with pytest.raises(ValueError):
        dploy.stow([source_a, source_c], dest)


def test_stow_with_non_existant_source(dest):
    with pytest.raises(ValueError):
        dploy.stow(['source'], dest)


def test_stow_with_non_existant_dest(source_a):
    with pytest.raises(ValueError):
        dploy.stow([source_a], 'dest')


def test_stow_with_file_as_source(file_a, dest):
    with pytest.raises(ValueError):
        dploy.stow([file_a], dest)


def test_stow_with_file_as_dest(source_a, file_a):
    with pytest.raises(ValueError):
        dploy.stow([source_a], file_a)


def test_stow_with_file_as_dest_and_source(file_a, file_b):
    with pytest.raises(ValueError):
        dploy.stow([file_a], file_b)


def test_stow_with_read_only_dest(source_a, dest):
    utils.read_only(dest)
    with pytest.raises(PermissionError):
        dploy.stow([source_a], dest)


def test_stow_with_write_only_source(source_a, source_c, dest):
    utils.write_only(source_a)
    with pytest.raises(PermissionError):
        dploy.stow([source_a, source_c], dest)


def test_stow_with_write_only_source_file(source_a, source_c, dest):
    utils.write_only(os.path.join(source_a, 'aaa'))
    with pytest.raises(PermissionError):
        dploy.stow([source_a, source_c], dest)
