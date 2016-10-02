"""
Tests for the ignore feature
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import dploy

SUBCMD = 'stow'

def test_ignore_by_ignoring_everthing(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignores=['*'])
    assert not os.path.exists(os.path.join(dest, 'aaa'))

def test_ignore_by_ignoring_only_subdirectory(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignores=['aaa'])
    assert not os.path.exists(os.path.join(dest, 'aaa'))

def test_ignore_by_ignoring_everthing_(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignores=['source_*/aaa'])
    assert not os.path.exists(os.path.join(dest, 'aaa'))

def test_ignore_by_ignoring_everthing__(source_a, source_c, dest):
    dploy.stow([source_a, source_c], dest, ignores=['*/aaa'])
    assert not os.path.exists(os.path.join(dest, 'aaa'))
