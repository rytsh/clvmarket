#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:53:27 +03 2019.

@author: Eray Ates, Sibel Gürbüz
"""
import sys
import signal
import json
import sqlalchemy as db

def signal_handler(signal, frame):
    """Catch SIGNINT."""
    print('Exited From Application')
    sys.exit(1)

def jsonread(filename):
    """Read Json file."""
    with open(filename, 'r') as myfile:
        data=myfile.read()
    
    return json.loads(data)

class MySQL(object):
    """MySQL connection object."""

    def __init__(self, username, password, host, port, dbname):
        """Init database engine and connection."""
        self.engine = db.create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
            username, password, host, port, dbname
        ), pool_recycle=3600)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
    
    def getTable(self,tablename):
        """Get table of the db."""
        return db.Table(tablename, self.metadata, autoload=True, autoload_with=self.engine)
    
    def clearData(self, tablename=None):
        """Clear table datas."""
        if tablename:
            print('Clear table {}'.format(tablename))
            table_tmp = self.getTable(tablename)
            self.connection.execute(table_tmp.delete())
        else:
            self.connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
            for table in self.engine.table_names():
                print('Clear table {}'.format(table))
                table_tmp = self.getTable(table)
                self.connection.execute(table_tmp.delete())
            
            self.connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
