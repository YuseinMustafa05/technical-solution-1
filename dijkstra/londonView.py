import tkinter as tk
import londonController

#Put the dictionary into a list of stations
def getStationList():
    stations = []
    stationList = londonController.getStations()

    for x in stationList:
        stations.append(stationList[x]['name'])

    stations.sort()

    return stations

#This will not the final project or the user interface. This is just a demo to show what the program does at this stage of working on it. 
class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

       
        self.stationList = getStationList()
        self.startingStation = ''
        self.endingStation = ''
        self.unavailableStations = []

      
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.errorLabel = tk.Label(self, text="", width=90) #Output for errors
        self.errorLabel.grid(row = 0, column = 0, columnspan = 3)

      #Stations in a list box for the user to pick from
        self.stationLabel = tk.Label(self, text="Stations", width=6)
        self.stationLabel.grid(row = 1, column = 0)

   #Activate station list box
        self.stations = tk.Listbox(self, width = 40, height = 5)
        self.stations.grid(row = 2, column = 0)

        #Add every and each station to that list box 
        for station in self.stationList:
            self.stations.insert(tk.END, station)

#Output message for a station that is not available
        self.unavailableStationLabel = tk.Label(self, text="Unavailable Stations", width=20)
        self.unavailableStationLabel.grid(row = 1, column = 2)
#Activate and initialise 
        self.unavailableStationsListBox = tk.Listbox(self, width = 40, height = 5)
        self.unavailableStationsListBox.grid(row = 2, column = 2)
#The button to choose a start station
        self.startingStationButton = tk.Button(self, text = 'Set Start', command = self.setStart, width = 15, padx = 0)
        self.startingStationButton.grid(row = 2, column = 1, sticky = tk.N)
#Initialising the start button
        self.endingStationButton = tk.Button(self, text = 'Set End', command = self.setEnd, width = 15, padx = 0)
        self.endingStationButton.grid(row = 2, column = 1)
#Button for destination station
        self.setUnavailable = tk.Button(self, text = 'Set Status', command = self.changeStatus, width = 15, padx = 0)
        self.setUnavailable.grid(row = 2, column = 1, sticky = tk.S)

#Initialising the butoon for destiantion station
        self.routeLabel = tk.Label(self, text="", width=50)
        self.routeLabel.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W)
#Button to confirm 
        self.confirmRoute = tk.Button(self, text = 'Confirm Route', command = self.findRoute, width = 15)
        self.confirmRoute.grid(row = 3, column = 2, sticky = tk.E)
#Initialise button
        self.routeText = tk.Text(self, height = 5, width = 80)
        self.routeText.grid(row = 4, column = 0, columnspan = 3, padx = 5)

#Make the start start button command
    def setStart(self):
        index = self.stations.curselection()[0]
        self.startingStation = self.stations.get(index)

        if self.endingStation != '':
            updatedText = "From %s to %s" % (self.startingStation, self.endingStation)
        else:
            updatedText = "From %s" % (self.startingStation)


        self.routeLabel.config(text = updatedText)

#Commnd for the destination button
    def setEnd(self):
        index = self.stations.curselection()[0]
        self.endingStation = self.stations.get(index)

        if self.startingStation != '':
            updatedText = "From %s to %s" % (self.startingStation, self.endingStation)
        else:
            updatedText = "%s to %s" % (self.routeLabel['text'], self.endingStation)

        self.routeLabel.config(text = updatedText)

   #Change the occupation of a station - if in stations list, move to unavailbale and vice versa
    def changeStatus(self):
       
        if (self.stations.curselection()):
            station = self.changeStationStatus(self.stations, self.unavailableStationsListBox)
            self.unavailableStations.append(station)


        if (self.unavailableStationsListBox.curselection()):
            station = self.changeStationStatus(self.unavailableStationsListBox, self.stations)
            self.unavailableStations.remove(station)

#A temporary list of all active stations that are in the list box, clear current list of stations in the taregt, insert into respective list box
#remove from previous list box and return the moved station
    def changeStationStatus(self, moveFrom, moveTo):
        index = moveFrom.curselection()[0]
        station = moveFrom.get(index)

        tempList = list(moveTo.get(0, tk.END))
        tempList.append(station)
        tempList.sort()

        moveTo.delete(0, tk.END)

        for item in tempList:
            moveTo.insert(tk.END, item)

        moveFrom.delete(index)

        return station

#Dijkstra in action imported from the other module, if route found, output it, if not, error message is outputted.
    def findRoute(self):
        route = londonController.findFastestRoute(self.startingStation, self.endingStation, self.unavailableStations)

        if isinstance(route, list):
            self.setRouteText(route)
            self.displayResponse({'error': False, 'msg': 'found'})
        else:
            self.setRouteText(None)
            self.displayResponse(route)

#Output the route, count how many stations are in the list , append to the output list. Dont add "-" if the station is last. 
    def setRouteText(self, route):
        self.routeText.delete(1.0, tk.END)

        if route:
            stationCount = len(route)
            self.routeText.insert(tk.END, "Suggested Route: ")

            for station in route:
                if str(station) == str(route[stationCount-1]):
                    station = "%s" % station
                else:
                    station = "%s - " % station

                self.routeText.insert(tk.END, station)

 #Output messages respectively
    def displayResponse(self, response):
        if response:
            background = 'Green'

            if response['error']:
                background = 'Red'

            self.errorLabel.config(background=background, text=response['msg'])

#Create object to output the demo 
def initiateView():
    app = GUI()
    app.master.title('London tube')
    app.mainloop()


initiateView()
