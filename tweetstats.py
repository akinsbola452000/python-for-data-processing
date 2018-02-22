import langid
import langdetect
import json
import sys
import heapq

langs = {}
langWordCounts = {}
with open(sys.argv[1], 'r') as tweetfile:
    for i, line in enumerate(tweetfile):
        if (i % 100) == 0:
            print >> sys.stderr, i
        tweet = json.loads(line)
        try:
            res = [langid.classify(tweet['text'])[0],
                   langdetect.detect(tweet['text']), tweet['lang']]
            for j, r in enumerate(res):
                if r not in langs:
                    langs[r] = [0, 0, 0]
                langs[r][j] += 1
            if res[2] not in langWordCounts:
                langWordCounts[res[2]] = {}
            for w in tweet['text'].split():
                if w not in langWordCounts[res[2]]:
                      langWordCounts[res[2]][w] = 0
                langWordCounts[res[2]][w] += 1
        except:
            pass

for lang in sorted(langs):
    print lang, langs[lang]
    if lang in langWordCounts:
        top10 = heapq.nlargest(10, langWordCounts[lang].iteritems(),
                                                          key = lambda x: x[1])
        print '\ttop10: ', ', '.join([w[0] for w in top10]) 
