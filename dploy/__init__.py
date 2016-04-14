"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""


import sys
assert sys.version_info >= (3, 3), "Requires Python 3.3 or Greater"
import dploy._stow
import dploy._link


def stow(source, dest):
    """
    sub command stow
    """

    dploy._stow.Stow(source, dest)


def unstow(source, dest):
    """
    sub command unstow
    """

    dploy._stow.UnStow(source, dest)


def link(source, dest):
    """
    sub command link
    """
    dploy._link.link(source, dest)
