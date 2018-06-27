#!/usr/bin/env python
import time
import os
import sys
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import copy

directory="./Daedongyeojido/"

class PictureCurve():
    def __init__(self):
        self.img = cv2.imread(directory+"Daedongyeojido-full.jpg", cv2.IMREAD_COLOR)
        self.y_size, self.x_size = self.img.shape[:2]
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.save_img=copy.deepcopy(self.img_gray)
        print(self.x_size, self.y_size)
        cv2.imwrite(directory+"map_gray.jpg", self.img_gray)

        self.img_data = []
        for i in range(len(self.img_gray)):
            row_data = []
            for j in range(len(self.img_gray[i])):
                if self.img_gray[i][j]>=200:
                    row_data.append(1)
                else:
                    row_data.append(0)
            self.img_data.append(row_data)

        print("Image Loaded")

    def generate(self):
		#branch point
        branch_cnt = 0
        print(len(self. img_data))
     	print(len(self.img_data[0]))
        for i in range(len(self.img_data)):
           for j in range(len(self.img_data[i])):
               if self.img_data[i][j]==1:
                   if self.connect(8, i, j)>=6:
                       branch_cnt = branch_cnt+1
                       self.img_data[i][j]=1
                       self.img_gray[i][j]=255
               else:
                   pass
        print("Number of Branch Points = "+str(branch_cnt))
        print("Branch Point Deleted")

        cv2.imwrite(directory+"branch_removed.jpg", self.img_gray)

	    #salt point
        salt_cnt=0
        for i in range(len(self.img_data)):
            for j in range(len(self.img_data[i])):
                if self.img_data[i][j]==0:
                    if self.connect(8, i, j)==8:
                        salt_cnt=salt_cnt+1
                        self.img_gray[i][j]=255
                    else:
                        pass
                else:
                    pass
        print("Number of Salt Points = "+str(salt_cnt))
        print("Salt Point Deleted")
        cv2.imwrite('image_phase_before.jpg', self.img_gray)
        #self.thinLineDetector()
        #self.eraseSmallBlob(self.img_gray)
        print(self.img.shape)
        cv2.imwrite(directory+'salt_removed.jpg', self.img_gray)

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

    def connect2(self, img, num, i, j):
        if i==0 or j==0 or i==self.y_size-1 or j==self.x_size-1:
            return -1
        else:
            p = []
            p.append(self.convert(img[i-1][j]))  #P1
            p.append(self.convert(img[i][j+1]))  #P2
            p.append(self.convert(img[i+1][j]))  #P3
            p.append(self.convert(img[i][j-1]))  #P4
            p.append(self.convert(img[i-1][j+1]))    #P5
            p.append(self.convert(img[i+1][j+1]))    #P6
            p.append(self.convert(img[i+1][j-1]))    #P7
            p.append(self.convert(img[i-1][j-1]))   #P8

        return sum(p[:num])
    
    def eraseSmallBlob(self, img):
        img_copy=copy.deepcopy(img)
        print(img_copy[20])
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img_copy[i][j]<220:
                    print("i,j:", i, j)
                    checkList=[[i,j]]
                    tmpList=[[i,j]]
                    elemCnt=0
                    img_copy[i][j]=255
                    while len(checkList)!=0:
                        a,b=checkList[0]
                        if a+1<len(img_copy) and img_copy[a+1][b]<220:
                            print("a", a+1, b)
                            checkList.append([a+1, b])
                            tmpList.append([a+1, b])
                            elemCnt=elemCnt+1
                            img_copy[a+1][b]=255
                        if a>0 and img_copy[a-1][b]<220:
                            print("b", a-1, b)
                            checkList.append([a-1,b])
                            tmpList.append([a-1, b])
                            elemCnt=elemCnt+1
                            img_copy[a-1][b]=255
                        if b+1<len(img_copy[a]) and img_copy[a][b+1]<220:
                            print("c", a, b+1)
                            checkList.append([a,b+1])
                            tmpList.append([a, b+1])
                            elemCnt=elemCnt+1
                            img_copy[a][b+1]=255
                        if b>0 and img_copy[a][b-1]<220:
                            print("d", a, b-1)
                            checkList.append([a,b-1])
                            tmpList.append([a, b-1])
                            elemCnt=elemCnt+1
                            img_copy[a][b-1]=255
                        checkList=checkList[1:]
                        elemCnt=elemCnt+1
                    print(elemCnt)
                    if elemCnt<50:
                        for a,b in tmpList:
                            img[a][b]=255
                            
                    


    def convert(self, data):
        if data<200:
            return 0
        else:
            return 1

    def thinLineDetector(self):
        print("DEBUG-0", len(self.img_gray), len(self.img_gray[1]))
        new_img=[]
        for i in range(len(self.img_gray)):
            new_row=[]
            for j in range(len(self.img_gray[i])):
                #if (self.connect(8, i, j)>=2) and (self.img_gray[i][j]>128 and self.img_gray[i][j]<250):
                if self.img_gray[i][j]>90 and self.img_gray[i][j]<230 and self.connect(8,i,j)>=7:
                    #self.img[i][j]=[0,0,0]
                    # new_row.append([self.save_img[i][j], self.save_img[i][j], self.save_img[i][j]])
                    new_row.append(self.img_gray[i][j])
                else:
                    #pass
                    new_row.append(255)
            new_img.append(new_row)
        new_img=np.array(new_img)
        cv2.imwrite("thinline.jpg", new_img)
        salt_cnt=0

        #Salt Point
        for i in range(len(new_img)):
            for j in range(len(new_img[i])):
                if new_img[i][j]<130:
                    if self.connect2(new_img, 8, i, j)==8:
                        salt_cnt=salt_cnt+1
                        new_img[i][j]=255
                    else:
                        pass
                else:
                    pass
        print("salt_cnt:", salt_cnt)
        new_img=np.array(new_img, dtype='i')

        blur=cv2.blur(new_img, (10,10))
        cv2.imwrite("thinline2.jpg", new_img)



if __name__ == "__main__":
    try:
        pc = PictureCurve()
        pc.generate()

    except Exception as e:
        print(e)
        sys.exit(1)
