import sys
import os
from mrjob.job import MRJob
from math import radians, cos, sin, asin, sqrt

def haversine(p1, p2):  # p1, p2 coordinate points of form [latitude, longitude].
    # Convert decimal degrees to radians (also ensures values are floats).
    pr1 = [radians(float(p1[0])), radians(float(p1[1]))]
    pr2 = [radians(float(p2[0])), radians(float(p2[1]))]

    # Haversine formula
    dlat = pr2[0] - pr1[0]   # Difference of latitudes.
    dlon = pr2[1] - pr1[1]   # Difference of longitudes.
    a = sin(dlat/2)**2 + cos(pr1[0]) * cos(pr2[0]) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    return c * r

class MRBusDists(MRJob):

    MRJob.SORT_VALUES = True
    
    def mapper(self, _, line):
        dataRow = line.split(',')
        if dataRow[0] != 'time':
            time = dataRow[0]
            hour = time[11:13]
            lat = dataRow[5]
            lon = dataRow[4]
            veh = dataRow[9]
            if veh.startswith('TKL') and lat != '0' and lon != '0':
                yield hour, veh + ',' + time + ',' + lat + ',' + lon

    def reducer(self, hour, vehLocs):
        prev = None
        kms = 0
        for vehLoc in vehLocs:
            curr = vehLoc.split(',')
            if prev is not None and curr[0] == prev[0] and curr[1] != prev[1]:
                d = haversine([curr[2], curr[3]], [prev[2], prev[3]])
                kms += d
#                if d > 1:
#                    print d, curr, prev
            prev = curr
        yield hour, kms

if __name__ == '__main__':
    MRBusDists.run()
