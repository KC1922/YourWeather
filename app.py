import requests
from flask import Flask, render_template
from datetime import datetime
import pytz
from icon_mapping import icon_mapping
from directions import degrees_to_direction

app = Flask(__name__)

@app.route('/')
def home():
    location = "Tampa, Florida" #hard code location for now
    # Make the API request
    url = "https://api.openweathermap.org/data/2.5/onecall"  
    params = {
        "lat": 27.9506,  # Latitude of Tampa, Florida
        "lon": -82.4572,  # Longitude of Tampa, Florida
        "appid": "fbf5ddfd48f2e22c88896a1be5ac73e7", 
        "units": "imperial"  # Get temperature in Fahrenheit
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Get the current date and time in the returned timezone
    tz = pytz.timezone(data['timezone'])
    now = datetime.now(tz)
    current_time = now.strftime("%B %d, %Y %I:%M %p")

    # Determine if day or night for the current weather icon
    condition_id = data["current"]["weather"][0]["id"]
    if 800 > condition_id > 602:
        time_of_day = ".svg" # Nessasary since some of the weather icons do not have day/night versions
    elif 6 <= now.hour < 19:  # Day time
        time_of_day = "-day.svg"
    else:  # Night time
        time_of_day = "-night.svg"


    # Get the corresponding icon filename from your mapping
    icon_filename = icon_mapping.get(condition_id) + time_of_day 

    # Extract needed values from data to be returned to the home.html template
    temperature = round(data["current"]["temp"])
    feels_like = round(data["current"]["feels_like"])
    condition = data["current"]["weather"][0]["description"]
    conditions = condition.title()
    
    temp_high = round(data["daily"][0]["temp"]["max"])
    temp_low = round(data["daily"][0]["temp"]["min"])
    humidity = round(data["current"]["humidity"])
    dew_point = round(data["current"]["dew_point"])

    rain_chance = round(data["daily"][0]["pop"]*100)
    wind_speed = round(data["current"]["wind_speed"])
    wind_direction_deg = data["current"]["wind_deg"]
    wind_direction = degrees_to_direction(wind_direction_deg)
    wind_gust = round(data["current"].get("wind_gust", 0))
    visability = (data["current"]["visibility"]) / 1000
 
    return render_template('home.html', temperature = temperature, time = current_time, location = location, feels_like = feels_like,
                           condition = conditions, icon_filename = icon_filename, temp_high = temp_high, temp_low = temp_low, humidity = humidity,
                           dew_point = dew_point, rain_chance = rain_chance, wind_speed = wind_speed, wind_direction = wind_direction, wind_gust = wind_gust,
                           visability = visability)


@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

@app.route('/weather-history')
def weather_history():
    return render_template('weather_history.html')

@app.route('/radar')
def radar():
    return render_template('radar.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
