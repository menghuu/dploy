#!/usr/bin/env python3

"""
The main entry point to the dploy script
"""

import argparse

import dploy

PARSER = argparse.ArgumentParser(description='dploy dotfiles')
PARSER.add_argument('target',
                    help='target or source of the files to dploy')
PARSER.add_argument('dest',
                    help='dest path to dploy file')
ARGS = PARSER.parse_args()

dploy.dploy(ARGS.target, ARGS.dest)
