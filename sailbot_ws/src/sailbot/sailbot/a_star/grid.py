
import Coordinate
#this will need to be fleshed out as we determine how to create and maintain the grid
#-- will it have the weights stored in it?
#-- will it just be 0s and 1s for navigatable vs not?

class Grid():

    def __init__(self, gridCorners):
		self.gridCorners = {topleft: { lat: 42.85414938719151, lng: -70.98833200038395 }, botleft: { lat: 42.84417554052568, lng: -70.98833200038395 }, botright: { lat: 42.84401759443596, lng: -70.97532473965633 }, topright: { lat: 42.85367747491202, lng: -70.97532473965633 }};
        self.gridNodes = []

	    self.squareRad = 0.001; # 10 meters is 4th decimal places I think? (near the equator it is 11)
    def get(x: int, y: int):
    	return self.gridNodes[x][y]

    def getGrid():
        return self.gridNodes
    
    def makeGrid():

		# generates grid of 13x10 at Lake attitash with a squareRad of 0.001
		# generate GridLines and their centers

	    latLines = []
	    lngLines = []

	    for i in range(self.gridCorners.topleft.lng, self.gridCorners.topright.lng, squareRad):
	        latLines.push([{lat: gridCorners.topleft.lat, lng: i}, {lat: gridCorners.botleft.lat, lng: i}])

	    for i in range(self.gridCorners.topleft.lat, self.gridCorners.botleft.lat, -squareRad):
	        lngLines.push([{lat: i, lng:  gridCorners.topleft.lng}, {lat: i, lng:  gridCorners.topright.lng}])

	    gridIntersects = []

	    # generating all the points where the 2 gridlines intersect
	    for latLine, i in latLines:
	        temp = []
	    	for lngLine, j in lngLines:
	            temp.push({x: i, y: j, lat: lngLine[0].lat, lng: latLine[0].lng})
	        gridIntersects.push(temp);
	    


	    for i in range(0, gridIntersects.length - 1):
	        temp = []
	        leftLngLine = gridIntersects[i]
	        rightLngLine = gridIntersects[i + 1]

	        for j in range(0, leftLngLine.length - 1):
	            topLeftCorner = leftLngLine[j]
	            topRightCorner = rightLngLine[j]
	            botLeftCorner = leftLngLine[j + 1]
	            center = { lat: (topLeftCorner.lat + botLeftCorner.lat)/2,lng: (topLeftCorner.lng + topRightCorner.lng)/2 };

	            temp.push(new Coordinate(x = i, y = j, lat = center.lat, lng = center.lng);
	        
	        gridNodes.push(temp);
