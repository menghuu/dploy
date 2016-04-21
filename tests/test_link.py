"""
Tests for the link sub command
"""
# pylint: disable=unused-argument
# pylint: disable=missing-docstring

import os
import pytest
import dploy
import util


def test_link_directory(source_a, dest):
    dploy.link(['source_a'], 'dest/source_a_link')
    assert os.path.islink('dest/source_a_link')


def test_link_file(source_a, dest):
    dploy.link(['source_a/aaa/aaa'], 'dest/source_a_link')
    assert os.path.islink('dest/source_a_link')


def test_link_with_non_existant_source(dest):
    with pytest.raises(SystemExit):
        dploy.link(['source_a'], 'dest/source_a_link')


def test_link_with_non_existant_dest(source_a):
    with pytest.raises(SystemExit):
        dploy.link(['source_a'], 'dest/source_a_link')


def test_link_with_read_only_dest(file_a, dest):
    util.read_only('dest')
    dploy.link(['file_a'], 'dest/file_a_link')


def test_link_with_write_only_source(file_a, dest):
    util.write_only('file_a')
    dploy.link(['file_a'], 'dest/file_a_link')
