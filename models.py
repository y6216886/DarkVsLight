import torch
import torch.nn as nn
from PIL import Image
import numpy as np

class ConvColumn6 (nn.Module):

    def __init__(self, numclass):
        super (ConvColumn6, self).__init__ ()
        # self.img = img
        self.conv_layer1 = self._make_conv_layer (3, 32)
        self.conv_layer2 = self._make_conv_layer (32, 64)
        self.conv_layer3 = self._make_conv_layer (64, 124)
        self.conv_layer4 = self._make_conv_layer (124, 256)
        # self.conv_layer4 = nn.Conv3d (124, 256, kernel_size=(2, 3, 1), padding=0)
        self.conv_layer5 = nn.Conv3d (256, 512, kernel_size=(1, 3, 3), padding=0)
        self.sigmoid = nn.Sigmoid()
        self.fc5 = nn.Linear (512, 512)
        self.relu = nn.LeakyReLU ()
        self.batch0 = nn.BatchNorm1d (512)
        self.drop = nn.Dropout (p=0.15)
        self.fc6 = nn.Linear (512, 256)
        self.relu = nn.LeakyReLU ()
        self.batch1 = nn.BatchNorm1d (256)
        self.maxpool3d = nn.MaxPool3d((3, 3, 1))
        self.drop = nn.Dropout (p=0.15)
        self.fc7 = nn.Linear (256, numclass)

    def _make_conv_layer(self, in_c, out_c):
        conv_layer = nn.Sequential (
            nn.Conv3d (in_c, out_c, kernel_size=(2, 3, 3), padding=0),
            nn.BatchNorm3d (out_c),
            nn.LeakyReLU (),
            nn.Conv3d (out_c, out_c, kernel_size=(2, 3, 3), padding=1),
            nn.BatchNorm3d (out_c),
            nn.LeakyReLU (),
            nn.MaxPool3d ((2, 2, 2)),
        )
        return conv_layer

    def forward(self, x):
        # x=self.img
        print("before 1", x.size())
        x = self.conv_layer1 (x)
        print("after 1", x.size())
        x = self.conv_layer2 (x)
        print("after 2",x.size())
        x = self.conv_layer3 (x)
        print("after 3",x.size())
        x = self.conv_layer4 (x)
        print("after 4", x.size())
        x = self.conv_layer5 (x)
        print("after 5",x.size())
        x = self.maxpool3d(x)
        print ("after pool", x.size ())
        x = x.view (x.size (0), -1)
        x = self.fc5 (x)
        x = self.relu (x)
        print ("before batch0", x.size ())
        x = self.batch0 (x)
        x = self.drop (x)
        x = self.fc6 (x)
        x = self.relu (x)
        x = self.batch1 (x)
        x = self.drop (x)
        # x1 = x
        x = self.fc7 (x)
        x=self.sigmoid(x)
        return x