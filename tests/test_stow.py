"""
Tests for the stow stub command
"""
# pylint: disable=unused-argument
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import pytest
import dploy
import util


def test_stow_with_basic_senario(source_a, dest):
    # pylint: disable=unused-argument
    dploy.stow(['source_a'], 'dest')
    assert os.readlink('dest/aaa') == '../source_a/aaa'


def test_stow_with_the_same_tree_twice(source_a, dest):
    # pylint: disable=unused-argument
    dploy.stow(['source_a'], 'dest')
    dploy.stow(['source_a'], 'dest')
    assert os.readlink('dest/aaa') == '../source_a/aaa'


def test_stow_unfolding_with_two_invocations(source_a, source_b, dest):
    # pylint: disable=unused-argument
    dploy.stow(['source_a'], 'dest')
    assert os.readlink('dest/aaa') == '../source_a/aaa'

    assert os.path.isfile('dest/aaa/aaa')
    assert os.path.isfile('dest/aaa/bbb')
    assert os.path.isdir('dest/aaa/ccc')

    dploy.stow(['source_b'], 'dest')
    assert os.path.isdir('dest/aaa')

    assert os.readlink('dest/aaa/aaa') == '../../source_a/aaa/aaa'
    assert os.readlink('dest/aaa/bbb') == '../../source_a/aaa/bbb'
    assert os.readlink('dest/aaa/ccc') == '../../source_a/aaa/ccc'

    assert os.readlink('dest/aaa/ddd') == '../../source_b/aaa/ddd'
    assert os.readlink('dest/aaa/eee') == '../../source_b/aaa/eee'
    assert os.readlink('dest/aaa/fff') == '../../source_b/aaa/fff'


def test_stow_unfolding_with_mutliple_sources(source_a, source_b, dest):
    # pylint: disable=unused-argument
    dploy.stow(['source_a', 'source_b'], 'dest')

    assert os.path.isdir('dest/aaa')
    assert os.readlink('dest/aaa/aaa') == '../../source_a/aaa/aaa'
    assert os.readlink('dest/aaa/bbb') == '../../source_a/aaa/bbb'
    assert os.readlink('dest/aaa/ccc') == '../../source_a/aaa/ccc'
    assert os.readlink('dest/aaa/ddd') == '../../source_b/aaa/ddd'
    assert os.readlink('dest/aaa/eee') == '../../source_b/aaa/eee'
    assert os.readlink('dest/aaa/fff') == '../../source_b/aaa/fff'


def test_stow_with_existing_file_conflicts(source_a, source_c, dest):
    # pylint: disable=unused-argument
    dploy.stow(['source_a'], 'dest')

    with pytest.raises(SystemExit):
        dploy.stow(['source_c'], 'dest')


def test_stow_with_existing_broken_link(source_a, dest):
    # pylint: disable=unused-argument
    os.symlink('non_existant_source', 'dest/aaa')

    with pytest.raises(SystemExit):
        dploy.stow(['source_a'], 'dest')


def test_stow_with_source_conflicts(source_a, source_c):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['source_a', 'source_c'], 'dest')


def test_stow_with_non_existant_source(dest):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['source'], 'dest')


def test_stow_with_non_existant_dest(source_a):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['source_a'], 'dest')


def test_stow_with_file_as_source(file_a, dest):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['file_a'], 'dest')


def test_stow_with_file_as_dest(source_a, file_a):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['source_a'], 'file_a')


def test_stow_with_file_as_dest_and_source(file_a, file_b):
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow(['file_a'], 'file_b')


def test_stow_with_read_only_dest(source_a, dest):
    util.read_only('dest')
    dploy.stow(['source_a'], 'dest')


def test_stow_with_write_only_source(source_a, dest):
    util.write_only('source_a')
    dploy.stow(['source_a'], 'dest')
