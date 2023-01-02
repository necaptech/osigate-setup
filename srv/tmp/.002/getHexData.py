#!/usr/bin/env python

from subprocess import call
import serial
import MySQLdb
import time

conn = MySQLdb.connect(host= "localhost",
    user="root", passwd="root", db="TECNOQ")
x = conn.cursor()
s_port = '/dev/ttyS0'
# s_port = '/dev/ttyUSB0'
b_rate = 1200

def read_serial(ser):
    
    while True:
        inp=''
        try:
            inp = ser.read(size=70) 
            if inp:

                # f = open("/srv/tmp/.002/getLoggg.log", "a")
                # f.write("%s\n%s\n\n" % (inp, inp.hex()))
                # f.close()
                
                x.execute('''INSERT into HEX_INPUT_TB (HEXSTR) values (%s)''',[inp.hex()])
                conn.commit()
            
            with open('/srv/tmp/relUpdate.txt', "r") as releUpdatesFile:
                releUpdates = [x.replace("\n", "") for x in releUpdatesFile.readlines()]
                if releUpdates:
                    for releUpdate in releUpdates:
                        byteUpd = bytes.fromhex(releUpdate)
                        ser.write(byteUpd)
            
                    with open('/srv/tmp/relUpdate.txt', "w") as resetReleUpdatesFile:
                        resetReleUpdatesFile.write("")
                    time.sleep(1)
                    break

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
    timeout=3,
    write_timeout=2.5
)

# print(">>> Receiving messages on radio interface from port %s ..." % s_port)

while True:
    rx = read_serial(ser)
