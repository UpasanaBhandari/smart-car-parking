import cv2
import numpy as np
import cvzone
import pickle

width, height = (70-22), (160-129)

# Get all the postions of all the positions marked
with open('CarParkPos','rb') as f:
    poslist = pickle.load(f)
f.close()
# Loading the video 
cap = cv2.VideoCapture('carPark.mp4')

# This function takes an image as input 
def cropimg(imgpro):
    spacecount = 0
    # Loops through the positions
    for i in poslist:
        x,y = i
        # Crops the postions from the image inorder to count the contours in each spot or position
        imgcrop = imgpro[y:y+height, x:x+width]
        
        # Resize the cropped image
        imgcrop = cv2.resize(imgcrop,(width, height),3)
        # cv2.imshow(str(x*y), imgcrop)

        # This counts the countors for the cropped image
        count = cv2.countNonZero(imgcrop)
        
        # This will print a text on the original image with a contour count 
        cvzone.putTextRect(img,str(count),(x, y+height-2),scale=1, thickness=2, offset=0, colorR=(0,0,255))

        # If the count is less than 170 then the car is not parked in that postion
        if count < 170:
            color = (0,255,0)
            thickness = 2
            spacecount +=1
        else:
            color = (0,0,255)
            thickness = 1
        
        # Finally we put the respective color and thickness on the original image
        cv2.rectangle(img, i, (i[0] + width, i[1] + height), color, thickness)
        
        # Put a text of total count of parkings on the whole image 
        cvzone.putTextRect(img,f' Free: {str(spacecount)}/{len(poslist)}',(120,40),scale=2, thickness=2, offset=5, colorR=(0,255,0))

while True:
    # This is to run the video on loop
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    
    # Resizing the images
    img = cv2.resize(img, (480,480))
    
    # Converting the image into greyscale reduces the contours to 522(for filled places)
    imggrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Applying the blur on the image reduces the contours to 458(for filled places)
    imgblur = cv2.GaussianBlur(imggrey, (3,3), 1)
    
    # Applying the thresholding on the image but doesnot have any change in contour count(for filled places)
     # here we are using gaussian mean of 25 neighbors to calculate the threshold value for each pixel.
    thresh = cv2.adaptiveThreshold(imgblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,25,16)# 16 is a value to be subtracted from the threshold value to get a fine tuned operation.
   
    # Applying the median blur on the image reduces the contours to 252(for filled places)
    median = cv2.medianBlur(thresh, 5)
    
    # Creating the kernel of 3x3 size with the input data type as 8-bit unsign int
    kernel = np.zeros((3,3),np.uint8)
    
    # Dialating the images with median using 3x3 kernel reduces the contours by 236(for filled places)
    imgdial = cv2.dilate(median, kernel, iterations=1)
    
    # Cropping the preproccessed image and counting the contours 
    cropimg(imgdial)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cap.release()
cv2.destroyAllWindow()
