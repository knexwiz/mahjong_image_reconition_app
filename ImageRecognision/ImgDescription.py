from __future__ import annotations
import cv2
import math

CONTOUR_BLUR = 5
CONTOUR_BOARDER_PADDING = 5
ORB_DESCRIPTION = cv2.ORB_create(nfeatures=5000)
BEST_FIT = cv2.BFMatcher()
ORB_ALPHA = 1.0
HIST_ALPHA = 1.0

class ImageDescription:
	def __init__(self, image, name="N/A") -> None:
		self.name = name
		self.sourceImage = image
		self.grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		self.hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		self.ORBFitness = (float)(0)
		self.HistFitness = (float)(0)
		self.imgWidth = len(image[0,:])
		self.imgHeight = len(image[:,0])
	
	def CreateORBDescription(self) -> None:
		self.kp, self.desc = \
			ORB_DESCRIPTION.detectAndCompute(self.grayImage, None)

	def CreateHistogramDescription(self) -> None:
		h_bins = 50
		s_bins = 60
		histSize = [h_bins, s_bins]
		
		# hue varies from 0 to 179, saturation from 0 to 255
		h_ranges = [0, 180]
		s_ranges = [0, 256]
		ranges = h_ranges + s_ranges # concat lists
		
		# Use the 0-th and 1-st channels
		channels = [0, 1]

		self.hist = cv2.calcHist([self.hsvImage], channels, None, histSize, ranges, accumulate=False)
		cv2.normalize(self.hist, self.hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

	def CreateContourDescription(self) -> None:
		self.threshImage = cv2.adaptiveThreshold(cv2.medianBlur(self.grayImage, CONTOUR_BLUR), \
			255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
		self.contours, self.heirachy = cv2.findContours(self.threshImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		self.filtered_contours = [False] * len(self.contours)

	def FilterContoursByBoarder(self) -> None:
		i = 0
		for i in range(len(self.contours)):
			if self.filtered_contours[i]: continue
			(x, y, h, w) = cv2.boundingRect(self.contours[i])
			if not (x > 5 and y > 5 and x+w < self.imgWidth - 5 and y+h < self.imgHeight - 5):
				self.filtered_contours[i] = True

	def FilterContoursByBoundsSize(self, min :list[2], max :list[2]) -> None:
		i = 0
		for i in range(len(self.contours)):
			if self.filtered_contours[i]: continue
			(x, y, h, w) = cv2.boundingRect(self.contours[i])
			if not (w >= min[0] and w <= max[0] and h >= min[1] and h <= max[1]):
				self.filtered_contours[i] = True

	def FilterContoursByArea(self, area :list[2]) -> None:
		i = 0
		for i in range(len(self.contours)):
			if self.filtered_contours[i]: continue
			carea = cv2.contourArea(self.contours[i])
			if not (carea > area[0] and carea < area[1]):
				self.filtered_contours[i] = True

	def CompareORBDescription(self, other :ImageDescription) -> list:
		try:
			matches = BEST_FIT.knnMatch(self.desc, other.desc, k=2)
			good = []
			for m, n in matches:
				if m.distance < 0.75 * n.distance:
					good.append([m])
			return good
		except:
			return [None]


	def GetORBMatches(self, descriptors :list[ImageDescription]) -> list[ImageDescription]:
		valid_matches = []
		for source in descriptors:
			source.goods = source.CompareORBDescription(self)
			source.ORBFitness = (source.ORBFitness * (1 - ORB_ALPHA)) + \
				((float)(len(source.goods)) * ORB_ALPHA)
			valid_matches.append( source )

		valid_matches.sort(key=lambda desc: desc.ORBFitness ,reverse=True)
		return valid_matches

	def GetBestORBMatch(self, descriptors :list[ImageDescription]) -> ImageDescription:
		return ImageDescription.GetORBMatches(descriptors, self)[0]

	def CompareHistDescription(self, other :ImageDescription) -> float:
		return cv2.compareHist(self.hist, other.hist, cv2.HISTCMP_CORREL)

	def GetHistMatches(self, descriptors :list[ImageDescription]) -> list[ImageDescription]:
		valid_matches = []
		for source in descriptors:
			source.HistFitness = (source.HistFitness * (1 - HIST_ALPHA)) + \
				(source.CompareHistDescription(self) * HIST_ALPHA)
			valid_matches.append( source )
			print(source.HistFitness)

		valid_matches.sort(key=lambda desc: desc.HistFitness ,reverse=True)
		return valid_matches

	'''
	Can only be used when comparing images of the same size!
	'''
	def GetNormMatches(self, descriptors :list[ImageDescription]) -> list[ImageDescription]:
		valid_matches = []
		for source in descriptors:
			source.errorL2 = cv2.norm( source.sourceImage, self.sourceImage, cv2.NORM_L2 )
			source.similarity = 1 - source.errorL2 / ( source.imgWidth * source.imgHeight )
			valid_matches.append( source )

		valid_matches.sort(key=lambda desc: desc.HistFitness ,reverse=True)
		return valid_matches

	def GetTemplateMatches(self, descriptors :list[ImageDescription]) -> list[ImageDescription]:
		valid_matches = []
		for source in descriptors:
			source.errorL2 = cv2.norm( source.sourceImage, self.sourceImage, cv2.NORM_L2 )
			source.similarity = 1 - source.errorL2 / ( source.imgWidth * source.imgHeight )
			valid_matches.append( source )

		valid_matches.sort(key=lambda desc: desc.HistFitness ,reverse=True)
		return valid_matches

def union(a,b):
	x = min(a[0], b[0])
	y = min(a[1], b[1])
	w = max(a[0]+a[2], b[0]+b[2]) - x
	h = max(a[1]+a[3], b[1]+b[3]) - y
	return (x, y, w, h)

def intersection(a,b):
	x = max(a[0], b[0])
	y = max(a[1], b[1])
	w = min(a[0]+a[2], b[0]+b[2]) - x
	h = min(a[1]+a[3], b[1]+b[3]) - y
	if w<0 or h<0: return False, (0,0,0,0)
	return True, (x, y, w, h)

def hasIntersection(a,b):
	x = max(a[0], b[0])
	y = max(a[1], b[1])
	w = min(a[0]+a[2], b[0]+b[2]) - x
	h = min(a[1]+a[3], b[1]+b[3]) - y
	if w<0 or h<0: return False
	return True

def scaleRect(a, target):
	(x, y, w, h) = a
	x -= (int)((target[0] - w)/2)
	y -= (int)((target[1] - h)/2)
	w += (int)(target[0] - w)
	h += (int)(target[1] - h)

	return (x, y, w, h)

def pointDistance(a,b):
	return math.hypot(a[0] - b[0], a[1] - b[1])