from __future__ import annotations
import cv2

CONTOUR_BLUR = 5
CONTOUR_BOARDER_PADDING = 5
ORB_DESCRIPTION = cv2.ORB_create(nfeatures=2000)
BEST_FIT = cv2.BFMatcher()
ORB_ALPHA = 0.3
HIST_ALPHA = 0.3

class ImageDescription:
	def __init__(self, image, name="N/A") -> None:
		self.name = name
		self.sourceImage = image
		self.grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
		h_ranges = [0, 180]
		s_ranges = [0, 256]
		ranges = h_ranges + s_ranges
		channels = [0, 1]

		self.hist = cv2.calcHist( \
			self.grayImage, channels, None, histSize, ranges, accumulate=False)
		cv2.normalize(self.hist, self.hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

	def CreateContourDescription(self) -> None:
		self.threshImage = cv2.adaptiveThreshold(cv2.medianBlur(self.grayImage, CONTOUR_BLUR), \
			255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
		self.contours, self.heirachy = cv2.findContours(self.threshImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	def FilterContoursByBoarder(self) -> None:
		filteredContours = []
		for c in self.contours:
			(x, y, h, w) = cv2.boundingRect(c)
			if x > 5 and y > 5 and x+w < self.imgWidth - 5 and y+h < self.imgHeight - 5:
				filteredContours.append(c)
		self.contours = filteredContours

	def FilterContoursByBoundsSize(self, min :list[2], max :list[2]) -> None:
		filteredContours = []
		for c in self.contours:
			(x, y, h, w) = cv2.boundingRect(c)
			if w >= min[0] and w <= max[0] and h >= min[1] and h <= max[1]:
				filteredContours.append(c)
		self.contours = filteredContours

	def FilterContoursByArea(self, area :list[2]) -> None:
		filteredContours = []
		for c in self.contours:
			carea = cv2.contourArea(c)
			if carea > area[0] and carea < area[1]:
				filteredContours.append(c)
		self.contours = filteredContours

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
		cv2.compareHist(self.hist, other.hist, cv2.HISTCMP_CORREL)
		return 0.0

	def GetHistMatches(self, descriptors :list[ImageDescription]) -> list[ImageDescription]:
		valid_matches = []
		for source in descriptors:
			fit = (source.HistFitness * (1 - HIST_ALPHA)) + \
				(source.CompareHistDescription(self) * HIST_ALPHA)
			valid_matches.append( fit )

		valid_matches.sort(reverse=True)
		return valid_matches