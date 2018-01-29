"""
Tests for the link sub command
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import dploy

SUBCMD = 'clean'


def test_clean_with_simple_senario(source_only_files, dest):
    broken = os.path.join('..', 'source_only_files', 'bbb')
    dest_path = os.path.join(dest, 'bbb')
    os.symlink(broken, dest_path)
    assert os.readlink(dest_path) == broken
    dploy.clean([source_only_files], dest)
    assert not os.path.exists(dest_path)
