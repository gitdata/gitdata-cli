"""
    gitdata repositories
"""

import logging
import os
import sqlite3
import sys

import gitdata.utils

INIT_HELP = """
Initializes a gitdata repository in the current directory.

usage: gitdata init
"""

STATUS_HELP = """
Returns the status of the current gitdata repository.

usage: gitdata status [-v | --verbose]

options:
    -v, --verbose   verbose output
"""

def initialize(location):
    """Initialize a gitdata repository in a location on the disk"""
    logger = logging.getLogger(__name__)
    logger.debug('initializing')
    pathname = os.path.join(location, '.gitdata')
    if not os.path.exists(pathname):
        connection = sqlite3.Connection(pathname)
        setup_repository(connection)
        print('Initialized empty GitData repository in', pathname)
    else:
        print('GitData respository already initialized in', pathname)


def setup_repository(connection):
    """Setup the sqlite3 repsoitory database"""
    filename = gitdata.utils.lib_path('sql/create_respository_sqlite3.sql')
    sql = gitdata.utils.load(filename)
    commands = list(filter(bool, sql.split(';\n')))
    cursor = connection.cursor()
    try:
        for command in commands:
            cursor.execute(command)
    finally:
        cursor.close()

def status(location, verbose=False):
    """Show the GitData respository status"""
    pathname = os.path.join(location, '.gitdata')
    if os.path.exists(pathname):
        connection = sqlite3.Connection(pathname)
        cursor = connection.cursor()
        try:
            cursor.execute('select count(*) from facts')
            count = list(cursor.fetchall())[0][0]
            print('{:,} facts'.format(count))
        finally:
            cursor.close()
    else:
        print('fatal: not a GitData repository')
        if verbose:
            print('pathname is %r' % pathname)
        sys.exit(-1)

class RepositoryRemotes(object):

    def __init__(self, repository):
        self.repository = repository

    def index(self):
        """Return a list of remotes"""
        db = self.repository.connection.cursor()
        try:
            db.execute('select name, location from remotes order by name')
            result = db.fetchall()
            return result
        finally:
            db.close()

    def add(self, name, location):
        """Add a remote"""
        db = self.repository.connection.cursor()
        try:
            cmd = 'insert into remotes (name, location) values (?, ?)'
            db.execute(cmd, (name, location))
            db.execute('select * from remotes')
            # print(db.fetchall())
            self.repository.connection.commit()
            # print(result.__dict__)
        finally:
            db.close()

    def __str__(self):
        remotes = self.index()
        if remotes:
            maxlen = max(len(name) for name,_ in remotes)
            return '\n'.join(
                '{:{width}}  {}'.format(width=maxlen, *remote)
                for remote in remotes
            )
        else:
            return 'no remotes'


class Repository(object):
    """GitData Repository"""

    def __init__(self, location=None):
        location = location if location is not None else os.getcwd()
        pathname = os.path.join(location, '.gitdata')
        self.connection = None
        self.cursor = None
        if os.path.exists(pathname):
            self.connection = sqlite3.Connection(pathname)
        else:
            msg = 'fatal: not a GitData repository'
            logger = logging.getLogger(__name__)
            logger.error(msg)
            logger.debug('pathname is %r', pathname)
            raise Exception(msg)

    def open(self):
        """Open the repository"""
        self.cursor = self.connection.cursor()
        return self.cursor

    def close(self):
        """Close the repository"""
        self.cursor.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        if value:
            raise value

    def status(self, verbose=False):
        """Return the repository status"""
        self.cursor.execute('select count(*) from facts')
        fact_count = list(self.cursor.fetchall())[0][0]
        self.cursor.execute('select count(*) from remotes')
        remote_count = list(self.cursor.fetchall())[0][0]
        return '{:,} facts\n{:,} remotes'.format(fact_count, remote_count)

    def remotes(self):
        """Add a remote data source to the repository"""
        return RepositoryRemotes(self)

