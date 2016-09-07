"""
todo
"""

import pytest
import utils


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
    utils.create_tree(tree)
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
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_c(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('source_c'))
    tree = [
        {
            name: [
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
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_only_files(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('source_only_files'))
    tree = [
        {
            name: [
                'aaa',
                'aaa',
            ]
        }
    ]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def dest(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('dest'))
    utils.create_directory(name)
    return name


@pytest.fixture()
def file_a(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('file_a'))
    utils.create_file(name)
    return name


@pytest.fixture()
def file_b(tmpdir):
    """
    todo
    """
    name = str(tmpdir.join('file_b'))
    utils.create_file(name)
    return name
