import sys

def dist(x,y):
  d = 0
  for i in range(5):
    if x[i]>=y[i]:
      d = d+x[i]-y[i]
    else:
      d = d+y[i]-x[i]
  return d



trainFile = sys.argv[1]
classFile = sys.argv[2]
testFile = sys.argv[3]

f = open(testFile)
testData = []
for line in f:
  testData = testData+[int(line.strip("\n"))]
f.close

f = open(classFile)
classData = []
for line in f:
  con = line.strip("\n").split()
  for i in range(len(con)):
    con[i]= int(con[i])
  classData = classData+con
f.close
n= int(0.2*len(classData))
classD = [[]*5]*n
for i in range(n):
  classD[i] = classData[i*5:(i*5+5)]
# save all the class data into a dict, the keys are the index from 0 to 9

f = open(trainFile)
trainData = []
for line in f:
  con = line.strip("\n").split()
  for i in range(len(con)):
    con[i]= int(con[i])
  trainData = trainData+con
f.close
n= int(len(trainData)/6)
trainD = {}
for i in range(n):
  trainD[i] = trainData[i*6:(i*6+6)]
# save all the train data into a dict, the keys are the index from 0 to 199


for i in range(len(classD)):
  xC= classD[i]
  # take the attributes value as a list in classification data
  distMin = dist(xC,trainD[0][1:6]) 
  valueMin = trainD[0][0]
  # take the class value.
  for j in range(n):

    if dist(xC,trainD[j][1:6]) == distMin:
      if trainD[j][0]<valueMin:
        valueMin = trainD[j][0]
        
    elif dist(xC,trainD[j][1:6]) < distMin:
      valueMin = trainD[j][0]
      distMin = dist(xC,trainD[j][1:6])
    else:
      distMin
      # no action needed. distMin can be other
  xCnum = str(xC[0])
  for item in [1,2,3,4]:
    xCnum += " "+str(xC[item])
  print "Item: %s prediction: %s correct: %s" %(xCnum,valueMin,testData[i])
