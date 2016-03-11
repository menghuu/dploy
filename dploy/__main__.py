#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse

import dploy
from dploy.util import dynamic_import

PARSER = argparse.ArgumentParser(description='dploy dotfiles')
PARSER.add_argument("--file",
                    default="~/dotfiles/setup_config.py",
                    help="path of the dploy file")

ARGS = PARSER.parse_args()

SETUP_CONFIG = dynamic_import(ARGS.file, "")


def main():
    """
    Main entry function
    """

    dploy.backup(SETUP_CONFIG.DOTFILES,
                 SETUP_CONFIG.DOTFILES_DIRECTORY)
    print("\n")

    dploy.symlink_files(SETUP_CONFIG.DOTFILES,
                        SETUP_CONFIG.DOTFILES_DIRECTORY)
    print("\n")

    dploy.create_files(SETUP_CONFIG.FILES)
    print("\n")

    dploy.create_directories(SETUP_CONFIG.DIRECTORIES)
    print("\n")

if __name__ == "__main__":
    main()
