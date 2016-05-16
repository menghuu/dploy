#!/usr/bin/env python3

"""
The entry point when dploy is called as a module
"""

import dploy.cli

def main():
    """
    main entry point when using dploy from the command line
    """
    dploy.cli.run()

if __name__ == '__main__':
    main()
