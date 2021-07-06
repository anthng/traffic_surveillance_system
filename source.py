import cv2
import numpy as np
import time
import datetime
import math
from utils import preprocessing, enhancement, speed_estimation, countVehicles

try:
    #video = cv2.VideoCapture('./video/01.mp4')
    #video = cv2.VideoCapture('./video/03.mp4')
    video = cv2.VideoCapture('./video/best')
except Exception as e:
    print("\nCheck path to video file\n")

BLACK = (0,0,0)
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
PINK = (255, 0, 255)
YELLOW = (0,255,255)
WHITE = (255,255,255)
LIGHT_BLUE = (255,255,0)

WIDTH = 640; HEIGHT = 480

W = video.get(3)
H = video.get(4)
#print(W,H)

line_down = int(4*(H/5))
line_center = int(5*(H/5))
line_up = int(1*(H/5))

frame_area = (W*H)
MAX_AREA = frame_area/250
print("MAX_AREA: ",MAX_AREA)
frames = 30
count = []

#print(line_down, line_up)

fgbg = cv2.createBackgroundSubtractorMOG2()

def tracking():
    while(video.isOpened):
        start_time = time.time()
        _, frame = video.read()
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        if _ == True:
            #mask = fgbg.apply(frame)
            mask = preprocessing(frame.copy(),fgbg)

            #RETR_EXT: chỉ lấy các đường viền cực bên ngoài.
            # cv.CHAIN_APPROX_SIMPLE (only 4 points).
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            cx = 0
            cy = 0
            for c in contours:
                area = cv2.contourArea(c)
                #print("CountourArea: ",area)
                #line_up_Red
                cv2.line(frame, (0, line_down), (int(W), line_down), RED, 2)

                cv2.line(frame, (0, line_down-25), (int(W), line_down-25), YELLOW, 2)
                cv2.line(frame, (0, line_up), (int(W), line_up), BLUE, 2)
                
                #if area from 4 point is very low (means that area from cv2.contourArea < MAX_AREA)
                #next
                if area>MAX_AREA:
                    # compute the center of the contours. Calculates all of the moments up to the third order of a polygon or rasterized shape.

                    centroid=cv2.moments(c)
                    cx=int(centroid['m10']/centroid['m00'])
                    cy=int(centroid['m01']/centroid['m00'])

                    (x,y,w,h) = cv2.boundingRect(c)

                    #cv2.circle(frame,(cx,cy),5,RED,-1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 2)
                    

                    if countVehicles(cy, line_down-23, line_down-0.001):
                        count.append(1)

            end_time = time.time()
            #calculate fps
            if not (end_time == start_time):
                fps = 1.0/(end_time - start_time)
            
            velocity = speed_estimation(cx,cy,int(W),line_down, fps)
            #print(int(velocity))
            cv2.putText(frame, "{:.2f} km/h".format(velocity), (cx, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, LIGHT_BLUE, 2)
            cv2.putText(frame, "FPS: {}".format(str(int(fps))), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, YELLOW, 2)
            
            #count label
            cv2.putText(frame, "COUNT: {}".format(str(len(count))), (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, LIGHT_BLUE, 2)

            timestamp = datetime.datetime.now()
            timest = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
            cv2.putText(frame, timest, (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)

            #show mask to debug
            #cv2.imshow('Frame', mask)      
            cv2.imshow('Detection and Tracking', frame)
            
            #esc to quit
            if cv2.waitKey(33) == 27:
        	    break
        else:
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    tracking()
