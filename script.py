try:
    import sys
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
    Path1='public/images'
    name = sys.argv[1]
    #path1 = 'D:\Volume D\STUDY\ml project\original images'
    #path1 updated,it needs to be changed according to system
    agmt = Downgrade()

    orgnl = cv2.imread(os.path.join(Path1, name), 0)
    print("image loaded")

    noisy = agmt.rndm_noise(orgnl)
    print("noise added")

    wpath1 = 'public/images'
    img = PIL.Image.fromarray((noisy).astype(np.uint8))
    svname = 'noisy_' + name 
    img.save(os.path.join(wpath1, svname))

    print("noisy image saved")

except:
    print("There is some error in the script")
