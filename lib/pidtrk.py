#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3
import os


class ProcessTrack(object):

    PIDFILE = os.environ['HOME'] + '/.pidtrk.txt'
    PIDB = os.environ['HOME'] + '/.pidtrk.db'

    def process_poll(self):
        self.create_db
        self.db_list = self.create_db_list
        pids = set()
        if os.path.isfile(self.PIDFILE): 
            os.remove(self.PIDFILE)
        while True:
            time.sleep(5)
            self.new_pids = {i for i in os.listdir('/proc') 
                             if i.isdigit() and i not in pids}
            if self.new_pids:
                self.file_log_process
                pids.update(self.new_pids)

    @property
    def file_log_process(self):
        for pid in self.new_pids:
            if os.path.isfile('/proc/%s/comm' % pid):
                with open('/proc/%s/comm' % pid) as f:
                    self.process = f.read().strip('\n')
                with open(self.PIDFILE, 'a+') as f:
                    f.write(self.process + ': ' + time.ctime() + '\n')
                self.db_log_process

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
