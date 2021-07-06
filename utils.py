import cv2
import numpy as np
import math

def speed_estimation(x1,y1,x2,y2, fps):
    """
        Speed calculation is based on euclide-distance:
            euclide_dist^2 = (x_2 - x_1)^2 + (y_2 - y_1)^2 
            euclide_dist = sqrt( (x_2 - x_1)^2 + (y_2 - y_1)^2 )

        Frame rate: speed at which those images are loaded (denoted fps)
                    that means each second of video loads n different images
            
            1 m/s   =    3.6 km/h
            v       =    euclide_dist*3.6

            v = s*t/frame/t

            fps = frame/second
            t = 

            v = s/t

            v = s/(frame/fps)
            = (s*fps)/frame

            v = s*fps = m/s 
    """

    euclide_dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    #0.2 mat do chiem cho, 28.888 fps
    v = euclide_dist/2.77777 * 29.88888 * 3.6
    return (v*(1e-3)) - 1e-3

def countVehicles(y, thres1, thres2):
    if y >= thres1 and y <= thres2:
        return True
    return False

def goDown(y):
    if y >= 383 and y < 385:
        return True
    return False

def enhancement(img):
    # #convert BGR to gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #median blur: denoise good for salt and pepper noise,
    med_blur = cv2.medianBlur(gray, 5)
    #gaussian blur:
    gauss_blur = cv2.GaussianBlur(med_blur,(5,5),3)
    #convert gray to bgr
    img = cv2.cvtColor(gauss_blur,cv2.COLOR_GRAY2BGR)
    return img

def preprocessing(img, fgbg):
    kernelOp = np.ones((3,3),np.uint8)
    kernelOp2 = np.ones((5,5),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)
    
    """
    fgbg: Gaussian Mixture-based Background/Foreground Segmentation
                using to seperate background and fouregroud.
                Where:
                    backgroud: static obj
                    foregroud: dynamic obj
                Output:
                    Return: output foregroud mask that is a binary image.
    """
    img = enhancement(img)

    #Each frame is a image, we will seperate foregroud and backgroud to extract feature.
    mask = fgbg.apply(img)
    #convert to binary image to remove shadows
    ret,imBin=cv2.threshold(mask,200,255,cv2.THRESH_BINARY)
    #morph_open to remove noise
    mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernelOp)
    
    #morph_close to join white regions
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelCl)
    
    return mask





