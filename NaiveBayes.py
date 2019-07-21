import csv
class NaiveBayes:
    def build(self,folderPath):
        self.folderPath = folderPath

        #readDATA
        with open(self.folderPath+'/train.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            self.train_Data = list(reader)
        file.close()

        #readContent
        with open(self.folderPath + "/Structure.txt", "r") as structureFile:
            self.content = {}
            attributes = structureFile.read().replace("\n", "").split("@ATTRIBUTE ")
            #print(attributes)
            for att in attributes:
                start = att.find('{')
                key = att[:start - 1]
                values = att[start + 1:-1]
                values = values.split(",")
                if (start != -1):
                    self.content[key] = values
                else:
                    start = att.find('NUMERIC')
                    if (start != -1):
                        key = att.split(" ")[0]
                        self.content[key] = 'NUMERIC'
            #print(self.content)
        structureFile.close()

    def fillEmptyValues(self):
        for line in self.train_Data:
            if('' in line):
                missingIndex = line.index('')

        for at in self.content:








NB = NaiveBayes()

NB.build("D:/documents/users/ilayfri/Downloads")