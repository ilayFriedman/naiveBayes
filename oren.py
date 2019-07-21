import math

from NaiveBayes import NaiveBayes




def discretization(bind):
    nb = NaiveBayes()
    nb.build("C:/Users/shororen/PycharmProjects/naiveBayes")
    for att in nb.content.items():
        if('NUMERIC' in att[1]):
            print ('###')
            index = nb.attIndexes[att[0]]
            nb.train_Data.sort(key=lambda x: x[index])
            col = map(float, nb.rowByIndex(index))
            mini = min(col)
            maxi = max(col)
            range = (maxi - mini)/bind
            currVal = round(mini + range,3)
            j = 1
            for i in nb.train_Data:
                # min =
                tmp = i[index]
                if(int(i[index]) <= currVal):
                    i[index] = round(currVal,3)
                else:
                    currVal += range
                    while(int(i[index]) > currVal):
                        currVal += range
                    i[index] = round(currVal,3)

    print(nb.train_Data)




discretization(100)