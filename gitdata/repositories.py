"""
    gitdata repositories
"""

import datetime as dt
import logging
import os
import sqlite3
import sys

import gitdata.utils
import gitdata.connectors.console


logger = logging.getLogger(__name__)


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

FETCH_HELP = """
Fetches data from a specified location.  A location can be a URL, a
local file or a predefined gitdata repository remote.

usage:
    gitdata fetch <location>

"""

EXPLORE_HELP = """
Explore data visually.
"""

SHOW_HELP = """
Show facts related to entities identified by uid values provided as arugments.

usage:
    gitdata show [-v | --verbose] [<args>...]

options:
    -v, --verbose   verbose output
"""

def setup_repository(connection):
    """Setup the sqlite3 repsoitory database"""
    filename = gitdata.utils.lib_path('sql/create_repository_sqlite3.sql')
    sql = gitdata.utils.load(filename)
    commands = list(filter(bool, sql.split(';\n')))
    cursor = connection.cursor()
    try:
        for command in commands:
            cursor.execute(command)
            # print('excecuting', command)
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


class Subject(dict):
    """Graph subject"""

    def show(self):
        """Show the subject"""
        return gitdata.utils.space(
            (name, repr(value))
            for name, value in self.items()
        )

    def __str__(self):
        return self.show()


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
        if os.path.exists(location):
            location = gitdata.utils.as_uri(location)
        db = self.repository.connection.cursor()
        try:
            cmd = 'insert into remotes (name, location) values (?, ?)'
            db.execute(cmd, (name, location))
            self.repository.connection.commit()
        except sqlite3.IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: remotes.name':
                print('remote exists')
                sys.exit(-1)
            else:
                raise
        finally:
            db.close()

    def remove(self, name):
        """Remove a remote"""
        if name not in [name for name,_ in self.index()]:
            print('fatal: no such remote: {}'.format(name))
            sys.exit(-1)
        db = self.repository.connection.cursor()
        try:
            cmd = 'delete from remotes where name = ?'
            db.execute(cmd, (name,))
            self.repository.connection.commit()
        finally:
            db.close()

    def get(self, name):
        db = self.repository.connection.cursor()
        try:
            db.execute('select location from remotes where name=?', (name,))
            result = db.fetchall()
            if result:
                return Subject(
                    name=name,
                    location=result[0][0]
                )
        finally:
            db.close()

    def __str__(self):
        remotes = self.index()
        if remotes:
            return gitdata.utils.space(remotes)
        else:
            return 'no remotes'


class Repository(object):
    """GitData Repository"""

    def __init__(self, location=None):
        self.connection = None
        self.location = location or os.getcwd()
        self.store = None
        self.graph = None

    def open(self):
        """Open the repository"""
        location = self.location
        if location == ':memory:':
            self.connection = sqlite3.Connection(location)
            setup_repository(self.connection)
            self.store = gitdata.stores.sqlite3.Sqlite3Store(location)
            self.store.setup()
        else:
            location = location if location is not None else os.getcwd()
            pathname = os.path.join(location, '.gitdata')
            if os.path.exists(pathname):
                self.connection = sqlite3.Connection(pathname)
            else:
                msg = 'fatal: not a GitData repository'
                logger.error(msg)
                logger.debug('pathname is %r', pathname)
                raise Exception(msg)
            self.store = gitdata.stores.sqlite3.Sqlite3Store(pathname)
        self.graph = gitdata.Graph(self.store)

    def initialize(self):
        """Initialize a repository"""
        location = self.location
        if location != ':memory:':
            logger.debug('initializing')
            pathname = os.path.join(location, '.gitdata')
            if not os.path.exists(pathname):
                connection = sqlite3.Connection(pathname)
                setup_repository(connection)
                print('Initialized empty GitData repository in', pathname)
            else:
                print('GitData respository already initialized in', pathname)

    def close(self):
        """Close the repository"""
        # self.cursor.close()

    def get(self, name):
        remote = self.remotes().get(name)
        if remote:
            return remote

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, _, value, traceback):
        self.close()
        if value:
            raise value

    def show(self, args):
        """Show objects"""
        if args:
            for name in args:
                subject = self.get(name)
                if subject:
                    print(subject)
        else:
            remotes = [name for name,_ in self.remotes().index()]
            print('\n'.join(remotes))

    def fetch(self, location):
        """Fetch from location

        Adds a location from which to fetch facts.  Fetching is a
        lazy operation so the facts are downloaded only when they are
        needed.
        """
        logger.debug('fetching location %r', location)
        if not self.graph.exists(kind='local', location=location):
            logger.debug('adding new location %r', location)
            now = dt.datetime.now()
            self.graph.add(
                dict(
                    kind='local',
                    location=location,
                    created=now,
                    updated=now,
                )
            )

    def explore(self, location, destination):
        """Explore a location"""
        self.fetch(location)
        gitdata.connectors.explore(location, destination)

    def clear(self, args):
        if '--all' in args['<args>']:
            self.graph.store.clear()
        else:
            for local in self.graph.find(kind='fetched'):
                local.delete()

    def dump(self):
        print(self.graph)

    def status(self, verbose=False):
        """Return the repository status"""
        local_count = len(self.graph.find(kind='local'))
        cursor = self.store.connection.cursor()
        try:
            cursor.execute('select count(*) from facts')
            fact_count = list(cursor.fetchall())[0][0]
            cursor.execute('select count(*) from remotes')
            remote_count = list(cursor.fetchall())[0][0]
        finally:
            cursor.close()
        return '{:,} local\n{:,} facts\n{:,} remotes'.format(
            local_count,
            fact_count,
            remote_count
        )

    def remotes(self):
        """Add a remote data source to the repository"""
        return RepositoryRemotes(self)

