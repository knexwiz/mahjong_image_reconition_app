from re import I
import cv2
import os
import numpy as np
import random
import VideoCaptureHelper
from ImgDescription import ImageDescription
import ImgDescription

TILE_SIZE = (75,100)
ORB_CLASSIFIER_PATH = "../mahjong_img"

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

		img = cv2.resize(img, TILE_SIZE)

		filename = os.path.splitext(dir)[0]
		imgDesc = ImageDescription(img, filename)

		imgDesc.CreateHistogramDescription()
		imgDesc.CreateORBDescription()

		dictionary.append( imgDesc )

		print("\t" + filename)
	return dictionary

imgdict = CreateImgDictionary(ORB_CLASSIFIER_PATH)
cv2.imshow("Image", imgdict[0].sourceImage)

while True:
	success, inputImage = cap.read()

	inputDesc = ImageDescription(inputImage.copy())
	inputDesc.CreateORBDescription()
	inputDesc.CreateHistogramDescription()

	inputDesc.CreateContourDescription()

	# inputDesc.FilterContoursByArea((100, TILE_SIZE[0] * TILE_SIZE[1]))
	inputDesc.FilterContoursByBoundsSize( (24, 24), (TILE_SIZE[1], TILE_SIZE[1]))
	inputDesc.FilterContoursByBoarder()

	for source in imgdict:
		color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
		res = cv2.matchTemplate(inputDesc.grayImage,source.grayImage,cv2.TM_CCOEFF_NORMED)
		threshold = 0.5
		loc = np.where( res >= threshold)
		pts = []
		for p in zip(*loc[::-1]): pts.append(p)
		radius = 20
		for i in range(len(pts)):
			found = False
			for j in range(i+1, len(pts)):
				if ImgDescription.pointDistance(pts[i],pts[j]) < radius:
					found = True
			
			if found: continue

			pt = pts[i]
				
			# string = "%.2f" %(res)
			cv2.putText(inputImage, source.name, (pt[0],pt[1]-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
			cv2.rectangle(inputImage, pt, (pt[0] + source.imgWidth, pt[1] + source.imgHeight), color, 2)


	# usedPoints = []
	# minRadius = (int)(TILE_SIZE[0]/2)
	# for i in range(len(inputDesc.contours)):
	# 	irect = cv2.boundingRect(inputDesc.contours[i])

	# 	if inputDesc.filtered_contours[i]: continue

	# 	color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

	# 	irect = ImgDescription.scaleRect(irect, TILE_SIZE)

	# 	j = i
	# 	while j+1 < len(inputDesc.contours):
	# 		j += 1
	# 		if inputDesc.filtered_contours[j]:
	# 			continue

	# 		jrect = cv2.boundingRect(inputDesc.contours[j])
	# 		if ImgDescription.hasIntersection( irect, jrect ):
	# 			inputDesc.filtered_contours[j] = True
	# 			irect = ImgDescription.union(irect, jrect)

	# 			irect = ImgDescription.scaleRect(irect, TILE_SIZE)

	# 			(x, y, w, h) = jrect

	# 			cv2.rectangle(inputImage, (x,y), (x+w,y+h), color, 1)

	# 			j = i

	# 	# cv2.drawContours(inputImage, inputDesc.contours, i, color, size)

	# 	(x, y, w, h) = irect
	# 	print (irect)
	# 	print (len(inputDesc.sourceImage))

	# 	midpoint = ( (x+w)/2, (y+h)/2 )
	# 	for p in usedPoints:
	# 		if ImgDescription.pointDistance(p, midpoint) < minRadius:
	# 			continue
	# 	usedPoints.append( midpoint )
	# 	cv2.rectangle(inputImage, (x,y), (x+w,y+h), color, 3)

		
	# 	cp = inputDesc.sourceImage[y:y+h,x:x+w]

		
	# 	if len(cp) < 5: continue

	# 	cropped = ImageDescription(cp)
	# 	cropped.CreateORBDescription()
	# 	cropped.CreateHistogramDescription()

	# 	matches = cropped.GetORBMatches(imgdict)
	# 	vals = cropped.GetHistMatches(imgdict)

	# 	string = "N/A"
	# 	if not (matches[0].goods is None or vals[0] is None):
	# 		# string = "%s -> %.2f" %(matches[0].name, matches[0].ORBFitness)
	# 		string = "%s -> %.2f" %(vals[0].name, vals[0].HistFitness)
	# 		temp1 = cv2.drawMatchesKnn(matches[0].grayImage, matches[0].kp, \
	# 			cropped.grayImage, cropped.kp, matches[0].goods, None, flags=2)
			
	# 		cv2.imshow("Cropped %d.1" %(len(usedPoints)), vals[0].hsvImage)
	# 		cv2.imshow("Cropped %d.2" %(len(usedPoints)), cropped.hsvImage)
			
	# 	cv2.putText(inputImage, string, (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)


	# matches = inputDesc.GetORBMatches(imgdict)

	# id = 0
	# while id < 5 and matches[id].ORBFitness > 10:
	# 	cv2.putText(inputImage, "%d -> %s :: %.2f" %(id, matches[id].name, matches[id].ORBFitness), \
	# 		(50,50 + 30 * id), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
	# 	id += 1
	# if id == 0:
	# 	cv2.putText(inputImage, "N/A", (50 + 30 * id,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)

	# if not matches[0].goods is None:
	# 	temp1 = cv2.drawMatchesKnn(matches[0].grayImage, matches[0].kp, \
	# 		inputDesc.grayImage, inputDesc.kp, matches[0].goods, None, flags=2)

	cv2.rectangle(inputImage, (0,0), TILE_SIZE, (0,255,255), 3)

	# outputImage = np.concatenate((inputImage, temp1), axis=1)
	temp = cv2.cvtColor(inputDesc.threshImage, cv2.COLOR_GRAY2BGR)
	# temp = np.concatenate((temp, temp1), axis=1)
	outputImage = np.concatenate((inputImage, temp), axis=0)
	cv2.imshow("Result", outputImage)

	if cv2.waitKey(0) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyWindow("Result")
exit(0)