import cv2
import os

class ImageDescription:
	orb = cv2.ORB_create(nfeatures=1000)
	bestfit = cv2.BFMatcher()

	def __init__(self, filename):
		self.filename = filename
		self.name = os.path.splitext(filename)[0]
		self.sourceImage = cv2.imread(filename, 0)

	def __init__(self, image):
		self.sourceImage = image
	
	def CreateORBDescription(self):
		self.kp, self.desc = \
			ImageDescription.orb.detectAndCompute(self.sourceImage, None)

	def CreateHistogramDescription(self):
		h_bins = 50
		s_bins = 60
		histSize = [h_bins, s_bins]
		h_ranges = [0, 180]
		s_ranges = [0, 256]
		ranges = h_ranges + s_ranges
		channels = [0, 1]

		self.hist = cv2.calcHist( \
			[self.sourceImage], channels, None, histSize, ranges, accumulate=False)

	def CompareORBDescription(self, other):
		try:
			matches = ImageDescription.bestfit.knnMatch(self.desc, other.desc, k=2)
			good = []
			for m, n in matches:
				if m.distance < 0.75 * n.distance:
					good.append([m])
			return good
		except:
			return None

	@staticmethod
	def GetBestORBFit(descriptors, target):
		valid_matches = []
		for source in descriptors:
			good = 
			valid_matches.append(ImageDescription.CompareORBDescrition(source, target))
		



global imgdic
global orb
global thresh
global alpha

path = "./ImageClassifiers"
imgdic = []

thresh = 10.0
alpha = 0.4

global prevMatches

dirlist = os.listdir(path)
print("Loading Images (len %d):"  %(len(dirlist)))
for dir in dirlist:
	filename = os.path.splitext(dir)[0]
	img = cv2.imread("%s/%s" %(path, dir), 0)

	print("\t" + filename)

prevMatches = [0.0] * len(imgdic)

def getIdentifier(kp2, desc2):
	global prevMatches

	bestfit = cv2.BFMatcher()
	matchList = [[None]] * len(imgdic)

	try:
		for index in range(len(imgdic)):
			(_, img1, kp1, desc1) = 
			matches = bestfit.knnMatch(imgdic[index].desc, desc2, k=2)
			good = []
			for m, n in matches:
				if m.distance < 0.75 * n.distance:
					good.append([m])

			matchList[index] = good
	except:
		pass

	maxValue = 0.0
	maxIndex = -1
	for index in range(len(imgdic)):
		val = ((float)(len(matchList[index])) * (alpha)) + (prevMatches[index] * (1 - alpha))
		prevMatches[index] = val

		if (maxValue < val) and (val > thresh):
			maxValue = val
			maxIndex = index

	if maxIndex == -1:
		return (None, None, None, None, None)
	(a, b, c, d) = imgdic[maxIndex]
	return a, b, c, d, matchList[index]

def filterContours(contours, img, size):
	filteredContours = []

	imgWidth = len(img[0,:])
	imgHeight = len(img[:,0])

	for c in contours:
		(x, y, h, w) = cv2.boundingRect(c)
		if x > 5 and y > 5 and x+w < imgWidth - 5 and y+h < imgHeight - 5 and \
				cv2.contourArea(c) > 100 and w*h < size[0] * size[1]:
			filteredContours.append(c)
	return filteredContours

camerano = 1 # CAMERA NUMBER
frameWidth = 640 # DISPLAY WIDTH
frameHeight = 480 # DISPLAY HEIGHT
cap = cv2.VideoCapture(camerano)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

tilesize = (90,120)
while True:
	success, img2 = cap.read()
	
	displayImage = img2.copy()

	img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
	img2 = cv2.medianBlur(img2, 5)
	kp2, desc2 = orb.detectAndCompute(img2, None)
	(filename, img1, kp1, desc, goods) = getIdentifier(kp2, desc2)
	if not filename:
		filename = "N/A"

	# t,threshImage = cv2.threshold(img2, 127, 255, 0)
	threshImage = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
			cv2.THRESH_BINARY,11,2)
	contours, _ = cv2.findContours(threshImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# Filter Contours that are conneted to the edge of the screen:
	contours = filterContours(contours, img2, tilesize)


	contours.sort(key=lambda c : cv2.contourArea(c), reverse=True)

	top = 10
	if len(contours) < top: top = len(contours)
	
	merging = contours[:top]
	id = 0
	mergingRange = 10
	while id < len(merging):
		color = (255,0,0)
		(x1, y1, w1, h1) = cv2.boundingRect(merging[id])
		(maxx, maxy, maxw, maxh) = (x1, y1, w1, h1)

		# j = id + 1
		# while j < len(merging):
		# 	(x2, y2, w2, h2) = cv2.boundingRect(merging[j])
		# 	xint = x2 > maxx - mergingRange and x2 < maxx+maxw + mergingRange
		# 	wint = x2+w2 > maxx - mergingRange and x2+w2 < maxx+maxw + mergingRange
		# 	yint = y2 > maxy - mergingRange and y2 < maxy+maxh + mergingRange
		# 	hint = y2+h2 > maxy - mergingRange and y2+h2 < maxy+maxh + mergingRange

		# 	intersect = xint or wint or yint or hint
		# 	if intersect:
		# 		color = (0,0,255)
		# 		if x2 < maxx: maxx = x2
		# 		if y2 < maxy: maxy = y2
		# 		if w2 > maxw: maxw = w2
		# 		if h2 > maxh: maxh = h2

		# 		del merging[j]
		# 		j = id + 1
		# 	j += 1

		if maxh-maxy * maxw-maxx > tilesize[0] * tilesize[1]:
			color = (0,255,0)
		cv2.rectangle(displayImage, (maxx,maxy), (maxx+maxw,maxy+maxh), color, 3)
		id += 1
	
	contours = contours[top:]

	cv2.imshow("Thresh Image", threshImage)

	cv2.drawContours(displayImage, contours, -1, (0,255,0), 1)
	# cv2.drawContours(displayImage, contours, 0, (255,0,0), 3)

	cv2.putText(displayImage, filename, (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
	# cmp = cv2.drawMatchesKnn(img1, kp1, img2, kp2, goods, None, flags=2)

	# cv2.rectangle(displayImage, (0,0), tilesize, (0,255,255), 3)


	
	cv2.imshow("Result", displayImage)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
