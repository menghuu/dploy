"""
Tests for the CLI interface
"""
# pylint: disable=missing-docstring
# disable lint errors for function names longer that 30 characters
# pylint: disable=invalid-name

import os
import re
import pytest
import dploy.cli

def test_cli_output_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = ['stow', source_only_files, dest]
    dploy.cli.run(args)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_only_files', 'aaa')
    out, _ = capsys.readouterr()
    d = os.path.join(dest, 'aaa')
    s = os.path.join(source_only_files, 'aaa')
    assert out == "dploy stow: link {dest} => {source}\n".format(source=s, dest=d)


def test_cli_output_with_link_directory(source_a, dest, capsys):
    args = ['link', source_a, os.path.join(dest, 'source_a_link')]
    dploy.cli.run(args)
    assert os.path.islink(os.path.join(dest, 'source_a_link'))
    output, _ = capsys.readouterr()
    expected_output_unformatted = "dploy link: link {dest} => {source}\n"
    expected_output = expected_output_unformatted.format(source=source_a,
                                                         dest=os.path.join(dest, 'source_a_link'))
    assert output == expected_output


def test_cli_dry_run_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = ['--dry-run', 'stow', source_only_files, dest]
    dploy.cli.run(args)
    with pytest.raises(FileNotFoundError):
        os.readlink(os.path.join(dest, 'aaa'))
    out, _ = capsys.readouterr()
    d = os.path.join(dest, 'aaa')
    s = os.path.join(source_only_files, 'aaa')
    assert out == "dploy stow: link {dest} => {source}\n".format(source=s, dest=d)


def test_cli_quiet_with_stow_with_simple_senario(source_only_files, dest, capsys):
    args = ['--quiet', 'stow', source_only_files, dest]
    dploy.cli.run(args)
    assert os.readlink(os.path.join(dest, 'aaa')) == os.path.join('..', 'source_only_files', 'aaa')
    out, _ = capsys.readouterr()
    assert out == ""


def test_cli_version_printing(capsys):
    args = ['--version']
    with pytest.raises(SystemExit):
        dploy.cli.run(args)
        out, _ = capsys.readouterr()
        assert re.match(r"dploy \d+.\d+\.\d+(-\w+)?\n", out) != None
