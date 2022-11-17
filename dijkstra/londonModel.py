import csv

#Creating a class for all the nodes
class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent =	{}
        self.dist = float('inf')
        self.previousVertex = False
        self.path = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def addNeighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight


    def getConnections(self):
        return self.adjacent.keys()


    def getId(self):
        return self.id


    def getWeight(self, neighbour):
        return self.adjacent[neighbour]


    def setDist(self, dist):
        self.dist = dist


    def getDist(self):
        return self.dist

    def setPreviousVertex(self, vertex):
    	self.previousVertex = vertex


    def getPreviousVertex(self):
    	return self.previousVertex

    def setPath(self, key, path):
        self.path[key] = path


    def getPath(self, key):
        return self.path[key]


#Creating a class for the graph of nodes(stations)
class Graph:
    def __init__(self):
        self.vertDict = {}
        self.numVertices = 0

    def __iter__(self):
        return iter(self.vertDict.values())

    def addVertex(self, id):
        self.numVertices += 1
        newVertex = Vertex(id)
        self.vertDict[id] = newVertex
        return newVertex


    def getVertex(self, n):
        if n in self.vertDict:
            return self.vertDict[n]
        else:
            return None


    def getVertices(self):
        return self.vertDict.keys()

        
    def addEdge(self, frm, to, cost=0):
        if frm not in self.vertDict:
            self.addVertex(frm)
        if to not in self.vertDict:
            self.addVertex(to)

        self.vertDict[frm].addNeighbour(self.vertDict[to], cost)
        self.vertDict[to].addNeighbour(self.vertDict[frm], cost)

#Read csv file with the data for stations, connections and lines 
#Put all of this data into a dictionary 

def readCSV(file):

	currentLine = 0
	output = {}
	headers = []

#File is opened here and read - looping through each station in the csv
	with open(file, 'r')  as openedFile:
		for line in csv.reader(openedFile):
			currentWord = 0
#Looping through every word 
			for word in line:
				if (currentLine == 0):
					output[word] = []
					headers.append(word)
				else:
                    #Add station to the dictionary under the correct category
                    #{"station1": [1]}
					output[headers[currentWord]].append(word)
				currentWord += 1
			currentLine += 1

	output['headers'] = headers # -> titles in the dictionary

	return output

#Connecting lines with IDs from the lines file with the connections file 
def formatLines(lines):
	formattedLines = {}

	for x in range(len(lines[lines['headers'][0]])):
		temp = {}

		for y in range(1, len(lines['headers'])):
			temp[lines['headers'][y]] = lines[lines['headers'][y]][x]

		formattedLines[lines[lines['headers'][0]][x]] = temp

	return formattedLines

#Connecting stations with IDs from stations file with the connections file
def formatStations(stations):
    formattedStations = {}

    for x in range(len(stations['id'])):
        formattedStations[stations['id'][x]] = {
            'id'            : stations['id'][x],
            'latitude'      : stations['latitude'][x],
            'longitude'     : stations['longitude'][x],
            'name'          : stations['name'][x],
            'display_name'  : stations['display_name'][x],
            'zone'          : stations['zone'][x],
            'total_lines'   : stations['total_lines'][x],
            'rail'          : stations['rail'][x],
        }

    return formattedStations
