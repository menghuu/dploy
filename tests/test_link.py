"""
todo
"""

import os
import pytest
import dploy


def test_link_basic(source_a, dest):
    # pylint: disable=unused-argument
    """
    todo
    """
    dploy.link('source_a', 'dest/source_a_link')
    assert os.path.islink('dest/source_a_link')

def test_link_non_existant_source(dest):
    # pylint: disable=unused-argument
    """
    todo
    """
    with pytest.raises(SystemExit):
        dploy.link('source_a', 'dest/source_a_link')

def test_link_non_existant_dest(source_a):
    # pylint: disable=unused-argument
    """
    todo
    """
    with pytest.raises(SystemExit):
        dploy.link('source_a', 'dest/source_a_link')
