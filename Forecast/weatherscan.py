# WeatherScan 2.0 - Used to generate text onto a template image, pulling from API

import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Degrees to Cardinal Direction Conversion
def degrees_to_cardinal(degrees):
    """
    Convert degrees to a cardinal direction.
    """
    if 337.5 <= degrees < 360 or 0 <= degrees < 22.5:
        return "North"
    elif 22.5 <= degrees < 67.5:
        return "Northeast"
    elif 67.5 <= degrees < 112.5:
        return "East"
    elif 112.5 <= degrees < 157.5:
        return "Southeast"
    elif 157.5 <= degrees < 202.5:
        return "South"
    elif 202.5 <= degrees < 247.5:
        return "Southwest"
    elif 247.5 <= degrees < 292.5:
        return "West"
    elif 292.5 <= degrees < 337.5:
        return "Northwest"
    else:
        return "Unknown"

# OpenWeatherMap API key and endpoint
api_key = "YOURAPIKEY"
api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
forecast_endpoint = "http://api.openweathermap.org/data/2.5/forecast"
nws_alerts_endpoint = f"https://api.weather.gov/alerts/active/zone/[YOURCOUNTYCODE]"

# Parameters for your location (replace with your coordinates in decimal degrees)
params = {
    'lat': 00.0000,
    'lon': -00.0000,
    'appid': api_key,
    'units': 'imperial'  # Use 'imperial' for Fahrenheit
}



# Location variables for text
location = "YOURLOCATION"
county = "YOURCOUNTY"


# Make API request for Current Conditions
response = requests.get(api_endpoint, params=params)
data = response.json()

# API request for Forecast
results = requests.get(forecast_endpoint, params=params)
dataForecast = results.json()

# API request for Active Alerts
response_alerts = requests.get(nws_alerts_endpoint)
alertsData = response_alerts.json()

# Extract relevant weather information (See OWM API for data you can use)
temp = data['main']['temp']
description = data['weather'][0]['description']
iconCode = data['weather'][0]['icon']
windSpeed = data['wind']['speed']
windDeg = data['wind']['deg']
strPrecipPercent = dataForecast['list'][0]['pop']
feelslike = data['main']['feels_like']

# Extract alert data from NWS API
alerts = alertsData.get('features', [])
alertTitles = [alert.get('properties', {}).get('event', 'Unknown Event') for alert in alerts]

# Print Alert titles if present, if not, print "There are no active alerts" string
if not alertTitles:
    alertText = ("There are no active alerts")
else:
    for title in alertTitles:
        alertText = (title)

# Round to nearest whole number
roundedTemp = round(temp)
roundedWind = round(windSpeed)
roundedFeelsLike = round(feelslike)

precipPercent = int(strPrecipPercent) # Convert decimal to string

convertedRain = precipPercent * 100 # Convert precipPercent from Decimal to Percentage

cardinal_direction = degrees_to_cardinal(windDeg) # Convert Wind Degrees to Cardinal Directions

background_color = (255, 255, 255)  # Specify the RGB values for the background color of icon (white in this example)

# Open a template image
img = Image.open("template_image.jpg")
draw = ImageDraw.Draw(img)

# Choose a different font and font size, used for main body
font_path1 = "/path/to/font.ttf"  # Replace with the path to your font file
font_size1 = 25
font1 = ImageFont.truetype(font_path1, font_size1)

# Choose a different font and font size, used for heading
font_path2 = "/path/to/font.ttf"  # Replace with the path to your font file
font_size2 = 25
font2 = ImageFont.truetype(font_path2, font_size2)

# Font used for alert text at bottom of window
font_path3 = "/path/to/font.ttf"
font_size3 = 20
font3 = ImageFont.truetype(font_path3, font_size3)

max_width = 450 # Set the maximum width for text wrapping

# Wrap the text using the textwrap module
wrappedText = textwrap.fill(f"Right now . . . in {location}, the temperature is {roundedTemp}\u00b0F, under {description}. \
                            Winds {cardinal_direction} at {roundedWind} miles per hour. It currently feels like {roundedFeelsLike}\u00b0F. \
                            Chance of precipitation {convertedRain} percent.", width=30)

wrappedInfo = textwrap.fill(f"Edit this line for your station info", width=35) # Text Wrap for Station Info

wrapped_alerts = textwrap.fill(f"{alertText} for {county}.", width=40) # Text Wrap for Alerts

# Body Text with drop shadow
shadowOffset = 2  # Adjust as needed
draw.text((60 + shadowOffset, 125 + shadowOffset), wrappedText, fill="black", font=font1)
draw.text((60, 125), wrappedText, fill="white", font=font1)

# Station Info text with drop shadow
draw.text((60 + shadowOffset, 330 + shadowOffset), wrappedInfo, fill="black", font=font1)
draw.text((60, 330), wrappedInfo, fill="white", font=font1)

# Title/Header Drop Shadow
draw.text((155 + shadowOffset, 45 + shadowOffset), "Weatherscan 2.0", fill="black", font=font2)
draw.text((155, 45), "Weatherscan 2.0", fill="yellow", font=font2)
draw.text((155 + shadowOffset, 75 + shadowOffset), "for {location}", fill="black", font=font2)
draw.text((155, 75), "for {location}" , fill="yellow", font=font2)

# Text for Alerts
draw.text((50 + shadowOffset, 430 + shadowOffset), wrapped_alerts, fill="black", font=font3)
draw.text((50, 430), wrapped_alerts, fill="white", font=font3)

# Insert the weather icon into the image and resize it
iconURL = f"http://openweathermap.org/img/w/{iconCode}.png"
iconImage = Image.open(requests.get(iconURL, stream=True).raw)

iconImage = iconImage.convert("RGBA") # Create a copy of the icon with an alpha channel

icon_background = Image.new('RGBA', iconImage.size, background_color) # Create a new image with the specified background color

iconWithBack = Image.alpha_composite(icon_background, iconImage) # Paste the icon onto the new image with the specified background color

# Resize the icon to the desired dimensions (e.g., 50x50)
iconSize = (60, 60)
iconBackResize = iconWithBack.resize(iconSize)

# Paste the resized icon onto the template image
img.paste(iconBackResize, (55, 35), iconBackResize)  # Adjust the coordinates based on your template

img.save("output_image.jpg") # Save the modified image

