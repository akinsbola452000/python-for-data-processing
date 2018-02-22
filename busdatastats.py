import json
from sys import argv
from datetime import datetime
import StringIO

busdata = {}
with open("busdata.json", 'r') as infile:
    databuf = StringIO.StringIO()
    for line in infile:
        databuf.write(line)
        if line == '}\n':
            databuf.seek(0)
            data = json.load(databuf)
            databuf.close()
            databuf = StringIO.StringIO()
            for trip in data['body']:
                route = trip['monitoredVehicleJourney']['lineRef']
                veh = trip['monitoredVehicleJourney']['vehicleRef']
                t = trip['recordedAtTime']
                if route not in busdata:
                    busdata[route] = {}
                if veh not in busdata[route]:
                    busdata[route][veh] = {}
                busdata[route][veh][t] = trip
            #with open ('bola.json', 'a') as f:
                #json.dump(data,f, indent=2)
                #f.write("\n")
    databuf.close()

for key in sorted(busdata):
    pointCount = sum(len(busdata[key][k]) for k in busdata[key])
    print key + ':', len(busdata[key]), 'vehicles and', pointCount, 'data points'
    print '  vehicles:', ', '.join(busdata[key])

