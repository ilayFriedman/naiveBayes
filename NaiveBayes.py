import csv
from collections import Counter

class NaiveBayes:
    def build(self,folderPath, bind):
        self.folderPath = folderPath

        #READ DATA
        with open(self.folderPath+'/train.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(file)
            self.train_Data = list(reader)
        file.close()

        #READ CONTENT
        with open(self.folderPath + "/Structure.txt", "r") as structureFile:
            self.content = {}
            self.attIndexes = {}
            attributes = structureFile.read().replace("\n", "").split("@ATTRIBUTE ")
            #print(attributes)
            i = 0
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
                        i += 1
            #print(self.content)
            #print(self.attIndexes)
        structureFile.close()


        # GET FILLED VALUES
        self.missingValues()

        # FILL MISSING VALUES
        self.fillEmptyValues()

        #discretization
        self.discretization(bind)


    def fillEmptyValues(self):

        for line in self.train_Data:
            includeEmptyCell = '' in line
            while(includeEmptyCell):
                # print (line)
                indexEmpty = line.index('')
                # print(indexEmpty)
                # if(self.content[self.attIndexes.keys()[self.attIndexes.values().index(indexEmpty)]] == 'NUMERIC'):
                #     print('NUMBERCC')
                #     line[indexEmpty] = "#"
                # else:
                #     print("no!")
                #     line[indexEmpty] = "#"
                line[indexEmpty] = self.missValues[indexEmpty]
                # print(line)
                includeEmptyCell = '' in line

    def missingValues(self):
        self.missValues ={}
        for att in self.attIndexes.items():
            if (self.content[self.attIndexes.keys()[self.attIndexes.values().index(att[1])]] == 'NUMERIC'):
                rowList = self.rowByIndex(att[1])
                self.missValues[att[1]] = str(round(sum(map(float,rowList)) / len(rowList),3))
            else:
                rowList = self.rowByIndex(att[1])
                self.missValues[att[1]] = Counter(rowList).most_common(1)[0][0]

        # print (self.missValues)


    def rowByIndex(self,index):
        rowInIndex=[]
        for line in self.train_Data:
            if(line[index] != ''):
                rowInIndex.append(line[index])
        return rowInIndex

    def discretization(self, bind):
        for att in self.content.items():
            if ('NUMERIC' in att[1]):
                print ('###')
                index = self.attIndexes[att[0]]
                self.train_Data.sort(key=lambda x: x[index])
                col = map(float, self.rowByIndex(index))
                mini = min(col)
                maxi = max(col)
                range = (maxi - mini) / bind
                currVal = round(mini + range, 3)
                j = 1
                for i in self.train_Data:
                    # min =
                    tmp = i[index]
                    if (float(i[index]) <= currVal):
                        i[index] = round(currVal, 3)
                    else:
                        currVal += range
                        while (float(i[index]) > currVal):
                            currVal += range
                        i[index] = round(currVal, 3)


NB = NaiveBayes()

NB.build("C:/Users/shororen/PycharmProjects/naiveBayes", 100)