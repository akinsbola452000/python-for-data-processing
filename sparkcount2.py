from pyspark import SparkContext
stopwords = set(['a','able','about','across','after',
'all','almost','also','am','among','an',
'and','any','are','as','at','be','because','been',
'but','by','can','cannot','could','dear','did','do',
'does','either','else','ever','every','for','from',
'get','got','had','has','have','he','her','hers','him',
'his','how','however','i','if','in','into','is','it','its',
'just','least','let','like','likely','may','me','might',
'most','must','my','neither','no','nor','not','of','off',
'often','on','only','or','other','our','own','rather','said',
'say','says','she','should','since','so','some','than','that',
'the','their','them','then','there','these','they','this','tis',
'to','too','twas','us','wants','was','we','were','what','when',
'where','which','while','who','whom','why','will','with',
'would','yet','you','your'])

def main():

    sc = SparkContext(appName='SparkWordCount')
    #stopwordslist = sc.textFile('stopwords.txt')
    #stopwordslist = data.split("\t")
    input_file = sc.textFile('/user/student/americana/')
    counts = input_file.flatMap(lambda line: line.split()) \
                        .map(lambda word: (word, 1)) \
                        .filter(lambda word: word not in stopwords) \
                        .reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile('/user/student/test04/4_3')
    sc.stop()
if __name__ == '__main__':
    main()
