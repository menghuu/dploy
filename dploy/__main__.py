#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import sys
import argparse
import dploy
import dploy.version

def main():
    """
    todo
    """

    parser = argparse.ArgumentParser(prog='dploy')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {version}'.format(version=dploy.version.__version__))

    sub_parsers = parser.add_subparsers(dest="sub_command")

    stow_parser = sub_parsers.add_parser('stow')
    stow_parser.add_argument('source',
                             nargs='+',
                             help='source directory to stow')
    stow_parser.add_argument('dest',
                             help='destination path to stow into')

    stow_parser = sub_parsers.add_parser('unstow')
    stow_parser.add_argument('source',
                             nargs='+',
                             help='source directory to unstow from')
    stow_parser.add_argument('dest',
                             help='destination path to unstow')

    link_parser = sub_parsers.add_parser('link')
    link_parser.add_argument('source',
                             help='source file or directory to link')
    link_parser.add_argument('dest',
                             help='destination path to link')

    args = parser.parse_args()

    if args.sub_command != None:
        if args.sub_command == 'stow':
            try:
                dploy.stow(args.source, args.dest)
            except (ValueError, PermissionError) as error:
                print(error, file=sys.stderr)
                sys.exit(1)


        elif args.sub_command == 'unstow':
            try:
                dploy.unstow(args.source, args.dest)
            except (ValueError, PermissionError) as error:
                print(error, file=sys.stderr)
                sys.exit(1)

        elif args.sub_command == 'link':
            try:
                dploy.link(args.source, args.dest)
            except (ValueError, PermissionError) as error:
                print(error, file=sys.stderr)
                sys.exit(1)

        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
