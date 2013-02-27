
import time
import sqlite3
import os


class ProcessTrack(object):

    def process_check(self):
        self.create_db()
        db_list = self.create_db_list()
        tagged = []
        try:
            os.remove('/home/haumea/.data.txt')
        except OSError:
            pass 
        while True:
            time.sleep(5)
            ps = [int(i) for i in os.listdir('/proc') if i.isdigit()]
            for i in ps:
                if os.path.isfile('/proc/%s/stat' % i):
                    try:
                        with open('/proc/%s/stat' % i, 'r+') as f:
                            name = f.readline()
                        f.close()
                        name = [j for j in name.split(' ') if '(' in j]
                        if name[0][1:-1] not in tagged:
                            tagged.append(name[0][1:-1])
                            with open('/home/haumea/.data.txt', 'a+') as f:
                                f.write(name[0][1:-1] + ': ' + time.ctime() + '\n')
                            f.close()
                        if name[0][1:-1] not in db_list:
                            self.enter_process(name[0][1:-1])
                            db_list.append(name[0][1:-1])
                    except AttributeError or IOError:
                        pass

    def create_db(self):
        con = sqlite3.connect('/home/haumea/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Process(pidname TEXT, time TEXT)")
 
    def create_db_list(self):
        con = sqlite3.connect('/home/haumea/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Process")
            prclst = [i[0] for i in cur.fetchall()]
        return prclst

    def enter_process(self, process):
        con = sqlite3.connect('/home/haumea/.pidtrk.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO Process VALUES(?,?)", (process, time.ctime()))

