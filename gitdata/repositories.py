"""
    gitdata repositories
"""

import logging
import os
import sqlite3
import sys

import gitdata.utils


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

def status(location):
    """Show the gitdata respository status"""
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
        print('fatal: not a gitdata repository')
        sys.exit(-1)