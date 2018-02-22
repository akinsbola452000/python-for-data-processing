import json
from sys import argv
import numpy

speeds = {}
with open(argv[1], 'r') as infile:
    for jsonline in infile:
        data = json.loads(jsonline)
        for item in data['body']:
            line = item['monitoredVehicleJourney']['lineRef'] 
            speed = item['monitoredVehicleJourney']['speed']
            vehicle = item['monitoredVehicleJourney']['vehicleRef']
            time = item['recordedAtTime']
            if line not in speeds:
                speeds[line] = {}
            if vehicle not in speeds[line]:
                speeds[line][vehicle] = {}
            speeds[line][vehicle][time] = float(speed)

for line in speeds:
    speeds[line] = [s for veh in speeds[line] for s in speeds[line][veh].values()]

print '\t'.join(sorted(speeds))
allDone = False
while not allDone:
    allDone = True
    row = []
    for line in sorted(speeds):
        if len(speeds[line]) > 0:
            row.append(str(speeds[line].pop()))
        else:
            row.append(" ")
        if len(speeds[line]) > 0:
            allDone = False
    print '\t'.join(row)
