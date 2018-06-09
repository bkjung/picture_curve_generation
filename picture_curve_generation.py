#!/usr/bin/env python

import time
import os
import sys
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt

class PictureCurve():
    def __init__(self):
        self.img = cv2.imread("image_edge.jpg", cv2.IMREAD_COLOR)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.y_size, self.x_size = self.img_gray.shape
        print(self.x_size, self.y_size)

        self.img_data = []
        for i in range(len(self.img_gray)):
            row_data = []
            for j in range(len(self.img_gray[i])):
                if self.img_gray[i][j]>=128:
                    row_data.append(1)
                else:
                    row_data.append(0)
            self.img_data.append(row_data)

        print("Image Loaded")

    def generate(self):
        #Phase-1 START
        #salt point
        salt_cnt = 0
        for i in range(len(self.img_data)):
            for j in range(len(self.img_data[i])):
                if self.img_data[i][j]==1:
                    if self.connect(8, i, j)==0:
                        salt_cnt = salt_cnt+1
                        self.img_data[i][j]=1
                        self.img[i][j]=[255,255,255]
                    else:
                        pass
                else:
                    pass
        print("Number of Salt Points = "+str(salt_cnt))
        print("Salt Point Deleted")

        #branch point
        branch_cnt = 0
        for i in range(len(self.img_data)):
            for j in range(len(self.img_data[i])):
                if self.img_data[i][j]==1:
                    if self.connect(4, i, j)>2:
                        branch_cnt = branch_cnt+1
                        self.img_data[i][j]=1
                        self.img[i][j]=[255,255,255]
                else:
                    pass
        print("Number of Branch Points = "+str(branch_cnt))
        print("Branch Point Deleted")
        #Phase-1 END


        #Phase-2 START

        #Phase-2 END

        cv2.imwrite('image_phase1.jpg', self.img)

    def connect(self, num, i, j):
        if i==0 or j==0 or i==self.y_size-1 or j==self.x_size-1:
            return -1
        else:
            p = []
            p.append(self.img_data[i-1][j])  #P1
            p.append(self.img_data[i][j+1])  #P2
            p.append(self.img_data[i+1][j])  #P3
            p.append(self.img_data[i][j-1])  #P4
            p.append(self.img_data[i-1][j+1])    #P5
            p.append(self.img_data[i+1][j+1])    #P6
            p.append(self.img_data[i+1][j-1])    #P7
            p.append(self.img_data[i-1][j-1])    #P8

            return sum(p[:num])

if __name__ == "__main__":
    try:
        pc = PictureCurve()
        pc.generate()

    except Exception as e:
        print(e)
        sys.exit(1)
