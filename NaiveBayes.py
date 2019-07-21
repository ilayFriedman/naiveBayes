import csv
from collections import Counter

class NaiveBayes:
    def build(self,folderPath):
        self.folderPath = folderPath

        #readDATA
        with open(self.folderPath+'/train.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(file)
            self.train_Data = list(reader)
        file.close()

        #readContent
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

    def fillEmptyValues(self):
        for line in self.train_Data:
            includeEmptyCell = '' in line
            while(includeEmptyCell):
                indexEmpty = line.index('')
                #print(indexEmpty)
                if(self.content[self.attIndexes.keys()[self.attIndexes.values().index(indexEmpty)]] == 'NUMERIC'):
                    print('NUMBERCC')
                    line[indexEmpty] = "#"
                else:
                    print("no!")
                    line[indexEmpty] = "#"
                includeEmptyCell = '' in line

    def missingValues(self):
        self.missValues ={}
        for att in self.attIndexes.items():
            if (self.content[self.attIndexes.keys()[self.attIndexes.values().index(att[1])]] == 'NUMERIC'):
                rowList = self.rowByIndex(att[1])
                print (sum)
                self.missValues[att[1]] = "NUMERIC"
            else:
                self.missValues[att[1]] = "NO"

        print (self.missValues)


    def rowByIndex(self,index):
        rowInIndex=[]
        for line in self.train_Data:
            rowInIndex.append(line[index])
        return rowInIndex


NB = NaiveBayes()

NB.build("D:/documents/users/ilayfri/Downloads")
NB.missingValues()