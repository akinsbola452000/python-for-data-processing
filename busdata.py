import urllib
import sys
import time

sleep = int(sys.argv[2])
timespan = int(sys.argv[3])
end = time.time() + timespan
i = 0
with open(sys.argv[1], 'w') as resfile:
    while time.time() < end:
        i += 1
        print >> sys.stderr, 'Iteration', str(i)
        data = urllib.urlopen("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
        print >> resfile, data.read()
        time.sleep(sleep)
