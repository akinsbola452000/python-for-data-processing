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

print '\t'.join(sorted(speeds))
means = []
for line in sorted(speeds):
    means.append(numpy.mean([sp for v in speeds[line] for sp in speeds[line][v].values()]))
print '\t'.join([str(x) for x in means])
