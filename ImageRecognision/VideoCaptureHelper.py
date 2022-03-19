import cv2

def createVideoCapture(camerano = 0, frameWidth = 640, frameHeight = 480):
	cap = cv2.VideoCapture(camerano)
	cap.set(3, frameWidth)
	cap.set(4, frameHeight)
	return cap