import cv2
import pickle
width, height = (70-22), (160-129)

# Check whether there are any position already inside the file if not then returns the empty list
try:
    with open('CarParkPos','rb') as f:
        poslist = pickle.load(f)
except:
    poslist=[]

# Created a function to get the position of the parking spot
def mouseClick(event,x,y,flags,param):
    # This function gives the position of the click in x, y co-ordinates 
    if event == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    # This will check if that position is in the position list if there then remove it else pass
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, j in enumerate(poslist):
            x1,y1 = j
            # This checks whether the click is in the area of the rectangle then remove that image
            if x1<x<(x1+width) and y1<y<(y1+height):
                poslist.pop(i)
    # Saving all the positions marked inside a file
    with open('CarParkPos', 'wb') as f:
        pickle.dump(poslist, f)


# Running the Function and Image in a loop
while True:
    # Reading the image
    img = cv2.imread('carParkImg.png')
    # Resizing the image
    img = cv2.resize(img, (480, 480))
    # (img, start point (width(x axis), height(y axis), last point(width, height), color, thickness)
    img = cv2.rectangle(img, (22, 129), (70, 160), (255, 0, 0), 2)
    for i in poslist:
        cv2.rectangle(img,i,(i[0]+width, i[1]+height),(255,0,0),2)
    # Show the image 
    cv2.imshow('Park Image', img)
    # This function will set rectangle inside the image and save the position in the file as well in the showed image
    cv2.setMouseCallback('Park Image', mouseClick)
    cv2.waitKey(1)
