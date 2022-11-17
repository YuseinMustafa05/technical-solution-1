import londonModel

#Reading the files 
lines = londonModel.formatLines(londonModel.readCSV('londonlines.csv'))
stations = londonModel.formatStations(londonModel.readCSV('londonstations.csv'))
connections = londonModel.readCSV('londonconnections.csv')


graph = None # -> The graph is a global variable

#Get all of the stations - a getter method
def getStations():
	return stations


#Dijkstra's algorithm in action from the londonModel
def findFastestRoute(start, end, unavailableStations):
	global graph

#Graph is creted and initialised
	graph = londonModel.Graph()
	response = validateStations(start, end, unavailableStations)#Checking inputs vor validity

	if response:
		return response
#Get ID From The File
	start = getStationIdFromName(start)
	end = getStationIdFromName(end)
#Stations are added to the graph
	addStations(unavailableStations)

	visited = []
	unvisited = list(graph.getVertices())

#Current node has a distance of 0 from itself to itself 
	for vertex in graph:
		if (start == vertex.getId()):
			vertex.setDist(0)
			start = vertex


		nextNode = getNextNode(unvisited)
		checkNeighbours(nextNode)
#Delete if station is unvisited
		del unvisited[unvisited.index(nextNode.getId())]
		visited.append(nextNode.getId())
#Rerurned to starting node 
	setPaths(start)
	path = getPath(start, end)

#Return the path if the route is valid
	if path != []:
		return path
	else:
		#Otherwise output an error message 
		response = {
			'error': True,
			'msg': 'No possible route between stations'
		}
		return response

#Check chosen stations by the user are valid - if route exixts, if only start or end is chosen; or if start and destination are the same
#and output a respective message 
def validateStations(start, end, unavailableStations):
	response = {
		'error': True,
		'msg': ''
	}
	if (start == '' or end == ''):
		response['msg'] = 'Please select a starting and ending station'
		return response

	
	if (start == end):
		response['msg'] = 'Starting and ending stations are the same'
		return response

	if start in unavailableStations or end in unavailableStations:
		response['msg'] = 'No possible route between stations'
		return response


	return None

#Get the ID number from the connections
def getStationIdFromName(target):
	for id in stations:
		if (stations[id]['name'] == target):
			return id

#Stations are added to the graph in order to add them to the graph and the respective lsit. Check if both start and destiantion are in the unavailable list
#and add to the graph if not
def addStations(unavailable):
	
	for x in range(len(connections['station1'])):

		if (unavailable == None):
			graph.addEdge(connections['station1'][x], connections['station2'][x], int(connections['time'][x]))
		else:
		
			if (stations[connections['station1'][x]]['name'] not in unavailable and stations[connections['station2'][x]]['name'] not in unavailable):
				graph.addEdge(connections['station1'][x], connections['station2'][x], int(connections['time'][x]))


def getNextNode(unvisited):
	nextNode = False

	for vertex in graph:
		if (vertex.getId() in set(unvisited)):
			if (nextNode == False):
				nextNode = vertex

			if (vertex.getDist() < nextNode.getDist()):
				nextNode = vertex

	return nextNode

#See the weights of the adjacent neighbours and add to the current node 
def checkNeighbours(currentNode):
	neighbours = []
	neighbours = currentNode.getConnections()

	for vertex in neighbours:
		tentativeDist = currentNode.getDist() + vertex.getWeight(currentNode)#-> Tentative list is the new distance and if it is less than the current distance 
		#to that node, update the shortest distance. If notm do not update
		if (tentativeDist < vertex.getDist()):
			vertex.setDist(tentativeDist)
			vertex.setPreviousVertex(currentNode)

#Set path for every node in the graph from starting node 
def setPaths(start):
	for vertex in graph:
		path = pathToVertex(vertex, [])

		if vertex.getDist() != float('inf'):
			vertex.setPath(start.getId(), path[::-1])

#Set the path to the node from the starting node
def pathToVertex(vertex, path):
	if (vertex.getPreviousVertex()): # If this node has a previous node, add the current node to the path.If there is no previous node, return self. 
		path.append(vertex.getId())
		pathToVertex(vertex.getPreviousVertex(), path)
	else:
		path.append(vertex.getId())

	return path

#Path from start node to destination
def getPath(start, end):
	vertex = graph.getVertex(end)
	path = []

	if  vertex == None:
		return path

	if vertex.getDist() == float('inf'):# -> No possible route since the distance is infinte
		
		return path

	for x in vertex.getPath(start.getId()):
		path.append(stations[x]['name'])

	return path
