"""
todo
"""

import pytest
import util


@pytest.fixture()
def source_a(request):
    """
    todo
    """
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

    def _source_a_teardown():
        util.remove_tree(name)
    request.addfinalizer(_source_a_teardown)


@pytest.fixture()
def source_b(request):
    """
    todo
    """
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

    def _source_b_teardown():
        util.remove_tree(name)
    request.addfinalizer(_source_b_teardown)


@pytest.fixture()
def source_c(request):
    """
    todo
    """
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

    def _source_c_teardown():
        util.remove_tree(name)
    request.addfinalizer(_source_c_teardown)


@pytest.fixture()
def dest(request):
    """
    todo
    """
    name = 'dest'
    util.create_directory(name)

    def _dest_teardown():
        util.remove_tree(name)
    request.addfinalizer(_dest_teardown)
