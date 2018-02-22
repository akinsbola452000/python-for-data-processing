from scipy.spatial.distance import cityblock as manhattan
from scipy.spatial.distance import euclidean
from sklearn.linear_model import Perceptron

def matches(a, b):
    res = 0
    if len(a) == len(b):
        for i in range(len(a)):
            res += (a[i] == b[i])
    return res

train_data = []
train_answ = []
test_data = []
test_answ = []

with open('vertigo_train.txt', 'r') as f:
    for line in f.readlines():
        vals = map(float, line.split())
        train_answ.append(vals[0])
        train_data.append(vals[1:])

with open('vertigo_predict.txt', 'r') as f:
    for line in f.readlines():
        test_data.append(map(float, line.split()))

with open('vertigo_answers.txt', 'r') as f:
    for line in f.readlines():
        test_answ.append(float(line))

#perceptron = Perceptron(n_iter = 100)
perceptron = Perceptron()
perceptron.fit(train_data, train_answ)
perceptron_answ = perceptron.predict(test_data)
n = float(len(test_data))
print "Perceptron: " + str(matches(perceptron_answ, test_answ) / n) + "% correct"

nearest_answ = []
for item in test_data:
    best = None
    for i in range(len(train_data)):
#        dist = euclidean(item, train_data[i])
        dist = manhattan(item, train_data[i])
        if not best or best[0] > dist:
            best = (dist, train_answ[i])
    nearest_answ.append(best[1])
print "Nearest neighbor: " + str(matches(nearest_answ, test_answ) / n) + "% correct"
