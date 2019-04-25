"""
    gitdata cli
"""

import os
import argparse
import logging

import gitdata
import gitdata.repositories


def init(args):
    """init command"""
    gitdata.repositories.initialize(os.getcwd())


def status(args):
    """init command"""
    gitdata.repositories.status(os.getcwd())


def main():
    """Main program

    called by gidata/bin/cdw
    """
    # pylint: disable=line-too-long

    parser = argparse.ArgumentParser()
    help = lambda a: parser.print_help()
    parser.add_argument(
        '-V', '--version', dest='func', action='store_const',
        const=gitdata.__version__, default=help
    )
    subparsers = parser.add_subparsers()

    # create a data repository
    new_parser = subparsers.add_parser('init')
    new_parser.add_argument('-v', '--verbose', action='store_true', help='verbose console output')
    new_parser.set_defaults(func=init)

    # show repository status
    new_parser = subparsers.add_parser('status')
    new_parser.set_defaults(func=status)

    # run
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()