import os
import json
from collections import Counter
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class MRLenDists(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol
    MRJob.SORT_VALUES = True
    
    def mapper(self, _, line):
        fileName = os.getenv('mapreduce_map_input_file')
        for word in line.split():
            yield os.path.basename(fileName), str(len(word))

    def reducer(self, fileName, wlens):
        jsonRes = dict(Counter(wlens))
        jsonRes['file'] = fileName
        yield None, json.dumps(jsonRes)

if __name__ == '__main__':
    MRLenDists.run()
