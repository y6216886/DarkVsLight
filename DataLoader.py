import torch
import torch.nn as nn
from PIL import Image
import pandas as pd
import torch.utils.data as data
import numpy as np
from darklightTree import *


def loadImg(path):
    img = Image.open(path).convert("RGB")
    return img



def readfilename(path):
    lines=[]
    for line in open(path):
        lines.append(line)
    return lines

def get_label(path):
    label_df = pd.read_csv(path)
    label_df = label_df.set_index("userId")  ##using userId to search for clock
    return label_df

def checkpairs(dicts, eyeType): ##dicts = create_pair.dicts[userId]
    # if dicts.leftChild.leftChild.key !=[] and dicts.leftChild.rightChild.key !=[]:  ##judge if left eye exsist pairs
    #     leftExsist =  True
    # else :
    #     leftExsist = False
    # if dicts.rightChild.leftChild.key != [] and dicts.rightChild.rightChild.key != []:##judge if left eye exsist pairs
    #     rightExsist =True
    # else:
    #     rightExsist =False
    Exsist = False
    if eyeType =="L":
        if dicts.leftChild.leftChild.key !=[] and dicts.leftChild.rightChild.key !=[]:
            Exsist = True
    elif eyeType =="R":
        if dicts.rightChild.leftChild.key != [] and dicts.rightChild.rightChild.key != []:
            Exsist =True
    return Exsist

def imgBatchLoader(pathList):
    imgs = []
    for path in pathList:
        imgs.append(loadImg(path))
    return imgs

def labelBatchLoader(userId, label_df):
    clock = label_df.loc[userId, 'clock']
    return clock

class pairloader(data.Dataset):
    def __init__(self, filename_path, eyeId_path, label_dir):
        self.dlpair = create_pairs(filename_path)
        self.dlpair.generateInfo()      ###demo : print(create_pair.dicts["CS-218_20190614_154507"].leftChild.leftChild.key)
        self.eyeId = readfilename(eyeId_path)   ##a list with (userId, eyeType) in each line    e.g. userId = "CS-218_20190614_154507"  eyeType = left
        self.index = 0   ##index for userId
        # self.transforms = transform
        self.loader = loadImg
        self.label_df = get_label(label_dir)

    def __getitem__(self, index):
        while 1:
            userID = self.eyeId[self.index][0:-2]  ##eyeId = (userId, eyeType)
            eyeType  =self.eyeId[self.index][-1]
            dltree = self.dlpair.dicts[userID]
            Exsist = checkpairs(dltree)
            if Exsist:
                break
            else:
                self.index +=1
        light_path =[]
        dark_path = []
        if eyeType =="L":
            light_path = dltree.leftChild.leftChild.key
            dark_path = dltree.leftChild.rightChild.key
        elif eyeType =="R":
            light_path = dltree.rightChild.leftChild.key
            dark_path = dltree.rightChild.rightChild.key
        darkImgs = imgBatchLoader(light_path)  ##add transform
        lightImgs = imgBatchLoader(dark_path)
        labels = labelBatchLoader(userID, eyeType)

        return (darkImgs, lightImgs, labels)
        # if left&right:
        #     left_light_path = dltree.leftChild.leftChild.key
        #     left_light_path = dltree.leftChild.leftChild.key
        #     right_light_path = dltree.rightChild.leftChild.key
        #     right_dark_path = dltree.rightChild.rightChild.key
        #     return 0
        # elif left:
        #     return 0
        # elif right :
        #     return 0
        # else:
        #     index+=1
    def __len__(self):
        return len(self.eyeId)



if __name__ == '__main__':
    filename_path = "I:/octdata/val.txt"
    eyeId_path = "I:/octdata/eyeId.txt" ##to do list
    label_dir = ""
    pairloader(filename_path, eyeId_path, label_dir)##    def __init__(self, filename_path, eyeId_path, label_dir):

