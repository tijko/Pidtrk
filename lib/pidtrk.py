#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sqlite3
import os


class ProcessTrack(object):

    def process_check(self):
        self.create_db()
        db_list = self.create_db_list()
        tagged_ps = list() 
        try:
            os.remove(os.environ['HOME'] + '/.pidtrk.txt')
        except OSError:
            pass 
        while True:
            time.sleep(5)
            ps = [i for i in os.listdir('/proc') if i.isdigit()]
            for i in ps:
                if os.path.isfile('/proc/%s/comm' % i):
                    try:
                        with open('/proc/%s/comm' % i) as f:
                            ps_name = f.read().strip('\n')
                        if ps_name not in tagged_ps:
                            tagged_ps.append(ps_name)
                            with open(os.environ['HOME'] + '/.pidtrk.txt', 'a+') as f:
                                f.write(ps_name + ': ' + time.ctime() + '\n')
                        if ps_name not in db_list:
                            self.enter_process(ps_name)
                            db_list.append(ps_name)
                    except AttributeError or IOError:
                        pass

    def create_db(self):
        con = sqlite3.connect(os.environ['HOME'] + '/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Process(pidname TEXT, time TEXT)")
        con.commit()
        con.close()
 
    def create_db_list(self):
        con = sqlite3.connect(os.environ['HOME'] + '/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Process")
            prclst = [i[0] for i in cur.fetchall()]
        con.commit()
        con.close()
        return prclst

    def enter_process(self, process):
        con = sqlite3.connect(os.environ['HOME'] + '/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Process VALUES(?,?)", (process, time.ctime()))
        con.commit()
        con.close()
