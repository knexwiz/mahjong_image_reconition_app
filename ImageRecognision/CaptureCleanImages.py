from operator import countOf
import numpy as np
import math
import cv2
import os
import time
#####################################################
myPath = 'data/000_UnmarkedImages'
cameraNo = 1
cameraBrightness = 190
moduleval = 25 # SAVE EVERY_ITH FRAME TO AVOID REPETITION
global minBlur # SMALLER VALUE MEANS MORE BLURRINESS PRESENT
minBlur = 310
global w_cropval
w_cropval = 200
global b_cropval
b_cropval = 20

grayImage = False # IMAGES SAVED COLORED OR GRAY
saveData = True # SAVE DATA FLAG
showImage = True # IMAGE DISPLAY FLAG
imgWidth = (int)(640/4)
imgHeight = (int)(480/4)

frameWidth = 640*4
frameHeight = 480*4

global countFolder
cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, cameraBrightness)

count = 0
countSave = 0

def saveDataFunc():
	if not os.path.exists(myPath):
		os.makedirs(myPath)
	return len(os.listdir(myPath))

countSave = saveDataFunc()

def empty(a):
	pass

def SetMinBlur(x):
	global minBlur
	minBlur = x

def SetWCrop(x):
	global w_cropval
	w_cropval = x

def SetBCrop(x):
	global b_cropval
	b_cropval = x

cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight+100)
cv2.createTrackbar("Current Blur","Result", minBlur, 1000, empty)
cv2.createTrackbar("Min Blur","Result", minBlur, 1000, SetMinBlur)
cv2.createTrackbar("White Crop","Result", w_cropval, 255, SetWCrop)
cv2.createTrackbar("Black Crop","Result", b_cropval, 255, SetBCrop)

while True:
	success, capimg = cap.read()
	img = capimg

	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# imgray = cv2.blur(imgray,(15,15))
	# ret,thresh = cv2.threshold(imgray,127, 255,0)
	# # dilated=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)))
	# contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# new_contours=[]
	# for c in contours:
	# 	# x,y,w,h = cv2.boundingRect(c)
	# 	# cv2.rectangle(capimg, (x,x+w), (y,y+h), (255,0,0), 1)
	# 	if cv2.contourArea(c)<4000000:
	# 		new_contours.append(c)
	
	# best_box=[-1,-1,-1,-1]
	# for c in new_contours:
	# 	x,y,w,h = cv2.boundingRect(c)
	# 	if best_box[0] < 0:
	# 		best_box=[x,y,x+w,y+h]
	# 	else:
	# 		if x<best_box[0]:
	# 			best_box[0]=x
	# 		if y<best_box[1]:
	# 			best_box[1]=y
	# 		if x+w>best_box[2]:
	# 			best_box[2]=x+w
	# 		if y+h>best_box[3]:
	# 			best_box[3]=y+h

	# if grayImage: img = imgray

	# cv2.drawContours(capimg, contours, -1, (0,255,0), 1)
	# cv2.drawContours(capimg, contours, 0, (255,0,0), 3)
	
	# img = img[best_box[0]:best_box[2], best_box[1]:best_box[3]]

	# if best_box[2] - best_box[0] < imgWidth or best_box[3] - best_box[1] < imgHeight:

	img = cv2.resize(capimg, (imgWidth, imgHeight))
	if saveData:
		blur = cv2.Laplacian(img, cv2.CV_64F).var()
		if count % moduleval == 0:
			cv2.setTrackbarPos("Current Blur","Result", (int)(blur) )
			if blur > minBlur:
				cv2.imwrite("%s/%d_%d_%s.png" %(myPath,
					countSave, blur, time.time()), img)
				countSave += 1
				count += 1
		else:
			count += 1

	if showImage:
		# cv2.rectangle(capimg, (best_box[0],best_box[2]), (best_box[1],best_box[3]), (255,0,255), 4)
		cv2.imshow("Result", capimg)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyWindow("Result")
