"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 3), "Requires Python 3.3 or Greater"
import dploy.main as main


def stow(sources, dest):
    """
    sub command stow
    """

    main.Stow(sources, dest) # pylint: disable=protected-access


def unstow(sources, dest):
    """
    sub command unstow
    """

    main.UnStow(sources, dest) # pylint: disable=protected-access


def link(source, dest):
    """
    sub command link
    """
    main.Link(source, dest) # pylint: disable=protected-access
