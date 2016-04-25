"""
todo
"""

import pytest
import util


@pytest.fixture()
def source_a(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('source_a'))
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
    return name


@pytest.fixture()
def source_b(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('source_b'))
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
    return name


@pytest.fixture()
def source_c(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('source_c'))
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
    return name


@pytest.fixture()
def dest(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('dest'))
    util.create_directory(name)
    return name


@pytest.fixture()
def file_a(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('file_a'))
    util.create_file(name)
    return name


@pytest.fixture()
def file_b(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('file_b'))
    util.create_file(name)
    return name
