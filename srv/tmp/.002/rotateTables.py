#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import time

dbuser = "root"
dbpass = "root"
dbdb = "TECNOQ"
dbtbhex = "HEX_INPUT_TB"
dbtbdec = "DEC_INPUT_TB"
dbtbupl = "UPL_INPUT_TB"
dbtbslo = "SLOW_UPLOADS"
dbtbsta = "STATISTIC_TB"
osdate = time.strftime("%d%m%Y")

try:
  con = mdb.connect('localhost', dbuser, dbpass, dbdb);
  cur = con.cursor()

#====================== START HEX =========================================#
  renameTableHex = '''RENAME TABLE %s TO %s_%s''' % (dbtbhex,dbtbhex,osdate)

  cur.execute(renameTableHex)
  con.commit()

  createTableHex = '''CREATE TABLE %s (
                      ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                      HEXSTR VARCHAR(300) NOT NULL,
                      RTIME TIMESTAMP,
                      CONVERTED VARCHAR(5) DEFAULT 'n'
                      )''' % (dbtbhex)

  cur.execute(createTableHex)
  con.commit()
#====================== END HEX ===========================================#

#====================== START DEC =========================================#
  renameTableDec = '''RENAME TABLE %s TO %s_%s''' % (dbtbdec,dbtbdec,osdate)

  cur.execute(renameTableDec)
  con.commit()

  createTableDec = '''CREATE TABLE %s (
                      ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                      CID VARCHAR(10) NOT NULL,
                      A1 INT(10) ,
                      A2 INT(10) ,
                      A3 INT(10) ,
                      A4 INT(10) ,
                      A5 INT(10) ,
                      A6 INT(10) ,
                      B7 INT(10) ,
                      B8 INT(10) ,
                      B9 INT(10) ,
                      B10 INT(10) ,
                      B11 INT(10) ,
                      B12 INT(10) ,
                      C13 INT(10) ,
                      C14 INT(10) ,
                      C15 INT(10) ,
                      C16 INT(10) ,
                      C17 INT(10) ,
                      C18 INT(10) ,
                      C19 INT(10) ,
                      C20 INT(10) ,
                      C21 INT(10) ,
                      C22 INT(10) ,
                      D23 INT(10) ,
                      D24 INT(10) ,
                      D25 INT(10) ,
                      D26 INT(10) ,
                      D27 INT(10) ,
                      D28 INT(10) ,
                      D29 INT(10) ,
                      BAT INT(10) ,
                      RC VARCHAR(10),
                      TS INT(20),
                      RTIME VARCHAR(50) NOT NULL,
                      CTIME TIMESTAMP,
                      SND VARCHAR(5) DEFAULT 'n'
                      )''' % (dbtbdec)

  cur.execute(createTableDec)
  con.commit()
#====================== END DEC ===========================================#

#====================== START UPL =========================================#
  renameTableUpl = '''RENAME TABLE %s TO %s_%s''' % (dbtbupl,dbtbupl,osdate)

  cur.execute(renameTableUpl)
  con.commit()

  createTableHex = '''CREATE TABLE %s (
                      ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                      CID VARCHAR(30) NOT NULL,
                      DATA VARCHAR(200) NOT NULL,
                      UTIME VARCHAR(50),
                      UPLOADED VARCHAR(5) DEFAULT 'n'
                      )''' % (dbtbupl)

  cur.execute(createTableHex)
  con.commit()
#====================== END UPL ===========================================#

#====================== START STA =========================================#
#  renameTableSta = '''RENAME TABLE %s TO %s_%s''' % (dbtbsta,dbtbsta,osdate)

#  cur.execute(renameTableSta)
#  con.commit()

#  createTableSta = '''CREATE TABLE %s (
#                      ID INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#                      INFO VARCHAR(30) NOT NULL,
#                      TIME TIMESTAMP,
#                      )''' % (dbtbsta)

#  cur.execute(createTableSta)
#  con.commit()


#====================== END STA ===========================================#

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:
    if con:
        con.close()

