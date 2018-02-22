from mrjob.job import MRJob

M = 200
PARTSIZE = 1000

class MRMovingAvg(MRJob):

    MRJob.SORT_VALUES = True
    
    def mapper(self, _, line):
        dataRow = line.split()
        i = int(dataRow[0])
        val = dataRow[1]
        part = i/PARTSIZE
        yield part, str(i) + '\t' + val
        prevPart = (i-M/2)/PARTSIZE
        nextPart = (i+M/2-1)/PARTSIZE
        if prevPart != part and prevPart >= 0:
            yield prevPart, str(i) + '\t' + val + '\tX'
        if nextPart != part:
            yield nextPart, str(i) + '\t' + val + '\tX'

    def reducer(self, part, vals):
        valDict = {}
        allXtra = True
        for val in vals:
            v = val.split('\t')
            if len(v) == 2:
                valDict[int(v[0])] = [float(v[1])]
                allXtra = False
            else:
                valDict[int(v[0])] = [float(v[1]), None]
        if not allXtra:
            for i in sorted(valDict):
                if len(valDict[i]) == 1:
                    total = 0
                    count = 0
                    for j in range(i-M/2, i+M/2):
                        if j in valDict:
                            total += valDict[j][0]
                            count += 1
                    yield i, total/count

if __name__ == '__main__':
    MRMovingAvg.run()
