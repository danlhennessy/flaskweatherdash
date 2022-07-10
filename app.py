import http.client
import json
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request

#Loading .env file
def configure():
    load_dotenv()


#Bringing data from met API
def getweather(lat, long):
    configure()
    conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

    headers = {
        'X-IBM-Client-Id': os.getenv('api_key'),
        'X-IBM-Client-Secret': os.getenv('api_secret'),
        'accept': "application/json"
        }

    conn.request("GET", f"/v0/forecasts/point/three-hourly?excludeParameterMetadata=true&includeLocationName=true&latitude={lat}&longitude={long}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    js = json.loads(data) #Return data as JSON

    #return(data.decode("utf-8")) Uncomment this for original data return
    return js

#Flask app section
app = Flask(__name__)

@app.route('/')
def weather_dash():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render():
    latitude = request.form['latitude'] # Takes user input from form on home.html
    longitude = request.form['longitude'] #The action from the form takes us from site/ to site/results
    data = getweather(latitude, longitude)
    location = data["features"][0]["properties"]["location"]["name"]
    timeSeries0 = data["features"][0]["properties"]["timeSeries"][0]
    #Pick up her next and narrow down data further
    mintemp0 = timeSeries0["minScreenAirTemp"]
    maxtemp0 = timeSeries0["maxScreenAirTemp"]
    windspeed0 = timeSeries0["windSpeed10m"]
    rain0 = timeSeries0["probOfRain"]
    return render_template('results.html', location = location, mintemp0 = mintemp0, maxtemp0 = maxtemp0, windspeed0 = windspeed0, rain0 = rain0)

if __name__ == '__main__':
    app.run()



    