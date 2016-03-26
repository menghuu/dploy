#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse

import dploy

PARSER = argparse.ArgumentParser(description='dploy dotfiles')
SUB_PARSERS = PARSER.add_subparsers(dest="subparser_name")

STOW_PARSER = SUB_PARSERS.add_parser('stow')
STOW_PARSER.add_argument('source',
                         nargs='+',
                         help='source directory to stow')
STOW_PARSER.add_argument('dest',
                         help='destination path to stow into')
ARGS = PARSER.parse_args()

if ARGS.subparser_name == 'stow':
    for source in ARGS.source:
        dploy.stow(source, ARGS.dest)
