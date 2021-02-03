import math
import Grid
import Coordinate

class Astar():

    def __init__(self, grid: Grid, wind_direction: int, start: Coordinate, end: Coordinate):

        ## required params
        self.grid = grid
        self.wind_direction = wind_direction
        self.start = start
        self.end = end

        ## globals
        self.lowestPath = []
        self.pathsToCheck = []
        self.lowestPathWeight = 999999999

        ## constants
        self.currentDirectionWeight = 20
        self.nodeWeightMultiplier = 10000


    # Heuristic stuff:
    #   - node weight: will be total distance from current node to the end
    #   - edge weight: will be current direction of travel + current wind direction vs edge direction
    #
    # Algo Stuff:
    #   - F(n) = g(n) + h(n)
    #       - g(n) = edge weight
    #       - h(n) = dest node weight
    #
    #   - Evaluate all pathsToCheck from a node, then start continuing on the lowest cost one
    #   - once you find the final node, keep going through your list until the value you have is lower than
    #       the top of the list
    def runAstar(self):

        # console.log(gridCenters)  # holds all the points, and their coords
        resetPaths(start)
        counter = 0
        # console.log(start, pathsToCheck)
        while (pathsToCheck.length > 0 and pathsToCheck[0][0].weight <= lowestPathWeight and counter < 500):
            findCheapestPath()
            counter += 1
            # console.log(counter, pathsToCheck)

            return self.lowestPath


    # Reset globals
    def resetPaths(self):
        self.pathsToCheck = [start] # hardcoded start
        self.lowestPathWeight = 999999999
        self.lowestPath = []


        def findCheapestPath(self):
            curPath = self.pathsToCheck.pop()
            pathNode = curPath[0]
            pathWeight = pathNode.weight
            pathNodeNeighbors = findNeightbors(pathNode.x, pathNode.y)

            for neighbor in pathNodeNeighbors:
                neighborWeight = findNodeWeight(neighbor, end)
                edgeWeight = findEdgeWeight(curPath, neighbor, windDirection)
                totalWeight = pathWeight + neighborWeight + edgeWeight
                tempPath = [*curPath]
            # console.log(`neighbor: ${neighborWeight}, end: ${end}, edge: ${edgeWeight}, pathWeight: ${pathWeight}, x-y: ${neighbor.x}-${neighbor.y}`)
            tempPath.unshift({weight: totalWeight, **neighbor})
            addPath(tempPath)


    def addPath(self, path):
        pathNode = path[0]
        if (pathNode.x == end.x and pathNode.y == end.y): ## if we get to the destination
            if (pathNode.weight < lowestPathWeight): ## keep this new path if its good
                lowestPathWeight = pathNode.weight
                lowestPath = path
             ## discard if we have a better one

        ## console.log('pre', pathsToCheck)
        self.pathsToCheck.push(path)  ## just put the path in teh global
        self.pathsToCheck.sort(key = lambda path: path[0].weight)  # sort it so we have the shortest path on top
        ## console.log('post',pathsToCheck)


    # calculate the distance from the destination for the current node
    def findNodeWeight(self, node, dest):
        # got the converter to meters here: https:#www.movable-type.co.uk/scripts/latlong.html
        R = 6371e3  # metres
        φ1 = node.lat * math.pi/180  # φ, λ in radians
        φ2 = dest.lat * math.pi/180
        Δφ = (dest.lat-node.lat) * math.pi/180
        Δλ = (dest.lng-node.lng) * math.pi/180

        a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

        meters = R * c  # in metres
        return meters
        ## return nodeWeightMultiplier * Math.pow(node.lat - dest.lat, 2) + Math.pow(node.lng - dest.lng, 2)
        ## return nodeWeightMultiplier * Math.max(Math.abs(node.lat - dest.lat) + Math.abs(node.lng - dest.lng))


    ## calculate the edge weight between the start node and dest node
    ##     So we calculate if it is staying the same direction, and direction with respect to wind
    def findEdgeWeight(self, prevPath, dest, windDirection):
        weight = 0

        if prevPath.length > 1:
            nodeA = prevPath[1]
            nodeB = prevPath[0]
            nodeC = dest
            slopeAB = (nodeA.y - nodeB.y)/(nodeA.x - nodeB.x)
            slopeBC = (nodeB.y - nodeC.y)/(nodeB.x - nodeC.x)
            if (slopeAB == slopeBC): # find out if nodes are collinear by seeing if slopes are equatl
                weight += currentDirectionWeight

            startNode = prevPath[0]
        # TODO ADD DIRECTION BASED ON WIND
        return weight


    # find and returns an array of the neighbors of a given point
    def findNeightbors(self, x, y):
        neighbors = []

        if (x != 0): # left
            neighbors.push(self.grid.get(x - 1, y))
        if (x != maxX): # right
            neighbors.push(self.grid.get(x + 1, y))
        if (x != 0 and y != 0): #  top left
            neighbors.push(self.grid.get(x - 1, y - 1))
        if (x != maxX and y != 0): # top right
            neighbors.push(self.grid.get(x + 1, y - 1))
        if (x != 0 and y != maxY): #  bot left
            neighbors.push(self.grid.get(x - 1, y + 1))
        if (x != maxX and y != maxY): # bot right
            neighbors.push(self.grid.get(x + 1, y + 1))
        if (y != 0): # top
            neighbors.push(self.grid.get(x, y - 1))
        if (y != maxY): # bottom
            neighbors.push(self.grid.get(x, y + 1))

        return neighbors



