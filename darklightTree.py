from collections import defaultdict

class BinaryTree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

def createTree(patientTree, patientId):
    inits = patientId
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    patientTree.leftChild = BinaryTree(inits)
    patientTree.leftChild.leftChild = BinaryTree (list1)
    patientTree.leftChild.rightChild = BinaryTree (list2)
    patientTree.rightChild = BinaryTree (inits)
    patientTree.rightChild.leftChild = BinaryTree (list3)
    patientTree.rightChild.rightChild = BinaryTree (list4)
def build_tree(patientTree, light , eyetype, line):
    # print(eyetype,light, patientTree.key)
    # point = None
    # if eyetype == "L":
    #     print("left")
    #     point = patientTree.leftChild
    # elif eyetype == "R":
    #     print("right")
    #     point = patientTree.rightChild
    # if light == "D":
    #     print("dark")
    #     point = patientTree.rightChild
    # elif light == "L":
    #     print("light")
    #     point = patientTree.leftChild
    if eyetype =="L" and light =="D":

        patientTree.leftChild.rightChild.key.append(line.strip("\n"))
        # print("LD",len(patientTree.leftChild.rightChild.key))
    elif eyetype == "L" and light == "L":
        patientTree.leftChild.leftChild.key.append (line.strip ("\n"))
    elif eyetype == "R" and light == "L":
        patientTree.rightChild.leftChild.key.append (line.strip ("\n"))
    elif eyetype == "R" and light == "D":
        patientTree.rightChild.rightChild.key.append (line.strip ("\n"))
    # point.key.append(line.strip("\n"))
    # print(len(point.key))
class create_pairs():
    def __init__(self, path):
        self.filenamepath = path
        self.patient_tree = BinaryTree
        self.dicts = defaultdict(list)

    def generateInfo(self):
        f = open(self.filenamepath,"r")
        f2 = open("I:/asoct/eyeId.txt", "a")
        patientIdlist = []
        for line in f.readlines():
            print(line)
            # self.personID = line.split("-")[0]+"-"+line.split("-")[1]
            # self.lightType = line.split("-")[2].split("_")[0]
            # self.patientDate = line.split("_")[1]+"_"+line.split("_")[2]
            # self.eyeType = line.split("_")[3]
            # self.deviceType = line.split("_")[4]
            # self.volumeIndex = line.split("_")[-1].strip(".jpg\n")
            # self.scanType = line.split("_")[-2]
            personID = line.split("-")[0]+"-"+line.split("-")[1]
            lightType = line.split("-")[2].split("_")[0]
            patientDate = line.split("_")[1]+"_"+line.split("_")[2]
            eyeType = line.split("_")[3]
            deviceType = line.split("_")[4]
            volumeIndex = line.split("_")[-1].strip(".jpg\n")
            scanType = line.split("_")[-2]

            # patientId = personID+"_"+patientDate
            patientId = personID
            eyeId = (patientId, eyeType)
            ###
            # if patientId+eyeType not in patientIdlist:
            #     patientIdlist.append(patientId+eyeType)
            #     f2.writelines(patientId+eyeType+"\n")
            # print(eyeId)



            ####
            # if self.dicts[patientId] != []:
            #     print("already built")

            if self.dicts[patientId] == []:
                inits =  patientId
                self.dicts[patientId] = BinaryTree(inits) ###
                createTree(self.dicts[patientId], patientId)
            build_tree(self.dicts[patientId], lightType, eyeType, line)
            # print(self.personID)
            # print(self.lightType)
            # print(self.patientDate)
            # print(self.eyeType)
            # print(self.deviceType)
            # print(self.volumeIndex)
            # print(self.scanType)
            # print(personID)
            # print(lightType)
            # print(patientDate)
            # print(eyeType)
            # print(deviceType)
            # print(volumeIndex)
            # print(scanType)
        # print(len(patientIdlist))
# if __name__ == '__main__':
#     path = "I:/octdata/val.txt"
#     create_pair = create_pairs(path)
#     create_pair.generateInfo()
#     # print(create_pair.dicts["CS-218_20190614_154507"].leftChild.leftChild.key)
#     # print(create_pair.dicts["CS-218"].rightChild.leftChild.key[:10])
#     print(len(create_pair.dicts["CS-176"].rightChild.leftChild.key))
#     print(create_pair.dicts["CS-176"].rightChild.leftChild.key)
#     print(create_pair.dicts["CS-176"].rightChild.rightChild.key)
#     # print(create_pair.dicts["CS-218"].rightChild.leftChild.key[:10])
