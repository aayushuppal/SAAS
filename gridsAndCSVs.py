#restructure the csvs so col 1 is the label, latitude, then longitude
import sys
import numpy as np
import csv

latLonNorthwest= (47.734145, -122.459696)
latLonSoutheast= (47.48172, -122.224433)

class GridSquare(object):
	def __init__(self, id, lenFeatureVector, lati, longi):
		self.id = id
		self.featureVector = np.zeros(lenFeatureVector,)
		self.latitudeNW = lati
		self.longitudeNW = longi

	def __str__(self):
		return ("[ id: "+`self.id`+", vector:"+`self.featureVector`+", lat:"+`
			self.latitudeNW`+", long:"+`self.longitudeNW`+"]")


def makeGridSquares(numWide, numTall, lenHandles):
	width = abs(latLonNorthwest[0]-latLonSoutheast[0])/numWide
	height = abs(latLonNorthwest[1]-latLonSoutheast[1])/numTall

	gridSquares = []
	Id = 0
	for row in range(numTall):
		newRow = []
		for col in range(numWide):
			lati = latLonNorthwest[0] - (row * height) 
			longi = latLonNorthwest[1] + (col * width)
			x = GridSquare(Id, lenHandles, lati, longi)
			newRow.append(x)
			Id +=1
		gridSquares.append(newRow)
	return gridSquares


def whichGridId(gridSquares, mysteryLat, mysteryLong):
	"""returns the grid id which represents which grid square it is in
	latitude longitude width and height?"""
	width = abs(latLonNorthwest[0]-latLonSoutheast[0])/numWide
	height = abs(latLonNorthwest[1]-latLonSoutheast[1])/numTall
	row = int((latLonNorthwest[0] - mysteryLat)/height)
	col = int((mysteryLong - latLonNorthwest[1])/width)
	return (min(numTall-1,row),min(numWide -1, col)) #AVOID BOUNDARIES


def addEventsToGrid(gridSquares, handles):
	"""add one to the grid square's appropriate feature vector every time we read
	one that is in that lil grid zone"""
	i = 0
	labels = {}
	for handle in handles:
		labels[handle[:-4]] = i
		with open(handle) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:	
				longitude = float(row[0])
				latitude = float(row[1])

				if (longitude>latLonNorthwest[1] and longitude<latLonSoutheast[1] and 
					latitude<latLonNorthwest[0] and latitude>latLonSoutheast[0]): #be in seattle please
					row,col = whichGridId(gridSquares, latitude, longitude)
					gridSquares[row][col].featureVector[i] += 1
				# else:
				# 	print "nothing happened :(" + `handle` +  "  " + `longitude` + " " + `latitude` #if you want to see the ones outside!
		i += 1
	return labels


# def writeOutputCSV():
# 	filenameDest = "output.csv"


if __name__ == "__main__":
	try:
		numWide = int(sys.argv[1])
		numTall = int(sys.argv[2])
	except:
		print "USAGE: width height csvname.csv csvname.csv"
	i = 3
	handles = [] #accumulates the csv names
	while i<len(sys.argv):
		handles.append(sys.argv[i])
		i+=1
	#call something with the handles
	gridSquares = makeGridSquares(numWide, numTall, len(handles))
	# whichGridId(gridSquares,47.634145, -122.359696)
	addEventsToGrid(gridSquares,handles)

	# for i in gridSquares:
	# 	for j in i:
	# 		print j