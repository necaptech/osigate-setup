#!/usr/bin/env python

from subprocess import call
import serial
import MySQLdb
import time

conn = MySQLdb.connect(host= "localhost",
    user="root", passwd="root", db="TECNOQ")
x = conn.cursor()
s_port = '/dev/ttyS0'
#s_port = '/dev/ttyUSB0'
b_rate = 1200

def read_serial(ser):
    c = 0
    while True:
        inp=''
        try:
            inp = ser.read(size=71) 
            if inp:
                c+=1
                print (" [*] inp = %s" % inp)
                if inp[0] == 'R':
                    print ("Message %d from OsiRELE" % c)
                    x.execute('''INSERT into OSIRE_STATUS (status) values (%s)''',[inp.hex()])
                else:
                    print ("Message %d from OsiNODE" % c)
                    print (inp)
                    print ('''INSERT into HEX_INPUT_TB (HEXSTR) values (%s)''',[inp.hex()])
                    x.execute('''INSERT into HEX_INPUT_TB (HEXSTR) values (%s)''',[inp.hex()])
                conn.commit()
        except Exception as e:
            f = open("/var/log/getHexData.log", "a")
            f.write("%s RX Error: %s, message: %s\n" % (time.asctime(), str(e), inp))
            f.close()
            continue
        except:
            f = open("/var/log/getHexData.log", "a")
            f.write("%s Unknown RX Error! Message: %s\n" % (time.asctime(), inp))
            f.close()
            continue

ser = serial.Serial(
    port=s_port,
    baudrate=b_rate,
    timeout=0.05
)

print(">>> Receiving messages on radio interface from port %s ..." % s_port)

while True:
    rx = read_serial(ser)
