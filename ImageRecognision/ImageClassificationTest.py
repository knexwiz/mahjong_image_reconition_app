import cv2
import os
import numpy as np
import VideoCaptureHelper
from ImgDescription import ImageDescription

TILE_SIZE = (90,120)
ORB_CLASSIFIER_PATH = "./ImageClassifiers"

cap = VideoCaptureHelper.createVideoCapture(camerano=1)

if cap is None:
	print("ERROR: Video Capture could not be started.\n")
	exit(1)


def CreateImgDictionary(path) -> list[ImageDescription]:
	dirlist = os.listdir(path)
	dictionary = []
	print("Loading Images (len %d):"  %(len(dirlist)))
	for dir in dirlist:
		img = cv2.imread("%s/%s" %(path, dir), cv2.IMREAD_COLOR)
		if img is None:
			continue

		filename = os.path.splitext(dir)[0]
		imgDesc = ImageDescription(img, filename)

		imgDesc.CreateHistogramDescription()
		imgDesc.CreateORBDescription()

		dictionary.append( imgDesc )

		print("\t" + filename)
	return dictionary

imgdict = CreateImgDictionary(ORB_CLASSIFIER_PATH)

while True:
	success, inputImage = cap.read()

	inputDesc = ImageDescription(inputImage)
	inputDesc.CreateORBDescription()
	inputDesc.CreateHistogramDescription()

	matches = inputDesc.GetORBMatches(imgdict)

	id = 0
	while id < 5 and matches[id].ORBFitness > 10:
		cv2.putText(inputImage, "%d -> %s :: %.2f" %(id, matches[id].name, matches[id].ORBFitness), \
			(50,50 + 30 * id), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
		id += 1
	if id == 0:
		cv2.putText(inputImage, "N/A", (50 + 30 * id,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)

	inputDesc.CreateContourDescription()
	inputDesc.FilterContoursByArea((100, TILE_SIZE[0] * TILE_SIZE[1]))
	inputDesc.FilterContoursByBoarder()
	cv2.drawContours(inputImage, inputDesc.contours, -1, (0,255,0), 1)

	if not matches[0].goods is None:
		temp1 = cv2.drawMatchesKnn(matches[0].grayImage, matches[0].kp, \
			inputDesc.grayImage, inputDesc.kp, matches[0].goods, None, flags=2)

	# cv2.rectangle(inputImage, (0,0), tilesize, (0,255,255), 3)

	outputImage = np.concatenate((inputImage, temp1), axis=1)
	temp = cv2.cvtColor(inputDesc.threshImage, cv2.COLOR_GRAY2BGR)
	temp = np.concatenate((temp, temp1), axis=1)
	outputImage = np.concatenate((outputImage, temp), axis=0)
	cv2.imshow("Result", outputImage)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
