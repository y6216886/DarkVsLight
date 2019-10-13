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
    df = pd.read_csv (path, encoding="cp1252")
    label_df = df.set_index ("Code")  ##using userId to search for clock
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
        imgs.append(loadImg("I:\lightVsDark_jpg\\full_version\jpg_D\\"+path))
    return imgs

def labelBatchLoader(userId, label_df, eyeType):
    if eyeType =="L":
        clock = label_df.loc[userId, 'Osclock']
    elif eyeType =="R":
        clock = label_df.loc[userId, 'Odclock']
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
            userID = self.eyeId[self.index][0:-2] .split("_")[0] ##eyeId = (userId, eyeType)
            eyeType  =self.eyeId[self.index][-1]
            print("userId", userID, eyeType)
            dltree = self.dlpair.dicts[userID]
            Exsist = checkpairs(dltree, eyeType)
            if Exsist:
                print("next")
                break
            else:
                print("not exsist")
                self.index +=1
        light_path =[]
        dark_path = []
        print("load path")
        if eyeType =="L":
            light_path = dltree.leftChild.leftChild.key
            dark_path = dltree.leftChild.rightChild.key
        elif eyeType =="R":
            light_path = dltree.rightChild.leftChild.key
            dark_path = dltree.rightChild.rightChild.key
        darkImgs = imgBatchLoader(light_path)  ##add transform
        lightImgs = imgBatchLoader(dark_path)
        labels = labelBatchLoader(userID, self.label_df, eyeType)

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
    filename_path = "I:\octdata\\brightVsDark_label/modified.txt"
    eyeId_path = "I:/octdata/eyeId.txt" ##to do list
    label_dir = "I:\octdata\\brightVsDark_label\\brightVsDarkLabels_v1.csv"
    darkImgs, lightImgs, labels =pairloader(filename_path, eyeId_path, label_dir)##    def __init__(self, filename_path, eyeId_path, label_dir):
    print(len(darkImgs))
