import cv2
import pickle
import numpy as np
import cvzone

width, height = 40, 80
vid_width, vid_height = 640,360

with open("CarparkPosition", "rb") as f:
        positionList = pickle.load(f)

vid = cv2.VideoCapture("carpark-video.mp4")

out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 20.0, (vid_width, vid_height))
def checkParkingSpace(imgProcessed):
    
    totalNumLots = len(positionList)
    numAvailableLots = 0
    
    for pos in positionList:
        x, y = pos
        imgCrop = imgProcessed[y:y+height, x:x+width]
        
        # cv2.imshow(str(x*y), imgCrop)
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 4)

        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-5), scale=0.7, thickness=1, offset=0)
        
        if count < 500:
            # available lot
            color = (0,255,0)
            numAvailableLots += 1
        else:
            # occupied lot
            color = (0,0,255)
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), color, 4)
        
    numOccupiedLots = totalNumLots - numAvailableLots
    
    cvzone.putTextRect(img, "Available: " + str(numAvailableLots) + "/" + str(totalNumLots), (25,175), scale=2, thickness=2, offset=0, colorR=(0,255,0))

    

while vid.isOpened():
    if vid.get(cv2.CAP_PROP_POS_FRAMES) == vid.get(cv2.CAP_PROP_FRAME_COUNT):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = vid.read()
    
    if success == True: 
        img = cv2.resize(img, (vid_width, vid_height, ))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernal = np.ones((3,3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernal, iterations=1)
        checkParkingSpace(imgDilate)
        out.write(img)
        cv2.imshow("carpark", img)
        
    else:
        break
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
    
vid.release()
out.release()
cv2.destroyAllWindows()
    
    
    
