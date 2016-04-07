"""
todo
"""

import os
import pytest
import dploy


def test_stow_basic(source_a, dest):
    """
    todo
    """
    # pylint: disable=unused-argument
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')


def test_stow_the_same_tree_twice(source_a, dest):
    """
    todo
    """
    # pylint: disable=unused-argument
    dploy.stow('source_a', 'dest')
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')


def test_stow_unfolding_basic(source_a, source_b, dest):
    """
    todo
    """
    # pylint: disable=unused-argument
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')

    assert os.path.isfile('dest/aaa/aaa')
    assert os.path.isfile('dest/aaa/bbb')
    assert os.path.isdir('dest/aaa/ccc')

    dploy.stow('source_b', 'dest')
    assert os.path.isdir('dest/aaa')

    assert os.path.islink('dest/aaa/aaa')
    assert os.path.samefile('dest/aaa/aaa','source_a/aaa/aaa')
    assert os.path.islink('dest/aaa/bbb')
    assert os.path.samefile('dest/aaa/bbb','source_a/aaa/bbb')
    assert os.path.islink('dest/aaa/ccc')
    assert os.path.samefile('dest/aaa/ccc','source_a/aaa/ccc')

    assert os.path.islink('dest/aaa/ddd')
    assert os.path.samefile('dest/aaa/ddd','source_b/aaa/ddd')
    assert os.path.islink('dest/aaa/eee')
    assert os.path.samefile('dest/aaa/eee','source_b/aaa/eee')
    assert os.path.islink('dest/aaa/fff')
    assert os.path.samefile('dest/aaa/fff','source_b/aaa/fff')

def test_unfoling_with_conflicts(source_a, source_c, dest):
    """
    todo
    """
    # pylint: disable=unused-argument
    dploy.stow('source_a', 'dest')

    with pytest.raises(SystemExit):
        dploy.stow('source_c', 'dest')


def test_with_non_existant_source(dest):
    """
    todo
    """
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow('source', 'dest')

def test_with_non_existant_dest(source_a):
    """
    todo
    """
    # pylint: disable=unused-argument
    with pytest.raises(SystemExit):
        dploy.stow('source_a', 'dest')
