import sys
import os

#use: pip install simplekml
from simplekml import Kml, Snippet, Types, AltitudeMode


if len(sys.argv) != 3:
    print("Wrong Payload!")
    quit()

input_filename = str(sys.argv[1])       # Input_filename is the first parameter
output_filename = str(sys.argv[2])      # Output_filename is the secound parameter

if not os.path.isfile(input_filename):  #Check if the Input file exists
    print("Input-File not found!")
    quit()

if os.path.isfile(output_filename):     #Check if the Output file already exists
    print("Output-File already exists! Do you want to overwrite?")
    i = input()
    while i not in ["YES", "NO"]:
        i = input("YES or NO?")
    if i == "NO":
        quit()

print("STARTING")
print('The File {} will be "translated" into {}'.format(input_filename, output_filename))

fileinput = open(input_filename, 'r')

kml = Kml(name="Tracks", open=1)
fol = kml.newfolder(name='Track')
trk = fol.newgxtrack(name='EFB GPS Mouse')
trk.altitudemode = AltitudeMode.absolute

read = {}
number = 0

for line in fileinput:
    read[number] = str(line.split())
    number = number + 1


for i in range(len(read)):
    # parse DATA-----------------------------------------------------------
    if i > 4:  # first line of log have no information
        JepLogLine = read[i].split("'")
        # for part in range (28):    #debug
        #    print (JepLogLine [part])    #debug

        JepLogDate = JepLogLine[3].split('/')
        # for step in range (3):    #debug
        #    print (JepLogDate [step])    #debug
        newDay = JepLogDate[0]
        newMonth = JepLogDate[1]
        newYear = JepLogDate[2]

        JepLogTime = JepLogLine[5].split(':')
        # for step in range (3):    #debug
        #    print (JepLogTime [step])    #debug
        newHour = JepLogTime[0]
        newMinute = JepLogTime[1]
        newSecunde = JepLogTime[2]

        newLatNS = JepLogLine[7]
        # print (newLatNS)    #debug
        newLatDegree = JepLogLine[9]
        # print (newLatDegree)    #debug
        newLatMinutes = JepLogLine[11]
        # print (newLatMinutes)    #debug
        newLatSecunds = JepLogLine[13]
        # print (newLatSecunds)    #debug
        JepLatSecunds = newLatSecunds.split('.')
        newLatSecundsFull = JepLatSecunds[0]
        # print (newLatSecundsFull)    #debug
        newLatDecimal = JepLatSecunds[1]
        # print (newLatDecimal)    #debug

        newLongEW = JepLogLine[15]
        # print (newLongEW)    #debug
        newLongDegree = JepLogLine[17]
        # print (newLongDegree)    #debug
        newLongMinutes = JepLogLine[19]
        # print (newLongMinutes)    #debug
        newLongSecunds = JepLogLine[21]
        # print (newLongSecunds)    #debug
        JepLongSecunds = newLongSecunds.split('.')
        newLongSecundsFull = JepLongSecunds[0]
        # print (newLongSecundsFull)    #debug
        newLongDecimal = JepLongSecunds[1]
        # print (newLongDecimal)    #debug

        newCourseDegree = JepLogLine[23]
        # print (newCourseDegree)    #debug

        newGroundSpeedKt = JepLogLine[25]
        # print (newGroundSpeedKt)    #debug

        newAltFeedMSL = JepLogLine[27]
        # print (newAltFeedMSL)    #debug

        # Calculate/Transform Decimalpoint of LAT/LONG ----------------------------------------
        calculatedLat = int(newLatDegree) + int(newLatMinutes) / 60 + float(newLatSecunds) / 3600
        # print (calculatedLat)    #debug
        calculatedLong = int(newLongDegree) + int(newLongMinutes) / 60 + float(newLongSecunds) / 3600
        # print (calculatedLong)    #debug
        calculatedAltMeterMSL = int(newAltFeedMSL) / 3.3
        # print (calculatedAltMeterMSL)    #debug

        trk.newwhen('{}-{}-{}T{}:{}:{}Z'.format(newYear, newMonth, newDay, newHour, newMinute, newSecunde))
        trk.newgxcoord([(calculatedLong,calculatedLat,calculatedAltMeterMSL)])

kml.save(output_filename)

print("FINISHED")
