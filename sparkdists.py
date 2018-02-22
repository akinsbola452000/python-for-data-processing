from pyspark import SparkContext
import json

import re

# input to wholeFile is a file name, file content pair

def wholeFile(x):

    name=x[0]
    c = {}
    f = {}
    words = re.sub('[^a-z0-9]+',' ',x[1].lower()).split()
    for word in set(words):
        if word in words:
            f['file'] = name
            c['count'] +=1
        else:
            f['file'] = name
            c['count'] = 1
    return {f,c}

sc = SparkContext(appName='WordsInFiles')

data = sc.wholeTextFiles ('/user/student/americana/')

word_index = data.flatMap(wholeFile).reduceByKey(lambda a,b:','.join((a,b))).map(lambda  x: json.dumps(x)).saveTextfile(ouput)


word_index.persist()

output=word_index.collect()

output.sort()

# print the first 10 values

for i in range(10):

    print output[i]

#explore(word_index)

sc.stop()
