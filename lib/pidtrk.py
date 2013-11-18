#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3
import logging
import os

from threading import Thread, Lock


class ProcessLogger(object):

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
        self.create_db
        self.db_list = self.create_db_list
        self.pids = dict()
        self.high_io = dict()
        self.high_thread = dict()
        lock = Lock()
        io = IOTrack(self, lock)
        pt = ProcessTrack(self, lock)
        tt = ThreadTrack(self, lock)
        io.start()
        pt.start()
        tt.start()
                                            
    def file_log_process(self, new_pids):
        for pid in new_pids:
            if os.path.isfile('/proc/%s/comm' % pid):
                with open('/proc/%s/comm' % pid) as f:
                    self.process = f.read().strip('\n')
                self.pids[self.process] = pid
                self.logger.debug('Process Spawned %s', pid)
                self.logger.info('Process: %s', self.process)
                self.db_log_process
            else:
                self.logger.warning('Process: %d', pid, 'dropped process')
        return

    @property
    def db_log_process(self):
        if self.process not in self.db_list:
            self.enter_process
            self.db_list.append(self.process)
        return

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

class IOTrack(Thread):

    def __init__(self, proc, lock):
        self.proc = proc
        self.lock = lock
        super(IOTrack, self).__init__()

    def run(self):
        while True:
            time.sleep(30)
            self.lock.acquire()            
            for pid in self.proc.pids:
                if pid not in self.proc.high_io:
                    with open('/proc/%s/io' % self.proc.pids[pid]) as f:
                        io = f.read()
                    io = {k:int(v) for k,v in [i.split(': ') 
                          for i in io.split('\n') if i]}
                    if io['read_bytes'] / 65336 > 1000:
                        self.proc.logger.warning('Process %s High disk read', 
                                                  self.proc.pids[pid])
                    if io['write_bytes'] / 65336 > 1000:
                        self.proc.logger.warning('Process %s High disk write', 
                                                  self.proc.pids[pid])
                    self.proc.high_io[pid] = self.proc.pids[pid]
            self.lock.release()
        return

class ProcessTrack(Thread):
    
    def __init__(self, proc, lock):
        self.proc = proc
        self.lock = lock
        super(ProcessTrack, self).__init__()

    def run(self): 
        while True:
            time.sleep(5)
            self.lock.acquire()
            self.new_pids = {i for i in os.listdir('/proc') 
                             if i.isdigit() and i not in 
                             self.proc.pids.values()}
            if self.new_pids:
                self.proc.file_log_process(self.new_pids)
            self.lock.release()
        return

class ThreadTrack(Thread):
    
    def __init__(self, proc, lock):
        self.proc = proc
        self.lock = lock
        super(ThreadTrack, self).__init__()

    def run(self):
        while True:
            time.sleep(15)
            self.lock.acquire()
            for pid in self.proc.pids:
                if pid not in self.proc.high_thread:
                    with open('/proc/%s/status' % self.proc.pids[pid]) as f:
                        status = f.read()
                    status = {k:v for k,v in [i.split(':\t') for 
                              i in status.split('\n') if i]}
                    if status['Threads'] > 10:
                        self.proc.logger.warning('Process %s High thread count', 
                                              pid)
                        self.proc.high_thread[pid] = self.proc.pids[pid]
        return
