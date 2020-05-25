import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorboard as tb
import PIL
import os
import cv2
from tqdm import tqdm
import random
Path1=input("Enter Path Of Image")
class Downgrade():
    '''
    This is the class to downsample the dataset. It adds various type of noises in the data.
    All of its methods just require an opencv Image as an input and returns a noisy image.
    '''

    def __init__(self):
        pass

    def rndm_noise(self, img):
        '''
        This Method randomly chosses the noises from an available set of noises and apply to the Image.
        Parameters: opencv image
        '''
        lst = [self.gausian,
               self.snp,
               self.poisson,
               self.sp]
        rnd = np.random.randint(1, 2)
        for i in range(rnd):
            img = random.choice(lst)(img)
        return img

    def gausian(self, img):
        '''
        It adds random gausian noise to the image
        '''
        row, col = img.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col))
        gauss = gauss.reshape(row, col)
        noisy = img + gauss
        return noisy

    def snp(self, img):
        '''
        It adds salt and pepper noise to the image
        '''
        prb = np.random.uniform(0, 0.05)
        otpt = np.zeros(img.shape, dtype=np.uint8)
        thres = 1 - prb
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                rnd = random.random()
                if rnd < prb:
                    otpt[i][j] = 0
                elif rnd > thres:
                    otpt[i][j] = 255
                else:
                    otpt[i][j] = img[i][j]
        return otpt

    def poisson(self, img):
        '''
        It adds poissons noise to the image.
        '''
        lam = np.random.randint(10, 40)
        noise = np.random.poisson(lam, img.shape)
        output = img + noise
        return output

    def sp(self, img):
        '''
        It adds Speckle noise to the Image.
        '''
        prob = np.random.uniform(0.01, 0.05)
        output = np.zeros(img.shape, np.uint8)
        thres = 1 - prob
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                rnd = random.random()
                if rnd < prob:
                    output[i][j] = 128
                    for k in range(5):
                        output[i - k][j - k] = 128 + 10 * rnd
                else:
                    output[i][j] = img[i][j]
        return output
#We have to change this path. It will be fixed according to the system.
path1 = input("Enter Path 1")

noisy1 = []
orgnl1 = []
agmt = Downgrade()
a = 0
for s in tqdm(os.listdir(path1)):
  pht = cv2.imread(os.path.join(path1, s), 0)
  orgnl1.append(pht)
  img = agmt.rndm_noise(pht)
  noisy1.append(img)
  a+=1

  wpath1 = 'D:\Volume D\STUDY\ml project\downgraded images'
  #WE MUST CHANGE WPATH1 ACCORDING TO SYSTEM WE SHOW PROGRAM IN
  name = '1'
  #We have to change this variable 'name' according to the name of the file we are processing. 
  for q in tqdm(noisy1):
      img = PIL.Image.fromarray((q).astype(np.uint8))
      img.save(os.path.join(wpath1, name) + '.jpeg')
      name = str(int(name) + 1)
