#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3
import os


class ProcessTrack(object):

    PIDFILE = os.environ['HOME'] + '/.pidtrk.txt'
    PIDB = os.environ['HOME'] + '/.pidtrk.db'

    def process_check(self):
        self.create_db
        db_list = self.create_db_list
        processes = set()
        if os.path.isfile(self.PIDFILE) 
            os.remove(self.PIDFILE)
        while True:
            time.sleep(5)
            new_proc = {i for i in os.listdir('/proc') 
                        if i.isdigit() and i not in processes}
            if new_proc:
                for proc in new_proc:
                    if os.path.isfile('/proc/%s/comm' % proc):
                    try:
                        with open('/proc/%s/comm' % proc) as f:
                            ps_name = f.read().strip('\n')
                            with open(self.PIDFILE, 'a+') as f:
                                f.write(ps_name + ': ' + time.ctime() + '\n')
                        if ps_name not in db_list:
                            self.enter_process(ps_name)
                            db_list.append(ps_name)
                    except AttributeError or IOError:
                        pass
                processes.update(new_proc)
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

    def enter_process(self, process):
        con = sqlite3.connect(self.PIDB)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Process VALUES(?,?)", (process, time.ctime()))
        return
