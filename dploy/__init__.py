"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 3), "Requires Python 3.3 or Greater"
import dploy._stow
import dploy._link


def stow(sources, dest):
    """
    sub command stow
    """

    dploy._stow.Stow(sources, dest) # pylint: disable=protected-access


def unstow(sources, dest):
    """
    sub command unstow
    """

    dploy._stow.UnStow(sources, dest) # pylint: disable=protected-access


def link(source, dest):
    """
    sub command link
    """
    dploy._stow.Link(source, dest) # pylint: disable=protected-access
