import pytest
import util
import os
import dploy


def test_stow_basic(source_a, dest):
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')


def test_stow_the_same_tree_twice(source_a, dest):
    dploy.stow('source_a', 'dest')
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')


def test_stow_unfolding_basic(source_a, source_b, dest):
    dploy.stow('source_a', 'dest')
    assert os.path.islink('dest/aaa')

    assert os.path.isfile('dest/aaa/aaa')
    assert os.path.isfile('dest/aaa/bbb')
    assert os.path.isdir('dest/aaa/ccc')

    dploy.stow('source_b', 'dest')
    assert os.path.isdir('dest/aaa')

    assert os.path.islink('dest/aaa/aaa')
    assert os.path.islink('dest/aaa/bbb')
    assert os.path.islink('dest/aaa/ccc')

    assert os.path.islink('dest/aaa/ddd')
    assert os.path.islink('dest/aaa/eee')
    assert os.path.islink('dest/aaa/fff')

def test_unfoling_with_conflicts(source_a, source_c, dest):
    dploy.stow('source_a', 'dest')

    with pytest.raises(SystemExit):
        dploy.stow('source_c', 'dest')


def test_with_non_existant_source(dest):
    with pytest.raises(SystemExit):
        dploy.stow('source', 'dest')

def test_with_non_existant_dest(source_a):
    with pytest.raises(SystemExit):
        dploy.stow('source_a', 'dest')
