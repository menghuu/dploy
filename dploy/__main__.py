#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse

import dploy
from dploy.util import dynamic_import

PARSER = argparse.ArgumentParser(description='dploy dotfiles')
PARSER.add_argument('target',
                    help='target or source of the files to dploy')
PARSER.add_argument('dest',
                    nargs='+',
                    help='dest path to dploy file')

ARGS = PARSER.parse_args()

def main():
    """
    Main entry function
    """

    for dest in ARGS.dest:
        dploy.deploy_files(ARGS.target, dest)

if __name__ == "__main__":
    main()
