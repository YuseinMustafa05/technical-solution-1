import requests 
import json 
import datetime 

appId = '0d3ca992cf024a1b933ad36e42ca42d9'
appKey = '7cb4785379de41e5a653e984990bb861'

def api():
    try:
        stationStart = input("Please enter the station you want to travel from ") 
        print(f"You have selected {stationStart}") 
        destination = input("Please enter your destination station ")
        print(f"You have selected{destination}")
        print("Now fetching route, please wait...")
        getRequest = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{stationStart}/to/{destination}&app_id={appId}&app_key={appKey}")
        data = getRequest.json()
        start = data['fromLocationDisambiguation']['disambiguationOptions'][0]['parameterValue']
        end = data['toLocationDisambiguation']['disambiguationOptions'][0]['parameterValue']
        journey = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{start}/to/{end}&app_id={appId}&app_key={appKey}")
        journeyJson = journey.json()
        journeyTime = journeyJson['journeys'][0]['duration']
        
        print(f"Journey is {journeyTime} minutes")
        
        print("This is the journey...\n")
        
        route = journeyJson['journeys'][0]['legs']
        
        for information in route:
            print("From ", information['arrivalPoint']['commonName'])
            print(information['instruction']['detailed'])
            print("Arrive at ", information['arrivalPoint']['commonName']) 
            
            disruptions = information['isDisrupted'] 
            if disruptions == True:
                for disruption in information['disruptions']:
                    print("\n=======Disruption:=======")
                    print(disruption['description'])
                    
            else:
                print("No disruptions available\n") 
            print("\n")
            
    except KeyError as e:
        print("Error (KeyError)! Please try again!") 
        
        
api()