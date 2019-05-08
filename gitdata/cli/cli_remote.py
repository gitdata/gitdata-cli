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
        repostitory = gitdata.repositories.Repository()
        repostitory.remotes().add(name, location)
    elif arguments['rm']:
        print('removing remote {}'.format(arguments['<name>']))
    else:
        repostitory = gitdata.repositories.Repository()
        print(repostitory.remotes())


if __name__ == '__main__':
    print(docopt(__doc__))

