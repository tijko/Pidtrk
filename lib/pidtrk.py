#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3
import logging
import os


class ProcessTrack(object):

    PIDB = os.environ['HOME'] + '/.pidtrk.db'
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    def __init__(self):
        self.logger = logging.getLogger('Pidtrk')
        self.logger.setLevel(logging.DEBUG)  
        self.handler = logging.FileHandler('.pidtrk.log', 'w')
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(self.FORMAT)
        self.handler.setFormatter(self.formatter) 
        self.logger.addHandler(self.handler)
        self.logger.info('Process Track')
                                            
    def process_poll(self):
        self.create_db
        self.db_list = self.create_db_list
        pids = set()
        while True:
            time.sleep(5)
            self.new_pids = {i for i in os.listdir('/proc') 
                             if i.isdigit() and i not in pids}
            print self.new_pids
            if self.new_pids:
                self.logger.debug('Process Spawned')
                self.file_log_process
                pids.update(self.new_pids)
            for pid in pids:
                try:
                    with open('/proc/%s/io' % pid) as f:
                        io = f.read()
                    io = {k:v for k,v in [i.split(': ') for i in io.split('\n') if i]}
                    if io['read_bytes'] / 65336 > 1000:
                        self.logger.warning('Process %s', pid, 'High disk read')
                    if io['write_bytes'] / 65336 > 1000:
                        self.logger.warning('Process %s', pid, 'High disk write')
                except OSError:
                    pass
    @property
    def file_log_process(self):
        for pid in self.new_pids:
            if os.path.isfile('/proc/%s/comm' % pid):
                with open('/proc/%s/comm' % pid) as f:
                    self.process = f.read().strip('\n')
                self.logger.info('Process: %s', self.process)
                self.db_log_process
            else:
                self.logger.warning('Process: %d', pid, 'dropped process')

    @property
    def db_log_process(self):
        if self.process not in self.db_list:
            self.enter_process(self.process)
            self.db_list.append(self.process)

    @property
    def create_db(self):
        con = sqlite3.connect(self.PIDB)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Process(pidname TEXT, time TEXT)")
        return

    @property 
    def create_db_list(self):
        con = sqlite3.connect(self.PIDB)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Process")
            prclst = [i[0] for i in cur.fetchall()]
        return prclst

    @property
    def enter_process(self):
        con = sqlite3.connect(self.PIDB)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Process VALUES(?,?)", 
                        (self.process, time.ctime()))
        return
