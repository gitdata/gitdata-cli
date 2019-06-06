"""
usage: gitdata [-V | --version] [-v | --verbose] [--help] <command> [<args>...]

The most commonly used gitdata commands are:
   init       Create an empty GitData repository in a new directory
   remote     Manage set of remote locations
   show       Show an entity
   status     Show the data repository status

See 'gitdata help <command>' for more information on a specific command.

"""

import docopt
import logging
import os
import sys

import gitdata
import gitdata.cli
import gitdata.repositories


def main():

    args = docopt.docopt(__doc__,
                         version='gitdata version {}'.format(gitdata.__version__),
                         options_first=True)

    verbose = False
    if '<args>' in args:
        if '-v' in args['<args>']:
            verbose = True

    if args['<command>'] == 'help':
        topic = next(iter(args['<args>']), None)

        if topic == 'init':
            print(gitdata.repositories.INIT_HELP)
        elif topic == 'remote':
            print(gitdata.cli.cli_remote.__doc__)
        elif topic == 'status':
            print(gitdata.repositories.STATUS_HELP)
        elif topic:
            exit("%r is not a gitdata command. See 'gitdata help'." % topic)
        else:
            exit(__doc__)

    elif args['<command>'] == 'init':
        gitdata.repositories.initialize(os.getcwd())

    elif args['<command>'] == 'remote':
        gitdata.cli.remote()

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

