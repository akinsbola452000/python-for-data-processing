from mrjob.job import MRJob

class MRWordFreqCount(MRJob):

    def mapper_init(self):
        self.stopset = set()
        with open('stopwords.txt', 'r') as stopfile:
            for w in stopfile.read().split(','):
                self.stopset.add(w)

    def mapper(self, _, line):
        for word in line.split():
            lowword = word.lower()
            if lowword not in self.stopset:
                yield lowword, 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    MRWordFreqCount.run()
