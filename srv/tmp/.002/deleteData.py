#!/usr/bin/env python

import MySQLdb
from datetime import datetime, timedelta
from time import sleep

conn = MySQLdb.connect(host= "localhost",
    user="root", passwd="root", db="TECNOQ")
x = conn.cursor()

nowTime = datetime.today()
todayTime = nowTime.replace(hour=0, minute=0, second=0, microsecond=0)
weekAgoTime = todayTime - timedelta(days=7)
weekAgoStr = str(weekAgoTime)

# SELECT table_schema, sum((data_length+index_length)/1024/1024) AS MB from information_schema.tables group by 1
for index in range(3):
    
    # DEC_INPUT_TB
    x.execute("DELETE FROM DEC_INPUT_TB where RTIME < '%s'" % (weekAgoStr))
    conn.commit()

    # HEX_INPUT_TB
    x.execute("DELETE FROM HEX_INPUT_TB where RTIME < '%s'" % (weekAgoStr))
    conn.commit()

    # OSIRE_STATUS
    x.execute("DELETE FROM OSIRE_STATUS where Unix < '%s'" % (weekAgoStr))
    conn.commit()

    # SLOW_UPLOADS
    x.execute("DELETE FROM SLOW_UPLOADS where TIMESTAMP < '%s'" % (weekAgoStr))
    conn.commit()

    # STATISTIC_TB
    x.execute("DELETE FROM STATISTIC_TB where TIME < '%s'" % (weekAgoStr))
    conn.commit()

    # UPL_INPUT_TB
    x.execute("DELETE FROM UPL_INPUT_TB where UTIME < '%s'" % (weekAgoStr))
    conn.commit()

    sleep(1)
