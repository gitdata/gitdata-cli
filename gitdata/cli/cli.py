"""
usage: gitdata [-V | --version] [-v | --verbose] [-d | --debug] [--help] <command> [<args>...]

The most commonly used gitdata commands are:
   init       Create an empty GitData repository in a new directory
   fetch      Fetch data
   explore    Explore data
   clear      Clear local data
   dump       Print the graph to stdout
   remote     Manage set of remote locations
   show       Show an entity
   status     Show the data repository status
   help       Show help

See 'gitdata help <command>' for more information on a specific command.

"""

import logging
import os
import sys

import docopt

import gitdata
import gitdata.cli
import gitdata.repositories
from gitdata.utils import trim


def print_help(doc):
    """Print help text"""
    print(trim(doc))


def main():

    args = docopt.docopt(__doc__,
                         version='gitdata version {}'.format(gitdata.__version__),
                         options_first=True)

    logger = logging.getLogger(__name__)

    verbose = False
    if '<args>' in args:
        if '-v' in args['<args>']:
            verbose = True

    if args['-d']:
        fmt = (
            '%(asctime)s %(levelname)-8s %(name)-30s '
            '%(lineno)-4s %(message)s'
        )
        console_formatter = logging.Formatter(fmt)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        logger.debug('debugging is on')
    else:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)

    if args['<command>'] == 'help':
        topic = next(iter(args['<args>']), None)

        if topic == 'init':
            print(gitdata.repositories.INIT_HELP)
        elif topic == 'remote':
            print(gitdata.cli.cli_remote.__doc__)
        elif topic == 'status':
            print(gitdata.repositories.STATUS_HELP)
        elif topic == 'show':
            print(gitdata.repositories.SHOW_HELP)
        elif topic == 'fetch':
            print_help(gitdata.repositories.FETCH_HELP)
        elif topic == 'explore':
            print_help(gitdata.repositories.EXPLORE_HELP)
        elif topic:
            exit("%r is not a gitdata command. See 'gitdata help'." % topic)
        else:
            exit(__doc__)

    elif args['<command>'] == 'init':
        repository = gitdata.repositories.Repository(os.getcwd())
        repository.initialize()

    elif args['<command>'] == 'remote':
        gitdata.cli.remote()

    elif args['<command>'] == 'fetch':
        for location in args['<args>']:
            gitdata.fetch(location)

    elif args['<command>'] == 'explore':
        for location in args['<args>']:
            gitdata.explore(location)

    elif args['<command>'] == 'clear':
        with gitdata.repositories.Repository(os.getcwd()) as repository:
            repository.clear(args)

    elif args['<command>'] == 'dump':
        with gitdata.repositories.Repository(os.getcwd()) as repository:
            repository.dump()

    elif args['<command>'] == 'show':
        with gitdata.repositories.Repository(os.getcwd()) as repository:
            repository.show(args['<args>'])

    elif args['<command>'] == 'status':
        with gitdata.repositories.Repository(os.getcwd()) as repository:
            print(repository.status(verbose=verbose))

    else:
        exit("%r is not a gitdata command. See 'gitdata --help'." % args['<command>'])


if __name__ == '__main__':
    main()

