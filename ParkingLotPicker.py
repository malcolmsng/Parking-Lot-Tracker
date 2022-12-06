import cv2
import pickle

# img = cv2.imread("parking-lot.png")

width, height = 40, 80
positionList = []

try:
    with open("CarparkPosition", "rb") as f:
        positionList = pickle.load(f)
except:
    positionList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        print(x)
        print(y)
        positionList.append((x,y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(positionList):
            x1,y1 = pos
            if x1 <x < x1+width and y1 < y < y1 + height:
                positionList.pop(i)

    with open("CarparkPosition", "wb") as f:
        pickle.dump(positionList, f)
        
        
while True:
    
    img = cv2.imread("carpark-image.png")
    for pos in positionList:
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.imwrite("boxes.jpg", img)
    cv2.waitKey(1)