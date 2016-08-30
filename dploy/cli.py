"""
The command line interface
"""

import sys
import argparse
import dploy.main
import dploy.version


def create_parser():
    """
    create the CLI argument parser
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
    return parser


def run(arguments=None):
    """
    interpret the parser arguments and execute the corresponding commands
    """
    parser = create_parser()

    if arguments is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(arguments)


    if args.sub_command == 'stow':
        try:
            dploy.main.Stow(args.source, args.dest, is_silent=False)
        except (ValueError, PermissionError) as error:
            print(error, file=sys.stderr)
            sys.exit(1)


    elif args.sub_command == 'unstow':
        try:
            dploy.main.UnStow(args.source, args.dest, is_silent=False)
        except (ValueError, PermissionError) as error:
            print(error, file=sys.stderr)
            sys.exit(1)

    elif args.sub_command == 'link':
        try:
            dploy.main.Link(args.source, args.dest, is_silent=False)
        except (ValueError, PermissionError) as error:
            print(error, file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
