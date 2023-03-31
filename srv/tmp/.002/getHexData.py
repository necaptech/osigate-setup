#!/usr/bin/env python

from datetime import datetime, timedelta
from subprocess import call
from random import random
import serial
import MySQLdb
import time
import os.path

conn = MySQLdb.connect(host= "localhost", user="root", passwd="root", db="TECNOQ")
x = conn.cursor()
s_port = '/dev/ttyS0'
# s_port = '/dev/ttyUSB0'
b_rate = 1200

nodeconvdb = 'DEC_INPUT_TB'
relestatusdb = 'OSIRE_STATUS'

class Rule:
    def __init__(self, rele, pin, node, port, compar, value, duration, delay):
        self.rele, self.pin = rele, pin
        self.node, self.port = node, port.upper()
        self.compar, self.value = compar, int(value)
        self.duration, self.delay = int(duration), int(delay)

    def __str__(self):
        return f"{self.rele}.{self.pin} {self.node}:{self.port} {self.compar} {self.value} ON FOR {self.duration}, FORCE OFF FOR {self.delay}"

onoff = 'ON'
duration = 'duration'
until = 'until'
delayend = 'delayend'
startRange = 'rStart'
endRange = 'rEnd'
maxTries = 8

# Get Rules
rules = []
relesStatus = {}
recentTries = {}
try:
    if (os.path.exists('/srv/data/osiRele')):
        with open('/srv/data/osiRele', "r") as relesNamesFile:
            relesNames = [x.replace("\n", "") for x in relesNamesFile.readlines()]
            for releName in relesNames:
                if releName:
                    recentTries[releName] = 0
                    relesStatus[releName] = {}
                    for relPin in range(1, 9):
                        relesStatus[releName][relPin] = {onoff: 0, until: 0, delayend: 0}
                        pinFileName = '/srv/data/' + releName + '.' + str(relPin)
                        if (os.path.exists(pinFileName)):
                            with open(pinFileName, "r") as pinFile:
                                pinRuleData = [x.replace("\n", "") for x in pinFile.readlines()]
                                try:
                                    rules.append(Rule(releName, relPin, pinRuleData[1], pinRuleData[2], pinRuleData[3], pinRuleData[4], pinRuleData[5], pinRuleData[6]))
                                except: pass
except: pass

# print([str(rule) for rule in rules])

# Get Time Range
rulesTimeRange = {}
for relPin in range(1, 9):
    try:
        with open('/srv/data/timeRange.' + str(relPin), "r") as timeRangeFile:
            rangeSt, rangeEn = [int(y.split(":")[0]) * 3600 + int(y.split(":")[1]) * 60 for y in [x.replace("\n", "") for x in timeRangeFile.readlines()]]
            rulesTimeRange[relPin] = {startRange: rangeSt, endRange: rangeEn}
    except:
        rulesTimeRange[relPin] = {startRange: 0, endRange: 86400}

# Get Rele Starting Status
try:
    x.execute("SELECT * from %s ORDER BY ID DESC LIMIT 8" % (relestatusdb))
    relesStartStatus = x.fetchall()

    relesStartNames = []
    for releStartStatus in relesStartStatus:
        if releStartStatus[1] not in relesStartNames:
            relesStartNames.append(releStartStatus[1])
            for relPin in range(1, 9):
                relesStatus[releStartStatus[1]][relPin][onoff] = (1 if releStartStatus[2][(relPin - 1) * 2 : relPin  * 2] == 'ff' else 0)
except: pass

# Get Inactivity Check
try:
    with open('/srv/data/tCONST', "r") as inactivityCheckFile:
        inactivityCheck = int(inactivityCheckFile.read())
except: inactivityCheck = 10

def read_serial(ser):

    # Init Time Check For Check
    timeCfC = time.time()

    # Init Misc
    mustBeUpdated = []
    updatingOtherReles = False
    
    # timeA = timeB = 0
    while True:

        # print(relesStatus)
        # print()

        inp=''
        try:
            inp = ser.read(size=70)
            if inp:

                # f = open("/srv/tmp/.002/getLoggg.log", "a")
                # f.write("%s\n%s\n%s\n\n" % (str(datetime.now()), inp, inp.hex()))
                # f.close()

                f = open("/var/www/html/log.log", "a") # TMP
                f.write("IN: %s (%s)\n" % (inp.hex(), str(datetime.now()))) # TMP
                f.close() # TMP

                # print(inp.hex())
                
                x = conn.cursor()
                x.execute('''INSERT into HEX_INPUT_TB (HEXSTR) values (%s)''',[inp.hex()])
                conn.commit()

            # Get Now Time
            nowTime = int(time.time())

            # Do cool stuff            
            if (nowTime > timeCfC and rules):

                f = open("/var/www/html/log.log", "a") # TMP
                f.write("STATUS: %s (%s)\n" % (str(relesStatus), str(datetime.now()))) # TMP
                f.close() # TMP

                # Get Current Data
                conn = MySQLdb.connect(host= "localhost", user="root", passwd="root", db="TECNOQ")
                x = conn.cursor()
                x.execute("SELECT * from %s where TS > %s ORDER BY ID DESC" % (nodeconvdb, nowTime - 2520)) 
                nodeUpdates = x.fetchall()
                # print(nodeUpdates)
                # print()
                
                if not updatingOtherReles:

                    now = datetime.now()
                    todayRel = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

                    # Setup Check NODE Once 
                    updNODENames = []

                    # Empty Rele-to-update list
                    mustBeUpdated = []

                    # Remove Old ON
                    for releN in relesStatus:
                        for relPin in range(1, 9):
                            pinSt = relesStatus[releN][relPin] 
                            if pinSt[onoff] and nowTime >= pinSt[until]:
                                pinSt[onoff] = pinSt[until] = 0
                                if releN not in mustBeUpdated:
                                    mustBeUpdated.append(releN)

                    # Check Recent Tries
                    y = conn.cursor()
                    y.execute("SELECT * from %s where Unix > '%s' ORDER BY ID DESC" % (relestatusdb, datetime.strftime(datetime.now() - timedelta(minutes=1), "%Y-%m-%d %H:%M:%S"))) 
                    relesRecentDB = y.fetchall()   # print(relesRecentDB)
                    for relNam in recentTries:
                        relTries = recentTries[relNam]
                        if relTries > 0:
                            isThereResponse = False
                            for relesRecent in relesRecentDB:
                                if relesRecent[1] == relNam:
                                    isThereResponse = True
                                    break

                            if isThereResponse:
                                recentTries[relNam] = 0
                            else:
                                recentTries[relNam] += 1
                                if relTries < maxTries and relNam not in mustBeUpdated:
                                    mustBeUpdated.append(rule.rele)

                    # Check Node for Rules
                    for nodeUpdate in nodeUpdates:
                        if (nodeUpdate[1] not in updNODENames):
                            updNODENames.append(nodeUpdate[1])

                            # Analyze Data
                            ports = {}
                            nodeID, ports['A1'], ports['A2'], ports['A3'], ports['A4'], ports['A5'], ports['A6'], ports['B7'], ports['B8'], ports['B9'], ports['B10'], ports['B11'], ports['B12'], ports['C13'], ports['C14'], ports['C15'], ports['C16'], ports['C17'], ports['C18'], ports['C19'], ports['C20'], ports['C21'], ports['C22'], ports['D23'], ports['D24'], ports['D25'], ports['D26'], ports['D27'], ports['D28'], ports['D29'], ports['BAT30'] = nodeUpdate[1:32]
                            for rule in rules:
                                if nodeID == rule.node:
                                    portValue = ports[rule.port]
                                    if ((rule.compar == 'lt' and portValue < rule.value) or (rule.compar == 'gt' and portValue > rule.value)): # VALUE
                                        if rulesTimeRange[rule.pin][startRange] <= todayRel <= rulesTimeRange[rule.pin][endRange]: # TIMERANGE
                                            if nowTime > relesStatus[rule.rele][rule.pin][delayend]: # DELAY
                                                x.execute("SELECT * from %s where CID = '%s' LIMIT %s" % (nodeconvdb, rule.node, inactivityCheck))
                                                checkNodeDatas = x.fetchall()
                                                
                                                # rule.port = 'B11'
                                                activityChecked = False
                                                portPos = 31 if rule.port == 'BAT30' else (int(rule.port[1:]) + 1)
                                                
                                                for checkNodeData in checkNodeDatas:
                                                    if checkNodeData[portPos] != portValue:
                                                        activityChecked = True
                                                        break

                                                if activityChecked or inactivityCheck < 3:
                                                    relesStatus[rule.rele][rule.pin][onoff] = 1
                                                    relesStatus[rule.rele][rule.pin][until] = nowTime + (rule.duration * 60)
                                                    relesStatus[rule.rele][rule.pin][delayend] = nowTime + (rule.duration + rule.delay) * 60 
                                                    if rule.rele not in mustBeUpdated:
                                                        mustBeUpdated.append(rule.rele)

                # print(relesStatus) # print() # print(5/0)

                updatingOtherReles = False
                if len(mustBeUpdated) > 0:
                    releName = mustBeUpdated[0]
                    del mustBeUpdated[0]

                    relStat = relesStatus[releName]

                    # Build Message
                    msg = ""
                    for ch in releName:
                        msg += f'{ord(ch):x}'
                    
                    for pinNum, pinStat in relStat.items():
                        msg += 'ff' if pinStat[onoff] else '00' 

                    msg += (f'{(sum(bytes.fromhex(msg))):x}'.zfill(4))
                    msg += '0ff0'    

                    # Send Message (Twice)
                    byteMsg = bytes.fromhex(msg)
                    # print(msg)
                    # print(byteMsg)
                    ser.write(byteMsg)

                    recentTries[releName] += 1

                    f = open("/var/www/html/log.log", "a") # TMP
                    f.write("OUT: %s (%s)\n" % (msg, str(now))) # TMP
                    f.close() # TMP
                
                    if len(mustBeUpdated) > 0:
                        updatingOtherReles = True
                
                time.sleep(random())

                # Update Check Time
                nowTime = int(time.time())
                if updatingOtherReles:
                    timeCfC = nowTime + 10
                else:
                    timeCfC = nowTime + 30

        except Exception as e:
            print(e)
            pass

ser = serial.Serial(
    port=s_port,
    baudrate=b_rate,
    timeout=3,
    write_timeout=1
)

# print(">>> Receiving messages on radio interface from port %s ..." % s_port)

while True:
    rx = read_serial(ser)
