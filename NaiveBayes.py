import csv
from collections import Counter


class NaiveBayes:
    def build(self, folderPath, bind):
        self.folderPath = folderPath
        self.minMax = {}
        self.numericAtt = {}
        self.bind = bind
        # READ DATA
        with open(self.folderPath + '/train.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(file)
            self.train_Data = list(reader)
        file.close()

        # READ CONTENT
        with open(self.folderPath + "/Structure.txt", "r") as structureFile:
            self.content = {}
            self.attIndexes = {}
            attributes = structureFile.read().replace("\n", "").split("@ATTRIBUTE ")
            # print(attributes)
            i = 0
            attributes.pop(0)
            for att in attributes:
                start = att.find('{')
                key = att[:start - 1]
                values = att[start + 1:-1]
                values = values.split(",")
                if (start != -1):
                    self.content[key] = values
                    self.attIndexes[key] = i
                    i += 1
                else:
                    start = att.find('NUMERIC')
                    if (start != -1):
                        key = att.split(" ")[0]
                        self.content[key] = 'NUMERIC'
                        self.attIndexes[key] = i
                        self.numericAtt[key] = i
                        i += 1
            # print(self.content)
            # print(self.attIndexes)
        structureFile.close()

        # GET FILLED VALUES
        self.missingValues()

        # FILL MISSING VALUES
        self.fillEmptyValues('train')

        # discretization
        self.discretization(self.bind, "train")

    def fillEmptyValues(self, type):
        if(type == 'train'):
            for line in self.train_Data:
                includeEmptyCell = '' in line
                while (includeEmptyCell):
                    indexEmpty = line.index('')
                    line[indexEmpty] = self.missValues[indexEmpty]
                    includeEmptyCell = '' in line
            del (self.missValues)
            self.missValues = {}
        elif(type == 'test'):
            for line in self.test_Data:
                includeEmptyCell = '' in line
                while (includeEmptyCell):
                    indexEmpty = line.index('')
                    line[indexEmpty] = self.missValues[indexEmpty]
                    includeEmptyCell = '' in line


    def missingValues(self):
        self.missValues = {}
        for att in self.attIndexes.items():
            if (att[0] in self.numericAtt):
                rowList = self.rowByIndex(att[1])
                self.missValues[att[1]] = str(round(sum(map(float, rowList)) / len(rowList), 3))
            else:
                rowList = self.rowByIndex(att[1])
                self.missValues[att[1]] = Counter(rowList).most_common(1)[0][0]

        # print (self.missValues)

    def rowByIndex(self, index):
        rowInIndex = []
        for line in self.train_Data:
            if (line[index] != ''):
                rowInIndex.append(line[index])
        return rowInIndex

    def discretization(self, bind, type):
        if (type == "train"):
            for att in self.content.items():
                if ('NUMERIC' in att[1]):
                    index = self.attIndexes[att[0]]
                    self.train_Data.sort(key=lambda x: x[index])
                    col = map(float, self.rowByIndex(index))
                    mini = min(col)
                    maxi = max(col)
                    self.minMax[att[0]] = [mini, maxi]
                    range = (maxi - mini) / bind
                    self.content[att[0]] = []
                    currVal = round(mini + range, 3)
                    j = 1
                    for i in self.train_Data:
                        tmp = i[index]
                        if (float(i[index]) <= currVal):
                            i[index] = round(currVal, 3)
                            self.content[att[0]].append(round(currVal, 3))
                        else:
                            currVal += range
                            while (float(i[index]) > currVal):
                                currVal += range
                            i[index] = round(currVal, 3)
                            self.content[att[0]].append(round(currVal, 3))
                    self.content[att[0]] = set(self.content[att[0]])
        elif (type == "test"):
            for att in self.numericAtt:
                index = self.numericAtt[att]
                self.test_Data.sort(key=lambda x: x[index])
                mini = self.minMax[att][0]
                maxi = self.minMax[att][1]
                rangeTest = (maxi - mini) / bind
                currValTest = round(mini + rangeTest, 3)
                for i in self.test_Data:
                    # min =
                    tmp = i[index]
                    if (float(i[index]) <= currValTest):
                        i[index] = round(currValTest, 3)
                    else:
                        currValTest += rangeTest
                        while (float(i[index]) > currValTest):
                            currValTest += rangeTest
                        i[index] = round(currValTest, 3)
    #
    # if (type == "train"):
    #     for att in self.content.items():
    #         if ('NUMERIC' in att[1]):
    #             index = self.attIndexes[att[0]]
    #             self.train_Data.sort(key=lambda x: x[index])
    #             col = map(float, self.rowByIndex(index, self.train_Data))
    #             mini = min(col)
    #             maxi = max(col)
    #             range = (maxi - mini) / bind
    #             self.content[att[0]] = []
    #             currVal = round(mini + range, 3)
    #             j = 1
    #             for i in self.train_Data:
    #                 # min =
    #                 tmp = i[index]
    #                 if (float(i[index]) <= currVal):
    #                     i[index] = round(currVal, 3)
    #                     self.content[att[0]].append(round(currVal, 3))
    #                 else:
    #                     currVal += range
    #                     while (float(i[index]) > currVal):
    #                         currVal += range
    #                     i[index] = round(currVal, 3)
    #                     self.content[att[0]].append(round(currVal, 3))
    #             self.content[att[0]] = set(self.content[att[0]])
    # elif (type == "test"):
    #     for att in self.numericAtt:
    #         index = self.numericAtt[att]
    #         self.test_Data.sort(key=lambda x: x[index])
    #         col = map(float, self.rowByIndex(index, self.train_Data))
    #         miniTest = min(col)
    #         maxiTest = max(col)
    #         rangeTest = (miniTest - maxiTest) / bind
    #         currValTest = round(maxiTest + rangeTest, 3)
    #         for i in self.test_Data:
    #             # min =
    #             tmp = i[index]
    #             if (float(i[index]) <= currValTest):
    #                 i[index] = round(currValTest, 3)
    #             else:
    #                 currValTest += rangeTest
    #                 while (float(i[index]) > currValTest):
    #                     currValTest += rangeTest
    #                 i[index] = round(currValTest, 3)

    def classify(self):
        # READ TEST
        with open(self.folderPath + '/test.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(file)
            self.test_Data = list(reader)
        file.close()
        finalResults = []
        self.missingValues()

        # FILL MISSING VALUES
        self.fillEmptyValues('test')
        self.discretization(self.bind, "test")

        for line in self.test_Data:
            prob0 = 1
            prob1 = 1
            i = 0
            for att in line[:-1]:
                prob0 *= self.mEstimator(i, att, len(self.content)-1, self.content['class'][0])
                # print prob0
                prob1 *= self.mEstimator(i, att, len(self.content)-1, self.content['class'][1])
                i += 1
            mone = self.rowByIndex(len(self.content)-1).count(self.content['class'][0])
            # print float(float(self.rowByIndex(len(self.content)-1).count(self.content['class'][0])) /float(len(self.train_Data)))
            prob0 = prob0 * float(float(self.rowByIndex(len(self.content)-1).count(self.content['class'][0])) /float(len(self.train_Data)))
            # print (prob0)
            prob1 = prob1 * float(float(self.rowByIndex(len(self.content)-1).count(self.content['class'][1])) /float(len(self.train_Data)))
            # print prob1
            if (prob0 > prob1):
                finalResults.append(self.content['class'][0])
                # print(self.content['class'][0])
            else:
                finalResults.append(self.content['class'][1])
                # print(self.content['class'][1])
        with open(self.folderPath + '/output.txt', 'w+') as resFile:
            for idx, result in enumerate(finalResults):
                resFile.write(str(idx) + " " + result + "\n")


    def mEstimator(self, attIndex, attValue, classIndex, classValue):
        m = 2
        # print (m)
        nc = self.ncValue(attIndex, attValue, classIndex, classValue)
        # print (float((len(self.content[self.attIndexes.keys()[self.attIndexes.values().index(attIndex)]]))))
        p = 1 / float((len(self.content[self.attIndexes.keys()[self.attIndexes.values().index(attIndex)]])))
        # print ("p: "+ str(p))
        n = self.rowByIndex(classIndex).count(classValue)
        # print ("n: " + str(n))
        # print (float(float(nc + float(m * p)) / float(n + m)))
        return float(float(nc + float(m * p)) / float(n + m))


    def ncValue(self, attIndex, attValue, classIndex, classValue):
        counter = 0
        for line in self.train_Data:
            if (line[attIndex] == attValue and line[classIndex] == classValue):
                counter += 1

        return counter


NB = NaiveBayes()

NB.build("C:/ass4", 100)
NB.classify()
