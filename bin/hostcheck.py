#!/usr/bin/python -tt

from pysqlite2 import dbapi2 as sqlite3
from time      import time
import commands


class HostChecker:
    """class for host checking and storing data in db"""
    connection = 0;
    cursor     = 0;
    host_list  = 0;
    
    def __init__(self):
        # db connect
        self.connection = sqlite3.connect("/media/storage/projects/hostmon/dbase/hostcheck.sqlite")
        self.cursor = con.cursor()

        # get host list
        cur.execute("select * from hosts")
        host_list = cur.fetchall()

#hc = HostChecker()


# db connect
con = sqlite3.connect("/media/storage/projects/hostmon/dbase/hostcheck.sqlite")
cur = con.cursor()

# get host list
cur.execute("select * from hosts")
host_list = cur.fetchall()

#print "time %i" % time()
time_start = time()

# start of the check
cur.execute("insert into checks (time_start) values (%i)" % time())
checkid = cur.lastrowid
#print checkid

for row in host_list:
    print row[1]
    out = commands.getstatusoutput("ping -c 3 %s | grep \"min/avg/max\" | awk '{print $4}'" % row[1])
    if ( out[1].strip() != "" ) :
        out = out[1].split("/")
        if ( len(out) > 0 ) :
            print out
            cur.execute("insert into pings (id_host, id_check, time) values (%i, %i, %s)" % (row[0], checkid, out[1]))
    
time_end = time()
print time_end - time_start

cur.execute("update checks set time_end = %i where id = %i" % (time(), checkid))

con.commit()
cur.close()
