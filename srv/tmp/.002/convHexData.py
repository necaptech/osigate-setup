#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import time

dbuser = "root"
dbpass = "root"
dbdb = "TECNOQ"
dbtbhex = "HEX_INPUT_TB"
dbtbdec = "DEC_INPUT_TB"
dbtbrel = "OSIRE_STATUS"
dbtbupl = "UPL_INPUT_TB"
dbtbsta = "STATISTIC_TB"
stdEndString = int("ffff", 16)
stdNullString = int("fffe", 16)

try:
    con = mdb.connect('localhost', dbuser, dbpass, dbdb)

    cur = con.cursor()
    cur.execute("SELECT * from %s where CONVERTED = 'n'" % (dbtbhex))

    notConvertedList = cur.fetchall()
    
    for notConverted in notConvertedList:

        notConvertedCheck = notConverted[1]	    # Get only HEX string
        notConvertedTstamp = notConverted[2]	# Get received timestamp RTIME of this HEX value
        notConvertedID = notConverted[0]		# Get row ID of this HEX value

        if notConvertedCheck[0:2] == '52':

            # Malformed
            if (len(notConvertedCheck) < 72):
                cur.execute("DELETE from %s where ID = '%s'" % (dbtbhex, notConvertedID))
                con.commit()
                continue
            
            rIDa = chr(int(notConvertedCheck[0:2], 16))
            rIDb = chr(int(notConvertedCheck[2:4], 16))
            rIDc = chr(int(notConvertedCheck[4:6], 16))
            rIDd = chr(int(notConvertedCheck[6:8], 16))
            rIDe = chr(int(notConvertedCheck[8:10], 16))
            rIDf = chr(int(notConvertedCheck[10:12], 16))

            rID = rIDa + rIDb + rIDc + rIDd + rIDe + rIDf

            A1 = notConvertedCheck[16:18]
            A2 = notConvertedCheck[22:24]
            B3 = notConvertedCheck[28:30]
            B4 = notConvertedCheck[34:36]
            C5 = notConvertedCheck[40:42]
            C6 = notConvertedCheck[46:48]
            D7 = notConvertedCheck[52:54]
            D8 = notConvertedCheck[58:60]

            relInfo = A1 + A2 + B3 + B4 + C5 + C6 + D7 + D8
            
            cur.execute('''INSERT into %s (ReleID,Status) values ('%s','%s')''' % (dbtbrel, rID, relInfo))
            con.commit()

            cur.execute("UPDATE %s set CONVERTED = 'y', RTIME = RTIME where ID = '%s'" % (dbtbhex,notConvertedID))
            con.commit()
        
        else:

            firstPart = notConvertedCheck [0:140]    

            if not firstPart[136:140]:
                # print "FOUND emptyend"
                cur.execute("DELETE from %s where ID = '%s'" % (dbtbhex, notConvertedID))
                con.commit()
                cur.execute('''INSERT into %s (INFO) VALUES ('EMPTYEND')''' %(dbtbsta))
                con.commit()
                continue
            else:
                endString = int(firstPart[136:140], 16)

            if not endString == stdEndString:
                cur.execute("DELETE from %s where ID = '%s'" % (dbtbhex, notConvertedID))
                con.commit()
                cur.execute('''INSERT into %s (INFO) VALUES ('MALFORMED')''' % (dbtbsta))
                con.commit()
                continue
        
            if firstPart: #== secondPart:
                cur.execute('''INSERT into %s (INFO) VALUES ('ACCEPTED')''' % (dbtbsta))
                con.commit()

                A1u = ""
                A2u = ""
                A3u = ""
                A4u = ""
                A5u = ""
                A6u = ""
                B7u = ""
                B8u = ""
                B9u = ""
                B10u  = ""
                B11u  = ""
                B12u  = ""
                C13u  = ""
                C14u  = ""
                C15u  = ""
                C16u  = ""
                C17u  = ""
                C18u  = ""
                C19u  = ""
                C20u  = ""
                C21u  = ""
                C22u  = ""
                D23u  = ""
                D24u  = ""
                D25u  = ""
                D26u  = ""
                D27u  = ""
                D28u  = ""
                D29u  = ""
                BATu  = ""
                RCu  = ""
                TSu  = ""
                DATA = ""

                cIDa = chr(int(firstPart[0:2], 16))
                cIDb = chr(int(firstPart[2:4], 16))
                cIDc = chr(int(firstPart[4:6], 16))
                cIDd = chr(int(firstPart[6:8], 16))
                cIDe = chr(int(firstPart[8:10], 16))
                cIDf = chr(int(firstPart[10:12], 16))

                cID = cIDa + cIDb + cIDc + cIDd + cIDe + cIDf
                # print ("CID is %s" % cID)

                if cID.isalnum():
                    # print ("cID VALID")
                    pass
                else:
                    cur.execute("DELETE from %s where ID = '%s'" % (dbtbhex,notConvertedID))
                    con.commit()
                    cur.execute('''INSERT into %s (INFO) VALUES ('MALFORMED')''' %(dbtbsta))
                    con.commit()
                    # print ("No cID VALID")
                    continue

                try:
                    blackList = open("/srv/data/blacklist","r")
                    blackListElements = blackList.read()
                    blackList.close()
                    # print ("Blacklist found")
                except IOError:
                    blackListElements=''
                    # print ("Blacklist not found")

                if cID in blackListElements:
                    SND = "b"
                else:
                    SND = "y"
    
                A1 = int(firstPart[12:16], 16)
                if not A1 == stdNullString:
                    A1u = "s[A1]=" + str(A1) + " "
                A2 = int(firstPart[16:20], 16)
                if not A2 == stdNullString:
                    A2u = "s[A2]=" + str(A2) + " "
                A3 = int(firstPart[20:24], 16)
                if not A3 == stdNullString:
                    A3u = "s[A3]=" + str(A3) + " "
                A4 = int(firstPart[24:28], 16)
                if not A4 == stdNullString:
                    A4u = "s[A4]=" + str(A4) + " "
                A5 = int(firstPart[28:32], 16)
                if not A5 == stdNullString:
                    A5u = "s[A5]=" + str(A5) + " "
                A6 = int(firstPart[32:36], 16)
                if not A6 == stdNullString:
                    A6u = "s[A6]=" + str(A6) + " "

                B7 = int(firstPart[36:40], 16)
                if not B7 == stdNullString:
                    B7u = "s[B7]=" + str(B7) + " "
                B8 = int(firstPart[40:44], 16)
                if not B8 == stdNullString:
                    B8u = "s[B8]=" + str(B8) + " "
                B9 = int(firstPart[44:48], 16)
                if not B9 == stdNullString:
                    B9u = "s[B9]=" + str(B9) + " "
                B10 = int(firstPart[48:52], 16)
                if not B10 == stdNullString:
                    B10u = "s[B10]=" + str(B10) + " "
                B11 = int(firstPart[52:56], 16)
                if not B11 == stdNullString:
                    B11u = "s[B11]=" + str(B11) + " "
                B12 = int(firstPart[56:60], 16)
                if not B12 == stdNullString:
                    B12u = "s[B12]=" + str(B12) + " "

                C13 = int(firstPart[60:64], 16)
                if not C13 == stdNullString:
                    C13u = "s[C13]=" + str(C13) + " "
                C14 = int(firstPart[64:68], 16)
                if not C14 == stdNullString:
                    C14u = "s[C14]=" + str(C14) + " "
                C15 = int(firstPart[68:72], 16)
                if not C15 == stdNullString:
                    C15u = "s[C15]=" + str(C15) + " "
                C16 = int(firstPart[72:76], 16)
                if not C16 == stdNullString:
                    C16u = "s[1]=" + str(C16) + " "
                C17 = int(firstPart[76:80], 16)
                if not C17 == stdNullString:
                    C17u = "s[C17]=" + str(C17) + " "
                C18 = int(firstPart[80:84], 16)
                if not C18 == stdNullString:
                    C18u = "s[C18]=" + str(C18) + " "
                C19 = int(firstPart[84:88], 16)
                if not C19 == stdNullString:
                    C19u = "s[C19]=" + str(C19) + " "
                C20 = int(firstPart[88:92], 16)
                if not C20 == stdNullString:
                    C20u = "s[C20]=" + str(C20) + " "
                C21 = int(firstPart[92:96], 16)
                if not C21 == stdNullString:
                    C21u = "s[C21]=" + str(C21) + " "
                C22 = int(firstPart[96:100], 16)
                if not C22 == stdNullString:
                    C22u = "s[C22]=" + str(C22) + " "

                D23 = int(firstPart[100:104], 16)
                if not D23 == stdNullString:
                    D23u = "s[D23]=" + str(D23) + " "
                D24 = int(firstPart[104:108], 16)
                if not D24 == stdNullString:
                    D24u = "s[D24]=" + str(D24) + " "
                D25 = int(firstPart[108:112], 16)
                if not D25 == stdNullString:
                    D25u = "s[2]=" + str(D25) + " "
                D26 = int(firstPart[112:116], 16)
                if not D26 == stdNullString:
                    D26u = "s[D26]=" + str(D26) + " "
                D27 = int(firstPart[116:120], 16)
                if not D27 == stdNullString:
                    D27u = "s[D27]=" + str(D27) + " "
                D28 = int(firstPart[120:124], 16)
                if not D28 == stdNullString:
                    D28u = "s[D28]=" + str(D28) + " "
                D29 = int(firstPart[124:128], 16)
                if not D29 == stdNullString:
                    D29u = "s[D29]=" + str(D29) + " "

                BAT = int(firstPart[128:132], 16)
                BATu = "s[BAT30]=" + str(BAT) + " "
                RC = int(firstPart[132:136], 16)
                RCu = "r=" + str(RC) + " "

                RTIME = notConvertedTstamp

                date_time = str(notConvertedTstamp)
                pattern = '%Y-%m-%d %H:%M:%S'
                TS = int(time.mktime(time.strptime(date_time, pattern)))
                TSu = "t=" + str(TS)

                DATA = A1u+A2u+A3u+A4u+A5u+A6u+B7u+B8u+B9u+B10u+B11u+B12u+C13u+C14u+C15u+C16u+C17u+C18u+C19u+C20u+C21u+C22u+D23u+D24u+D25u+D26u+D27u+D28u+D29u+BATu+RCu+TSu

                cur.execute('''INSERT into %s 
                        (CID,A1,A2,A3,A4,A5,A6,B7,B8,B9,B10,B11,B12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,D23,D24,D25,D26,D27,D28,D29,BAT,RC,TS,RTIME,SND)
                        values ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s')'''
                        % (dbtbdec,cID,A1,A2,A3,A4,A5,A6,B7,B8,B9,B10,B11,B12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,D23,D24,D25,D26,D27,D28,D29,BAT,RC,TS,RTIME,SND))
                con.commit()

                if not SND == "b":
                    cur.execute('''INSERT into %s (CID,DATA) values ('%s',"%s")''' % (dbtbupl,cID,DATA))
                    con.commit()

                cur.execute("UPDATE %s set CONVERTED = 'y', RTIME = RTIME where ID = '%s'" % (dbtbhex,notConvertedID))
                con.commit()

            else:
                cur.execute("DELETE from %s where ID = '%s'" % (dbtbhex, notConvertedID))
                con.commit()
                continue

except mdb.Error as e:
  
    # print (e)
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()
