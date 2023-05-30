import requests
def get_location_name(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key=AIzaSyDgH8JbnLrW49E5rE8RFXXewRkJLHLXekM"
    response = requests.get(url)
    data = response.json()
    
    #may want to add error checking for failed requests here

    #have to loop through the results to pull out the city and state names
    city, state = None, None
    for result in data['results']:
        for component in result['address_components']:
            if "locality" in component['types']:
                city = component['long_name']
            elif "administrative_area_level_1" in component['types']:
                state = component['long_name']
                
    #if city and state are found, concatenate them into a single string
    if city and state:
        location_name = f"{city}, {state}"
    else:
        location_name = None 
    
    return location_name
