import pytest
import util
import os
import dploy


@pytest.fixture(scope='module')
def source_a(request):
    name = 'source_a'
    tree = [
        {
            name : [
                {
                    'aaa': [
                        'aaa',
                        'bbb',
                        {
                            'ccc': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    util.create_tree(tree)

    def source_a_teardown():
        util.remove_tree(name)
    request.addfinalizer(source_a_teardown)


@pytest.fixture(scope='module')
def source_b(request):
    name = 'source_b'
    tree = [
        {
            name : [
                {
                    'aaa': [
                        'ddd',
                        'eee',
                        {
                            'fff': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    util.create_tree(tree)

    def source_b_teardown():
        util.remove_tree(name)
    request.addfinalizer(source_b_teardown)


@pytest.fixture(scope='module')
def source_c(request):
    name = 'source_c'
    tree = [
        {
            name : [
                {
                    'aaa': [
                        'aaa',
                        'bbb',
                        {
                            'ccc': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    util.create_tree(tree)

    def source_c_teardown():
        util.remove_tree(name)
    request.addfinalizer(source_c_teardown)


@pytest.fixture(scope='module')
def dest(request):
    name = 'dest'
    util.create_directory(name)

    def dest_teardown():
        util.remove_tree(name)
    request.addfinalizer(dest_teardown)


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
    dploy.stow('source_c', 'dest')
