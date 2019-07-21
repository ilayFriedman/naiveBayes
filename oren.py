import math

from NaiveBayes import NaiveBayes

nb = NaiveBayes()
nb.build("D:/documents/users/ilayfri/Downloads", 100)

def mEstimator(attIndex, attValue, classIndex,classValue):
    m = 2
    #print (m)
    nc = ncValue(attIndex,attValue,classIndex,classValue)
   # print ("nc: "+ str(nc))
    p = 1/float((len(nb.content[nb.attIndexes.keys()[nb.attIndexes.values().index(attIndex)]])))
    #print ("p: "+ str(p))
    n = nb.rowByIndex(classIndex).count(classValue)
    #print ("n: " + str(n))

    return float(float(nc+float(m*p))/float(n+m))

def ncValue(attIndex,attValue,classIndex,classValue):
    counter = 0
    for line in nb.train_Data:
        if(line[attIndex] == attValue and line[classIndex] == classValue):
            counter += 1

    return counter


print (mEstimator(9,"Rural",10,"Y"))
