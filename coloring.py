#!/usr/bin/env python
import time
import os
import sys
import math
import numpy as np
import cv2
import copy
import random

def eraseSmallBlob( img):
    img_copy=copy.deepcopy(img)
    for i in range(len(img)):        
        for j in range(len(img[i])):
            if img_copy[i][j]>220:
                checkList=[[i,j]]
                tmpList=[[i,j]]
                elemCnt=0
                grayScaleSum=0
                img_copy[i][j]=255

                while len(checkList)!=0:
                    a,b=checkList[0]
                    if a+1<len(img_copy) and img_copy[a+1][b]>220:
                        checkList.append([a+1, b])
                        tmpList.append([a+1, b])
                        img_copy[a+1][b]=0
                    if a>0 and img_copy[a-1][b]>220:
                        checkList.append([a-1,b])
                        tmpList.append([a-1, b])
                        img_copy[a-1][b]=0
                    if b+1<len(img_copy[a]) and img_copy[a][b+1]>220:
                        checkList.append([a,b+1])
                        tmpList.append([a, b+1])
                        img_copy[a][b+1]=0
                    if b>0 and img_copy[a][b-1]>220:
                        checkList.append([a,b-1])
                        tmpList.append([a, b-1])
                        img_copy[a][b-1]=0
                    checkList=checkList[1:]
                    elemCnt=elemCnt+1
                    grayScaleSum+=img[a][b]

                grayScaleSum=grayScaleSum/elemCnt
                color=random.randrange(0,256)
                for a,b in tmpList:
                    # img[a][b]=grayScaleSum
                    #### DEBUG
                    img[a][b]=color
    return img
                    

if __name__ == "__main__":
    img=cv2.imread("33964.jpg", cv2.IMREAD_COLOR)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_colored=eraseSmallBlob(img_gray)
    cv2.imshow("colored img", img_colored)
    cv2.waitKey(0)
