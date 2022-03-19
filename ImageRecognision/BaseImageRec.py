import cv2
import os

#################################################################

camerano = 1 # CAMERA NUMBER
frameWidth = 640 # DISPLAY WIDTH
frameHeight = 480 # DISPLAY HEIGHT
#################################################################

global cascades
cascades = []

def AddCasecade(xml, name, color, innerObject = False):
	if not os.path.exists(xml):
		print("ERROR: Cascade %s was not added because it does not exist." %(xml))

	if innerObject:
		innerObject[0] = cv2.CascadeClassifier(innerObject[0])
	
	cascades.append( (cv2.CascadeClassifier(xml), name, color, innerObject) )

cap = cv2.VideoCapture(camerano)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
	pass

# CREATE TRACKBAR
cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight+100)
cv2.createTrackbar("Scale","Result", 400, 1000, empty)
cv2.createTrackbar("Neig", "Result", 8, 20, empty)
cv2.createTrackbar("Min Area", "Result", 0, 100000, empty)
cv2.createTrackbar("Brightness", "Result", 180, 255, empty)

# AddCasecade(cv2.data.haarcascades + "haarcascade_frontalface_default.xml", "Face", (255, 0, 255),
# 	(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml", "Eyes", (255, 255, 0)) )

AddCasecade("./Saved_Haars/tileback.002.xml", "TileBack", (255, 0, 255))
AddCasecade("./Saved_Haars/south_wind.xml", "SouthWind", (0, 0, 255))


while True:
# SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
	cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
	cap.set(10, cameraBrightness)
	# GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
	success, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# DETECT THE OBJECT USING THE CASCADE
	scaleval = 1 + (cv2.getTrackbarPos("Scale", "Result") /1000)
	neig = cv2.getTrackbarPos("Neig", "Result")

	for (cascade, objName, color, inner) in cascades:
		objects = cascade.detectMultiScale(gray, scaleval, neig)

		# DISPLAY THE DETECTED OBJECTS
		for (x,y,w,h) in objects:
			area = w*h
			minArea = cv2.getTrackbarPos("Min Area", "Result")
			if area > minArea:
				cv2.rectangle(img, (x,y), (x+w,y+h), color, 3)
				cv2.putText(img, objName, (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
				# gray_crop = img[y:y+h, x:x+w]
	
	cv2.imshow("Result", img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyWindow("Image")