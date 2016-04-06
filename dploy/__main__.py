#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse
import dploy.version

def main():
    PARSER = argparse.ArgumentParser(prog='dploy')
    PARSER.add_argument('--version',
                action='version',
                version='%(prog)s {version}'.format(version=dploy.version.__version__))

    SUB_PARSERS = PARSER.add_subparsers(dest="sub_command")

    STOW_PARSER = SUB_PARSERS.add_parser('stow')
    STOW_PARSER.add_argument('source',
                 nargs='+',
                 help='source directory to stow')
    STOW_PARSER.add_argument('dest',
                 help='destination path to stow into')

    LINK_PARSER = SUB_PARSERS.add_parser('link')
    LINK_PARSER.add_argument('source',
                 help='source files or directories to link')
    LINK_PARSER.add_argument('dest',
                 help='destination path to link')

    ARGS = PARSER.parse_args()

    if ARGS.sub_command != None:
        if ARGS.sub_command == 'stow':
            for source in ARGS.source:
                dploy.stow(source, ARGS.dest)
        elif ARGS.sub_command == 'link':
            dploy.link(ARGS.source, ARGS.dest)
    else:
        PARSER.print_help()
