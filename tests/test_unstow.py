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


def test_unstow_with_basic_senario(source_a, dest):
    dploy.stow([source_a], dest)
    dploy.unstow([source_a], dest)
    assert not os.path.exists(os.path.join(dest, 'aaa'))


def test_unstow_with_existing_broken_link(source_a, dest):
    os.symlink('non_existant_source', os.path.join(dest, 'aaa'))

    with pytest.raises(ValueError):
        dploy.unstow([source_a], dest)


def test_unstow_with_existing_broken_link_in_source(source_a, dest):
    os.mkdir(os.path.join(dest, 'aaa'))
    dploy.stow([source_a], dest)
    os.symlink(os.path.join(source_a, 'non_existant_source'),
               os.path.join(dest, 'aaa', 'non_existant_source'))


def test_unstow_with_non_existant_source(dest):
    with pytest.raises(ValueError):
        dploy.unstow(['source'], dest)


def test_unstow_with_non_existant_dest(source_a):
    with pytest.raises(ValueError):
        dploy.unstow([source_a], 'dest')


def test_unstow_with_file_as_source(file_a, dest):
    with pytest.raises(ValueError):
        dploy.unstow([file_a], dest)


def test_unstow_with_file_as_dest(source_a, file_a):
    with pytest.raises(ValueError):
        dploy.unstow([source_a], file_a)


def test_unstow_with_file_as_dest_and_source(file_a, file_b):
    with pytest.raises(ValueError):
        dploy.unstow([file_a], file_b)


def test_unstow_with_read_only_dest(source_a, dest):
    dploy.stow([source_a], dest)
    utils.read_only(dest)
    with pytest.raises(PermissionError):
        dploy.unstow([source_a], dest)


def test_unstow_with_read_only_dest_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.read_only(os.path.join(dest, 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_write_only_source(source_a, dest):
    dploy.stow([source_a], dest)
    utils.write_only(source_a)
    with pytest.raises(PermissionError):
        dploy.unstow([source_a], dest)


def test_unstow_with_write_only_source_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.write_only(os.path.join(source_a, 'aaa', 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_write_only_dest_file(source_a, dest):
    dploy.stow([source_a], dest)
    utils.write_only(os.path.join(dest, 'aaa'))
    dploy.unstow([source_a], dest)


def test_unstow_with_same_directory_used_as_source_and_dest(source_a):
    with pytest.raises(ValueError):
        dploy.unstow([source_a], source_a)


def test_unstow_with_same_simple_directory_used_as_source_and_dest(source_only_files):
    with pytest.raises(ValueError):
        dploy.unstow([source_only_files], source_only_files)


def test_unstow_folding_basic(source_a, source_b, dest):
    dploy.stow([source_a, source_b], dest)
    dploy.unstow([source_b], dest)
    assert os.path.islink(os.path.join(dest, 'aaa'))


def test_unstow_folding_with_multiple_sources(source_a, source_b, source_d, dest):
    dploy.stow([source_a, source_b, source_d], dest)
    dploy.unstow([source_b, source_d], dest)
    assert os.path.islink(os.path.join(dest, 'aaa'))


def test_unstow_folding_with_multiple_stowed_sources(source_a, source_b, source_d, dest):
    dploy.stow([source_a, source_b, source_d], dest)
    dploy.unstow([source_b], dest)
    assert not os.path.islink(os.path.join(dest, 'aaa'))
