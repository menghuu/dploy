import pytest
import os
import dploy


def test_link_basic(source_a, dest):
    dploy.link('source_a', 'dest/source_a_link')
    assert os.path.islink('dest/source_a_link')

def test_link_non_existant_source(dest):
    with pytest.raises(SystemExit):
        dploy.link('source_a', 'dest/source_a_link')

def test_link_non_existant_dest(source_a):
    with pytest.raises(SystemExit):
        dploy.link('source_a', 'dest/source_a_link')
