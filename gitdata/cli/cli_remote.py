"""
usage: gitdata remote
       gitdata remote add <name> <location>
       gitdata remote rm <name>

options:
    -v, --verbose         verbose output
"""

from docopt import docopt

import gitdata.repositories


def remote():
    arguments = docopt(__doc__)

    if arguments['add']:
        name = arguments['<name>']
        location = arguments['<location>']
        with gitdata.Repository() as repository:
            repository.remotes().add(name, location)

    elif arguments['rm']:
        name = arguments['<name>']
        with gitdata.Repository() as repository:
            repository.remotes().remove(name)

    else:
        with gitdata.Repository() as repository:
            print(repository.remotes())


if __name__ == '__main__':
    print(docopt(__doc__))

