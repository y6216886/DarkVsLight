import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from models import ConvColumn6
from DataLoader import  loadImg
def train(pathlist):
    gpus = [0]
    device = torch.device ("cuda")
    model = ConvColumn6(12)
    model = torch.nn.DataParallel (model, device_ids=gpus).to (device)
    # model.train ()
    imgs = []
    model.eval()
    for filename in pathlist:
        imgTemp = loadImg("/home/yangyifan/data/DB18slices/demodata/" + filename)
        imgTemp = imgTemp.resize((84,84))
        imgTemp = np.array (imgTemp)
        # imgTemp.resize((1,imgTemp.shape[0],imgTemp.shape[1],imgTemp.shape[2]))
        # print("dimension", imgTemp.shape)
        # imgs.append(imgTemp)

        imgTemp = torch.from_numpy (imgTemp)
        imgs.append (torch.unsqueeze (imgTemp, 0))
    # print()
    # imgRes = np.concatenate (([img for img in imgs]), axis=0)
    imgs = torch.cat(imgs)
    print("after cat",imgs.shape)
    imgs = imgs.permute (3, 0, 1, 2)

    # imgRes.resize((1,imgRes.shape[0],imgRes.shape[1], imgRes.shape[2],imgRes.shape[3]))
    # imgs = torch.from_numpy (imgRes)
    imgs = imgs.float ()
    print(imgs.type())
    imgs.resize_((1,int(imgs.shape[0]),int(imgs.shape[1]), int(imgs.shape[2]),int(imgs.shape[3])))
    print ("imgsss", imgs.shape)
    imgs = imgs.to(device)
    output1 = model(imgs)
    print (output1.shape)
    print(output1)