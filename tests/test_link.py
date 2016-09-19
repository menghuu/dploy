"""
Tests for the link sub command
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import pytest
import dploy
import utils


def test_link_with_directory_as_source(source_a, dest):
    dploy.link(source_a, os.path.join(dest, 'source_a_link'))
    assert os.path.islink(os.path.join(dest, 'source_a_link'))


def test_link_with_file_as_source(file_a, dest):
    dploy.link(file_a, os.path.join(dest, 'file_a'))
    assert os.path.islink(os.path.join(dest, 'file_a'))


def test_link_with_non_existant_source(dest):
    with pytest.raises(FileNotFoundError):
        dploy.link('source_a', os.path.join(dest, 'source_a_link'))


def test_link_with_non_existant_dest(source_a):
    with pytest.raises(FileNotFoundError):
        dploy.link(source_a, os.path.join('dest', 'source_a_link'))


def test_link_with_read_only_dest(file_a, dest):
    utils.read_only(dest)
    with pytest.raises(PermissionError):
        dploy.link(file_a, os.path.join(dest, 'file_a_link'))


def test_link_with_write_only_source(file_a, dest):
    utils.write_only(file_a)
    with pytest.raises(PermissionError):
        dploy.link(file_a, os.path.join(dest, 'file_a_link'))


def test_link_with_conflicting_broken_link_at_dest(file_a, dest):
    os.symlink('non_existant_source', os.path.join(dest, 'file_a_link'))
    with pytest.raises(ValueError) as e:
        dploy.link(file_a, os.path.join(dest, 'file_a_link'))
    assert utils.is_subcmd_error_message('link', e)
