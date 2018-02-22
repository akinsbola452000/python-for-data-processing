import sys
import numpy
with open(sys.argv[1], 'r') as f:
    x = map(lambda val: float(val), f.read().split())
print "Minimum:", numpy.amin(x)
print "Maximum:", numpy.amax(x)
print "Average:", numpy.mean(x)
print "Median:", numpy.median(x)
print "Variance:", numpy.nanvar(x)
