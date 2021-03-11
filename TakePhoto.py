import cv2
import os
import errno
from datetime import datetime
import pandas as pd
import serial
import math

com = "/dev/rfcomm0"

s = serial.Serial(com,
                  baudrate = 9600, 
                  parity=serial.PARITY_ODD, 
                  stopbits=serial.STOPBITS_TWO,
                  timeout=1)

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

path  = "/home/pi/Projects/images/"
imgList = []
steeringList = []

left_motor = 128
right_motor = 128
label = 0
photo_enabled = False

def getSteering():
    global s, left_motor, right_motor, label, photo_enabled
    if s.isOpen():
        if(s.in_waiting> 0):
            line = s.read(3)
            if(line[0] == 0xFF):
                left_motor = line[1]
                right_motor = line[2]
                label = int((left_motor - right_motor)/10)               
                label = min(label, 8) if (label > 0) else max(label, -8)               
                print(left_motor, right_motor, label)
            if(line[0] == 0xFE):
                if(line[2] != 0):
                    photo_enabled = True
                    print("Taking photos..")
                else:
                    photo_enabled = False
                    print("stoppped taking photos..")



def createImage(frame, path):
    global imgList, steeringList, label
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    filename = os.path.join(path, f'Image_{timestamp}.jpg')
    cv2.imwrite(filename, frame)
    #print("image printed")
    imgList.append(filename)
    steeringList.append(label)
    

def saveToCsv(path):
    rawData = {
        'Image': imgList,
        'Steering': steeringList
    }
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(path, f'log.csv'), index=False, header=False, mode='a')
    print('Log saved')

if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

#os.chdir(path)

while True:
    getSteering()

    k = cv2.waitKey(1)

    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

        
        
        #elif k%256 == 32:
            # SPACE pressed
    if(photo_enabled):
        createImage(frame, path)
    

    if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            saveToCsv(path)        
            break
        
cam.release()

cv2.destroyAllWindows()