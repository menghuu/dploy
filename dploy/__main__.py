#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse

import dploy

PARSER = argparse.ArgumentParser(description='dploy dotfiles')
PARSER.add_argument('source',
                    nargs='+',
                    help='source files or directories to dploy')
PARSER.add_argument('dest',
                    help='destination path to dploy source to')
ARGS = PARSER.parse_args()

for source in ARGS.source:
    dploy.stow(source, ARGS.dest)
